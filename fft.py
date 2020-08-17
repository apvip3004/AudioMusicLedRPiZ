#!/usr/bin/env python3
import pyaudio
import numpy as np
import struct
import time

def getFFT(data,rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    data=data*np.hamming(len(data))
    fft=np.fft.fft(data)
    fft=np.abs(fft)
    #fft=10*np.log10(fft)
    freq=np.fft.fftfreq(len(fft),1.0/rate)
    return freq[:int(len(freq)/2)],fft[:int(len(fft)/2)]

CHUNK = 1024*8
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "test.wav"

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
   fftx, fft = getFFT(data_int, RATE)
  
   i=160
   sum_160_300 = 0
   while i < 300:
      sum_160_300 += fft[int(i/5.38)]
      i += 5.38

   i=300
   sum_300_600 = 0
   while i < 600:
      sum_300_600 += fft[int(i/5.38)]
      i += 5.38

   i=600
   sum_600_1200 = 0
   while i < 1200:
      sum_600_1200 += fft[int(i/5.38)]
      i += 5.38

   i=1200
   sum_1200_2400 = 0
   while i < 2400:
      sum_1200_2400 += fft[int(i/5.38)]
      i += 5.38

   i=2400
   sum_2400_5000 = 0
   while i < 5000:
      sum_2400_5000 += fft[int(i/5.38)]
      i += 5.38

   print("sum_160_300" + str(sum_160_300))
   print("sum_300_600" + ("=" * int(sum_300_600)))
   print("sum_600_1200" + ("=" * int(sum_600_1200)))
   print("sum_1200_2400" + ("=" * int(sum_1200_2400)))
   print("sum_2400_5000" + ("=" * int(sum_2400_5000)))

