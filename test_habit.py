from habit import Habit
import pytest
from freezegun import freeze_time
from db import *
import os


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")
        self.habit = Habit("driving", "daily", "Drive for 30 minutes")

        add_habit(self.db, "coding", "daily", "Code for 60 minutes", "2023-12-01", 1)
        add_habit(self.db, "exercise", "daily", "Exercise for 30 minutes", "2023-12-01", 0)
        add_habit(self.db, "studying", "weekly", "Study for 60 minutes", "2023-12-01", 0)
        add_habit(self.db, "reading", "weekly", "Read for 2 hours", "2023-12-01", 1)
        add_habit(self.db, "swimming", "monthly", "Swim for 60 minutes", "2023-12-01", 1)
        add_habit(self.db, "camping", "yearly", "Camp for 2 nights", "2023-12-01", 1)

        update_log(self.db, "coding", 1, "2023-12-02")
        update_log(self.db, "reading", 1, "2023-12-04")
        update_log(self.db, "swimming", 1, "2023-12-06")
        update_log(self.db, "camping", 1, "2023-12-08")

    def test_create(self):
        self.habit.create(self.db)
        assert is_habit_exists(self.db, "driving") is True

    def test_delete(self):
        self.habit.create(self.db)
        self.habit.delete(self.db)
        assert is_habit_exists(self.db, "driving") is False

    def test_edit_name(self):
        self.habit.create(self.db)
        self.habit.edit_name(self.db, "biking")
        assert is_habit_exists(self.db, "biking") is True
        assert is_habit_exists(self.db, "driving") is False

    def test_edit_description(self):
        self.habit.create(self.db)
        self.habit.edit_description(self.db, "Drive for 1 hour")
        assert get_description(self.db, "driving") == "Drive for 1 hour"

    def test_change_periodicity(self):
        self.habit.create(self.db)
        self.habit.change_periodicity(self.db, "weekly")
        assert get_periodicity(self.db, "driving") == "weekly"

    def test_add_event(self):
        self.habit.create(self.db)
        self.habit.add_event(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

    def test_handle_streak_when_last_event_date_None(self):
        self.habit.create(self.db)




    def teardown_method(self):
        self.db.close()
        os.remove("test.db")