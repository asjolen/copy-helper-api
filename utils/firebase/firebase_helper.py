import pyrebase


class FirebaseHelper:
    config = {
        "apiKey": "AIzaSyANqsIP4A3O4oFNrvowWNVgEWGnrBRqoqY",
        "authDomain": "copybot-4b0d0.firebaseapp.com",
        "projectId": "copybot-4b0d0",
        "storageBucket": "copybot-4b0d0.appspot.com",
        "messagingSenderId": "834833953925",
        "appId": "1:834833953925:web:96fa1b6ad7ca77bab0a5ec",
        "databaseURL": "https://copybot-4b0d0-default-rtdb.europe-west1.firebasedatabase.app",
    }

    def set(self, path, value):
        firebase = pyrebase.initialize_app(self.config)
        firebase.database().child("/".join(path)).set(value)

    def update(self, path, value):
        firebase = pyrebase.initialize_app(self.config)
        firebase.database().child("/".join(path)).update(value)

    def push(self, path, value):
        firebase = pyrebase.initialize_app(self.config)
        firebase.database().child("/".join(path)).push(value)
