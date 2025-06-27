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
        # Create default list for new user
        mongo.db.lists.insert_one({"username": username, "list_name": "Your list"})
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

@app.route("/todos", methods=["GET"])
def todos():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    lists = list(mongo.db.lists.find({"username": username}))
    selected_list = request.args.get("list")
    if not selected_list and lists:
        selected_list = lists[0]["list_name"]
    todos = mongo.db.todos.find({"username": username, "list_name": selected_list}) if selected_list else []
    return render_template("todos.html", todos=todos, username=username, lists=lists, selected_list=selected_list)

@app.route("/add", methods=["POST"])
def add_task():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    task = request.form["task"]
    list_name = request.form["list_name"]
    mongo.db.todos.insert_one({
        "username": username,
        "task": task,
        "completed": False,
        "list_name": list_name
    })
    return redirect(url_for("todos", list=list_name))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/delete/<id>")
def delete(id):
    if "username" not in session:
        return redirect(url_for("login"))

    mongo.db.todos.delete_one({"_id": ObjectId(id), "username": session["username"]})
    return redirect(url_for("todos"))

@app.route("/toggle/<id>", methods=["POST"])
def toggle_complete(id):
    if "username" not in session:
        return redirect(url_for("login"))

    completed = "completed" in request.form
    mongo.db.todos.update_one(
        {"_id": ObjectId(id), "username": session["username"]},
        {"$set": {"completed": completed}}
    )
    list_name = request.form.get("list")
    if list_name:
        return redirect(url_for("todos", list=list_name))
    return redirect(url_for("todos"))

@app.route("/new_list", methods=["POST"])
def new_list():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    list_name = request.form["list_name"]
    existing = mongo.db.lists.find_one({"username": username, "list_name": list_name})
    if not existing:
        mongo.db.lists.insert_one({"username": username, "list_name": list_name})
    return redirect(url_for("todos", list=list_name))

@app.route("/delete_list/<list_name>", methods=["POST"])
def delete_list(list_name):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    mongo.db.lists.delete_one({"username": username, "list_name": list_name})
    mongo.db.todos.delete_many({"username": username, "list_name": list_name})
    return redirect(url_for("todos"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)