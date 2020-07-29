from pyrebase import pyrebase
from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
import json

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

@app.route('/')
def about():
    return render_template('about.html',title='About')

@app.route('/userinput')
def userinput():
    return render_template('userinput.html')


@app.route('/userpost',methods=['GET','POST'])
def userpost():
    if request.method=="POST":
        user=request.form['user']
        age=request.form['age']
        email=request.form['email']

        post={
            "user":user,
            "age":age,
            "email":email,
        }

        db.child('todo').push(post)
        userdetails=db.child('todo').get().val()
        return render_template('userpost.html',userdetails=userdetails)
    else:
        userdetails=db.child('todo').get().val()
        return render_template('userpost.html',userdetails=userdetails)


@app.route('/delete/<id>',methods=["GET","POST"])
def delete(id):
    db.child("todo").child(id).remove()
    return redirect('/userpost')
    
@app.route('/update/<id>',methods=['GET','POST'])
def update(id):
    return render_template('update.html',id=id)

@app.route('/update/<id>',methods=['GET','POST'])
def updated(id):
    if request.method=='POST':
        id=request.form['id']
        user=request.form['user']
        age=request.form['age']

        updated={
            "user":user,
            "id":id,
            "age":age
        }

        db.child('todo').child(id).update(updated)
        return render_template('update.html',id=id)
   

if __name__ == '__main__':
    app.run(debug=True)





