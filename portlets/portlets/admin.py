from django.contrib import admin

from portlets.models import PortletAssignment
from portlets.models import PortletBlocking
from portlets.models import PortletRegistration
from portlets.models import Slot

admin.site.register(PortletAssignment)
admin.site.register(PortletRegistration)
admin.site.register(PortletBlocking)
admin.site.register(Slot)