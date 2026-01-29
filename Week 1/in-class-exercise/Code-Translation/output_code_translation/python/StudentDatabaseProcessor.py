import sqlite3
from typing import List, Dict


class StudentDatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_student_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                grade INTEGER
            )
        """
        self.execute_query(create_table_query, [])

    def insert_student(self, student_data: Dict[str, str]) -> None:
        insert_query = """
            INSERT INTO students (name, age, gender, grade)
            VALUES (?, ?, ?, ?)
        """
        params = [
            student_data["name"],
            student_data["age"],
            student_data["gender"],
            student_data["grade"]
        ]
        self.execute_query(insert_query, params)

    def search_student_by_name(self, name: str) -> List[Dict[str, str]]:
        select_query = """
            SELECT * FROM students WHERE name = ?
        """
        results = self.query_result(select_query, [name])
        students: List[Dict[str, str]] = []
        for row in results:
            student = {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "grade": row[4]
            }
            students.append(student)
        return students

    def delete_student_by_name(self, name: str) -> None:
        delete_query = """
            DELETE FROM students WHERE name = ?
        """
        self.execute_query(delete_query, [name])

    def execute_query(self, query: str, params: List[str]) -> None:
        conn = sqlite3.connect(self.database_name)
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
        finally:
            conn.close()

    def query_result(self, query: str, params: List[str]) -> List[List[str]]:
        conn = sqlite3.connect(self.database_name)
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            # Convert each column value to string to match C++ behavior
            return [[str(col) if col is not None else "" for col in row] for row in rows]
        finally:
            conn.close()
