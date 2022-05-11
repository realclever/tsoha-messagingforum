from db import db
import users

def get_threads(): 
    sql = "SELECT id, name, des, created_at FROM threads WHERE visible=1 ORDER BY name"
    return db.session.execute(sql).fetchall()

def get_thread(thread_id):
    sql = "SELECT id, name, des FROM threads WHERE visible=1 AND id=:thread_id"
    return db.session.execute(sql, {"thread_id": thread_id}).fetchone()        

def create_thread(name, des): 
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO threads (name, des, created_at, visible) VALUES (:name, :des, NOW(), 1)"
    db.session.execute(sql, {"name":name, "des":des})
    db.session.commit()
    return True

def remove_thread(thread_id):
    sql = "UPDATE threads SET visible=0 WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
