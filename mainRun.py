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
    leftMedMotor.run(-600)
    time.sleep(1)
    leftMedMotor.hold()
    rightMedMotor.hold()

    MoveToAngle(600, 612, -600, -610)
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    leftMotor.hold()
    rightMotor.hold()
    MoveToAngle(500, 510, -600, -610)
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    leftMotor.hold()
    rightMotor.hold()
    MoveToAngle(200, 204, -600, -610)
    rightMedMotor.run(-600)
    time.sleep(1)
    rightMedMotor.hold()
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    MoveToAngle(92, 90, -610, -600)
    time.sleep(0.1)
    MoveToAngle(1250, 1250, 600, 600)
    rightMedMotor.run(600)
    time.sleep(1)
    rightMedMotor.hold()
    MoveToAngle(1800, 1800, 800, 800)

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

def Run4():
    WriteOnScreen("Run 4 Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    MoveToAngle(100, 100, -600, -600)
    MoveToAngle(155, 0, -600, 0)
    MoveToAngle(300, 300, -600, -600)
    SinglePDTrackTillDegrees(1000, 3, 50, 0.65, 10, -75)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -75)
    MoveToAngle(50, 50, -600, -600)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -75)
    MoveToAngle(0, 340, 0, -600)
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    MoveToAngle(260, 260, -600, -600)
    rightMedMotor.run(600)
    time.sleep(1.5)
    rightMedMotor.hold()
    MoveToAngle(260, 260, 300, 300)
    rightMedMotor.run(-600)
    time.sleep(1.5)
    rightMedMotor.hold()
    MoveToAngle(0, 590, 0, 300)
    MoveToAngle(1000, 1000, 600, 600)
    time.sleep(0.5)
    MoveToAngle(80, 80, -600, -600)
    MoveToAngle(170, 170, 600, -600)
    MoveToAngle(450, 450, 100, 100)


Run1()
Run3()
Run4()
