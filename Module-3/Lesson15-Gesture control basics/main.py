# import cv2
# import mediapipe as mp

# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils

# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=2,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )

# # Start webcam
# cap = cv2.VideoCapture(0)

# while True:
#     success, frame = cap.read()
#     if not success:
#         break

#     # Convert the BGR image to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the frame and detect hands
#     results = hands.process(rgb_frame)

#     # Draw hand landmarks and bounding box if any hands detected
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Get bounding box coordinates
#             h, w, c = frame.shape
#             x_min = w
#             y_min = h
#             x_max = y_max = 0

#             for lm in hand_landmarks.landmark:
#                 x, y = int(lm.x * w), int(lm.y * h)
#                 if x < x_min:
#                     x_min = x
#                 if y < y_min:
#                     y_min = y
#                 if x > x_max:
#                     x_max = x
#                 if y > y_max:
#                     y_max = y

#             # Draw green box around hand
#             cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (0, 255, 0), 2)

#             # Draw landmarks (optional)
#             mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#     # Show the frame
#     cv2.imshow("Hand Tracker", frame)

#     # Exit on 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

# Set up webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture image.")
        break
    
    # Convert to HSV for color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the range for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a mask to detect skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply the mask to the frame
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Find contours (hand shape) in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If contours are found, draw them
    if contours:
        max_contour = max(contours, key=cv2.contourArea)  # Get largest contour
        if cv2.contourArea(max_contour) > 500:  # Ignore small contours
            # Draw the bounding box around the detected hand
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Get the center of the hand for further tracking or interaction
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot at center
    
    # Display the original and result frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Filtered Frame', result)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()