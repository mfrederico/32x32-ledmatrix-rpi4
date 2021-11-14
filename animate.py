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

# Speed of movement, in seconds (recommend 0.1-0.3)
SPEED=0.05

# Size of your matrix
MATRIX_WIDTH=32
MATRIX_HEIGHT=32

myMatrix = mymatrix.getMatrix()

# https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all

# Check that we have sensible width & height
if MATRIX_WIDTH * MATRIX_HEIGHT != len(myMatrix):
  raise Exception("Matrix width x height does not equal length of myMatrix")

def allonecolour(strip,colour):
  # Paint the entire matrix one colour
  for i in range(strip.numPixels()):
    strip.setPixelColor(i,colour)
  strip.show()

def colour(r,g,b):
  # Fix for Neopixel RGB->GRB, also British spelling
  return Color(g,r,b)
  #return Color(r,g,b)

def colourTuple(rgbTuple):
  return Color(rgbTuple[0],rgbTuple[1],rgbTuple[2])

def initLeds(strip):
  # Intialize the library (must be called once before other functions).
  strip.begin()
  # Wake up the LEDs by briefly setting them all to white
  allonecolour(strip,colour(0,0,0))
  #t.sleep(0.01)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
initLeds(strip)

for (dirpath, dirnames, filenames) in walk(animations) : break

fidx = 0
now = datetime.now()
beginning_of_day = datetime.combine(now.date(), time(0))
timetrack = (now - beginning_of_day).seconds
seccheck  = 0;

loadIm = Image.open(animations + filenames[0])
# And here we go.
while(True) :

    print ("Timer: ",seccheck - timetrack)
    if (abs(seccheck - timetrack) >= 10 or seccheck == 0) :
        if fidx == len(filenames): fidx = 0 
        print("Running: " + filenames[fidx]);
        allonecolour(strip, colour(0,0,0))
        # Load the image
        loadIm = Image.open(animations + filenames[fidx])
        fidx = fidx +1
        timetrack = (now - beginning_of_day).seconds

        # If the image height doesn't match the matrix, resize it
        origIm = loadIm.copy()
        im = Image.new('RGB',(origIm.size[0] + MATRIX_WIDTH,MATRIX_HEIGHT))
        im.paste(origIm,(0, 0, origIm.size[0], MATRIX_HEIGHT))

    now = datetime.now()
    seccheck = (now - beginning_of_day).seconds

    x=0
    while x < im.size[0] - MATRIX_WIDTH:
      thissleep=SPEED
      thisincrement=MATRIX_WIDTH;

      rg=im.crop((x,0,x+MATRIX_WIDTH,MATRIX_HEIGHT))
      dots=list(rg.getdata())
  
      for i in range(len(dots)):
        strip.setPixelColor(myMatrix[i],colourTuple(dots[i]))

      strip.show()

      x = x + thisincrement
      t.sleep(thissleep)

#except (KeyboardInterrupt, SystemExit):
#  print "Stopped"
#  allonecolour(strip,colour(0,0,0))

