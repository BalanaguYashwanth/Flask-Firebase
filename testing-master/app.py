from flask import Flask,render_template,request
app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/userinput')
def userinput():
    return render_template('userinput.html')

@app.route('/userpost',methods=['POST','GET'])
def userpost():
    if request.method=='POST':
        user=request.form['user']        
        return render_template('userpost.html',user=user)


if __name__ == '__main__':
    app.run(debug=True)





