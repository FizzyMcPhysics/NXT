class SynchronizedTacho(object):
    def __init__(self, leader_tacho, follower_tacho):
        self.leader_tacho = leader_tacho
        self.follower_tacho = follower_tacho

    def get_target(self, tacho_limit, direction):
        """This method will leave follower's target as None"""
        leader_tacho = self.leader_tacho.get_target(tacho_limit, direction)
        return SynchronizedTacho(leader_tacho, None)

    def is_greater(self, other, direction):
        return self.leader_tacho.is_greater(other.leader_tacho, direction)

    def is_near(self, other, threshold):
        return self.leader_tacho.is_near(other.leader_tacho, threshold)

    def __str__(self):
        if self.follower_tacho is not None:
            t2 = str(self.follower_tacho.tacho_count)
        else:
            t2 = 'None'
        t1 = str(self.leader_tacho.tacho_count)
        return 'tacho: ' + t1 + ' ' + t2