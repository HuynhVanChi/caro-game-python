# 🎮 Trò Chơi Cờ Caro (Caro Game Python)

Dự án game cờ Caro (Gomoku / Tic-Tac-Toe) được xây dựng hoàn toàn bằng ngôn ngữ **Python** và thư viện giao diện đồ họa **Tkinter**, hỗ trợ hai chế độ chơi: **2 Người đối kháng (2P)** và **Đấu với Máy (AI)**.

---

## ✨ Tính Năng Nổi Bật

* **2 Chế độ chơi linh hoạt:**
  * **2 Người (2 Players):** Đấu trí trực tiếp trên cùng một máy tính.
  * **Đấu Máy (AI Mode):** Thử thách với bot máy tính thông minh.
* **Đa dạng kích thước bàn cờ:**
  * **3x3 (Tic-Tac-Toe):** Ván cờ nhanh, AI áp dụng thuật toán **Minimax** vét cạn tối ưu.
  * **24x24 (Cờ Caro Việt Nam / Gomoku):** Bàn cờ rộng lớn có thanh cuộn mượt mà, AI sử dụng thuật toán **Heuristic** khoanh vùng ứng viên lân cận và đánh giá thế cờ.
* **Chuẩn hóa luật chơi cờ Caro Việt Nam:**
  * Áp dụng luật **chặn 2 đầu không thắng**: Tạo chuỗi 5 quân nhưng bị chặn cả 2 đầu bởi quân đối thủ sẽ không tính thắng.
  * Hỗ trợ highlight nước vừa đi và tô màu đường cờ chiến thắng.

---

## 📂 Cấu Trúc Dự Án

```text
caro-game-python/
├── Main.py                 # Điểm khởi chạy ứng dụng chính
├── Logic_Caro.py           # Core logic: Khởi tạo bảng, đánh dấu nước đi, trọng tài kiểm tra thắng/hòa
├── AI_Logic.py             # Thuật toán AI: Minimax (3x3) & Heuristic cục bộ (24x24)
├── KE_HOACH_CAI_TIEN.md    # Bản kế hoạch và lộ trình cải tiến tính năng (Roadmap)
├── README.md               # Tài liệu hướng dẫn sử dụng dự án
├── .gitignore              # Cấu hình loại bỏ file rác khi đẩy lên Git
└── UI_caro/                # Module giao diện đồ họa (Tkinter)
    ├── __init__.py         # Khởi tạo package UI
    ├── config.py           # Cấu hình màu sắc, font chữ, kích thước ô cờ
    ├── ui_board.py         # View bàn cờ (xử lý hiển thị lưới cờ và thanh cuộn)
    ├── ui_main.py          # Controller chính điều phối luồng trò chơi và menu
    └── ui_popup.py         # Quản lý các popup thông báo tạm dừng / kết thúc
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Game

### 1. Yêu cầu hệ thống
* Cài đặt **Python 3.8+** trở lên (Khuyến nghị Python 3.10, 3.11, 3.12, 3.13).
* Thư viện `tkinter` (thường đã tích hợp sẵn trong bộ cài đặt chuẩn của Python trên Windows).

### 2. Tải về và khởi chạy
Mở terminal hoặc PowerShell tại thư mục dự án và chạy lệnh:

```bash
python Main.py
```

---

## 🗺️ Lộ Trình Phát Triển Tiếp Theo

Chi tiết kế hoạch nâng cấp và kiểm thử tính năng được theo dõi tại [KE_HOACH_CAI_TIEN.md](KE_HOACH_CAI_TIEN.md):
- [x] Đồng bộ luật chặn 2 đầu và sửa triệt để bộ nhớ AI.
- [ ] Bổ sung bàn cờ chuẩn 15x15 (không cần thanh cuộn).
- [ ] Cho phép người chơi chọn quân đi trước (X) hoặc đi sau (O).
- [ ] Thêm tính năng Hoàn tác (Undo).
- [ ] Nâng cấp vẽ bàn cờ bằng Canvas và hiệu ứng âm thanh.

---

## 📄 Giấy phép (License)
Dự án được phát hành dưới giấy phép mã nguồn mở MIT License. Tự do học tập, sử dụng và phát triển thêm!
