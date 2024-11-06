import sqlite3
from datetime import datetime


class LogDataProvider:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def get_customer_data(self, customer_id: int, from_date: datetime):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT timestamp, status_code, duration FROM api_logs
                        WHERE customer_id = ? AND timestamp >= ?
                    ''', (customer_id, from_date))

        data = cursor.fetchall()
        conn.close()

        return data
