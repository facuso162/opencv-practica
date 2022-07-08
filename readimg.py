import cv2 as cv

# lee la imagen y la guarda en una variable
img = cv.imread('Imagenes/escudobc.png')

# muestra la imagen (titulo ventana, imagen)
cv.imshow('Escudo BC', img)

# con 0 espera indefinidamente
cv.waitKey(0)