#!/usr/bin/env pybricks-micropython
import time

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import Font, ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

# Create your objects here.
big_font = Font(size=18, bold=True)
ev3 = EV3Brick()
last_error = 0

# Motors
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
rightMedMotor = Motor(Port.A)
leftMedMotor = Motor(Port.D)

# Sensors
rightSensor = ColorSensor(Port.S1)
middleSensor = ColorSensor(Port.S2)
leftSensor = ColorSensor(Port.S3)
buttonSensor = TouchSensor(Port.S4)
ev3.speaker.set_volume(20, which='Beep')
ev3.speaker.set_volume(100, which='PCM')
ev3.speaker.set_speech_options(language='en', voice='m2', speed=180, pitch=50)
'''
ev3.speaker.play_notes(['D#4/4', 'F4/4', 'G4/4', 'G#4/8', 'A#4/4', 'R/16',
                        'G#4/4', 'D#4/8', 'C#4/8', 'D#4/8', 'C#4/4', 'R/8',
                        'G4/4', 'D#4/8', 'C#4/8', 'D#4/8', 'C#4/4', 'R/8',
                        'B4/4', 'B4/8', 'B4/8', 'G#4/8', 'B4/8', 'C#5/8', 'B4/8', 'D#5/2', 'R/32',
                        'D#4/8', 'D#4/8', 'C#5/4', 'R/32',
                        'D#4/8', 'D#4/8', 'C#5/4', 'R/32',
                        'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4',
                        'B4/8', 'Bb4/8', 'B4/8', 'Bb4/8', 'G#4/8', 'G#4/4', 'Gb4/8', 'G#4/4', 'R/4',
                        'G#4/4', 'Gb4/8', 'G#4/4', 'R/4',
                        'G#4/4', 'Gb4/8', 'G#4/4', 'R/4', ], tempo=120)
'''
# Functions


def MoveToAngle(leftAngle, rightAngle, leftSpeed, rightSpeed):
    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)
    leftMotor.run(leftSpeed)
    rightMotor.run(rightSpeed)
    while (abs(leftMotor.angle()) < abs(leftAngle)) or (abs(rightMotor.angle()) < abs(rightAngle)):
        if abs(rightMotor.angle()) >= abs(rightAngle):
            rightMotor.hold()
        if abs(leftMotor.angle()) >= abs(leftAngle):
            leftMotor.hold()
    leftMotor.hold()
    rightMotor.hold()


def MoveStalled(leftDC, rightDC):
    leftMotor.dc(leftDC)
    rightMotor.dc(rightDC)

    while True:
        if leftMotor.control.stalled():
            leftMotor.stop()
            rightMotor.stop()
            break
        if rightMotor.control.stalled():
            leftMotor.stop()
            rightMotor.stop()
            break


def SinglePTrack(sensorPort, threshold, kp, speed):
    if sensorPort == 3:
        ref = leftSensor.reflection()
        leftMotor.run(speed + ((ref - threshold) * kp))
        rightMotor.run(speed - ((ref - threshold) * kp))
    elif sensorPort == 2:
        ref = middleSensor.reflection()
        leftMotor.run(speed + ((ref - threshold) * kp))
        rightMotor.run(speed - ((ref - threshold) * kp))
    else:
        ref = rightSensor.reflection()
        leftMotor.run(speed + ((ref - threshold) * kp))
        rightMotor.run(speed - ((ref - threshold) * kp))


def SinglePTrackTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, kp, speed):
    if junctionPort == 3:
        while leftSensor.reflection() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    elif junctionPort == 2:
        while middleSensor.reflection() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    else:
        while rightSensor.reflection() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    leftMotor.stop()
    rightMotor.stop()


def SinglePTrackTillDegrees(degrees, trackingPort, trackingThreshold, kp, speed):
    leftMotor.reset_angle(0)
    while abs(leftMotor.angle()) < abs(degrees):
        SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    leftMotor.stop()
    rightMotor.stop()


def WaitUntillPressed(text: str):
    while buttonSensor.pressed() == False:
        pass
    print(text)


def ev3Print(text: str):
    print(text)
    ev3.screen.set_font(big_font)
    ev3.screen.clear()
    ev3.screen.print(text)


def betterStalled(leftSpeed, rightSpeed):
    leftMotor.run(leftSpeed)
    rightMotor.run(rightSpeed)
    wait(2000)
    while True:
        if (abs(leftMotor.speed()) < abs(leftSpeed * 0.1)) or (abs(rightMotor.speed()) < abs(rightSpeed * 0.1)):
            leftMotor.stop()
            rightMotor.stop()
            break


def SinglePDTrack(sensorPort, threshold, kp, kd, speed):
    ref = rightSensor.reflection()
    global last_error  # im so smart
    error = ref - threshold
    p_gain = error * kp
    derivative = error - last_error
    d_gain = derivative * kd
    leftMotor.run(speed-(p_gain+d_gain))
    rightMotor.run(speed+(p_gain+d_gain))
    last_error = error


def SinglePDTrackDegrees(degrees, trackingPort, threshold, kp, kd, speed):
    leftMotor.reset_angle(0)
    while abs(leftMotor.angle()) < abs(degrees):
        SinglePDTrack(trackingPort, threshold, kp, kd, speed)
    leftMotor.hold()
    rightMotor.hold()


def SinglePDTrackTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, kp, kd, speed):
    if junctionPort == 3:
        while leftSensor.reflection() > junctionThreshold:
            SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    elif junctionPort == 2:
        while middleSensor.reflection() > junctionThreshold:
            SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    else:
        while rightSensor.reflection() > junctionThreshold:
            SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    leftMotor.hold()
    rightMotor.hold()

def startRun():
    leftMedMotor.stop()
    rightMedMotor.stop()
    WaitUntillPressed("1")
    leftMedMotor.hold()
    rightMedMotor.hold()

####### R E A L #### R U N ##########

def run1():
    # Basketball + Bocia
    # Run 1
    startRun()
    ev3Print("RUN 1")
    ev3Print("Going Forward")
    MoveToAngle(640, 640, -600, -600)
    MoveToAngle(250, 0, -400, 0)
    SinglePDTrackDegrees(700, 1, 43, 1.2, 10, -350)
    SinglePDTrackTillJunction(3, 11, 1, 43, 1.2, 10, -150)
    ev3Print("Arrived at the 2 stations")
    wait(300)
    MoveToAngle(0, 215, 0, 200)
    leftMotor.run_time(-170,2000,then=Stop.HOLD,wait=False)
    rightMotor.run_time(-150,2000,then=Stop.HOLD,wait=True)
    wait(300)
    leftMedMotor.run_time(1000, 7000, then=Stop.HOLD, wait=True)
    wait(300)
    leftMedMotor.run_time(-1000,800,then=Stop.HOLD, wait=True)
    MoveToAngle(300, 300, 500, 500)
    MoveToAngle(170, 0, -350, 0)
    MoveToAngle(1200, 1200, -1000, -900)
def run2():
    # Treadmill, Row Machine
    # Run 2
    startRun()
    ev3Print("RUN 2")
    MoveToAngle(-1000, -1000, -600, -600)
    SinglePDTrackDegrees(1300, 1, 43, 1.2, 10, -500)
    SinglePDTrackTillJunction(3, 11, 1, 43, 1.2, 10, -120)
    ev3Print("reached junction")
    MoveToAngle(-100, -100, -300, -300)
    leftMedMotor.run_angle(1000, 200, then=Stop.HOLD, wait=False)
    rightMedMotor.run_time(1000, 9000, then=Stop.HOLD, wait=True)
    ev3Print("complete treadmill")
    wait(250)
    MoveToAngle(200, 200, 500, 500)
    wait(250)
    ev3Print("turning 1")
    MoveToAngle(150, 0, -400, -173)
    wait(250)
    ev3Print("raising left")
    leftMedMotor.run_angle(-1000, 200, then=Stop.HOLD, wait=True)
    wait(250)
    ev3Print("turning 2")
    MoveToAngle(75, 0, -200, -0)
    wait(250)
    ev3Print("wall align")
    MoveToAngle(500, 1000, 300, 600)
    wait(250)
    MoveToAngle(-210, -210, -200, -200)
    wait(250)
    MoveToAngle(-370, 0, -400, 0)
    wait(250)
    MoveToAngle(2500, 2125, -1000, -850)
    wait(250)
    print("done")

def run3():
    # Run 3 dropping of cubes
    startRun()
    ev3Print("RUN 3")
    rightMedMotor.run_time(-600,600,then=Stop.HOLD,wait=False)
    MoveToAngle(-1620,-1800,-1000,-800)
    leftMotor.run_time(-750,1500,then=Stop.HOLD,wait=False)
    rightMotor.run_time(-780,1500,then=Stop.HOLD,wait=True)
    wait(300)
    MoveToAngle(110,110,400,400)
    MoveToAngle(200,200,-500,500)
    wait(250)
    leftMotor.run_time(500,1000,then=Stop.HOLD,wait=False)
    rightMotor.run_time(500,1000,then=Stop.HOLD,wait=True)
    SinglePDTrackDegrees(900,3,43,1.2,10,-450)

    while leftSensor.reflection() > 11:
        SinglePDTrack(1, 43, .9, 8, -550)

    '''
    leftMotor.run(-200)
    rightMotor.run(-200)
    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)
    while (leftSensor.reflection() > 10) or (leftMotor.angle() < 400) or (rightMotor.angle() < 400):
        pass
    leftMotor.stop()
    rightMotor.stop()
    '''
    MoveToAngle(310,310,-600,-600)
    wait(100)

    rightMedMotor.run_time(600, 600, then=Stop.HOLD, wait=True)
    rightMedMotor.run_time(-600, 600, then=Stop.HOLD, wait=True)
    leftMedMotor.run_time(-600, 650, then=Stop.HOLD, wait=True)

    MoveToAngle(185,185,300,300)
    MoveToAngle(0,430,0,-350)
    MoveToAngle(60,60,-150,-150)
    wait(250)
    MoveToAngle(800,800,1000,1000)
    wait(100)
    MoveToAngle(330,0,-500,0)
    MoveToAngle(2000,2000,1000,1000)
  

def run4():
    # Run 4 slide, kids
    startRun()
    ev3Print("RUN 4")
    leftMotor.run_time(-750,2300,then=Stop.HOLD,wait=False)
    rightMotor.run_time(-750,2300,then=Stop.HOLD,wait=True)
    wait(100)
    MoveToAngle(2000, 2000, 1000, 1000)

def run5():
    # bench
    # Run 5
    startRun()
    ev3Print("RUN 5")

    MoveToAngle(-600, -600, -800, -800)
    #MoveToAngle(-200, -200, -200, -200)
    leftMotor.run_time(-200,1500,then=Stop.HOLD,wait=False)
    rightMotor.run_time(-200,1500,then=Stop.HOLD,wait=True)
    leftMotor.run(1000)
    rightMotor.run(500)
    WaitUntillPressed('1')
    leftMotor.hold()
    rightMotor.hold()
    wait(100)

def run6():

    # #Run 6
    startRun()
    ev3Print("RUN 6")
    MoveToAngle(1100,1100,-700,-700)
    SinglePDTrackDegrees(400,1,43,1.2,10,-360)
    SinglePDTrackTillJunction(2,10,1,43,1.2,10,-400)
    MoveToAngle(40,40,200,200)
    MoveToAngle(75,-450,50,-300)
    leftMotor.run_time(-750,1000,then=Stop.HOLD,wait=False)
    rightMotor.run_time(-750,1000,then=Stop.HOLD,wait=True)
    MoveToAngle(800,800,1000,1000)
    leftMedMotor.run_time(1000, 13000, then=Stop.HOLD, wait=False)
    rightMedMotor.run_time(1000, 13000, then=Stop.HOLD, wait=True)
    
#run1()
#run2()
#run3()
#run4()
#run5()
#run6()



leftMedMotor.run_time(1000, 13000, then=Stop.HOLD, wait=False)
rightMedMotor.run_time(1000, 13000, then=Stop.HOLD, wait=True)