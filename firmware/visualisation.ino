#include <EEPROM.h>

// CONFIGURABLE SETTINGS

// ! set threshold values manually if EEPROM is not used
const bool useEEPROM = false;
int eepromAddress = -1;

// Define analog pins used for sensors, customize these manually
const int analogPins[] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                          A8, A9, A10, A11, A12, A13, A14, A15};

const int pinCount = sizeof(analogPins) / sizeof(analogPins[0]);

// total expected values to be read
int sensorsInput[pinCount];
int sensorThreshold[pinCount];

void setup() {
  Serial.begin(115200);

  sensorThreshold[pinCount] = {-1, -1, -1, -1, -1, -1, -1, -1,
                               -1, -1, -1, -1, -1, -1, -1, -1};

  // make sure to set the EEPROM address if used
  // Make sure the size is within sensorThreshold array bounds
  if (useEEPROM && eepromAddress >= 0) {
    EEPROM.get(eepromAddress, sensorThreshold);
  }
}

void loop() {

  // Receives "R" from main.py after running the script
  if (Serial.available() && Serial.read() == 'R') {
    readSensors();
    sendSensorData();
  }

  delay(10);
}

/**
 * @brief Read sensors from analog pins and store in sensorsInput array
 * @note This function reads the analog values from the defined pins
 * and stores them in the sensorsInput array.
 */
void readSensors() {

  for (int i = 0; i < pinCount; i++) {
    sensorsInput[i] = analogRead(analogPins[i]);
  }
}

/**
 * @brief Sending over serial for main.py to read
 * @note main.py assumes data is split by commas,
 * if you change this then change it there too
 */
void sendSensorData() {

  for (int i = 0; i < pinCount; i++) {
    Serial.print(sensorsInput[i]);
    Serial.print(",");
  }

  for (int i = 0; i < pinCount; i++) {
    Serial.print(sensorThreshold[i]);
    if (i < pinCount - 1)
      Serial.print(",");
  }
  Serial.println(); // End transmission
}