# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 19:40:11 2013

@author: benjamin
"""


# Works great! =D



from Robot import * 


        
robot = Robot()

robot.move(75)
#robot.turn(75, 1800)


for i in range(4):
    robot.wait(1)
    #print robot.tacho()
    try:
        print robot.tacho()
    except:
        print "Your balls ass method didn't work"
        break
    
robot.stop()

