import cv2 as cv
import time
import HandTrackingModule as htm
import numpy as np
import os

#############################
wCam, hCam = 1080, 720
#############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon = .8, trackCon = .8)

TIMER = int(3)

fotosFolderPath = 'C:/Users/Facu/Desktop/Facu/Facultad/SGDPV/opencv/Hand Tracking Apps/Fotos'
fotosPathList = os.listdir(fotosFolderPath)
fotos = []
for fotoPath in fotosPathList:
    foto = cv.imread(f'{fotosFolderPath}/{fotoPath}')
    fotos.append(foto)
nFotos = len(fotos) + 1

videosFolderPath = 'C:/Users/Facu/Desktop/Facu/Facultad/SGDPV/opencv/Hand Tracking Apps/Videos'
videosPathList = os.listdir(videosFolderPath)
videos = []
for videoPath in videosPathList:
    video = cv.imread(f'{videosFolderPath}/{videoPath}')
    videos.append(video)
nVideos = len(videos) + 1

size = (wCam, hCam)

pTime = 0

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.detectHands(img, False)
    x, y = detector.findXY(img, 8)

    if x and y:
        cv.circle(img, (x, y), 10, (255, 255, 255), -1)

        if (x > 200 and x < 300) and (y > 50 and y < 150):
            # Foto
            prev = time.time()

            while TIMER >= 0:
                success, img = cap.read()
                img = cv.flip(img, 1)

                cv.putText(img, str(TIMER), (150, 150), 
                            cv.FONT_HERSHEY_COMPLEX,
                            4, (0, 0, 0), 4)
                cv.imshow('Webcam', img)
                cv.waitKey(1)

                cur = time.time()

                if cur - prev >= 1:
                    prev = cur
                    TIMER = TIMER - 1
            else:
                success, img = cap.read()
                img = cv.flip(img, 1)

                # Muestra la foto sacada 2 segundos
                cv.imshow('Webcam', img)
                # Tiempo que se muestra la foto
                cv.waitKey(2000)

                photoPath = f'Hand Tracking Apps/Fotos/{nFotos:04d} - foto.jpg'
                nFotos = nFotos + 1

                # Se guarda la foto en el directorio 'camera.jpg'
                cv.imwrite(photoPath, img)
                # Se resetea el temporizador para futuras fotos
                TIMER = int(3)
        elif (x > 350 and x < 450) and (y > 50 and y < 150):
            # Video
            videoPath = f'Hand Tracking Apps/Videos/{nVideos:04d} - video.mp4'
            vGrabador = cv.VideoWriter(videoPath, cv.VideoWriter_fourcc(*'MJPG'), 10, size)
            prev = time.time()

            while TIMER >= 0:
                success, img = cap.read()
                img = cv.flip(img, 1)
                if success:
                    vGrabador.write(img)

                    cv.imshow('Webcam', img)
                    cv.waitKey(1)

                    cur = time.time()

                    if cur - prev >= 1:
                        prev = cur
                        TIMER = TIMER - 1
            nVideos = nVideos + 1
            TIMER = int(3)
        elif (x > 500 and x < 600) and (y > 50 and y < 150):
            # Ventana Parpadeando

            redImg = np.zeros((200, 200, 3), dtype= 'uint8')
            blueImg = np.zeros((200, 200, 3), dtype= 'uint8')

            redImg[:,:] = (0, 0, 255)
            blueImg[:,:] = (255, 0, 0)

            prev = time.time()
            i = 0

            while TIMER >= 0:
                success, img = cap.read()
                img = cv.flip(img, 1)

                cv.imshow('Webcam', img)
                cv.waitKey(1)

                cur = time.time()
                if i % 2 == 0:
                    cv.imshow('Ventana Parpadeante', redImg)
                else:
                    cv.imshow('Ventana Parpadeante', blueImg)
                if cur - prev >= 0.2:
                    prev = cur
                    i = i + 1
                    if i == 5:
                        TIMER = TIMER - 1
                        i = 0

            cv.destroyWindow('Ventana Parpadeante')
            TIMER = int(3)

    img[50:150, 200:300] = cv.imread('Hand Tracking Apps/ButtonAppImages/foto.png') # Foto Button
    img[50:150, 350:450] = cv.imread('Hand Tracking Apps/ButtonAppImages/videoCamara.png') # Video Button
    img[50:150, 500:600] = cv.imread('Hand Tracking Apps/ButtonAppImages/parpadea.png') # Parpadea Button

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (50, 40), cv.FONT_HERSHEY_COMPLEX, 1, 
                    (0, 255, 0), 2)

    cv.imshow("Webcam", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()