import time
import serial
import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial(
    port='COM5',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS
)

start = time.time()
times = []
values = []

i = 0
while True:
    val = ser.readline()
    values.append(int(val))
    times.append(time.time()-start)

    xpoints = np.array(times)
    ypoints = np.array(values)
    plt.clf()
    plt.plot(xpoints, ypoints)
    plt.show()
    i += 1
    if i >= 20:
        break

print(times)
print(values)
