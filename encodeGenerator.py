import cv2
import face_recognition
import  pickle
import os


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

#ref = db.reference("employee")


folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds=[]

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    filename = os.path.join(folderPath,path)
    bucket = storage.bucket()
    blob= bucket.blob(filename)
    blob.upload_from_filename(filename)

    # print(path)
    # print(os.path.splitext(path)[0])
print(len(imgList))

def findEncoadings(imagesList):
    encodeList=[]
    for img in imagesList:
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("encoding started")
encodeListKnown= findEncoadings(imgList)
encodeListKnownwithIDs=[encodeListKnown,studentIds]
print(encodeListKnown)
print("encoding complete")

file=open("EncodeFile.p","wb")
pickle.dump(encodeListKnownwithIDs,file)
file.close()
print("filesaved")