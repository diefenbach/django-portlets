# django imports
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Portlet(models.Model):
    """Base portlet. All portlets should inherit from this class.
    """
    title = models.CharField(_(u"Title"), blank=True, max_length=100)

    class Meta:
        abstract = True

    def render(self):
        """Renders the portlet as html. Have to be implemented by sub classes.
        """
        raise NotImplemented

    def form(self, **kwargs):
        """returns the form for the portlet. Have to be implemented by sub
        classes.
        """
        raise NotImplemented


class PortletAssignment(models.Model):
    """Assigns portlets to slots and content.
    """
    slot = models.ForeignKey("Slot", verbose_name=_(u"Slot"))

    content_type = models.ForeignKey(ContentType, related_name="pa_content")
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')

    portlet_type = models.ForeignKey(ContentType, related_name="pa_portlets")
    portlet_id = models.PositiveIntegerField()
    portlet = GenericForeignKey('portlet_type', 'portlet_id')

    position = models.PositiveSmallIntegerField(_("Position"), default=999)

    class Meta:
        app_label = "portlets"
        ordering = ["position"]
        verbose_name_plural = _(u"Portlet assignments")

    def __unicode__(self):
        try:
            return "%s (%s)" % (self.portlet.title, self.slot.name)
        except AttributeError:
            return ""


class PortletBlocking(models.Model):
    """Blocks portlets for given slot and content object.
    """
    slot = models.ForeignKey("Slot", verbose_name=_(u"Slot"))

    content_type = models.ForeignKey(ContentType, related_name="pb_content")
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')

    class Meta:
        app_label = "portlets"
        unique_together = ["slot", "content_id", "content_type"]

    def __unicode__(self):
        try:
            return "%s (%s)" % (self.content.title, self.slot.name)
        except AttributeError:
            return ""


class PortletRegistration(models.Model):
    """
    Registered portlets. These are provided to be added to customer.

    Parameters:

        * type:
            The type of the portlet. This must be the exactly class name of
            the portlet, e.g. TextPortlet

        * name
            The name of the portlet. This is displayed to the user.

        * active
            If true the portlet will be provided to assign to content object
     """
    type = models.CharField(_(u"Type"), max_length=30, unique=True)
    name = models.CharField(_(u"Name"), max_length=50, unique=True)
    active = models.BooleanField(_(u"Active"), default=True)

    class Meta:
        app_label = "portlets"
        ordering = ("name", )

    def __unicode__(self):
        return "%s %s" % (self.type, self.name)


class Slot(models.Model):
    """
    Slots are places to which portlets can be assigned.
    """
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        app_label = "portlets"

    def __unicode__(self):
        return self.name

    def get_portlets(self, obj):
        """
        Returns portlet objs for a given slot and obj (content object).

        **Parameters**

        obj
            The object for the portlets should be returned. Must be a Django model
            instance.
        """
        ctype = ContentType.objects.get_for_model(obj)
        portlet_assignments = PortletAssignment.objects.filter(
            slot=self, content_type=ctype.id, content_id=obj.id).order_by("position")

        portlets = []
        for portlet_assignment in portlet_assignments:
            portlets.append(portlet_assignment.portlet)

        return portlets

    def has_portlets(self, obj):
        """
        Returns True if the passed object has portlets for passed slot.

        **Parameters:**

            obj
                The object which is tested. Must be a Django model instance.
        """
        while obj:
            if len(self.get_portlets(obj)) > 0:
                return True
            if self.is_blocked(obj):
                break
            try:
                obj = obj.get_parent_for_portlets()
            except AttributeError:
                break

        return False

    def is_blocked(self, obj):
        """
        Returns True if the passed slot is blocked for the passed object.
        Otherwise False.

        **Parameters:**

            slot
                The slot for which the blocking is tested. Must be a Slot
                instance.
        """
        ct = ContentType.objects.get_for_model(obj)
        try:
            PortletBlocking.objects.get(slot=self, content_type=ct.id, content_id=obj.id)
        except PortletBlocking.DoesNotExist:
            return False
        else:
            return True
