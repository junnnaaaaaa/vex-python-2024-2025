# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Paxton Bennison                                              #
# 	Created:      7/11/2024, 8:34:42 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math as m
# Brain should be defined by default
brain=Brain()
rightBack = Motor(Ports.PORT10, GearSetting.RATIO_6_1, True)
rightFront = Motor(Ports.PORT8, GearSetting.RATIO_6_1, True)
rightTop = Motor(Ports.PORT9, GearSetting.RATIO_6_1, False)
leftBack = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
leftFront = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
leftTop = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
intake= Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
rightSide = MotorGroup(rightBack, rightFront, rightTop)
leftSide = MotorGroup(leftBack, leftFront, leftTop)
armMotor = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
control = Controller(PRIMARY)
flap = DigitalOut(brain.three_wire_port.h)
mogoMech = DigitalOut(brain.three_wire_port.g)
def sgn(x):
    if x == 0:
        return 0
    return (x > 0) * 2 - 1
def preAuto():
    pass
def auto():
    armMotor.spin_for(FORWARD, 300, DEGREES)
def drive():
    mogoToggle = False
    canMogo = True
    slamToggle = False
    canSlam = True
    while True:
        if mogoToggle:
            mogoMech.set(True)
        else:
            mogoMech.set(False)
        if slamToggle:
            flap.set(True)
        else:
            flap.set(False)
        rightSide.set_stopping(COAST)
        leftSide.set_stopping(COAST)
        rightSide.spin(FORWARD)
        leftSide.spin(FORWARD)
        axis3 = control.axis3.position()
        axis1 = ((m.e**(-2.3+2.3*abs(control.axis1.position()/100)))*sgn(control.axis1.position()/100))*100
        leftSide.set_velocity(axis3-axis1, PERCENT)
        rightSide.set_velocity(axis3+axis1, PERCENT)
        intake.spin(FORWARD)
        armMotor.spin(FORWARD)
        if control.buttonA.pressing() and canMogo:
            canMogo = False
            if not mogoToggle:
                mogoToggle = True
            elif mogoToggle:
                mogoToggle = False
        elif not control.buttonA.pressing():
            canMogo = True
        if control.buttonB.pressing() and canSlam:
            canSlam = False
            if not slamToggle:
                slamToggle = True
            elif slamToggle:
                slamToggle = False
        elif not control.buttonB.pressing():
            canSlam = True     
        if control.buttonR1.pressing():
            intake.set_velocity(100, PERCENT)
        elif control.buttonR2.pressing():
            intake.set_velocity(-100, PERCENT)
        else:
            intake.stop()
        if control.buttonL1.pressing():
            armMotor.set_velocity(100, PERCENT)
        elif control.buttonL2.pressing():
            armMotor.set_velocity(-100, PERCENT)
        else:
            armMotor.set_velocity(0)
    
comp = Competition(drive(), auto)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
