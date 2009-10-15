# django imports
from django.contrib.flatpages.models import FlatPage
from django.db import IntegrityError
from django.test import TestCase

# reviews imports
from portlets.example.models import TextPortlet
from portlets.models import PortletAssignment
from portlets.models import PortletBlocking
from portlets.models import PortletRegistration
from portlets.models import Slot
import portlets.utils

class PortletsModelsTestCase(TestCase):
    """Tests the models
    """
    def test_portlet(self):
        """
        """
        text_portlet = TextPortlet.objects.create(title="Text")
        self.assertEqual(text_portlet.title, "Text")
        self.failIf(text_portlet.render().find("portlet-header") == -1)
        self.failIf(text_portlet.form().as_p().find('id="id_title"') == -1)

    def test_slot(self):
        """
        """
        slot = Slot.objects.create(name="Left")
        self.assertEqual(slot.name, "Left")

    def test_portlet_registration(self):
        """
        """
        portlet_registration = PortletRegistration.objects.create(
            type = "textportlet",
            name = "TextPortlet",
        )

        self.assertEqual(portlet_registration.type, "textportlet")
        self.assertEqual(portlet_registration.name, "TextPortlet")
        self.assertEqual(portlet_registration.active, True)

        # try to add another portlet with same type or name
        self.assertRaises(IntegrityError, PortletRegistration.objects.create, type = "textportlet")
        self.assertRaises(IntegrityError, PortletRegistration.objects.create, name = "TextPortlet")

        # add another portlet with other name
        portlet_registration_2 = PortletRegistration.objects.create(
            type = "textportlet_2",
            name = "TextPortlet_2",
        )

    def test_portlet_assignment(self):
        """
        """
        slot = Slot.objects.create(name="Left")
        page = FlatPage.objects.create(url="/test/", title="Test")
        portlet = TextPortlet.objects.create(title="Text")

        portlet_assignment = PortletAssignment.objects.create(
            slot = slot,
            content = page,
            portlet = portlet,
        )

        self.assertEqual(portlet_assignment.slot, slot)
        self.assertEqual(portlet_assignment.content, page)
        self.assertEqual(portlet_assignment.portlet, portlet)

    def test_portlet_blocking(self):
        """
        """
        slot = Slot.objects.create(name="Left")
        page = FlatPage.objects.create(url="/test/", title="Test")

        portlet_blocking = PortletBlocking.objects.create(
            slot = slot,
            content = page,
        )

        self.assertEqual(portlet_blocking.slot, slot)
        self.assertEqual(portlet_blocking.content, page)

class PortletsUtilsTestCase(TestCase):
    """Tests the methods of utils.py
    """
    def setUp(self):
        """
        """
        # Create a page which server as content
        self.page = FlatPage.objects.create(url="/test/", title="Test")

        # Create a portlet
        self.portlet = TextPortlet.objects.create(title="Text")

        # Create some slots
        self.left_slot = Slot.objects.create(name="Left")
        self.right_slot = Slot.objects.create(name="Right")

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
        PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=self.portlet, position=1)

        slots = portlets.utils.get_slots(self.page)
        self.assertEqual(slots["has_portlets"], True)
        self.assertEqual(slots["items"][0]["name"], "Left")
        self.assertEqual(slots["items"][0]["portlets"][0]["title"], "Text")
        self.assertEqual(slots["items"][1]["name"], "Right")
        self.assertEqual(slots["items"][1]["portlets"], [])

        # Create another portlet ...
        portlet_2 = TextPortlet.objects.create(title="Text 2")

        # ... and assign it also to the left slot of the page
        PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=portlet_2, position=2)

        slots = portlets.utils.get_slots(self.page)
        self.assertEqual(slots["has_portlets"], True)
        self.assertEqual(slots["items"][0]["name"], "Left")
        self.assertEqual(slots["items"][0]["portlets"][0]["title"], "Text")
        self.assertEqual(slots["items"][0]["portlets"][1]["title"], "Text 2")
        self.assertEqual(slots["items"][1]["name"], "Right")
        self.assertEqual(slots["items"][1]["portlets"], [])

        # Create another portlet ...
        portlet_3 = TextPortlet.objects.create(title="Text 3")

        # ... and assign it the right slot of the page
        PortletAssignment.objects.create(
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
        PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=self.portlet, position=1)

        result = portlets.utils.has_portlets(self.left_slot, self.page)
        self.assertEqual(result, True)

        result = portlets.utils.has_portlets(self.right_slot, self.page)
        self.assertEqual(result, False)

        # Assigning the text portlet to the right slot of the page
        PortletAssignment.objects.create(
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
        portlets.utils.register_portlet(TextPortlet, "TextPortlet")
        result = portlets.utils.get_registered_portlets()
        self.assertEqual(result, {u"textportlet" : u"TextPortlet"})

        # Unregister the TextPortlet
        portlets.utils.unregister_portlet(TextPortlet)
        result = portlets.utils.get_registered_portlets()
        self.assertEqual(result, {})

    def test_is_blocked(self):
        """
        """
        # Assigning the text portlet to the left slot of the page
        PortletAssignment.objects.create(
            slot=self.left_slot, content=self.page, portlet=self.portlet, position=1)

        # Assigning the text portlet to the left slot of the page
        PortletAssignment.objects.create(
            slot=self.right_slot, content=self.page, portlet=self.portlet, position=1)

        result = portlets.utils.is_blocked(self.page, self.left_slot)
        self.assertEqual(result, False)

        result = portlets.utils.is_blocked(self.page, self.right_slot)
        self.assertEqual(result, False)

        # Blocking the left slot of the page
        PortletBlocking.objects.create(slot=self.left_slot, content=self.page)

        result = portlets.utils.is_blocked(self.page, self.left_slot)
        self.assertEqual(result, True)

        result = portlets.utils.is_blocked(self.page, self.right_slot)
        self.assertEqual(result, False)

        # Blocking the left right of the page
        PortletBlocking.objects.create(slot=self.right_slot, content=self.page)

        result = portlets.utils.is_blocked(self.page, self.left_slot)
        self.assertEqual(result, True)

        result = portlets.utils.is_blocked(self.page, self.right_slot)
        self.assertEqual(result, True)
