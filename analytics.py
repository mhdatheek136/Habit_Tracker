from db import get_db
from prettytable import PrettyTable


def get_all_habits_info(db):
    """
    Retrieve information for all habits from the habit_info table.

    Parameters:
    - db: Database connection.

    Returns:
    List of tuples containing habit information.
    """
    cur = db.cursor()
    column_names = (("Habit", "Periodicity", "Description", "Creation Date", "Current Streak"), )
    cur.execute("SELECT * FROM habit_info")
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No habit information found; Please add a habit first")


def get_all_habits(db):
    """
    Retrieve the names of all habits from the habit_info table.

    Parameters:
    - db: Database connection.

    Returns:
    List of habit names.
    """
    cur = db.cursor()
    column_names = (("Habit Name", ), )
    cur.execute("SELECT habit FROM habit_info")
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No habit found; Please add a habit first")

def get_all_habits_based_on_periodicity(db, periodicity):
    """
    Retrieve habits based on a specific periodicity from the habit_info table.

    Parameters:
    - db: Database connection.
    - periodicity: Periodicity of habits to retrieve.

    Returns:
    List of tuples containing habit information.
    """
    cur = db.cursor()
    column_names = (("Habit", "Periodicity", "Description", "Creation Date", "Current Streak"),)
    cur.execute("SELECT * FROM habit_info WHERE periodicity = ?", (periodicity,))
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No habit found with that periodicity.")


def get_data_of_single_habit(db, name):
    """
    Retrieve information for a specific habit from the habit_info table.

    Parameters:
    - db: Database connection.
    - name: Name of the habit.

    Returns:
    List of tuples containing habit information.
    """
    cur = db.cursor()
    column_names = (("Habit", "Periodicity", "Description", "Creation Date", "Current Streak"),)
    cur.execute("SELECT * FROM habit_info WHERE habit = ?", (name,))
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No habit found; Please add a habit first")


def get_longest_streak_for_given_habit(db, name):
    """
    Retrieve the longest streak for a specific habit from the event_log table.

    Parameters:
    - db: Database connection.
    - name: Name of the habit.

    Returns:
    Integer representing the longest streak.
    """
    cur = db.cursor()
    string = name.capitalize() + " Longest Streak"
    column_names = ((string, ),)
    cur.execute("SELECT MAX(streak) FROM event_log WHERE habit = ?", (name,))
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No habit found; Please add a habit first")


def get_longest_streaks_of_all_habits(db):
    """
    Retrieve the longest streak for each habit from the event_log table.

    Parameters:
    - db: Database connection.

    Returns:
    List of tuples containing the longest streak for each habit.
    """
    cur = db.cursor()
    column_names = (("Habit Name", "Longest Streak"), )
    cur.execute("SELECT habit, MAX(streak) AS max_streak FROM event_log WHERE habit IN (SELECT habit FROM habit_info) GROUP BY habit")
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No habit found; Please add a habit first")


def get_event_logs_by_habit(db, name):
    """
    Retrieve event logs for a specific habit from the event_log table.

    Parameters:
    - db: Database connection.
    - name: Name of the habit.

    Returns:
    List of tuples containing event log information for the habit.
    """
    cur = db.cursor()
    column_names = (("Habit", "Streak", "Event Date"),)
    cur.execute("SELECT * FROM event_log WHERE habit = ?", (name,))
    rows = cur.fetchall()
    rows_with_header = column_names + tuple(rows)
    if len(rows) > 0:
        return rows_with_header
    else:
        raise ValueError("No check-in event found for given Habit.")


def print_tabular(data, db):
    """
    Print tabular data.

    Parameters:
    - data: List of tuples containing tabular data.
    - db: Database connection.
    """
    if not data:
        print("No data to display.")
        return

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = data[0]

    # Add rows to the table
    for row in data[1:]:
        table.add_row(row)

    print(table)
