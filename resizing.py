import cv2 as cv

def rescaleFrame(frame: cv.Mat, scale: float = 0.75) -> cv.Mat:
    # Imagenes, Videos y Lives
    # [1] es el ancho
    # [0] es el alto
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimentions = (width, height)

    return cv.resize(frame, dimentions, interpolation = cv.INTER_AREA)

# Todavia no se como usar esta funcion
def changeRes(capture: cv.VideoCapture, widht: int, height: int):
    # Lives
    capture.set(3, widht)
    capture.set(4, height)

img = cv.imread('Imagenes/2pac.jpg')

capture = cv.VideoCapture('Videos/messirve.mp4')

cv.imshow('2Pac', img)

cv.waitKey(0)

cv.imshow('2Pac Resized', rescaleFrame(img))

cv.waitKey(0)

cv.destroyAllWindows()

while True:

    # se hace en un bloque try-except para que cuando 
    # no haya mas frames en el video no tire error
    try:
        success, frame = capture.read()
        cv.imshow('Video Messi', frame)
        if cv.waitKey(1) & 0xFF == ord('p'):
            break
    except:
        print("Termino el video")
        break

cv.destroyAllWindows()

# se vuelve a asignar el video, para que lo vuelva a leer frame a frame desde 0
capture = cv.VideoCapture('Videos/messirve.mp4')

while True:

    try:
        success, frame = capture.read()
        cv.imshow('Video Cachetada Resized', rescaleFrame(frame, 0.5))
        if cv.waitKey(1) & 0xFF == ord('p'):
            break
    except:
        print("Termino el video")
        break

capture.release()
cv.destroyAllWindows()