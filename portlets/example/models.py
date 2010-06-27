# django imports
from django import forms
from django.db import models
from django.db.models.signals import post_syncdb
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# portlets imports
import portlets
from portlets.models import Portlet
from portlets.utils import register_portlet

class TextPortlet(Portlet):
    """A simple portlet to display some text.
    """
    text = models.TextField(_(u"Text"), blank=True)

    def __unicode__(self):
        return "%s" % self.id

    def render(self, context=None):
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