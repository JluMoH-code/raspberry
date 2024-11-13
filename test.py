from libcamera import Transform, controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
import RPi.GPIO as GPIO
import time
import cv2

TIME_CAPTURING = 0
TIME_STEP = 3
TIME_BLINK = 1
TIME_SHUTDOWN = 5
SAVE_FOLDER_IMG = '/home/Lincos/code/camera/imgs'
SAVE_FOLDER_VIDEO = '/home/Lincos/code/camera/videos'
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
#photo_config = get_config(camera, 1, SIZE, "photo")
video_config = get_config(camera, SIZE, "video")
camera.configure(video_config)
camera.start()

video_path = SAVE_FOLDER_VIDEO + "//" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".h264"

encoder = H264Encoder(bitrate=12000000)

camera.start_recording(encoder, video_path, quality=Quality.HIGH)
time.sleep(10)
camera.stop_recording()

