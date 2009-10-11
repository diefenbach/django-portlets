# django imports
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

class Portlet(models.Model):
    """Base portlet. All portlets should inherit from this class.
    """
    title = models.CharField(blank=True, max_length=100)

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
    slot = models.ForeignKey("Slot")

    content_type = models.ForeignKey(ContentType, related_name="pa_content")
    content_id = models.PositiveIntegerField()
    content = generic.GenericForeignKey('content_type', 'content_id')

    portlet_type = models.ForeignKey(ContentType, related_name="pa_portlets")
    portlet_id = models.PositiveIntegerField()
    portlet = generic.GenericForeignKey('portlet_type', 'portlet_id')

    position = models.PositiveSmallIntegerField(default=999)

    class Meta:
        ordering = ["position"]
        verbose_name_plural = "Portlet assignments"

    def __unicode__(self):
        try:
            return "%s (%s)" % (self.portlet.title, self.slot.name)
        except AttributeError:
            return ""

class PortletBlocking(models.Model):
    """Blocks portlets for given slot and content object.
    """
    slot = models.ForeignKey("Slot")

    content_type = models.ForeignKey(ContentType, related_name="pb_content")
    content_id = models.PositiveIntegerField()
    content = generic.GenericForeignKey('content_type', 'content_id')

    class Meta:
        unique_together = ["slot", "content_id", "content_type"]

    def __unicode__(self):
        try:
            return "%s (%s)" % (self.content.title, self.slot.name)
        except AttributeError:
            return ""

class PortletRegistration(models.Model):
    """Registered portlets. These are provided to be added to customer.

    Parameters:

        * type:
            The type of the portlet. This must be the exactly class name of
            the portlet, e.g. TextPortlet

        * name
            The name of the portlet. This is displayed to the user.
            
        * active
            If true the portlet will be provided to assign to content object
     """
    type = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name", )

    def __unicode__(self):
        return "%s %s" % (self.type, self.name)


class Slot(models.Model):
    """Slots are places to which portlets can be assigned.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name