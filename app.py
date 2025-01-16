from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)
<<<<<<< HEAD
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
=======

# MongoDB Configuration
with open('uri.txt', "r") as file:
    uri = file.read().strip()

client = MongoClient(uri, server_api=ServerApi('1'))
>>>>>>> 88f29f6 (moved app.py file from sqlite to mongoDB)

db = client["blog_cs"]
articles_collection = db["articles"]

<<<<<<< HEAD
class User(db.Model):
    #User class definition creates space in the database for user data
    uid = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(100), nullable=True)
    
    
=======
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
>>>>>>> 88f29f6 (moved app.py file from sqlite to mongoDB)

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
<<<<<<< HEAD
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
=======
    try:
        articles = list(articles_collection.find().sort("date", -1))
        return render_template("posts.html", articles=articles)
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return "An error occurred while fetching articles.", 500

@app.route('/posts/<string:id>')
def post_detail(id):
    try:
        if not ObjectId.is_valid(id):
            return "Invalid article ID", 404
            
        article = articles_collection.find_one({"_id": ObjectId(id)})
        if article:
            return render_template("post_detail.html", article=article)
        return "Article not found", 404
    except Exception as e:
        print(f"Error fetching post details: {e}")
        return "An error occurred while fetching the article.", 500

@app.route('/posts/<string:id>/delete', methods=['POST'])
def post_delete(id):
    try:
        if not ObjectId.is_valid(id):
            return "Invalid article ID", 404
            
        result = articles_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return redirect('/posts')
        return "Article not found", 404
    except Exception as e:
        print(f"Error deleting post: {e}")
        return "An error occurred while deleting the article.", 500
>>>>>>> 88f29f6 (moved app.py file from sqlite to mongoDB)

@app.route('/create-article', methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"].strip()
        intro = request.form["intro"].strip()
        text = request.form["text"].strip()
        
        # Basic validation
        if not title or not intro or not text:
            return "All fields must be filled out", 400
            
        article = {
            "title": title,
            "intro": intro,
            "text": text,
            "date": datetime.utcnow()
        }

        try:
            articles_collection.insert_one(article)
            return redirect('/posts')
        except Exception as e:
            print(f"Error creating article: {e}")
            return "An error occurred while creating the article.", 500
    else:
        return render_template("create-article.html")
        #tell flask to display the create article page

@app.route('/posts/<string:id>/edit', methods=["POST", "GET"])
def edit_article(id):
<<<<<<< HEAD
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
=======
    try:
        if not ObjectId.is_valid(id):
            return "Invalid article ID", 404
            
        article = articles_collection.find_one({"_id": ObjectId(id)})
        if not article:
            return "Article not found", 404
>>>>>>> 88f29f6 (moved app.py file from sqlite to mongoDB)

        if request.method == "POST":
            title = request.form["title"].strip()
            intro = request.form["intro"].strip()
            text = request.form["text"].strip()
            
            # Basic validation
            if not title or not intro or not text:
                return "All fields must be filled out", 400
                
            updated_article = {
                "title": title,
                "intro": intro,
                "text": text,
                "date": datetime.utcnow()
            }
            
            result = articles_collection.update_one(
                {"_id": ObjectId(id)}, 
                {"$set": updated_article}
            )
            
            if result.modified_count:
                return redirect('/posts')
            return "No changes made to the article.", 400
        else:
            return render_template("edit_article.html", article=article)
    except Exception as e:
        print(f"Error editing article: {e}")
        return "An error occurred while editing the article.", 500

if __name__ == "__main__":
    app.run()
