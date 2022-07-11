import cv2 as cv
import mediapipe as mp

# Grabbing the Holistic Model from Mediapipe and
# Initializing the Model
mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
  
# Initializing the drawng utils for drawing the facial landmarks on image
mp_draw = mp.solutions.drawing_utils

capture = cv.VideoCapture(0)

while True:

    isTrue, frame = capture.read()

    frame.flags.writeable = False
    results = holistic_model.process(frame)
    frame.flags.writeable = True

    mp_draw.draw_landmarks(
      frame, 
      results.right_hand_landmarks, 
      mp_holistic.HAND_CONNECTIONS
    )

    mp_draw.draw_landmarks(
      frame, 
      results.left_hand_landmarks, 
      mp_holistic.HAND_CONNECTIONS
    )

    frame = cv.rectangle(frame, (50, 50), (150, 150), (255,255,255), 5)

    cv.imshow('Video Webcam', frame)

    if cv.waitKey(1) & 0xFF == ord('p'):
        break

capture.release()
cv.destroyAllWindows()