#include <EEPROM.h>

int pinCount = 16; // Total number of analog pins to initialize arrays

const int8_t analogPins[pinCount] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                     A8, A9, A10, A11, A12, A13, A14, A15};

int sensorsInput[pinCount];

//
/**
 * @brief // Put in your values, or use EEPROM to load them
 * Use -1 to disable thresholds for certain sensors.
 */
int sensorThreshold[pinCount] = {-1};

/**
 * @note EEPROM is not used by default, set the address
 * if you want to use it.
 * ! make sure EEPROM actually has the data you want to read.
 */
const int eepromAddress = -1;

/**
 * @brief Multiplexer is not used by default, but can be enabled if needed.
 * ! make sure to set the useMultiplexer boolean to true.
 * ! make sure to set the multiplexer pin correctly.
 */
const int multiplexerPin = -1; // Multiplexer pin not used in this version
bool useMultiplexer = false;   // Set to true if using a multiplexer

const int8_t analogPinsLOW[pinCount] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                        A8, A9, A10, A11, A12, A13, A14, A15};
const int8_t analogPinsHIGH[pinCount] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                         A8, A9, A10, A11, A12, A13, A14, A15};

void setup() {
  Serial.begin(115200);
  if (useMultiplexer && multiplexerPin >= 0) {
    pinMode(multiplexerPin, OUTPUT);
  }

  // ! make sure to set the EEPROM address if used
  if (eepromAddress >= 0) {
    // EEPROM.get(eepromAddress, sensorThreshold);
  }
}

void loop() {
  if (Serial.available() && Serial.read() == 'R') {

    if (useMultiplexer)
      readSensorsWithMultiplexer();
    else
      readSensors();

    sendSensorData(); // Send both sensors and thresholds
  }
  delay(10);
}

void readSensors() {
  // Read first 16 sensors (LOW)
  int numPins = sizeof(analogPins) / sizeof(analogPins[0]);
  for (int i = 0; i < numPins; i++) {
    sensorsInput[i] = analogRead(analogPins[i]);
  }
}

void readSensorsWithMultiplexer() {

  int numAnalogPinsLow = sizeof(analogPinsLOW) / sizeof(analogPinsLOW[0]);
  int numAnalogPinsHigh = sizeof(analogPinsHIGH) / sizeof(analogPinsHIGH[0]);

  // Read first 16 sensors (LOW)
  digitalWrite(multiplexerPin, LOW);
  for (int i = 0; i < numAnalogPinsLow; i++)
    sensorsInput[i] = analogRead(analogPinsLOW[i]);

  // Read next 16 sensors (HIGH)
  digitalWrite(multiplexerPin, HIGH);
  for (int i = 0; i < numAnalogPinsHigh; i++)
    sensorsInput[numAnalogPinsLow + i] = analogRead(analogPinsHIGH[i]);
}

void sendSensorData() {

  int numSensors = sizeof(sensorsInput) / sizeof(sensorsInput[0]);
  int numThresholds = sizeof(sensorThreshold) / sizeof(sensorThreshold[0]);

  // Send sensor values (0-31)
  for (int i = 0; i < numSensors; i++) {
    Serial.print(sensorsInput[i]);
    Serial.print(",");
  }

  // Send thresholds (0-31)
  for (int i = 0; i < numThresholds; i++) {
    Serial.print(sensorThreshold[i]);
    if (i < numThresholds - 1)
      Serial.print(",");
  }
  Serial.println(); // End transmission
}