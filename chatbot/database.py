import os
import sqlite3

# Set path to the SQLite DB file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "safety_reports.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            type TEXT,
            location TEXT,
            severity TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def store_report(user_id, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (user_id, type, location, severity, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        data.get("type"),
        data.get("location"),
        data.get("severity"),
        data.get("date")
    ))
    conn.commit()
    conn.close()

def get_user_reports(user_id=None):
    print("db..", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT type, location, severity, date FROM reports WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        result = [
            {"type": r[0], "location": r[1], "severity": r[2], "date": r[3]} for r in rows
        ]
    else:
        cursor.execute("SELECT user_id, type, location, severity, date FROM reports")
        rows = cursor.fetchall()
        print("rows...", rows)
        result = [
            {"user_id": r[0], "type": r[1], "location": r[2], "severity": r[3], "date": r[4]} for r in rows
        ]
    conn.close()
    return result

def update_user_location(user_id, location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Find the latest report by user
    cursor.execute("SELECT id FROM reports WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    row = cursor.fetchone()

    if row:
        report_id = row[0]
        cursor.execute("UPDATE reports SET location = ? WHERE id = ?", (location, report_id))
        print(f"Updated location for report ID {report_id}")
    else:
        print(f"No existing reports found for user: {user_id}")
    
    conn.commit()
    conn.close()

def get_user_location(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT location FROM reports WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
