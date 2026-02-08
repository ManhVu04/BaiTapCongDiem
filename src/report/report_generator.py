"""
Module Report - Tạo báo cáo và thống kê
Thành viên 4 phụ trách
"""

import csv
import os
import json
from datetime import datetime


class ReportGenerator:
    """Class tạo báo cáo thống kê"""
    
    def __init__(self, database, student_manager=None, activity_manager=None, score_calculator=None):
        self.database = database
        self.student_manager = student_manager
        self.activity_manager = activity_manager
        self.score_calculator = score_calculator
    
    def generate_student_report(self, student_id: str) -> str:
        """Tạo báo cáo cho một sinh viên"""
        student = None
        activities_list = []
        total_score = 0.0
        
        # Tìm sinh viên
        if self.student_manager:
            student = self.student_manager.find_student(student_id)
        
        # Lấy danh sách hoạt động sinh viên tham gia
        if self.activity_manager:
            for activity in self.activity_manager.list_activities():
                if student_id in activity.participants:
                    activities_list.append(activity)
                    total_score += activity.points
        
        # Tính điểm cuối cùng (giới hạn tối đa 2.0)
        if self.score_calculator:
            total_score = self.score_calculator.apply_bonus_rules(total_score)
        else:
            total_score = min(total_score, 2.0)
        
        # Tạo báo cáo
        student_name = student.name if student else "Không tìm thấy"
        student_class = student.class_name if student else "N/A"
        
        activities_str = ""
        if activities_list:
            for act in activities_list:
                activities_str += f"  - {act.name} ({act.activity_type.value}): {act.points} điểm\n"
        else:
            activities_str = "  (Chưa tham gia hoạt động nào)\n"
        
        report = f"""
========================================
        BÁO CÁO ĐIỂM CỘNG SINH VIÊN
========================================
Mã sinh viên: {student_id}
Họ tên: {student_name}
Lớp: {student_class}
Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}
----------------------------------------
Chi tiết hoạt động:
{activities_str}----------------------------------------
Tổng điểm cộng: {total_score}
========================================
        """
        return report
    
    def generate_class_report(self, class_name: str) -> str:
        """Tạo báo cáo cho một lớp"""
        students_in_class = []
        
        if self.student_manager:
            for student in self.student_manager.list_all_students():
                if student.class_name == class_name:
                    students_in_class.append(student)
        
        if not students_in_class:
            return f"Không tìm thấy sinh viên nào trong lớp {class_name}"
        
        # Tính điểm cho từng sinh viên
        student_scores = []
        for student in students_in_class:
            score = 0.0
            if self.score_calculator:
                score = self.score_calculator.calculate_student_score(student.student_id)
            student_scores.append((student, score))
        
        # Sắp xếp theo điểm giảm dần
        student_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Tính thống kê
        scores = [s[1] for s in student_scores]
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        
        students_str = ""
        for idx, (student, score) in enumerate(student_scores, 1):
            students_str += f"  {idx}. {student.student_id} - {student.name}: {score} điểm\n"
        
        report = f"""
========================================
        BÁO CÁO ĐIỂM CỘNG LỚP {class_name}
========================================
Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Tổng số sinh viên: {len(students_in_class)}
----------------------------------------
Danh sách sinh viên:
{students_str}----------------------------------------
Thống kê:
  - Điểm trung bình: {avg_score:.2f}
  - Điểm cao nhất: {max_score}
  - Điểm thấp nhất: {min_score}
========================================
        """
        return report
    
    def generate_activity_report(self, activity_id: str) -> str:
        """Tạo báo cáo cho một hoạt động"""
        activity = None
        
        if self.activity_manager:
            for act in self.activity_manager.list_activities():
                if act.activity_id == activity_id:
                    activity = act
                    break
        
        if not activity:
            return f"Không tìm thấy hoạt động với mã {activity_id}"
        
        participants_str = ""
        if activity.participants:
            for idx, student_id in enumerate(activity.participants, 1):
                student_name = student_id
                if self.student_manager:
                    student = self.student_manager.find_student(student_id)
                    if student:
                        student_name = f"{student_id} - {student.name}"
                participants_str += f"  {idx}. {student_name}\n"
        else:
            participants_str = "  (Chưa có sinh viên tham gia)\n"
        
        report = f"""
========================================
        BÁO CÁO HOẠT ĐỘNG
========================================
Mã hoạt động: {activity.activity_id}
Tên hoạt động: {activity.name}
Loại: {activity.activity_type.value}
Điểm cộng: {activity.points}
Ngày tổ chức: {activity.date.strftime('%d/%m/%Y') if activity.date else 'N/A'}
Ngày tạo báo cáo: {datetime.now().strftime('%d/%m/%Y %H:%M')}
----------------------------------------
Danh sách sinh viên tham gia ({len(activity.participants)} người):
{participants_str}========================================
        """
        return report
    
    def generate_summary_report(self) -> str:
        """Tạo báo cáo tổng hợp"""
        stats = self.get_statistics()
        
        # Lấy top 5 sinh viên
        top_students = self.get_top_students(5)
        top_str = ""
        for idx, (student, score) in enumerate(top_students, 1):
            top_str += f"  {idx}. {student.student_id} - {student.name}: {score} điểm\n"
        if not top_str:
            top_str = "  (Chưa có dữ liệu)\n"
        
        report = f"""
========================================
        BÁO CÁO TỔNG HỢP HỆ THỐNG
========================================
Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}
----------------------------------------
THỐNG KÊ TỔNG QUAN:
  - Tổng số sinh viên: {stats['total_students']}
  - Tổng số hoạt động: {stats['total_activities']}
  - Điểm trung bình: {stats['average_score']:.2f}
  - Điểm cao nhất: {stats['max_score']}
  - Điểm thấp nhất: {stats['min_score']}
----------------------------------------
TOP 5 SINH VIÊN ĐIỂM CAO NHẤT:
{top_str}========================================
        """
        return report
    
    def export_to_csv(self, report_type: str, filename: str) -> bool:
        """Xuất báo cáo ra file CSV"""
        try:
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
            
            if report_type == "students":
                return self._export_students_csv(filename)
            elif report_type == "activities":
                return self._export_activities_csv(filename)
            elif report_type == "scores":
                return self._export_scores_csv(filename)
            else:
                print(f"Loại báo cáo không hợp lệ: {report_type}")
                return False
        except Exception as e:
            print(f"Lỗi xuất CSV: {e}")
            return False

    def export_to_json(self, report_type: str, filename: str) -> bool:
        """Xuất báo cáo ra file JSON"""
        try:
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)

            if report_type == "students":
                return self._export_students_json(filename)
            elif report_type == "activities":
                return self._export_activities_json(filename)
            elif report_type == "scores":
                return self._export_scores_json(filename)
            else:
                print(f"Loại báo cáo không hợp lệ: {report_type}")
                return False
        except Exception as e:
            print(f"Lỗi xuất JSON: {e}")
            return False
    
    def _export_students_csv(self, filename: str) -> bool:
        """Xuất danh sách sinh viên ra CSV"""
        if not self.student_manager:
            return False
        
        students = self.student_manager.list_all_students()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Mã SV', 'Họ tên', 'Lớp', 'Điểm cộng'])
            for student in students:
                score = 0.0
                if self.score_calculator:
                    score = self.score_calculator.calculate_student_score(student.student_id)
                writer.writerow([student.student_id, student.name, student.class_name, score])
        print(f"Đã xuất file: {filename}")
        return True
    
    def _export_activities_csv(self, filename: str) -> bool:
        """Xuất danh sách hoạt động ra CSV"""
        if not self.activity_manager:
            return False
        
        activities = self.activity_manager.list_activities()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Mã HĐ', 'Tên hoạt động', 'Loại', 'Điểm', 'Số người tham gia'])
            for act in activities:
                writer.writerow([act.activity_id, act.name, act.activity_type.value, 
                               act.points, len(act.participants)])
        print(f"Đã xuất file: {filename}")
        return True
    
    def _export_scores_csv(self, filename: str) -> bool:
        """Xuất điểm cộng ra CSV"""
        if not self.student_manager or not self.score_calculator:
            return False
        
        students = self.student_manager.list_all_students()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Mã SV', 'Họ tên', 'Lớp', 'Điểm cộng'])
            for student in students:
                score = self.score_calculator.calculate_student_score(student.student_id)
                writer.writerow([student.student_id, student.name, student.class_name, score])
        print(f"Đã xuất file: {filename}")
        return True

    def _export_students_json(self, filename: str) -> bool:
        """Xuất danh sách sinh viên ra JSON"""
        if not self.student_manager:
            return False

        students = self.student_manager.list_all_students()
        data = []
        for student in students:
            score = 0.0
            if self.score_calculator:
                score = self.score_calculator.calculate_student_score(student.student_id)
            data.append({
                'student_id': student.student_id,
                'name': student.name,
                'class_name': student.class_name,
                'bonus_points': score
            })

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã xuất file JSON: {filename}")
        return True

    def _export_activities_json(self, filename: str) -> bool:
        """Xuất danh sách hoạt động ra JSON"""
        if not self.activity_manager:
            return False

        activities = self.activity_manager.list_activities()
        data = []
        for act in activities:
            data.append({
                'activity_id': act.activity_id,
                'name': act.name,
                'type': act.activity_type.value,
                'points': act.points,
                'participants_count': len(act.participants),
                'date': act.date.strftime('%Y-%m-%d') if act.date else None
            })

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã xuất file JSON: {filename}")
        return True

    def _export_scores_json(self, filename: str) -> bool:
        """Xuất điểm cộng ra JSON"""
        if not self.student_manager or not self.score_calculator:
            return False

        students = self.student_manager.list_all_students()
        data = []
        for student in students:
            score = self.score_calculator.calculate_student_score(student.student_id)
            data.append({
                'student_id': student.student_id,
                'name': student.name,
                'class_name': student.class_name,
                'bonus_points': score
            })

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã xuất file JSON: {filename}")
        return True
    
    def get_top_students(self, limit: int = 10) -> list:
        """Lấy danh sách sinh viên có điểm cộng cao nhất"""
        if not self.student_manager:
            return []
        
        students = self.student_manager.list_all_students()
        student_scores = []
        
        for student in students:
            score = 0.0
            if self.score_calculator:
                score = self.score_calculator.calculate_student_score(student.student_id)
            student_scores.append((student, score))
        
        # Sắp xếp theo điểm giảm dần
        student_scores.sort(key=lambda x: x[1], reverse=True)
        
        return student_scores[:limit]
    
    def get_statistics(self) -> dict:
        """Lấy thống kê tổng quan"""
        total_students = 0
        total_activities = 0
        scores = []
        
        if self.student_manager:
            students = self.student_manager.list_all_students()
            total_students = len(students)
            
            for student in students:
                score = 0.0
                if self.score_calculator:
                    score = self.score_calculator.calculate_student_score(student.student_id)
                scores.append(score)
        
        if self.activity_manager:
            total_activities = len(self.activity_manager.list_activities())
        
        return {
            "total_students": total_students,
            "total_activities": total_activities,
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
            "max_score": max(scores) if scores else 0.0,
            "min_score": min(scores) if scores else 0.0
        }
