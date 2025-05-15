# models/database.py
import sqlite3

class Database:
    def __init__(self, db_name="app.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        # Tabela de funcionários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                apelido TEXT,
                genero TEXT,
                idade INTEGER,
                salario REAL,
                tempo_trabalho TEXT
            )
        """)
        self.conn.commit()
