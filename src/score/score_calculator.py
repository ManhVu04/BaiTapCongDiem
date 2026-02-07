"""
Module Score - Tính toán điểm cộng
Thành viên 3 phụ trách
"""


class ScoreCalculator:
    """Class tính toán điểm cộng cho sinh viên"""
    
    def __init__(self, database):
        self.database = database
        self.max_bonus_points = 2.0  # Điểm cộng tối đa
    
    def calculate_student_score(self, student_id: str) -> float:
        """Tính tổng điểm cộng của sinh viên"""
        # TODO: Thành viên 3 implement
        pass
    
    def calculate_activity_score(self, activity_id: str, student_id: str) -> float:
        """Tính điểm cộng từ một hoạt động"""
        # TODO: Thành viên 3 implement
        pass
    
    def apply_bonus_rules(self, raw_score: float) -> float:
        """Áp dụng các quy tắc tính điểm cộng"""
        # TODO: Thành viên 3 implement
        # Ví dụ: giới hạn điểm cộng tối đa
        if raw_score > self.max_bonus_points:
            return self.max_bonus_points
        return raw_score
    
    def get_score_breakdown(self, student_id: str) -> dict:
        """Lấy chi tiết điểm cộng của sinh viên"""
        # TODO: Thành viên 3 implement
        pass
    
    def update_all_scores(self) -> bool:
        """Cập nhật điểm cộng cho tất cả sinh viên"""
        # TODO: Thành viên 3 implement
        pass
    
    def validate_score(self, score: float) -> bool:
        """Kiểm tra điểm hợp lệ"""
        # TODO: Thành viên 3 implement
        return 0 <= score <= self.max_bonus_points
