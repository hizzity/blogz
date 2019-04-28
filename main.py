from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    entry = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, entry, owner): ##constructor 
        self.title = title
        self.entry = entry
        self.owner = owner                    #correct, it is owner, not owner_id 

    def __str__(self):
        return '<Blog {0}>'.format(self.title)  ##to see in python shell? not nec to run site

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')   #correct

    def __init__(self, username, password):
        self.username = username
        self.password = password                    

#def get_user():                                       for flick list getting email by user
#    return User.query.filter_by(email=session['user'])  #not complete, info from studio 4/25 
# render_template('edit.html', watchlist=get_current)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')        #TODO test for correct username incorrect password 
        else:                                  #TODO 
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

#@app.route('/signup')
#def signup():
    #TODO use code from user signup for validation

#@app.route('/logout')
#def logout():
#handles POST request to /logout and redirects user to /index (/blog in instructions)
#after deleting the username from the session


@app.route('/single_blog')  # ?id= blog_id in path?
def one_post():
    blog_id = request.args.get('id')      
    blog = Blog.query.get(blog_id) 
    return render_template('single_blog.html', blog=blog)


@app.route('/newpost', methods=['POST','GET']) 
def newpost():
    if request.method == 'GET':           #from class 4/18
        return render_template('/newpost.html')
    else:
        title = request.form['new_title']
        entry = request.form['new_entry']
        if title == '' and entry == '':
            error = "Please enter a title."
            entry_error = "The blog entry can not be left blank"
            return render_template('/newpost.html', error=error, entry_error=entry_error)
        elif title == '':
            error = "Please enter a title."
            return render_template('/newpost.html', error=error)
        elif entry == '':
            entry_error = "The blog entry can not be left blank"
            return render_template('/newpost.html', entry_error=entry_error)
        else:
            #passes info from new post to /single_blog and commits the new blog to the database
            blog = Blog(title,entry)
            db.session.add(blog)
            db.session.commit()
        return render_template('/single_blog.html', blog=blog)
 
    
@app.route('/') 
def index():     
    blogs = Blog.query.all()  # Blog.query.get(new_title) to get id of the new_title 
    return render_template("/index.html", blogs=blogs)


if __name__ == '__main__':
    app.run()

    