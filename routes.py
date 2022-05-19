from app import app
from flask import flash, render_template, request, redirect
import users
import threads
import subthreads
import messages
from db import db

@app.route("/", methods=["GET", "POST"])
def index():
    thread = threads.get_threads()
    count = subthreads.subthreads_count()
    kauant = messages.messages_count()

    if request.method == "GET":
        return render_template("index.html", threads=thread, subthreads=count, messages=kauant)

    if request.method == "POST":
        users.require_role(2)

        name = request.form["name"]
        des = request.form["des"]
    if threads.create_thread(name, des):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Something went wrong") 

@app.route("/thread/<int:id>", methods=["GET", "POST"])
def thread(id):
    thread = threads.get_thread(id)
    subthread = subthreads.get_subthreads(id)

    if request.method == "GET":
        return render_template("thread.html", thread=thread, subthreads=subthread)

    if request.method == "POST":
        users.require_role(1)
        name = request.form["name"]
        content = request.form["content"]
    if subthreads.create_subthread(name, content, id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Something went wrong")

@app.route("/subthread/<int:id>", methods=["GET", "POST"])
def subthread(id):
    subthread = subthreads.get_subthread(id)
    message = messages.get_messages(id)

    if request.method == "GET":
        return render_template("subthread.html", subthreads=subthread, messages=message)

    if request.method == "POST":
        users.require_role(1)
        content = request.form["content"]
    if messages.create_message(content, id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Something went wrong")    

@app.route("/remove_subthread", methods=["POST"])   
def remove_subthread():
    
    if "subthread_id" in request.form:
        subthread_id = request.form["subthread_id"]
        subthreads.remove_subthread(subthread_id)
    return redirect(request.referrer)

@app.route("/remove_thread", methods=["POST"])   
def remove_thread():
    users.require_role(2)
    
    if "thread_id" in request.form:
        thread_id = request.form["thread_id"]
        threads.remove_thread(thread_id)
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if not users.login(username, password):
            return render_template("error.html", message="Invalid username or password.")
        return redirect("/")    

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")
            
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords don't match, try again.")

        if password1 == "":
            return render_template("error.html", message="Password can't be null.")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Unknown user role, try again.")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Something went wrong, try again.")
        return redirect("/")