from libcamera import Transform, controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
import RPi.GPIO as GPIO
import time
import cv2
import subprocess

TIME_CAPTURING = 0
TIME_STEP = 2
TIME_BLINK = 1
TIME_SHUTDOWN = 5
SAVE_FOLDER_IMG = '/home/Lincos/code/camera/imgs'
SAVE_FOLDER_VIDEO = '/home/Lincos/code/camera/videos'
PHOTO_SIZE = (3840, 2160)
VIDEO_SIZE = (1920, 1080)

is_capturing = False
is_streaming = False

camera = Picamera2()
photo_config = camera.create_still_configuration(
    main={"size": PHOTO_SIZE, "format": 'RGB888'},
    controls={"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast}
)
video_config = camera.create_video_configuration(
    main={"size": VIDEO_SIZE, "format": 'RGB888'},  
    controls={"FrameRate": 30, "AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast}
)
camera.configure(photo_config)
camera.start()

leds = [23, 24]
for led in leds: 
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, GPIO.LOW)

tabs = [13, 6, 26, 19]
for tab in tabs:
	GPIO.setup(tab, GPIO.IN)
	GPIO.setup(tab, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def blinking(led, sleep):
	GPIO.output(led, GPIO.HIGH)
	time.sleep(sleep)
	GPIO.output(led, GPIO.LOW)
	time.sleep(sleep)

def capturing():
	global camera_capture
	filename = SAVE_FOLDER_IMG + '//' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".jpg"
			
	GPIO.output(leds[1], GPIO.HIGH)
	camera.capture_file(filename)
	print(f"save: {filename}")
	time.sleep(TIME_BLINK)
	GPIO.output(leds[1], GPIO.LOW)
	
	time.sleep(TIME_STEP - TIME_BLINK)
	
def start_streaming():
	camera.switch_mode(video_config)
	video_path = SAVE_FOLDER_VIDEO + "//" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".h264"
	encoder = H264Encoder(bitrate=12000000)
	camera.start_recording(encoder, video_path, quality=Quality.HIGH)
	GPIO.output(leds[0], GPIO.LOW)
	GPIO.output(leds[1], GPIO.HIGH)
	while is_streaming:
		time.sleep(1)
		
def stop():
	global is_streaming, is_capturing
	if is_streaming:
		camera.stop_recording()
		is_streaming = False
	is_capturing = False
	GPIO.output(leds[1], GPIO.LOW)
	
def handle_stop(channel):
	stop()

def shutdown():
	if is_streaming:
		camera.stop_recording()

	blinking(leds[0], TIME_SHUTDOWN)
	command = "/usr/bin/sudo /sbin/shutdown -h now"
	
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print("stop")
	
GPIO.add_event_detect(tabs[1], GPIO.FALLING, callback=handle_stop, bouncetime=200)	
	
while True:
	if GPIO.input(tabs[0]) == GPIO.LOW:
		if is_streaming:
			camera.stop_recording()
			is_streaming = False
		if not is_capturing:	
			is_capturing = True
			camera.switch_mode(photo_config)
		
	if GPIO.input(tabs[2]) == GPIO.LOW:
		if is_capturing:
			is_capturing = False
		if not is_streaming:
			is_streaming = True	
			start_streaming()	
			
	if GPIO.input(tabs[3]) == GPIO.LOW:
		shutdown()
	
	if is_capturing:
		capturing()		
	elif not is_streaming:
		blinking(leds[0], TIME_BLINK)
