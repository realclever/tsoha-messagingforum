from db import db
import users


def get_threads():
    sql = '''SELECT t.id, t.name, t.des, t.created_at, t.visible, t.restricted,
    (SELECT COUNT(s.id) FROM subthreads s WHERE t.id = s.thread_id AND s.visible = 1),
    (SELECT COUNT(m.id) FROM messages m, subthreads s  
    WHERE s.id = m.subthread_id AND t.id = s.thread_id AND s.visible = 1 AND m.visible = 1),
    (SELECT TO_CHAR(m.created_at, 'HH12:MI AM Month DD') FROM messages m INNER JOIN subthreads s ON s.id = m.subthread_id 
    WHERE t.id = s.thread_id AND s.visible = 1 AND m.visible = 1 
    ORDER BY m.created_at DESC LIMIT 1)
    FROM threads t WHERE t.visible = 1 AND t.restricted = 0 ORDER BY name'''
    return db.session.execute(sql, {}).fetchall()


def get_thread(thread_id):
    sql = "SELECT id, name, des, visible, restricted FROM threads WHERE id=:thread_id AND visible = 1"
    return db.session.execute(sql, {"thread_id": thread_id}).fetchone()


def get_restricted_threads():
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = '''SELECT t.id, t.name, t.des, t.created_at, t.visible, t.restricted, 
    (SELECT COUNT(s.id) FROM subthreads s WHERE T.id = s.thread_id AND s.visible = 1),
    (SELECT COUNT(m.id) FROM messages m, subthreads s  
    WHERE s.id = m.subthread_id AND T.id = s.thread_id AND s.visible = 1 AND m.visible = 1),
    (SELECT TO_CHAR(m.created_at, 'HH12:MI AM Month DD') FROM messages m INNER JOIN subthreads s ON s.id = m.subthread_id 
    WHERE T.id = s.thread_id AND s.visible = 1 AND m.visible = 1 
    ORDER BY m.created_at DESC LIMIT 1)
    FROM threads t INNER JOIN threads_restricted r ON t.id=r.thread_id WHERE visible = 1 AND restricted = 1 AND r.user_id=:user_id 
    GROUP BY t.id, t.name, t.des, t.created_at, t.visible, t.restricted ORDER BY name'''
    return db.session.execute(sql, {"user_id": user_id}).fetchall()
    
   
def create_thread(name, des, restricted):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO threads (name, des, created_at, visible, restricted) VALUES (:name, :des, NOW(), 1, :restricted) RETURNING id"
    thread_id = db.session.execute(
        sql, {"name": name, "des": des, "restricted": restricted}).fetchone()
    db.session.commit()
    if restricted:
        add_permission_to_restricted(thread_id[0], user_id)   
    return thread_id


def remove_thread(thread_id):
    sql = "UPDATE threads SET visible = 0 WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id": thread_id})
    db.session.commit()


def add_permission_to_restricted(thread_id, user_id):
    sql = "INSERT INTO threads_restricted (thread_id, user_id) VALUES (:thread_id, :user_id)"
    db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
    db.session.commit()
    return True

def remove_permission_to_restricted(thread_id, user_id):
    sql = "DELETE FROM threads_restricted WHERE thread_id=:thread_id AND user_id=:user_id"
    db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
    db.session.commit()
    return True    
