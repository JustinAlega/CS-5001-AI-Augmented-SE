import sqlite3
from typing import List, Dict


class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def open_database(self) -> sqlite3.Connection:
        try:
            return sqlite3.connect(self.database_name)
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        db = self.open_database()
        create_table_query = (
            f"CREATE TABLE IF NOT EXISTS {table_name} "
            f"(id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
        )
        try:
            db.execute(create_table_query)
            db.commit()
        except sqlite3.Error as e:
            db.close()
            raise RuntimeError(f"Failed to create table: {e}")
        db.close()

    def insert_into_database(
        self,
        table_name: str,
        data: List[Dict[str, str]],
    ) -> None:
        db = self.open_database()
        insert_query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
        cursor = db.cursor()
        try:
            for item in data:
                cursor.execute(
                    insert_query,
                    (item["name"], int(item["age"])),
                )
            db.commit()
        except (KeyError, ValueError, sqlite3.Error) as e:
            db.close()
            raise RuntimeError(f"Failed to execute statement: {e}")
        finally:
            cursor.close()
            db.close()

    def search_database(self, table_name: str, name: str) -> List[List[str]]:
        result: List[List[str]] = []
        try:
            db = sqlite3.connect(self.database_name)
            query = f"SELECT * FROM {table_name} WHERE name = ?"
            cursor = db.execute(query, (name,))
            for row in cursor:
                result.append(["" if v is None else str(v) for v in row])
        except sqlite3.Error:
            pass
        finally:
            db.close()
        return result

    def delete_from_database(self, table_name: str, name: str) -> None:
        db = self.open_database()
        delete_query = f"DELETE FROM {table_name} WHERE name = ?"
        cursor = db.cursor()
        try:
            cursor.execute(delete_query, (name,))
            db.commit()
        except sqlite3.Error as e:
            db.close()
            raise RuntimeError(f"Failed to execute statement: {e}")
        finally:
            cursor.close()
            db.close()
