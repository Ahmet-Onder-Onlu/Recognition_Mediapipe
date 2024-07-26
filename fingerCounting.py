import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "/home/user34/Desktop/gestureVolumeControl/images"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    


detector = htm.HandDetector()

tipIds = [4, 8, 12, 16, 20]


while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            
        #print(fingers)
        totalFingers = fingers.count(1)


        h, w, c = overlayList[0].shape
        img[100:h + 100, 80:w+80] = overlayList[totalFingers - 1]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = cv2.flip(img, 1)

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN,
                1, (255, 0, 0), 2)
    

    cv2.imshow("Image", img)
    cv2.waitKey(1)