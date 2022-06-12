from tabnanny import check
from app import app
from flask import render_template, request, redirect, flash
import users
import threads
import subthreads
import messages
from db import db


@app.route("/", methods=["GET", "POST"])
def index():
    thread = threads.get_threads()
    restricted_thread = threads.get_restricted_threads()

    if request.method == "GET":
        return render_template("index.html", threads=thread, restricted_threads=restricted_thread)

    if request.method == "POST":
        users.check_csrf()
        users.require_role(2)

        name = request.form["name"]
        des = request.form["des"]
        restricted = request.form["restricted"]

    if restricted not in ("0", "1"):
        flash("Unknown thread type, try again.", "warning")

        return redirect(request.referrer)
    if len(name) < 3 or len(name) > 50:
        flash("Subject should be 3-50 characters.", "warning")

        return redirect(request.referrer)
    if len(des) < 10 or len(des) > 500:
        flash("Description should be 10-500 characters.", "warning")
        return redirect(request.referrer)

    if threads.create_thread(name, des, restricted):
        flash("New thread successfully added", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong.", "danger")
        return redirect(request.referrer)


@app.route("/thread/<int:id>", methods=["GET", "POST"])
def thread(id):
    thread = threads.get_thread(id)
    subthread = subthreads.get_subthreads(id)
    check_validation = users.check_permission(id)

    check_permission = False
    if thread.restricted and check_validation:
        check_permission = True

    if request.method == "GET":
        return render_template("thread.html", thread=thread, subthreads=subthread, check_permission=check_permission)

    if request.method == "POST":
        users.check_csrf()
        users.require_role(1)

        name = request.form["name"]
        content = request.form["content"]

    if len(name) < 3 or len(name) > 50:
        flash("Subject should be 3-50 characters.", "warning")
        return redirect(request.referrer)

    if len(content) < 10 or len(content) > 300:
        flash("Description should be 10-300 characters.", "warning")
        return redirect(request.referrer)

    if subthreads.create_subthread(name, content, id):
        flash("New discussion successfully added", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong.", "danger")
        return redirect(request.referrer)


@app.route("/subthread/<int:id>", methods=["GET", "POST"])
def subthread(id):
    subthread = subthreads.get_subthread(id)
    message = messages.get_messages(id)
    thread = threads.get_thread(id)

    if request.method == "GET":
        return render_template("subthread.html", subthreads=subthread, threads=thread, messages=message)

    if request.method == "POST":
        users.check_csrf()
        users.require_role(1)

        content = request.form["content"]
    if len(content) < 1 or len(content) > 800:
        flash("Reply should be 1-800 characters.", "warning")
        return redirect(request.referrer)

    if messages.create_message(content, id):
        return redirect(request.referrer)

    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)


@app.route("/remove_subthread", methods=["POST"])
def remove_subthread():
    users.check_csrf()

    if "subthread_id" in request.form:
        subthread_id = request.form["subthread_id"]
        subthreads.remove_subthread(subthread_id)
        flash("Conversation successfully removed", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)


@app.route("/remove_thread", methods=["POST"])
def remove_thread():
    users.check_csrf()
    users.require_role(2)

    if "thread_id" in request.form:
        thread_id = request.form["thread_id"]
        threads.remove_thread(thread_id)
        flash("Thread successfully removed", "success")
        return redirect("/")

    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)


@app.route("/remove_message", methods=["POST"])
def remove_message():
    users.check_csrf()

    if "message_id" in request.form:
        message_id = request.form["message_id"]
        messages.remove_message(message_id)
        flash("Message successfully removed", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong", "danger")
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
            flash("Reply should be 1-800 characters.", "warning")
            return redirect(request.referrer)

        subthreads.edit_subthread(content, subthread_id)
        flash("Message successfully edited.", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong", "danger")
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
            flash("Reply should be 1-800 characters.", "warning")
            return redirect(request.referrer)

        messages.edit_message(content, message_id)
        flash("Message successfully edited.", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)


@app.route("/permission/<int:id>", methods=["GET", "POST"])
def permission(id):
    thread = threads.get_thread(id)
    users.require_role(2)

    if request.method == "GET":
        return render_template("permission.html", threads=thread)

    if request.method == "POST":
        users.check_csrf()

    if "thread_id" in request.form:
        username = request.form["username"]
        thread_id = request.form["thread_id"]

    if len(username) < 1 or len(username) > 20:
        flash("Username should be 1-20 characters.", "warning")
        return redirect(request.referrer)

    if users.get_check_user(username) == False:
        flash("Can't find member. Try again.", "warning")
        return redirect(request.referrer)

    if threads.add_permission_to_restricted(thread_id, users.get_check_user(username)):
        flash("Permission granted.", "success")
        return redirect(request.referrer)

    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            flash("Invalid username or password.", "warning")
            return redirect(request.referrer)

        else:
            flash("Successfully logged in", "success")
            return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    flash("Successfully logged out", "success")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            flash("Username should be 1-20 characters.", "warning")
            return redirect(request.referrer)

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Passwords don't match, try again.", "warning")
            return redirect(request.referrer)

        if password1 == "":
            flash("Password can't be null.", "warning")
            return redirect(request.referrer)

        role = request.form["role"]
        if role not in ("1", "2"):
            flash("Unknown user role, try again.", "warning")
            return redirect(request.referrer)

        if not users.register(username, password1, role):
            flash("Something went wrong, try again.", "danger")
            return redirect(request.referrer)

        else:
            flash("Registration completeted. Welcome to Discussion Forum", "success")
            return redirect("/")


@app.route("/search", methods=["POST"])
def search():

    if "message" in request.form:
        message = request.form["message"]
        msgs = messages.search_messages(message)
        return render_template("search.html", message=message, msgs=msgs, len=len(msgs))

    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)
