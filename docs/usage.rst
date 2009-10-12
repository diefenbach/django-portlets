Usage
=====

In order to use django portlets you first have to implement a portlet. This is 
done by inheriting from the provided base class, for instance:

Create a portlet
----------------

Let's create a simple text portlet::

    # django imports
    from django import forms
    from django.db import models
    from django.template.loader import render_to_string
    from django.utils.translation import ugettext_lazy as _

    from portlets.models import Portlet

    class TextPortlet(Portlet):
        """A simple portlet to display some text.
        """
        text = models.TextField(_(u"Text"), blank=True)

        def __unicode__(self):
            return "%s" % self.id

        def render(self, context):
            """Renders the portlet as html.
            """
            return render_to_string("portlets/text_portlet.html", {
                "title" : self.title,
                "text" : self.text
            })

        def form(self, **kwargs):
            """
            """
            return TextPortletForm(instance=self, **kwargs)

    class TextPortletForm(forms.ModelForm):
        """Form for the TextPortlet.
        """
        class Meta:
            model = TextPortlet

Register the portlet
--------------------

In order to make it available for selection, the portlet has to be registered 
(make sure that this is called, when django starts up)::

    from portlets.utils import register_portlet
    register_portlet(TextPortlet, "TextPortlet")

To display portlets within your templates, just use the provided portlet_slot 
tag, e.g.::

   {% load portlets_tags %}
   
   <table>
        <tr>
            <td>
                {% portlet_slot 'Left' flatpage %}
            </td>
            <td>
                Content goes here.
            </td>
            <td>
                {% portlet_slot 'Right' flatpage %}
            </td>
        </tr>
   </table>

Assign the portlet to content
-----------------------------

Now go to the admin interface and add a Slot, e.g. "Left" and a TextPortlet 
(assuming you have it registered for the django's admin application). Now you 
can assign the portlet (via PortletAssignment) to any content object.