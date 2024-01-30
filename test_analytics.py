from datetime import datetime
from analytics import *
import textwrap
import pytest
from freezegun import freeze_time
from db import *
import os


class TestAnalytics:

    def setup_method(self):
        """
        Set up the test environment by creating a test database and adding sample data.
        """
        self.db = get_db("test.db")
        add_habit(self.db, "studying", "weekly", "Study for 60 minutes", "2023-01-15", 1)
        add_habit(self.db, "coding", "daily", "Code for 60 minutes", "2023-01-22", 3)
        add_habit(self.db, "exercise", "daily", "Exercise for 30 minutes", "2023-03-09", 0)
        add_habit(self.db, "swimming", "monthly", "Swim for 60 minutes", "2023-07-20", 2)
        add_habit(self.db, "reading", "weekly", "Read for 2 hours", "2023-10-07", 0)
        add_habit(self.db, "camping", "yearly", "Camp for 2 nights", "2023-11-18", 1)

        update_log(self.db, "studying", 1, "2023-01-15")
        update_log(self.db, "studying", 2, "2023-01-22")
        update_log(self.db, "coding", 1, "2023-01-23")
        update_log(self.db, "coding", 2, "2023-01-24")
        update_log(self.db, "coding", 3, "2023-01-25")
        update_log(self.db, "studying", 3, "2023-01-29")
        update_log(self.db, "studying", 4, "2023-02-05")
        update_log(self.db, "studying", 1, "2023-03-05")
        update_log(self.db, "swimming", 1, "2023-07-20")
        update_log(self.db, "swimming", 2, "2023-08-10")
        update_log(self.db, "camping", 1, "2023-11-19")

    def test_get_all_habits_info(self):
        """
        Test the function get_all_habits_info from the analytics module.
        """
        assert len(get_all_habits_info(self.db)) == 7

    def test_get_all_habits(self):
        """
        Test the function get_all_habits from the analytics module.
        """
        assert len(get_all_habits(self.db)) == 7

    def test_get_all_habits_based_on_periodicity(self):
        """
        Test the function get_all_habits_based_on_periodicity from the analytics module.
        """
        assert len(get_all_habits_based_on_periodicity(self.db, "daily")) == 3
        assert len(get_all_habits_based_on_periodicity(self.db, "weekly")) == 3
        assert len(get_all_habits_based_on_periodicity(self.db, "monthly")) == 2
        assert len(get_all_habits_based_on_periodicity(self.db, "yearly")) == 2

    def test_get_data_of_single_habit(self):
        """
        Test the function get_data_of_single_habit from the analytics module.
        """
        assert len(get_data_of_single_habit(self.db, "coding")) == 2

    def test_get_longest_streak_for_given_habit(self):
        """
        Test the function get_longest_streak_for_given_habit from the analytics module.
        """
        assert len(get_longest_streak_for_given_habit(self.db, "studying")) == 2
        assert get_longest_streak_for_given_habit(self.db, "studying")[1][0] == 4

    def test_get_longest_streaks_of_all_habits(self):
        """
        Test the function get_longest_streaks_of_all_habits from the analytics module.
        """
        assert len(get_longest_streaks_of_all_habits(self.db)) == 5

    def test_get_event_logs_by_habit(self):
        """
        Test the function get_event_logs_by_habit from the analytics module.
        """
        assert len(get_event_logs_by_habit(self.db, "studying")) == 6

    def test_print_tabular(self, capfd):
        """
        Test the function print_tabular from the analytics module.
        """
        records = get_all_habits_info(self.db)
        print_tabular(records, self.db)
        captured = capfd.readouterr()
        expected_output = textwrap.dedent("""\
            +----------+-------------+-------------------------+---------------+----------------+
            |  Habit   | Periodicity |       Description       | Creation Date | Current Streak |
            +----------+-------------+-------------------------+---------------+----------------+
            | studying |    weekly   |   Study for 60 minutes  |   2023-01-15  |       1        |
            |  coding  |    daily    |   Code for 60 minutes   |   2023-01-22  |       3        |
            | exercise |    daily    | Exercise for 30 minutes |   2023-03-09  |       0        |
            | swimming |   monthly   |   Swim for 60 minutes   |   2023-07-20  |       2        |
            | reading  |    weekly   |     Read for 2 hours    |   2023-10-07  |       0        |
            | camping  |    yearly   |    Camp for 2 nights    |   2023-11-18  |       1        |
            +----------+-------------+-------------------------+---------------+----------------+
        """)
        assert captured.out == expected_output
    def teardown_method(self):
        """
        Clean up resources after each test case.

        Close the database connection and remove the test database file.
        """
        self.db.close()
        os.remove("test.db")
