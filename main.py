from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8891/build-a-blog'
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

@app.route('/<blog_id>')  # ?id= blog_id in path? @app.route("/data/<section>") def data(section): assert section == request.view_args['section']
def one_post(blog_id):
    blog_id = request.form['blog_id']  #TODO maybe use sessions instead?
    title = session.query(Blog).get('blog_id')
    entry = session.query(Blog).get('blog_id')
    return render_template('single_blog', title=title, entry=entry)

#@app.route('/<blog_id>') the info I'm finding online

@app.route('/newpost', methods=['POST','GET']) 
def newpost():
    if request.method == 'GET':           #from today in class 4/18
        return render_template('/newpost.html')
    else:
        #passes info from new post to /single_blog and commits the new blog to the database
        title = request.form['new_title']
        entry = request.form['new_entry']
        db.session.add(Blog(title,entry))
        db.session.commit()
    return render_template('/single_blog.html', title=title, entry=entry)
 #TODO test this function
    
@app.route('/') 
def index():     
    blogs = Blog.query.all()  # Blog.query.get(new_title) to get id of the new_title 
    return render_template("/index.html", blogs=blogs)


if __name__ == '__main__':
    app.run()

    