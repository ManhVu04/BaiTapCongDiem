import os
import json
import tempfile
import unittest

from database.data_storage import DataStorage
from student.student_manager import StudentManager
from activity.activity_manager import ActivityManager, ActivityType
from score.score_calculator import ScoreCalculator
from report.report_generator import ReportGenerator


class TestReportExport(unittest.TestCase):
    def test_export_json_and_csv(self):
        # Tạo môi trường tạm
        with tempfile.TemporaryDirectory() as tmpdir:
            db = DataStorage(data_dir=tmpdir)
            sm = StudentManager(db)
            am = ActivityManager(db)
            sc = ScoreCalculator(db, sm, am)
            rg = ReportGenerator(db, sm, am, sc)

            # Thêm sinh viên và hoạt động
            s = sm.add_student('SV001', 'Nguyen Van A', 'CNTT1')
            a = am.create_activity('HD001', 'Hoat dong test', ActivityType.VOLUNTEER, 0.5)
            am.add_participant('HD001', 'SV001')

            # Xuất JSON
            json_file = os.path.join(tmpdir, 'students.json')
            ok_json = rg.export_to_json('students', json_file)
            self.assertTrue(ok_json)
            self.assertTrue(os.path.exists(json_file))

            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(data[0]['student_id'], 'SV001')

            # Xuất CSV
            csv_file = os.path.join(tmpdir, 'students.csv')
            ok_csv = rg.export_to_csv('students', csv_file)
            self.assertTrue(ok_csv)
            self.assertTrue(os.path.exists(csv_file))


if __name__ == '__main__':
    unittest.main()
