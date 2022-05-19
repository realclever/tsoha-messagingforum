from db import db
import users

def get_messages(subthread_id):
    sql = "SELECT m.id, m.content, m.created_at, u.username, u.id AS user_id FROM messages m "\
          "INNER JOIN users u ON m.user_id = u.id "\
          "WHERE m.subthread_id=:subthread_id AND m.visible = 1 ORDER BY m.id"
    return db.session.execute(sql, {"subthread_id":subthread_id}).fetchall()    

def create_message(content, subthread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO messages (content, subthread_id, user_id, created_at, visible) VALUES (:content, :subthread_id, :user_id, NOW(), 1)"
    db.session.execute(sql, {"content":content, "subthread_id":subthread_id, "user_id":user_id})
    db.session.commit()
    return True

def messages_count(): 
    sql = "SELECT COUNT(*) FROM messages WHERE visible=1"
    return db.session.execute(sql).fetchone()      
    


