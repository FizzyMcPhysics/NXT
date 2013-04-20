class TachoInfo:
    """An object containing the information about the rotation of a motor"""
    def __init__(self, values):
        self.tacho_count, self.block_tacho_count, self.rotation_count = values

    def get_target(self, tacho_limit, direction):
        """Returns a TachoInfo object which corresponds to tacho state after
        moving for tacho_limit ticks. Direction can be 1 (add) or -1 (subtract)
        """
        # TODO: adjust other fields
        if abs(direction) != 1:
            raise ValueError('Invalid direction')
        new_tacho = self.tacho_count + direction * tacho_limit
        return TachoInfo([new_tacho, None, None])

    def is_greater(self, target, direction):
        return direction * (self.tacho_count - target.tacho_count) > 0

    def is_near(self, target, threshold):
        difference = abs(target.tacho_count - self.tacho_count)
        return difference < threshold

    def __str__(self):
        return str((self.tacho_count, self.block_tacho_count,
                   self.rotation_count))
