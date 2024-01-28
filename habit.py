from datetime import datetime
from db import *


class Habit:
    """
        A class representing a habit with methods to manage and track habit-related information.
    """

    def __init__(self, name: str = None, periodicity: str = None, description: str = None):
        """
        Initialize a Habit object with specified attributes.

        Parameters:
        - name: Name of the habit.
        - periodicity: Frequency at which the habit should be performed (daily, weekly, monthly, yearly).
        - description: Description of the habit.
        """
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
        self.streak = 0

    def create(self, db):
        """
        Create a new habit in the database.

        Parameters:
        - db: Database object.

        Prints a success message if the habit is created, or an error message if the habit name is already taken.
        """
        if is_habit_exists(db, self.name) is False:
            add_habit(db, self.name, self.periodicity, self.description, self.creation_date, self.streak)
            print(f"\nNew habit '{self.name.capitalize()}' is created successfully.\n")
        else:
            print("\nHabit name typed is already taken. Try new habit name.\n")
        return

    def delete(self, db):
        """
        Delete the habit from the database.

        Parameters:
        - db: Database object.

        Prints a success message after deleting the habit.
        """
        remove_habit(db, self.name)
        print(f"\nHabit'{self.name.capitalize()}' is deleted successfully.\n")

    def edit_name(self, db, new_name):
        """
        Delete the habit from the database.

        Parameters:
        - db: Database object.

        Prints a success message after deleting the habit.
        """
        if is_habit_exists(db, new_name) is False:
            update_habit_name(db, self.name, new_name)
            print(f"\nHabit name is changed successfully.\n")
        else:
            print("\nHabit name typed is already taken. Try new habit name.\n")
        return

    def edit_description(self, db, new_description):
        """
        Delete the habit from the database.

        Parameters:
        - db: Database object.

        Prints a success message after deleting the habit.
        """
        update_description(db, self.name, new_description)
        print(f"\nDescription changed successfully.\n")
        return

    def change_periodicity(self, db, new_periodicity):
        """
        Change the periodicity of the habit in the database.

        Parameters:
        - db: Database object.
        - new_periodicity: New periodicity for the habit.

        Resets the streak and prints a success message after changing the periodicity.
        """
        update_periodicity(db, self.name, new_periodicity)
        reset_streak(db, self.name)
        print(f"\nPeriodicity for  '{self.name.capitalize()}' is changed to '{new_periodicity}'.\n")
        return

    def increment_streak(self, db):
        """
        Increment the streak for the habit.

        Parameters:
        - db: Database object.

        Prints the current streak after incrementing it.
        """
        self.streak = get_current_streak(db, self.name)
        self.streak += 1
        print(f"\nYour current streak for the habit  '{self.name.capitalize()}' is '{self.streak}'.\n")
        return

    def add_event(self, db):
        """
        Add an event to the habit, incrementing the streak and updating the log.

        Parameters:
        - db: Database object.
        """
        self.increment_streak(db)
        current_date = datetime.now().strftime("%Y-%m-%d")
        update_log(db, self.name, self.streak, current_date)
        update_streak(db, self.name, self.streak)
        return

    def handle_streaks(self, db):
        """
        Handle streaks based on the habit's periodicity.

        Parameters:
        - db: Database object.

        Manages streaks based on different cases for daily, weekly, monthly, and yearly habits.
        """
        last_event_date = get_last_update_date(db, self.name)
        # Case 01: No previous events recorded
        if last_event_date is None:
            self.add_event(db)
        # Habit is set to be performed daily
        elif get_periodicity(db, self.name) == "daily":
            # Case 02: Checked in today
            if self.get_day_difference(db) == 0:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' today. You can check-in again "
                      f"tomorrow.\n")
            # Case 03: Checked in yesterday
            elif self.get_day_difference(db) == 1:
                self.add_event(db)
            # Case 04: Previous streak broken
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for "
                      f"habit '{self.name.capitalize()}' is 1.\n")
        # Case 03: Habit is set to be performed weekly
        elif get_periodicity(db, self.name) == "weekly":
            days_to_complete_week = self.get_days_to_complete_week(db)
            day_difference = self.get_day_difference(db)
            next_possible_day = days_to_complete_week - day_difference + 1
            # Case 05: Already checked for the entire week
            if days_to_complete_week >= day_difference:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' for this week. You can "
                      f"check-in again in '{next_possible_day}' days.\n")
            # Case 06: Checked in within the past week
            elif days_to_complete_week < day_difference <= days_to_complete_week + 7:
                self.add_event(db)
            # Case 07: Previous streak broken
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for "
                      f"habit '{self.name.capitalize()}' is 1.\n")
        # Habit is set to be performed monthly
        elif get_periodicity(db, self.name) == "monthly":
            # Case 08: Already checked for the entire month
            if self.get_month_difference(db) == 0:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' for this month. "
                      f"You can check-in again next month.\n")
            # Case 09: Checked in within the past month
            elif self.get_month_difference(db) == 1:
                self.add_event(db)
            # Case 10: Previous streak broken
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for "
                      f"habit '{self.name.capitalize()}' is 1.\n")
        # Habit is set to be performed yearly
        elif get_periodicity(db, self.name) == "yearly":
            # Case 11: Already checked for the entire year
            if self.get_year_difference(db) == 0:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' for this year. "
                      f"You can check-in again next year.\n")
            # Case 12: Checked in within the past year
            elif self.get_year_difference(db) == 1:
                self.add_event(db)
            # Case13: Previous streak broken
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for "
                      f"habit '{self.name.capitalize()}' is 1.\n")

    def get_day_difference(self, db):
        """
        Calculate the difference in days between the last event date and the current date.

        Parameters:
        - db: Database object.

        Returns:
        - int: The difference in days or None if there is no last event date.
        """
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date is not None:
            last_event_date = datetime.strptime(last_event_date, "%Y-%m-%d")
            current_date = datetime.now()
            difference = current_date - last_event_date
            return difference.days
        else:
            return None

    def get_days_to_complete_week(self, db):
        """
        Calculate the number of days left to complete the current week for a weekly habit.

        Parameters:
        - db: Database object.

        Returns:
        - int: The number of days left in the week or None if there is no last event date.
        """
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date is not None:
            last_event_date = datetime.strptime(last_event_date, "%Y-%m-%d")
            # monday = 1, tuesday = 2 ...
            day_of_week = last_event_date.weekday() + 1
            days_to_complete_week = 7 - day_of_week
            return days_to_complete_week
        else:
            return None

    def get_month_difference(self, db):
        """
        Calculate the number of days left to complete the current week for a weekly habit.

        Parameters:
        - db: Database object.

        Returns:
        - int: The number of days left in the week or None if there is no last event date.
        """
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date is not None:
            current_date = datetime.now().strftime("%Y-%m-%d")
            year1, month1, day1 = last_event_date.split('-')
            year2, month2, day2 = current_date.split('-')
            month1_int = int(month1)
            month2_int = int(month2)
            year1_int = int(year1)
            year2_int = int(year2)

            month_difference = (year2_int - year1_int) * 12 + (month2_int - month1_int)

            return month_difference
        else:
            return None

    def get_year_difference(self, db):
        """
        Calculate the difference in years between the last event date and the current date.

        Parameters:
        - db: Database object.

        Returns:
        - int: The difference in years or None if there is no last event date.
        """
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date is not None:
            last_event_date = datetime.strptime(last_event_date, "%Y-%m-%d")
            current_date = datetime.now()
            year_difference = current_date.year - last_event_date.year
            return year_difference
        else:
            return None
