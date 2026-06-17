import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "data" / "dbTOSS.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def register_user(username, password, role, position, rememberToken, createdAt):
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO tblUser (
                    userName,
                    strUserPosition,
                    userPassword,
                    userRole,
                    remember_token,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, position, password, role, rememberToken, createdAt),
            )

        return True
    except sqlite3.Error:
        return False


def validate_user(username, password):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                userID,
                userName,
                strUserPosition,
                userRole
            FROM tblUser
            WHERE userName = ?
              AND userPassword = ?
            """,
            (username, password),
        )

        user = cur.fetchone()

    if user is None:
        return None

    return dict(user)
