import time as t
import json
from datetime import datetime, time
import sys, os, re
from os import walk
from rpi_ws281x import *
import argparse
import mymatrix 

from neopixel import * # See https://learn.adafruit.com/neopixels-on-raspberry-pi/software
from PIL import Image, ImageDraw, ImageFont, ImageOps  # Use apt-get install python-imaging to install this

# LED strip configuration:
LED_COUNT      = 1024      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 4     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Speed of movement kind of relates to FPS, in seconds (recommend 0.1-0.3)
SPEED=.3

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

# Start creating real-time timers
now = datetime.now()

# smallfont = ImageFont.truetype('fonts/space-harrier-original.ttf', 8)
smallfont = ImageFont.truetype('fonts/raster.ttf', 8)

weather = "-"

# And here we go.
while(True) :
    x = 0;

    now = datetime.now()
    hour = now.strftime("%H")
    min  = now.strftime("%M")
    sec  = now.strftime("%S")

    # build a seconds bar of percent across the top or something

    hhmm = now.strftime("%H:%M")

    # Create a new image (I hope garbage collection in python is good!)
    im = Image.new('RGBA',[MATRIX_WIDTH, MATRIX_HEIGHT]);

    d1 = ImageDraw.Draw(im)

    left    = 0,0
    right   = 32,32
    # d1.ellipse([left, right], fill = (130,130,130))

    if os.path.exists(sys.argv[1] + "/current-32x32.png"):
        try: 
            loadIm = Image.open(sys.argv[1] + "/current-32x32.png")
            im.paste(loadIm,(0,0))
        except:
            print("Couldn't load image file.. will try again later")       

        with open(sys.argv[1]+'/current_weather.json', 'r') as f:
            
            try: 
                array   = json.load(f)
                weather = (array['current']['condition']['text'])
                temp    = int(array['current']['temp_f'])
                msgwidth, msgheight = d1.textsize(weather,font=smallfont)
                d1.text(((MATRIX_WIDTH - msgwidth) / 2, MATRIX_HEIGHT - msgheight-2), weather, font=smallfont, fill =(0, 0, 120))
                msgwidth, msgheight = d1.textsize(str(temp),font=smallfont)
                msgwidth, msgheight = d1.textsize(str(temp))
                d1.text(((MATRIX_WIDTH - msgwidth) / 2, (MATRIX_HEIGHT - msgheight) / 2), str(temp), fill =(1, 1, 1))
            except:
                print("Could not decode json!")

    # Hour / Minute
    msgwidth, msgheight = d1.textsize(hhmm)

    # drop shadow
    d1.text((((MATRIX_WIDTH - msgwidth) / 2)+1, 1), hhmm, fill=(0, 0, 0))
    d1.text(((MATRIX_WIDTH - msgwidth) / 2, 0), hhmm, fill=(150, 150, 150))

    # Seconds
    # msgwidth, msgheight = d1.textsize(sec)
    # d1.text(((MATRIX_WIDTH - msgwidth) / 2, (((MATRIX_HEIGHT - msgheight) / 2) + msgheight)-6), sec, fill=(150, 150, 150))

    # hmm.. I may have "wired" my pixels backwards
    im = ImageOps.mirror(im)

    # Convert my image data into pixels
    dots=list(im.getdata())
    im.close()

    for i in range(len(dots)):
        strip.setPixelColor(myMatrix[i], colorTuple(dots[i]))

    # Now we have a our strip matrix filled with image data
    strip.show()

    t.sleep(SPEED) # Delay between "frames"
