import cv2
import mediapipe as mp
import imutils

SENTDATA = 0
cap = cv2.VideoCapture('PO.png')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
mpHands = mp.solutions.hands #ใช้คำสั่ง เพื่อเตรียมข้อมูลสำหรับการตรวจจับมือ
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils #ในการวาดผลลัพธ์ลงไป

fingerCoordinates = [(8,6),(12,10),(16,14),(20,18)] #พิกัดนิ้ว
thumbCoordinate = (4,2) #หัวแม่มือ

while True:
    success, img = cap.read() #ใช้ในการอ่านเฟรมวิดีโอ
    results = hands.process(img) #ผลลัพธ์
    multiLandMarks = results.multi_hand_landmarks
    #ใช้ระบุรายละเอียดของมือจะถูกเก็บไว้ในตัวแปร
    # print(multiLandMarks)


    if multiLandMarks:
        handsPoints = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            #รับค่าข้อมูลที่รับมาจากวิดีโอเพื่อใช้วาดผลลัพธ์ลงไป และระบุ landmark เพื่อระบุจุดที่ต้องการวาดผลลัพธ์

            for idx, lm in enumerate(handLms.landmark):
                #หาจุดตำแหน่งของนิ้วมือ
                # print(idx,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                # print(cx,cy)
                handsPoints.append((cx,cy))
        for point in handsPoints:
            cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)
            # print(point)
        upCountL = 0
        upCountR = 0

        # นิ้วชี้ถึงก้อย
        for coordinate in fingerCoordinates:  # 1 0 | 4 5
            if handsPoints[coordinate[0]][1] < handsPoints[coordinate[1]][1]:
                upCountR += 1
        # นิ้วหัวแม่มือ
        if handsPoints[thumbCoordinate[0]][0] > handsPoints[thumbCoordinate[1]][0]:
            upCountL += 1
        if upCountR == 0 and upCountL == 0:
            TEXZT = "OFF 2 LIGHT"
            SENTDATA = "OFF 2 LIGHT"
        elif upCountR == 0 and upCountL == 1:
            TEXZT = "OFF 2 LIGHT"
            SENTDATA = "OFF 2 LIGHT"

            #  เปิด ทั้ง หน้า หลัง
        elif upCountR == 4 and upCountL == 0:
            TEXZT = "ON 2 LIGHT"
            SENTDATA = "ON 2 LIGHT"
        elif upCountR == 4 and upCountL == 1:
            TEXZT = "ON 2 LIGHT"
            SENTDATA = "ON 2 LIGHT"
        else:
            TEXZT = "NONE"
            SENTDATA = "NONE"
        print(upCountR, upCountL)
        cv2.putText(img, TEXZT, (150, 150), cv2.FONT_HERSHEY_PLAIN, 8, (255, 255, 0), 12)
    cv2.imshow("HProject", img)
    cv2.waitKey(1)

