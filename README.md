# Arduino Christmas tree
###### (Work currently in progress)
Smart Christmas tree LEDs project

This project creates a smart christmas tree controller. I'm making everything I come up with publicly available without any further support from my side.

There are 3 arduino nanos - each is controlling 40 LEDs, all arduinos are connected to the Raspberry Pi via an I2C bus. Each Arduino has 5 TI SN74HC595 8-bit shift registers connected to the arduino's SPI output to allow full PWM. Each arduino is listening over I2C (ID stored in EEPROM) and it expects two bytes - first byte is LED ID and the second byte is the intensity. For the performance reasons I chose just 64 PWM intensity levels. The Arduino nano then has about 90% load.

For the Raspberry pi controller, I am making a python daemon with Flask web UI with Skeleton CSS template. That way I can control the christmas tree with my iPhone over wifi.

Arduino connection - use this manual https://www.arduino.cc/en/Tutorial/ShiftOut

Just change the clock pin to arduino's pin 13, latch pin is pin 10 and data serial is pin 11 - that way you can use the SPI output for much faster changes allowing an actual PWM output. Connect as many shift registers as you deem suitable, just remember to tune the specs in the arduino source code. I used the code from https://github.com/elcojacobs/ShiftPWM

My final setup has 120 LEDs (3x40), they're connected with 150 ohm resistors.

*Currently works:*
* arduino controllers listen on I2C and can control LEDs
* arduino has primitive serial control interface that allows I2C ID setup
* basic raspberry pi python control daemon
* raspberry pi has a ledmaster control class that abstracts all the low level I2C calls and adds something like a video buffer

*Planned features:*
* rewrite snowing simulator from embedded C to python
* add more effects
* add python listening daemon over ethernet so it can be controlled from a network connected computer

I will be pushing changes into it probably until Christmas 2017 (if I don't revisit this project later) - that is my deadline.
