#define SHIFTPWM_USE_TIMER2
const int ShiftPWM_latchPin=10;

// const int ShiftPWM_dataPin = 11;
// const int ShiftPWM_clockPin = 13;


// If your LED's turn on if the pin is low, set this to true, otherwise set it to false.
const bool ShiftPWM_invertOutputs = false; 

// You can enable the option below to shift the PWM phase of each shift register by 8 compared to the previous.
// This will slightly increase the interrupt load, but will prevent all PWM signals from becoming high at the same time.
// This will be a bit easier on your power supply, because the current peaks are distributed.
const bool ShiftPWM_balanceLoad = false;

#include <ShiftPWM.h>   // include ShiftPWM.h after setting the pins!
// Get it at https://github.com/elcojacobs/ShiftPWM
#include <Wire.h>
#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <SerialCommand.h>
// Get it at https://github.com/scogswell/ArduinoSerialCommand

SerialCommand SCmd;

#define EEPROMADDRESS 0

#define LEDCOUNT 40

const unsigned char maxBrightness = 63;
const unsigned char pwmFrequency = 60;
const int numRegisters = LEDCOUNT;

void(* resetBoard) (void) = 0;

byte getI2CID() {
  return EEPROM.read(EEPROMADDRESS);
}

void setI2CID(byte value) {
  EEPROM.write(EEPROMADDRESS, value);
}

byte sanitizeBrightness(int input) {
  if (input < 0)
    return 0x00;
  else if (input > maxBrightness)
    return (byte) maxBrightness;
  else
    return (byte) input;
}

void pulseAll() {
  ShiftPWM.SetAll(0);
  for (int i=0; i<=maxBrightness; i+=4) {
    ShiftPWM.SetAll(i);
    delay(20);
  }
  delay(200);

  for (int i=maxBrightness; i>=0; i-=4) {
    ShiftPWM.SetAll(i);
    delay(20);
  }
  ShiftPWM.SetAll(0);
}

void setup(){
  Serial.begin(115200);

  Serial.println("PWM 40 LED controller initializing");
  // Sets the number of 8-bit registers that are used.
  ShiftPWM.SetAmountOfRegisters(numRegisters);

  Serial.print("numRegisters: ");
  Serial.println(numRegisters);
  // SetPinGrouping allows flexibility in LED setup. 
  // If your LED's are connected like this: RRRRGGGGBBBBRRRRGGGGBBBB, use SetPinGrouping(4).
  ShiftPWM.SetPinGrouping(1); //This is the default, but I added here to demonstrate how to use the funtion
  
  ShiftPWM.Start(pwmFrequency,maxBrightness);

  Serial.print("pwmFrequency: ");
  Serial.println(pwmFrequency);
  Serial.print("maxBrightness: ");
  Serial.println(maxBrightness);

  Serial.println("Starting pulseAll");
  pulseAll();
  Serial.println("pulseAll finished");

  Serial.println("Initializing I2C interface");
  Wire.begin(getI2CID());
  Serial.print("I2C slave ID: ");
  Serial.println(getI2CID());
  Wire.onReceive(receiveEvent);
  Serial.println("I2C initialized");
  
  SCmd.addCommand("get", serialGetCommand);
  SCmd.addCommand("set", serialSetCommand);
  SCmd.addCommand("reset", serialResetCommand);
  SCmd.addCommand("help", serialHelpCommand);
  SCmd.addDefaultHandler(serialUnrecognized);
  Serial.println("Serial parser initialized");
  Serial.println("type \"help\" for list of commands");
  Serial.println("READY");
}

void serialHelpCommand() {
  Serial.println("get      - Show I2C ID");
  Serial.println("set [ID] - Set I2C ID");
  Serial.println("reset    - Reset the board");
  Serial.println("help     - This help");
}

void serialResetCommand() {
  Serial.println("Resetting the board");
  Serial.flush();
  resetBoard();
}

void serialUnrecognized() {
  Serial.println("Invalid command");
}

void serialGetCommand() {
  Serial.print("I2C ID: ");
  Serial.println(getI2CID());
}

void serialSetCommand() {
  char *arg;
  arg = SCmd.next();
  if (arg != NULL) {
    int ID = atoi(arg);
    setI2CID(ID);
    Serial.print("Setting I2C slave ID to: ");
    Serial.println(ID);
    Serial.println("Reset the board to take effect");
  } else {
    serialUnrecognized();
  }
}

void receiveEvent(int len) {
  if (len%2 == 0) {
    // We have a chunk of data
    for (int i=0; i < (len / 2); ++i) {
      byte ledID = Wire.read();
      byte intensity = Wire.read();
      if (ledID == 0xFF && intensity == 0xFF)
        serialResetCommand();
      if (ledID < LEDCOUNT)
        ShiftPWM.SetOne(ledID, intensity);
    }
  }
}

void loop() {
  SCmd.readSerial();
}
