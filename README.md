# Closed-Loop Adaptive Biomedical Monitoring System

An intelligent framework designed to manage limited sensing, processing, and communication resource constraints on embedded biomedical monitoring nodes.

## 🧠 System Architecture Theory
Instead of evaluating patient data at static timelines (which wastes battery during health intervals or misses acute cardiovascular anomalies), this system builds an **adaptive closed-loop agent**. 

1. **Embedded Layer (Microcontroller):** Direct hardware execution layer reading physiological sensors. Dynamically scales clock speeds and sampling intervals to prioritize energy management.
2. **Intelligence Layer (Python Agent):** Continuously monitors streams, determines risk state metrics, and evaluates cross-functional performance policies.

## ⚙️ How to Deploy and Run

### Step 1: Uploading Firmware
1. Open the code in `firmware/firmware.ino` inside **Arduino IDE** or **STM32CubeIDE**.
2. Connect your microcontroller development board via USB.
3. Select your correct target device board type and port, then click **Upload**.

### Step 2: Running the Python Controller
1. Open your local machine terminal environment.
2. Install the necessary system communication drivers:
   ```bash
   pip install -r python_agent/requirements.txt
   ```
3. Open `python_agent/intelligent_agent.py` and modify the `SERIAL_PORT` parameter to your current port profile (e.g., `COM3` or `/dev/ttyUSB0`).
4. Boot up the processing brain:
   ```bash
   python python_agent/intelligent_agent.py
   ```
