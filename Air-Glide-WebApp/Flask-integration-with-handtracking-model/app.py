from flask import Flask,render_template,Response
import cv2
from HANDDETECTION import HandDetector
import time

app=Flask(__name__)
# camera=cv2.VideoCapture(0)

def generate_frames():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, 1463)
    cap.set(4, 823)
    detector = HandDetector()
    while True:
            
        ## read the camera frame
        success,frame=cap.read()
        frame = cv2.flip(frame,1)
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)

        if len(lmList) != 0:
            print(lmList[8])
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
