from FrameCapture import PiCamera2Capture
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time
import cv2

TIME_CAPTURING = 0
TIME_STEP = 3
TIME_BLINK = 1
TIME_SHUTDOWN = 5
SAVE_FOLDER_IMG = '/home/user/code/camera/imgs'
SAVE_FOLDER_VIDEO = '/home/user/code/camera/videos'
SIZE = (1920, 1080)

is_capturing = False
is_streaming = False
output = None

camera_capture = PiCamera2Capture(mode=2, form="video", size=SIZE)

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

for i in range(4):
	blinking(leds[0], TIME_BLINK)

def capturing():
	filename = SAVE_FOLDER_IMG + '//' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".jpg"
	
	GPIO.output(leds[1], GPIO.HIGH)
	camera_capture.capture_file(filename)
	print(f"save: {filename}")
	time.sleep(TIME_BLINK)
	GPIO.output(leds[1], GPIO.LOW)
	
	time.sleep(TIME_STEP - TIME_BLINK)
	
def shutdown():
	blinking(leds[0], TIME_SHUTDOWN)
	command = "/usr/bin/sudo /sbin/shutdown -h now"
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print("stop")
	
	
while True:
	if GPIO.input(tabs[0]) == GPIO.LOW:
		if is_streaming:
			is_streaming = False
			output.release()
		is_capturing = True
		
	if GPIO.input(tabs[1]) == GPIO.LOW:
		if is_capturing:
			is_capturing = False
		elif is_streaming:
			is_streaming = False
			output.release()
			
		GPIO.output(leds[1], GPIO.LOW)
			
	#if GPIO.input(tabs[2]) == GPIO.LOW:
	#	if not is_streaming:
	#		is_streaming = starting = True
	
	if GPIO.input(tabs[3]) == GPIO.LOW:
		shutdown()
	
	if is_capturing:
		capturing()		
	elif is_streaming:
		if starting:
			video_path = SAVE_FOLDER_VIDEO + "//" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".avi"
			output = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"MPEG"), 30, SIZE)
			starting = False
			GPIO.output(leds[1], GPIO.HIGH)
			print("starting")
		
		frame = camera_capture.camera.capture_array()
		output.write(frame)
		print("Video capturing")
	else:
		blinking(leds[0], TIME_BLINK)

