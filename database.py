
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://mv-attendence-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")

data={

    "40024141":{
        "name":"Suraj Patel",
        "Position":"Engineer",
        "BU": "ICP",
        "ticket":1,
        "startyear": 2017,
        "standing": "good",
        "year" : 4,
        "last_attendence_time": "2022-12-11 00:54:34"

    },

    "40027214": {
        "name": "Nimesh Pagi",
        "Position":"Engineer",
        "BU": "ICP",
        "ticket":1,
        "startyear": 2016,
        "standing": "very good",
        "year": 4,
        "last_attendence_time": "2022-12-10 00:54:34"

    },
    "40001821":{
        "name":"Jaisheel Chattrawala",
        "Position":"Senior Engineer",
        "BU": "ICP",
        "ticket":1,
        "startyear": 2012,
        "standing": "good",
        "year" : 2,
        "last_attendence_time": "2018-16-11 00:54:34"

    },
    "40031014": {
        "name": "Animeshkumar Nayak",
        "Position":"Senior Engineer",
        "BU": "ICP",
        "ticket":1,
        "startyear": 2022,
        "standing": "excelent",
        "year": 0.2,
        "last_attendence_time": "2022-12-25 00:54:34"

    }
}

for key, value in data.items():
    ref.child(key).set(value)