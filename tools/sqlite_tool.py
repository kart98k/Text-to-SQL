import sqlite3
import pandas as pd
import os

# Path to SQLite database file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "college.db")


def run_query(sql: str):
    """
    Execute SQL query and return pandas DataFrame
    """
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(sql, conn)
        return df

    finally:
        conn.close()


def get_schema():
    """
    Dynamically read all tables and columns
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema = ""

    try:
        # Get all user tables
        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%';
        """).fetchall()

        for table in tables:
            table_name = table[0]

            schema += f"\nTable: {table_name}\n"

            columns = cursor.execute(
                f"PRAGMA table_info({table_name});"
            ).fetchall()

            for col in columns:
                col_name = col[1]
                col_type = col[2]

                schema += f"{col_name} ({col_type})\n"

    finally:
        conn.close()

    return schema