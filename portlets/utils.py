# django imports
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# portlets imports
from portlets.models import PortletAssignment
from portlets.models import PortletBlocking
from portlets.models import PortletRegistration
from portlets.models import Slot

def get_slots(obj):
    """Returns slot with all assigned portlets as dict.
    """
    portlet_types = get_registered_portlets()
    ct = ContentType.objects.get_for_model(obj)

    # Stores whether at least one slot has at least one portlet.
    has_portlets = False

    items = []
    for slot in Slot.objects.all():
        temp = []
        for pa in PortletAssignment.objects.filter(
            slot=slot, content_id=obj.id, content_type=ct.id):
            has_portlets = True

            # Display only registered portlets
            portlet_type = portlet_types.get(pa.portlet.__class__.__name__.lower())
            if portlet_type:
                temp.append({
                    "pa_id" : pa.id,
                    "title" : pa.portlet.title,
                    "type" : portlet_types.get(pa.portlet.__class__.__name__.lower(), ""),
                })

        items.append({
            "id"   : slot.id,
            "name" : slot.name,
            "is_blocked" : is_blocked(obj, slot),
            "portlets" : temp,
        })

    return {
        "has_portlets" : has_portlets,
        "items" : items
    }

def is_blocked(obj, slot):
    """Returns True if for the given object the given slot is blocked.
    """
    ct = ContentType.objects.get_for_model(obj)
    try:
        pb = PortletBlocking.objects.get(
            slot=slot, content_type=ct.id, content_id=obj.id)
    except PortletBlocking.DoesNotExist:
        return False

    return True

def has_portlets(slot, obj):
    """Returns True if the given obj has portlets for given slot.
    """
    while obj:
        if len(get_portlets(slot, obj)) > 0:
            return True
        if is_blocked(obj, slot):
            break
        try:
            obj = obj.get_parent_for_portlets()
        except AttributeError:
            break

    return False

def get_portlets(slot, obj):
    """Returns portlet objs for a given slot and obj (content object).
    
    **Parameters**
    
    slot
        The slot for which the portlets should be returned. Must be a Slot 
        instance.
        
    obj
        The object for the portlets should be returned. Must be a Django model.
        
    """
    ctype = ContentType.objects.get_for_model(obj)
    try:
        slot = Slot.objects.get(id=slot.id)
    except ObjectDoesNotExist:
        portlet_assignments = []
    else:
        portlet_assignments = PortletAssignment.objects.filter(
            slot=slot, content_type=ctype.id, content_id=obj.id).order_by("position")

    portlets = []
    for portlet_assignment in portlet_assignments:
        portlets.append(portlet_assignment.portlet)

    return portlets

def get_registered_portlets():
    """Returns registered portlet types as dict.
    """
    portlet_types = {}
    for pr in PortletRegistration.objects.all():
        portlet_types[pr.type] = pr.name

    return portlet_types

def register_portlet(klass, name):
    """Registers a portlet. Name and klass must both be unique.
    
    **Parameters**
    
    klass
        The portlet's python class
        
    name
        Then unique name under which the portlet is registered
    """
    type = klass.__name__.lower()
    if not PortletRegistration.objects.filter(Q(type=type) | Q(name=name)):
        PortletRegistration.objects.create(type=type, name=name)

def unregister_portlet(klass):
    """Unregisters portlet the passed portlet.

    **Parameters**
    
    klass
        The portlet's python class
    """
    type = klass.__name__.lower()
    try:
        pr = PortletRegistration.objects.get(type=type)
    except PortletRegistration.DoesNotExist:
        pass
    else:
        pr.delete()