import cv2 #เป็นไลบรารีสำหรับจัดการเกี่ยวกับรูปภาพ
import mediapipe as mp
import imutils # library เบื้องต้นของ image processing พวกหมุนภาพ กลับภาพ ปรับขนาด
SENTDATA = 0


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
mpHands = mp.solutions.hands #ใช้คำสั่ง mp.solutions.hands.Hands() เพื่อเตรียมข้อมูลสำหรับการตรวจจับมือ
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils #ในการวาดผลลัพธ์ลงไปจะใช้คำสั่ง

fingerCoordinates = [(8,6),(12,10),(16,14),(20,18)] #พิกัดนิ้ว
thumbCoordinate = (4,2) #ทัม คอเน็ต หัวแม่มือ

while True:
    success, img = cap.read() #ใช้ในการอ่านเฟรมวิดีโอ
    # imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # results = hands.process(imgRGB)
    results = hands.process(img) #ผลลัพธ์
    multiLandMarks = results.multi_hand_landmarks #ใช้ระบุรายละเอียดของมือจะถูกเก็บไว้ในตัวแปร
    # print(multiLandMarks)


    if multiLandMarks:
        handsPoints = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #ที่รับค่า ข้อมูลที่รับมาจากวิดีโอเพื่อใช้วาดผลลัพธ์ลงไป และระบุ landmark เพื่อระบุจุดที่ต้องการวาดผลลัพธ์

            for idx, lm in enumerate(handLms.landmark):
                # print(idx,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                # print(cx,cy)
                handsPoints.append((cx,cy))
        for point in handsPoints:
            cv2.circle(img,point, 10, (0,0,255), cv2.FILLED)
            # print(point)
        upCountL = 0
        upCountR = 0
        for coordinate in fingerCoordinates:  #1 0 | 4 5
            if handsPoints[coordinate[0]][1] < handsPoints[coordinate[1]][1]:
                upCountR += 1

        if handsPoints[thumbCoordinate[0]][0] > handsPoints[thumbCoordinate[1]][0]:
            upCountL += 1
        #  ดับ ทั้ง หน้า หลัง
        if upCountR == 0 and upCountL == 0:
            TEXZT = "OFF 2 LIGHT"
            SENTDATA = "OFF 2 LIGHT"
        elif upCountR == 0 and upCountL == 1:
            TEXZT = "OFF 2 LIGHT"
            SENTDATA = "OFF 2 LIGHT"

        #  ติดบน ทั้ง หน้า หลัง
        elif upCountR == 1 and upCountL == 0:
            TEXZT = "ON UP LIGHT"
            SENTDATA = "ON UP LIGHT"
        elif upCountR == 1 and upCountL == 1:
            TEXZT = "ON UP LIGHT"
            SENTDATA = "ON UP LIGHT"

        #  ติดล่าง ทั้ง หน้า หลัง
        elif upCountR == 3 and upCountL == 0:
            TEXZT = "ON DOWN LIGHT"
            SENTDATA = "ON DOWN LIGHT"
        elif upCountR == 3 and upCountL == 1:
            TEXZT = "ON DOWN LIGHT"
            SENTDATA = "ON DOWN LIGHT"

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

        # TEXZT = "TEST"
        print(upCountR , upCountL)
        cv2.putText(img,TEXZT,(150,150), cv2.FONT_HERSHEY_PLAIN, 8,(255,255,0),12)
        # print(SENTDATA)


    cv2.imshow("HProject",img)
    cv2.waitKey(1)
