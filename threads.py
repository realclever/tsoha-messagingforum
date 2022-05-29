from db import db
import users


def get_threads():
    sql = '''SELECT id, name, des, created_at, visible, 
    (SELECT COUNT(s.id) FROM subthreads s WHERE threads.id = s.thread_id AND s.visible = 1),
    (SELECT COUNT(m.id) FROM messages m, subthreads s  
    WHERE s.id = m.subthread_id AND threads.id = s.thread_id AND s.visible = 1 AND m.visible = 1),
    (SELECT TO_CHAR(m.created_at, 'HH12:MI AM MON DD') FROM messages m INNER JOIN subthreads s ON s.id = m.subthread_id 
    WHERE threads.id = s.thread_id AND s.visible = 1 AND m.visible = 1 
    ORDER BY m.created_at DESC LIMIT 1)
    FROM threads WHERE visible = 1 ORDER BY name'''
    return db.session.execute(sql, {}).fetchall()


def get_thread(thread_id):
    sql = "SELECT id, name, des, visible FROM threads WHERE id=:thread_id AND visible = 1"
    return db.session.execute(sql, {"thread_id": thread_id}).fetchone()


def create_thread(name, des):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO threads (name, des, created_at, visible) VALUES (:name, :des, NOW(), 1)"
    db.session.execute(sql, {"name": name, "des": des})
    db.session.commit()
    return True


def remove_thread(thread_id):
    sql = "UPDATE threads SET visible=0 WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id": thread_id})
    db.session.commit()
