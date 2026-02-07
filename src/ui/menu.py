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
        """Xử lý menu sinh viên"""
        # TODO: Thành viên 5 implement
        self.display_student_menu()
        print("(Chức năng đang được phát triển)")
    
    def handle_activity_menu(self):
        """Xử lý menu hoạt động"""
        # TODO: Thành viên 5 implement
        self.display_activity_menu()
        print("(Chức năng đang được phát triển)")
    
    def handle_score_menu(self):
        """Xử lý menu điểm"""
        # TODO: Thành viên 5 implement
        self.display_score_menu()
        print("(Chức năng đang được phát triển)")
    
    def handle_report_menu(self):
        """Xử lý menu báo cáo"""
        # TODO: Thành viên 5 implement
        self.display_report_menu()
        print("(Chức năng đang được phát triển)")
