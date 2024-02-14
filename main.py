import questionary as q
from db import get_db
import helper
from habit import Habit
import analytics
from freezegun import freeze_time

# Welcome message
print("""
*** Welcome to the Habit Tracker ***
""")

# Get the database connection
db = get_db()


def main_menu():
    # Main menu options
    choice = q.select(
        "Select an option below:",
        choices=[
            "Create New Habit",
            "Delete Existing Habit",
            "Customize Habit Information",
            "Check-in Habit",
            "Analytics",
            "Exit"
        ]).ask()

    # Handling user choices
    if choice == "Create New Habit":
        # Get habit details from user and create a new habit
        habit_name = helper.prompt_habit_name()
        habit_periodicity = helper.prompt_habit_periodicity()
        habit_description = helper.prompt_habit_description()
        if helper.prompt_habit_create_confirmation(habit_name):
            habit = Habit(habit_name, habit_periodicity, habit_description)
            habit.create(db)
        else:
            print("\nHabit was not created\n")

    elif choice == "Delete Existing Habit":
        # Delete an existing habit
        try:
            habit_name = helper.prompt_list_of_habits()
        except ValueError:
            print("\nNo habit found. Please create a habit first to use this option.\n")
        else:
            habit = Habit(habit_name)
            if helper.prompt_habit_delete_confirmation(habit_name):
                habit.delete(db)
            else:
                print("\nNo Changes were made\n")

    elif choice == "Customize Habit Information":
        # Submenu for customizing habit information
        second_choice = q.select(
            "What would you like to Edit:",
            choices=[
                "Habit Name",
                "Habit Periodicity",
                "Habit description",
                "Back to Main Menu"
            ]).ask()

        if second_choice == "Habit Name":
            # Edit habit name
            try:
                old_habit_name = helper.prompt_list_of_habits()
            except ValueError:
                print("\nNo habit found. Please create a habit first to use this option.\n")
            else:
                new_habit_name = helper.prompt_new_habit_name()
                if helper.prompt_edit_habit_name_confirmation():
                    habit = Habit(old_habit_name)
                    habit.edit_name(db, new_habit_name)
                else:
                    print(f"\nName of {old_habit_name} remains unchanged!\n")

        elif second_choice == "Habit Periodicity":
            # Edit habit periodicity
            try:
                habit_name = helper.prompt_list_of_habits()
            except ValueError:  # ValueError is raised when there are no habits in the database
                print("\nNo Habit Found; Please add a habit first.\n")
            else:
                new_periodicity = helper.prompt_habit_periodicity()
                if helper.prompt_change_periodicity_confirmation():
                    habit = Habit(habit_name)
                    habit.change_periodicity(db, new_periodicity)
                else:
                    print(f"\nPeriodicity of {habit_name} remains unchanged!\n")

        elif second_choice == "Habit description":
            # Edit habit description
            try:
                habit_name = helper.prompt_list_of_habits()
            except ValueError:
                print("\nNo habit found. Please create a habit first to use this option.\n")
            else:
                new_description = helper.prompt_new_habit_description()
                if helper.prompt_edit_description_confirmation():
                    habit = Habit(habit_name)
                    habit.edit_description(db, new_description)
                else:
                    print(f"\nDescription of {habit_name} remains unchanged!\n")

        elif second_choice == "Back to Main Menu":
            main_menu()

    elif choice == "Check-in Habit":
        # Check-in for a habit
        try:
            habit_name = helper.prompt_list_of_habits()
        except ValueError:
            print("\nNo habit found. please add a habit first to complete it!\n")
        else:
            habit = Habit(habit_name)
            habit.handle_streaks(db)

    elif choice == "Analytics":
        # Submenu for analytic
        second_choice = q.select(
            "What would you like to view:",
            choices=[
                "List of all currently tracked habits",
                "List of all currently tracked habits with information",
                "List of all habits with the same periodicity",
                "Longest run streak of all defined habits",
                "Longest run streak for a given habit",
                "Back to Main Menu"
            ]).ask()

        if second_choice == "List of all currently tracked habits":
            try:
                analytics.get_all_habits(db)
            except ValueError:
                print("\nNo habit found; Please add a habit first\n")
            else:
                print("\nList of all currently tracked habits:\n")
                records = analytics.get_all_habits(db)
                analytics.print_tabular(records, db)

        elif second_choice == "List of all currently tracked habits with information":
            try:
                analytics.get_all_habits_info(db)[1:]
            except ValueError:
                print("\nNo habit found; Please add a habit first\n")
            else:
                print("\nList of all currently tracked habits with information:\n")
                records = analytics.get_all_habits_info(db)
                analytics.print_tabular(records, db)

        elif second_choice == "List of all habits with the same periodicity":
            periodicity = helper.prompt_habit_periodicity()
            try:
                analytics.get_all_habits_based_on_periodicity(db, periodicity)[1:]
            except ValueError:
                print(f"\nNo habit found with periodicity '{periodicity}'.\n")
            else:
                print("\nList of all habits with the same periodicity:\n")
                records = analytics.get_all_habits_based_on_periodicity(db, periodicity)
                analytics.print_tabular(records, db)

        elif second_choice == "Longest run streak of all defined habits":
            try:
                analytics.get_longest_streaks_of_all_habits(db)[1:]
            except ValueError:
                print("\nNo Check-in Events is Found.\n")
            else:
                print("Longest run streak of all defined habits:")
                records = analytics.get_longest_streaks_of_all_habits(db)
                analytics.print_tabular(records, db)

        elif second_choice == "Longest run streak for a given habit":
            try:
                habit_name = helper.prompt_list_of_habits()
            except ValueError:
                print("\nNo habit found. please add a habit first to complete it!\n")
            else:

                try:
                    analytics.get_longest_streak_for_given_habit(db, habit_name)[1:]
                except ValueError:
                    print(f"\nNo Check-in Events is Found for the habit '{habit_name}'.\n")
                else:
                    print("Longest run streak for a given habit:")
                    records = analytics.get_longest_streak_for_given_habit(db, habit_name)
                    analytics.print_tabular(records, db)
        elif second_choice == "Back to Main Menu":
            main_menu()
    elif choice == "Exit":
        print("\nHave a Nice Day! Remember to check-in your habits.\n")
        exit()


if __name__ == "__main__":
    while True:
        main_menu()
