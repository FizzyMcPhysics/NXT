# -*- coding: utf-8 -*-
"""
Created on Wed May  1 16:28:53 2013

IT WORKS!!!

Added sonar readings with velocity and acceloration calculations for both. 

@author: benjamin
"""

from time import sleep
from nxt.motor import Motor, PORT_A, PORT_C, SynchronizedMotors
from nxt.sensor import Ultrasonic, PORT_1
import nxt.locator
import string

brick = nxt.locator.find_one_brick()
left = Motor(brick, PORT_C)
right = Motor(brick, PORT_A)
tracks = SynchronizedMotors(left, right, 0)
tacho_zero = [0,0] # An array for resetting the tacho readings. 

# This program uses the physics notiation of:
# X for position
# V for velocity, a.k.a: X-dot
# A for acceleration, a.k.a: X-double-dot

tachoX0 = [0,0] # Current tacho position in degrees
tachoX1 = [0,0] # Previous tacho position
tachoV0 = [0,0] # Current tacho velocity in dgrees per second
tachoV1 = [0,0] # Tacho velocity at previous time step
tachoA0 = [0,0] # Current tacho acceleration in dgrees per second per second

sonarX0 = [0,0] # Current sonar reading provides distance in cm from objects
sonarX1 = [0,0] # Previous sonar reading
sonarV0 = [0,0] # Current soar velocity in cm per second: the speed with which the object approaches
sonarV1 = [0,0] # Well, you get the idea. Sonar is actually only one reading, but I've stored it in a two element array...
sonarA0 = [0,0] # ...this makes it easyer for the velocity and acceloration functions to work with anything they are given.

sleepytime = 1 # Time between readings in seconds
steps = 4
power = 75 # Percentage of available power
     
# This function is rediculously over complicated! It stems from the fact that the NXT library is a mess and is therefore
# not my fault!

def tacho_position():
    get_tacho = str(tracks.get_tacho()) # Gets tacho readings in the form: 'tacho: ' + t1 + ' ' + t2
    tacho_strings = string.split(get_tacho) # Splits tacho into form ['tacho: ', 't1', 't2']
   
    tacho_reading = [] # new array
    tacho_reading.append(int(tacho_strings[1])-tacho_zero[0]) # Turns 't1' back into an integer and appends to new array
    tacho_reading.append(int(tacho_strings[2])-tacho_zero[1]) # Turns 't2' back into an integer and appends to new array   
    return tacho_reading
    
# These next two functions do EXACTLY the same thing, but have different names. I belive that this makes the code lower
# down, where they are called, more readable, so I've decided to keep them seperate. 
   
def velocity(x0, x1): # Claculates change in position over time. 
    xdot = []
    xdot.append(int( (x0[0]-x1[0]) /sleepytime )) 
    xdot.append(int( (x0[1]-x1[1]) /sleepytime ))
    return xdot
    
def acceloration(v0, v1): # Claculates the change in velocity over time.
    xdotdot = []
    xdotdot.append(int( (v0[0]-v1[0]) / sleepytime ))
    xdotdot.append(int( (v0[1]-v1[1]) / sleepytime ))
    return xdotdot
    
def sonar_reading():
    x = [Ultrasonic(brick, PORT_1).get_sample(), 0]
    return x


tacho_zero = tacho_position() # Restes the tachometer
tracks.run(power) # Takes +ve and -ve values =)

for i in range(steps):
    sleep(sleepytime)
   
    tachoX1 = tachoX0
    tachoX0 = tacho_position()
   
    tachoV1 = tachoV0
    tachoV0 = velocity(tachoX0, tachoX1)
    tachoA0 = acceloration(tachoV0, tachoV1)
   
    sonarX1 = sonarX0
    sonarX0 = sonar_reading()
    
    sonarV1 = sonarV0
    sonarV0 = velocity(sonarX0, sonarX1)
    sonarA0 = acceloration(sonarV0, sonarV1)
   
    print tachoX0, tachoV0, tachoA0
    print sonarX0[0], sonarV0[0], sonarA0[0] 
    print ' '
    
tracks.idle()    












