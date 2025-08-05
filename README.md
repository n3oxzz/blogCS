# Blog CS Project

## Overview
This is our final project for CS 11 - a fully functional **blog platform** where users can:
- Register & log in securely
- Create, edit, and delete posts
- Upload images to articles
- View posts in a clean, readable format

Everything is built using **Flask + MongoDB** - keeping it lightweight but powerful.

---

## Tech Stack
- **Backend:** Python + Flask
- **Database:** MongoDB Atlas (with `pymongo`)
- **Templating:** Jinja2
- **Security:** Password hashing via Flask-Bcrypt, sessions for auth
- **Frontend:** HTML, CSS

---

## MongoDB Setup (Local Dev)
We use **MongoDB Atlas** to store all user and article data.

To connect:
1. Ask a team member for access to the `.env` file (not included in the repo).
2. Make sure it contains the `MONGO_DB_URI` key.
    Example:
    ```env
    MONGO_DB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/blogDB
    SECRET_KEY=your_secret_key
    ```
3. Flask automatically loads it using `dotenv`.

---

## Running Locally
```bash
git clone https://github.com/your/repo.git
cd repo
pip install -r requirements.txt
flask run 
```

---

## Why This Project
We wanted to build something meaningful for our school community - a space where people can say what they think, share what they feel, and express themselves freely.

We combined **VISST** and **space** - and that's how **VISSPACE** was born.


