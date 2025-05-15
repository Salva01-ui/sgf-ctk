# models/user_model.py
import re
import sqlite3
import hashlib

class UserModel:
    def __init__(self, db):
        self.db = db

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def create_user(self, username: str, email: str, password: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email inválido!")
        hashed = self.hash_password(password)
        cursor = self.db.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed),
            )
            self.db.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Usuário já existe!")

    def get_user_by_username(self, username: str):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    def authenticate(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if user and user[3] == self.hash_password(password):
            return user
        return None

    def get_all_users(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, username, email FROM users")
        return cursor.fetchall()

    def update_user(self, user_id: int, username: str, email: str, password: str = None):
        cursor = self.db.conn.cursor()
        if password:
            hashed = self.hash_password(password)
            cursor.execute(
                "UPDATE users SET username=?, email=?, password=? WHERE id=?",
                (username, email, hashed, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET username=?, email=? WHERE id=?",
                (username, email, user_id)
            )
        self.db.conn.commit()

    def delete_user(self, user_id: int):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db.conn.commit()
