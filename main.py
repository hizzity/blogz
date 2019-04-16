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
        return '<Blog {0}>'.format(self.name)  ##to see in python shell?


#@app.route('/newpost') 
#def newpost():
#    new_title = request.form['title']
#    new_entry = request.form['entry']
#    if len(title) == 0 or len(entry) == 0:
#         redirect('/blog')
#    else:
#        next_title = Blog(new_title)
#        next_entry = Blog(new_entry)
#        db.sessions.add(next_title, next_task) ###how to enter mulitiply cols of info into table?
#        db.session.commit()  
#
#    return render_template("blog.html")

#@app.route('/single_blog')
# when click on a blog, get id number, use that to display the title and entry
#def one_entry():
    #get title from the data table title = blog[i].title
    #get entry from the data table entry = blog[i].entry
    # return rendered_template("single_blog.html", title=title, entry=entry)

    

@app.route('/') 
def blog():
    
    blogs = Blog.query.all()  # Blog.query.get(new_title) to get id of the new_title 
    return render_template("blog.html", blogs=blogs) 

if __name__ == '__main__':
    app.run()