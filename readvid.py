import cv2 as cv

# con 0 captura de la webcam
# sino poner la ubicacion del video para reproducirlo
capture = cv.VideoCapture(0)

while True:

    # capture.read() devuelve un frame de la captura obtenida de la webcam
    # succes es True si pudo leer un frame del video, de lo contrario es False
    success, frame = capture.read()

    # se muestra el frame
    cv.imshow('Video Webcam', frame)

    # < & 0xFF > es una bite mask utilizada para cortar el binario de un caracter
    # logrando que solo se lean los ultimos bits, que son los que determinan al caracter
    # y que se compare correctamente con el ASCII del caracter especificado, en este caso 'p'
    # & es el and binario, 0 & 0 = 0, 0 & 1 = 0, 1 & 0 = 0, 1 & 1 = 1
    # el numero hexadecimal FF es el 11111111, los necesarios para capturar el caracter de cv.waitKey()
    if cv.waitKey(1) & 0xFF == ord('p'):
        break

# libera la captura
capture.release()

# destruye las ventanas
cv.destroyAllWindows()

# el error (-215:Assertion failed) indica que se termino el video y no hay un nuevo
# frame para capturar o que la direccion de la imagen esta mal escrita o no existe