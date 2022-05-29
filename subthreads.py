from db import db
import users


def get_subthreads(thread_id):
    sql = '''SELECT id, name, content, user_id, created_at, visible,
    (SELECT TO_CHAR(m.created_at, \'HH12:MI AM MON DD\') FROM messages m 
    WHERE m.subthread_id = s.id AND m.visible = 1 ORDER BY m.created_at DESC LIMIT 1),
    (SELECT COUNT(m.id) FROM messages m WHERE s.id = m.subthread_id AND m.visible = 1)
    FROM subthreads s WHERE s.thread_id = :thread_id AND s.visible = 1 ORDER BY name'''
    return db.session.execute(sql, {"thread_id": thread_id}).fetchall()


def create_subthread(name, content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO subthreads (name, content, thread_id, user_id, created_at, visible) VALUES (:name, :content, :thread_id, :user_id, NOW(), 1)"
    db.session.execute(sql, {"name": name, "content": content,
                       "thread_id": thread_id, "user_id": user_id})
    db.session.commit()
    return True


def get_subthread(subthread_id):
    sql = "SELECT s.id, s.name, s.content, s.thread_id, s.user_id, s.created_at, s.visible, users.username FROM subthreads s "\
        "INNER JOIN users ON s.user_id = users.id "\
        "INNER JOIN threads ON s.thread_id = threads.id "\
        "WHERE s.id=:subthread_id AND s.visible = 1"
    return db.session.execute(sql, {"subthread_id": subthread_id}).fetchone()


def remove_subthread(subthread_id):
    sql = "UPDATE subthreads SET visible = 0 WHERE id=:subthread_id"
    db.session.execute(sql, {"subthread_id": subthread_id})
    db.session.commit()


def subthreads_count():
    sql = "SELECT COUNT(*) FROM subthreads s "\
        "INNER JOIN threads t ON s.thread_id = t.id "\
        "WHERE s.visible = 1 AND t.visible = 1"
    return db.session.execute(sql).fetchone()


def edit_subthread(content, subthread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "UPDATE subthreads SET content=:content WHERE id=:subthread_id"
    db.session.execute(sql, {"content": content, "subthread_id": subthread_id})
    db.session.commit() 
