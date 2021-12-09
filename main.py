#!/usr/bin/env python3

from time import sleep

from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, MediumMotor,OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, SpeedPercent
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, TouchSensor

# Motors
leftMotor = LargeMotor(OUTPUT_B)
rightMotor = LargeMotor(OUTPUT_C)

leftMedMotor = MediumMotor(OUTPUT_D)
rightMedMotor = MediumMotor(OUTPUT_A)

# Tank drives
main_drive = MoveTank(OUTPUT_B, OUTPUT_C)
secondary_drive = MoveTank(OUTPUT_D, OUTPUT_A,motor_class=MediumMotor)

# Sensors
leftSensor = ColorSensor(INPUT_1)
middleSensor = ColorSensor(INPUT_2)
rightSensor = ColorSensor(INPUT_3)
button = TouchSensor(INPUT_4)

print("Done importing")

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

def follow_lineForDegrees(degrees, trackingPort, trackingThreshold, speed, left):
    leftMotor.reset_angle(0)
    main_drive.cs = trackingPort
    left = not left
    while abs(leftMotor.position()) < abs(degrees):
        main_drive.follow_line(
        kp, ki, kd, speed, target_light_intensity=trackingThreshold, follow_left_edge=left, white=90
        )
    leftMotor.stop()
    rightMotor.stop()

def follow_lineTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, speed, left):
    main_drive.cs = trackingPort
    left = not left
    if junctionPort == 3:
        while leftSensor.reflected_light_intensity() > junctionThreshold:
            main_drive.follow_line(
            kp, ki, kd, speed, target_light_intensity=trackingThreshold, follow_left_edge=left, white=90
            )
    elif junctionPort == 2:
        while middleSensor.reflected_light_intensity() > junctionThreshold:
            main_drive.follow_line(
            kp, ki, kd, speed, target_light_intensity=trackingThreshold, follow_left_edge=left, white=90
            )
    else:
        while rightSensor.reflected_light_intensity() > junctionThreshold:
            main_drive.follow_line(
            kp, ki, kd, speed, target_light_intensity=trackingThreshold, follow_left_edge=left, white=90
            )
    leftMotor.stop()
    rightMotor.stop()

def run1():
    main_drive.on_for_degrees(globalSpeed, globalSpeed, 600)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, blackWhite, globalSpeed, False
    )
    main_drive.on_for_degrees(globalSpeed, globalSpeed, 100)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, blackWhite, globalSpeed, False
    )
    main_drive.on_for_degrees(globalSpeed, globalSpeed, 100)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, blackWhite, globalSpeed, False
    )
    main_drive.on_for_degrees(globalSpeed, globalSpeed, 210)
    rightMedMotor.on_for_degrees(globalSpeed, 500)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, blackWhite, globalSpeed, False
    )
    leftMedMotor.on_for_degrees(globalSpeed, 500)
    main_drive.on_for_degrees(-globalSpeed, -globalSpeed, 1400)

def run2():
    main_drive.on_for_degrees(globalSpeed, globalSpeed, 600)
    main_drive.follow_lineTillJunction(
        leftSensor, black, rightSensor, blackWhite, globalSpeed, False
    )


# RUN STARTS HERE

globalSpeed = SpeedPercent(-50)
kp = 2
kd = 0
ki = 0.0
blackWhite = 45
black = 10

print('waiting for launch')
secondary_drive.on(SpeedPercent(-20),SpeedPercent(-20))
button.wait_for_bump()
print('launching')
secondary_drive.on(0,SpeedPercent(-5))
leftMedMotor.stop()
button.wait_for_bump()
print('Starting')
main_drive.cs = ColorSensor(INPUT_3)
while middleSensor.reflected_light_intensity > black + 5:
    main_drive.follow_line(
    kp, ki, kd, SpeedPercent(-20), target_light_intensity=45, follow_left_edge=True, white=90
    )


leftMedMotor.stop()
rightMedMotor.stop()
leftMotor.stop()
rightMotor.stop()