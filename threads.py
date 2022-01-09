from db import db
import users

def get_threads(): 
    sql = "SELECT id, name, created_at FROM threads WHERE visible=1 ORDER BY name"
    return db.session.execute(sql).fetchall()

def create_thread(name): 
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (name, created_at, visible) VALUES (:name, NOW(), 1)"
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return True

def remove_thread(thread_id):
    sql = "UPDATE threads SET visible=0 WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
