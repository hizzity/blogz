from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    entry = db.Column(db.String(1000))

    def __init__(self, title, entry): ##constructor 
        self.title = title
        self.entry = entry

    def __str__(self):
        return '<Blog {0}>'.format(self.name)  ##to see in python shell? not nec to run site

@app.route('/eachblog', methods=['POST'])
# when click on a blog, 
# get id number, use that to 
# display the title and entry



@app.route('/new', methods=['POST','GET']) 
def newpost():
    return render_template("newpost.html")
## after info entered: go to single_blog.html, with title and entry passed
# ...need new function within this route? or need to route?

# if request.method == 'GET':
#    redirect ('/newpost.html')




@app.route('/', methods=['POST','GET']) 
def index():
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_entry = request.form['new_entry']
        db.session.add(new_title, new_entry)
        db.session.commit()
    blogs = Blog.query.all()  # Blog.query.get(new_title) to get id of the new_title 
    return render_template("blog.html", blogs=blogs)


if __name__ == '__main__':
    app.run()