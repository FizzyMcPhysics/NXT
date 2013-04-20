MODE_IDLE = 0x00
MODE_MOTOR_ON = 0x01
MODE_BRAKE = 0x02
MODE_REGULATED = 0x04

class Brick:
    def __init__(self):
        self.state = State()
        return

    def get_output_state(self, arg1):
        return self.state

    def set_output_state(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):
        # print arg1
        # print arg2
        # print arg3
        # print arg4
        # print arg5
        # print arg6
        # print arg7
        return


class State:
    def __init__(self):
        self.state = [ 'other', 'power', 'mode', 'regulation', 'turn_ratio', 'run_state', 'tacho_limit', 'tacho_count', 'tacho_block_count', 'rotation_count' ]

    def __getitem__(self, key):
        return self.state[key]

    def __setitem__(self, key, value):
        self.state[key] = value
        return

