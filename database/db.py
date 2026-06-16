import sqlite3

DB_NAME = "dbTOSS.db"


def connect():
    return sqlite3.connect(DB_NAME)


# def init_db():
#     conn = connect()
#     cur = conn.cursor()
#
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL
#     )
#     """)
#
#     conn.commit()
#     conn.close()


def register_user(username, password, role, position, rememberToken, createdAt):
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO tblUsers (userName, strUserPosition, "
                    "userPassword, userRole, remember_token, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, position, password, role,  rememberToken, createdAt))

        conn.commit()
        conn.close()
        return True
    except:
        return False


def validate_user(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tblUsers WHERE userName=? AND userPassword=?",
                (username, password))

    user = cur.fetchone()
    conn.close()

    return user is not None