#include <EEPROM.h>

// Sensor wiring (adjust pins if needed)
const int8_t analogPinsHIGH[16] = {A0, A1, A2, A3, A7, A6, A8, A9, A17, A10, A11, A12, A13, A14, A16, A15};
const int8_t analogPinsLOW[16] = {A0, A1, A2, A3, A7, A6, A8, A17, A9, A10, A11, A12, A13, A14, A16, A15};

// Variables
int thresholdLineSens[32];  // Loaded from EEPROM
int sensors[32];            // Raw sensor values

void setup() {
  Serial.begin(115200);
  pinMode(37, OUTPUT);
  EEPROM.get(200, thresholdLineSens);  // Load thresholds from EEPROM address 200
}

void loop() {
  if (Serial.available() && Serial.read() == 'R') {
    readSensors();
    sendSensorData();  // Send both sensors and thresholds
  }
  delay(10);
}

void readSensors() {
  // Read first 16 sensors (LOW)
  digitalWriteFast(37, LOW);
  for (int i = 0; i < 16; i++) sensors[i] = analogRead(analogPinsLOW[i]);
  
  // Read next 16 sensors (HIGH)
  digitalWriteFast(37, HIGH);
  for (int i = 0; i < 16; i++) sensors[16 + i] = analogRead(analogPinsHIGH[i]);
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
    if (i < 31) Serial.print(",");
  }
  Serial.println();  // End transmission
}