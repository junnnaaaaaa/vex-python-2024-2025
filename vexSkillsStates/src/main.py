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
intake = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False )
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
    driveTrain.set_timeout(6, SECONDS) #setting timeout to avoid issues with it being stuck
    mogoMech.set(False) #ensuring mogoMech is off at the start of the program
    driveTrain.set_stopping(HOLD) #set stopping to hold for more accurate driving
    driveTrain.drive_for(REVERSE, 100, MM, 100, PERCENT) #reverse quickly to try to bring front intake down
    driveTrain.drive_for(REVERSE, 400, MM, 25, PERCENT)  #reverse to goal
    mogoMech.set(True) #grab goal
    intake.spin(FORWARD) 
    wait(0.2, SECONDS) #give intake time to put on preload and 
    driveTrain.turn_for(LEFT, 0.56, TURNS, 100, PERCENT) #180 turn, also turns so intake is at front to pick up rings
    wait(0.1, SECONDS)
    intake.set_velocity(100, PERCENT)
    driveTrain.drive_for(FORWARD, 1400, MM, 25, PERCENT) #drives to get rings
    intake.set_velocity(30, PERCENT) #slows intake down to avoid flinging rings off
    wait(0.1, SECONDS)
    driveTrain.turn_for(RIGHT, 0.29, TURNS, 40, PERCENT) #90 turn, points towards more rings
    wait(0.1, SECONDS) 
    intake.set_velocity(100, PERCENT) #sets intake back to max speed
    driveTrain.drive_for(FORWARD, 1300, MM, 40, PERCENT) #grabs next ring
    intake.set_velocity(30, PERCENT)#slows intake down to avoid flinging rings off
    driveTrain.turn_for(RIGHT, 0.29, TURNS, 40, PERCENT) #turns to next set of rings
    wait(0.1, SECONDS)
    intake.set_velocity(100, PERCENT) #sets intake back to max speed
    driveTrain.drive_for(FORWARD, 1700, MM, 40, PERCENT) #gets next to rings
    wait(0.5, SECONDS) #waits to allow rings to go into the intake
    #moves back then turns for last ring
    driveTrain.drive_for(REVERSE, 400, MM, 25, PERCENT)  
    driveTrain.turn_for(LEFT, 0.32, TURNS, 40, PERCENT)
    #grabs final ring     
    driveTrain.drive_for(FORWARD, 300, MM, 40, PERCENT)   
    wait(0.5, SECONDS)
    driveTrain.turn_for(LEFT, 0.4, TURNS, 40, PERCENT) #turns to correct angle for putting goal in corner
    #puts goal in corner
    driveTrain.drive_for(REVERSE, 600, MM, 25, PERCENT)  
    mogoMech.set(False)
    #shakes goal and drives out
    driveTrain.drive_for(REVERSE, 200, MM, 100, PERCENT)   
    driveTrain.drive_for(FORWARD, 800, MM, 100, PERCENT)   
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
        