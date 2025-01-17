from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

# MongoDB Configuration
with open('uri.txt', "r") as file:
    uri = file.read().strip()

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["blog_cs"]
articles_collection = db["articles"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/create_account', methods = ["CREATE"])
def create():
    if request.method=="CREATE":
        return render_template('create_account.html',)
    
@app.route('/posts')
def posts():
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

@app.route('/posts/<string:id>/edit', methods=["POST", "GET"])
def edit_article(id):
    try:
        if not ObjectId.is_valid(id):
            return "Invalid article ID", 404
            
        article = articles_collection.find_one({"_id": ObjectId(id)})
        if not article:
            return "Article not found", 404

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
    app.run(host='0.0.0.0', port=5000)