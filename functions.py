#!/usr/bin/env python3

# DO NOT TOUCH THE COMMANDS HERE, THIS IS BACK UP BEACUSE INBUILT ASSSSS

from time import sleep, time

from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, MediumMotor,OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, SpeedPercent
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, TouchSensor

print("Done importing")

leftMotor = LargeMotor(OUTPUT_B)
rightMotor = LargeMotor(OUTPUT_C)

leftMedMotor = MediumMotor(OUTPUT_D)
rightMedMotor = MediumMotor(OUTPUT_A)

# Tank drives
main_drive = MoveTank(OUTPUT_B, OUTPUT_C)
secondary_drive = MoveTank(OUTPUT_D, OUTPUT_A,motor_class=MediumMotor)

leftSensor = ColorSensor(INPUT_1)
middleSensor = ColorSensor(INPUT_2)
rightSensor = ColorSensor(INPUT_3)
button = TouchSensor(INPUT_4)

print('Initalization Done')

def LineTrace(Target, Kp, Kd, Speed):
    temp = 0
    ref = rightSensor.reflected_light_intensity
    error = ref - Target
    p_gain = error * Kp
    while temp == 0:
        last_error = 0
        derivative = error
        temp += 1
    else:
        derivative = error - last_error
    d_gain = derivative * Kd
    change = (p_gain+d_gain)/10
    #print(change)
    leftMotor.on(SpeedPercent(Speed-(change)), brake=False)
    rightMotor.on(SpeedPercent(Speed+(change)),brake=False)
    last_error = error

def LineTraceTillJunc(Target, Kp, Kd, Black, Speed):
    while middleSensor.reflected_light_intensity > Black:
        LineTrace(Target, Kp, Kd, Speed)
    leftMotor.on(0)
    rightMotor.on(0)

def LineSquaring(Seconds, Target, Black, White, Approach, Forward, Backward):
    Approach = SpeedPercent(Approach)
    Forward = SpeedPercent(Forward)
    Backward = SpeedPercent(Backward)
    print('Rough Approach')
    while True:
        while leftSensor.reflected_light_intensity > Black and rightSensor.reflected_light_intensity > Black:
            temp = 0
            while temp == 0:
                print('approaching line')
                temp += 1
            leftMotor.on(Approach)
            rightMotor.on(Approach)
        print('rough squaring')
        if leftSensor.reflected_light_intensity < Black:
            leftMotor.on(0)
            while rightSensor.reflected_light_intensity > Black:
                rightMotor.on(Forward)
            rightMotor.on(0)
            break
        elif rightSensor.reflected_light_intensity < Black:
            rightMotor.on(0)
            while leftSensor.reflected_light_intensity > Black:
                leftMotor.on(Forward)
            leftMotor.on(0)
            break
    print("Done Rough Approach")
    print('Fine Adjustments')
    
print('waiting for command')
button.wait_for_bump()
print('launching')
#LineTraceTillJunc(55, 2, 0.05, 12, -30)
LineSquaring(5, 55, 20, 90, -20, -10, 10)

