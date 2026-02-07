# Hướng dẫn đóng góp cho dự án

## Quy tắc làm việc

### 1. Quy tắc đặt tên nhánh
- Mỗi thành viên làm việc trên nhánh riêng: `feature/member-X`
- Nhánh sửa lỗi: `bugfix/mô-tả-lỗi`
- Nhánh hotfix: `hotfix/mô-tả`

### 2. Quy tắc commit message
Sử dụng định dạng:
```
<type>: <mô tả ngắn>

<mô tả chi tiết nếu cần>
```

Các loại commit:
- `feat`: Thêm tính năng mới
- `fix`: Sửa lỗi
- `docs`: Cập nhật tài liệu
- `refactor`: Tái cấu trúc code
- `test`: Thêm hoặc sửa test

Ví dụ:
```
feat: thêm chức năng tìm kiếm sinh viên

- Thêm method find_student trong StudentManager
- Hỗ trợ tìm theo mã số và tên
```

### 3. Quy trình Pull Request
1. Đảm bảo code chạy không lỗi
2. Viết test cho các tính năng mới
3. Tạo Pull Request với mô tả rõ ràng
4. Chờ review từ team lead hoặc thành viên khác
5. Xử lý các feedback trước khi merge

### 4. Code style
- Sử dụng docstring cho tất cả các function và class
- Đặt tên biến và function bằng tiếng Anh
- Comment bằng tiếng Việt nếu cần giải thích

## Liên hệ
Nếu có thắc mắc, hãy tạo Issue trên GitHub hoặc liên hệ team lead.
