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
#Assigning ports
#assigning motors
rightBack = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
rightFront = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
rightTop = Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)
leftBack = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
leftFront = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
leftTop = Motor(Ports.PORT14, GearSetting.RATIO_6_1, True)
intake = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
#assigning motor groups for drivetrain and intake

rightSide = MotorGroup(rightBack, rightFront, rightTop)
leftSide = MotorGroup(leftBack, leftFront, leftTop)
#assigning non motor ports
armMotor = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
control = Controller(PRIMARY)
slam = DigitalOut(brain.three_wire_port.a)
mogoMech = DigitalOut(brain.three_wire_port.b)
inertia = Inertial(Ports.PORT2)
driveTrain = DriveTrain(leftSide, rightSide, 319.19, 295, 230, MM, 1.3333333333333333)
#movement functions for auto

#test change
   
def sgn(x): #sign function. makes everything positive or negative one
    if x == 0:
        return 0
    return (x > 0) * 2 - 1
def preAuto():
   # Start calibration.
    inertia.calibrate()
# Print that the Inertial Sensor is calibrating while
# waiting for it to finish calibrating.
    while inertia.is_calibrating():
        control.screen.clear_screen()
        control.screen.set_cursor(1,1)
        control.screen.print("Inertial Sensor Calibrating")
        wait(50, MSEC)
    control.screen.clear_screen()
    control.screen.set_cursor(1,1)
    control.screen.print("Inertial Sensor Done")
def auto():
    #note, reverse left and right
    mogoMech.set(False)
    leftSide.set_stopping(HOLD)
    rightSide.set_stopping(HOLD)
    driveTrain.drive_for(REVERSE, 200, MM, 100, PERCENT) #jerk backward to try to bring the front intake down
    driveTrain.drive_for(REVERSE, 1800, MM, 30, PERCENT) #mooves backwards to the goal
    mogoMech.set(True) #grabs goal
    driveTrain.turn_for(LEFT, 0.34, TURNS, 30, PERCENT) #0.3 roughly is 90 degrees, also turns to grab goal
    intake.set_velocity(100, PERCENT)
    driveTrain.drive_for(FORWARD, 100, MM, 30, PERCENT) #drives forward a bit towards next ring
    intake.spin(FORWARD)
    wait(0.5, SECONDS) # gives the intake time to flick the front intake down, incase the first bit doesnt work. also puts the preload on the goal
    driveTrain.drive_for(FORWARD, 1300, MM, 70, PERCENT) #grabs first ring
    driveTrain.drive_for(FORWARD, 100, MM, 30, PERCENT) #slows down to ensure grabbing
    driveTrain.turn_for(LEFT, 0.32, TURNS, 30, PERCENT)  #turns to last ring
    driveTrain.drive_for(FORWARD, 450, MM, 70, PERCENT) #moves to grab last ring
    wait(1, SECONDS) #since the robot risks crossing the line, we cant move very far, so we have to give it time for the intake to work
    driveTrain.drive_for(REVERSE, 650, MM, 50, PERCENT)#reverses back away from stack
    driveTrain.turn_for(LEFT, 0.34, TURNS, 30, PERCENT) #turns to direction for touching pole
    #final jiggle to make sure all rings go on
    driveTrain.drive_for(REVERSE, 70, MM, 100, PERCENT)
    driveTrain.drive_for(FORWARD, 70, MM, 100, PERCENT)
    mogoMech.set(False) #lets go of mogo
    driveTrain.drive_for(FORWARD, 2000, MM, 30, PERCENT) #drives to touch middle structure. 
    #note: leave intake on so it climbs the structure, ensuring that its touching it
        
def driveA():
    mogoToggle = False
    canMogo = True
    slamToggle = False
    canSlam = True
    canSpin = True
    spinToggle = False
    while True:
        if mogoToggle:
            mogoMech.set(True)
        else:
            mogoMech.set(False)
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
        if control.buttonR1.pressing():
            intake.set_velocity(100, PERCENT)
            spinToggle = False
        elif control.buttonR2.pressing():
            intake.set_velocity(-100, PERCENT)
            spinToggle = False
        else:
            if control.buttonDown.pressing() and canSpin:
                canSpin = False 
                if not spinToggle:
                    spinToggle = True
                elif spinToggle:
                    spinToggle = False
            elif not control.buttonDown.pressing():
                canSpin = True
            if spinToggle:
                intake.set_velocity(100, PERCENT)
            else:
                intake.stop()
        if control.buttonL1.pressing():
            armMotor.set_velocity(100, PERCENT)
        elif control.buttonL2.pressing():
            armMotor.set_velocity(-100, PERCENT)
        else:
            armMotor.set_velocity(0)
def inertial():
    global multi, difference
    a = 0
    while True:
        control.screen.set_cursor(1,1)
        brain.screen.set_cursor(1,1)
        control.screen.print("inertial heading: " + str(round(inertia.heading(), 2)))
        control.screen.new_line()
        if comp.is_autonomous():
            #a += 1
            #control.screen.print(multi)
            #control.screen.new_line()
            #control.screen.print(str(round(difference, 1)))
            #control.screen.new_line()
            #control.screen.print(a)
            pass
        wait(0.1, SECONDS)
        control.screen.clear_screen()
        brain.screen.clear_screen
def drive():
    dTaskA = Thread( driveA )
    while( comp.is_driver_control() and comp.is_enabled()):
        wait(10, MSEC)
    dTaskA.stop()
thread = Thread(inertial)
comp = Competition(drive, auto)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
preAuto()
        
