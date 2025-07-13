// #include <EEPROM.h>

// Sensor wiring (adjust pins if needed)
const int8_t analogPins[32] = {A0,  A1,  A2,  A3,  A4,  A5,  A6,  A7,
                               A8,  A9,  A10, A11, A12, A13, A14, A15,
                               A16, A17, A18, A19, A20, A21, A22, A23,
                               A24, A25, A26, A27, A28, A29, A30, A31};
// Variables
int thresholdLineSens[32];
int sensors[32]; // Raw sensor values

void setup() {
  Serial.begin(115200);
  // EEPROM.get(EEPROM ADDRESS, thresholdLineSens);

  threholdLineSens = {
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // Initialize thresholds
}

void loop() {
  if (Serial.available() && Serial.read() == 'R') {
    readSensors();
    sendSensorData(); // Send both sensors and thresholds
  }
  delay(10);
}

void readSensors() {
  // Read first 16 sensors (LOW)
  for (int i = 0; i < 32; i++) {
    sensors[i] = analogRead(analogPins[i]);
  }
}

void sendSensorData() {
  // Send sensor values (0-31)
  for (int i = 0; i < 32; i++) {
    Serial.print(sensors[i]);
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