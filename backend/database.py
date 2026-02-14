import sqlite3
from datetime import datetime
import os

# Get absolute path to database folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "grief_circle.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id TEXT UNIQUE,
                  grief_type TEXT,
                  time_frame TEXT,
                  need TEXT,
                  circle_id INTEGER,
                  created_at TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS memorial_stones
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message TEXT,
                  created_at TIMESTAMP)''')

    conn.commit()
    conn.close()


def add_user(session_id, grief_type, time_frame, need):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO users (session_id, grief_type, time_frame, need, created_at)
                 VALUES (?, ?, ?, ?, ?)''',
              (session_id, grief_type, time_frame, need, datetime.now()))
    conn.commit()
    conn.close()


def get_waiting_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE circle_id IS NULL')
    users = c.fetchall()
    conn.close()
    return users


def assign_circle(user_ids, circle_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for user_id in user_ids:
        c.execute('UPDATE users SET circle_id = ? WHERE id = ?', (circle_id, user_id))
    conn.commit()
    conn.close()


def add_memorial_stone(message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO memorial_stones (message, created_at) VALUES (?, ?)',
              (message, datetime.now()))
    conn.commit()
    conn.close()


def get_memorial_stones(limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT message, created_at FROM memorial_stones ORDER BY created_at DESC LIMIT ?', (limit,))
    stones = c.fetchall()
    conn.close()
    return stones
