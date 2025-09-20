#!/usr/bin/python3
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="users.db"):
        """Initialize with a database name"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open connection and return cursor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit changes and close connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()

if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
