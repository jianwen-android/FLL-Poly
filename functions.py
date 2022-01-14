#!/usr/bin/env python3

# DO NOT TOUCH THE COMMANDS HERE, THIS IS BACK UP BEACUSE INBUILT ASSSSS

from time import sleep, time

from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from ev3dev2.motor import LargeMotor, MediumMotor,OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, SpeedPercent, Motor
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, TouchSensor

print("Done Importing")

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

last_error = 0

screen = Display()

print('Initalization Done')

def LineTrace(TraceSensor, Target, Kp, Kd, Speed):
    global last_error
    if TraceSensor == 1:
        ref = leftSensor.reflected_light_intensity
    elif TraceSensor == 2:
        ref = middleSensor.reflected_light_intensity
    elif TraceSensor == 3:
        ref = rightSensor.reflected_light_intensity
    error = ref - Target
    p_gain = error * Kp
    derivative = error - last_error
    d_gain = derivative * Kd
    change = (p_gain+d_gain) / 2
    print(last_error, error, p_gain, derivative, d_gain, change)
    # if (Speed+change) < 0:
    #     leftSpeed = max(-100,Speed+change)
    # else:
    #     leftSpeed = min(100,Speed+change)
    # if (Speed-change) < 0:
    #     rightSpeed = max(-100,Speed-change)
    # else:
    #     rightSpeed = min(100,Speed-change)
    #print(change)
    leftMotor.duty_cycle_sp = (Speed-change)
    rightMotor.duty_cycle_sp = (Speed+change)
    last_error = error

def LineTraceTillJunc(TraceSensor, JuncSensor, Target, Kp, Kd, Black, Speed):
    print("LineTraceTillJunc|TS:{}|JS:{}|Tar:{}|Kp:{}|Kd:{}|BLK:{}|SPD:{}".format(TraceSensor,JuncSensor,Target,Kp,Kd,Black,Speed))
    while True:
        if JuncSensor == 1:
            ref = leftSensor.reflected_light_intensity
        elif JuncSensor == 2:
            ref = middleSensor.reflected_light_intensity
        elif JuncSensor == 3:
            ref = rightSensor.reflected_light_intensity
        if ref < Black:
            break
        else:
            LineTrace(TraceSensor, Target, Kp, Kd, Speed)
    leftMotor.on(0)
    rightMotor.on(0)

def LineTraceTillDegress(Degrees, TraceSensor, Target, Kp, Kd, Speed):
    print("LineTraceTillDeg|Deg:{}|TS:{}|Tar:{}|Kp:{}|Kd:{}|SPD:{}".format(Degrees,TraceSensor,Target,Kp,Kd,Speed))
    leftMotor.position = 0
    rightMotor.position = 0
    while abs(leftMotor.position) < abs(Degrees) and abs(rightMotor.position) < abs(Degrees):
        LineTrace(TraceSensor, Target, Kp, Kd, Speed)
    leftMotor.on(0)
    rightMotor.on(0)

def LineSquaring(Seconds, Target, Black, White, Approach, Forward, Backward):
    Approach = SpeedPercent(Approach)
    Forward = SpeedPercent(Forward)
    Backward = SpeedPercent(Backward)
    while True:
        while leftSensor.reflected_light_intensity < White and rightSensor.reflected_light_intensity < White:
            temp = 0
            while temp == 0:
                temp += 1
            leftMotor.on(Approach)
            rightMotor.on(Approach)
        while leftSensor.reflected_light_intensity > Black and rightSensor.reflected_light_intensity > Black:
            temp = 0
            while temp == 0:
                temp += 1
            leftMotor.on(Approach)
            rightMotor.on(Approach)
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
    timeout = time() + Seconds
    while True:
        if leftSensor.reflected_light_intensity < Target:
            while leftSensor.reflected_light_intensity < Target:
                leftMotor.on(Backward)
            leftMotor.on(0)
        elif leftSensor.reflected_light_intensity > Target:
            while leftSensor.reflected_light_intensity > Target:
                leftMotor.on(Forward)
            leftMotor.on(0)
        if rightSensor.reflected_light_intensity < Target:
            while rightSensor.reflected_light_intensity < Target:
                rightMotor.on(Backward)
            rightMotor.on(0)
        elif rightSensor.reflected_light_intensity > Target:
            while rightSensor.reflected_light_intensity > Target:
                rightMotor.on(Forward)
            rightMotor.on(0)
        if time() > timeout:
            break

def Text(text):
    screen.text_pixels(text,font=fonts.load('luBS24'))
    screen.update()
    print(text)


# LineTraceTillJunc(3, 2, 55, 2, 0.025, 20, -30)
# # LineTraceTillJunc(2, 1, 55, 2, 0.05, 15, -30)

# LineTraceTillDegress(5000, 3, 55 , 2, 0.025, -30)

Text("Testing Line Tracing")
button.wait_for_bump()
Text("Running Line Tracing")
while True:
    LineTrace(1, 48, 0.3, 1, -30)
