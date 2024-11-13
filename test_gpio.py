import gpiod
import time
import RPi.GPIO

print(RPi.GPIO.VERSION)
'''
leds = [23, 24]
chip = gpiod.Chip('gpiochip4')

for led in leds:
	chip.get_line(led).request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

buttons = [13, 6, 26, 19]
for button in buttons:
	chip.get_line(button).request(consumer="BUTTON", type=gpiod.LINE_REQ_DIR_IN)

while True:

	if chip.get_line(buttons[0]).get_value() == 1:
		print("button 1")
		
	if chip.get_line(buttons[1]).get_value() == 1:
		print("button 2")
		
	if chip.get_line(buttons[2]).get_value() == 1:
		print("button 3")
		
	if chip.get_line(buttons[3]).get_value() == 1:
		print("button 4")
	'''
