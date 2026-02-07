"""
Module Activity - Quản lý hoạt động và sự kiện
Thành viên 2 phụ trách
"""

from datetime import datetime
from enum import Enum


class ActivityType(Enum):
    """Loại hoạt động"""
    VOLUNTEER = "Tình nguyện"
    ACADEMIC = "Học thuật"
    SPORT = "Thể thao"
    CULTURE = "Văn hóa"
    OTHER = "Khác"


class Activity:
    """Class đại diện cho một hoạt động"""
    
    def __init__(self, activity_id: str, name: str, activity_type: ActivityType, 
                 points: float, date: datetime = None):
        self.activity_id = activity_id
        self.name = name
        self.activity_type = activity_type
        self.points = points
        self.date = date or datetime.now()
        self.participants = []
    
    def __str__(self):
        return f"{self.activity_id} - {self.name} ({self.activity_type.value}) - {self.points} điểm"


class ActivityManager:
    """Class quản lý danh sách hoạt động"""
    
    def __init__(self, database):
        self.database = database
        self.activities = []
    
    def create_activity(self, activity_id: str, name: str, 
                        activity_type: ActivityType, points: float) -> Activity:
        """Tạo hoạt động mới"""
        # TODO: Thành viên 2 implement
        activity = Activity(activity_id, name, activity_type, points)
        self.activities.append(activity)
        print(f"Đã tạo hoạt động: {activity}")
        return activity
    
    def delete_activity(self, activity_id: str) -> bool:
        """Xóa hoạt động"""
        for activity in self.activities:
            if activity.activity_id == activity_id:
                self.activities.remove(activity)
                print(f"Đã xóa hoạt động: {activity}")
                return True
        print(f"Không tìm thấy hoạt động với ID: {activity_id}")
        return False
    
    def add_participant(self, activity_id: str, student_id: str) -> bool:
        """Thêm sinh viên tham gia hoạt động"""
        for activity in self.activities:
            if activity.activity_id == activity_id:
                if student_id not in activity.participants:
                    activity.participants.append(student_id)
                    print(f"Đã thêm sinh viên {student_id} vào hoạt động {activity_id}")
                    return True
                else:
                    print(f"Sinh viên {student_id} đã tham gia hoạt động {activity_id}")
                    return False
        print(f"Không tìm thấy hoạt động với ID: {activity_id}")
        return False
    
    def remove_participant(self, activity_id: str, student_id: str) -> bool:
        """Xóa sinh viên khỏi hoạt động"""
        for activity in self.activities:
            if activity.activity_id == activity_id:
                if student_id in activity.participants:
                    activity.participants.remove(student_id)
                    print(f"Đã xóa sinh viên {student_id} khỏi hoạt động {activity_id}")
                    return True
                else:
                    print(f"Sinh viên {student_id} không tham gia hoạt động {activity_id}")
                    return False
        print(f"Không tìm thấy hoạt động với ID: {activity_id}")
        return False
    
    def list_activities(self) -> list:
        """Liệt kê tất cả hoạt động"""
        # TODO: Thành viên 2 implement
        return self.activities
    
    def get_activities_by_type(self, activity_type: ActivityType) -> list:
        """Lấy hoạt động theo loại"""
        return [activity for activity in self.activities if activity.activity_type == activity_type]
