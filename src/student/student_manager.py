"""
Module Student - Quản lý thông tin sinh viên
Thành viên 1 phụ trách
"""

from typing import Optional


class Student:
    """Class đại diện cho một sinh viên"""
    
    def __init__(self, student_id: str, name: str, class_name: str):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.bonus_points = 0.0
    
    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.class_name})"


class StudentManager:
    """Class quản lý danh sách sinh viên"""
    
    def __init__(self, database):
        self.database = database
        self.students = []
        self._load_from_storage()

    def _load_from_storage(self):
        """Nạp danh sách sinh viên từ nguồn lưu trữ"""
        if self.database is None:
            return

        loaded_students = self.database.load_students()
        if not isinstance(loaded_students, list):
            return

        for item in loaded_students:
            if isinstance(item, Student):
                self.students.append(item)
                continue

            if not isinstance(item, dict):
                continue

            student_id = str(item.get("student_id", "")).strip()
            name = str(item.get("name", "")).strip()
            class_name = str(item.get("class_name", "")).strip()
            if not student_id or not name or not class_name:
                continue

            student = Student(student_id, name, class_name)
            try:
                student.bonus_points = float(item.get("bonus_points", 0.0))
            except (TypeError, ValueError):
                student.bonus_points = 0.0
            self.students.append(student)

    def _save_to_storage(self):
        """Lưu danh sách sinh viên vào nguồn lưu trữ"""
        if self.database is None:
            return False
        return self.database.save_students(self.students)
    
    def add_student(self, student_id: str, name: str, class_name: str) -> Student:
        """Thêm sinh viên mới"""
        student_id = student_id.strip()
        name = name.strip()
        class_name = class_name.strip()

        if not student_id or not name or not class_name:
            raise ValueError("Thông tin sinh viên không được để trống")

        if self.find_student(student_id) is not None:
            raise ValueError(f"Mã sinh viên '{student_id}' đã tồn tại")

        student = Student(student_id, name, class_name)
        self.students.append(student)
        self._save_to_storage()
        return student
    
    def remove_student(self, student_id: str) -> bool:
        """Xóa sinh viên theo mã số"""
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print(f"Đã xóa sinh viên: {student}")
                return True
        return False
    
    def find_student(self, student_id: str) -> Optional[Student]:
        """Tìm sinh viên theo mã số"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def list_all_students(self) -> list:
        """Liệt kê tất cả sinh viên"""
        return list(self.students)
    
    def update_student(self, student_id: str, **kwargs) -> bool:
        """Cập nhật thông tin sinh viên"""
        student = self.find_student(student_id)
        if student:
            if 'name' in kwargs:
                student.name = kwargs['name']
            if 'class_name' in kwargs:
                student.class_name = kwargs['class_name']
            if 'bonus_points' in kwargs:
                student.bonus_points = kwargs['bonus_points']
            print(f"Đã cập nhật sinh viên: {student}")
            return True
        return False
