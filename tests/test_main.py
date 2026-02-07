"""
Tests cho Hệ Thống Quản Lý Điểm Cộng
"""

import unittest


class TestStudentManager(unittest.TestCase):
    """Test cases cho StudentManager"""
    
    def test_add_student(self):
        """Test thêm sinh viên"""
        # TODO: Viết test
        pass
    
    def test_remove_student(self):
        """Test xóa sinh viên"""
        # TODO: Viết test
        pass


class TestActivityManager(unittest.TestCase):
    """Test cases cho ActivityManager"""
    
    def test_create_activity(self):
        """Test tạo hoạt động"""
        # TODO: Viết test
        pass


class TestScoreCalculator(unittest.TestCase):
    """Test cases cho ScoreCalculator"""
    
    def test_calculate_score(self):
        """Test tính điểm"""
        # TODO: Viết test
        pass
    
    def test_max_score_limit(self):
        """Test giới hạn điểm tối đa"""
        # TODO: Viết test
        pass


if __name__ == "__main__":
    unittest.main()
