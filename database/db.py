import hashlib
import hmac
import os
import secrets
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "data" / "dbTOSS.db"
HASH_NAME = "sha256"
HASH_ITERATIONS = 120_000
SALT_SIZE = 16


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    salt = os.urandom(SALT_SIZE)
    password_hash = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )

    return f"pbkdf2_{HASH_NAME}${HASH_ITERATIONS}${salt.hex()}${password_hash.hex()}"


def verify_password(password, stored_password):
    if not stored_password:
        return False

    if not stored_password.startswith("pbkdf2_"):
        return hmac.compare_digest(password, stored_password)

    try:
        algorithm, iterations, salt_hex, password_hash_hex = stored_password.split("$")
        hash_name = algorithm.replace("pbkdf2_", "")
        new_hash = hashlib.pbkdf2_hmac(
            hash_name,
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(new_hash.hex(), password_hash_hex)
    except ValueError:
        return False


def username_exists(username):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM tblUser WHERE lower(userName) = lower(?) LIMIT 1",
            (username,),
        )
        return cur.fetchone() is not None


def register_user(username, password, role, rememberToken, createdAt, fullname):
    try:
        password_hash = hash_password(password)

        with connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO tblUser (
                    userName,
                    userPassword,
                    userRole,
                    remember_token,
                    created_at, userFullname
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, password_hash, role, rememberToken, createdAt, fullname),
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
                userRole,
                userPassword,
                userFullname
            FROM tblUser
            WHERE userName = ?
            LIMIT 1
            """,
            (username,),
        )

        user = cur.fetchone()

    if user is None:
        return None

    user = dict(user)

    if not verify_password(password, user["userPassword"]):
        return None

    del user["userPassword"]
    return user


def create_remember_token(user_id):
    token = secrets.token_urlsafe(32)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE tblUser SET remember_token = ? WHERE userID = ?",
            (token, user_id),
        )

    return token


def get_user_by_remember_token(token):
    if not token:
        return None

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                userID,
                userName,
                userRole,
                userFullname
            FROM tblUser
            WHERE remember_token = ?
            LIMIT 1
            """,
            (token,),
        )

        user = cur.fetchone()

    if user is None:
        return None

    return dict(user)


def clear_remember_token(user_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE tblUser SET remember_token = '' WHERE userID = ?",
            (user_id,),
        )


def get_service_types():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                serviceTypeID,
                trim(serviceTypeName) AS serviceTypeName
            FROM tblServiceType
            ORDER BY serviceTypeID
            """
        )
        rows = cur.fetchall()

    return [dict(row) for row in rows]
