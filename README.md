# Blog CS Project

## Scope & Purpose
This is a project for our CS 11 course, we decided to develop a blog website with such features like posting, reading, editing, etc.

## Starting up MongoDB instance
To save the data for the articles that will be displayed on the website we decided to go with MongoDB. To connect to it, you must have access to the account we're using, specifically you need the uri of the db, we currently keep it locally in a file `.env`. This file is read by the `os.getenv`.