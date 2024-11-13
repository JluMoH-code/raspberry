import serial
import cv2
import time
# from struct import *

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
#from matplotlib import pyplot as plt

# import datetime
import timeit
import RPi.GPIO as GPIO

chan_list = 15 
chan_list2 = 18 
  
GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)
#chan_list = [15]  
GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list2, GPIO.OUT)
#chan_list2 = [18]  

GPIO.setup(26, GPIO.IN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""
from Tkinter import *  
def click_button():
    global sel
    print('cl')
    sel = 's'
    #clicks += 1
    #window.title("Clicks {}".format(clicks))
    
def click_close():
    global sel
    print('cl')
    sel = 'x'


def nothing(*arg):
   #print("br",br)
   # print("co",co)
    pass

def blit(dest, src, loc):
    pos = [i if i >= 0 else None for i in loc]
    neg = [-i if i < 0 else None for i in loc]
    target = dest[[slice(i,None) for i in pos]]
    src = src[[slice(i, j) for i,j in zip(neg, target.shape)]]
    target[[slice(None, i) for i in src.shape]] = src
    return dest
    
"""    

def nothing(*arg):
   #print("br",br)
   # print("co",co)
    pass

def ftrue():
    GPIO.output(chan_list, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(chan_list, GPIO.LOW)
    time.sleep(0.5) 
    GPIO.output(chan_list, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(chan_list, GPIO.LOW)
    time.sleep(0.5) 
    GPIO.output(chan_list, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(chan_list, GPIO.LOW)
    time.sleep(0.5) 
    GPIO.output(chan_list, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(chan_list, GPIO.LOW)
    time.sleep(0.5)  
              
    
def shutdown():
    ftrue()
    print("stop")
    time.sleep(3)   
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    # print output    
    print("stop")
    

cv2.namedWindow( "Set" )
cv2.moveWindow("Set", 10, 100)
#cv2.resizeWindow("Set", 80, 60)
cv2.createTrackbar('br', 'Set', 0, 100, nothing) 
cv2.createTrackbar('co', 'Set', 0, 100, nothing)
cv2.createTrackbar('ex', 'Set', 0, 2, nothing)  
#cv2.createTrackbar('r8', 'Set', 0, 200, nothing)
cv2.setTrackbarPos('br', 'Set', 58) 
cv2.setTrackbarPos('co', 'Set', 95)

camera = PiCamera()

camera.resolution = (1296, 972)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size= (1296, 972))
#rawCapture = PiRGBArray(camera, size= (1296, 972))
#camera.resolution = (1920, 1080)
#camera.framerate = 20
#rawCapture = PiRGBArray(camera, size= (1920, 1080))
#rawCapture = PiRGBArray(camera, size= (1296, 972))


camera.brightness = 88
camera.preview_fullscreen = False
camera.preview_window = (50, 50, 640, 480)

camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

ftrue()  

#camera.resolution = (1248, 1088)
camera.resolution = (1200, 1000)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1200, 1000))

#camera.resolution = (1920, 1080)
#camera.framerate = 30
#rawCapture = PiRGBArray(camera, size=(1920, 1080))
camera.resolution = (2592, 1944)
#camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(2592, 1944))
#ser = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=3.0)

#camera.preview_window = (0, 0, 192, 108)
#while True:
t = 0
f = 0
s = 0
sn = 0
sel = 'n'
#cv2.namedWindow( "Set" )
#cv2.moveWindow("Set", 10, 100)
#cv2.resizeWindow("Set", 180, 160)

#window = Tk()  
#window.geometry('200x50+20+20')
#window.title("GUI")
#closeButton = Button(text="Close",command=click_close)
#closeButton.pack(side=RIGHT, padx=5, pady=5)
#okButton = Button(text="Save",command=click_button)
#okButton.pack(side=RIGHT)
#camera.stop_preview()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    a = timeit.default_timer()   #print("start")    #print(timeit.default_timer()-a)        
    img = frame.array            #print(timeit.default_timer()-a)
    key = cv2.waitKey(10)        #& 0xFF   # print('key - ',key)   # if sel == 's':
    s = s + 1
    timev = 6 
    
    br = cv2.getTrackbarPos('br', 'Set')
    camera.brightness = br
    co = cv2.getTrackbarPos('co', 'Set')
    camera.contrast = co
    
    cv2.imshow("Set"  ,   img)
    #fn = today.strftime('%m-%d-%H.%M.%S')
    #b = GPIO.input(26)
    print(sel) 
        
    if  GPIO.input(26) == GPIO.LOW:
       #GPIO.output(chan_list, GPIO.HIGH)
        sel = 'r'
        s = 0
        print('R') 
    if  GPIO.input(19) == GPIO.LOW:
        sel = 'n'
       #GPIO.output(chan_list, GPIO.HIGH)
        print('N')  
    if  GPIO.input(13) == GPIO.LOW:
        sel = 'e'
        print('E')  
        shutdown()
        break
    
    if sel == 'n':
        sn = sn + 1
        if sn == 6:
            GPIO.output(chan_list, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(chan_list, GPIO.LOW)
            sn = 0         
    if (s) == 5:
        if sel == 'r':
            t = t + 1
            camera.capture('v'+str(t)+'.jpg')
            GPIO.output(chan_list2, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(chan_list2, GPIO.LOW)
            s = 0
            if (t) == 500:
               t = 0
               shutdown()
               break
    rawCapture.truncate(0)
cv2.destroyAllWindows()   
   
