import cv2 as cv
import time
import HandTrackingModule as htm

cap = cv.VideoCapture(0)

#############################
wCam, hCam = 1080, 720
#############################

cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon = .8, trackCon = .8)

tipIds = [4, 8, 12, 16, 20]

pTime = 0

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.detectHands(img)
    lmList = detector.getPositions(img)

    if len(lmList) > 0:
        fingers = detector.fingersUp(lmList)
        totalFingers = fingers.count(1)

        cv.rectangle(img, (20, 225), (170, 425), (10, 10, 10), -1)
        cv.putText(img, str(totalFingers), (45, 375), cv.FONT_HERSHEY_PLAIN,
                    10, (255, 255, 255), 25)

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