import cv2 as cv

#############################
wCam, hCam = 1080, 720
#############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

wCapture = int(cap.get(3))
hCapture = int(cap.get(4))

size = (wCapture, hCapture)

if not cap.isOpened(): 
    print("Error reading video file")

fourcc = cv.VideoWriter_fourcc(*'MJPG')
videoPath = 'Videos/video.avi'
vGrabador = cv.VideoWriter(videoPath, fourcc, 10, size)

while True:

    success, img = cap.read()

    cv.imshow('Webcam', img)

    if success:
        vGrabador.write(img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
vGrabador.release()
cv.destroyAllWindows()
