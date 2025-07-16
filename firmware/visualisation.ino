#include <EEPROM.h>

// CONFIGURABLE SETTINGS

// ! set threshold values manually if EEPROM is not used
const bool useEEPROM = true;
int eepromAddress = 200;

// Define analog pins used for sensors, customize these manually
const int8_t analogPinsHIGH[16] = {A0,  A1,  A2,  A3,  A7,  A6,  A8,  A9,
                                   A17, A10, A11, A12, A13, A14, A16, A15};
const int8_t analogPinsLOW[16] = {A0, A1,  A2,  A3,  A7,  A6,  A8,  A17,
                                  A9, A10, A11, A12, A13, A14, A16, A15};

const int pinCount = sizeof(analogPinsHIGH) / sizeof(analogPinsHIGH[0]);

// total expected values to be read
int sensorsInput[pinCount * 2];
int sensorThreshold[pinCount * 2];

void setup() {
  Serial.begin(115200);

  sensorThreshold[pinCount * 2] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};

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

  digitalWriteFast(37, LOW);
  for (int i = 0; i < pinCount; i++) {
    sensorsInput[i] = analogRead(analogPinsLOW[i]);
  }

  digitalWriteFast(37, HIGH);
  for (int i = 0; i < pinCount; i++) {
    sensorsInput[pinCount + i] = analogRead(analogPinsHIGH[i]);
  }
}

/**
 * @brief Sending over serial for main.py to read
 * @note main.py assumes data is split by commas,
 * if you change this then change it there too
 */
void sendSensorData() {

  for (int i = 0; i < pinCount * 2; i++) {
    Serial.print(sensorsInput[i]);
    Serial.print(",");
  }

  for (int i = 0; i < pinCount * 2; i++) {
    Serial.print(sensorThreshold[i]);
    if (i < pinCount * 2 - 1)
      Serial.print(",");
  }
  Serial.println(); // End transmission
}