
class SynchronizedMotors(BaseMotor):
    """The object used to make two motors run in sync. Many objects may be
    present at the same time but they can't be used at the same time.
    Warning! Movement methods reset tacho counter.
    THIS CODE IS EXPERIMENTAL!!!
    """
    def __init__(self, leader, follower, turn_ratio):
        """Turn ratio can be >= 0 only! If you want to have it reversed,
        change motor order.
        """
        if follower.brick != leader.brick:
            raise ValueError('motors belong to different bricks')
        self.leader = leader
        self.follower = follower
        self.method = self.leader.method #being from the same brick, they both have the same com method.

        if turn_ratio < 0:
            raise ValueError('Turn ratio <0. Change motor order instead!')

        if self.leader.port == self.follower.port:
            raise ValueError("The same motor passed twice")
        elif self.leader.port > self.follower.port:
            self.turn_ratio = turn_ratio
        else:
            self._debug_out('reversed')
            self.turn_ratio = -turn_ratio

    def _get_new_state(self):
        return self.leader._get_new_state()

    def _set_state(self, state):
        self.leader._set_state(state)
        self.follower._set_state(state)

    def get_tacho(self):
        leadertacho = self.leader.get_tacho()
        followertacho = self.follower.get_tacho()
        return SynchronizedTacho(leadertacho, followertacho)

    def reset_position(self, relative):
        """Resets the counters. Relative can be True or False"""
        self.leader.reset_position(relative)
        self.follower.reset_position(relative)

    def _enable(self): # This works as expected. I'm not sure why.
        #self._disable()
        self.reset_position(True)
        self.leader.sync = True
        self.follower.sync = True
        self.leader.turn_ratio = self.turn_ratio
        self.follower.turn_ratio = self.turn_ratio

    def _disable(self): # This works as expected. (tacho is reset ok)
        self.leader.sync = False
        self.follower.sync = False
        #self.reset_position(True)
        self.leader.idle()
        self.follower.idle()
        #self.reset_position(True)

    def run(self, power=100):
        """Warning! After calling this method, make sure to call idle. The
        motors are reported to behave wildly otherwise.
        """
        self._enable()
        self.leader.run(power, True)
        self.follower.run(power, True)

    def brake(self):
        self._disable() # reset the counters
        self._enable()
        self.leader.brake() # brake both motors at the same time
        self.follower.brake()
        self._disable() # now brake as usual
        self.leader.brake()
        self.follower.brake()

    def idle(self):
        self._disable()

    def turn(self, power, tacho_units, brake=True, timeout=1):
        self._enable()
        # non-emulation is a nightmare, tacho is being counted differently
        try:
            if power < 0:
                self.leader, self.follower = self.follower, self.leader
            BaseMotor.turn(self, power, tacho_units, brake, timeout, emulate=True)
        finally:
            if power < 0:
                self.leader, self.follower = self.follower, self.leader

    def _eta(self, tacho, target, power):
        return self.leader._eta(tacho.leader_tacho, target.leader_tacho, power)

    def _is_blocked(self, tacho, last_tacho, direction):
        # no need to check both, they're synced
        return self.leader._is_blocked(tacho.leader_tacho, last_tacho.leader_tacho, direction)
