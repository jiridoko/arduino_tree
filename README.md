# Arduino Christmas tree
Smart Christmas tree LEDs project

This project creates a smart christmas tree controller. I'm making everything I come up with publicly available without any further support from my side.

There are 3 arduino nanos - each is controlling 40 LEDs, all arduinos are connected to the Raspberry Pi via an I2C bus. Each Arduino has 5 TI SN74HC595 8-bit shift registers connected to the arduino's SPI output to allow full PWM. Each arduino is listening over I2C (ID stored in EEPROM) and it expects two bytes - first byte is LED ID and the second byte is the intensity. For the performance reasons I chose just 64 PWM intensity levels. The Arduino nano then has about 90% load.

For the Raspberry pi controller, I am making a python daemon with Flask web UI with Skeleton CSS template. That way I can control the christmas tree with my iPhone over wifi.

Arduino connection - use this manual https://www.arduino.cc/en/Tutorial/ShiftOut
Just change the clock pin to arduino's pin 13, latch pin is pin 10 and data serial is pin 11 - that way you can use the SPI output for much faster changes allowing an actual PWM. Connect as many shift registers as you deem suitable, just remember to tune the specs in the arduino.

My final setup has 120 LEDs (3x40), they're connected with 150 ohm resistors.
