import os
from db import db
from flask import abort, session, request
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True


def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]


def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,role) VALUES (:username,:password,:role)"
        db.session.execute(
            sql, {"username": username, "password": hash_value, "role": role})
        db.session.commit()
    except:
        return False
    return login(username, password)


def user_id():
    return session.get("user_id", 0)


def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def check_permission(thread_id):
    sql = "SELECT id FROM threads_restricted WHERE thread_id=:thread_id AND user_id=:user_id"
    if db.session.execute(sql, {"user_id": session.get("user_id", 0), "thread_id": thread_id}).fetchone():
        return True


def get_check_user(username):
    sql = "SELECT id FROM users WHERE username ILIKE :username"
    result = db.session.execute(sql, {"username": username}).fetchone()
    if result is None:
        return False
    else:
        return result[0]


def check_role():
    return session.get("user_role", 0)
