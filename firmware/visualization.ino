// #include <EEPROM.h>

// Sensor wiring (adjust pins if needed)
const int8_t analogPins[32] = {A0,  A1,  A2,  A3,  A4,  A5,  A6,  A7,
                               A8,  A9,  A10, A11, A12, A13, A14, A15,
                               A16, A17, A18, A19, A20, A21, A22, A23,
                               A24, A25, A26, A27, A28, A29, A30, A31};
int thresholdLineSens[32];
int sensorsInput[32]; // Raw sensor values

/**
 * @brief Multiplexer is not used by default, but can be enabled if needed.
 * ! make sure to set the useMultiplexer boolean to true.
 * ! make sure to set the multiplexer pin correctly.
 */
int multiplexerPin = nullptr; // Multiplexer pin not used in this version
bool useMultiplexer = false;  // Set to true if using a multiplexer

pinMode(multiplexerPin, OUTPUT);

const int8_t analogPinsLOW[16] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                  A8, A9, A10, A11, A12, A13, A14, A15};
const int8_t analogPinsHIGH[16] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                                   A8, A9, A10, A11, A12, A13, A14, A15};

/**
 * @note EEPROM is not used by default, uncomment in setup() and set the address
 * if you want to use it.
 * ! comment the array in line 37
 *
 */
const int eepromAddress = nullptr;

void setup() {
  Serial.begin(115200);

  // ! make sure to set the EEPROM address if used
  // EEPROM.get(EEPROM ADDRESS, thresholdLineSens);

  threholdLineSens = {
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // Initialize thresholds
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
  for (int i = 0; i < 32; i++) {
    sensorsInput[i] = analogRead(analogPins[i]);
  }
}

void sendSensorData() {
  // Send sensor values (0-31)
  for (int i = 0; i < 32; i++) {
    Serial.print(sensorsInput[i]);
    Serial.print(",");
  }

  // Send thresholds (0-31)
  for (int i = 0; i < 32; i++) {
    Serial.print(thresholdLineSens[i]);
    if (i < 31)
      Serial.print(",");
  }
  Serial.println(); // End transmission
}

void readSensorsWithMultiplexer() {
  // Read first 16 sensors (LOW)
  digitalWriteFast(multiplexerPin, LOW);
  for (int i = 0; i < 16; i++)
    sensorsInput[i] = analogRead(analogPinsLOW[i]);

  // Read next 16 sensors (HIGH)
  digitalWriteFast(multiplexerPin, HIGH);
  for (int i = 0; i < 16; i++)
    sensorsInput[16 + i] = analogRead(analogPinsHIGH[i]);
}