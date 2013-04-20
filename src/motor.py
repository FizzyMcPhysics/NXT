from base_motor import *
from output_state import OutputState
from tacho_info import TachoInfo

PORT_A = 0x00
PORT_B = 0x01
PORT_C = 0x02
PORT_ALL = 0xFF

def get_tacho_and_state(values):
    """A convenience function. values is the list of values from
        get_output_state. Returns both OutputState and TachoInfo.
    """
    return OutputState(values[1:7]), TachoInfo(values[7:])

class Motor(BaseMotor):
    def __init__(self, brick, port): #, values
        self.brick = brick
        self.port = port
        self._read_state()
        self.sync = 0
        self.turn_ratio = 0
        self.tacho_count
        self.block_tacho_count
        #self.rotation_count = values
        try:
            self.method = brick.sock.type
        except:
            print "Warning: Socket did not report a type!"
            print "Please report this problem to the developers!"
            print "For now, turn() accuracy will not be optimal."
            print "Continuing happily..."
            self.method = None

    def _set_state(self, state):
        self._debug_out('Setting brick output state...')
        list_state = [self.port] + state.to_list()
        self.brick.set_output_state(*list_state)
        self._debug_out(state)
        self._state = state
        self._debug_out('State set.')

    def _read_state(self):
        self._debug_out('Getting brick output state...')
        values = self.brick.get_output_state(self.port)
        self._debug_out('State got.')
        self._state, tacho = get_tacho_and_state(values)
        #return self._state, tacho
        return tacho

    #def get_tacho_and_state here would allow tacho manipulation

    def get_tacho_and_state(values):
        """A convenience function. values is the list of values from
            get_output_state. Returns both OutputState and TachoInfo.
        """
        return OutputState(values[1:7]), TachoInfo(values[7:])

    def _get_state(self):
        """Returns a copy of the current motor state for manipulation."""
        return OutputState(self._state.to_list())

    def _get_new_state(self):
        state = self._get_state()
        if self.sync:
            state.mode = MODE_MOTOR_ON | MODE_REGULATED
            state.regulation = REGULATION_MOTOR_SYNC
            state.turn_ratio = self.turn_ratio
        else:
            state.mode = MODE_MOTOR_ON | MODE_REGULATED
            state.regulation = REGULATION_MOTOR_SPEED
        state.run_state = RUN_STATE_RUNNING
        state.tacho_limit = LIMIT_RUN_FOREVER
        return state

    def get_tacho(self):
        #return self._read_state()[1]
        return OutputState(values[1:7])

        '''
            MY NEW SHIT



        '''

    def tacho_count(self):
        return self.tacho_count

    def block_tacho_count(self):
        return self.block_tacho_count

#    def rotation_count(self):
#        return self.rotation_count

        '''



            MY NEW SHIT
        '''

    def reset_position(self, relative):
        """Resets the counters. Relative can be True or False"""
        self.brick.reset_motor_position(self.port, relative)

    def run(self, power=100, regulated=False):
        '''Tells the motor to run continuously. If regulated is True, then the
        synchronization starts working.
        '''
        state = self._get_new_state()
        state.power = power
        if not regulated:
            state.mode = MODE_MOTOR_ON
        self._set_state(state)

    def brake(self):
        """Holds the motor in place"""
        state = self._get_new_state()
        state.power = 0
        state.mode = MODE_MOTOR_ON | MODE_BRAKE | MODE_REGULATED
        self._set_state(state)

    def idle(self):
        '''Tells the motor to stop whatever it's doing. It also desyncs it'''
        state = self._get_new_state()
        state.power = 0
        state.mode = MODE_IDLE
        state.regulation = REGULATION_IDLE
        state.run_state = RUN_STATE_IDLE
        self._set_state(state)

    def weak_turn(self, power, tacho_units):
        """Tries to turn a motor for the specified distance. This function
        returns immediately, and it's not guaranteed that the motor turns that
        distance. This is an interface to use tacho_limit without
        REGULATION_MODE_SPEED
        """
        tacho_limit = tacho_units
        tacho = self.get_tacho()
        state = self._get_new_state()

        # Update modifiers even if they aren't used, might have been changed
        state.mode = MODE_MOTOR_ON
        state.regulation = REGULATION_IDLE
        state.power = power
        state.tacho_limit = tacho_limit

        self._debug_out('Updating motor information...')
        self._set_state(state)

    def _eta(self, current, target, power):
        """Returns time in seconds. Do not trust it too much"""
        tacho = abs(current.tacho_count - target.tacho_count)
        return (float(tacho) / abs(power)) / 5

    def _is_blocked(self, tacho, last_tacho, direction):
        """Returns if any of the engines is blocked"""
        return direction * (last_tacho.tacho_count - tacho.tacho_count) >= 0
