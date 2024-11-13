from libcamera import Transform, controls
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

TIME_CAPTURING = 0
TIME_STEP = 3
TIME_BLINK = 1
TIME_SHUTDOWN = 5
SAVE_FOLDER_IMG = '/home/pi/code/camera/imgs/'
SIZE = (1920, 1080)

def get_config(camera, size, form):

	if form == "video": 
		camera_config = camera.create_video_configuration(
		main={                                  # основной поток
			"size": size,
			"format": 'RGB888'
		},               
		#transform=Transform(hflip=1, vflip=1),  # отражение по горизонтали/вертикали
		#buffer_count=16,                         # хранимый буфер кадров, больше -- плавнее
		queue=True,
		controls={
			"FrameRate": 60,
			#"FrameDurationLimits": (33333, 33333),    # microseconds per frame
			"AfMode": controls.AfModeEnum.Continuous,
			"AfSpeed": controls.AfSpeedEnum.Fast,
		},
		)  
 							   
	return camera_config

camera = Picamera2()
photo_config = get_config(camera, SIZE, "photo")
camera.configure(photo_config)

camera.start_and_capture_file(SAVE_FOLDER_IMG + "test.jpg")