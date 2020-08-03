import pyrebase

config = {
  "apiKey": '<API KEY>',
  "authDomain": '<AUTHDOMAIN>',
  "databaseURL": '<DATABASE URL>',
  "storageBucket": '<STORAGE BUCKET>',
  "serviceAccount": '<FIREBASE CREDENTIALS>'
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

