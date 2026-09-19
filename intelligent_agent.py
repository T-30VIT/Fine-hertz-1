import serial
import time
import sys

# CHANGE THIS to your hardware's actual USB port. 
# Windows: 'COM3', 'COM4' | Mac/Linux: '/dev/tty.usbmodem...' or '/dev/ttyUSB0'
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600

def compute_agent_policy(heart_rate, battery):
    """
    Intelligent Agent State Assessment Function.
    Evaluates risk and tells the embedded device how aggressively to sample.
    """
    # State 1: Battery Emergency
    if battery < 15.0:
        return "SHUTDOWN", "🚨 BATTERY CRITICAL (<15%). Forcing emergency backup preservation."
        
    # State 2: Patient Anomaly Detected (Tachycardia / Spikes)
    elif heart_rate > 100 or heart_rate < 55:
        return "CRITICAL", "⚠️ ANOMALY DETECTED. Instructing hardware to switch to High-Frequency Monitoring."
        
    # State 3: Patient is Stable & Battery is Normal
    else:
        return "STABLE", "✅ PATIENT STABLE. Instructing hardware to switch to Low-Frequency Power-Saving Mode."

def main():
    print("==================================================")
    print("  Adaptive Biomedical Monitoring System - Agent   ")
    print("==================================================")
    print(f"Attempting connection to microcontroller on port {SERIAL_PORT}...")

    try:
        # Establish connection with Arduino/STM32
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Await hardware initialization
        print("Successfully connected! Monitoring incoming vital signals...\n")
        
        while True:
            if ser.in_waiting > 0:
                # Read stream line from the serial connection
                raw_line = ser.readline().decode('utf-8').strip()
                
                # Ignore empty transmissions
                if not raw_line or "," not in raw_line:
                    continue
                
                try:
                    # Parse transmitted data array
                    heart_rate_str, battery_str = raw_line.split(",")
                    heart_rate = int(heart_rate_str)
                    battery = float(battery_str)
                    
                    # Run the policy framework engine
                    action_cmd, explanation = compute_agent_policy(heart_rate, battery)
                    
                    # Print monitoring metrics to screen terminal
                    print(f"[DATA RCV] Vital: {heart_rate} BPM | Battery: {battery:.1f}%")
                    print(f"[DECISION] {explanation}")
                    
                    # Send feedback command control word back down to microcontroller
                    ser.write(f"{action_cmd}\n".encode('utf-8'))
                    print(f"[TX CMD]  Dispatched signal: '{action_cmd}' to hardware.")
                    print("-" * 50)
                    
                except ValueError:
                    # Capture formatting glitches gracefully
                    continue
                    
            time.sleep(0.1)

    except serial.SerialException:
        print(f"\n❌ Could not open port {SERIAL_PORT}.")
        print("💡 Troubleshoot: Check connection, or update SERIAL_PORT variable inside the script.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopping Intelligent Agent Process safely. Goodbye.")
        sys.exit(0)

if __name__ == "__main__":
    main()
