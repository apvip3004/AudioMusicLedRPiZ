#!/usr/bin/env python3
import pyaudio
import numpy as np
import struct
from rpi_ws281x import *

# MIC configuration:
CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RMS_SENS = 5000000
#RMS_SENS = 25240000

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 13      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,LED_DMA,LED_INVERT,LED_BRIGHTNESS,LED_CHANNEL)
strip.begin()

while True:
   data = stream.read(CHUNK, exception_on_overflow = False)
   data = struct.unpack(str(CHUNK)+"i", data)
   data_int = np.array(data, dtype=int)

   rms = np.sqrt(np.mean((data_int - np.mean(data_int)) ** 2))

   rms_level = int(rms*10/RMS_SENS)
   if rms_level > LED_COUNT:
      rms_level = LED_COUNT

   for x in range(0,rms_level):
      strip.setPixelColor(x,Color(138,43,226))

   if rms_level < LED_COUNT:
      for x in range(rms_level,LED_COUNT):
         strip.setPixelColor(x,Color(0,0,0))

   strip.show()

