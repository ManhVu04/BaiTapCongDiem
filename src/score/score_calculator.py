"""
Module Score - Tính toán điểm cộng
Thành viên 3 phụ trách
"""


class ScoreCalculator:
    """Class tính toán điểm cộng cho sinh viên"""
    
    def __init__(self, database, student_manager=None, activity_manager=None):
        self.database = database
        self.student_manager = student_manager
        self.activity_manager = activity_manager
        self.max_bonus_points = 2.0  # Điểm cộng tối đa
    
    def calculate_student_score(self, student_id: str) -> float:
        """Tính tổng điểm cộng của sinh viên"""
        total_score = 0.0
        
        # Sử dụng activity_manager được truyền vào hoặc tạo mới
        if self.activity_manager is not None:
            activities = self.activity_manager.list_activities()
        else:
            from ..activity.activity_manager import ActivityManager
            activity_manager = ActivityManager(self.database)
            activities = activity_manager.list_activities()
        
        # Tính tổng điểm từ các hoạt động sinh viên tham gia
        for activity in activities:
            if student_id in activity.participants:
                total_score += activity.points
        
        # Áp dụng các quy tắc tính điểm
        final_score = self.apply_bonus_rules(total_score)
        return final_score
    
    def calculate_activity_score(self, activity_id: str, student_id: str) -> float:
        """Tính điểm cộng từ một hoạt động"""
        # Sử dụng activity_manager được truyền vào hoặc tầo mới
        if self.activity_manager is not None:
            activities = self.activity_manager.list_activities()
        else:
            from ..activity.activity_manager import ActivityManager
            activity_manager = ActivityManager(self.database)
            activities = activity_manager.list_activities()
        
        # Tìm hoạt động theo ID
        for activity in activities:
            if activity.activity_id == activity_id:
                # Kiểm tra sinh viên có tham gia không
                if student_id in activity.participants:
                    return activity.points
                else:
                    return 0.0
        
        # Không tìm thấy hoạt động
        return 0.0
    
    def apply_bonus_rules(self, raw_score: float) -> float:
        """Áp dụng các quy tắc tính điểm cộng"""
        # Giới hạn điểm cộng tối đa
        if raw_score > self.max_bonus_points:
            return self.max_bonus_points
        
        # Đảm bảo điểm không âm
        if raw_score < 0:
            return 0.0
        
        # Làm tròn đến 2 chữ số thập phân
        return round(raw_score, 2)
    
    def get_score_breakdown(self, student_id: str) -> dict:
        """Lấy chi tiết điểm cộng của sinh viên"""
        # Sử dụng activity_manager được truyền vào hoặc tạo mới
        if self.activity_manager is not None:
            activities = self.activity_manager.list_activities()
        else:
            from ..activity.activity_manager import ActivityManager
            activity_manager = ActivityManager(self.database)
            activities = activity_manager.list_activities()
        
        breakdown = {
            'student_id': student_id,
            'activities': [],
            'total_raw_score': 0.0,
            'final_score': 0.0
        }
        
        # Thu thập thông tin các hoạt động sinh viên tham gia
        for activity in activities:
            if student_id in activity.participants:
                activity_info = {
                    'activity_id': activity.activity_id,
                    'name': activity.name,
                    'type': activity.activity_type.value,
                    'points': activity.points,
                    'date': activity.date.strftime('%Y-%m-%d') if activity.date else 'N/A'
                }
                breakdown['activities'].append(activity_info)
                breakdown['total_raw_score'] += activity.points
        
        # Áp dụng quy tắc tính điểm
        breakdown['final_score'] = self.apply_bonus_rules(breakdown['total_raw_score'])
        breakdown['total_raw_score'] = round(breakdown['total_raw_score'], 2)
        
        return breakdown
    
    def update_all_scores(self) -> bool:
        """Cập nhật điểm cộng cho tất cả sinh viên"""
        try:
            # Sử dụng student_manager được truyền vào hoặc tạo mới
            if self.student_manager is not None:
                students = self.student_manager.list_all_students()
            else:
                from ..student.student_manager import StudentManager
                student_manager = StudentManager(self.database)
                students = student_manager.list_all_students()
            
            # Cập nhật điểm cho từng sinh viên
            for student in students:
                new_score = self.calculate_student_score(student.student_id)
                student.bonus_points = new_score
            
            # Lưu vào database
            self.database.save_students(students)
            print(f"Đã cập nhật điểm cho {len(students)} sinh viên")
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật điểm: {e}")
            return False
    
    def validate_score(self, score: float) -> bool:
        """Kiểm tra điểm hợp lệ"""
        return 0 <= score <= self.max_bonus_points
