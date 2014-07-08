# django imports
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# portlets imports
from portlets.models import PortletAssignment
from portlets.models import PortletBlocking
from portlets.models import PortletRegistration
from portlets.models import Slot

# Load logger
import logging
logger = logging.getLogger(__name__)


def get_slots(obj):
    """Returns all slots with all assigned portlets for the passed object.

    **Parameters:**

        obj
            The obj for which the slots should be returned.
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
                    "pa_id": pa.id,
                    "title": pa.portlet.title,
                    "type": portlet_types.get(pa.portlet.__class__.__name__.lower(), ""),
                })

        items.append({
            "id": slot.id,
            "name": slot.name,
            "is_blocked": slot.is_blocked(obj),
            "portlets": temp,
        })

    return {
        "has_portlets": has_portlets,
        "items": items
    }


# DEPRECATED 1.2
def is_blocked(obj, slot):
    """
    Returns True if the passed slot is blocked for the passed object.
    Otherwise False.

    **Parameters:**

        obj
            The object for which the blocking is tested. Must be a Django
            model instance.

        slot
            The slot for which the blocking is tested. Must be a Slot
            instance.
    """
    logger.info("Decprecated: portlets: the utility function 'is_blocked' is deprecated. Please use 'Slot.is_blocked'.")
    return slot.is_blocked(obj)


# DEPRECATED 1.2
def has_portlets(obj, slot):
    """Returns True if the passed object has portlets for passed slot.

    **Parameters:**

        obj
            The object which is tested. Must be a Django model instance.

        slot
            The slot which is tested. Must be a Slot instance.
    """
    logger.info("Decprecated: portlets: the utility function 'has_portlets' is deprecated. Please use 'Slot.has_portlets'.")
    return slot.has_portlets(obj)


# DEPRECATED 1.2
def get_portlets(obj, slot):
    """Returns portlet objs for a given slot and obj (content object).

    **Parameters**

    slot
        The slot for which the portlets should be returned. Must be a Slot
        instance.

    obj
        The object for the portlets should be returned. Must be a Django model
        instance.

    """
    logger.info("Decprecated: portlets: the utility function 'get_portlets' is deprecated. Please use 'Slot.get_portlets'.")
    return slot.get_portlets(obj)


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
