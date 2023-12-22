from flask import Flask,render_template,Response,redirect,url_for,request,session,flash
import cv2
import os
import numpy as np
import face_recognition
import time
import pyautogui
import HANDDETECTION as hdt
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
#import re
import win32api
import win32con
import speech_recognition as sr
from playsound import playsound

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ""
app.config["MYSQL_DB"]= 'air_glide_data'

mysql= MySQL(app)

# global id_db

cap=cv2.VideoCapture(0)
app.secret_key='dont tell'
 
def camera():
    success,frame=cap.read()
    return frame

def speech_recognition():
 
    r = sr.Recognizer()
 
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
 
        playsound("static/Say.mp3")
 
        audio = r.listen(source)
 
        print("Recognizing Now .... ")
 
 
        # recognize speech using google
 
        try:
            print("You have said \n" + r.recognize_google(audio))

            print("Audio Recorded Successfully \n ")
            return r.recognize_google(audio)
 
        except Exception as e:
            print("Error :  " + str(e))
            playsound("static\Say2.mp3")

  
def generate_frames():
    while True:
        frame=camera()
        frame = cv2.flip(frame,1)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def generate_frame_login():
    #Taking the images from the given path and passing in myList
    path='Images'
    images=[]
    ClassNames=[]
    myList=os.listdir(path)
    print(myList)

    # passing images in image list and spliting names and appending them in ClassName
    for cl in myList:
        frame=cv2.imread(f'{path}/{cl}')
        images.append(frame)
        ClassNames.append(os.path.splitext(cl)[0])
    print(ClassNames)

    #Function to append encodings of the images
    def findEncodings(images):
        encodeList=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown=findEncodings(images)
    while True:
        frame=camera()
        #imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #Finding Locations of frame and encoding each frame
        faceCurFrame= face_recognition.face_locations(imgS)
        encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

        #Matching the encodings and getting min distance to get best match
        for encodeFace,faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex=np.argmin(faceDis)


            #Matching with DataBase
            if matches[matchIndex]:
                name=ClassNames[matchIndex].upper()
                #color= 'green'
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(imgS, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(imgS, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgS, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
                print(name)
                global id_db
                id_db=str(name)
                pyautogui.hotkey('alt','l')
                return 
                    

            else:
                #color= 'red'
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(imgS, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(imgS, (x1, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
                print("NAHI HAI")
                pyautogui.hotkey('alt','w')
                return 
                


        #Showing The original Image again.
        imgS = cv2.cvtColor(imgS, cv2.COLOR_RGB2BGR)
        ret,buffer=cv2.imencode('.jpg',imgS)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames_virtual_mouse():
    pyautogui.FAILSAFE=False
    hweb = 480
    wweb = 640
    cap.set(3,wweb)
    cap.set(4,hweb)
    pTime = 0
    wscr , hscr = pyautogui.size()
    tym = 0
    pixels = 100
    smooth = 1.07
    plocx,plocy = 0,0
    clocx,clocy = 0,0
    tipIds = [4, 8, 12, 16, 20]
    detector = hdt.HandDetector()
    while True:
        frame=camera()
        frame = cv2.flip(frame,1)
        frame = detector.findHands(frame)
        lmlist = detector.findPosition(frame)

        #tip of all the fingers

        if lmlist :
            x0,y0 = lmlist[4][1:]
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]
            x3, y3 = lmlist[16][1:]
            x4, y4 = lmlist[20][1:]

            fingers = detector.fingersup()
            fing = detector.scroll_fingers()


            cv2.rectangle(frame,(pixels,pixels),(wweb - pixels, hweb - pixels),(255,255,0),2)


            #only index finger moving mode:
            if fingers == [0,1,1,0,0]:
                lenght, frame  = detector.distance(8,12,frame)
                lenght2,frame = detector.distance(5,9,frame)
                ratio = lenght/lenght2
                if ratio < 1.5:
                    xc = np.interp(x1,(pixels,wweb - pixels),(0,wscr))
                    yc = np.interp(y1, (pixels, hweb - pixels), (0, hscr))

                    clocx = plocx + (xc - plocx)/smooth
                    clocy = plocy + (yc - plocy)/smooth


                    pyautogui.moveTo(clocx,clocy)
                    cv2.circle(frame,(x1,y1),15,(140,140,0),cv2.FILLED)

                    plocx = clocx
                    plocy = clocy

            #for clicking: middle and index fing
            if fingers == [0,1,1,0,0]:
            
                lenght, frame  = detector.distance(8,12,frame)
                lenght2,frame = detector.distance(5,9,frame)
                ratio = lenght/lenght2    #ratio to keep the depth of the hand in mind
                #print(ratio)
                if ratio > 1.7:
                    tym+=1
                    if tym>25:
                        cv2.circle(frame,(x1,y1),15,(0,255,0),cv2.FILLED)
                        pyautogui.click()
                        tym = 0

            #fist scrolling using thumbs up and down
            if fing == [1] and fingers == [1,0,0,0,0]:
                if (lmlist[tipIds[1]][2] > lmlist[tipIds[0]][2]) or (lmlist[tipIds[2]][2] > lmlist[tipIds[0]][2]) or (lmlist[tipIds[3]][2] > lmlist[tipIds[0]][2]) or (lmlist[tipIds[4]][2] > lmlist[tipIds[0]][2]):
                    cv2.circle(frame, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.scroll(75)
                elif (lmlist[tipIds[1]][2] < lmlist[tipIds[0]][2]) or (lmlist[tipIds[2]][2] < lmlist[tipIds[0]][2]) or (lmlist[tipIds[3]][2] < lmlist[tipIds[0]][2]) or (lmlist[tipIds[4]][2] < lmlist[tipIds[0]][2]):
                    cv2.circle(frame, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.scroll(-75)
            
            #to enable voice recognition
            if fingers == [0,0,0,0,1]:
                tym+=1
                if tym>30:
                    cv2.circle(frame, (x4, y4), 15, (0, 255,0),cv2.FILLED)
                    text=speech_recognition()
                    if text:
                        pyautogui.typewrite(text)
                        pyautogui.hotkey('enter')
                    tym=0
            
            #pause/play
            if fingers == [1,1,1,1,1]:
                tym+=1
                if tym > 30:
                    cv2.circle(frame, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x3, y3), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x4, y4), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.hotkey("space")
                    tym = 0
            
            #Mute
            if fingers == [0,1,0,0,1]:
                tym+=1
                if tym>30:
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x4, y4), 15, (0, 255,0),cv2.FILLED)
                    pyautogui.hotkey("M")
                    tym=0
                    
            #click and hold     
            if fingers == [0,1,1,1,0]:
                cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x3, y3), 15, (0, 255, 0), cv2.FILLED)
                len1,frame = detector.distance(8,16,frame)
                len2,frame = detector.distance(5,13,frame)
                tym+=1
                ratio = len1/len2
                # print(ratio)
                if ratio<1.25 and tym>25:
                    cv2.circle(frame, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.mouseDown(button='left')
                    tym = 0
                elif ratio>1.8 and tym>25:
                    cv2.circle(frame, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
                    pyautogui.mouseUp()
                    tym=0
            
            
            #volume up down
            if  fingers == [1,1,0,0,0]:


                cv2.circle(frame,(x0,y0),15,(0,255,0),cv2.FILLED)
                cv2.circle(frame,(x1,y1),15,(0,255,0),cv2.FILLED)
                cv2.line(frame, (x0, y0), (x1, y1), (0, 255, 0), 3)


                len,frame = detector.distance(4,8,frame)
                len1, frame = detector.distance(2, 6, frame)
                tym+=1
                ratio = len/len1
                if ratio<1.05 and tym > 4:
                    cv2.line(frame, (x0, y0), (x1, y1), (0, 0, 255), 5)
                    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
                    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
                    tym = 0
                elif ratio>1.45 and tym >4:
                    cv2.line(frame, (x0, y0), (x1, y1), (0, 0,255), 5)
                    win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
                    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
                    tym = 0
                    
        #frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup_get', methods=['POST'])
def signup_get():
    cur= mysql.connection.cursor()
    if request.method=="POST":
        name=request.form["full_name"]
        email=request.form["email"]
        password=request.form["password"]
        confirm=request.form["confirm"]
        secure_password=sha256_crypt.encrypt(str(password))
        user=cur.execute( "SELECT email FROM users WHERE email LIKE %s", [email])
        user=cur.fetchone()
        if user==None:
            if password==confirm:
                cur.execute(""" INSERT INTO users(full_name,email,password) VALUES (%s, %s, %s)""", (name,email,secure_password))
                mysql.connection.commit()
                global id
                id=cur.execute( "SELECT id FROM users WHERE email LIKE %s", [email])
                id=cur.fetchone()
                id=id[0]
                return redirect(url_for('capture'))
            else:
                flash(" Password doesnot match confirm password!")
                return render_template("signup.html")
        else:
            flash("Email already exists, please login or contact admin!")
            return render_template("signup.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login_get', methods=["POST","GET"])
def login_get():
    cur= mysql.connection.cursor()
    if request.method == "POST":
        email=request.form["email"]
        password=request.form["password"]
        
        email=cur.execute( "SELECT email FROM users WHERE email LIKE %s", [email])
        email=cur.fetchone()
        passworddata=cur.execute( "SELECT password FROM users WHERE email LIKE %s", [email])
        passworddata=cur.fetchone()
        
        if email is None:
            flash("Email does not exist, please signup!")
            return render_template("login_message.html")
        else:
            for passwor_data in passworddata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"]=True
                    name=cur.execute( "SELECT full_name FROM users WHERE email LIKE %s", [email])
                    name=cur.fetchone()
                    name=name[0]
                    return render_template("main.html",name=name)
                else:
                    flash("Incorrect password!")
                    return render_template("login_message.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/login_message')
def login_message():
    return render_template("login_message.html")

@app.route('/main')
def main():
    cur= mysql.connection.cursor()
    cur.execute("SELECT full_name FROM users WHERE id LIKE %s", [id_db])
    full_name=cur.fetchone()
    full_name=full_name[0]
    return render_template("main.html",name=full_name)

@app.route('/video_signup')
def video_signup():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_login')
def video_login():
    return Response(generate_frame_login(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_virtual_mouse')
def video_virtual_mouse():
    return Response(generate_frames_virtual_mouse(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    while True:
        frame=camera()
        path='E:\Air-Glide(WebApp) not gitHub\Images'
        cv2.imwrite(os.path.join(path,f"{id}.png"), frame)
        break
    return redirect(url_for('login'))
    
    
    
if __name__=="__main__":
    app.run()