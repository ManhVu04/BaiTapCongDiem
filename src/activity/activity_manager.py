"""
Activity module.
"""

from datetime import datetime
from enum import Enum
from typing import Optional


class ActivityType(Enum):
    """Supported activity types."""

    VOLUNTEER = "Tinh nguyen"
    ACADEMIC = "Hoc thuat"
    SPORT = "The thao"
    CULTURE = "Van hoa"
    OTHER = "Khac"


class Activity:
    """Represents a student activity."""

    def __init__(
        self,
        activity_id: str,
        name: str,
        activity_type: ActivityType,
        points: float,
        date: Optional[datetime] = None,
        participants: Optional[list] = None,
    ):
        self.activity_id = activity_id
        self.name = name
        self.activity_type = activity_type
        self.points = points
        self.date = date or datetime.now()
        self.participants = list(participants) if participants else []

    def __str__(self):
        return (
            f"{self.activity_id} - {self.name} "
            f"({self.activity_type.value}) - {self.points} diem"
        )


class ActivityManager:
    """Manages activities and participants."""

    def __init__(self, database):
        self.database = database
        self.activities = []
        self._load_from_storage()

    def _load_from_storage(self):
        """Load activities from storage if available."""
        if self.database is None:
            return

        records = self.database.load_activities()
        if not isinstance(records, list):
            return

        for record in records:
            activity = self._to_activity(record)
            if activity is not None:
                self.activities.append(activity)

    def _save_to_storage(self):
        """Persist activities to storage."""
        if self.database is None:
            return False
        return self.database.save_activities(self.activities)

    def _to_activity(self, value) -> Optional[Activity]:
        """Normalize record loaded from storage."""
        if isinstance(value, Activity):
            return value
        if not isinstance(value, dict):
            return None

        activity_id = str(value.get("activity_id", "")).strip()
        name = str(value.get("name", value.get("activity_name", ""))).strip()
        if not activity_id or not name:
            return None

        raw_type = str(value.get("activity_type", "OTHER")).strip().upper()
        try:
            activity_type = ActivityType[raw_type]
        except KeyError:
            activity_type = ActivityType.OTHER

        try:
            points = float(value.get("points", value.get("bonus_points", 0.0)))
        except (TypeError, ValueError):
            points = 0.0

        date_value = value.get("date")
        activity_date = None
        if isinstance(date_value, str) and date_value.strip():
            try:
                activity_date = datetime.fromisoformat(date_value)
            except ValueError:
                activity_date = None

        participants = []
        raw_participants = value.get("participants", [])
        if isinstance(raw_participants, list):
            participants = [
                str(student_id).strip()
                for student_id in raw_participants
                if str(student_id).strip()
            ]

        return Activity(
            activity_id=activity_id,
            name=name,
            activity_type=activity_type,
            points=points,
            date=activity_date,
            participants=participants,
        )

    def find_activity(self, activity_id: str) -> Optional[Activity]:
        """Find an activity by id."""
        normalized_id = activity_id.strip()
        for activity in self.activities:
            if activity.activity_id == normalized_id:
                return activity
        return None

    def create_activity(
        self, activity_id: str, name: str, activity_type: ActivityType, points: float
    ) -> Activity:
        """Create and store a new activity."""
        activity_id = activity_id.strip()
        name = name.strip()

        if not activity_id or not name:
            raise ValueError("Activity info must not be empty")
        if self.find_activity(activity_id) is not None:
            raise ValueError(f"Activity id '{activity_id}' already exists")

        try:
            points_value = float(points)
        except (TypeError, ValueError):
            raise ValueError("Points must be a number")
        if points_value < 0:
            raise ValueError("Points must not be negative")

        activity = Activity(activity_id, name, activity_type, points_value)
        self.activities.append(activity)
        self._save_to_storage()
        print(f"Da tao hoat dong: {activity}")
        return activity

    def remove_activity(self, activity_id: str) -> bool:
        """Remove an activity by id."""
        activity = self.find_activity(activity_id)
        if activity is None:
            print(f"Khong tim thay hoat dong voi ID: {activity_id}")
            return False

        self.activities.remove(activity)
        self._save_to_storage()
        print(f"Da xoa hoat dong: {activity}")
        return True

    def delete_activity(self, activity_id: str) -> bool:
        """Backward-compatible alias."""
        return self.remove_activity(activity_id)

    def add_participant(self, activity_id: str, student_id: str) -> bool:
        """Add a student into activity."""
        activity = self.find_activity(activity_id)
        if activity is None:
            print(f"Khong tim thay hoat dong voi ID: {activity_id}")
            return False

        student_id = student_id.strip()
        if not student_id:
            print("Ma sinh vien khong hop le")
            return False
        if student_id in activity.participants:
            print(f"Sinh vien {student_id} da tham gia hoat dong {activity_id}")
            return False

        activity.participants.append(student_id)
        self._save_to_storage()
        print(f"Da them sinh vien {student_id} vao hoat dong {activity_id}")
        return True

    def remove_participant(self, activity_id: str, student_id: str) -> bool:
        """Remove a student from activity."""
        activity = self.find_activity(activity_id)
        if activity is None:
            print(f"Khong tim thay hoat dong voi ID: {activity_id}")
            return False
        if student_id not in activity.participants:
            print(f"Sinh vien {student_id} khong tham gia hoat dong {activity_id}")
            return False

        activity.participants.remove(student_id)
        self._save_to_storage()
        print(f"Da xoa sinh vien {student_id} khoi hoat dong {activity_id}")
        return True

    def list_activities(self) -> list:
        """Return all activities."""
        return list(self.activities)

    def get_activities_by_type(self, activity_type: ActivityType) -> list:
        """Filter activities by type."""
        return [a for a in self.activities if a.activity_type == activity_type]
