# models/employee_model.py
import sqlite3

class EmployeeModel:
    def __init__(self, db):
        self.db = db

    def create_employee(self, codigo: str, nome: str, apelido: str,
                        genero: str, idade: int, salario: float,
                        tempo_trabalho: str):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO employees 
                (codigo, nome, apelido, genero, idade, salario, tempo_trabalho)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (codigo, nome, apelido, genero, idade, salario, tempo_trabalho),
            )
            self.db.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Funcionário com este código já existe!")

    def get_all_employees(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()

    def get_employee_by_id(self, employee_id: int):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        return cursor.fetchone()

    def update_employee(self, employee_id: int, codigo: str, nome: str, apelido: str,
                        genero: str, idade: int, salario: float, tempo_trabalho: str):
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            UPDATE employees SET 
                codigo = ?,
                nome = ?,
                apelido = ?,
                genero = ?,
                idade = ?,
                salario = ?,
                tempo_trabalho = ?
            WHERE id = ?
            """,
            (codigo, nome, apelido, genero, idade, salario, tempo_trabalho, employee_id),
        )
        self.db.conn.commit()

    def delete_employee(self, employee_id: int):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        self.db.conn.commit()
