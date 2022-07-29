# YOLO object detection
import cv2 as cv
import numpy as np
import time

img = cv.imread('./Imagenes/horse.jpg')
cv.imshow('window',  img)
cv.waitKey(0)

# Give the configuration and weight files for the model and load the network.
net = cv.dnn.readNetFromDarknet('YOLO/yolov3.cfg', 'YOLO/yolov3.weights')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

ln = net.getLayerNames()
print(len(ln), ln)

# construct a blob from the image
blob = cv.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
r = blob[0, 0, :, :]

text = f'Blob shape={blob.shape}'
cv.putText(r, text, (60, 40), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 0, 0), 2)
cv.imshow('blob', r)
# aca iba el text, lo movi 3 lineas mas arriba
#cv.displayOverlay('blob', text)
cv.waitKey(0)

net.setInput(blob)
t0 = time.time()
outputs = net.forward(ln)
t = time.time()

#cv.displayOverlay('window', f'forward propagation time={t-t0}')
cv.putText(img, f'forward propagation time={t-t0}', (60, 40), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 0, 0), 2)
cv.imshow('window',  img)
cv.waitKey(0)
cv.destroyAllWindows()