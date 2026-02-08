"""
Score calculation module.
"""


class ScoreCalculator:
    """Computes bonus scores for students."""

    def __init__(
        self, database, student_manager=None, activity_manager=None, max_bonus_points: float = 2.0
    ):
        self.database = database
        self.student_manager = student_manager
        self.activity_manager = activity_manager
        self.max_bonus_points = max_bonus_points

    def _get_activity_manager(self):
        if self.activity_manager is None:
            from activity.activity_manager import ActivityManager

            self.activity_manager = ActivityManager(self.database)
        return self.activity_manager

    def _get_student_manager(self):
        if self.student_manager is None:
            from student.student_manager import StudentManager

            self.student_manager = StudentManager(self.database)
        return self.student_manager

    def calculate_student_score(self, student_id: str) -> float:
        """Compute total bonus score for one student."""
        total_score = 0.0
        activities = self._get_activity_manager().list_activities()

        for activity in activities:
            if student_id in getattr(activity, "participants", []):
                try:
                    total_score += float(getattr(activity, "points", 0.0))
                except (TypeError, ValueError):
                    continue

        return self.apply_bonus_rules(total_score)

    def calculate_activity_score(self, activity_id: str, student_id: str) -> float:
        """Compute score from one activity for one student."""
        activities = self._get_activity_manager().list_activities()

        for activity in activities:
            if activity.activity_id == activity_id:
                if student_id in getattr(activity, "participants", []):
                    try:
                        return float(getattr(activity, "points", 0.0))
                    except (TypeError, ValueError):
                        return 0.0
                return 0.0

        return 0.0

    def apply_bonus_rules(self, raw_score: float) -> float:
        """Apply max cap and lower bound to score."""
        if raw_score > self.max_bonus_points:
            return self.max_bonus_points
        if raw_score < 0:
            return 0.0
        return round(raw_score, 2)

    def get_score_breakdown(self, student_id: str) -> dict:
        """Return score details for one student."""
        activities = self._get_activity_manager().list_activities()

        breakdown = {
            "student_id": student_id,
            "activities": [],
            "total_raw_score": 0.0,
            "final_score": 0.0,
        }

        for activity in activities:
            if student_id not in getattr(activity, "participants", []):
                continue

            activity_type = getattr(activity, "activity_type", None)
            activity_type_name = (
                activity_type.value
                if hasattr(activity_type, "value")
                else str(activity_type or "N/A")
            )

            activity_date = getattr(activity, "date", None)
            date_text = activity_date.strftime("%Y-%m-%d") if activity_date else "N/A"

            try:
                points = float(getattr(activity, "points", 0.0))
            except (TypeError, ValueError):
                points = 0.0

            breakdown["activities"].append(
                {
                    "activity_id": activity.activity_id,
                    "name": getattr(activity, "name", ""),
                    "type": activity_type_name,
                    "points": points,
                    "date": date_text,
                }
            )
            breakdown["total_raw_score"] += points

        breakdown["final_score"] = self.apply_bonus_rules(breakdown["total_raw_score"])
        breakdown["total_raw_score"] = round(breakdown["total_raw_score"], 2)
        return breakdown

    def update_all_scores(self) -> bool:
        """Recalculate and persist all student scores."""
        try:
            students = self._get_student_manager().list_all_students()
            for student in students:
                student.bonus_points = self.calculate_student_score(student.student_id)

            if self.database is not None:
                self.database.save_students(students)
            print(f"Da cap nhat diem cho {len(students)} sinh vien")
            return True
        except Exception as exc:
            print(f"Loi khi cap nhat diem: {exc}")
            return False

    def validate_score(self, score: float) -> bool:
        """Check score in valid range."""
        return 0 <= score <= self.max_bonus_points
