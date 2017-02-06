class PortletsBase(object):
    """Mixin class to make objects portlets aware.
    """
    def get_portlets(self, slot):
        """Returns True if the passed slot is blocked. Otherwise False.

        **Parameters:**

            slot
                The slot for which the blocking is tested. Must be a Slot
                instance.
        """
        return slot.get_portlets(self)

    def get_slots(self):
        """Returns all slots with all assigned portlets.
        """
        import portlets.utils
        return portlets.utils.get_slots(self)

    def has_portlets(self, slot):
        """Returns True if the ther are portlets for the passed slot.

        **Parameters:**

            slot
                The slot which is tested. Must be a Slot instance.
        """
        return slot.has_portlets(self)

    def is_blocked(self, slot):
        """Returns True if the passed slot is blocked. Otherwise False.

        **Parameters:**

            slot
                The slot for which the blocking is tested. Must be a Slot
                instance.
        """
        return slot.is_blocked(self)

    def get_parent_for_portlets(self):
        """Returns the parent from which portlets are inherited.
        """
        return None
