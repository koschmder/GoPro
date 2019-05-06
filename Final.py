#GoPro Photo Mode
#GoPro Capture (HERO7 cameras only)
import asyncio
import time

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

#PASS IN PARSED MESSAGE
commands = "photo;back"
# "video;stationary%video;pan;front"
# "photo;front%photo;left%photo;right"
# "photo;front%video;pan;front"
# "photo;back%video;pan;360%timelapse;back"
speed = 50
videoTime = 5
timeLapse = 20

#         HELPER FUNCTIONS

#DRIVE STRAIGHT
def driveStraight(robot):
    robot.drive_straight(cozmo.util.distance_mm(200), cozmo.util.speed_mmps(speed)).wait_for_completed()
    
#BACK UP
def backUp(robot):
    robot.drive_straight(cozmo.util.distance_mm(-200), cozmo.util.speed_mmps(speed)).wait_for_completed()
    
#TURN AROUND
def turnAround(robot):
    robot.turn_in_place(degrees(180)).wait_for_completed()

#RETURN TO CHARGER
def returnToCharger(robot):
    robot.turn_in_place(degrees(-180)).wait_for_completed()
    charger = None
    # see if Cozmo already knows where the charger is
    if robot.world.charger:
        if robot.world.charger.pose.is_comparable(robot.pose):
            print("Cozmo already knows where the charger is!")
            charger = robot.world.charger
        else:
            pass
    if not charger:
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try:
            charger = robot.world.wait_for_observed_charger(timeout=5)
        except asyncio.TimeoutError:
            print("Didn't see the charger")
        finally:
            look_around.stop()
    if charger:
        # Attempt to drive near to the charger, and then stop.
        action = robot.go_to_object(charger, distance_mm(65.0))
        action.wait_for_completed()
        robot.turn_in_place(cozmo.util.degrees(180)).wait_for_completed()
        robot.drive_straight(cozmo.util.distance_mm(-175), cozmo.util.speed_mmps(50)).wait_for_completed()
        print("Done.")
    
#TAKE PHOTO
def takePhoto(robot):
    robot.say_text("GoPro turn on", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro take photo", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro turn off", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()

#VIDEO SECTION - RUN VIDEO + TAKE VIDEO
#parsing - 0=video; 1=stationary/pan; 2=(optional)=front/back/360
# example commandStr = video;pan;front , video;pan;back , video;pan;360
def startVideo(robot):
    robot.say_text("GoPro turn on", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro start video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
def stopVideo(robot):
    robot.say_text("GoPro stop video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(3)
    robot.say_text("GoPro turn off", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed() 

#TIME LAPSE
#ex commandStr = timelapse;front , timelapse;back , timelapse;left , timelapse;right
def takeTimeLapse(robot):
    robot.say_text("GoPro turn on", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro start time lapse", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(timeLapse)
    robot.say_text("GoPro stop time lapse", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(3)
    robot.say_text("GoPro turn off", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()

    
def cozmo_program(robot: cozmo.robot.Robot):
    robot.drive_off_charger_contacts().wait_for_completed()
    robot.drive_straight(cozmo.util.distance_mm(200), cozmo.util.speed_mmps(50)).wait_for_completed()
    robot.say_text("please Place Go Pro on my lift", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(4)
    
    #parse
    commandList = commands.split('%')
    for command in commandList:
        instructions = command.split(';')
        
        #PHOTO SECTION
        if instructions[0] == "photo":
            robot.say_text("photo program initiated", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
            driveStraight(robot)
            if instructions[1] == "front":
                takePhoto(robot)
                backUp(robot)
            if instructions[1] == "back":
                turnAround(robot)
                takePhoto(robot)
                turnAround(robot)
                backUp(robot)
            if instructions[1] == "left":
                robot.turn_in_place(degrees(90)).wait_for_completed()
                driveStraight(robot)
                takePhoto(robot)
                backUp(robot)
                robot.turn_in_place(degrees(-90)).wait_for_completed()
                backUp(robot)
            if instructions[1] == "right":
                robot.turn_in_place(degrees(-90)).wait_for_completed()
                driveStraight(robot)
                takePhoto(robot)
                backUp(robot)
                robot.turn_in_place(degrees(90)).wait_for_completed()
                backUp(robot)            
            
        #VIDEO SECTION    
        if instructions[0] == "video":
            robot.say_text("video program initiated", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
            driveStraight(robot)
            if instructions[1] == "stationary":
                startVideo(robot)
                time.sleep(videoTime)
                stopVideo(robot)
                backUp(robot)
            if instructions[1] == "pan":
                if instructions[2] == "front":
                    robot.turn_in_place(degrees(90)).wait_for_completed()
                    startVideo(robot)
                    robot.turn_in_place(degrees(-180),None,0,None,degrees(3)).wait_for_completed() 
                    stopVideo(robot)
                    robot.turn_in_place(degrees(90)).wait_for_completed()
                    backUp(robot)
                if instructions[2] == "back":
                    robot.turn_in_place(degrees(-90)).wait_for_completed()
                    startVideo(robot)
                    robot.turn_in_place(degrees(-180),None,0,None,degrees(3)).wait_for_completed() 
                    stopVideo(robot)
                    robot.turn_in_place(degrees(-90)).wait_for_completed()
                    backUp(robot)
                if instructions[2] == "360":
                    startVideo(robot)
                    robot.turn_in_place(degrees(-360),None,0,None,degrees(3)).wait_for_completed() 
                    stopVideo(robot)
                    backUp(robot)            
            
        #TIME LAPSE SECTION
        if instructions[0] == "timelapse":
            robot.say_text("time lapse program initiated", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
            driveStraight(robot)
            if instructions[1] == "front":
                takeTimeLapse(robot)
                backUp(robot)
            if instructions[1] == "back":
                turnAround(robot)
                takeTimeLapse(robot)
                turnAround(robot)
                backUp(robot)
            if instructions[1] == "left":
                robot.turn_in_place(degrees(90)).wait_for_completed()
                driveStraight(robot)
                takeTimeLapse(robot)
                backUp(robot)
                robot.turn_in_place(degrees(-90)).wait_for_completed()
                backUp(robot)
            if instructions[1] == "right":
                robot.turn_in_place(degrees(-90)).wait_for_completed()
                driveStraight(robot)
                takeTimeLapse(robot)
                backUp(robot)
                robot.turn_in_place(degrees(90)).wait_for_completed()
                backUp(robot)
                    
    #AFTER ALL COMMANDS                
    robot.say_text("Please take Go Pro off my lift", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(4)        
    returnToCharger(robot)
        
    
cozmo.run_program(cozmo_program)