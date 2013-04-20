# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:04:52 2013

@author: benjamin
"""

# Works great! =D

from time import sleep

from nxt_interface import *
from motor import Motor, PORT_A, PORT_B, PORT_C

FORTH = 100
BACK = -100


class Robot(object):

    def __init__(self, brick='NXT'):
        r'''Creates a new Robot controller.

            brick
                Either an nxt.brick.Brick object, or an NXT brick's name as a
                string. If omitted, a Brick named 'NXT' is looked up.
        '''
        if isinstance(brick, basestring):
            brick = find_one_brick(name=brick)

        self.brick = brick
        self.tool = Motor(brick, PORT_B)
        self.tracks = [Motor(brick, PORT_A), Motor(brick, PORT_C)]


        self.ultrasonic = Ultrasonic(brick, PORT_1)
        self.sound = Sound(brick, PORT_2)
        self.light = Light(brick, PORT_3)
        self.touch = Touch(brick, PORT_4)

    def turn(self, power, angle):
        for motor in self.tracks:
            motor.turn(power, angle)

    def move(self, power=FORTH):
        r'''Simultaneously activates the tracks motors, causing Robot to move.

            power
                The strength effected by the motors. Positive values will cause
                Robot to move forward, while negative values will cause it
                to move backwards. If you are unsure about how much force to
                apply, the special values FORTH and BACK provide reasonable
                defaults. If omitted, FORTH is used.
        '''
        for motor in self.tracks:
            motor.run(power=power)

    def wait(self, seconds):
        ''' secsonds
                How long the motors will rotate.
                Will this take values < 0? Most motor commands work in ms.
                Try passing sleep 1/seconds (miliseconds)
        '''
        sleep(seconds)

    def stop(self):
        for motor in self.tracks:
            motor.idle()

    def tacho(self):
        '''
           returns an array of two elements which are the motor tacho readings
        '''
        tachos = []
        for motor in self.tracks:
            #tachos.append(motor.get_tacho())
            tachos.append(motor.get_tacho_count()) #, rotation_count

        return tachos

    def act(self, power=FORTH):
        r'''Make Robot move its tool.

            power
                The strength effected by the motor. If omitted, (100) is used.
        '''
        self.tool.run(power=power)


    def echolocate(self):
        r'''Reads the Ultrasonic sensor's output.
        '''
        return self.ultrasonic.get_sample()

    def feel(self):
        r'''Reads the Touch sensor's output.
        '''
        return self.touch.get_sample()

    def hear(self):
        r'''Reads the Sound sensor's output.
        '''
        return self.sound.get_sample()

    def say(self, line, times=1):
        r'''Plays a sound file named (line + '.rso'), which is expected to be
            stored in the brick. The file is played (times) times.

            line
                The name of a sound file stored in the brick.

            times
                How many times the sound file will be played before this method
                returns.
        '''
        for i in range(0, times):
            self.brick.play_sound_file(False, line + '.rso')
            sleep(1)

    def see(self):
        r'''Reads the Light sensor's output.
        '''
        return self.light.get_sample()
