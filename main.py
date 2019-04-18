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
        return '<Blog {0}>'.format(self.title)  ##to see in python shell? not nec to run site

@app.route('/<blog_id>')  #blog_id in path? @app.route("/data/<section>") def data(section): assert section == request.view_args['section']
def one_post(blog_id):
    assert blog_id == int(request.form['title']  #'title' would be the one 'clicked' on
    title = Blog.query.get(blog_id)   #TODO what goes in ()
    entry = Blog.query.get(blog_id)   #TODO what goes in ()
    return render_template('single_blog.html', title=title, entry=entry)


@app.route('/new', methods=['POST','GET']) 
def newpost():
    return render_template('/newpost.html')
    #TODO route or redirect to /single_blog.html
    
@app.route('/blog', methods=['POST','GET']) 
def index():
    #this should add any new entries to the list of blogs...*should*
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_entry = request.form['new_entry']
        db.session.add(new_title, new_entry)
        db.session.commit()
        
    blogs = Blog.query.all()  # Blog.query.get(new_title) to get id of the new_title 
    return render_template("blog.html", blogs=blogs)


if __name__ == '__main__':
    app.run()