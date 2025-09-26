# import cv2
# import numpy as np

# class SimpleEmotionDetector:
#     def __init__(self):
#         # Load Haar cascades for face, eye, and mouth detection
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#         self.mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
#     def detect_emotion(self, face_roi):
#         """
#         Simple emotion detection based on facial features
#         This is a basic approach and won't be as accurate as ML models
#         """
#         gray_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
#         # Detect eyes and mouth
#         eyes = self.eye_cascade.detectMultiScale(gray_roi, 1.1, 5)
#         mouths = self.mouth_cascade.detectMultiScale(gray_roi, 1.1, 20)
        
#         # Basic emotion logic based on detected features
#         emotion = "Neutral"
#         confidence = 0.5
        
#         # If we detect a smile (mouth region)
#         if len(mouths) > 0:
#             emotion = "Happy"
#             confidence = 0.7
        
#         # If we detect very few or no eyes (possibly squinting/angry)
#         elif len(eyes) < 2:
#             emotion = "Angry"
#             confidence = 0.6
        
#         # If we detect normal eyes but no smile
#         elif len(eyes) >= 2 and len(mouths) == 0:
#             # Analyze the mouth region for sadness
#             h, w = gray_roi.shape
#             mouth_region = gray_roi[int(h*0.6):h, int(w*0.2):int(w*0.8)]
            
#             if mouth_region.size > 0:
#                 # Check if mouth corners are turned down (very basic)
#                 mean_brightness = np.mean(mouth_region)
#                 if mean_brightness < 90:  # Darker mouth region might indicate frown
#                     emotion = "Sad"
#                     confidence = 0.6
        
#         return emotion, confidence
    
#     def analyze_facial_expression(self, face_roi):
#         """
#         More sophisticated analysis using contour detection
#         """
#         gray_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
#         # Apply Gaussian blur to reduce noise
#         blurred = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        
#         # Edge detection to find facial contours
#         edges = cv2.Canny(blurred, 50, 150)
        
#         # Find contours
#         contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         emotion = "Neutral"
#         confidence = 0.5
        
#         # Analyze contour characteristics
#         if len(contours) > 10:
#             # More contours might indicate more facial movement (happiness/surprise)
#             emotion = "Happy"
#             confidence = 0.6
#         elif len(contours) < 5:
#             # Fewer contours might indicate a more flat expression (sad/neutral)
#             emotion = "Sad"
#             confidence = 0.5
        
#         # Combine with basic feature detection
#         basic_emotion, basic_confidence = self.detect_emotion(face_roi)
        
#         # Use the result with higher confidence
#         if basic_confidence > confidence:
#             emotion = basic_emotion
#             confidence = basic_confidence
            
#         return emotion, confidence

# # Initialize the detector
# detector = SimpleEmotionDetector()

# # Start video capture from the default webcam
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# print("Emotion Detection Started!")
# print("Press 'q' to quit")
# print("Note: This is a basic implementation - results may vary")

# while True:
#     ret, frame = cap.read()
    
#     if not ret:
#         print("Error: Failed to capture image")
#         break
    
#     # Convert frame to grayscale for face detection
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Detect faces
#     faces = detector.face_cascade.detectMultiScale(gray, 1.1, 5)
    
#     # Process each detected face
#     for (x, y, w, h) in faces:
#         # Draw rectangle around face
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
#         # Extract face region
#         face_roi = frame[y:y+h, x:x+w]
        
#         if face_roi.size > 0:
#             # Detect emotion
#             emotion, confidence = detector.analyze_facial_expression(face_roi)
            
#             # Display emotion and confidence
#             text = f"{emotion} ({confidence:.2f})"
#             cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
#             # Draw additional info
#             cv2.putText(frame, "Basic Detection", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
#     # Add instructions on the frame
#     cv2.putText(frame, "Press 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#     cv2.putText(frame, "Simple Emotion Detection", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
#     # Display the frame
#     cv2.imshow('Simple Emotion Detection', frame)
    
#     # Exit on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Clean up
# cap.release()
# cv2.destroyAllWindows()
# print("Emotion detection stopped.")

# ===================================================================
# import cv2
# from deepface import DeepFace

# # Load OpenCV's Haar cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to capture image")
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     for (x, y, w, h) in faces:
#         # Draw face rectangle
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Crop the face
#         face_roi = frame[y:y+h, x:x+w]

#         try:
#             # Analyze emotions only on the face
#             analysis = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

#             dominant_emotion = analysis[0]['dominant_emotion']

#             # Show emotion above face box
#             cv2.putText(frame, dominant_emotion, (x, y - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#         except Exception as e:
#             print("Detection error:", e)

#     cv2.imshow("Emotion Detection", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# ========================================================================
# import cv2
# from deepface import DeepFace

# # Start webcam
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to capture image")
#         break

#     try:
#         # Analyze emotions using DeepFace (it auto-downloads pretrained model)
#         analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

#         # Get dominant emotion
#         dominant_emotion = analysis[0]['dominant_emotion']

#         # Display emotion text on the frame
#         cv2.putText(frame, f"Emotion: {dominant_emotion}", (50, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
#     except Exception as e:
#         print("Error:", e)

#     # Show video
#     cv2.imshow("Emotion Detection", frame)

#     # Exit on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# ========================================================================
# import cv2
# from fer import FER

# # Initialize the FER emotion detector
# emotion_detector = FER(mtcnn=True)  # mtcnn=True improves face detection

# # Start video capture from the default webcam
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to capture image")
#         break

#     # Detect emotions in the current frame
#     emotion_data = emotion_detector.detect_emotions(frame)

#     # Draw bounding boxes and display emotions
#     for face in emotion_data:
#         (x, y, w, h) = face["box"]
#         emotions = face["emotions"]

#         # Find dominant emotion
#         dominant_emotion = max(emotions, key=emotions.get)
#         emotion_score = emotions[dominant_emotion]

#         # Draw rectangle and emotion label
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#         emotion_text = f"{dominant_emotion}: {emotion_score:.2f}"
#         cv2.putText(frame, emotion_text, (x, y - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

#     # Show the frame
#     cv2.imshow("Face and Emotion Detection", frame)

#     # Exit when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# import cv2

# import numpy as np

# from fer import FER


# # Initialize the FER emotion detector

# emotion_detector = FER()


# # Start video capture from the default webcam

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():

#     print("Error: Could not open camera.")
    
#     exit()


# while True:

#     ret, frame = cap.read()
    
#     if not ret:
    
#         print("Error: Failed to capture image")
        
#         break


#     # Use FER to detect emotions directly on the frame
    
#     emotion_data = emotion_detector.detect_emotions(frame)


#     # Process each detected face and its emotions
    
#     for face in emotion_data:
    
#         # Extract face coordinates
        
#         (x, y, w, h) = face["box"]
        
#         emotions = face["emotions"]


#         # Find the dominant emotion
        
#         dominant_emotion = max(emotions, key=emotions.get)
        
#         emotion_score = emotions[dominant_emotion]


#         # Draw rectangle around the face
        
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


#         # Display the predicted emotion on the frame
        
#         emotion_text = f"{dominant_emotion}: {emotion_score:.2f}"
        
#         cv2.putText(frame, emotion_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


#     # Display the resulting frame
    
#     cv2.imshow('Face and Emotion Detection', frame)


#     # Exit on pressing the 'q' key
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
    
#         break


# # Release the capture and close any open windows

# cap.release()

# cv2.destroyAllWindows()

# =========================================
import cv2

import numpy as np

from tensorflow.keras.models import load_model # type: ignore

from keras.preprocessing.image import img_to_array


# Load the pre-trained Haar Cascade classifier for face detection

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Load the emotion detection model (e.g., fer2013)

emotion_model = load_model('emotion_model.h5')  # Replace with your model path


# Define emotion labels

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


# Start video capture from the default webcam

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Error: Could not open camera.")
    
    exit()


while True:

    ret, frame = cap.read()
    
    if not ret:
    
        print("Error: Failed to capture image")
        
        break


    # Convert frame to grayscale (face detection works better on grayscale)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Detect faces in the grayscale image
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


    # For each detected face, perform emotion recognition
    
    for (x, y, w, h) in faces:
    
        # Draw rectangle around the face
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


        # Extract the ROI for emotion detection
        
        roi_gray = gray[y:y + h, x:x + w]
        
        roi_color = frame[y:y + h, x:x + w]


        # Resize the face to match the input shape of the emotion model
        
        roi_resized = cv2.resize(roi_gray, (48, 48))
        
        roi_resized = roi_resized.astype('float32') / 255
        
        roi_resized = img_to_array(roi_resized)
        
        roi_resized = np.expand_dims(roi_resized, axis=0)


        # Predict emotion
        
        emotion_pred = emotion_model.predict(roi_resized)
        
        max_index = np.argmax(emotion_pred[0])
        
        predicted_emotion = emotion_labels[max_index]


        # Display the predicted emotion on the frame
        
        cv2.putText(frame, predicted_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


    # Display the resulting frame
    
    cv2.imshow('Face and Emotion Detection', frame)


    # Exit on pressing the 'q' key
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
    
        break


# Release the capture and close any open windows

cap.release()

cv2.destroyAllWindows()