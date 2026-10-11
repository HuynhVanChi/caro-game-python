# ======================= QUẢN LÝ CẤU HÌNH (MÀU SẮC, FONT CHỮ, KÍCH THƯỚC) ====================
# MỤC ĐÍCH: Lưu trữ các hằng số cấu hình (Màu sắc, Font, Kích thước)

# 1. MÀU SẮC (COLORS)
COLOR_BG = "#f0f0f0"           # Màu nền cửa sổ chính (Xám nhạt cho sang trọng)
COLOR_BTN_BG = "SystemButtonFace" # Màu nền nút mặc định của Windows
COLOR_TEXT_X = "red"           # Màu chữ X
COLOR_TEXT_O = "blue"          # Màu chữ O
COLOR_LAST_MOVE = "#87CEFA"    # Màu highlight nước vừa đi (Xanh dương nhạt - LightSkyBlue)
COLOR_WIN_BG = "#FFD700"       # Màu highlight chiến thắng (Vàng kim - Gold)

# 2. FONT CHỮ (FONTS)
# Font tiêu đề to (Màn hình menu)
FONT_TITLE = ("Arial", 28, "bold")

# Font phụ đề (Các mục nhỏ)
FONT_SUBTITLE = ("Arial", 16)

# Font chữ thường (Status bar, nút bấm thường)
FONT_NORMAL = ("Arial", 12)

# [QUAN TRỌNG] Font chữ trong ô cờ
# Đây là biến quyết định độ to của ô cờ.
# - Nếu bạn thấy bàn cờ vẫn nhỏ, hãy tăng số 11 lên 12 hoặc 14.
# - Nếu bàn cờ bị tràn màn hình, hãy giảm xuống 9 hoặc 10.
FONT_TEXT_BOARD = ("Arial", 11, "bold")

# 3. KÍCH THƯỚC Ô CỜ (BUTTON SIZE)
# Lưu ý: Trong Tkinter, Width tính bằng số ký tự, Height tính bằng số dòng.
# Tỷ lệ 3:1 (Rộng 3, Cao 1) thường giúp nút vuông vắn nhất trên Windows.
BUTTON_WIDTH = 3
BUTTON_HEIGHT = 1
