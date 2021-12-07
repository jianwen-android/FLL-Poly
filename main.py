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

# Functions
def MoveTillJunction(junctionPort, junctionThreshold, speed):
    if junctionPort == 3:
        while leftSensor.reflected_light_intensity() > junctionThreshold:
            leftMotor.on(speed)
            rightMotor.on(speed)
    elif junctionPort == 2:
        while middleSensor.reflected_light_intensity() > junctionThreshold:
            leftMotor.on(speed)
            rightMotor.on(speed)
    else:
        while rightSensor.reflected_light_intensity() > junctionThreshold:
            leftMotor.on(speed)
            rightMotor.on(speed)
    leftMotor.stop()
    rightMotor.stop()

def MoveTillStalled(leftSpeed, rightSpeed):
    leftMotor.on(leftSpeed)
    rightMotor.on(rightSpeed)
    sleep(2000)
    while True:
        if (abs(leftMotor.speed()) < abs(leftSpeed * 0.1)) or (abs(rightMotor.speed()) < abs(rightSpeed * 0.1)):
            leftMotor.stop()
            rightMotor.stop()
            break

def follow_lineForDegrees(degrees, trackingPort, speed, left):
    leftMotor.reset_angle(0)
    main_drive.cs = trackingPort
    while abs(leftMotor.position()) < abs(degrees):
        main_drive.follow_line(
        kp, ki, kd, speed, follow_left_edge=left
        )
    leftMotor.stop()
    rightMotor.stop()

def follow_lineTillJunction(junctionPort, junctionThreshold, trackingPort, speed, left):
    main_drive.cs = trackingPort
    if junctionPort == 3:
        while leftSensor.reflected_light_intensity() > junctionThreshold:
            main_drive.follow_line(
            kp, ki, kd, speed, follow_left_edge=left
            )
    elif junctionPort == 2:
        while middleSensor.reflected_light_intensity() > junctionThreshold:
            main_drive.follow_line(
            kp, ki, kd, speed, follow_left_edge=left
            )
    else:
        while rightSensor.reflected_light_intensity() > junctionThreshold:
            main_drive.follow_line(
            kp, ki, kd, speed, follow_left_edge=left
            )
    leftMotor.stop()
    rightMotor.stop()

def run1():
    main_drive.on_for_rotation(globalSpeed, globalSpeed, 600)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, globalSpeed, True
    )
    main_drive.on_for_rotation(globalSpeed, globalSpeed, 100)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, globalSpeed, True
    )
    main_drive.on_for_rotation(globalSpeed, globalSpeed, 100)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, globalSpeed, True
    )
    main_drive.on_for_rotation(globalSpeed, globalSpeed, 210)
    rightMedMotor.on_for_degrees(globalSpeed, 500)


# RUN STARTS HERE

globalSpeed = SpeedPercent(50)
kp = 1.2
kd = 10
ki = 0.5

black = 9

run1()

leftMedMotor.stop()
rightMedMotor.stop()
leftMedMotor.stop()
rightMedMotor.stop()