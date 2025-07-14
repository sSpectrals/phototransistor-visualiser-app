// #include <EEPROM.h>

int pinCount = 16; // Total number of analog pins to initialize arrays

const int8_t analogPins[pinCount] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                     A8, A9, A10, A11, A12, A13, A14, A15};

int sensorsInput[pinCount];

int sensorThreshold[pinCount];

// Put in your values, or use EEPROM to load them
sensorThreshold = {0};

/**
 * @note EEPROM is not used by default, set the address
 * if you want to use it.
 * ! make sure EEPROM actually has the data you want to read.
 */
const int eepromAddress = nullptr;

/**
 * @brief Multiplexer is not used by default, but can be enabled if needed.
 * ! make sure to set the useMultiplexer boolean to true.
 * ! make sure to set the multiplexer pin correctly.
 */
int multiplexerPin = nullptr; // Multiplexer pin not used in this version
bool useMultiplexer = false;  // Set to true if using a multiplexer

pinMode(multiplexerPin, OUTPUT);

const int8_t analogPinsLOW[pinCount] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                        A8, A9, A10, A11, A12, A13, A14, A15};
const int8_t analogPinsHIGH[pinCount] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                         A8, A9, A10, A11, A12, A13, A14, A15};

void setup() {
  Serial.begin(115200);

  // ! make sure to set the EEPROM address if used
  // EEPROM.get(EEPROM ADDRESS, sensorThreshold);
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

  numAnalogPinsLow = sizeof(analogPinsLOW) / sizeof(analogPinsLOW[0]);
  numAnalogPinsHigh = sizeof(analogPinsHIGH) / sizeof(analogPinsHIGH[0]);

  // Read first 16 sensors (LOW)
  digitalWriteFast(multiplexerPin, LOW);
  for (int i = 0; i < numAnalogPinsLow; i++)
    sensorsInput[i] = analogRead(analogPinsLOW[i]);

  // Read next 16 sensors (HIGH)
  digitalWriteFast(multiplexerPin, HIGH);
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