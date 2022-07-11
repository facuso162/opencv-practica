import cv2 as cv
import time
import HandTrackingModule as htm
import numpy as np

#############################
wCam, hCam = 1080, 720
#############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon = .8, trackCon = .8)

pTime = 0

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.detectHands(img)
    lmList = detector.getPositions(img)

    if len(lmList) > 0:
        fingers = detector.fingersUp(lmList)
        for hg in htm.HandDetector.HAND_GESTURES:
            if np.array_equal(fingers, hg[0]):
                img[50:350, 50:250] = hg[1]
                break

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (50, 40), cv.FONT_HERSHEY_COMPLEX, 1, 
                    (255, 0, 0), 2)

    cv.imshow("Webcam", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()