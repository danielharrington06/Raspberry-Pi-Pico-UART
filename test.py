import serial

ser = serial.Serial(
    port='COM5',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS
)

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
            if value == 0: #checksum
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

while True:
    value = receiveData()
    print(value)
        

