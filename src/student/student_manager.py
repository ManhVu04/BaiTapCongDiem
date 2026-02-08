"""
Module Student - Quản lý thông tin sinh viên
Thành viên 1 phụ trách
"""


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
    
    def add_student(self, student_id: str, name: str, class_name: str) -> Student:
        """Thêm sinh viên mới"""
        # TODO: Thành viên 1 implement
        student = Student(student_id, name, class_name)
        self.students.append(student)
        print(f"Đã thêm sinh viên: {student}")
        return student
    
    def remove_student(self, student_id: str) -> bool:
        """Xóa sinh viên theo mã số"""
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print(f"Đã xóa sinh viên: {student}")
                return True
        return False
    
    def find_student(self, student_id: str) -> Student:
        """Tìm sinh viên theo mã số"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def list_all_students(self) -> list:
        """Liệt kê tất cả sinh viên"""
        # TODO: Thành viên 1 implement
        return self.students
    
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
