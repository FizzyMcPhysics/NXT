class OutputState(object):
    """An object holding the internal state of a motor, not including rotation
    counters.
    """
    def __init__(self, values):
        (self.power, self.mode, self.regulation,
            self.turn_ratio, self.run_state, self.tacho_limit) = values

    def to_list(self):
        """Returns a list of properties that can be used with set_output_state.
        """
        return [self.power, self.mode, self.regulation,
            self.turn_ratio, self.run_state, self.tacho_limit]

    def __str__(self):
        modes = []
        if self.mode & MODE_MOTOR_ON:
            modes.append('on')
        if self.mode & MODE_BRAKE:
            modes.append('brake')
        if self.mode & MODE_REGULATED:
            modes.append('regulated')
        if not modes:
            modes.append('idle')
        mode = '&'.join(modes)
        regulation = 'regulation: ' + \
                            ['idle', 'speed', 'sync'][self.regulation]
        run_state = 'run state: ' + {0: 'idle', 0x10: 'ramp_up',
                            0x20: 'running', 0x40: 'ramp_down'}[self.run_state]
        return ', '.join([mode, regulation, str(self.turn_ratio), run_state] + [str(self.tacho_limit)])
