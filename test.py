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

camera_capture = Picamera2()
camera_capture.video_configuration.main.size = (1920, 1080)
camera_capture.start()


video_path = SAVE_FOLDER_VIDEO + "//" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".avi"
output = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"MPEG"), 30, SIZE)
			
while True:
	
		
	frame = camera_capture.capture_array()
	output.write(frame)

	print("sss")
