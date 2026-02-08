"""
Tests for bonus score management system.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from activity.activity_manager import ActivityManager, ActivityType
from database.data_storage import DataStorage
from report.report_generator import ReportGenerator
from score.score_calculator import ScoreCalculator
from student.student_manager import StudentManager


class TestStudentManager(unittest.TestCase):
    """Unit tests for StudentManager."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = DataStorage(data_dir=self.temp_dir.name)
        self.manager = StudentManager(self.database)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_student(self):
        student = self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.assertEqual(student.student_id, "SV001")
        self.assertEqual(student.name, "Nguyen Van A")
        self.assertEqual(student.class_name, "CTK44")
        self.assertEqual(len(self.manager.list_all_students()), 1)
        self.assertIsNotNone(self.manager.find_student("SV001"))

    def test_remove_student(self):
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.assertTrue(self.manager.remove_student("SV001"))
        self.assertIsNone(self.manager.find_student("SV001"))
        self.assertFalse(self.manager.remove_student("SV001"))

    def test_prevent_duplicate_student_id(self):
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        with self.assertRaises(ValueError):
            self.manager.add_student("SV001", "Nguyen Van B", "CTK45")

    def test_update_student(self):
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        updated = self.manager.update_student(
            "SV001", name="Tran Van A", class_name="CTK45", bonus_points=1.5
        )
        self.assertTrue(updated)
        student = self.manager.find_student("SV001")
        self.assertEqual(student.name, "Tran Van A")
        self.assertEqual(student.class_name, "CTK45")
        self.assertEqual(student.bonus_points, 1.5)

    def test_load_students_from_storage(self):
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.manager.add_student("SV002", "Nguyen Van B", "CTK44")

        new_manager = StudentManager(self.database)
        students = new_manager.list_all_students()

        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].student_id, "SV001")
        self.assertEqual(students[1].student_id, "SV002")


class TestActivityManager(unittest.TestCase):
    """Unit tests for ActivityManager."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = DataStorage(data_dir=self.temp_dir.name)
        self.manager = ActivityManager(self.database)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_activity_and_reload(self):
        activity = self.manager.create_activity(
            "HD001", "Mua he xanh", ActivityType.VOLUNTEER, 0.75
        )
        self.assertEqual(activity.activity_id, "HD001")
        self.assertEqual(activity.name, "Mua he xanh")
        self.assertEqual(activity.points, 0.75)

        reloaded_manager = ActivityManager(self.database)
        reloaded_activity = reloaded_manager.find_activity("HD001")
        self.assertIsNotNone(reloaded_activity)
        self.assertEqual(reloaded_activity.activity_type, ActivityType.VOLUNTEER)
        self.assertEqual(reloaded_activity.points, 0.75)

    def test_add_participant(self):
        self.manager.create_activity("HD001", "Seminar", ActivityType.ACADEMIC, 0.5)
        self.assertTrue(self.manager.add_participant("HD001", "SV001"))
        self.assertFalse(self.manager.add_participant("HD001", "SV001"))

        reloaded_manager = ActivityManager(self.database)
        activity = reloaded_manager.find_activity("HD001")
        self.assertIn("SV001", activity.participants)


class TestScoreCalculator(unittest.TestCase):
    """Unit tests for ScoreCalculator."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = DataStorage(data_dir=self.temp_dir.name)
        self.student_manager = StudentManager(self.database)
        self.activity_manager = ActivityManager(self.database)
        self.score_calculator = ScoreCalculator(
            self.database,
            student_manager=self.student_manager,
            activity_manager=self.activity_manager,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_calculate_score_with_cap(self):
        self.student_manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.activity_manager.create_activity("HD001", "A", ActivityType.ACADEMIC, 1.2)
        self.activity_manager.create_activity("HD002", "B", ActivityType.SPORT, 1.1)
        self.activity_manager.add_participant("HD001", "SV001")
        self.activity_manager.add_participant("HD002", "SV001")

        score = self.score_calculator.calculate_student_score("SV001")
        self.assertEqual(score, 2.0)
        self.assertEqual(self.score_calculator.calculate_activity_score("HD001", "SV001"), 1.2)

    def test_update_all_scores_persisted(self):
        self.student_manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.activity_manager.create_activity("HD001", "A", ActivityType.ACADEMIC, 0.9)
        self.activity_manager.add_participant("HD001", "SV001")

        self.assertTrue(self.score_calculator.update_all_scores())

        reloaded_manager = StudentManager(self.database)
        student = reloaded_manager.find_student("SV001")
        self.assertIsNotNone(student)
        self.assertEqual(student.bonus_points, 0.9)

    def test_validate_score(self):
        self.assertTrue(self.score_calculator.validate_score(0.0))
        self.assertTrue(self.score_calculator.validate_score(2.0))
        self.assertFalse(self.score_calculator.validate_score(-0.1))
        self.assertFalse(self.score_calculator.validate_score(2.1))


class TestReportGenerator(unittest.TestCase):
    """Unit tests for ReportGenerator."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = DataStorage(data_dir=self.temp_dir.name)
        self.report_generator = ReportGenerator(self.database)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_export_csv_alias(self):
        self.assertFalse(self.report_generator.export_csv("report.csv"))

    def test_generate_report_defaults(self):
        self.assertIsInstance(self.report_generator.generate_student_report("SV001"), str)
        self.assertIsInstance(self.report_generator.generate_class_report("CTK44"), str)
        self.assertIsInstance(self.report_generator.generate_summary_report(), str)


if __name__ == "__main__":
    unittest.main()
