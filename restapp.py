from pyrebase import pyrebase
from flask import Flask,render_template,jsonify,request
app=Flask(__name__)

config = {
    "apiKey": "AIzaSyAsANFIT1V5_zmwYzRi4zJpBUXBPtEKz7Q",
    "authDomain": "test-36fdb.firebaseapp.com",
    "databaseURL": "https://test-36fdb.firebaseio.com",
    "projectId": "test-36fdb",
    "storageBucket": "test-36fdb.appspot.com",
    "messagingSenderId": "927510521637",
    "appId": "1:927510521637:web:9bcecef3e4297679f85ccc",
    "measurementId": "G-00SGGQ0ZE4"
  }

firebase = pyrebase.initialize_app(config)
db=firebase.database()

content={}

@app.route('/',methods=['GET'])
def get():
    user=db.child("todo").get().val()
    for i,j in user.items():
        content[i]=j
    return jsonify({'user':content}),201



@app.route('/post',methods=['POST'])
def post():
    somejson=request.get_json()
    return jsonify({'res':somejson})


if __name__=='__main__':
    app.run(debug=True)


 