from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#create an instance of flask, __name__ is the application's module or package.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cs_project.db"
db = SQLAlchemy(app)
#link app and db to sqlite and sqlAlchemy

class Article(db.Model):
    #Article class definition creates space in the database for articles
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String(20),nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.id

class User(db.Model):
    #User class definition creates space in the database for user data
    uid = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(100), nullable=True)
    
    

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")
    #display the posts page


@app.route('/about')
def about():
    return render_template("about.html")
    #display the about page


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)
    #query the posts in chronological order, tell flask to display the posts page


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    #query for article, failure results in 404
    

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
        #delete the article, commit, send the user to the posts page
    except:
        return "An error occurred while handling the article deletion."
    #because of the way this is set up with no user authentication, I'm pretty sure anyone can delete articles just by navigating to '/posts/<int:id>/delete'

@app.route('/create-article', methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while handling the article creation."
    else:
        return render_template("create-article.html")
        #tell flask to display the create article page


@app.route('/posts/<int:id>/edit', methods=["POST", "GET"])
def edit_article(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while handling the article editing."
    else:
        return render_template("edit_article.html", article=article)
        #same thing as delete for editting too


if __name__ == "__main__":
    app.run()
