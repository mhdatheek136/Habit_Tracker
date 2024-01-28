from datetime import datetime
from habit import Habit
import pytest
from freezegun import freeze_time
from db import *
import os


class TestHabit:
    """
    Test suite for the Habit class and its associated methods.

    This suite covers the functionality of creating, editing, and handling streaks for habits in the system.
    """
    def setup_method(self):
        """
        Set up the necessary resources and instances before each test case.
        """
        self.db = get_db("test.db")
        self.habit1 = Habit("driving", "daily", "Drive for 30 minutes")
        self.habit2 = Habit("reading", "weekly", "Code for 30 minutes")
        self.habit3 = Habit("swimming", "monthly", "Swim for 30 minutes")
        self.habit4 = Habit("camping", "yearly", "Camp for 30 minutes")

    def test_create(self):
        """
        Test the creation of a habit and check if it exists in the database.

        This test case verifies that the 'create' method of the Habit class correctly adds a habit to the database.
        """
        self.habit1.create(self.db)
        assert is_habit_exists(self.db, "driving") is True

    def test_delete(self):
        """
        Test the deletion of a habit and check if it doesn't exist in the database.

        This test case verifies that the 'delete' method of the Habit class correctly removes a habit from the database.
        """
        self.habit1.create(self.db)
        self.habit1.delete(self.db)
        assert is_habit_exists(self.db, "driving") is False

    def test_edit_name(self):
        """
        Test editing the name of a habit and check if the changes are reflected in the database.

        This test case verifies that the 'edit_name' method of the Habit class correctly updates the name of a habit.
        """
        self.habit1.create(self.db)
        self.habit1.edit_name(self.db, "biking")
        assert is_habit_exists(self.db, "biking") is True
        assert is_habit_exists(self.db, "driving") is False

    def test_edit_description(self):
        """
        Test editing the description of a habit and check if the changes are reflected in the database.

        This test case verifies that the 'edit_description' method of the Habit class correctly updates the description.
        """
        self.habit1.create(self.db)
        self.habit1.edit_description(self.db, "Drive for 1 hour")
        assert get_description(self.db, "driving") == "Drive for 1 hour"

    def test_change_periodicity(self):
        """
        Test changing the periodicity of a habit and check if streaks are reset accordingly.

        This test case verifies that changing the periodicity resets streaks correctly using the 'change_periodicity' method.
        """
        self.habit1.create(self.db)
        self.habit1.handle_streaks(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")
        self.habit1.change_periodicity(self.db, "weekly")
        assert get_periodicity(self.db, "driving") == "weekly"
        assert get_current_streak(self.db, "driving") == 0

    def test_add_event(self):
        """
        Test adding an event to a habit and check if streaks are updated accordingly.

        This test case verifies that adding an event updates streaks correctly using the 'add_event' method.
        """
        self.habit1.create(self.db)
        self.habit1.add_event(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

    def test_handle_streak_when_last_event_date_none(self):
        """
        Test handling streaks when the last event date is None.

        This test case verifies that streaks are handled correctly when the last event date is None.
        """
        self.habit1.create(self.db)
        self.habit1.handle_streaks(self.db)
        assert get_current_streak(self.db, "driving") == 1
        assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

    def test_handle_streak_daily(self):
        """
        Test handling streaks for a daily habit with frozen time at different dates.

        This test case verifies that streaks are handled correctly for a daily habit with different frozen dates.

        Streaks for a daily habit should increase on consecutive days but not on the same day.
        If the streak is broken, it should reset to one.
        """
        frozen_date = datetime(2023, 12, 2)
        with freeze_time(frozen_date):
            self.habit1.create(self.db)
            self.habit1.handle_streaks(self.db)

            # Check that the current streak is 1 after the first handling
            assert get_current_streak(self.db, "driving") == 1
            assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

            # Handle streaks again on the same day, streak should not increase
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 1

        frozen_date = datetime(2023, 12, 3)
        with freeze_time(frozen_date):
            # Handle streaks on the next day, streak should increase to 2
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 2
            assert get_last_update_date(self.db, "driving") == datetime.now().strftime("%Y-%m-%d")

        # Move the frozen date to December 5, 2023 (skipping December 4, simulating a broken streak)
        frozen_date = datetime(2023, 12, 5)
        with freeze_time(frozen_date):
            # Handle streaks after a day of break, streak should reset to 1
            self.habit1.handle_streaks(self.db)
            assert get_current_streak(self.db, "driving") == 1

    def test_handle_streak_weekly(self):
        """
        Test handling streaks for a weekly habit with frozen time at different dates.

        This test case verifies that streaks are handled correctly for a weekly habit with different frozen dates.

         Streaks for a weekly habit should increase on consecutive weeks but not on the same week.
        If the streak is broken (more than a week between events), it should reset to one.
        """

        frozen_date = datetime(2023, 12, 1)

        with freeze_time(frozen_date):
            self.habit2.create(self.db)
            self.habit2.handle_streaks(self.db)

            # Check that the current streak is 1 after the first handling
            assert get_current_streak(self.db, "reading") == 1
            assert get_last_update_date(self.db, "reading") == datetime.now().strftime("%Y-%m-%d")

            # Handle streaks again on the same week, streak should not increase
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1

        # Move the frozen date to December 3 (Sunday), 2023 (still within the same week)
        frozen_date = datetime(2023, 12, 3)
        with freeze_time(frozen_date):
            # Handle streaks on the same week, streak should not increase
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1

        # Move the frozen date to December 4 (Monday), 2023 (next week)
        frozen_date = datetime(2023, 12, 4)
        with freeze_time(frozen_date):
            # Handle streaks on the next week, streak should increase to 2
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 2
            assert get_last_update_date(self.db, "reading") == datetime.now().strftime("%Y-%m-%d")
        # Move the frozen date to December 22, 2023 (skipped week)
        frozen_date = datetime(2023, 12, 22)
        with freeze_time(frozen_date):
            # Handle streaks after a week of break, streak should reset to 1
            self.habit2.handle_streaks(self.db)
            assert get_current_streak(self.db, "reading") == 1

    def test_handle_streak_monthly(self):
        """
        Test handling streaks for a monthly habit with frozen time at different dates.

        This test case verifies that streaks are handled correctly for a monthly habit with different frozen dates.

        Streaks for a monthly habit should increase on consecutive months but not on the same month.
        If the streak is broken (more than a month between events), it should reset to one.
        """
        frozen_date = datetime(2023, 12, 4)

        with freeze_time(frozen_date):
            self.habit3.create(self.db)
            self.habit3.handle_streaks(self.db)

            # Check that the current streak is 1 after the first handling
            assert get_current_streak(self.db, "swimming") == 1
            assert get_last_update_date(self.db, "swimming") == datetime.now().strftime("%Y-%m-%d")

            # Handle streaks again in the same month, streak should not increase
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1

        # Move the frozen date to December 27, 2023 (still within the same month)
        frozen_date = datetime(2023, 12, 27)
        with freeze_time(frozen_date):
            # Handle streaks in the same month, streak should not increase
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1

        # Move the frozen date to January 10, 2024 (next month)
        frozen_date = datetime(2024, 1, 10)
        with freeze_time(frozen_date):
            # Handle streaks on the next month, streak should increase to 2
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 2
            assert get_last_update_date(self.db, "swimming") == datetime.now().strftime("%Y-%m-%d")

        # Move the frozen date to March 2, 2024 (skipped February)
        frozen_date = datetime(2024, 3, 2)
        with freeze_time(frozen_date):
            # Handle streaks after a month of break, streak should reset to 1
            self.habit3.handle_streaks(self.db)
            assert get_current_streak(self.db, "swimming") == 1

    def test_handle_streaks_yearly(self):
        """
        Test handling streaks for a yearly habit with frozen time at different dates.

        This test case verifies that streaks are handled correctly for a yearly habit with different frozen dates.

        Streaks for a yearly habit should increase on consecutive years but not on the same year.
        If the streak is broken (more than a year between events), it should reset to one.
        """

        frozen_date = datetime(2023, 12, 4)
        with freeze_time(frozen_date):
            self.habit4.create(self.db)
            self.habit4.handle_streaks(self.db)

            # Check that the current streak is 1 after the first handling
            assert get_current_streak(self.db, "camping") == 1
            assert get_last_update_date(self.db, "camping") == datetime.now().strftime("%Y-%m-%d")

            # Handle streaks again in the same year, streak should not increase
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1

        # Move the frozen date to December 27, 2023 (still within the same year)
        frozen_date = datetime(2023, 12, 27)
        with freeze_time(frozen_date):
            # Handle streaks in the same year, streak should not increase
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1

        # Move the frozen date to January 10, 2024 (next year)
        frozen_date = datetime(2024, 1, 10)
        with freeze_time(frozen_date):
            self.habit4.handle_streaks(self.db)
            # Handle streaks on the next year, streak should increase to 2
            assert get_current_streak(self.db, "camping") == 2
            assert get_last_update_date(self.db, "camping") == datetime.now().strftime("%Y-%m-%d")

        # Move the frozen date to March 2, 2026 (skipped years)
        frozen_date = datetime(2026, 3, 2)
        with freeze_time(frozen_date):
            # Handle streaks after more than a year of break, streak should reset to 1
            self.habit4.handle_streaks(self.db)
            assert get_current_streak(self.db, "camping") == 1

    def teardown_method(self):
        """
        Clean up resources after each test case.

        Close the database connection and remove the test database file.
        """
        self.db.close()
        os.remove("test.db")