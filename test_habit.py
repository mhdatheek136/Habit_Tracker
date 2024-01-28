from datetime import datetime
from habit import Habit
import pytest
from freezegun import freeze_time
from db import *
import os


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")
        self.habit1 = Habit("driving", "daily", "Drive for 30 minutes")
        self.habit2 = Habit("reading", "weekly", "Code for 30 minutes")
        self.habit3 = Habit("swimming", "monthly", "Swim for 30 minutes")
        self.habit4 = Habit("camping", "yearly", "Camp for 30 minutes")

    def test_create(self):
        self.habit1.create(self.db)
        assert is_habit_exists(self.db, "driving") is True

    def test_delete(self):
        self.habit1.create(self.db)
        self.habit1.delete(self.db)
        assert is_habit_exists(self.db, "driving") is False

    def test_edit_name(self):
        self.habit1.create(self.db)
        self.habit1.edit_name(self.db, "biking")
        assert is_habit_exists(self.db, "biking") is True
        assert is_habit_exists(self.db, "driving") is False

    def test_edit_description(self):
        self.habit1.create(self.db)
        self.habit1.edit_description(self.db, "Drive for 1 hour")
        assert get_description(self.db, "driving") == "Drive for 1 hour"

    def test_change_periodicity(self):
        self.habit1.create(self.db)
        self.habit1.handle_streaks(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")
        self.habit1.change_periodicity(self.db, "weekly")
        assert get_periodicity(self.db, "driving") == "weekly"
        assert get_current_streak(self.db, "driving") == 0

    def test_add_event(self):
        self.habit1.create(self.db)
        self.habit1.add_event(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

    def test_handle_streak_when_last_event_date_none(self):
        self.habit1.create(self.db)
        self.habit1.handle_streaks(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

    def test_handle_streak_daily(self):
        frozen_date = datetime(2023, 12, 2)
        with freeze_time(frozen_date):
            self.habit1.create(self.db)
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 1
            assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 1
        frozen_date = datetime(2023, 12, 3)
        with freeze_time(frozen_date):
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 2
            assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")
        frozen_date = datetime(2023, 12, 5)
        with freeze_time(frozen_date):
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 1

    def test_handle_streak_weekly(self):
        frozen_date = datetime(2023, 12, 1)
        with freeze_time(frozen_date):
            self.habit2.create(self.db)
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1
            assert get_last_update_date(self.db, "reading") == datetime.now().strftime("%Y-%m-%d")
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1
        frozen_date = datetime(2023, 12, 3)
        with freeze_time(frozen_date):
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1
        frozen_date = datetime(2023, 12, 4)
        with freeze_time(frozen_date):
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 2
            assert get_last_update_date(self.db, "reading") == datetime.now().strftime("%Y-%m-%d")
        frozen_date = datetime(2023, 12, 22)
        with freeze_time(frozen_date):
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1

    def test_handle_streak_monthly(self):
        frozen_date = datetime(2023, 12, 4)
        with freeze_time(frozen_date):
            self.habit3.create(self.db)
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1
            assert get_last_update_date(self.db, "swimming") == datetime.now().strftime("%Y-%m-%d")
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1
        frozen_date = datetime(2023, 12, 27)
        with freeze_time(frozen_date):
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1
        frozen_date = datetime(2024, 1, 10)
        with freeze_time(frozen_date):
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 2
            assert get_last_update_date(self.db, "swimming") == datetime.now().strftime("%Y-%m-%d")
        frozen_date = datetime(2024, 3, 2)
        with freeze_time(frozen_date):
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1

    def test_handle_streaks_yearly(self):
        frozen_date = datetime(2023, 12, 4)
        with freeze_time(frozen_date):
            self.habit4.create(self.db)
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1
            assert get_last_update_date(self.db, "camping") == datetime.now().strftime("%Y-%m-%d")
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1
        frozen_date = datetime(2023, 12, 27)
        with freeze_time(frozen_date):
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1
        frozen_date = datetime(2024, 1, 10)
        with freeze_time(frozen_date):
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 2
            assert get_last_update_date(self.db, "camping") == datetime.now().strftime("%Y-%m-%d")
        frozen_date = datetime(2026, 3, 2)
        with freeze_time(frozen_date):
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1

    def teardown_method(self):
        self.db.close()
        os.remove("test.db")
