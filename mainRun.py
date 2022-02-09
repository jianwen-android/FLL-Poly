#!/usr/bin/env pybricks-micropython

from func import *


def Run1():
    WriteOnScreen("Run 1")
    WaitForPress()
    WriteOnScreen("Change Attachment")
    rightMedMotor.run(100)
    rightMedMotor.hold()
    leftMedMotor.hold()
    WaitForPress()
    WriteOnScreen("Launching")
    leftMedMotor.run(-450)
    time.sleep(1)
    leftMedMotor.hold()
    rightMedMotor.hold()

    MoveToAngle(600, 612, -500, -510)
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    leftMotor.hold()
    rightMotor.hold()
    MoveToAngle(500, 510, -500, -510)
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    leftMotor.hold()
    rightMotor.hold()
    MoveToAngle(200, 204, -500, -510)
    rightMedMotor.run(-600)
    time.sleep(1)
    rightMedMotor.hold()
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    MoveToAngle(92, 90, -510, -500)
    time.sleep(0.1)
    MoveToAngle(1250, 1250, 500, 500)
    rightMedMotor.run(600)
    time.sleep(1)
    rightMedMotor.hold()
    MoveToAngle(1800, 1800, 500, 500)

    """
    SinglePDTrackTillJunction(2, 15, 3, 55, 2.7, 2.7, -370)
    MoveToAngle(570, 570, -500, -500)
    SinglePDTrackTillJunction(2, 15, 3, 55, 2.7, 2.7, -370)
    MoveToAngle(570, 712, -400, -500)
    SinglePDTrackTillDegrees(180, 3, 55, 2.7, 2.7, -370)
    rightMedMotor.run(200)
    sleep(1)
    rightMedMotor.hold()
    leftMedMotor.hold()
    SinglePDTrackTillJunction(2, 15, 3, 55, 2.7, 2.7, -370)
    MoveToAngle(100, 100, -500, -500)
    """


def Run3():  # single onion flat up
    WriteOnScreen("Run 3 Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    MoveToAngle(650, 650, -500, -500)
    SinglePDTrackTillDegrees(700, 3, 50, 0.65, 10, -75)
    SinglePDTrackTillDegrees(300, 3, 50, 0.4, 10, -75)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -75)
    MoveToAngle(175, 175, -500, -500)
    while leftSensor.reflection() != 11:
        leftMotor.dc(50)
        rightMotor.dc(50)
    MoveToAngle(400, 400, 500, 500)
    leftMedMotor.run(600)
    time.sleep(3)
    leftMedMotor.hold()
    MoveToAngle(1800, 1800, 500, 500)

Run1()
Run3()
