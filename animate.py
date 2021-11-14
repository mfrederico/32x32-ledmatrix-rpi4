import time as t
from datetime import datetime, time
import sys, os, re
from os import walk
from rpi_ws281x import *
import argparse
import mymatrix 

from neopixel import * # See https://learn.adafruit.com/neopixels-on-raspberry-pi/software
from PIL import Image  # Use apt-get install python-imaging to install this

# Folder where animations are stored
animations = 'icons/'

# LED strip configuration:
LED_COUNT      = 1024      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 4     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Speed of movement kind of relates to FPS, in seconds (recommend 0.1-0.3)
SPEED=0.05

# How long to show a complete image or animation for (seconds)
# 7 Seconds is the attention span of most people
DURATION=7

# Size of your matrix
MATRIX_WIDTH=32
MATRIX_HEIGHT=32

myMatrix = mymatrix.getMatrix()

# https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all

# Check that we have sensible width & height
if MATRIX_WIDTH * MATRIX_HEIGHT != len(myMatrix):
  raise Exception("Matrix width x height does not equal length of myMatrix")

def getAnimations(animations):
    for (dirpath, dirnames, filenames) in walk(animations) : break
    return filenames

def allonecolor(strip, color):
  # Paint the entire matrix one color
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
  strip.show()

def rgbColor(r,g,b):
  # Fix for Neopixel RGB->GRB
  return Color(g,r,b)
  #return Color(r,g,b)

def colorTuple(rgbTuple):
  return Color(rgbTuple[0], rgbTuple[1], rgbTuple[2])

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin();
allonecolor(strip, rgbColor(0,0,0))


# File Index (Keep track of where we are)
fidx = 0

# Start creating real-time timers
now = datetime.now()
beginning_of_day = datetime.combine(now.date(), time(0))
timetrack = (now - beginning_of_day).seconds
seccheck  = 0;

# And here we go.
while(True) :

    print ("Timer: ",seccheck - timetrack)
    if (abs(seccheck - timetrack) >= DURATION or seccheck == 0) :
        # After timer runs - Check for new / removed animations icons etc
        filenames = getAnimations(animations);
        if fidx == len(filenames): fidx = 0 

        print("Current Sprite: " + filenames[fidx]);
        timetrack = (now - beginning_of_day).seconds

        # Load the image
        # If the image height doesn't match the matrix, resize it
        loadIm = Image.open(animations + filenames[fidx])
        im = Image.new('RGB',(loadIm.size[0] + MATRIX_WIDTH, MATRIX_HEIGHT))
        im.paste(loadIm,(0, 0, loadIm.size[0], MATRIX_HEIGHT))

        # Cue the next image
        fidx = fidx +1 

    # Timer Housekeeping
    now = datetime.now()
    seccheck = (now - beginning_of_day).seconds
    x = 0

    # Our images are "sprite" format
    # Fill the pixels with goodness
    while x < im.size[0] - MATRIX_WIDTH:
        thissleep       = SPEED
        thisincrement   = MATRIX_WIDTH;

        rg=im.crop((x,0,x+MATRIX_WIDTH, MATRIX_HEIGHT))
        dots=list(rg.getdata())
  
        for i in range(len(dots)):
            strip.setPixelColor(myMatrix[i], colorTuple(dots[i]))

        # Now we have a our strip matrix filled with image data
        strip.show()

        x = x + thisincrement
        t.sleep(thissleep) # Delay between "frames"

