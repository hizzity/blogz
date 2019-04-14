from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    entry = db.Column(db.String(1000))

    def __init__(self, title, entry): ##?? 
        self.title = title
        self.entry = entry


@app.route('/newpost')
def blogpost():
    title = request.form['title']
    entry = request.form['entry']
    if title == '' or entry == '':
        redirect('/blog')
    else:
        new_title = Blog(title)
        new_entry = Blog(entry)
        db.sessions.add(new_title, new_task) ###how to enter info into table?
        db.session.commit()

       

    return render_template("newpost.html")

    

@app.route('/blog')
def index():
    blog_title = request.form['title']
    entry = request.form['entry']


    return render_template("blog.html")

if __name__ == '__main__':
    app.run()