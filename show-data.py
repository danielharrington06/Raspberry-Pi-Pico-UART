import matplotlib.pyplot as plt
import numpy as np
import time
import keyboard
import serial
from matplotlib.widgets import Button

global times, values
times = []
values = []

global start
start = 0
AMOUNT = 20

global scrollMode, modifier
scrollMode = "auto"
modifier = 0

global displayTimes, displayValues

figure, axis = plt.subplots()

def setupGraph():
    global displayTimes, displayValues
    pass

def auto():
    #make sure auto is latest info
    global displayTimes, displayValues
    min = times[len(times)-1]-AMOUNT
    for i, item in enumerate(times):
        if item >= min:
            index = i
            break
    displayTimes = times[index:]
    displayValues = values[len(values)-len(times[index:]):]

def manual():
    global displayTimes, displayValues, modifier
    min = displayTimes[0]+modifier
    modifier = 0
    #set max and min to something at the start
    for i, item in enumerate(times):
        if item >= min:
            minI = i
            break
    for i, item in enumerate(times):
        if item < min + AMOUNT:
            maxI = i
        else:
            break
    displayTimes = times[minI:maxI+1]
    displayValues = values[minI:maxI+1]

class Mode:
    
    def manual(self, event):
        global scrollMode
        print("Manual mode activated")
        scrollMode = "manual"
    
    def auto(self, event):
        global scrollMode
        print("Automatic mode activated")
        scrollMode = "auto"

    def left(self, event):
        global scrollMode, modifier
        modifier = -2.5
    
    def right(self, event):
        global scrollMode, modifier
        modifier = 2.5
    
def updateGraph(value):
    global displayTimes, displayValues
    global scrollMode
    times.append(time.time()-start)
    if value != None:
        values.append(int(value))

        if scrollMode == "auto": #scrolls automatically

            auto()

        elif scrollMode == "manual": #scrolls based on user's control
            manual()
            #do manual things.
            #https://www.geeksforgeeks.org/matplotlib-button-widget/
            pass
        else:
            print("This should not execute")


        plt.clf()

        figure.subplots_adjust(bottom=0.2)

        plt.xlabel("Time (s)")
        plt.ylabel("ADC Value")
        plt.ylim(-2000, 70025)

        xpoints = np.array(displayTimes)
        ypoints = np.array(displayValues)

        plt.plot(xpoints, ypoints, color="cornflowerblue", markersize=12)
        if scrollMode == "auto":
            
            a_manual = figure.add_axes((0.7, 0.05, 0.22, 0.075))
            #axnext = figure.add_axes([0.81, 0.05, 0.1, 0.075])
            b_manual = Button(a_manual, 'Activate Manual')
            b_manual.on_clicked(control.manual)

        if scrollMode == "manual":
            a_left = figure.add_axes((0.1, 0.05, 0.05, 0.075))
            a_auto = figure.add_axes((0.7, 0.05, 0.22, 0.075))
            a_right = figure.add_axes((0.16, 0.05, 0.05, 0.075))
            b_left = Button(a_left, "<")
            b_auto = Button(a_auto, 'Activate Automatic')
            b_right = Button(a_right, ">")
            b_left.on_clicked(control.left)
            b_auto.on_clicked(control.auto)
            b_right.on_clicked(control.right)



        plt.show(block=False)
        plt.pause(0.0001)

def getByte():
    x = int.from_bytes(ser.read(1), "little")
    #print(x)
    return x

def receiveData():
    data = []
    value = getByte()
    if value == 2: #start
        value = getByte()
        if value == 1: #hex
            value = getByte()
            for i in range(value): #payload
                data.append(getByte())
            value = getByte()
            check = 0
            for item in data:
                check += item
            check = check % 256
            if value == check: #checksum
                value = getByte()
                if value == 3: #end
                    #use data
                    if len(data) == 2:
                        value = data[0] * 16**2 + data[1]
                    else:
                        value = data[0]

                    
                    return value
                
        elif value == 0: #den
            value = getByte()
            for i in range(value): #payload
                data.append(getByte()-48)
            value = getByte()
            if value == 0: #checksum
                value = getByte()
                if value == 3: #end
                    #use data
                    value = ""
                    for item in data:
                        value += str(item)
                    value = int(value)

                    return value

ser = serial.Serial(
    port='COM5',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS
)

setupGraph()

value = receiveData()
start = time.time()

control = Mode()
updateGraph(value)


while True:

    value = receiveData()
    #print(value)
    
    updateGraph(value)
    
    if keyboard.is_pressed("ctrl+c"):
        break
