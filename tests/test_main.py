"""
Tests cho Hệ Thống Quản Lý Điểm Cộng
"""

from pathlib import Path
import tempfile
import unittest

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database.data_storage import DataStorage
from student.student_manager import StudentManager


class TestStudentManager(unittest.TestCase):
    """Test cases cho StudentManager"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = DataStorage(data_dir=self.temp_dir.name)
        self.manager = StudentManager(self.database)

    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_add_student(self):
        """Test thêm sinh viên"""
        student = self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.assertEqual(student.student_id, "SV001")
        self.assertEqual(student.name, "Nguyen Van A")
        self.assertEqual(student.class_name, "CTK44")
        self.assertEqual(len(self.manager.list_all_students()), 1)
        self.assertIsNotNone(self.manager.find_student("SV001"))
    
    def test_remove_student(self):
        """Test xóa sinh viên"""
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.assertTrue(self.manager.remove_student("SV001"))
        self.assertIsNone(self.manager.find_student("SV001"))
        self.assertFalse(self.manager.remove_student("SV001"))

    def test_prevent_duplicate_student_id(self):
        """Không cho phép thêm trùng mã sinh viên"""
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        with self.assertRaises(ValueError):
            self.manager.add_student("SV001", "Nguyen Van B", "CTK45")

    def test_update_student(self):
        """Test cập nhật thông tin sinh viên"""
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
        """Đảm bảo dữ liệu được nạp lại từ storage"""
        self.manager.add_student("SV001", "Nguyen Van A", "CTK44")
        self.manager.add_student("SV002", "Nguyen Van B", "CTK44")

        new_manager = StudentManager(self.database)
        students = new_manager.list_all_students()

        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].student_id, "SV001")
        self.assertEqual(students[1].student_id, "SV002")


@unittest.skip("Chua co test cho ActivityManager")
class TestActivityManager(unittest.TestCase):
    """Test cases cho ActivityManager"""
    
    def test_create_activity(self):
        """Test tạo hoạt động"""
        pass


@unittest.skip("Chua co test cho ScoreCalculator")
class TestScoreCalculator(unittest.TestCase):
    """Test cases cho ScoreCalculator"""
    
    def test_calculate_score(self):
        """Test tính điểm"""
        pass
    
    def test_max_score_limit(self):
        """Test giới hạn điểm tối đa"""
        pass


if __name__ == "__main__":
    unittest.main()
