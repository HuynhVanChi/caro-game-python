# MỤC ĐÍCH: Controller chính - Điều phối hoạt động Game

import tkinter as tk
# Import Logic và AI từ thư mục gốc
from Logic_Caro import Tao_Bang, danh_dau, kiem_tra_thang_Bang3x3, kiem_tra_thang_Bang24x24, kiem_tra_hoa
from AI_Logic import AI_nuoc_di, AI_reset

# Import các thành phần UI
from UI_caro.config import *
from UI_caro.ui_popup import PopupManager
from UI_caro.ui_board import BoardView

class CaroUI:
    def __init__(self, root, kich_thuoc=3):
        self.root = root
        self.root.title("Game Caro - 2 Người / Đấu Máy")
        self.root.configure(bg=COLOR_BG) 
        
        # [FIX] Kích thước mặc định hợp lý hơn
        self.root.geometry("900x650")

        # Cho phép co giãn 2 chiều
        self.root.resizable(True, True)

        # Khởi tạo các biến trạng thái game
        self.kich_thuoc = kich_thuoc
        self.Bang = [] 
        self.che_do = "2P" 
        self.luot_nguoi_choi = "X" 
        self.khoa_nguoi_choi = False 
        
        self.view_board = None 
        self.lbl_status = None 

        self.tao_giao_dien_chinh() 

    # ====== 1. CÁC HÀM TẠO GIAO DIỆN (MENU) ======
    def xoa_giao_dien(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tao_giao_dien_chinh(self):
        """Màn hình 1: Menu chính"""
        self.xoa_giao_dien()

        bg_frame = tk.Frame(self.root, bg=COLOR_BG)
        bg_frame.pack(fill="both", expand=True)
        
        f = tk.Frame(bg_frame, bg=COLOR_BG) # [FIX] Thêm bg=COLOR_BG
        f.place(relx=0.5, rely=0.5, anchor="center") 
        
        tk.Label(f, text="🎮 GAME CARO 🎮", font=FONT_TITLE, bg=COLOR_BG).pack(pady=20) 
        tk.Button(f, text="2 Người", width=15, font=FONT_NORMAL, command=lambda: self.menu_chon_size("2P")).pack(pady=5)
        tk.Button(f, text="Đấu Máy", width=15, font=FONT_NORMAL, command=lambda: self.menu_chon_size("AI")).pack(pady=5)
        tk.Button(f, text="Thoát", width=15, font=FONT_NORMAL, command=self.root.quit).pack(pady=5)

    def menu_chon_size(self, mode):
        """Màn hình 2: Chọn kích thước bàn cờ"""
        self.che_do = mode
        self.xoa_giao_dien()

        bg_frame = tk.Frame(self.root, bg=COLOR_BG)
        bg_frame.pack(fill="both", expand=True)

        f = tk.Frame(bg_frame, bg=COLOR_BG) # [FIX] Thêm bg=COLOR_BG
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="Chọn kích thước", font=FONT_SUBTITLE, bg=COLOR_BG).pack(pady=20)
        tk.Button(f, text="3x3", width=15, font=FONT_NORMAL, command=lambda: self.bat_dau_game(3)).pack(pady=5)
        tk.Button(f, text="24x24", width=15, font=FONT_NORMAL, command=lambda: self.bat_dau_game(24)).pack(pady=5)
        tk.Button(f, text="Trở về", width=15, font=FONT_NORMAL, command=self.tao_giao_dien_chinh).pack(pady=5)

    def bat_dau_game(self, size):
        self.kich_thuoc = size
        self.Bang = Tao_Bang(size, size) 
        self.luot_nguoi_choi = "X"
        self.khoa_nguoi_choi = False
        AI_reset()
        self.tao_man_hinh_game() 

    def tao_man_hinh_game(self):
        """Màn hình 3: Bàn cờ đang chơi"""
        self.xoa_giao_dien()

        # 1. Container chính (Chiếm toàn bộ màn hình)
        main_container = tk.Frame(self.root, bg=COLOR_BG)
        main_container.pack(fill="both", expand=True)

        # 2. Thanh công cụ phía trên
        top_frame = tk.Frame(main_container, bg=COLOR_BG)
        top_frame.pack(side="top", fill="x", pady=5)
        
        top_center = tk.Frame(top_frame, bg=COLOR_BG)
        top_center.pack(anchor="center")

        tk.Button(top_center, text="Menu", font=FONT_NORMAL, command=self.hien_menu_popup).pack(side="left", padx=10)
        self.lbl_status = tk.Label(top_center, text=f"Lượt của {self.luot_nguoi_choi}", font=FONT_NORMAL, bg=COLOR_BG)
        self.lbl_status.pack(side="left", padx=20)

        # 3. Khu vực bàn cờ
        # [QUAN TRỌNG] Thay vì place, ta dùng pack cho CẢ 2 trường hợp
        # Để board_area luôn chiếm hết phần còn lại của màn hình
        board_area = tk.Frame(main_container, bg="black") 
        board_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 4. Khởi tạo BoardView
        self.view_board = BoardView(board_area, self.kich_thuoc, self.xu_ly_click)

    # ====== 2. XỬ LÝ LOGIC TRONG GAME ======
    def hien_menu_popup(self):
        PopupManager.hien_menu_trong_tran(
            self.root, 
            lambda: None, 
            lambda: self.bat_dau_game(self.kich_thuoc), 
            self.tao_giao_dien_chinh 
        )

    def xu_ly_click(self, r, c):
        if self.khoa_nguoi_choi or not danh_dau(self.Bang, r, c, self.luot_nguoi_choi):
            return

        color = COLOR_TEXT_X if self.luot_nguoi_choi == "X" else COLOR_TEXT_O
        self.view_board.cap_nhat_o(r, c, self.luot_nguoi_choi, color)
        self.view_board.highlight_nuoc_di(r, c) 

        if self.kiem_tra_ket_thuc(r, c):
            return 

        self.luot_nguoi_choi = "O" if self.luot_nguoi_choi == "X" else "X"
        self.lbl_status.config(text=f"Lượt của {self.luot_nguoi_choi}")

        if self.che_do == "AI" and self.luot_nguoi_choi == "O":
            self.khoa_nguoi_choi = True 
            self.lbl_status.config(text="🤖 Máy đang nghĩ...")
            self.root.after(100, self.luot_may) # [TWEAK] Giảm delay xuống 100ms cho mượt

    def luot_may(self):
        mx, my = AI_nuoc_di(self.Bang, "O")

        # [DEBUG] Có thể bỏ print để code sạch hơn
        # print("--- Bàn cờ sau khi AI tính xong ---") 
        
        self.Bang[mx][my] = "O"
        self.view_board.cap_nhat_o(mx, my, "O", COLOR_TEXT_O)
        self.view_board.highlight_nuoc_di(mx, my) 
        
        if not self.kiem_tra_ket_thuc(mx, my):
            self.luot_nguoi_choi = "X"
            self.khoa_nguoi_choi = False 
            self.lbl_status.config(text="Lượt của bạn (X)")

    def kiem_tra_ket_thuc(self, r, c):
        player = self.Bang[r][c]
        win_path = None 
        
        if self.kich_thuoc == 3:
            win_path = kiem_tra_thang_Bang3x3(self.Bang, player)
        else:
            win_path = kiem_tra_thang_Bang24x24(self.Bang, player, r, c)

        if win_path:
            self.view_board.to_mau_thang(win_path) 
            self.view_board.khoa_ban_co() 
            
            # [FIX QUAN TRỌNG] Sửa lỗi cú pháp lambda ở đây
            PopupManager.hien_ket_thuc(
                self.root, 
                f"{player} CHIẾN THẮNG!", 
                lambda: None, # Hàm xem lại (chỉ cần đóng popup)
                lambda: self.bat_dau_game(self.kich_thuoc) # Hàm chơi lại
            )
            return True
        
        if kiem_tra_hoa(self.Bang):
            self.view_board.khoa_ban_co()
            PopupManager.hien_ket_thuc(
                self.root, 
                "HÒA CỜ!", 
                lambda: None, 
                lambda: self.bat_dau_game(self.kich_thuoc)
            )
            return True
            
        return False