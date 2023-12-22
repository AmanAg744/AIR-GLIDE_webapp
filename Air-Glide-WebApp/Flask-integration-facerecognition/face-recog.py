#Importing modules
import cv2
import numpy as np
import face_recognition
import os

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

#Web-Cam
cap=cv2.VideoCapture(0)

#Main Loop for running
while True:
    ret, frame=cap.read()
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

        else:
            #color= 'red'
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(imgS, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(imgS, (x1, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
            print("NAHI HAI")


    #Showing The original Image again.
    imgS = cv2.cvtColor(imgS, cv2.COLOR_RGB2BGR)
    cv2.imshow('Attendance',imgS)
    if cv2.waitKey(1) == ord('q'):
        break



#releasing all cameras
cap.release()
cv2.destroyAllWindows()