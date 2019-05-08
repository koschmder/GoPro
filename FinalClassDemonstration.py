import cozmo
import socket
import errno
from socket import error as socket_error

#need to get movement info
from cozmo.util import degrees, distance_mm, speed_mmps



#INPUTS

#commands = "chase&photo;front%video;stationary"
# "chase&video;pan;front%photo;back"
# "chase&photo;left%photo;right%video;pan;360"

#How fast cozmo moves when moving forward & back
speed = 50
#Length of video to be taken (seconds)
videoTime = 5
#Length of timeLapse to be taken (seconds)
timeLapse = 20



# HELPER FUNCTIONS



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
    #looks for charger
    charger = None
    # see if Cozmo already knows where the charger is
    if robot.world.charger:
        if robot.world.charger.pose.is_comparable(robot.pose):
            print("Cozmo already knows where the charger is!")
            charger = robot.world.charger
        else:
            pass
    # look for charger here
    if not charger:
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try:
            charger = robot.world.wait_for_observed_charger(timeout=5)
        except asyncio.TimeoutError:
            print("Didn't see the charger")
        finally:
            look_around.stop()
    # if charger, dock with it
    if charger:
        # Attempt to drive near to the charger, and then stop.
        action = robot.go_to_object(charger, distance_mm(65.0))
        action.wait_for_completed()
        robot.turn_in_place(cozmo.util.degrees(180)).wait_for_completed()
        robot.drive_straight(cozmo.util.distance_mm(-175), cozmo.util.speed_mmps(50)).wait_for_completed()
        print("Done.")
    
#TAKE PHOTO - cozmo voice commands to GoPro
def takePhoto(robot):
    robot.say_text("GoPro turn on", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro take photo", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro turn off", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()

#VIDEO SECTION - cozmo voice commands to GoPro
#separate functions to start and stop to ensure video captures select action
def startVideo(robot):
    robot.say_text("GoPro turn on", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(8)
    robot.say_text("GoPro start video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    
def stopVideo(robot):
    robot.say_text("GoPro stop video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
    time.sleep(3)
    robot.say_text("GoPro turn off", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed() 

#TIME LAPSE - cozmo voice commands to GoPro
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
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket_error as msg:
        robot.say_text("socket failed" + msg).wait_for_completed()
    ip = "10.0.1.10"
    port = 5000
    
    try:
        s.connect((ip, port))
    except socket_error as msg:
        robot.say_text("socket failed to bind").wait_for_completed()
    cont = True
    
    robot.say_text("ready").wait_for_completed()    
    
    #SET COZMO's NAME
    myName = 'chase'
    while cont:
        bytedata = s.recv(4048)
        #data = str(bytedata)
        data = bytedata.decode('utf-8')
        if not data:
            cont = False
            s.close()
            quit()
        else:
            #---------------------------------------------------------
            #This is where you need to adjust the program
            #---------------------------------------------------------
            print(data)
            instructions = data.split('&')
            if len(instructions) == 2:
                if instructions[0] == myName:
                    robot.drive_off_charger_contacts().wait_for_completed()
                    robot.drive_straight(cozmo.util.distance_mm(200), cozmo.util.speed_mmps(50)).wait_for_completed()
                    robot.say_text("please Place Go Pro on my lift", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                    time.sleep(4)
                    #split second part of instructions into separate command list (commands for photo/video/TL)
                    commands = instructions[1].split("%")
                    for command in commands:
                        #split separate commands into individual pieces
                        message = command.split(";")
                        
            
            
                        #PHOTO SECTION 
                        #step 1 = "photo"
                        #step 2 = "front, back, left or right"
                        #return to original position in front of charger
                        if message[0] == "photo":
                            robot.say_text("photo program initiated", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                            driveStraight(robot)
                            if message[1] == "front":
                                takePhoto(robot)
                                backUp(robot)
                            if message[1] == "back":
                                turnAround(robot)
                                takePhoto(robot)
                                turnAround(robot)
                                backUp(robot)
                            if message[1] == "left":
                                robot.turn_in_place(degrees(90)).wait_for_completed()
                                driveStraight(robot)
                                takePhoto(robot)
                                backUp(robot)
                                robot.turn_in_place(degrees(-90)).wait_for_completed()
                                backUp(robot)
                            if message[1] == "right":
                                robot.turn_in_place(degrees(-90)).wait_for_completed()
                                driveStraight(robot)
                                takePhoto(robot)
                                backUp(robot)
                                robot.turn_in_place(degrees(90)).wait_for_completed()
                                backUp(robot)            
                            
                        # VIDEO SECTION
                        # step 1 = "video"
                        # step 2 = "stationary or pan"
                        # step 3 = "front, back or 360"
                        # return to original position in front of charger
                        if message[0] == "video":
                            robot.say_text("video program initiated", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                            driveStraight(robot)
                            if message[1] == "stationary":
                                startVideo(robot)
                                time.sleep(videoTime)
                                stopVideo(robot)
                                backUp(robot)
                            if message[1] == "pan":
                                if message[2] == "front":
                                    robot.turn_in_place(degrees(90)).wait_for_completed()
                                    startVideo(robot)
                                    robot.turn_in_place(degrees(-180),None,0,None,degrees(3)).wait_for_completed() 
                                    stopVideo(robot)
                                    robot.turn_in_place(degrees(90)).wait_for_completed()
                                    backUp(robot)
                                if message[2] == "back":
                                    robot.turn_in_place(degrees(-90)).wait_for_completed()
                                    startVideo(robot)
                                    robot.turn_in_place(degrees(-180),None,0,None,degrees(3)).wait_for_completed() 
                                    stopVideo(robot)
                                    robot.turn_in_place(degrees(-90)).wait_for_completed()
                                    backUp(robot)
                                if message[2] == "360":
                                    startVideo(robot)
                                    robot.turn_in_place(degrees(-360),None,0,None,degrees(3)).wait_for_completed() 
                                    stopVideo(robot)
                                    backUp(robot)            
                            
                        #TIME LAPSE SECTION
                        # step 1 = "timelapse"
                        # step 2 = "front, back, left or right"
                        # return to original position in front of charger
                        if message[0] == "timelapse":
                            robot.say_text("time lapse program initiated", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                            driveStraight(robot)
                            if message[1] == "front":
                                takeTimeLapse(robot)
                                backUp(robot)
                            if message[1] == "back":
                                turnAround(robot)
                                takeTimeLapse(robot)
                                turnAround(robot)
                                backUp(robot)
                            if message[1] == "left":
                                robot.turn_in_place(degrees(90)).wait_for_completed()
                                driveStraight(robot)
                                takeTimeLapse(robot)
                                backUp(robot)
                                robot.turn_in_place(degrees(-90)).wait_for_completed()
                                backUp(robot)
                            if message[1] == "right":
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