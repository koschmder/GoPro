import cozmo
import socket
import errno
from socket import error as socket_error

#need to get movement info
from cozmo.util import degrees, distance_mm, speed_mmps

instructions = "chase;other;chase"

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
            instructions = data.split(';')
            #check the name:
            if command[0] == myName:
                robot.drive_straight(cozmo.util.distance_mm(300), cozmo.util.speed_mmps(50)).wait_for_completed()
                robot.turn_in_place(degrees(-180)).wait_for_completed()
                robot.say_text("please Place Go Pro on my lift", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                time.sleep(4)
                robot.say_text("Cozmo in position to take video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                time.sleep(1)
                robot.say_text("Go Pro turn on", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                time.sleep(6)
                robot.say_text("Go Pro start video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()

            if command[1] == otherName:
                robot.turn_in_place(degrees(-360)).wait_for_completed()
                robot.set_head_angle(degrees(20)).wait_for_completed()
                robot.set_head_angle(degrees(0)).wait_for_completed()                
                robot.turn_in_place(degrees(-360)).wait_for_completed()
                robot.play_anim(name="anim_poked_giggle").wait_for_completed()
                
            if command[2] == myName:
                robot.say_text("Go Pro stop video", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()
                ime.sleep(3)
                robot.say_text("Go Pro turn off", play_excited_animation=False, use_cozmo_voice=False, duration_scalar=0.6, voice_pitch=0.3, in_parallel=False, num_retries=0).wait_for_completed()                
                    
cozmo.run_program(cozmo_program)