#!/usr/bin/env python3
from time import sleep
import asyncio

from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, MediumMotor,OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, SpeedPercent
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4, ColorSensor

# Motors
leftMotor = LargeMotor(OUTPUT_B)
rightMotor = LargeMotor(OUTPUT_C)
rightMedMotor = MediumMotor(OUTPUT_A)
leftMedMotor = MediumMotor(OUTPUT_D)

# Tank drives
main_drive = MoveTank(leftMotor, rightMotor)
secondary_drive = MoveTank(leftMedMotor, rightMedMotor)

# Sensors
leftSensor = ColorSensor(INPUT_1)
middleSensor = ColorSensor(INPUT_2)
rightSensor = ColorSensor(INPUT_3)

def SinglePDTrack(sensorPort, threshold, kp, kd, speed):
    ref = rightSensor.reflected_light_intensity()
    global last_error  # im so smart
    error = ref - threshold
    p_gain = error * kp
    derivative = error - last_error
    d_gain = derivative * kd
    leftMotor.on(speed-(p_gain+d_gain))
    rightMotor.on(speed+(p_gain+d_gain))
    last_error = error

def MoveStalled(leftDC, rightDC):
    leftMotor.on(leftDC)
    rightMotor.on(rightDC)

    while True:
        if leftMotor.is_stalled():
            leftMotor.stop()
            rightMotor.stop()
            break
        if rightMotor.is_stalled():
            leftMotor.stop()
            rightMotor.stop()
            break

def MoveToAngle(leftAngle, rightAngle, leftSpeed, rightSpeed):
    leftMotor.position() = 0
    rightMotor.position() = 0
    leftMotor.on(leftSpeed)
    rightMotor.on(rightSpeed)
    while (abs(leftMotor.position()) < abs(leftAngle)) or (abs(rightMotor.position()) < abs(rightAngle)):
        if abs(rightMotor.position()) >= abs(rightAngle):
            rightMotor.stop()
        if abs(leftMotor.position()) >= abs(leftAngle):
            leftMotor.stop()
    leftMotor.stop()
    rightMotor.stop()

def SinglePTrack(sensorPort, threshold, kp, speed):
    if sensorPort == 3:
        ref = leftSensor.reflected_light_intensity()
        leftMotor.on(speed + ((ref - threshold) * kp))
        rightMotor.on(speed - ((ref - threshold) * kp))
    elif sensorPort == 2:
        ref = middleSensor.reflected_light_intensity()
        leftMotor.on(speed + ((ref - threshold) * kp))
        rightMotor.on(speed - ((ref - threshold) * kp))
    else:
        ref = rightSensor.reflected_light_intensity()
        leftMotor.on(speed + ((ref - threshold) * kp))
        rightMotor.on(speed - ((ref - threshold) * kp))


def SinglePTrackTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, kp, speed):
    if junctionPort == 3:
        while leftSensor.reflected_light_intensity() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    elif junctionPort == 2:
        while middleSensor.reflected_light_intensity() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    else:
        while rightSensor.reflected_light_intensity() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    leftMotor.stop()
    rightMotor.stop()


def SinglePTrackTillDegrees(degrees, trackingPort, trackingThreshold, kp, speed):
    leftMotor.position() = 0
    while abs(leftMotor.position()) < abs(degrees):
        SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    leftMotor.stop()
    rightMotor.stop()
