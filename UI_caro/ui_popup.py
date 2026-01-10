# =========================== QUẢN LÝ CỬA SỔ PHỤ ===============================
# MỤC ĐÍCH: Quản lý các cửa sổ phụ (Thông báo, Menu tạm dừng)

import tkinter as tk # Import thư viện giao diện Tkinter
from UI_caro.config import * # Import cấu hình màu sắc/font

class PopupManager:
    """Class quản lý các popup (cửa sổ phụ) trong game Caro"""
    @staticmethod 
    def can_giua(window, w, h): # Hàm căn giữa cửa sổ 
        """
        Hàm toán học để tính toán vị trí đặt cửa sổ vào chính giữa màn hình.
        - window: đối tượng cửa sổ cần căn
        - w, h: chiều rộng, chiều cao mong muốn
        """
        window.update_idletasks() # Cập nhật trạng thái vẽ để lấy thông số màn hình chuẩn
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (w // 2)
        y = (screen_height // 2) - (h // 2)

        # Đặt kích thước và vị trí cho cửa sổ (format: RộngxCao+X+Y)
        window.geometry(f"{w}x{h}+{x}+{y}")

    @staticmethod
    def hien_menu_trong_tran(root, on_tiep_tuc, on_choi_lai, on_ve_menu):
        """
        Hiển thị Menu tạm dừng khi đang chơi.
        Nhận vào 3 hàm callback (hàm sẽ chạy khi bấm nút).
        """
        # Tạo cửa sổ con (Toplevel) dựa trên cửa sổ chính (root)
        popup = tk.Toplevel(root)
        popup.title("Menu") # Tiêu đề cửa sổ menu tạm dừng
        PopupManager.can_giua(popup, 300, 250)

        popup.resizable(False, False) # Không cho người dùng kéo giãn cửa sổ
        popup.grab_set() # QUAN TRỌNG: Chặn tương tác với cửa sổ chính khi popup này đang mở

        tk.Label(popup, text="Tạm dừng", font=("Arial", 14, "bold")).pack(pady=10)

        # Các nút chức năng
        tk.Button(popup, text="Tiếp tục", width=15, height=2, 
                  command=lambda: [popup.destroy(), on_tiep_tuc()]).pack(pady=5)
        
        tk.Button(popup, text="Chơi lại", width=15, height=2, 
                  command=lambda: [popup.destroy(), on_choi_lai()]).pack(pady=5)

        tk.Button(popup, text="Về Menu chính", width=15, height=2, 
                  command=lambda: [popup.destroy(), on_ve_menu()]).pack(pady=5)

    @staticmethod
    def hien_ket_thuc(root, thong_bao, on_ok , on_choi_lai):
        """Hiển thị thông báo kết quả trận đấu (Thắng/Hòa)"""
        popup = tk.Toplevel(root)
        popup.title("Kết thúc") # Tiêu đề cửa sổ kết thúc trận đấu 
        PopupManager.can_giua(popup, 300, 200)
        popup.resizable(False, False) # Không cho người dùng kéo giãn cửa sổ
        popup.grab_set() # Chặn tương tác bên ngoài

        tk.Label(popup, text="🎉 KẾT THÚC 🎉", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(popup, text=thong_bao, font=FONT_NORMAL).pack(pady=10)

        # Khi bấm OK, đóng popup và chạy hàm xử lý sau khi thắng (ví dụ: mở khóa bàn cờ)
        tk.Button(popup, text="OK", width=10, command=lambda: [popup.destroy(), on_ok()]).pack(pady=10)
        tk.Button(popup, text="Chơi lại", width=10, command=lambda: [popup.destroy(), on_choi_lai()]).pack(pady=10)
