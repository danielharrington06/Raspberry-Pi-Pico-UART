# Raspberry-Pi-Pico-UART
I spent a few days with a tech consultancy company in Cambridge that specialises in embedded systems called eg Technology for Work Experience.
During this time I worked on a Raspberry Pi Pico and a breadboard. My overall goal was to send values from an ADC through UART to a python program on my computer that 
took this data and showed it graphically which scrolled across the screen as more data was received. I also programmed a way to manual 'scrub' through data that wasn't
necessarily in the latest 20 seconds of data.

I found a few ways to make the project more advanced, such as coding a flashing LED to signify when the UART was writing from the Raspberry Pi Pico to the Computer.
I designed the Raspberry Pi Pico to send the data in a hexadecimal or denary (changed by the push of a button and indicated by two LED lights) form to the computer. This included sending a start byte, length byte, mode byte (hexadecimal or 
denary), the payload byte(s), a (simple) checksum byte, and an end byte. I found this project very interesting and engaging. It was suitably challenging as I hadn't
done anything of the sort before.

This project gave me an insight into the world of embedded programming and how interesting it is. I really enjoyed doing this project and was most interested by the the
different communication protocols. I had the chance to research CRC's and how they are useful. As someone who likes understanding the maths behind how things work, I found
this very interesting and fascinating to think about how and why it works.

The 'transmit-uart.py' file is uploaded to the raspberry pi and runs on there while the 'show-data.py' file is run from the computer.

