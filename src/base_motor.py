import time

MODE_IDLE = 0x00
MODE_MOTOR_ON = 0x01
MODE_BRAKE = 0x02
MODE_REGULATED = 0x04

REGULATION_IDLE = 0x00
REGULATION_MOTOR_SPEED = 0x01
REGULATION_MOTOR_SYNC = 0x02

RUN_STATE_IDLE = 0x00
RUN_STATE_RAMP_UP = 0x10
RUN_STATE_RUNNING = 0x20
RUN_STATE_RAMP_DOWN = 0x40

LIMIT_RUN_FOREVER = 0

class BlockedException(Exception):
    pass


class BaseMotor(object):
    """Base class for motors"""
    debug = 0
    def _debug_out(self, message):
        if self.debug:
            print message

    def turn(self, power, tacho_units, brake=True, timeout=1, emulate=True):
        """Use this to turn a motor. The motor will not stop until it turns the
        desired distance. Accuracy is much better over a USB connection than
        with bluetooth...
        power is a value between -127 and 128 (an absolute value greater than
                 64 is recommended)
        tacho_units is the number of degrees to turn the motor. values smaller
                 than 50 are not recommended and may have strange results.
        brake is whether or not to hold the motor after the function exits
                 (either by reaching the distance or throwing an exception).
        timeout is the number of seconds after which a BlockedException is
                 raised if the motor doesn't turn
        emulate is a boolean value. If set to False, the motor is aware of the
                 tacho limit. If True, a run() function equivalent is used.
                 Warning: motors remember their positions and not using emulate
                 may lead to strange behavior, especially with synced motors
        """

        tacho_limit = tacho_units

        if tacho_limit < 0:
            raise ValueError, "tacho_units must be greater than 0!"
        #TODO Calibrate the new values for ip socket latency.
        if self.method == 'bluetooth':
            threshold = 70
        elif self.method == 'usb':
            threshold = 5
        elif self.method == 'ipbluetooth':
            threshold = 80
        elif self.method == 'ipusb':
            threshold = 15
        else:
            threshold = 30 #compromise

        tacho = self.get_tacho()
        state = self._get_new_state()

        # Update modifiers even if they aren't used, might have been changed
        state.power = power
        if not emulate:
            state.tacho_limit = tacho_limit

        self._debug_out('Updating motor information...')
        self._set_state(state)

        direction = 1 if power > 0 else -1
        self._debug_out('tachocount: ' + str(tacho))
        current_time = time.time()
        tacho_target = tacho.get_target(tacho_limit, direction)

        blocked = False
        try:
            while True:
                time.sleep(self._eta(tacho, tacho_target, power) / 2)

                if not blocked: # if still blocked, don't reset the counter
                    last_tacho = tacho
                    last_time = current_time

                tacho = self.get_tacho()
                current_time = time.time()
                blocked = self._is_blocked(tacho, last_tacho, direction)
                if blocked:
                    self._debug_out(('not advancing', last_tacho, tacho))
                    # the motor can be up to 80+ degrees in either direction from target when using bluetooth
                    if current_time - last_time > timeout:
                        if tacho.is_near(tacho_target, threshold):
                            break
                        else:
                            raise BlockedException("Blocked!")
                else:
                    self._debug_out(('advancing', last_tacho, tacho))
                if tacho.is_near(tacho_target, threshold) or tacho.is_greater(tacho_target, direction):
                    break
        finally:
            if brake:
                self.brake()
            else:
                self.idle()
