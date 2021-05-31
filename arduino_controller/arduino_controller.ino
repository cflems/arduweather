const byte N_PINS = 8;
const byte ANODE_PINS[N_PINS] = {13, 12, 11, 10, 9, 8, 7, 6};
const byte CATHODE_PINS[N_PINS] = {A3, A2, A1, A0, 5, 4, 3, 2};

void ANODE_OFF(byte index) {
  digitalWrite(ANODE_PINS[index], HIGH);
}
void ANODE_ON(byte index) {
  digitalWrite(ANODE_PINS[index], LOW);
}
void CATHODE_OFF(byte index) {
  digitalWrite(CATHODE_PINS[index], HIGH);
}
void CATHODE_ON(byte index) {
  digitalWrite(CATHODE_PINS[index], LOW);
}
void ALL_OFF() {
  for (byte i = 0; i < N_PINS; i++) {
    ANODE_OFF(i);
    CATHODE_OFF(i);
  }  
}

void setup() {
  for (byte i = 0; i < N_PINS; i++) {
    pinMode(ANODE_PINS[i], OUTPUT);
    pinMode(CATHODE_PINS[i], OUTPUT);
  }

  ALL_OFF();
  
  Serial.begin(115200);
  Serial.setTimeout(100);
}

// upgraded with brightness capability
static const byte MAX_BRIGHTNESS = 15;
static const byte BYTES_PER_ROW = 4;
static const byte BITS_PER_COL = 4;
// message[N_PINS*BYTES_PER_ROW]
void display(byte message[32]) {
  for (byte brightness = 0; brightness < MAX_BRIGHTNESS; brightness++){
    for (byte row = 0; row < N_PINS; row++) {
      for (byte b = 0; b < BYTES_PER_ROW; b++) {
        byte w = message[BYTES_PER_ROW*row + b];
        for (byte col = 0; col < N_PINS/BYTES_PER_ROW; col++) {
          byte led_value = (w >> col*BITS_PER_COL & 0xf);
          if (led_value > brightness)
            CATHODE_ON(N_PINS/BYTES_PER_ROW*b+col);
          else CATHODE_OFF(N_PINS/BYTES_PER_ROW*b+col);
        }
      }
      ANODE_ON(row);
      delayMicroseconds(250/MAX_BRIGHTNESS);
      ANODE_OFF(row);
    }
  }
}

// read pattern from port and display it
void loop() {
  // compressed; we only need 4 bits for a brightness, so we can read 4 bytes per row = 32 bytes total
  static byte boofer[N_PINS*BYTES_PER_ROW]; // I think buffer is a reserved keyword so... yea.

  if (!Serial.available() || Serial.readBytes(boofer, sizeof(boofer)) == sizeof(boofer)) {
    display(boofer);
    return; // don't hit the error case
  }
  
  // this is the invalid data / not connected case: turn off all lights
  ALL_OFF();
}
