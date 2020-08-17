#!/usr/bin/env python3
import pyaudio
import numpy as np
import struct

CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK)

while True:
   data = stream.read(CHUNK, exception_on_overflow = False)
   data = struct.unpack(str(CHUNK)+"i", data)
   data_int = np.array(data, dtype=int)
   rms = np.sqrt(np.mean((data_int - np.mean(data_int)) ** 2))

   print("c" + ("=" * int(rms*40/25236783)))

