#!/usr/bin/env pybricks-micropython

print("Starting import")

import time

from pybricks.ev3devices import (ColorSensor,Motor, TouchSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import Font, ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

print("Done Importing, starting program")

# Object Init
big_font = Font(size=18, bold=True) # Fonts
ev3 = EV3Brick() # EV3Brick
last_error = 0

ev3.speaker.set_volume(20, which='Beep')
ev3.speaker.set_volume(100, which='PCM')
ev3.speaker.set_speech_options(language='en', voice='m2', speed=180, pitch=50)
# ev3.speaker.play_notes(['D#4/4', 'F4/4', 'G4/4', 'G#4/8', 'A#4/4', 'R/16',
#                         'G#4/4', 'D#4/8', 'C#4/8', 'D#4/8', 'C#4/4', 'R/8',
#                         'G4/4', 'D#4/8', 'C#4/8', 'D#4/8', 'C#4/4', 'R/8',
#                         'B4/4', 'B4/8', 'B4/8', 'G#4/8', 'B4/8', 'C#5/8', 'B4/8', 'D#5/2', 'R/32',
#                         'D#4/8', 'D#4/8', 'C#5/4', 'R/32',
#                         'D#4/8', 'D#4/8', 'C#5/4', 'R/32',
#                         'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4',
#                         'B4/8', 'Bb4/8', 'B4/8', 'Bb4/8', 'G#4/8', 'G#4/4', 'Gb4/8', 'G#4/4', 'R/4',
#                         'G#4/4', 'Gb4/8', 'G#4/4', 'R/4',
#                         'G#4/4', 'Gb4/8', 'G#4/4', 'R/4', ], tempo=120)


# Setting Motors
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)

leftMedMotor = Motor(Port.D)
rightMedMotor = Motor(Port.A)

# Setting Sensors
leftSensor = ColorSensor(Port.S1)
middleSensor = ColorSensor(Port.S2)
rightSensor = ColorSensor(Port.S3)
buttonSensor = TouchSensor(Port.S4)

# Creating Functions
## Moving by given angle
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


## Line Tracking
def SinglePDTrack(sensorPort, threshold, kp, kd, speed): #test kp then kd, -(kp, kd) for right side line tracing
    if sensorPort == 1:
        ref = leftSensor.reflection()
        
    elif sensorPort == 2:
        ref = middleSensor.reflection()

    else:
        ref = rightSensor.reflection()

    #print(ref)
    global last_error  # im so smart
    error = ref - threshold
    p_gain = error * kp
    derivative = error - last_error
    d_gain = derivative * kd
    leftMotor.dc(min(100, speed-(p_gain+d_gain))) #im a genius
    rightMotor.dc(max(-100, speed+(p_gain+d_gain)))
    last_error = error


## Line Tracking Till Junction
def SinglePDTrackTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, kp, kd, speed):
    if junctionPort == 1:
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

## Line Tracking Till Degrees
def SinglePDTrackTillDegrees(degrees, trackingPort, trackingThreshold, kp, kd, speed):
    leftMotor.reset_angle(0)
    while abs(leftMotor.angle()) < abs(degrees):
        SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    leftMotor.stop()
    rightMotor.stop()

## Wait until it is pressed
def WaitForPress():
    while buttonSensor.pressed() == False:
        pass
    time.sleep(0.5)

## Write on ev3 screen
def WriteOnScreen(text):
    print(text)
    ev3.screen.set_font(big_font)
    ev3.screen.clear()
    ev3.screen.print(text)

## Squaring on the line
def SquareOnLine(Seconds, Target, Black, White, Approach, Forward, Backward):
    while True:
        while leftSensor.reflection() < White and rightSensor.reflection() < White:
            leftMotor.run(Forward)
            rightMotor.run(Forward)
        while leftSensor.reflection() > Black and rightSensor.reflection() > Black:
            leftMotor.run(Backward)
            rightMotor.run(Backward)
        if leftSensor.reflection() < Black:
            leftMotor.hold()
            while rightSensor.reflection() > Black:
                rightMotor.run(Forward)
            rightMotor.hold()
            break
        elif rightSensor.reflection() < Black:
            rightMotor.hold()
            while leftSensor.reflection() > Black:
                leftMotor.run(Forward)
            leftMotor.hold()
            break
    timeout = time.time() + Seconds
    while True:
        if leftSensor.reflection() < Target:
            while leftSensor.reflection() < Target:
                leftMotor.run(Backward)
            leftMotor.hold()
        elif leftSensor.reflection() > Target:
            while leftSensor.reflection() > Target:
                leftMotor.run(Approach)
            leftMotor.hold()
        if rightSensor.reflection() < Target:
            while rightSensor.reflection() < Target:
                rightMotor.run(Backward)
            rightMotor.hold()
        elif rightSensor.reflection() > Target:
            while rightSensor.reflection() > Target:
                rightMotor.run(Approach)
            rightMotor.hold()
        if time.time() > timeout:
            break

