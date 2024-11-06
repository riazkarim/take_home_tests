import sqlite3
DB_FILE = 'log_data.db'
LOG_FILE = 'api_requests.log'

# Create database and table
def create_db():
    print('Creating database...')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            customer_id INTEGER,
            request_path TEXT,
            status_code INTEGER,
            duration INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Populate database from log file
def populate_db():
    print('Populating database...')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    with open(LOG_FILE, 'r') as file:
        for line in file:
            row = line.split(' ')
            timestamp, customer_id, request_path, status_code, duration = row[0] + ' ' + row[1], row[2].split('_')[1], row[3], row[4], row[5].strip()
            cursor.execute('''
                INSERT INTO api_logs (timestamp, customer_id, request_path, status_code, duration)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, customer_id, request_path, status_code, duration))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    populate_db()
