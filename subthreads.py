from db import db
import users

def get_subthreads(thread_id): 
    sql = "SELECT id, name, user_id FROM subthreads WHERE thread_id=:thread_id AND visible = 1"
    return db.session.execute(sql, {"thread_id": thread_id}).fetchall()

def create_subthread(name, content, thread_id): 
    user_id = users.user_id()
    if user_id == 0:
        return False
        
    sql = "INSERT INTO subthreads (name, content, thread_id, user_id, visible) VALUES (:name, :content, :thread_id, :user_id, 1)"
    db.session.execute(sql, {"name":name, "content":content, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True

def get_subthread(subthread_id):
    sql = "SELECT s.id, s.name, s.content, s.thread_id, s.user_id, users.username FROM subthreads s "\
          "INNER JOIN users ON s.user_id = users.id "\
          "INNER JOIN threads ON s.thread_id = threads.id "\
          "WHERE s.id=:subthread_id AND s.visible = 1"
    return db.session.execute(sql, {"subthread_id": subthread_id}).fetchone()        

def remove_subthread(subthread_id):
    sql = "UPDATE subthreads SET visible=0 WHERE id=:subthread_id"
    db.session.execute(sql, {"subthread_id":subthread_id})
    db.session.commit()
  