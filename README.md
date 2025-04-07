# Brightness_hand_control
This project uses OpenCV and MediaPipe to track the distance between your thumb and index finger in real-time. The measured distance is sent to an Arduino Uno via Firmata, which controls the brightness of an LED using PWM.
Absolutely! Here’s a **plain text GitHub-style `README` instructions section** you can include in your repository to explain how to run your project step-by-step:

---

## 📦 How to Run This Project

### 🔧 Requirements
Make sure you have the following installed:

- Python 3.7+
- Arduino IDE (for uploading Firmata firmware)
- USB cable for Arduino Uno
- Webcam (built-in or external)

### 📦 Python Dependencies

Install the required Python packages:

```bash
pip install opencv-python mediapipe pyfirmata2 pyserial
```

---

### 🛠 Step-by-Step Setup

#### 1. **Upload Firmata to Arduino**
- Open the **Arduino IDE**
- Go to `File > Examples > Firmata > StandardFirmata`
- Select your Arduino board and correct COM port
- Click **Upload**

#### 2. **Connect Your Hardware**
- Connect an **LED to a PWM-capable pin** (e.g., D9) with a current-limiting resistor (220Ω)

#### 3. **Run the Python Script**
- Run the Python script using:

```bash
python brightness_hand_control.py
```

- The script will:
  - Detect available serial ports
  - Let you choose the correct port (your Arduino)
  - Let you choose a valid **PWM pin** (e.g., D3, D5, D6, D9, D10, D11)
  - Start the webcam and begin tracking

---

### 📌 How It Works
- The webcam detects your **hand** using MediaPipe.
- It measures the distance between your **thumb and index finger**.
- This distance is sent to Arduino and converted to **LED brightness** (PWM).

---

### 🛑 Exit
- Press **`q`** on the keyboard to quit the program safely.

---

## 🎥 Watch it in Action

[![Watch the demo](https://img.youtube.com/vi/CgUA7XS_OXY/0.jpg)](https://www.youtube.com/watch?v=CgUA7XS_OXY)
