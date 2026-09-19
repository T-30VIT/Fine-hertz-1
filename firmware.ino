#define SENSOR_PIN A0      // Pin simulating or reading a pulse/ECG signal
#define INDICATOR_LED 13   // Blinks when sampling occurs

int samplingInterval = 2000; // Default: sample every 2 seconds (Normal mode)
float batteryLevel = 100.0;  // Simulated battery percentage

void setup() {
  Serial.begin(9600);        // Initialize USB serial communication
  pinMode(INDICATOR_LED, OUTPUT);
}

void loop() {
  // 1. Read the physiological data point
  int rawSignal = analogRead(SENSOR_PIN);
  
  // Map raw analog reading to a realistic heart rate range (e.g., 50 to 140 bpm)
  int heartRate = map(rawSignal, 0, 1023, 50, 140);
  
  // 2. Simulate battery drain depending on system performance speed
  // Faster sampling rates drain the battery significantly faster
  if (samplingInterval < 1000) {
    batteryLevel -= 0.2;  // Intensive High-Frequency Alert Mode
  } else {
    batteryLevel -= 0.05; // Resource-saving Low-Frequency Mode
  }
  
  // Keep battery from dropping below zero
  if (batteryLevel < 0) batteryLevel = 0;

  // 3. Format data string and transmit over USB Serial to Python Agent
  // Format: "heartRate,batteryLevel"
  Serial.print(heartRate);
  Serial.print(",");
  Serial.println(batteryLevel);

  // Visual blink indicator for reading action
  digitalWrite(INDICATOR_LED, HIGH);
  delay(50);
  digitalWrite(INDICATOR_LED, LOW);

  // 4. Listen for commands back from the Python Agent
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "CRITICAL") {
      samplingInterval = 500;   // High Alert: sample aggressively every 500ms
    } else if (command == "STABLE") {
      samplingInterval = 3000;  // Power Save: sample every 3 seconds
    } else if (command == "SHUTDOWN") {
      samplingInterval = 10000; // Critical battery: drop down to emergency mode
    }
  }

  // Adaptive delay based on the agent's real-time command decisions
  delay(samplingInterval);
}
