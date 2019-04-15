from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
#import jinja2

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

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


#@app.route('/newpost') 
#def newpost():
#    title = request.form['title']
#    entry = request.form['entry']
#    if len(title) == 0 or len(entry) == 0:
#         redirect('/blog')
#    else:
#        new_title = Blog(title)
#        new_entry = Blog(entry)
#        db.sessions.add(new_title, new_task) ###how to enter mulitiply cols of info into table?
#        db.session.commit()  

#    return render_template("blog.html")

#@app.route('/single_blog')
# when click on a blog, get id number, use that to display the title and entry
#def one_entry():
    #get title from the data table title = blog[i].title
    #get entry from the data table entry = blog[i].entry
    # return rendered_template("single_blog.html", title=title, entry=entry)

    

@app.route('/') # should it be '/blog'? no bc function invokes blog.html...I think?
def blog():
    #title = request.form['title']
    #entry = request.form['entry']
    #template = jinja_env.get_template('blog.html')
    #return template.render()   ## lines 43-46 from class 6 prep on jinja2
    
    blogs = Blog.query.all()
    return render_template("blog.html", title="Blog", blogs=blogs) #if not using jinja

if __name__ == '__main__':
    app.run()