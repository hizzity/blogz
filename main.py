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
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')   #correct

    def __init__(self, username, password):
        self.username = username
        self.password = password                    

@app.before_request
def require_login():
    allowed_routes = ['index','blog','login','validate','allposts'] #allowed functions not the decorator (decorator is @app.blah)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login') 

#def get_user():                                       for flick list getting email by user
#    return User.query.filter_by(email=session['user'])  #not complete, info from studio 4/25 
# render_template('edit.html', watchlist=get_current)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first() #TODO does this test that the user is in Blog database?
        if user and user.password == password:  
            session['username'] = username  #instructions tell me to put username in session
            return redirect('/newpost')     #logged in correctly and sent to /newpost  
        if not user:                        #if username not in database return error message
            error = "That username does not exist"  
            return render_template ('login.html', error=error)  
        else:
            password != user.password        #checks to make sure the correct password was entered
            session['username'] = username
            error = "Incorrect password"
            return render_template ('login.html', error=error)
    else:                                    #if GET request, direct to login page to fill out
        return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def validate():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        password_user_verified = request.form['password_user_verified']

        password_error = ''
        if (' ' in password) == True:
            password_error = "Your password cannot contain spaces or be left blank."     
        if len(password) < 3 or len(password) > 20:
            password_error = "Your password must be between 3 and 20 characters."

        password_same_error = ''
        if password != password_user_verified:
            password_same_error = "Passwords do not match."

        username_error = ''
        if (' ' in username) == True:                                             
            username_error = "Your username cannot contain spaces or be left blank."    
        if len(username) < 3 or len(username) > 20:
            username_error = "Your username must be between 3 and 20 characters."   
        #TODO check make sure username not already in data base, return error if so


        if username_error == '' and password_error == '' and password_same_error == '': 
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return render_template("newpost.html", username = username)    

        else:

            return render_template("blog.html", username = username,
            password_same_error = password_same_error, password_error = password_error,  
            username_error = username_error)

    if request.method == 'GET':
        return render_template('signup.html')    

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
#handles POST request to /logout and redirects user to /blog
#after deleting the username from the session

@app.route('/newpost', methods=['POST','GET']) 
def newpost():
    if request.method == 'GET':           #from class 4/18
        return render_template('newpost.html')
    else:
        title = request.form['new_title']
        entry = request.form['new_entry']
        if title == '' and entry == '':
            error = "Please enter a title."
            entry_error = "The blog entry can not be left blank"
            return render_template('newpost.html', error=error, entry_error=entry_error)
        elif title == '':
            error = "Please enter a title."
            return render_template('newpost.html', error=error)
        elif entry == '':
            entry_error = "The blog entry can not be left blank"
            return render_template('newpost.html', entry_error=entry_error)
        else:
            #passes info from new post to /single_blog and commits the new blog to the database
            owner = User.query.filter_by(username=session['username']).first()
            blog = Blog(title,entry,owner)
            db.session.add(blog)
            db.session.commit()
        return render_template('single_blog.html', blog=blog)
 
@app.route('/blog', methods=['POST','GET'])
def blog():
    owner = User.query.filter_by(username=session['username']).first()
    

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_entry = request.form['entry']
        new_blog = Blog(blog_title, blog_entry, owner)
        db.session.add(new_blog)
        db.session.commit()  

    blogs = Blog.query.filter_by(owner).all()

    return render_template('singleUser.html', blogs=blogs) 

# from build-a-blog, code for cycling through each blog
#@app.route('/single_blog')  # ?id= blog_id in path?
#def one_post():
#    user_id = request.args.get('id')      
#    blog = Blog.query.get(user_id) 
#    return render_template('single_blog.html', blog=blog)

@app.route('/singleUser') 
#TODO this is printing all blog posts, not blogs by this user
def all_blogs_one_user():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')    
    owner_id = request.args.get('owner')   
    
    return render_template('singleUser.html', blogs=blogs)

@app.route('/allposts')
def allposts():
    blogs = Blog.query.all()  
    blog_id = request.args.get('id')
    user_id = request.args.get('owner_id')
    if blog_id:
        blogs = Blog.query.filter_by(id=blog_id)
        return render_template('allposts.html', blogs=blogs)
    if user_id:
        blogs = Blog.query.filter_by(owner_id=user_id)
    return render_template('allposts.html', blogs=blogs)


@app.route('/') 
def index():
    users = User.query.all()
    user_id = request.args.get('id')

    if user_id:
        owner = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('singleUser.html', owner=owner, blogs=blogs)
    
    return render_template('blog.html', users=users)   
 


if __name__ == '__main__':
    app.run()

    