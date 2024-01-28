import sqlite3


def get_db(name="main.db"):
    """
    Get a connection to the SQLite database with the specified name.

    Parameters:
    - name (str): Name of the SQLite database file.

    Returns:
    - sqlite3.Connection: Connection object to the database.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Create tables in the database if they do not exist.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    """
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
    """
    Add a new habit to the habit_info table in the database.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    - periodicity (str): Frequency at which the habit should be performed.
    - description (str): Description of the habit.
    - creation_date (str): Date when the habit was created.
    - streak (int): Current streak of the habit.
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habit_info VALUES (?, ?, ?, ?, ?)",
                (name, periodicity, description, creation_date, streak))
    db.commit()


def is_habit_exists(db, name):
    """
    Check if a habit with the given name already exists in the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.

    Returns:
    - bool: True if the habit exists, False otherwise.
    """

    cur = db.cursor()
    cur.execute("SELECT 1 FROM habit_info WHERE habit = ?", (name, ))
    return True if cur.fetchone() is not None else False


def remove_habit(db, name):
    """
    Remove a habit with the given name from the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habit_info WHERE habit = ?", (name, ))
    db.commit()


def update_habit_name(db, old_name, new_name):
    """
    Update the name of a habit in the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - old_name (str): Current name of the habit.
    - new_name (str): New name for the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET habit = ? WHERE habit = ?", (new_name, old_name))
    db.commit()


def update_description(db, name, new_description):
    """
    Update the description of a habit in the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    - new_description (str): New description for the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET description = ? WHERE habit = ?", (new_description, name))
    db.commit()


def update_periodicity(db, name, new_periodicity):
    """
    Update the periodicity of a habit in the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    - new_periodicity (str): New periodicity value for the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET periodicity = ? WHERE habit = ?", (new_periodicity, name))
    db.commit()


def reset_streak(db, name):
    """
    Reset the streak of a habit to zero in the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET streak = ? WHERE habit = ?", (0, name))
    db.commit()


def get_current_streak(db, name):
    """
    Get the current streak of a habit from the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.

    Returns:
    - int: Current streak of the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT streak FROM habit_info WHERE habit = ?", (name, ))
    current_streak = cur.fetchone()
    return current_streak[0]


def update_log(db, name, streak, event_date):
    """
    Update the event log with a new entry for a habit in the event_log table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    - streak (int): Current streak of the habit.
    - event_date (str): Date of the event.
    """
    cur = db.cursor()
    cur.execute("INSERT INTO event_log VALUES (?, ?, ?)", (name, streak, event_date))
    db.commit()


def update_streak(db, name, streak):
    """
    Update the streak of a habit in the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.
    - streak (int): New streak value for the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habit_info SET streak = ? WHERE habit = ?", (streak, name))
    db.commit()


def get_last_update_date(db, name):
    """
    Get the date of the last recorded event for a habit.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.

    Returns:
    - str or None: Date of the last recorded event, or None if no events exist for the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT event_date FROM event_log WHERE habit = ? ORDER BY event_date DESC LIMIT 1", (name, ))
    row = cur.fetchone()
    return row[0] if row is not None else None


def get_periodicity(db, name):
    """
    Get the periodicity of a habit from the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.

    Returns:
    - str: Periodicity of the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habit_info WHERE habit = ?", (name,))
    periodicity = cur.fetchone()
    return periodicity[0]


def get_description(db, name):
    """
    Get the description of a habit from the habit_info table.

    Parameters:
    - db (sqlite3.Connection): Connection object to the database.
    - name (str): Name of the habit.

    Returns:
    - str: Description of the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT description FROM habit_info WHERE habit = ?", (name,))
    desc = cur.fetchone()
    return desc[0]
