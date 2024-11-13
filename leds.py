import RPi.GPIO as GPIO
import time


led_1 = 23
led_2 = 24 
  
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_1, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_2, GPIO.OUT)

def blink_led(led_pin, sleep_time):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(sleep_time)
    GPIO.output(led_pin, GPIO.LOW)

tabs = [6, 13, 19, 26]
for tab in tabs:
	GPIO.setup(tab, GPIO.IN)
	GPIO.setup(tab, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	if GPIO.input(tabs[3]) == GPIO.LOW:
		blink_led(led_1, 1)
