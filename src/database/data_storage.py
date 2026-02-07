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
        try:
            data = [self._activity_to_dict(a) for a in activities]
            with open(self.activities_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi lưu hoạt động: {e}")
            return False
    
    def load_activities(self) -> list:
        """Tải danh sách hoạt động"""
        if not os.path.exists(self.activities_file):
            return []
        try:
            with open(self.activities_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi tải hoạt động: {e}")
            return []
    
    def save_scores(self, scores: dict) -> bool:
        """Lưu điểm cộng"""
        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi lưu điểm: {e}")
            return False
    
    def load_scores(self) -> dict:
        """Tải điểm cộng"""
        if not os.path.exists(self.scores_file):
            return {}
        try:
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi tải điểm: {e}")
            return {}
    
    def backup_data(self, backup_name: str = None) -> bool:
        """Sao lưu dữ liệu"""
        import shutil
        from datetime import datetime
        
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            if backup_name is None:
                backup_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_path = os.path.join(backup_dir, backup_name)
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            
            # Sao lưu các file dữ liệu
            if os.path.exists(self.students_file):
                shutil.copy(self.students_file, os.path.join(backup_path, "students.json"))
            if os.path.exists(self.activities_file):
                shutil.copy(self.activities_file, os.path.join(backup_path, "activities.json"))
            if os.path.exists(self.scores_file):
                shutil.copy(self.scores_file, os.path.join(backup_path, "scores.json"))
            
            return True
        except Exception as e:
            print(f"Lỗi sao lưu dữ liệu: {e}")
            return False
    
    def restore_data(self, backup_name: str) -> bool:
        """Khôi phục dữ liệu từ bản sao lưu"""
        import shutil
        
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            backup_path = os.path.join(backup_dir, backup_name)
            
            if not os.path.exists(backup_path):
                print(f"Bản sao lưu '{backup_name}' không tồn tại")
                return False
            
            # Khôi phục các file dữ liệu
            backup_students = os.path.join(backup_path, "students.json")
            if os.path.exists(backup_students):
                shutil.copy(backup_students, self.students_file)
            
            backup_activities = os.path.join(backup_path, "activities.json")
            if os.path.exists(backup_activities):
                shutil.copy(backup_activities, self.activities_file)
            
            backup_scores = os.path.join(backup_path, "scores.json")
            if os.path.exists(backup_scores):
                shutil.copy(backup_scores, self.scores_file)
            
            return True
        except Exception as e:
            print(f"Lỗi khôi phục dữ liệu: {e}")
            return False
    
    def _student_to_dict(self, student) -> dict:
        """Chuyển đổi Student object thành dict"""
        return {
            "student_id": student.student_id,
            "name": student.name,
            "class_name": student.class_name,
            "bonus_points": student.bonus_points
        }
    
    def _activity_to_dict(self, activity) -> dict:
        """Chuyển đổi Activity object thành dict"""
        return {
            "activity_id": activity.activity_id,
            "activity_name": activity.activity_name,
            "bonus_points": activity.bonus_points,
            "description": activity.description
        }
    
    def clear_all_data(self) -> bool:
        """Xóa tất cả dữ liệu (cẩn thận khi sử dụng)"""
        try:
            if os.path.exists(self.students_file):
                os.remove(self.students_file)
            if os.path.exists(self.activities_file):
                os.remove(self.activities_file)
            if os.path.exists(self.scores_file):
                os.remove(self.scores_file)
            return True
        except Exception as e:
            print(f"Lỗi xóa dữ liệu: {e}")
            return False
