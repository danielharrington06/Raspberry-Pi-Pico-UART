from machine import Pin, UART, ADC, PWM
import time

UART_INTERVAL = 0.40
LIGHT_INTERVAL = 0.01

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=1)

adc = ADC(Pin(26))

pwm = PWM(Pin(12))

update = Pin(13, Pin.OUT)
red = Pin(14, Pin.OUT)
green = Pin(15, Pin.OUT)

red.on()
green.off()

button = Pin(11, Pin.IN, Pin.PULL_DOWN)

pwm.freq(1000) 

i = 0
method = "hex"
while True:
    if button.value():
        red.toggle()
        green.toggle()
        time.sleep(0.1)
        if method == "hex":
            method = "den"
        else:
            method = "hex"

    val = min(adc.read_u16(), 65535)
    duty  = val if val > 0 else 0

    pwm.duty_u16(duty)
    

    if i == UART_INTERVAL/LIGHT_INTERVAL:
        update.on()
        i = 0
        command = bytearray()

        command.append(2)#start
        if method == "hex":
            command.append(1) #method

            
            length = 2
            big = duty // 256
            small = duty % 256
            if big == 0:
                length = 1
            else:
                length = 2

            command.append(length) #length (bytes)

            if length >= 2:
                command.append(big) #payload part one
            command.append(small) #payload part two

            check = big + small
            check = check % 256
            command.append(check) #checksum (0 for now)

            command.append(3) #end

            uart.write(command)
        elif method == "den":
            command.append(0) #method

            length = len(str(duty))
            command.append(length) #length

            for i in range(length): #payload
                command.append(int(str(duty)[i])+48)

            command.append(0) #checksum

            command.append(3) #end
            uart.write(command)

    time.sleep(LIGHT_INTERVAL)
    update.off()
    i += 1

