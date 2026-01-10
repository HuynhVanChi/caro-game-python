# ======================= QUẢN LÝ CẤU HÌNH (MÀU SẮC, FONT CHỮ, KÍCH THƯỚC) ====================
# MỤC ĐÍCH: Lưu trữ các hằng số cấu hình (Màu sắc, Font, Kích thước)

# --- Cấu hình Font chữ (Kiểu chữ, Cỡ chữ, Độ đậm) ---
FONT_TITLE = ("Arial", 20, "bold") # Font tiêu đề lớn ở Menu
FONT_SUBTITLE = ("Arial", 16, "bold") # Front tiêu đề phụ
FONT_NORMAL = ("Arial", 12) # Front chữ thường

# Font riêng cho quân cờ (X/O) trên bàn cờ
FONT_GAME_BIG = ("Arial", 18, "bold")  # Cho bàn 3x3
FONT_GAME_SMALL = ("Arial", 10, "bold") # Cho bàn 24x24

# --- Cấu hình Màu sắc ---
COLOR_BG_WIN = "yellow"
COLOR_TEXT_X = "red"
COLOR_TEXT_O = "blue"

COLOR_LAST_MOVE = "cyan" # Màu xanh lơ (hoặc dùng "lightgreen", "pink" tùy bạn)
COLOR_DEFAULT_BG = "SystemButtonFace" # Màu nền mặc định của nút bấm (Button)

# --- Cấu hình Kích thước nút bấm (Button) ---
SIZE_BTN_3X3 = {'w': 6, 'h': 3} # Nút to cho bàn nhỏ
SIZE_BTN_24X24 = {'w': 2, 'h': 1} # Nút nhỏ cho bàn lớn
