import cv2
import mediapipe as mp
import time
import os
class handDetector():

    folderPath = 'C:/Users/Facu/Desktop/Facu/Facultad/SGDPV/opencv/Hand Tracking Apps/FingerImages'
    imPathList = os.listdir(folderPath)
    images = []
    for imPath in imPathList:
        img = cv2.imread(f'{folderPath}/{imPath}')
        images.append(img)

    HAND_GESTURES: list = [
        # Arreglos que simbolizan los gestos
        # Los arreglos comentados son gestos
        # que no se agregaron, para agregarlo
        # se descomenta y se le agrega una imagen
        # que sera mostrada al reproducir el gesto
        [[0,0,0,0,0], images[0]],
        # [0,0,0,0,1],
        # [0,0,0,1,0],
        # [0,0,0,1,1],
        # [0,0,1,0,0],
        # [0,0,1,0,1],
        # [0,0,1,1,0],
        # [0,0,1,1,1],
        [[0,1,0,0,0], images[1]],
        # [0,1,0,0,1],
        # [0,1,0,1,0],
        # [0,1,0,1,1],
        [[0,1,1,0,0], images[2]],
        # [0,1,1,0,1],
        [[0,1,1,1,0], images[3]],
        [[0,1,1,1,1], images[4]],
        # [1,0,0,0,0],
        # [1,0,0,0,1],
        # [1,0,0,1,0],
        # [1,0,0,1,1],
        # [1,0,1,0,0],
        # [1,0,1,0,1],
        # [1,0,1,1,0],
        # [1,0,1,1,1],
        # [1,1,0,0,0],
        # [1,1,0,0,1],
        # [1,1,0,1,0],
        # [1,1,0,1,1],
        # [1,1,1,0,0],
        # [1,1,1,0,1],
        # [1,1,1,1,0],
        [[1,1,1,1,1], images[5]]
    ]

    def __init__(self, mode: bool=False, maxHands: int= 1, modelComplexity: int = 1, 
                detectionCon: float=0.5, trackCon: float=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        # self.mpHands = mp.solutions.hands
        self.hands = mp.solutions.hands.Hands(mode, maxHands, modelComplexity,
                                        detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # Detecta la/las manos en la imagen img, y las dibuja si lo indica el parametro
    def detectHands(self, img: cv2.Mat, draw: bool=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               mp.solutions.hands.HAND_CONNECTIONS)
        return img
    
    # Devuelve la posicion x e y del id seleccionado
    def findXY(self, img: cv2.Mat, id: int, handNum: int = 0):

        if (handNum > self.maxHands - 1 ):
            raise ValueError(f"El numero de la mano debe ser menor a self.maxHands = {self.maxHands}")

        if id > 20 or id < 0:
            # Porque los ids de la mano van de 0 a 20
            raise ValueError("El id debe estar entre 0 y 20")

        if self.results.multi_hand_landmarks:
            # Selecciona la mano indicada en el parametro handNum
            selectedHand = self.results.multi_hand_landmarks[handNum]
            height, width, channels = img.shape
            lm = selectedHand.landmark
            x, y = int(lm[id].x * width), int(lm[id].y * height)
            return x, y
        else:
            # Cuando no detecta la mano
            return None, None

    # Devuelve una lista de las posiciones de los ids de la mano indicada
    def getPositions(self, img, handNum = 0):

        if (handNum > self.maxHands - 1 ):
            raise ValueError(f"El numero de la mano debe ser menor a self.maxHands = {self.maxHands}")

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for lm in myHand.landmark:
                height, width, channels = img.shape
                x, y = int(lm.x * width), int(lm.y * height)
                lmList.append([x, y])
        # Si no detecta la mano devuelve un arreglo vacio
        return lmList

    # Devuelve un arreglo que simboliza el gesto de la mano
    # 1 = levantado, 0 = guardado
    # Ejemplo: [0, 0, 1, 0, 0] es el gesto de 'fuck you'
    def fingersUp(self, lmList: list):
        
        # Ids que representan la punta de los dedos
        tipIds = [4, 8, 12, 16, 20]
        fingers = []
        if len(lmList) == 0:
            raise ValueError("El arreglo lmList no puede ser el arreglo vacio")
        for id in tipIds:
            if id == 4:
                # Pulgar
                if lmList[id][0] < lmList[id - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # Los otros 4 dedos
                if lmList[id][1] < lmList[id - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

def main():

    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    hd = handDetector()

    while True:

        success, img = cap.read()

        img = cv2.flip(img, 1)

        img = hd.detectHands(img)

        x,y = hd.findXY(img, 8)
        print(x, y)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        if x and y:
            cv2.circle(img, (x, y), 10, (255, 0, 255), cv2.FILLED)

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()