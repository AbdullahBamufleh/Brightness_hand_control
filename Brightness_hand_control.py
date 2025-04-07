import time
import cv2
import mediapipe as mp
import pyfirmata2
import math
import serial.tools.list_ports

# ========== Greeting ==========
print("👋 Hello! Welcome to the Hand Tracking LED Controller using Arduino Uno\n")

# ========== List Available Serial Ports ==========
print("🔍 Scanning available serial ports...\n")
ports = list(serial.tools.list_ports.comports())

if not ports:
    print("❌ No serial ports found. Please connect your Arduino.")
    exit()

# Print all available ports with indexes
for i, port in enumerate(ports):
    print(f"{i + 1}. {port.device} - {port.description}")

# User selects the Arduino port
while True:
    try:
        choice = int(input("\nEnter the number of your Arduino port: "))
        if 1 <= choice <= len(ports):
            selected_port = ports[choice - 1].device
            break
        else:
            print("❗ Invalid choice. Please enter a valid number.")
    except ValueError:
        print("❗ Please enter a number.")

print(f"\n✅ Selected port: {selected_port}")

# ========== Connect to Arduino ==========
print("🔌 Connecting to Arduino...")
board = pyfirmata2.Arduino(selected_port)
print("✅ Connected successfully!\n")

# ========== Ask user to choose a PWM pin ==========
pwm_pins = [3, 5, 6, 9, 10, 11]  # Valid PWM pins on Arduino Uno

print("💡 Choose a PWM pin for the LED from the following options:")
for i, pin in enumerate(pwm_pins):
    print(f"{i + 1}. D{pin}")

while True:
    try:
        pin_choice = int(input("Enter the number of your chosen PWM pin: "))
        if 1 <= pin_choice <= len(pwm_pins):
            selected_pwm_pin = pwm_pins[pin_choice - 1]
            break
        else:
            print("❗ Invalid choice. Please enter a valid number.")
    except ValueError:
        print("❗ Please enter a number.")

# Create pin string for pyfirmata2: 'd:9:p' style
pwm_pin_str = f'd:{selected_pwm_pin}:p'
ledPin = board.get_pin(pwm_pin_str)

print(f"✅ PWM pin D{selected_pwm_pin} selected for LED brightness.\n")

# Optional: set a ground pin low
groundPin = board.get_pin('d:8:o')
groundPin.write(0)

# ========== Initialize Webcam ==========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)

# ========== Initialize MediaPipe Hands ==========
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=2)

print("📸 Camera started. Show your hand to the camera.")
print("👉 Press 'q' to quit.\n")

# ========== Main Loop ==========
while True:
    success, frame = cap.read()
    if not success:
        continue

    # Convert frame to RGB for MediaPipe
    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    if result.multi_hand_landmarks:
        # Use the first detected hand
        handLandmarks = result.multi_hand_landmarks[0]

        # Get thumb tip and index tip landmarks
        thumbTip = handLandmarks.landmark[4]
        indexTip = handLandmarks.landmark[8]

        # Calculate distance between thumb and index finger (normalized)
        distance = math.sqrt((thumbTip.x - indexTip.x)**2 + (thumbTip.y - indexTip.y)**2)

        # Write distance value to PWM LED pin
        ledPin.write(distance)

        # Print the distance for debugging
        print(f"📏 Distance (0.0 - 1.0): {distance:.4f}")

        # Draw landmarks
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the video frame
    cv2.imshow("Hand Tracking", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n👋 Exiting...")
        break

# ========== Cleanup ==========
cap.release()
cv2.destroyAllWindows()
