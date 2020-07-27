import pyrebase

config = {
  "apiKey": "AIzaSyAuas_66oL2Fsdy7uoOA4A-hK3w6EPnZ5Q",
  "authDomain": "telegram-bot-bbc09.firebaseapp.com",
  "databaseURL": "https://telegram-bot-bbc09.firebaseio.com",
  "storageBucket": "telegram-bot-bbc09.appspot.com",
  "serviceAccount": "./credentials.json"
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()

def check_user(id):
    user = db.child(id).get()
    if user.val() == None:
        return False
    return True

def update(id, shortlist):
    db.child(id).update({"stocks": shortlist})

def create_update(id, shortlist):
    data = {"stocks": shortlist}
    db.child(id).set(data)



# more = {"stocks": "FB GOOGL TSLA"}
# db.child("users").child(551145).set(more)
# db.child("users").child("YK").update({"id": 1234})


# user = db.child("users").child(12345).child('stocks').get()
# print(user.val())

user = db.child("users").child(345).get()
print(user.val())

