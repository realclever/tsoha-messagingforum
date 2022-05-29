from app import app
from flask import render_template, request, redirect
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
    userCount = users.users_count()

    if request.method == "GET":
        return render_template("index.html", threads=thread, subthreads=count, messages=kauant, users=userCount)

    if request.method == "POST":
        users.check_csrf()
        users.require_role(2)

        name = request.form["name"]
        des = request.form["des"]
    if len(name) < 3 or len(name) > 20:
        return render_template("error.html", message="Subject should be 3-20 characters.")
    if len(des) < 10 or len(des) > 500:
        return render_template("error.html", message="Description should be 10-500 characters.")
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
        users.check_csrf()
        users.require_role(1)

        name = request.form["name"]
        content = request.form["content"]
    if len(name) < 3 or len(name) > 50:
        return render_template("error.html", message="Subject should be 3-50 characters.")
    if len(content) < 10 or len(content) > 300:
        return render_template("error.html", message="Description should be 10-300 characters.")
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
        users.check_csrf()
        users.require_role(1)

        content = request.form["content"]
    if len(content) < 1 or len(content) > 800:
        return render_template("error.html", message="Reply should be 1-800 characters.")
    if messages.create_message(content, id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Something went wrong")


@app.route("/remove_subthread", methods=["POST"])
def remove_subthread():
    users.check_csrf()

    if "subthread_id" in request.form:
        subthread_id = request.form["subthread_id"]
        subthreads.remove_subthread(subthread_id)
    return redirect(request.referrer)


@app.route("/remove_thread", methods=["POST"])
def remove_thread():
    users.check_csrf()
    users.require_role(2)

    if "thread_id" in request.form:
        thread_id = request.form["thread_id"]
        threads.remove_thread(thread_id)
    return redirect("/")


@app.route("/remove_message", methods=["POST"])
def remove_message():
    users.check_csrf()

    if "message_id" in request.form:
        message_id = request.form["message_id"]
        messages.remove_message(message_id)
    return redirect(request.referrer)


@app.route('/edit_subthread/<int:id>', methods=["GET", "POST"])
def edit_subthread(id):
    subthread = subthreads.get_subthread(id)

    if request.method == "GET":
        return render_template("subthread_update.html", subthreads=subthread)

    if request.method == "POST":
        users.check_csrf()

        if "subthread_id" in request.form:
            content = request.form["content"]
            subthread_id = request.form["subthread_id"]
        if len(content) < 1 or len(content) > 800:
            return render_template("error.html", message="Reply should be 1-800 characters.")
        subthreads.edit_subthread(content, subthread_id)

    return redirect(request.referrer)


@app.route('/subthread/<int:s_id>/edit_message/<int:id>', methods=["GET", "POST"])
def edit_message(id, s_id):
    subthread = subthreads.get_subthread(s_id)
    message = messages.get_message(id)

    if request.method == "GET":
        return render_template("message_update.html", subthreads=subthread, messages=message)

    if request.method == "POST":
        users.check_csrf()

        if "message_id" in request.form:
            content = request.form["content"]
            message_id = request.form["message_id"]
        if len(content) < 1 or len(content) > 800:
            return render_template("error.html", message="Reply should be 1-800 characters.")
        messages.edit_message(content, message_id)

    return redirect(request.referrer)


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
            return render_template("error.html", message="Username should be 1-20 characters.")

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


@app.route("/search", methods=["POST"])
def search():
    users.check_csrf()
    
    if "message" in request.form:
        message = request.form["message"]
    if message == "":
        return render_template("error.html", message="Input at least 1 character")    

    msgs = messages.search_messages(message)
    return render_template("search.html", message=message, msgs=msgs, len=len(msgs))