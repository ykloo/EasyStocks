import pyrebase

config = {
  "apiKey": "AIzaSyAuas_66oL2Fsdy7uoOA4A-hK3w6EPnZ5Q",
  "authDomain": "telegram-bot-bbc09.firebaseapp.com",
  "databaseURL": "https://telegram-bot-bbc09.firebaseio.com",
  "storageBucket": "telegram-bot-bbc09.appspot.com",
  "serviceAccount": r'C:\Bot\telegram-bot-bbc09-firebase-adminsdk-u38dz-15b70d4665.json'
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()

def check_user(id):
    user = db.child(id).get()
    if user.val() == None:
        return False
    return True

def overwrite(id, shortlist):
    db.child(id).update({"stocks": shortlist})

def create_update(id, shortlist):
    data = {"stocks": shortlist}
    db.child(id).set(data)

def retrieve_stocks(id):
    stocks = db.child(id).child('stocks').get()
    return stocks.val()

# user = db.child("users").child(345).get()
# print(user.val())

