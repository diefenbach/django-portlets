# django imports
from django import template
from django.conf import settings
from django.core.cache import cache

# portlets imports
from portlets.models import Slot

register = template.Library()


@register.inclusion_tag('portlets/portlet_slot.html', takes_context=True)
def portlet_slot(context, slot_name, instance=None):
    """
    Returns the portlets for given slot and instance. If the instance implements
    the ``get_parent_for_portlets`` method the portlets of the parent of the
    instance are also added.
    """
    request = context.get("request")

    # CACHE
    content_type = instance.__class__.__name__.lower()
    cache_key = "%s-portlets-%s-%s-%s-%s-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,
        content_type, instance.id, slot_name, request.user.id, context.get("CURRENT_LANGUAGE"))

    rendered_portlets = cache.get(cache_key)

    if rendered_portlets:
        return {"portlets": rendered_portlets}

    if instance is None:
        return {"portlets": []}

    try:
        slot = Slot.objects.get(name=slot_name)
    except Slot.DoesNotExist:
        return {"portlets": []}

    # Get portlets for given instance
    temp = slot.get_portlets(instance)

    # Get inherited portlets
    try:
        instance.get_parent_for_portlets()
    except AttributeError:
        instance = None

    while instance:
        # If the portlets are blocked no portlets should be added
        if slot.is_blocked(instance):
            break

        # If the instance has no get_parent_for_portlets, there are no portlets
        try:
            instance = instance.get_parent_for_portlets()
        except AttributeError:
            break

        # If there is no parent for portlets, there are no portlets to add
        if instance is None:
            break

        parent_portlets = slot.get_portlets(instance)
        parent_portlets.reverse()
        for p in parent_portlets:
            if p not in temp:
                temp.insert(0, p)

    rendered_portlets = []
    for portlet in temp:
        rendered_portlets.append(portlet.render(context))

    cache.set(cache_key, rendered_portlets)

    return {"portlets": rendered_portlets}
