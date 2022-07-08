import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
# lo hago con 1 mano para que haya mas fps
# static_image_mode = False, esta por defecto asi
# si lo pongo en True todo el tiempo esta en deteccion
hands = mpHands.Hands(static_image_mode = False, max_num_hands = 1)
mpDrawingTool = mp.solutions.drawing_utils

# n = 0

currentTime = 0
previousTime = 0

while True:
    success, frame = cap.read()
    frame = cv.flip(frame, 1)
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    cv.rectangle(frame, (100, 50), (200, 150), (255, 0, 0), -1)
    cv.rectangle(frame, (250, 50), (350, 150), (0, 255, 0), -1)
    cv.rectangle(frame, (400, 50), (500, 150), (0, 0, 255), -1)

    # n = n + 1
    # print(f"Frame nro: {n}")
    # print(results.multi_hand_landmarks)
    # if results.multi_hand_landmarks:
    #     # me dice cuantas manos detecte
    #     print("Cuantas manos?", len(results.multi_hand_landmarks))

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            mpDrawingTool.draw_landmarks(frame, handLandmarks, mpHands.HAND_CONNECTIONS)
            for id, landmark in enumerate(handLandmarks.landmark):
                height, width, channels = frame.shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                if id == 8:
                    cv.circle(frame, (x, y), 15, (255, 30, 220), -1)
                    if (x >= 100 and x <= 200) and (y >= 50 and y <= 150):
                        print("Boton A apretado")
                    elif (x >= 250 and x <= 350) and (y >= 50 and y <= 150):
                        print("Boton B apretado")
                    elif (x >= 400 and x <= 500) and (y >= 50 and y <= 150):
                        print("Boton C apretado")

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv.putText(frame, str(int(fps)), (20, 60), cv.FONT_HERSHEY_PLAIN, 2, (60, 230, 60), 3)

    cv.imshow('WebCam', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()