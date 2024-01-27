import sqlite3
from datetime import datetime


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_info (
            habit TEXT PRIMARY KEY , 
            periodicity TEXT,
            description TEXT,
            creation_date TEXT,
            streak INT  
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS event_log (
            habit TEXT,
            streak INT,
            event_date DATE,
            FOREIGN KEY (habit) 
            REFERENCES habit_info (habit) 
            ON UPDATE CASCADE 
            ON DELETE CASCADE
        )""")

    db.commit()


def add_habit(db, name, periodicity, description, creation_date, streak):
    cur = db.cursor()
    cur.execute("INSERT INTO habit_info VALUES (?, ?, ?, ?, ?)", (name, periodicity, description, creation_date, streak))
    db.commit()


def is_habit_exists(db, name):
    cur = db.cursor()
    cur.execute("SELECT 1 FROM habit_info WHERE habit = ?", (name, ))
    return True if cur.fetchone() is not None else False


def remove_habit(db, name):
    cur = db.cursor()
    cur.execute("DELETE FROM habit_info WHERE habit = ?", (name, ))
    db.commit()


def update_habit_name(db, old_name, new_name):
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET habit = ? WHERE habit = ?", (new_name, old_name))
    db.commit()


def update_description(db, name, new_description):
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET description = ? WHERE habit = ?", (new_description, name))
    db.commit()


def update_periodicity(db, name, new_periodicity):
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET periodicity = ? WHERE habit = ?", (new_periodicity, name))
    db.commit()


def reset_streak(db, name):
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET streak = ? WHERE habit = ?", (0, name))
    db.commit()


def get_current_streak(db, name):
    cur = db.cursor()
    cur.execute("SELECT streak FROM habit_info WHERE habit = ?", (name, ))
    current_streak = cur.fetchone()
    return current_streak[0]


def update_log(db, name, streak, event_date):
    cur = db.cursor()
    cur.execute("INSERT INTO event_log VALUES (?, ?, ?)", (name, streak, event_date))
    db.commit()


def update_streak(db, name, streak):
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET streak = ? WHERE habit = ?", (streak, name))
    db.commit()


def get_last_update_date(db, name):
    cur = db.cursor()
    cur.execute("SELECT event_date FROM event_log WHERE habit = ? ORDER BY event_date DESC LIMIT 1", (name, ))
    last_update_date = cur.fetchone()
    return last_update_date[0]


def get_periodicity(db, name):
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habit_info WHERE habit = ?", (name,))
    periodicity = cur.fetchone()
    return periodicity[0]


def get_description(db, name):
    cur = db.cursor()
    cur.execute("SELECT description FROM habit_info WHERE habit = ?", (name,))
    desc = cur.fetchone()
    return desc[0]




