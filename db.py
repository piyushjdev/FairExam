import sqlite3

def get_connection():
    return sqlite3.connect("fairexam.db", check_same_thread=False)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam TEXT,
        issue_type TEXT,
        state TEXT,
        description TEXT,
        sentiment TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_incident(exam, issue_type, state, description, sentiment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO incidents (exam, issue_type, state, description, sentiment)
    VALUES (?, ?, ?, ?, ?)
    """, (exam, issue_type, state, description, sentiment))

    conn.commit()
    conn.close()

def fetch_incidents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows