from typing import List, Tuple


class SQLQueryBuilder:
    @staticmethod
    def select(table: str,
               columns: List[str] = ["*"],
               where: List[Tuple[str, str]] = []) -> str:
        # SELECT clause
        if len(columns) == 1 and columns[0] == "*":
            query = "SELECT *"
        else:
            query = "SELECT " + ", ".join(columns)

        query += f" FROM {table}"

        # WHERE clause
        if where:
            conditions = [f"{key}='{value}'" for key, value in where]
            query += " WHERE " + " AND ".join(conditions)

        return query

    @staticmethod
    def insert(table: str,
               data: List[Tuple[str, str]]) -> str:
        columns = ", ".join(col for col, _ in data)
        values = ", ".join(f"'{val}'" for _, val in data)
        return f"INSERT INTO {table} ({columns}) VALUES ({values})"

    @staticmethod
    def delete_(table: str,
                where: List[Tuple[str, str]] = []) -> str:
        query = f"DELETE FROM {table}"
        if where:
            conditions = [f"{key}='{value}'" for key, value in where]
            query += " WHERE " + " AND ".join(conditions)
        return query

    @staticmethod
    def update(table: str,
               data: List[Tuple[str, str]],
               where: List[Tuple[str, str]] = []) -> str:
        set_clause = ", ".join(f"{col}='{val}'" for col, val in data)
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            conditions = [f"{key}='{value}'" for key, value in where]
            query += " WHERE " + " AND ".join(conditions)
        return query
