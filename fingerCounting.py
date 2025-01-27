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
sorted_files = sorted(myList, key=lambda x: int(x.split('.')[0]))

overlayList = []
for imPath in sorted_files:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    print(imPath)



detector = htm.HandDetector()

tipIds = [4, 8, 12, 16, 20]


while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    img = cv2.flip(img, 1)

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
        img[90:h + 90, 40:w+40] = overlayList[totalFingers - 1]

        cv2.rectangle(img, (10, 265), (170, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (35, 385), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN,
                1, (255, 0, 0), 2)
    

    cv2.imshow("Image", img)
    cv2.waitKey(1)
