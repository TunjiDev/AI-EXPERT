# Installation Guide for Gesture-Controlled Scroll System

## 📦 Dependencies Installation

### Windows
# Install Python packages
pip install mediapipe opencv-python pyautogui

# Install Microsoft Visual C++ Redistributable
winget install Microsoft.VCRedist.2015+.x64




# For Apple Silicon (M1/M2/M3)
pip3 install mediapipe-silicon opencv-python pyautogui

# For Intel Macs
pip3 install mediapipe opencv-python pyautogui



🛠️ Post-Installation Steps

Verification Script
Create test_install.py:

python

import cv2, mediapipe, pyautogui
print("✅ All dependencies installed successfully!")
Run with:
python test_install.py

🚨 Troubleshooting
Common Issues
Windows:
# Fix OpenCV issues
pip uninstall opencv-python && pip install opencv-python


macOS:

# Camera permission fix:
1. System Preferences → Security & Privacy → Camera
2. Check "VS Code" in application list



MediaPipe Installation Issues:

# Force reinstall for Apple Silicon
pip3 uninstall mediapipe-silicon && pip3 install mediapipe-silicon


🚀 Run the Program

Note: Keep hands 1-2 feet from camera for best detection

