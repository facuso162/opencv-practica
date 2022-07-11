import math
from operator import imod
import cv2 as cv
from cv2 import sqrt
import numpy as np
import time
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#############################
wCam, hCam = 1080, 720
#############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon = .8, trackCon = .8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

pTime = 0

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.detectHands(img, False)
    lmList = detector.getPositions(img)
    if len(lmList) > 0:
        # Coordenadas x,y de la punta del pulgar
        px, py = lmList[4][0], lmList[4][1]
        # Coordenadas x,y de la punta del indice
        ix, iy = lmList[8][0], lmList[8][1]
        # Coordenadas x,y del punto medio
        cx, cy = (px + ix) // 2, (py + iy) // 2
        
        # Linea entre punto pulgar - punto indice
        cv.line(img, (px, py), (ix, iy), (255, 0, 255), 2)
        # Punto pulgar
        cv.circle(img, (px, py), 10,  (255, 255, 255), -1)
        # Punto indice
        cv.circle(img, (ix, iy), 10,  (255, 255, 255), -1)
        # Punto medio
        cv.circle(img, (cx, cy), 10,  (255, 255, 255), -1)

        # Distancia entre punto pulgar - punto indice
        d = math.sqrt((px - ix)**2+(py - iy)**2)

        if d <= 50:
            # Marca tope inferior
            cv.circle(img, (cx, cy), 10,  (0, 255, 0), -1)
        elif d >= 300:
            # Marca tope superior
            cv.circle(img, (cx, cy), 10,  (0, 0, 255), -1)

        # Cambio volumen
        # Hand Range 50 - 300
        # Volume Range -65 - 0 -> minVol - maxVol
        vol = np.interp(d, [50, 300], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        # Relleno barra volumen
        # VolBar Range 400 - 150
        volBar = np.interp(d, [50, 300], [400, 150])
        cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Barra volumen vacia
    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
    
    # Indicador FPS's
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (20, 60), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv.imshow("Webcam", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()