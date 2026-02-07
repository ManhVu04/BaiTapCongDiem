Môn: Công cụ và môi trường phát triển phần mềm sáng T5.
# Hệ Thống Quản Lý Điểm Cộng

## Mô tả dự án
Đây là dự án nhóm để thực hành làm việc với Git. Hệ thống giúp quản lý và tính toán điểm cộng cho sinh viên.

## Thành viên nhóm và phân công
Vũ Đức Mạnh: tạo dự án, phân công, tạo project và duyệt.

| STT | Thành viên | Nhánh | Nhiệm vụ |
|-----|------------|-------|----------|
| 1 | Trần Thị Thanh Mai | feature/member-1 | Module Student (Quản lý sinh viên) |
| 2 | Phạm Xuân Minh Quân | feature/member-2 | Module Activity (Quản lý hoạt động) |
| 3 | Trần Đức Minh | feature/member-3 | Module Score (Tính điểm cộng) |
| 4 | Lượng Thị Thủy Hằng| feature/member-4 | Module Report (Báo cáo thống kê) |
| 5 | Bùi Thị Bích Liêu | feature/member-5 | Module UI (Giao diện người dùng) |
| 6 | Trần Như Liễu | feature/member-6 | Module Database (Lưu trữ dữ liệu) |

## Cấu trúc dự án

```
CongDiem/
├── src/
│   ├── student/       # Module quản lý sinh viên
│   ├── activity/      # Module quản lý hoạt động
│   ├── score/         # Module tính điểm
│   ├── report/        # Module báo cáo
│   ├── ui/            # Module giao diện
│   └── database/      # Module lưu trữ
├── tests/             # Thư mục chứa test
├── docs/              # Tài liệu dự án
└── README.md
```

## Hướng dẫn làm việc với Git

### Clone dự án
```bash
git clone <repository-url>
cd CongDiem
```

### Chuyển sang nhánh của mình
```bash
git checkout feature/member-X  # X là số thứ tự thành viên
```

### Quy trình làm việc
1. Pull code mới nhất từ main
2. Checkout sang nhánh của mình
3. Code và commit thường xuyên
4. Push lên remote
5. Tạo Pull Request để merge vào main

### Các lệnh Git cơ bản
```bash
git status                    # Kiểm tra trạng thái
git add .                     # Thêm tất cả thay đổi
git commit -m "Mô tả"         # Commit với message
git push origin <tên-nhánh>   # Push lên remote
git pull origin main          # Lấy code mới từ main
```

## Cách chạy dự án
```bash
python src/main.py
```

## License
MIT License
