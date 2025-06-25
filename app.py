from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from flask import render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

app.secret_key = os.getenv("SECRETKEY")

mongo = PyMongo(app)

@app.route("/")
def home():
    return redirect(url_for("todos"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        print(username, password)

        existing_user = mongo.db.users.find_one({"username": username})
        
        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        mongo.db.users.insert_one({"username": username, "password": password})
        return redirect(url_for("login"))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = mongo.db.users.find_one({"username": username})

        if user and user["password"] == password:
            session["username"] = username
            return redirect(url_for("todos"))
        else:
            flash("Invalid username or password!")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/todos", methods=["GET", "POST"])
def todos():
    if "username" not in session:
        return redirect(url_for("login"))
    user = mongo.db.users.find_one({"username": session["username"]})

    if request.method == "POST":
        todo = request.form["todo"]
        if todo.strip() != "":
            mongo.db.todos.insert_one({"user_id": user["_id"], "task": todo})

    user_todos = list(mongo.db.todos.find({"user_id": user["_id"]}))
    return render_template("todos.html", todos=user_todos, username=user["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/delete/<id>")
def delete(id):
    if "username" not in session:
        return redirect(url_for("login"))

    user = mongo.db.users.find_one({"username": session["username"]})
    mongo.db.todos.delete_one({"_id": ObjectId(id), "user_id": user["_id"]})
    return redirect(url_for("todos"))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)