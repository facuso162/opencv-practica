import cv2 as cv
import numpy as np

# crea un arreglo de dimension [500][500][3]
# 500 filas, 500 columnas y 3 elementos en cada una de esas celdas
# cada uno de esos 3 elementos es un entero sin signo de 8 bits 'uint8'
# con 8 bits se forman 256 combinaciones, las mismas que cada elemento del formato RGB
# una imagen es un arreglo de dimension [n][m][3] de tamaño nxm
# con diferentes valores en esos 3 elementos, formando diferentes colores
# la funcion numpy.zeros, genera un arreglo de las dimensiones dadas, lleno de ceros
# el negro se reprensenta en formato RGB como (0, 0, 0)
# por lo tanto la imagen es una imagen en negro 
img = np.zeros((500,500,3), dtype='uint8')
cv.imshow('Negro', img)

# 1. Un cuadrado azul desde el pixel 200 al 300 de ancho
# y del 300 al 400 de alto
img[200:300, 300:400] = (0,0,255)
cv.imshow('Rectangulo Azul', img)

# 2. Dibuja en la imagen 'img' un rectangulo 
# desde el pixel (0,0) al (250, 250) en este caso
# ya que shape[1]//2 da la mitad del ancho de la imagen
# y shape[0]//2 da la mitad del alto de la imagen.
# El rectangulo es de color verde (0, 255, 0)
# 0 de rojo, 255 de verde y 0 de azul (RedGreenBlue = RGB)
# thickness es el grosor de la linea que dibuja el rectangulo
# -1 significa que rellena el rectangulo 
cv.rectangle(img, (0,0), (img.shape[1]//2, img.shape[0]//2), (0,255,0), thickness=-1)
cv.imshow('Rectangulo', img)

# 3. Dibuja en la imagen 'img' un circulo relleno  
# de color azul, con centro en (250, 250) y de radio 40
cv.circle(img, (img.shape[1]//2, img.shape[0]//2), 40, (0,0,255), thickness=-1)
cv.imshow('Circulo', img)

# 4. Dibuja en la imagen 'img' una linea desde
# el punto (100, 250) al (300, 400) de color
# blanco (255, 255, 255) de 3 pixeles de grosor 
cv.line(img, (100,250), (300,400), (255,255,255), thickness=3)
cv.imshow('Linea', img)

# 5. Escribe en la imagen 'img'
# un texto que dice 'Hola bro'
# con extremo inferior izquierdo en el punto (0, 225)
# con fuente cv.FONT_HERSHEY_TRIPLEX,
# con una escala = 1, de un color gris
# y un grosor de 2 pixeles
cv.putText(img, 'Hola bro', (0,225), cv.FONT_HERSHEY_TRIPLEX, 1.0, (60, 60, 60), 2)
cv.imshow('Texto', img)

cv.waitKey(0)