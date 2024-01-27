from datetime import datetime
from monthdelta import monthdelta
from db import *



class Habit:

    def __init__(self, name: str = None, periodicity: str = None, description: str = None):
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
        self.streak = 0

    def create(self, db):
        if is_habit_exists(db, self.name) is False:
            add_habit(db, self.name, self.periodicity, self.description, self.creation_date, self.streak)
            update_log(db, self.name, 0, self.creation_date)
            print(f"\nNew habit '{self.name.capitalize()}' is created successfully.\n")
        else:
            print("\nHabit name typed is already taken. Try new habit name.\n")
        return

    def delete(self, db):
        remove_habit(db, self.name)
        print(f"\nHabit'{self.name.capitalize()}' is deleted successfully.\n")

    def edit_name(self, db, new_name):
        if is_habit_exists(db, new_name) is False:
            update_habit_name(db, self.name, new_name)
            print(f"\nHabit name is changed successfully.\n")
        else:
            print("\nHabit name typed is already taken. Try new habit name.\n")
        return

    def edit_description(self, db, new_description):
        update_description(db, self.name, new_description)
        print(f"\nDescription changed successfully.\n")
        return

    def change_periodicity(self, db, new_periodicity):
        update_periodicity(db, self.name, new_periodicity)
        reset_streak(db, self.name)
        print(f"\nPeriodicity for  '{self.name.capitalize()}' is changed to '{new_periodicity}'.\n")
        return

    def increment_streak(self, db):
        self.streak = get_current_streak(db, self.name)
        self.streak += 1
        print(f"\nYour current streak for the habit  '{self.name.capitalize()}' is '{self.streak}'.\n")
        return

    def add_event(self, db):
        self.increment_streak(db)
        current_date = datetime.now().strftime("%Y-%m-%d")
        update_log(db, self.name, self.streak, current_date)
        update_streak(db, self.name, self.streak)
        return


    def handle_streaks(self, db):
        last_event_date = get_last_update_date(db, self.name)
        if get_periodicity(db, self.name) == "daily":
            if self.get_day_difference(db) == 0:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' today. You can check-in again tomorrow.\n")
            elif self.get_day_difference(db) == 1 or last_event_date is None:
                self.add_event(db)
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for habit '{self.name.capitalize()}' is 1.\n")

        elif get_periodicity(db, self.name) == "weekly":
            days_to_complete_week = self.get_days_to_complete_week(db)
            day_difference = self.get_day_difference(db)
            next_possible_day = days_to_complete_week - day_difference + 1
            if days_to_complete_week > day_difference:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' for this week. You can check-in again in '{next_possible_day}' days.\n")
            elif (days_to_complete_week < day_difference <= days_to_complete_week + 7) or last_event_date is None:
                self.add_event(db)
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for habit '{self.name.capitalize()}' is 1.\n")

        elif get_periodicity(db, self.name) == "monthly":
            if self.get_month_difference(db) == 0:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' for this month. You can check-in again next month.\n")
            elif self.get_month_difference(db) == 1 or last_event_date is None:
                self.add_event(db)
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for habit '{self.name.capitalize()}' is 1.\n")

        elif get_periodicity(db, self.name) == "yearly":
            if self.get_year_difference(db) == 0:
                print(f"\nYou have already checked the habit '{self.name.capitalize()}' for this month. You can check-in again next month.\n")
            elif self.get_year_difference(db) == 1 or last_event_date is None:
                self.add_event(db)
            else:
                update_streak(db, self.name, 1)
                print(f"\nYour previous streak is broken. Here we go again. Current Streak for habit '{self.name.capitalize()}' is 1.\n")


    def get_day_difference(self, db):
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date:
            current_date = datetime.now()
            difference = current_date - last_event_date
            return difference.days
        else:
            return None

    def get_days_to_complete_week(self, db):
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date:
            current_date = datetime.now()
            # monday = 1, tuesday = 2 ...
            day_of_week = current_date.weekday() + 1
            days_to_complete_week = 7 - day_of_week
            return days_to_complete_week
        else:
            return None

    def get_month_difference(self, db):
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date:
            current_date = datetime.now()
            difference = current_date - last_event_date
            month_difference = monthdelta(difference)
            return month_difference
        else:
            return None

    def get_year_difference(self, db):
        last_event_date = get_last_update_date(db, self.name)
        if last_event_date:
            current_date = datetime.now()
            year_difference = current_date.year - last_event_date.year
            return year_difference
        else:
            return None








