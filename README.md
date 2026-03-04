# AI-Driven Gesture Volume Controller

A real-time Human-Computer Interaction (HCI) system developed as part of my portfolio as a **Mechatronics Engineer**. This application allows users to control system volume through hand gestures using Computer Vision.

## 🛠️ Key Features
* **Asynchronous Hand Tracking:** Uses MediaPipe Tasks API for smooth, real-time performance.
* **21-Landmark Detection:** Precise mapping of hand points to interpret volume adjustments.
* **Visual Feedback:** Includes an on-screen volume bar and skeleton overlay for a better user experience.

## 💻 Tech Stack
* **Python**: Core logic and signal processing.
* **OpenCV & MediaPipe**: Vision and hand tracking.
* **Pycaw**: Windows audio control.

## 📐 How it Works
The system calculates the **Euclidean Distance** between the thumb (Landmark 4) and the index finger (Landmark 8). This value is then interpolated to map to the system's decibel range.

## 🚀 Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Download the `hand_landmarker.task` model and place it in the project root.
4. Run `python main.py`.

## 🔎 Example of use 

https://github.com/user-attachments/assets/9ff6251e-e338-4abe-9708-e7bac1485436




