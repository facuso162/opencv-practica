#clase del 16/06/22

#import numpy as np
import cv2
#from matplotlib import pyplot as plt

# instale matplotlib al pedo

cap = cv2.VideoCapture(0)
contador=0
ubicacion = (100,150)
font = cv2.FONT_HERSHEY_TRIPLEX
tamañoLetra = 5
# del 0 al 255
colorLetra = (255,255,255)
grosorLetra = 10

while(True):
  ret, frame = cap.read()
  contador=contador+1
  # invierte la imagen para que tenga un efecto espejo
  frame = cv2.flip(frame, 1)
  # bottomLeftOrigin = False, ya esta por defecto
  cv2.putText(frame, str(contador), ubicacion, font, tamañoLetra, colorLetra, grosorLetra)
  cv2.imshow('frame',frame)
  
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

print(contador)
cap.release()
cv2.destroyAllWindows()