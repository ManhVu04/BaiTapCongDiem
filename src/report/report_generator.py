"""
Report generation module.
"""

from datetime import datetime


class ReportGenerator:
    """Creates report texts for console display."""

    def __init__(self, database):
        self.database = database

    def generate_student_report(self, student_id: str) -> str:
        return f"""
========================================
        BAO CAO DIEM CONG SINH VIEN
========================================
Ma sinh vien: {student_id}
Ngay tao: {datetime.now().strftime('%d/%m/%Y %H:%M')}
----------------------------------------
Chi tiet hoat dong:
(Danh sach hoat dong se hien thi o day)
----------------------------------------
Tong diem cong: 0.0
========================================
        """

    def generate_class_report(self, class_name: str) -> str:
        return f"Bao cao lop '{class_name}' chua duoc trien khai."

    def generate_activity_report(self, activity_id: str) -> str:
        return f"Bao cao hoat dong '{activity_id}' chua duoc trien khai."

    def generate_summary_report(self) -> str:
        return "Bao cao tong hop chua duoc trien khai."

    def export_to_csv(self, report_type: str, filename: str) -> bool:
        # Placeholder: keep a stable return type until full report module is done.
        _ = report_type
        _ = filename
        return False

    def export_csv(self, filename: str) -> bool:
        """Compatibility wrapper used by the menu flow."""
        return self.export_to_csv("summary", filename)

    def get_top_students(self, limit: int = 10) -> list:
        _ = limit
        return []

    def get_statistics(self) -> dict:
        return {
            "total_students": 0,
            "total_activities": 0,
            "average_score": 0.0,
            "max_score": 0.0,
            "min_score": 0.0,
        }
