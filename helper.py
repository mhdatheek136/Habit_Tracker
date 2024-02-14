import questionary as q
from db import *


def prompt_habit_name():
    """
    Prompt the user to enter the name of a habit.

    Returns:
    - str: The entered habit name in lowercase.
    """
    return q.text("Please Enter the Name of Your Habit:",
                  validate=lambda name: True if name.isalpha() and len(name) > 0
                  else "Please enter a valid name").ask().lower()


def prompt_new_habit_name():
    """
    Prompt the user to enter the new name for a habit.

    Returns:
    - str: The entered new habit name in lowercase.
    """
    return q.text("Please Enter the New Name of Your Habit:",
                  validate=lambda name: True if name.isalpha() and len(name) > 0
                  else "Please enter a valid name").ask().lower()


def prompt_habit_periodicity():
    """
    Prompt the user to select the periodicity of a habit.

    Returns:
    - str: The selected habit periodicity in lowercase (Daily, Weekly, Monthly, Yearly).
    """
    return q.select("Please Select Habit Periodicity",
                    choices=["Daily", "Weekly", "Monthly", "Yearly"]).ask().lower()


def prompt_habit_description():
    """
    Prompt the user to enter the description for a new habit.

    Returns:
    - str: The entered habit description in lowercase.
    """
    return q.text("Please Enter Description for New Habit:",
                  validate=lambda description: True if len(description) > 0
                  else "Please enter a valid Description").ask().lower()


def prompt_new_habit_description():
    """
    Prompt the user to enter the new description for a habit.

    Returns:
    - str: The entered new habit description in lowercase.
    """
    return q.text("Please Enter New Description for Habit:",
                  validate=lambda description: True if len(description) > 0
                  else "Please enter a valid Description").ask().lower()


def prompt_list_of_habits():
    """
    Prompt the user to select a habit from the list of available habits.

    Returns:
    - str: The selected habit name in lowercase.

    Raises:
    - ValueError: If no habit is found in the database.
    """
    db = get_db()
    habits_list = get_all_habits_as_choices(db)
    if habits_list is not None:
        return q.select("Please Select a Habit",
                        choices=sorted(habits_list)).ask().lower()
    else:
        raise ValueError("No habit found. Please create a habit first to use this option.")


def prompt_habit_create_confirmation(habit_name):
    """
    Prompt the user to confirm the creation of a new habit.

    Parameters:
    - habit_name (str): The name of the habit.

    Returns:
    - bool: True if the user confirms, False otherwise.
    """
    return q.confirm(f"This action will create habit '{habit_name}'. Would you like to continue?").ask()


def prompt_habit_delete_confirmation(habit_name):
    """
    Prompt the user to confirm the deletion of a habit.

    Parameters:
    - habit_name (str): The name of the habit.

    Returns:
    - bool: True if the user confirms, False otherwise.
    """
    return q.confirm(f"This action will delete the '{habit_name}' habit and it's past streaks information. Would you like to continue?").ask()


def prompt_change_periodicity_confirmation():
    """
    Prompt the user to confirm the change of a habit's periodicity.

    Returns:
    - bool: True if the user confirms, False otherwise.
    """
    return q.confirm("Changing periodicity of a habit will reset the streak. Would you like to continue?").ask()


def prompt_edit_description_confirmation():
    """
    Prompt the user to confirm the edit of a habit's description.

    Returns:
    - bool: True if the user confirms, False otherwise.
    """
    return q.confirm("Your current description will be deleted. Would you like to continue?").ask()


def prompt_edit_habit_name_confirmation():
    """
    Prompt the user to confirm the edit of a habit's name.

    Returns:
    - bool: True if the user confirms, False otherwise.
    """
    return q.confirm("Your current habit name will be changed. Would you like to continue?").ask()
