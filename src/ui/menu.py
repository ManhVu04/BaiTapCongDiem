"""
Module UI - Giao diện người dùng
Thành viên 5 phụ trách
"""


class Menu:
    """Class quản lý giao diện menu console"""
    
    def __init__(self, student_manager, activity_manager, 
                 score_calculator, report_generator):
        self.student_manager = student_manager
        self.activity_manager = activity_manager
        self.score_calculator = score_calculator
        self.report_generator = report_generator
    
    def display_main_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "=" * 40)
        print("        MENU CHÍNH")
        print("=" * 40)
        print("1. Quản lý sinh viên")
        print("2. Quản lý hoạt động")
        print("3. Tính điểm cộng")
        print("4. Xem báo cáo")
        print("5. Thoát")
        print("-" * 40)
    
    def display_student_menu(self):
        """Hiển thị menu quản lý sinh viên"""
        # TODO: Thành viên 5 implement
        print("\n--- QUẢN LÝ SINH VIÊN ---")
        print("1. Thêm sinh viên")
        print("2. Xóa sinh viên")
        print("3. Tìm sinh viên")
        print("4. Danh sách sinh viên")
        print("5. Quay lại")
    
    def display_activity_menu(self):
        """Hiển thị menu quản lý hoạt động"""
        # TODO: Thành viên 5 implement
        print("\n--- QUẢN LÝ HOẠT ĐỘNG ---")
        print("1. Tạo hoạt động")
        print("2. Xóa hoạt động")
        print("3. Thêm sinh viên vào hoạt động")
        print("4. Danh sách hoạt động")
        print("5. Quay lại")
    
    def display_score_menu(self):
        """Hiển thị menu tính điểm"""
        # TODO: Thành viên 5 implement
        print("\n--- TÍNH ĐIỂM CỘNG ---")
        print("1. Xem điểm sinh viên")
        print("2. Cập nhật tất cả điểm")
        print("3. Quay lại")
    
    def display_report_menu(self):
        """Hiển thị menu báo cáo"""
        # TODO: Thành viên 5 implement
        print("\n--- BÁO CÁO ---")
        print("1. Báo cáo sinh viên")
        print("2. Báo cáo lớp")
        print("3. Thống kê tổng hợp")
        print("4. Xuất CSV")
        print("5. Quay lại")
    
    def get_user_input(self, prompt: str) -> str:
        """Lấy input từ người dùng"""
        return input(prompt)
    
    def run(self):
        """Chạy vòng lặp menu chính"""
        while True:
            self.display_main_menu()
            choice = self.get_user_input("Chọn chức năng (1-5): ")
            
            if choice == "1":
                self.handle_student_menu()
            elif choice == "2":
                self.handle_activity_menu()
            elif choice == "3":
                self.handle_score_menu()
            elif choice == "4":
                self.handle_report_menu()
            elif choice == "5":
                print("Cảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def handle_student_menu(self):
        while True:
            self.display_student_menu()
            choice = self.get_user_input("Chọn chức năng (1-5): ")
            if choice == "1":
                # Thêm sinh viên
                student_id = self.get_user_input("Nhập mã sinh viên: ")
                name = self.get_user_input("Nhập tên sinh viên: ")
                class_name = self.get_user_input("Nhập tên lớp: ")
                self.student_manager.add_student(student_id, name, class_name)
            elif choice == "2":
                # Xóa sinh viên
                student_id = self.get_user_input("Nhập mã sinh viên cần xóa: ")
                result = self.student_manager.remove_student(student_id)
                if result:
                    print("Đã xóa sinh viên thành công.")
                else:
                    print("Không tìm thấy sinh viên.")
            elif choice == "3":
                # Tìm sinh viên
                student_id = self.get_user_input("Nhập mã sinh viên cần tìm: ")
                student = self.student_manager.find_student(student_id)
                if student:
                    print(f"Tìm thấy: {student}")
                else:
                    print("Không tìm thấy sinh viên.")
            elif choice == "4":
                # Danh sách sinh viên
                students = self.student_manager.list_all_students() if hasattr(self.student_manager, 'list_all_students') else self.student_manager.students
                print("\n--- DANH SÁCH SINH VIÊN ---")
                for s in students:
                    print(s)
            elif choice == "5":
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def handle_activity_menu(self):
        while True:
            self.display_activity_menu()
            choice = self.get_user_input("Chọn chức năng (1-5): ")
            if choice == "1":
                # Tạo hoạt động
                activity_id = self.get_user_input("Nhập mã hoạt động: ")
                name = self.get_user_input("Nhập tên hoạt động: ")
                activity_type = self.get_user_input("Nhập loại hoạt động (VOLUNTEER/ACADEMIC/SPORT/CULTURE/OTHER): ")
                points = float(self.get_user_input("Nhập số điểm cộng: "))
                from activity.activity_manager import ActivityType
                try:
                    atype = ActivityType[activity_type.upper()]
                except Exception:
                    print("Loại hoạt động không hợp lệ. Sử dụng OTHER.")
                    atype = ActivityType.OTHER
                self.activity_manager.create_activity(activity_id, name, atype, points) if hasattr(self.activity_manager, 'create_activity') else print("Chức năng chưa hỗ trợ.")
            elif choice == "2":
                # Xóa hoạt động
                activity_id = self.get_user_input("Nhập mã hoạt động cần xóa: ")
                self.activity_manager.delete_activity(activity_id) if hasattr(self.activity_manager, 'delete_activity') else print("Chức năng chưa hỗ trợ.")
            elif choice == "3":
                # Thêm sinh viên vào hoạt động
                activity_id = self.get_user_input("Nhập mã hoạt động: ")
                student_id = self.get_user_input("Nhập mã sinh viên: ")
                self.activity_manager.add_participant(activity_id, student_id) if hasattr(self.activity_manager, 'add_participant') else print("Chức năng chưa hỗ trợ.")
            elif choice == "4":
                # Danh sách hoạt động
                activities = self.activity_manager.list_activities() if hasattr(self.activity_manager, 'list_activities') else self.activity_manager.activities
                print("\n--- DANH SÁCH HOẠT ĐỘNG ---")
                for a in activities:
                    print(a)
            elif choice == "5":
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def handle_score_menu(self):
        while True:
            self.display_score_menu()
            choice = self.get_user_input("Chọn chức năng (1-3): ")
            if choice == "1":
                # Xem điểm sinh viên
                student_id = self.get_user_input("Nhập mã sinh viên: ")
                score = self.score_calculator.calculate_student_score(student_id)
                print(f"Tổng điểm cộng của sinh viên {student_id}: {score}")
            elif choice == "2":
                # Cập nhật tất cả điểm (giả lập)
                print("Cập nhật điểm cho tất cả sinh viên...")
                if hasattr(self.student_manager, 'students'):
                    for s in self.student_manager.students:
                        score = self.score_calculator.calculate_student_score(s.student_id)
                        s.bonus_points = score
                        print(f"{s}: {score}")
                else:
                    print("Không có danh sách sinh viên.")
            elif choice == "3":
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def handle_report_menu(self):
        while True:
            self.display_report_menu()
            choice = self.get_user_input("Chọn chức năng (1-5): ")
            if choice == "1":
                # Báo cáo sinh viên
                student_id = self.get_user_input("Nhập mã sinh viên: ")
                report = self.report_generator.generate_student_report(student_id)
                print(report)
            elif choice == "2":
                # Báo cáo lớp
                class_name = self.get_user_input("Nhập tên lớp: ")
                if hasattr(self.report_generator, 'generate_class_report'):
                    report = self.report_generator.generate_class_report(class_name)
                    print(report)
                else:
                    print("Chức năng chưa hỗ trợ.")
            elif choice == "3":
                # Thống kê tổng hợp
                if hasattr(self.report_generator, 'generate_summary_report'):
                    report = self.report_generator.generate_summary_report()
                    print(report)
                else:
                    print("Chức năng chưa hỗ trợ.")
            elif choice == "4":
                # Xuất CSV
                if hasattr(self.report_generator, 'export_to_csv'):
                    print("Chọn loại báo cáo: 1-Sinh viên, 2-Hoạt động, 3-Điểm")
                    report_choice = self.get_user_input("Chọn (1-3): ")
                    report_types = {"1": "students", "2": "activities", "3": "scores"}
                    report_type = report_types.get(report_choice, "students")
                    filename = self.get_user_input("Nhập tên file CSV: ")
                    if not filename.endswith('.csv'):
                        filename += '.csv'
                    self.report_generator.export_to_csv(report_type, filename)
                else:
                    print("Chức năng chưa hỗ trợ.")
            elif choice == "5":
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
