"""
Module Database - Lưu trữ và quản lý dữ liệu
Thành viên 6 phụ trách
"""

import json
import os


class DataStorage:
    """Class quản lý lưu trữ dữ liệu"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, "students.json")
        self.activities_file = os.path.join(data_dir, "activities.json")
        self.scores_file = os.path.join(data_dir, "scores.json")
        
        # Tạo thư mục data nếu chưa tồn tại
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Đảm bảo thư mục data tồn tại"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_students(self, students: list) -> bool:
        """Lưu danh sách sinh viên"""
        # TODO: Thành viên 6 implement
        try:
            data = [self._student_to_dict(s) for s in students]
            with open(self.students_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi lưu sinh viên: {e}")
            return False
    
    def load_students(self) -> list:
        """Tải danh sách sinh viên"""
        # TODO: Thành viên 6 implement
        if not os.path.exists(self.students_file):
            return []
        try:
            with open(self.students_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi tải sinh viên: {e}")
            return []
    
    def save_activities(self, activities: list) -> bool:
        """Lưu danh sách hoạt động"""
        # TODO: Thành viên 6 implement
        pass
    
    def load_activities(self) -> list:
        """Tải danh sách hoạt động"""
        # TODO: Thành viên 6 implement
        pass
    
    def save_scores(self, scores: dict) -> bool:
        """Lưu điểm cộng"""
        # TODO: Thành viên 6 implement
        pass
    
    def load_scores(self) -> dict:
        """Tải điểm cộng"""
        # TODO: Thành viên 6 implement
        pass
    
    def backup_data(self, backup_name: str = None) -> bool:
        """Sao lưu dữ liệu"""
        # TODO: Thành viên 6 implement
        pass
    
    def restore_data(self, backup_name: str) -> bool:
        """Khôi phục dữ liệu từ bản sao lưu"""
        # TODO: Thành viên 6 implement
        pass
    
    def _student_to_dict(self, student) -> dict:
        """Chuyển đổi Student object thành dict"""
        return {
            "student_id": student.student_id,
            "name": student.name,
            "class_name": student.class_name,
            "bonus_points": student.bonus_points
        }
    
    def clear_all_data(self) -> bool:
        """Xóa tất cả dữ liệu (cẩn thận khi sử dụng)"""
        # TODO: Thành viên 6 implement
        pass
