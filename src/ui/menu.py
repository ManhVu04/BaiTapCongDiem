"""
Console menu module.
"""


class Menu:
    """Manages console-based UI flows."""

    def __init__(self, student_manager, activity_manager, score_calculator, report_generator):
        self.student_manager = student_manager
        self.activity_manager = activity_manager
        self.score_calculator = score_calculator
        self.report_generator = report_generator

    def display_main_menu(self):
        print("\n" + "=" * 40)
        print("          MENU CHINH")
        print("=" * 40)
        print("1. Quan ly sinh vien")
        print("2. Quan ly hoat dong")
        print("3. Tinh diem cong")
        print("4. Xem bao cao")
        print("5. Thoat")
        print("-" * 40)

    def display_student_menu(self):
        print("\n--- QUAN LY SINH VIEN ---")
        print("1. Them sinh vien")
        print("2. Xoa sinh vien")
        print("3. Tim sinh vien")
        print("4. Danh sach sinh vien")
        print("5. Quay lai")

    def display_activity_menu(self):
        print("\n--- QUAN LY HOAT DONG ---")
        print("1. Tao hoat dong")
        print("2. Xoa hoat dong")
        print("3. Them sinh vien vao hoat dong")
        print("4. Danh sach hoat dong")
        print("5. Quay lai")

    def display_score_menu(self):
        print("\n--- TINH DIEM CONG ---")
        print("1. Xem diem sinh vien")
        print("2. Cap nhat tat ca diem")
        print("3. Quay lai")

    def display_report_menu(self):
        print("\n--- BAO CAO ---")
        print("1. Bao cao sinh vien")
        print("2. Bao cao lop")
        print("3. Thong ke tong hop")
        print("4. Xuat CSV")
        print("5. Quay lai")

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)

    def run(self):
        while True:
            self.display_main_menu()
            choice = self.get_user_input("Chon chuc nang (1-5): ")

            if choice == "1":
                self.handle_student_menu()
            elif choice == "2":
                self.handle_activity_menu()
            elif choice == "3":
                self.handle_score_menu()
            elif choice == "4":
                self.handle_report_menu()
            elif choice == "5":
                print("Cam on ban da su dung he thong. Tam biet!")
                break
            else:
                print("Lua chon khong hop le. Vui long thu lai.")

    def handle_student_menu(self):
        while True:
            self.display_student_menu()
            choice = self.get_user_input("Chon chuc nang (1-5): ")

            if choice == "1":
                student_id = self.get_user_input("Nhap ma sinh vien: ")
                name = self.get_user_input("Nhap ten sinh vien: ")
                class_name = self.get_user_input("Nhap ten lop: ")
                try:
                    student = self.student_manager.add_student(student_id, name, class_name)
                    print(f"Da them sinh vien: {student}")
                except ValueError as exc:
                    print(f"Loi: {exc}")
            elif choice == "2":
                student_id = self.get_user_input("Nhap ma sinh vien can xoa: ")
                result = self.student_manager.remove_student(student_id)
                if result:
                    print("Da xoa sinh vien thanh cong.")
                else:
                    print("Khong tim thay sinh vien.")
            elif choice == "3":
                student_id = self.get_user_input("Nhap ma sinh vien can tim: ")
                student = self.student_manager.find_student(student_id)
                if student:
                    print(f"Tim thay: {student}")
                else:
                    print("Khong tim thay sinh vien.")
            elif choice == "4":
                students = self.student_manager.list_all_students()
                print("\n--- DANH SACH SINH VIEN ---")
                for student in students:
                    print(student)
            elif choice == "5":
                break
            else:
                print("Lua chon khong hop le. Vui long thu lai.")

    def handle_activity_menu(self):
        from activity.activity_manager import ActivityType

        while True:
            self.display_activity_menu()
            choice = self.get_user_input("Chon chuc nang (1-5): ")

            if choice == "1":
                activity_id = self.get_user_input("Nhap ma hoat dong: ")
                name = self.get_user_input("Nhap ten hoat dong: ")
                activity_type = self.get_user_input(
                    "Nhap loai hoat dong (VOLUNTEER/ACADEMIC/SPORT/CULTURE/OTHER): "
                )
                raw_points = self.get_user_input("Nhap so diem cong: ")

                try:
                    points = float(raw_points)
                except ValueError:
                    print("Diem cong khong hop le. Vui long nhap so.")
                    continue

                try:
                    atype = ActivityType[activity_type.strip().upper()]
                except KeyError:
                    print("Loai hoat dong khong hop le. Su dung OTHER.")
                    atype = ActivityType.OTHER

                try:
                    created = self.activity_manager.create_activity(activity_id, name, atype, points)
                    print(f"Da tao hoat dong: {created}")
                except ValueError as exc:
                    print(f"Loi: {exc}")
            elif choice == "2":
                # Xóa hoạt động
                activity_id = self.get_user_input("Nhập mã hoạt động cần xóa: ")
                self.activity_manager.delete_activity(activity_id) if hasattr(self.activity_manager, 'delete_activity') else print("Chức năng chưa hỗ trợ.")
            elif choice == "3":
                activity_id = self.get_user_input("Nhap ma hoat dong: ")
                student_id = self.get_user_input("Nhap ma sinh vien: ")
                self.activity_manager.add_participant(activity_id, student_id)
            elif choice == "4":
                activities = self.activity_manager.list_activities()
                print("\n--- DANH SACH HOAT DONG ---")
                for activity in activities:
                    print(activity)
            elif choice == "5":
                break
            else:
                print("Lua chon khong hop le. Vui long thu lai.")

    def handle_score_menu(self):
        while True:
            self.display_score_menu()
            choice = self.get_user_input("Chon chuc nang (1-3): ")

            if choice == "1":
                student_id = self.get_user_input("Nhap ma sinh vien: ")
                score = self.score_calculator.calculate_student_score(student_id)
                print(f"Tong diem cong cua sinh vien {student_id}: {score}")
            elif choice == "2":
                print("Cap nhat diem cho tat ca sinh vien...")
                if not self.score_calculator.update_all_scores():
                    print("Khong the cap nhat diem.")
            elif choice == "3":
                break
            else:
                print("Lua chon khong hop le. Vui long thu lai.")

    def handle_report_menu(self):
        while True:
            self.display_report_menu()
            choice = self.get_user_input("Chon chuc nang (1-5): ")

            if choice == "1":
                student_id = self.get_user_input("Nhap ma sinh vien: ")
                report = self.report_generator.generate_student_report(student_id)
                print(report)
            elif choice == "2":
                class_name = self.get_user_input("Nhap ten lop: ")
                report = self.report_generator.generate_class_report(class_name)
                print(report if report is not None else "Chuc nang chua ho tro.")
            elif choice == "3":
                report = self.report_generator.generate_summary_report()
                print(report if report is not None else "Chuc nang chua ho tro.")
            elif choice == "4":
                # Xuất file (CSV hoặc JSON)
                print("Chọn loại báo cáo: 1-Sinh viên, 2-Hoạt động, 3-Điểm")
                report_choice = self.get_user_input("Chọn (1-3): ")
                report_types = {"1": "students", "2": "activities", "3": "scores"}
                report_type = report_types.get(report_choice, "students")

                fmt_choice = self.get_user_input("Chọn định dạng xuất: 1-CSV, 2-JSON (mặc định CSV): ")
                if fmt_choice.strip() == "2":
                    filename = self.get_user_input("Nhập tên file JSON: ")
                    if not filename.endswith('.json'):
                        filename += '.json'
                    if hasattr(self.report_generator, 'export_to_json'):
                        self.report_generator.export_to_json(report_type, filename)
                    else:
                        print("Chức năng JSON chưa được hỗ trợ trong ReportGenerator.")
                else:
                    filename = self.get_user_input("Nhập tên file CSV: ")
                    if not filename.endswith('.csv'):
                        filename += '.csv'
                    if hasattr(self.report_generator, 'export_to_csv'):
                        self.report_generator.export_to_csv(report_type, filename)
                    else:
                        print("Chức năng CSV chưa hỗ trợ.")
            elif choice == "5":
                break
            else:
                print("Lua chon khong hop le. Vui long thu lai.")
