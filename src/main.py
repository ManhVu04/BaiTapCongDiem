"""
Hệ Thống Quản Lý Điểm Cộng
Main entry point của ứng dụng
"""

from student.student_manager import StudentManager
from activity.activity_manager import ActivityManager
from score.score_calculator import ScoreCalculator
from report.report_generator import ReportGenerator
from ui.menu import Menu
from database.data_storage import DataStorage


def main():
    """Hàm main khởi chạy ứng dụng"""
    print("=" * 50)
    print("   HỆ THỐNG QUẢN LÝ ĐIỂM CỘNG")
    print("=" * 50)
    
    # Khởi tạo các module
    database = DataStorage()
    student_manager = StudentManager(database)
    activity_manager = ActivityManager(database)
    score_calculator = ScoreCalculator(
        database,
        student_manager=student_manager,
        activity_manager=activity_manager
    )
    report_generator = ReportGenerator(database)
    
    # Khởi chạy giao diện menu
    menu = Menu(
        student_manager=student_manager,
        activity_manager=activity_manager,
        score_calculator=score_calculator,
        report_generator=report_generator
    )
    
    menu.run()


if __name__ == "__main__":
    main()
