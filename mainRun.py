#!/usr/bin/env pybricks-micropython

from func import *


def Run1():
    WriteOnScreen("Run 1 Ready")
    rightMedMotor.run(100)
    WaitForPress()
    WriteOnScreen("Launching")
    rightMedMotor.hold()
    leftMedMotor.hold()
    leftMedMotor.run(-1000)
    time.sleep(1)
    leftMedMotor.hold()
    rightMedMotor.hold()
    MoveToAngle(600, 612, -800, -800)
    while leftSensor.reflection() > 15:
        rightMotor.run(-500)
        leftMotor.run(-500)
    leftMotor.hold()
    rightMotor.hold()
    MoveToAngle(500, 510, -990, -1000)
    while leftSensor.reflection() > 15:
        rightMotor.run(-500)
        leftMotor.run(-500)
    leftMotor.hold()
    rightMotor.hold()
    MoveToAngle(200, 204, -800, -801)
    rightMedMotor.run(-200)
    time.sleep(2)
    rightMedMotor.hold()
    while leftSensor.reflection() > 15:
        rightMotor.run(-800)
        leftMotor.run(-800)
    MoveToAngle(92, 90, -1000, -990)
    time.sleep(0.1)
    MoveToAngle(1230, 1230, 1000, 1000)
    rightMedMotor.run(800)
    time.sleep(0.8)
    rightMedMotor.hold()
    MoveToAngle(1800, 1800, 1000, 1000)

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

def Run3():  
    WriteOnScreen("Run 3 Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    MoveToAngle(200, 200, -1000, -1000)
    rightMedMotor.run(1000)
    time.sleep(1.5)
    rightMedMotor.run(-1000)
    time.sleep(1)
    rightMedMotor.hold()
    MoveToAngle(200, 200, -1000, -1000)
    SinglePDTrackTillDegrees(700, 3, 50, 0.65, 10, -60)
    SinglePDTrackTillDegrees(300, 3, 50, 0.4, 10, -60)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -60)
    MoveToAngle(190, 190, -500, -500)
    while leftSensor.reflection() != 11:
        leftMotor.dc(50)
        rightMotor.dc(50)
    MoveToAngle(300, 300, 700, 680)
    leftMedMotor.run(1000)
    time.sleep(2)
    leftMedMotor.hold()
    MoveToAngle(70, 70, 1000, 1000)
    rightMedMotor.run(1000)
    time.sleep(2)
    MoveToAngle(1250, 1250, 700, 680)
    rightMedMotor.run(-1000)
    time.sleep(1)
    rightMedMotor.hold()

def Run2():

    WriteOnScreen("Run 2 Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    # leave quarter circle starting zone
    MoveToAngle(100, 100, -600, -600)
    MoveToAngle(160, 0, -600, 0)
    MoveToAngle(300, 300, -600, -600)
    #linetrace to objective
    SinglePDTrackTillDegrees(1000, 3, 50, 0.65, 10, -75)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.45, 10, -75) # third junction on the left
    MoveToAngle(50, 50, -600, -600) #move a little more to adjust
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -75)
    MoveToAngle(50, 50, -600, -600)
    SinglePDTrackTillDegrees(50, 3, 50, 0.65, 10, -75)
    MoveToAngle(280,280,-600,-600)
    MoveToAngle(0,75,0,-200)
    SinglePDTrackTillDegrees(400, 2, 50, -0.45, -8, -75) #trace with middle sensor 
    SinglePDTrackTillJunction(1, 12, 2, 50, -0.65, -10, -75)
    # parcel drop
    MoveToAngle(100,100,-500,-600)
    MoveToAngle(120, 120, 200,200)# reverse from parcel
    MoveToAngle(0,470,0,600) #turn back
    MoveToAngle(550,550,1000,1000) #wall align
    MoveToAngle(0,140,0,-500) #turn towards line
    MoveToAngle(250,250,-500,-500)
    MoveToAngle(70,0,-500,0)
    SinglePDTrackTillDegrees(100, 2, 50, 0.5, 10, -75) #trace to middle of the path
    rightMedMotor.run(1000) #turn down the attachment
    leftMedMotor.run(-500) #drop the cargo
    time.sleep(1)
    rightMedMotor.hold()
    leftMedMotor.hold()
    SinglePDTrackTillDegrees(200, 2, 50, 0.5, 10, -30)
    SinglePDTrackTillJunction(2, 12, 1, 50, 0.2, 4, -40) #linetrace to cargo sorter
    MoveToAngle(50,50,600,600) # go back to go home
    rightMedMotor.run(-500)
    leftMedMotor.run(500)
    time.sleep(2)
    rightMedMotor.hold()
    leftMedMotor.hold()
    MoveToAngle(550,550,600,600) # go back to go home
    MoveToAngle(330,0,-750,0) # go back to go home
    MoveToAngle(1800,1800,-600,-625) # run back home
    MoveToAngle(2000,2000,-670,-600) # run back home

def Run4():
    WriteOnScreen("Run 4 Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    leftMedMotor.hold()
    MoveToAngle(100, 100, -600, -600)
    MoveToAngle(185, 0, -600, 0)
    MoveToAngle(200, 200, -600, -600)
    SinglePDTrackTillDegrees(1300, 3, 50, 0.65, 10, -55)
    leftMedMotor.run(900)
    time.sleep(1.2)
    leftMedMotor.hold()
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -60)
    MoveToAngle(50, 50, -600, -600)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -60)
    MoveToAngle(50, 50, -600, -600)
    SinglePDTrackTillDegrees(50, 3, 50, 0.65, 10, -60)
    rightMedMotor.run(1000)
    time.sleep(1.2)
    rightMedMotor.hold()
    MoveToAngle(0,40,0,-200)
    SinglePDTrackTillDegrees(650, 3, 50, 0.65, 10, -60)
    MoveToAngle(0,110,0,-600)
    time.sleep(0.3)
    MoveToAngle(600,600,700,700)
    rightMedMotor.run(-1000)
    time.sleep(1)
    rightMedMotor.hold()
    MoveToAngle(0,470,0,-600)
    SinglePDTrackTillDegrees(1500, 1, 50, 0.65, 10, -60)
    MoveToAngle(1500,1500,-1000,-1000)

def Run5():
    WriteOnScreen("Final Run Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    MoveToAngle(100, 100, -600, -600)
    MoveToAngle(155, 0, -600, 0)
    MoveToAngle(300, 300, -600, -600)
    SinglePDTrackTillDegrees(1000, 3, 50, 0.65, 10, -75)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -75)
    MoveToAngle(50, 50, -600, -600)
    SinglePDTrackTillJunction(2, 12, 3, 50, 0.65, 10, -75)
    MoveToAngle(0, 360, 0, -600)
    while leftSensor.reflection() > 15:
        rightMotor.run(-300)
        leftMotor.run(-300)
    MoveToAngle(260, 260, -600, -600)
    rightMedMotor.run(600)
    time.sleep(1.8)
    rightMedMotor.hold()
    MoveToAngle(260, 260, 300, 300)
    rightMedMotor.run(-600)
    time.sleep(1.8)
    rightMedMotor.hold()
    MoveToAngle(0, 590, 0, 300)
    MoveToAngle(1000, 1000, 600, 600)
    time.sleep(0.5)
    MoveToAngle(80, 80, -600, -600)
    MoveToAngle(170, 170, 600, -600)
    MoveToAngle(450, 450, 100, 100)

def ActualRun1():
    WriteOnScreen("Run 1 Ready")
    WaitForPress()
    WriteOnScreen("Launching")
    MoveToAngle(8000,8000,1000,1000)
    MoveToAngle(550,550,-1000,-1000)
    MoveToAngle(200,200,200,200)
    MoveToAngle(150,0,-700,0)
    SinglePDTrackTillJunction(1, 12, 2, 50, -0.65, -10, -75)
    # parcel drop
    MoveToAngle(100,100,-500,-600)
    MoveToAngle(120, 120, 200,200)# reverse from parcel
    MoveToAngle(0,490,0,600) #turn back
    MoveToAngle(550,550,1000,1000) #wall align
    MoveToAngle(0,140,0,-500) #turn towards line
    MoveToAngle(260,260,-500,-500)
    MoveToAngle(80,0,-500,0)
    SinglePDTrackTillDegrees(100, 2, 50, 0.5, 10, -75) #trace to middle of the path
    rightMedMotor.run(1000) #turn down the attachment
    leftMedMotor.run(-500) #drop the cargo
    time.sleep(0.8)
    rightMedMotor.hold()
    leftMedMotor.hold()
    SinglePDTrackTillDegrees(200, 2, 50, 0.5, 10, -30)
    SinglePDTrackTillJunction(2, 12, 1, 50, 0.2, 4, -40) #linetrace to cargo sorter
    MoveToAngle(50,50,600,600) # give spacing
    rightMedMotor.run(-1000)
    time.sleep(0.5)
    rightMedMotor.hold()
    MoveToAngle(550,550,600,600) # go back to go home
    # MoveToAngle(330,0,-750,0) # go back to go home
    # MoveToAngle(1800,1800,-600,-625) # run back home
    # MoveToAngle(2000,2000,-670,-600) # run back home
    rightMedMotor.run(-500)
    time.sleep(0.5)
    rightMedMotor.hold()

ActualRun1()
Run3()
Run4()
Run5()

## Run1()
## Run2()