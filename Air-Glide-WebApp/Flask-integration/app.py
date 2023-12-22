from flask import Flask,render_template,Response
import cv2
import time
import numpy as np
import HANDDETECTION as hdt
import time
import pyautogui

app=Flask(__name__)
# camera=cv2.VideoCapture(0)

def generate_frames():
    pyautogui.FAILSAFE=False
    hweb = 480
    wweb = 640
    cap = cv2.VideoCapture(0)
    cap.set(3,wweb)
    cap.set(4,hweb)
    pTime = 0
    wscr , hscr = pyautogui.size()
    tym = 0
    pixels = 100


    detector = hdt.HandDetector()
    while True:
        ## read the camera frame
        success,img=cap.read()
        img = cv2.flip(img,1)
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)

        #tip of all the fingers

        if len(lmlist) != 0:
            x0,y0 = lmlist[4][1:]
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]
            x3, y3 = lmlist[16][1:]
            x4, y4 = lmlist[20][1:]

            fingers = detector.fingersup()


            cv2.rectangle(img,(pixels,pixels),(wweb - pixels, hweb - pixels),(255,255,0),2)


            #only index finger moving mode:
            if fingers == [0,1,0,0,0]:
                xc = np.interp(x1,(pixels,wweb - pixels),(0,wscr))
                yc = np.interp(y1, (pixels, hweb - pixels), (0, hscr))

                pyautogui.moveTo(xc,yc)
                cv2.circle(img,(x1,y1),15,(140,140,0),cv2.FILLED)

            #for clicking: middle and index fing
            if fingers == [0,1,1,0,0]:

                lenght, img  = detector.distance(8,12,img)

                if lenght <40:
                    tym+=1
                    if tym>30:
                        cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
                        pyautogui.click()
                        tym = 0

            #thumb up for win r
            if fingers == [1,0,0,0,0]:
                tym+=1
                if tym > 40:
                    cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.hotkey("win","r")
                    tym = 0


            #for closing opencv
            if fingers == [0,0,0,0,1]:
                tym+=1
                if tym > 40:
                    cv2.circle(img, (x4, y4), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.hotkey("q")
                    tym = 0

        #frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        ret,buffer=cv2.imencode('.jpg',img)
        img=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
