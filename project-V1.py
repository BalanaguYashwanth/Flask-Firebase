import os
from flask import Flask, request, jsonify, send_file
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
import pytesseract

import sys
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)                   # default: roughly a floppy

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
    f = request.files['img']
    try:
        todir='/media/byashwanth/others/lets-flask/lprojects'
        filename=secure_filename(f.filename)
        
        arr=(filename.split("."))
        arr_length=len(arr)-1
        extension = arr[arr_length]
        
        filename1=filename.split(".")[0]
        f.save(filename)

       ############add-on##############
        partnum = 0
        input = open(filename, 'rb')                   # use binary mode on Windows
        folder = os.path.join(todir, filename1)
        os.makedirs(folder)
        while 1:                                       # eof=empty string from read
            chunk = input.read(chunksize)              # get next part <= chunksize
            if not chunk: 
                break
            partnum  = partnum+1
            filename = os.path.join(folder, ('part%04d' % partnum))
            fileobj  = open(filename, 'wb')
            fileobj.write(chunk)
            #print(fileobj)
            fileobj.close()                            # or simply open(  ).write(  )
            filenamex=filename1+"-"+extension+"_"+str(partnum)
            storage.child(filenamex).put(filename)

        input.close(  )
        assert partnum <= 9999                         # join sort fails if 5 digits
        ##############add-on#######################
        
        #filenamex=filename1+"_"+str(partnum)
        #storage.child(filename1+"/"+filenamex).put(filename)
        #url=storage.child(filename1).get_url(filename1)
        return jsonify({'name':filename1+"-"+extension}),200
    except:
        return jsonify({'message':'error in uploading image'}),400


@app.route('/getfolder',methods=['POST'])
def getfolder():
    path='/media/byashwanth/others/lets-flask/lprojects'
    readsize = 1024
    f=request.json['name']
    ext=f.split('-')[1]
    file_dir=os.path.join(path,f+'new'+"."+ext) 
    output=open(file_dir,'wb')
    folders=storage.child().list_files()
    for i in folders:
        if i.name.split("_")[0] == f:
            #second=(i.name.split('-')[1])
            #third_split=second.split('_')[0]
            print(storage.child(i.name).download(i.name))
            filepath = os.path.join(path, i.name)
            fileobj=open(filepath,'rb')
            while 1:
                filebytes=fileobj.read(readsize)
                if not filebytes:
                    break
                output.write(filebytes)
            fileobj.close()
    output.close()
    return send_file(os.path.join(path,f+'new'+"."+ext)),200

if __name__=="__main__":
    app.run(debug=True)


