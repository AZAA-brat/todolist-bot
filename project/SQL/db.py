import sqlite3
from datetime import datetime
from interface.config import DB_PATH
def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_text TEXT,
        is_done INTEGER,
        created_at TEXT 
    );  
    """
    )
    connection.commit()
    connection.close()

def add_task(user_id, task_text):
    created_at = datetime.now().isoformat()
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
    """
    INSERT INTO tasks (user_id, task_text, is_done, created_at) VALUES (?, ?, ?, ?) 
    """,
    (user_id, task_text, 0, created_at)
    )
    connection.commit()
    connection.close()

def get_tasks(user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
    """
    SELECT * FROM tasks WHERE user_id = ?
    """,
    (user_id,)
    )
    rows = cursor.fetchall()
    connection.close()
    return rows

def mark_done(task_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
    """
    UPDATE tasks SET is_done = ? WHERE id = ?
    """,
    (1, task_id)
    )
    connection.commit()
    connection.close()

def delete_task(task_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
    """
    DELETE FROM tasks WHERE id = ?
    """,
    (task_id,)
    )
    connection.commit()
    connection.close()
