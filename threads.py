from db import db
import users


def get_threads():
    sql = '''SELECT id, name, des, created_at, visible, restricted,
    (SELECT COUNT(s.id) FROM subthreads s WHERE threads.id = s.thread_id AND s.visible = 1),
    (SELECT COUNT(m.id) FROM messages m, subthreads s  
    WHERE s.id = m.subthread_id AND threads.id = s.thread_id AND s.visible = 1 AND m.visible = 1),
    (SELECT TO_CHAR(m.created_at, 'HH12:MI AM MON DD') FROM messages m INNER JOIN subthreads s ON s.id = m.subthread_id 
    WHERE threads.id = s.thread_id AND s.visible = 1 AND m.visible = 1 
    ORDER BY m.created_at DESC LIMIT 1)
    FROM threads WHERE visible = 1 AND restricted = 0 ORDER BY name'''
    return db.session.execute(sql, {}).fetchall()


def get_thread(thread_id):
    sql = "SELECT id, name, des, visible, restricted FROM threads WHERE id=:thread_id AND visible = 1"
    return db.session.execute(sql, {"thread_id": thread_id}).fetchone()


def get_restricted_threads():
    sql = '''SELECT id, name, des, created_at, visible, restricted,
    (SELECT COUNT(s.id) FROM subthreads s WHERE threads.id = s.thread_id AND s.visible = 1),
    (SELECT COUNT(m.id) FROM messages m, subthreads s  
    WHERE s.id = m.subthread_id AND threads.id = s.thread_id AND s.visible = 1 AND m.visible = 1),
    (SELECT TO_CHAR(m.created_at, 'HH12:MI AM MON DD') FROM messages m INNER JOIN subthreads s ON s.id = m.subthread_id 
    WHERE threads.id = s.thread_id AND s.visible = 1 AND m.visible = 1 
    ORDER BY m.created_at DESC LIMIT 1)
    FROM threads WHERE visible = 1 AND restricted = 1 ORDER BY name'''
    return db.session.execute(sql, {}).fetchall()


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
