import threading
from libcamera import Transform, controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
import RPi.GPIO as GPIO
import time

# Конфигурация и настройки
TIME_BLINK = 1
SAVE_FOLDER_IMG = '/home/Lincos/code/camera/imgs'
SAVE_FOLDER_VIDEO = '/home/Lincos/code/camera/videos'
PHOTO_SIZE = (3840, 2160)
VIDEO_SIZE = (1920, 1080)

is_capturing = False
is_streaming = False

# Инициализация камеры и конфигураций
camera = Picamera2()
photo_config = camera.create_still_configuration(
    main={"size": PHOTO_SIZE, "format": 'RGB888'},
    controls={"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast}
)
video_config = camera.create_video_configuration(
    main={"size": VIDEO_SIZE, "format": 'YUV420'},  # Изменено для лучшей производительности
    controls={"FrameRate": 30, "AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast}
)

# Инициализация GPIO
leds = [23, 24]
GPIO.setmode(GPIO.BCM)
for led in leds:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)

tabs = [13, 6, 26, 19]
for tab in tabs:
    GPIO.setup(tab, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Функции записи и выключения
def capturing():
    filename = f"{SAVE_FOLDER_IMG}/{time.strftime('%Y-%m-%d %H:%M:%S')}.jpg"
    GPIO.output(leds[1], GPIO.HIGH)
    camera.capture_file(filename)
    print(f"Фото сохранено: {filename}")
    time.sleep(TIME_BLINK)
    GPIO.output(leds[1], GPIO.LOW)

def start_streaming():
    global is_streaming
    if not is_streaming:
        is_streaming = True
        camera.switch_mode(video_config)
        video_path = f"{SAVE_FOLDER_VIDEO}/{time.strftime('%Y-%m-%d %H:%M:%S')}.h264"
        encoder = H264Encoder(bitrate=8000000)
        camera.start_recording(encoder, video_path, quality=Quality.MEDIUM)
        GPIO.output(leds[0], GPIO.LOW)
        GPIO.output(leds[1], GPIO.HIGH)
        print("Запись видео начата")

def stop_streaming():
    global is_streaming
    if is_streaming:
        camera.stop_recording()
        is_streaming = False
        GPIO.output(leds[1], GPIO.LOW)
        print("Запись видео остановлена")

def shutdown():
    if is_streaming:
        stop_streaming()
    print("Выключение системы")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Обработчики событий кнопок
def handle_capture(channel):
    global is_capturing
    if is_streaming:
        stop_streaming()
    if not is_capturing:
        is_capturing = True
        camera.switch_mode(photo_config)
        capturing()
        is_capturing = False

def handle_stop(channel):
    global is_capturing
    if is_capturing:
        is_capturing = False
    if is_streaming:
        stop_streaming()
    GPIO.output(leds[1], GPIO.LOW)

def handle_start_streaming(channel):
    global is_capturing
    if is_capturing:
        is_capturing = False
    if not is_streaming:
        threading.Thread(target=start_streaming).start()

def handle_shutdown(channel):
    shutdown()

# Назначаем события для GPIO
GPIO.add_event_detect(tabs[0], GPIO.FALLING, callback=handle_capture, bouncetime=200)
GPIO.add_event_detect(tabs[1], GPIO.FALLING, callback=handle_stop, bouncetime=200)
GPIO.add_event_detect(tabs[2], GPIO.FALLING, callback=handle_start_streaming, bouncetime=200)
GPIO.add_event_detect(tabs[3], GPIO.FALLING, callback=handle_shutdown, bouncetime=200)

# Основной поток
try:
    while True:
        if not is_streaming:
            GPIO.output(leds[0], GPIO.HIGH)
            time.sleep(TIME_BLINK)
            GPIO.output(leds[0], GPIO.LOW)
            time.sleep(TIME_BLINK)
except KeyboardInterrupt:
    GPIO.cleanup()
