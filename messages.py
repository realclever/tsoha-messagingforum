from db import db
import users


def get_messages(subthread_id):
    sql = "SELECT m.id, m.content, m.created_at, u.username, u.id AS user_id FROM messages m "\
        "INNER JOIN users u ON m.user_id = u.id "\
        "WHERE m.subthread_id=:subthread_id AND m.visible = 1 ORDER BY m.id"
    return db.session.execute(sql, {"subthread_id": subthread_id}).fetchall()


def get_message(message_id):
    sql = "SELECT m.id, m.content, m.subthread_id, m.user_id, m.created_at, u.username FROM messages m "\
        "INNER JOIN users u ON m.user_id = u.id "\
        "INNER JOIN subthreads ON m.subthread_id = subthreads.id "\
        "WHERE m.id=:message_id AND m.visible = 1"
    return db.session.execute(sql, {"message_id": message_id}).fetchone()


def create_message(content, subthread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO messages (content, subthread_id, user_id, created_at, visible) VALUES (:content, :subthread_id, :user_id, NOW(), 1)"
    db.session.execute(
        sql, {"content": content, "subthread_id": subthread_id, "user_id": user_id})
    db.session.commit()
    return True


def remove_message(message_id):
    sql = "UPDATE messages SET visible = 0 WHERE id=:message_id"
    db.session.execute(sql, {"message_id": message_id})
    db.session.commit()


def messages_count():
    sql = "SELECT COUNT(*) FROM messages m "\
        "INNER JOIN subthreads s ON m.subthread_id = s.id "\
        "INNER JOIN threads t ON s.thread_id = t.id "\
        "WHERE m.visible = 1 AND s.visible = 1 AND t.visible = 1"
    return db.session.execute(sql).fetchone()


def subthreads_count():
    sql = "SELECT COUNT(*) FROM subthreads s "\
        "INNER JOIN threads t ON s.thread_id = t.id "\
        "WHERE s.visible = 1 AND t.visible = 1"
    return db.session.execute(sql).fetchone()


def edit_message(content, message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "UPDATE messages SET content=:content WHERE id=:message_id"
    db.session.execute(sql, {"content": content, "message_id": message_id})
    db.session.commit()


def search_messages(message):
    sql = "SELECT m.id, m.content, m.subthread_id, s.name, m.created_at FROM messages m "\
        "INNER JOIN subthreads s ON m.subthread_id = s.id "\
        "INNER JOIN threads t ON s.thread_id = t.id "\
        "WHERE m.content ILIKE :message AND m.visible = 1 AND s.visible = 1 AND t.visible = 1 ORDER by m.id"
    return db.session.execute(sql, {"message": "%"+message+"%"}).fetchall()   
