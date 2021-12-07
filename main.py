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