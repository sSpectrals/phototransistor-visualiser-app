#include <EEPROM.h>

// CONFIGURABLE SETTINGS

/**
 * @brief Define the amount of sensors / the amount you're expecting to read
 * @note if you use a multiplexer, the amount of sensors can be more than the
 * amount of analog pins.
 */
const int SENSOR_BUFFER_SIZE = 16;

// ! set threshold values manually if EEPROM is not used
const bool useEEPROM = false;
int eepromAddress = -1;

// turn on and define pin for multiplexer
const bool useMultiplexer = false;
int multiplexerPin = -1;

// Define analog pins used for sensors, customize these manually
const int analogPins[] = {A0, A1, A2,  A3,  A4,  A5,  A6,  A7,
                          A8, A9, A10, A11, A12, A13, A14, A15};

// pinCount != sensor buffer size if multiplexer is used
const int pinCount = sizeof(analogPins) / sizeof(analogPins[0]);

// total expected values to be read
int sensorsInput[SENSOR_BUFFER_SIZE];
int sensorThreshold[SENSOR_BUFFER_SIZE] = {
    -1, -1, -1, -1, /* ... up to SENSOR_BUFFER_SIZE values ... */};

void setup() {
  Serial.begin(115200);

  while (pinCount > SENSOR_BUFFER_SIZE) {
    Serial.println("Error: Amount of analog pins exceeds sensor buffer size.");
    delay(1000);
  }

  if (useMultiplexer && multiplexerPin >= 0) {
    pinMode(multiplexerPin, OUTPUT);
  }

  // make sure to set the EEPROM address if used
  // Make sure the size is within sensorThreshold array bounds
  if (useEEPROM && eepromAddress >= 0) {
    EEPROM.get(eepromAddress, sensorThreshold);
  }
}

void loop() {

  if (Serial.available() && Serial.read() == 'R') {
    readSensors();
    sendSensorData();
  }

  delay(10);
}

void readSensors() {

  if (useMultiplexer && multiplexerPin >= 0) {

    // ! assuming the total amount of sensors is twice the amount of analog pins
    // (pinCount)
    //  adjust as needed for your specific multiplexer setup
    digitalWrite(multiplexerPin, LOW);
    for (int i = 0; i < pinCount; i++) {
      sensorsInput[i] = analogRead(analogPins[i]);
    }

    digitalWrite(multiplexerPin, HIGH);
    for (int i = 0; i < pinCount; i++) {
      sensorsInput[pinCount + i] = analogRead(analogPins[i]);
    }
  } else {
    for (int i = 0; i < pinCount; i++) {
      sensorsInput[i] = analogRead(analogPins[i]);
    }
  }
}

void sendSensorData() {

  for (int i = 0; i < SENSOR_BUFFER_SIZE; i++) {
    Serial.print(sensorsInput[i]);
    Serial.print(",");
  }

  for (int i = 0; i < SENSOR_BUFFER_SIZE; i++) {
    Serial.print(sensorThreshold[i]);
    if (i < pinCount - 1)
      Serial.print(",");
  }
  Serial.println(); // End transmission
}