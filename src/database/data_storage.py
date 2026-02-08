"""
Data storage module.
"""

import json
import os
import shutil
from datetime import datetime


class DataStorage:
    """Handles reading and writing project data files."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, "students.json")
        self.activities_file = os.path.join(data_dir, "activities.json")
        self.scores_file = os.path.join(data_dir, "scores.json")
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_students(self, students: list) -> bool:
        """Save students to JSON."""
        try:
            data = [self._student_to_dict(student) for student in students]
            with open(self.students_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except Exception as exc:
            print(f"Loi luu sinh vien: {exc}")
            return False

    def load_students(self) -> list:
        """Load students from JSON."""
        if not os.path.exists(self.students_file):
            return []
        try:
            with open(self.students_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except Exception as exc:
            print(f"Loi tai sinh vien: {exc}")
            return []

    def save_activities(self, activities: list) -> bool:
        """Save activities to JSON."""
        try:
            data = [self._activity_to_dict(activity) for activity in activities]
            with open(self.activities_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except Exception as exc:
            print(f"Loi luu hoat dong: {exc}")
            return False

    def load_activities(self) -> list:
        """Load activities from JSON."""
        if not os.path.exists(self.activities_file):
            return []
        try:
            with open(self.activities_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except Exception as exc:
            print(f"Loi tai hoat dong: {exc}")
            return []

    def save_scores(self, scores: dict) -> bool:
        """Save scores to JSON."""
        try:
            with open(self.scores_file, "w", encoding="utf-8") as file:
                json.dump(scores, file, ensure_ascii=False, indent=2)
            return True
        except Exception as exc:
            print(f"Loi luu diem: {exc}")
            return False

    def load_scores(self) -> dict:
        """Load scores from JSON."""
        if not os.path.exists(self.scores_file):
            return {}
        try:
            with open(self.scores_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
        except Exception as exc:
            print(f"Loi tai diem: {exc}")
            return {}

    def backup_data(self, backup_name: str = None) -> bool:
        """Create a timestamped backup folder under data/backups."""
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            if backup_name is None:
                backup_name = datetime.now().strftime("%Y%m%d_%H%M%S")

            backup_path = os.path.join(backup_dir, backup_name)
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)

            if os.path.exists(self.students_file):
                shutil.copy(self.students_file, os.path.join(backup_path, "students.json"))
            if os.path.exists(self.activities_file):
                shutil.copy(self.activities_file, os.path.join(backup_path, "activities.json"))
            if os.path.exists(self.scores_file):
                shutil.copy(self.scores_file, os.path.join(backup_path, "scores.json"))

            return True
        except Exception as exc:
            print(f"Loi sao luu du lieu: {exc}")
            return False

    def restore_data(self, backup_name: str) -> bool:
        """Restore files from data/backups/<backup_name>."""
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            backup_path = os.path.join(backup_dir, backup_name)
            if not os.path.exists(backup_path):
                print(f"Ban sao luu '{backup_name}' khong ton tai")
                return False

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
        except Exception as exc:
            print(f"Loi khoi phuc du lieu: {exc}")
            return False

    def _student_to_dict(self, student) -> dict:
        return {
            "student_id": student.student_id,
            "name": student.name,
            "class_name": student.class_name,
            "bonus_points": student.bonus_points,
        }

    def _activity_to_dict(self, activity) -> dict:
        activity_id = str(getattr(activity, "activity_id", "")).strip()
        name = str(getattr(activity, "name", getattr(activity, "activity_name", ""))).strip()

        activity_type_obj = getattr(activity, "activity_type", "OTHER")
        if hasattr(activity_type_obj, "name"):
            activity_type = activity_type_obj.name
        else:
            activity_type = str(activity_type_obj).strip().upper() or "OTHER"

        raw_points = getattr(activity, "points", getattr(activity, "bonus_points", 0.0))
        try:
            points = float(raw_points)
        except (TypeError, ValueError):
            points = 0.0

        raw_date = getattr(activity, "date", None)
        if isinstance(raw_date, datetime):
            date_text = raw_date.isoformat()
        elif raw_date is None:
            date_text = None
        else:
            date_text = str(raw_date)

        raw_participants = getattr(activity, "participants", [])
        if isinstance(raw_participants, list):
            participants = [str(student_id) for student_id in raw_participants]
        else:
            participants = []

        return {
            "activity_id": activity_id,
            "name": name,
            "activity_name": name,
            "activity_type": activity_type,
            "points": points,
            "bonus_points": points,
            "date": date_text,
            "participants": participants,
            "description": str(getattr(activity, "description", "")),
        }

    def clear_all_data(self) -> bool:
        """Delete all persisted data files."""
        try:
            if os.path.exists(self.students_file):
                os.remove(self.students_file)
            if os.path.exists(self.activities_file):
                os.remove(self.activities_file)
            if os.path.exists(self.scores_file):
                os.remove(self.scores_file)
            return True
        except Exception as exc:
            print(f"Loi xoa du lieu: {exc}")
            return False
