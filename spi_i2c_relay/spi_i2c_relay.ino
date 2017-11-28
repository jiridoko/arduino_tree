nclude <SPI.h>

#define LEDCOUNT 120

byte ledBuffer[LEDCOUNT];
byte changeBuffer[LEDCOUNT];

byte LED_ID;
byte LED_INTENSITY;
bool LED_FIRST;

void(* resetBoard) (void) = 0;

void setup() {
  for (int i = 0; i < LEDCOUNT; ++i) {
    ledBuffer[i] = 0x00;
    changeBuffer[i] = 0x00;
  }
  
  LED_FIRST = true;
  LED_ID = 0x00;
  LED_INTENSITY = 0x00;

  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
  
  Wire.begin();
  Wire.setClock(400000);
  
  Serial.begin(115200);
  Serial.println("READY");
}

ISR (SPI_STC_vect) {
  byte input = SPDR;
  if (input == 0xFF) {
    if (LED_ID < LEDCOUNT) {
      changeBuffer[LED_ID] = LED_INTENSITY;
      LED_FIRST = true;
    } else if (LED_ID == 0xFF && LED_INTENSITY == 0xFF) {
      resetBoard();
    }
  } else if (LED_FIRST) {
    LED_ID = input;
    LED_FIRST = false;
  } else if (!LED_FIRST) {
    LED_INTENSITY = input;
  }
}

void notifyI2CSlave(byte address, byte ledId, byte intensity) {
  Wire.beginTransmission(address);
  Wire.write(ledId);
  Wire.write(intensity);
  Wire.endTransmission();
}

void sendLedEvent(byte id, byte intensity) {
  if (id < 40)
    notifyI2CSlave(11, id, intensity);
  else if (id < 80)
    notifyI2CSlave(12, id-40, intensity);
  else if (id < 120)
    notifyI2CSlave(13, id-80, intensity);
}

void loop() {
  for (int i = 0; i < LEDCOUNT; ++i) {
    if (ledBuffer[i] != changeBuffer[i]) {
      ledBuffer[i] = changeBuffer[i];
      sendLedEvent(i, ledBuffer[i]);
    }
  }
}
