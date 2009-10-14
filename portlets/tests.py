# django imports
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

# reviews imports
import portlets.example.models
import portlets.models
import portlets.utils

class DummySession(object):
    session_key = "42"

class DummyRequest(object):
    def __init__(self, method="POST", user=None):
        self.user = user
        self.method = method
        self.session = DummySession()

class UtilsTestCase(TestCase):
    """Tests the methods of utils.py
    """
    def setUp(self):
        """
        """
        # Create a page which server as content
        self.page = FlatPage.objects.create(url="/test/", title="Test")

        # Create a portlet
        self.portlet = portlets.example.models.TextPortlet.objects.create(title="Text")

        # Create some slots
        self.left_slot = portlets.models.Slot.objects.create(name="Left")
        self.right_slot = portlets.models.Slot.objects.create(name="Right")

    def test_get_slots(self):
        """
        """
        # At the beginning no slot has portlets
        slots = portlets.utils.get_slots(self.page)
        self.assertEqual(slots["has_portlets"], False)
        self.assertEqual(slots["items"][0]["name"], "Left")
        self.assertEqual(slots["items"][0]["portlets"], [])
        self.assertEqual(slots["items"][1]["name"], "Right")
        self.assertEqual(slots["items"][1]["portlets"], [])

        # Assigning the text portlet to the left slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=self.portlet, position=1)

        slots = portlets.utils.get_slots(self.page)
        self.assertEqual(slots["has_portlets"], True)
        self.assertEqual(slots["items"][0]["name"], "Left")
        self.assertEqual(slots["items"][0]["portlets"][0]["title"], "Text")
        self.assertEqual(slots["items"][1]["name"], "Right")
        self.assertEqual(slots["items"][1]["portlets"], [])

        # Create another portlet ...
        portlet_2 = portlets.example.models.TextPortlet.objects.create(title="Text 2")

        # ... and assign it also to the left slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=portlet_2, position=2)

        slots = portlets.utils.get_slots(self.page)
        self.assertEqual(slots["has_portlets"], True)
        self.assertEqual(slots["items"][0]["name"], "Left")
        self.assertEqual(slots["items"][0]["portlets"][0]["title"], "Text")
        self.assertEqual(slots["items"][0]["portlets"][1]["title"], "Text 2")
        self.assertEqual(slots["items"][1]["name"], "Right")
        self.assertEqual(slots["items"][1]["portlets"], [])

        # Create another portlet ...
        portlet_3 = portlets.example.models.TextPortlet.objects.create(title="Text 3")

        # ... and assign it the right slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.right_slot, content=self.page, portlet=portlet_3, position=1)

        slots = portlets.utils.get_slots(self.page)
        self.assertEqual(slots["has_portlets"], True)
        self.assertEqual(slots["items"][0]["name"], "Left")
        self.assertEqual(slots["items"][0]["portlets"][0]["title"], "Text")
        self.assertEqual(slots["items"][0]["portlets"][1]["title"], "Text 2")
        self.assertEqual(slots["items"][1]["name"], "Right")
        self.assertEqual(slots["items"][1]["portlets"][0]["title"], "Text 3")

    def test_has_portlets(self):
        """
        """
        # At the beginning no slot has portlets
        result = portlets.utils.has_portlets(self.left_slot, self.page)
        self.assertEqual(result, False)

        result = portlets.utils.has_portlets(self.right_slot, self.page)
        self.assertEqual(result, False)

        # Assigning the text portlet to the left slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=self.portlet, position=1)

        result = portlets.utils.has_portlets(self.left_slot, self.page)
        self.assertEqual(result, True)

        result = portlets.utils.has_portlets(self.right_slot, self.page)
        self.assertEqual(result, False)

        # Assigning the text portlet to the right slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.right_slot, content=self.page, portlet=self.portlet, position=1)

        result = portlets.utils.has_portlets(self.left_slot, self.page)
        self.assertEqual(result, True)

        result = portlets.utils.has_portlets(self.right_slot, self.page)
        self.assertEqual(result, True)

    def test_register_portlets(self):
        """
        """
        # At the beginning no portlets are registered
        result = portlets.utils.get_registered_portlets()
        self.assertEqual(result, {})

        # Register the TextPortlet
        portlets.utils.register_portlet(portlets.example.models.TextPortlet, "TextPortlet")
        result = portlets.utils.get_registered_portlets()
        self.assertEqual(result, {u"textportlet" : u"TextPortlet"})

        # Unregister the TextPortlet
        portlets.utils.unregister_portlet(portlets.example.models.TextPortlet)
        result = portlets.utils.get_registered_portlets()
        self.assertEqual(result, {})

    def test_is_blocked(self):
        """
        """
        # Assigning the text portlet to the left slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=self.portlet, position=1)

        # Assigning the text portlet to the left slot of the page
        portlets.models.PortletAssignment.objects.create(
            slot=self.right_slot, content=self.page, portlet=self.portlet, position=1)

        result = portlets.utils.is_blocked(self.page, self.left_slot)
        self.assertEqual(result, False)

        result = portlets.utils.is_blocked(self.page, self.right_slot)
        self.assertEqual(result, False)
        
        # Blocking the left slot of the page
        portlets.models.PortletBlocking.objects.create(slot=self.left_slot, content=self.page)

        result = portlets.utils.is_blocked(self.page, self.left_slot)
        self.assertEqual(result, True)

        result = portlets.utils.is_blocked(self.page, self.right_slot)
        self.assertEqual(result, False)

        # Blocking the left right of the page
        portlets.models.PortletBlocking.objects.create(slot=self.right_slot, content=self.page)

        result = portlets.utils.is_blocked(self.page, self.left_slot)
        self.assertEqual(result, True)

        result = portlets.utils.is_blocked(self.page, self.right_slot)
        self.assertEqual(result, True)
        