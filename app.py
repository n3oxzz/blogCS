from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from datetime import datetime, timezone
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
import certifi
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from bson import ObjectId
from supabase import create_client





load_dotenv()

sup_url = os.getenv("SUPABASE_URL")
sup_key = os.getenv("SUPABASE_KEY")
supabase = create_client(sup_url, sup_key)

app = Flask(__name__)


bcrypt = Bcrypt(app)

app.secret_key = os.getenv("SECRET_KEY")

uri = os.getenv('MONGO_DB_URI')

app.config["UPLOAD_FOLDER"] = "static/uploads"

client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client["blogDB"]
articles_collection = db["Articles"]
users_collection = db["Users"]


try:
    print("attempting to ping...")
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if(users_collection.find_one({"username": username})):
            return "Username already exists", 400
    
        if not username or not password:
            return "Username and password are required", 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            users_collection.insert_one({"username": username, "password": hashed_password})
            return redirect('/login')
        except Exception as e:
            print(f"Error registering user: {e}")
            return "An error occurred during registration.", 500
    else:
        return render_template('register.html')
    

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = users_collection.find_one({"username": username})

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            return redirect('/')
        return "Invalid username or password", 401
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")
#@app.route('/create_account', methods = ["CREATE"])
#def create():
#   if request.method=="CREATE":
 #       return render_template('create_account.html',)
    

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
            return render_template("post_detail.html", article=article, session=session)
        return "Article not found", 404
    except Exception as e:
        print(f"Error fetching post details: {e}")
        return "An error occurred while fetching the article.", 500


@app.route('/posts/<string:id>/delete', methods=['POST'])
def post_delete(id):
    if "user_id" not in session:
        return redirect('/login')
    try:
        article = articles_collection.find_one({"_id": ObjectId(id)})

        if not article:
            return "Article not found", 404
        if article["author_id"] != session["user_id"]:
            return "You have no permission to edit this post.", 403
            
        result = articles_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count:
            return redirect('/posts')
        return "Article not found", 404
    except Exception as e:
        print(f"Error deleting post: {e}")
        return "An error occurred while deleting the article.", 500


@app.route('/create-article', methods=["POST", "GET"])
def create_article():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        title = request.form["title"].strip()
        intro = request.form["intro"].strip()
        text = request.form["text"]
        if "photo" in request.files:
            file = request.files["photo"]
            if file.filename != "":
                file_name = f"{datetime.now().timestamp()}_{file.filename}"
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
                file.save(file_path)
                photo_url = f"/{file_path}"
            else:
                photo_url = None
        else:
            photo_url = None

            
        author_username = session.get("username")
        
        article = {
            "title": title,
            "intro": intro,
            "text": text,
            "photo": photo_url,
            "date": datetime.now(timezone.utc),
            "author_id": session["user_id"],
            "author_username": author_username
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
    if "user_id" not in session:
        return redirect('/login')
    
    try:    
        article = articles_collection.find_one({"_id": ObjectId(id)})

        if not article:
            return "Article not found", 404
        
        # Проверка, что автор статьи совпадает с текущим пользователем
        if article["author_id"] != session["user_id"]:
            return "You have no permission to edit this post.", 403

        if request.method == "POST":
            title = request.form["title"].strip()
            intro = request.form["intro"].strip()
            text = request.form["text"]
            photo_url = None 
            if "photo" in request.files:
                file = request.files["photo"]
                if file.filename != "":
                    file_name = f"{datetime.now().timestamp()}_{file.filename}"
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
                    file.save(file_path)
                    photo_url = f"/{file_path}"
            else:
                photo_url = None
            
            # Basic validation
            if not title or not intro or not text:
                return "All fields must be filled out", 400
                
            updated_article = {
                "title": title,
                "intro": intro,
                "text": text,
                "photo": photo_url if photo_url else article.get("photo"),
                "date": datetime.now(timezone.utc)
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
        return f"An error occurred while editing the article: {e}", 500
    
@app.route('/account')
def account():
    if "user_id" not in session:
        return redirect('/login')
    user = users_collection.find_one({"_id": ObjectId(session["user_id"])})
    return render_template("account.html", user=user)

if __name__ == "__main__":
    app.run()