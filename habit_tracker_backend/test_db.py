from db import get_db, add_habit, remove_habit, is_habit_exists
import pytest


class TestDB:

    def setup_method(self):
        self.db = get_db("tes.db")
        add_habit(self.db, "studying", "weekly", "Study for 60 minutes", "2023-02-15", 0)
        add_habit(self.db, "coding", "daily", "Code for 60 minutes", "2024-01-22", 0)
        add_habit(self.db, "exercise", "daily", "Exercise for 30 minutes", "2023-08-09", 0)
        add_habit(self.db, "swimming", "monthly", "Swim for 60 minutes", "2023-10-31", 0)
        add_habit(self.db, "Reading", "weekly", "Read for 2 hours", "2023-04-07", 0)
        add_habit(self.db, "Camping", "yearly", "Camp for 2 nights", "2023-11-18", 0)

