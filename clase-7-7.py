# Hay que capturar la mano, y
# en uno de los puntos de la mano,
# insertar una imagen que se vaya moviendo junto
# con la mano, cuando esta llegue a un limite de la
# ventana se debe cerrar la imagen.
# 
# Por ejemplo: en la punta de mi dedo indice inserto 
# la imagen de un perro, la cual se mueve junto con el movimiento
# de mi mano, cuando esta imagen se vea cortada por los limites
# de la ventana se debe cerrar.
import cv2 as cv
import HandTrackingApps.HandTrackingModule as htm

#############################
wCam, hCam = 1080, 720
#############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon = .8, trackCon = .8)

while True:

    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.detectHands(img, False)
    x, y = detector.findXY(img, 8)

    if x and y:
        topLeft = (x - 75, y - 75)
        topRight = (x + 75, y - 75)
        bottomLeft = (x - 75, y + 75)
        bottomRight = (x + 75, y + 75)

        if (topLeft[0] >= 0 and topLeft[1] >= 0) and (
        topRight[0] <= img.shape[1] and topRight[1] >= 0) and (
        bottomLeft[0] >= 0 and bottomLeft[1] <= img.shape[0]) and (
        bottomRight[0] <= img.shape[1] and bottomRight[1] <= img.shape[0]):
            img[y-75 : y+75 , x-75 : x+75] = cv.imread('Imagenes/carita_feliz.png')
            cv.rectangle(img, topLeft, bottomRight, (90, 240, 70), 2)
        else:
            cv.circle(img, (x, y), 6, (95, 80, 230), -1)
            cv.rectangle(img, topLeft, bottomRight, (95, 80, 230), 2)

    cv.imshow('Webcam', img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()