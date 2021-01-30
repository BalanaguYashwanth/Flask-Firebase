import os
from flask import Flask, request, jsonify
import json,pyrebase
from flask_cors import CORS
import firebase_admin
#from firebase_admin import auth
from werkzeug.security import generate_password_hash
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
from PIL import Image
from werkzeug.utils import secure_filename
from firebase import Firebase
import requests

app = Flask(__name__)
CORS(app)
cred=credentials.Certificate('key.json')
default_app=firebase_admin.initialize_app(cred)

db = firestore.client()
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))

firebase = Firebase(json.load(open('fbconfig.json')))
storage = firebase.storage()

@app.route("/")
def home():
    return '<h1> hello </h1>'

@app.route("/post/<object>",methods=['POST'])
def post(object):
    try:
        db.collection(object).add(request.json) #By url we will get collection name & By post request we will get data
        return jsonify({"success":True}),200    
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/imagecompressor',methods=['POST'])
def photo():
    img = Image.open(request.files['img'])
    try:  
        filename=secure_filename(request.files['img'].filename)
        #img.save(filename,optimize=True,quality=70)
        

        storage.child("images/"+filename).put(filename)
        url=storage.child("images/"+filename).get_url(filename)
        return jsonify({'message':url}),200
    except:
        return jsonify({'message':'error in uploading image'}),400


if __name__=="__main__":
    app.run(debug=True)

