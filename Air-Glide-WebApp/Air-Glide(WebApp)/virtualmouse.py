import cv2
import numpy as np
import HANDDETECTION as hdt
import time
import pyautogui
import win32api
import win32con
import speech_recognition as sr
import os
from playsound import playsound
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL


    
pyautogui.FAILSAFE = False
hweb = 480
wweb = 640
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cap.set(3,wweb)
cap.set(4,hweb)
pTime = 0
wscr , hscr = pyautogui.size()
tym = 0
pixels = 100
smooth = 1.03
plocx,plocy = 0,0
clocx,clocy = 0,0
tipIds = [4, 8, 12, 16, 20]

recognizer = sr.Recognizer()

# Function to convert speech to text
def speech_recognition():
 
    r = sr.Recognizer()
 
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
 
        playsound(r"static\\Say.mp3")
 
        audio = r.listen(source)
 
        print("Recognizing Now .... ")
 
 
        # recognize speech using google
 
        try:
            print("You have said \n" + r.recognize_google(audio))

            print("Audio Recorded Successfully \n ")
 
 
        except Exception as e:
            print("Error :  " + str(e))
    return r.recognize_google(audio)

#pycaw library initialization for gesture volume control
'''devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#get volume range
volMin, volMax = volume.GetVolumeRange()[:2]'''


#hand detector
detector = hdt.HandDetector()


while True:
    ret,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    #tip of all the fingers

    if lmlist :
        x0,y0 = lmlist[4][1:]
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        x3, y3 = lmlist[16][1:]
        x4, y4 = lmlist[20][1:]

        fingers = detector.fingersup()
        fing = detector.scroll_fingers()


        cv2.rectangle(img,(pixels,pixels),(wweb - pixels, hweb - pixels),(255,255,0),2)


        #only index finger moving mode:
        if fingers == [0,1,1,0,0]:
            lenght, img  = detector.distance(8,12,img)
            lenght2,img = detector.distance(5,9,img)
            ratio = lenght/lenght2
            if ratio < 1.5:
                xc = np.interp(x1,(pixels,wweb - pixels),(0,wscr))
                yc = np.interp(y1, (pixels, hweb - pixels), (0, hscr))

                clocx = plocx + (xc - plocx)/smooth
                clocy = plocy + (yc - plocy)/smooth


                pyautogui.moveTo(clocx,clocy)
                cv2.circle(img,(x1,y1),15,(140,140,0),cv2.FILLED)

                plocx = clocx
                plocy = clocy

        #for clicking: middle and index fing
        if fingers == [0,1,1,0,0]:
        
            lenght, img  = detector.distance(8,12,img)
            lenght2,img = detector.distance(5,9,img)
            ratio = lenght/lenght2    #ratio to keep the depth of the hand in mind
            #print(ratio)
            if ratio > 1.7:
                tym+=1
                if tym>25:
                    cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
                    pyautogui.click()
                    tym = 0

        #to enable voice recognition
        if fingers == [0,0,0,0,1]:
            tym+=1
            if tym>30:
                cv2.circle(img, (x4, y4), 15, (0, 255,0),cv2.FILLED)
                text=speech_recognition()
                pyautogui.typewrite(text)
                tym=0

        #pause/play
        if fingers == [1,1,1,1,1]:
            tym+=1
            if tym > 25:
                cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x4, y4), 15, (0, 255,0),cv2.FILLED)
                pyautogui.hotkey("space")
                tym = 0


        #fist scrolling using thumbs up and down
        if fing == [1] and fingers == [1,0,0,0,0]:

            if (lmlist[tipIds[1]][2] > lmlist[tipIds[0]][2]) or (lmlist[tipIds[2]][2] > lmlist[tipIds[0]][2]) or (lmlist[tipIds[3]][2] > lmlist[tipIds[0]][2]) or (lmlist[tipIds[4]][2] > lmlist[tipIds[0]][2]):
                cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.scroll(75)
            elif (lmlist[tipIds[1]][2] < lmlist[tipIds[0]][2]) or (lmlist[tipIds[2]][2] < lmlist[tipIds[0]][2]) or (lmlist[tipIds[3]][2] < lmlist[tipIds[0]][2]) or (lmlist[tipIds[4]][2] < lmlist[tipIds[0]][2]):
                cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.scroll(-75)

        #Mute
        if fingers == [0,1,0,0,1]:
            tym+=1
            if tym>30:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x4, y4), 15, (0, 255,0),cv2.FILLED)
                pyautogui.hotkey("M")
                tym=0
        
        #click and hold     
        if fingers == [0,1,1,1,0]:
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 255, 0), cv2.FILLED)
            len1,img = detector.distance(8,16,img)
            len2,img = detector.distance(5,13,img)
            tym+=1
            ratio = len1/len2
            # print(ratio)
            if ratio<1.25 and tym>25:
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.mouseDown(button='left')
                tym = 0
            elif ratio>1.8 and tym>25:
                cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
                pyautogui.mouseUp()
                tym=0
        
        #volume up down
        if  fingers == [1,1,0,0,0]:
            

            cv2.circle(img,(x0,y0),15,(0,255,0),cv2.FILLED)
            cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
            cv2.line(img, (x0, y0), (x1, y1), (0, 255, 0), 3)


            len,img = detector.distance(4,8,img)
            len1, img = detector.distance(2, 6, img)
            tym+=1
            ratio = len/len1
            if ratio<1.05 and tym > 4:
                cv2.line(img, (x0, y0), (x1, y1), (0, 0, 255), 5)
                win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
                win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
                tym = 0
            elif ratio>1.45 and tym >4:
                cv2.line(img, (x0, y0), (x1, y1), (0, 0,255), 5)
                win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
                win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
                tym = 0





    #frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

    cv2.imshow("IMAGE", img)
    if cv2.waitKey(1) == ord("q"):
        break






