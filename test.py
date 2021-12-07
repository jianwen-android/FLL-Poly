#!/usr/bin/env pybricks-micropython
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

kp = 1.2
kd = 10
ki = 0.5

while True:
    main_drive.cs = rightSensor
    main_drive.follow_line(
    kp, ki, kd, SpeedPercent(50), follow_left_edge=False
    )

