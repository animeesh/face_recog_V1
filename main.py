import cv2
import os
import face_recognition
import pickle
import numpy as np
import cvzone
from datetime import datetime

#database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://mv-attendence-default-rtdb.firebaseio.com/",
    "storageBucket" : "mv-attendence.appspot.com"
})
bucket = storage.bucket()

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
imgbackground=cv2.imread("Resources/background_mod.png")
folderModePath = 'Resources/Modes/mode'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

#Load the encoading file

print("Loading encoading file......")
file =open("EncodeFile.p","rb")
encodeListKnownwithIDs= pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListKnownwithIDs
print(encodeListKnownwithIDs)
print(studentIds)

modeType=0
counter=0
id=-1
imgStudent=[]

while True:
    success,img = cap.read()
    imgS =cv2.resize(img,(0,0),None,0.25,0.25)
    imgS= cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame= face_recognition.face_locations(imgS)
    encoedeCurFrame= face_recognition.face_encodings(imgS,faceCurFrame)

    imgbackground[162:162+480,55:55+640]=img
    imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace,FaceLoc in zip(encoedeCurFrame,faceCurFrame):
        matches =face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print("matches",matches)
        #print("face distance ",faceDis)
        matchIndex= np.argmin(faceDis)

        #print("match Index",matchIndex)

        if matches[matchIndex]:
            y1,x2,y2,x1 = FaceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            bbox = 55+x1,162+y1,x2-x1,y2-y1
            imgbackground= cvzone.cornerRect(imgbackground,bbox,rt=0)

            id = studentIds[matchIndex]
            #print(id)
            if counter==0:
                # cvzone.putTextRect(imgbackground, "Loading", (275, 400))
                # cv2.imshow("Face Attendance", imgbackground)
                # cv2.waitKey(1)
                counter=1
                modeType=1
    if counter!=0:
        if counter==1:
            #with no internet it wont work around try putting try catch
            studentInfo=db.reference(f'Students/{id}').get()
            print("studentInfo:",studentInfo)
            #get the image from the storage

            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            datetimeObject = datetime.strptime(studentInfo["last_attendence_time"], "%Y-%d-%m %H:%M:%S")
            secondElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondElapsed)

            if secondElapsed>30:
                ref = db.reference(f'Students/{id}')
                studentInfo["ticket"]+=1
                ref.child("ticket").set(studentInfo["ticket"])
                ref.child(studentInfo["last_attendence_time"]).set(datetime.now().strftime("%Y-%d-%m %H:%M:%S"))
            else:
                modeType = 0
                counter = 0
                studentInfo = []
                imgStudent = []
                imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


        if modeType!=3:
            if 10<counter<18:
                modeType=2
                imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


            if counter<=10:
                cv2.putText(imgbackground,str(studentInfo["ticket"]),(871,125),cv2.FONT_HERSHEY_COMPLEX,1,
                             (0,0,0),2)
                cv2.putText(imgbackground, str(studentInfo["BU"]), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0, 0, 0), 2)
                cv2.putText(imgbackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0, 0, 0), 2)
                cv2.putText(imgbackground, str(studentInfo["standing"]), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                            (0, 0, 0), 1)
                cv2.putText(imgbackground, str(studentInfo["ticket"]), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                            (0, 0, 0), 1)
                cv2.putText(imgbackground, str(studentInfo["startyear"]), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                            (0, 0, 0), 1)

                (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2
                cv2.putText(imgbackground, str(studentInfo["name"]), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 0), 2)
                imgbackground[175:175+216,909:909+216]= imgStudent

            counter+=1

            if counter>=19:
                modeType=0
                counter=0
                studentInfo=[]
                imgStudent=[]
                imgbackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            #print("known face was detected.. ! ",studentIds[matchIndex])
    #cv2.imshow("L&T technology services",img)
    cv2.imshow("L&T technology services",imgbackground)
    cv2.waitKey(1)