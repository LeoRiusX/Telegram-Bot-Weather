import os
import sqlite3
from datetime import datetime

from aiogram import BaseMiddleware



db = sqlite3.connect("users.db")
cursor = db.cursor()

# Database structure ->

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    city TEXT
)
""")


# Functions for working with databases!



db.commit()

#Logging messages to the database -> (txt)

class LoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        message = data.get("event_update", None)
        if hasattr(message, "message") and message.message:
            msg = message.message
            content = msg.text if msg.text else f"<{msg.content_type}>"
            user_info = f"{msg.from_user.id} | @{msg.from_user.username or '-'} | {msg.from_user.full_name}"

            # Получаем текущее время
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Записываем в лог
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{now}] {user_info}: {content}\n")

        return await handler(event, data)



# Logging user to the database -> (sql)
def add_user(user_id, username, first_name, city=None):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name, city) VALUES (?, ?, ?, ?)",
        (user_id, username, first_name, city)
    )
    db.commit()

def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()

    # for row in rows:
    #     print(row)  # печатаем

    return [row[0] for row in rows]

def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    db.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

USERS = get_all_users()
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "log.txt")

def set_user_city(user_id, city):
    cursor.execute("UPDATE users SET city=? WHERE user_id=?", (city, user_id))
    db.commit()

def get_user_city(user_id):
    cursor.execute("SELECT city FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def clear_user_city(user_id: int):
    cursor.execute(
        "UPDATE users SET city = NULL WHERE user_id = ?",
        (user_id,)
    )
    db.commit()

def full_city(user_id: int) -> bool:
    cursor.execute(
        "SELECT city FROM users WHERE user_id = ? AND city IS NOT NULL",
        (user_id,)
    )
    return cursor.fetchone() is not None








