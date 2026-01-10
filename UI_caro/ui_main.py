# MỤC ĐÍCH: Controller chính - Điều phối hoạt động Game

import tkinter as tk
# Import Logic và AI từ thư mục gốc (Parent Directory)
from Logic_Caro import Tao_Bang, danh_dau, kiem_tra_thang_Bang3x3, kiem_tra_thang_Bang24x24, kiem_tra_hoa
from AI_Logic import AI_nuoc_di

# Import các thành phần UI từ gói UI_Caro
from UI_caro.config import *
from UI_caro.ui_popup import PopupManager
from UI_caro.ui_board import BoardView

class CaroUI:
    def __init__(self, root, kich_thuoc=3):
        self.root = root
        self.root.title("Game Caro Pro")
        self.default_size = kich_thuoc

        # Khởi tạo các biến trạng thái game
        self.kich_thuoc = kich_thuoc
        self.Bang = [] # Lưu trạng thái bàn cờ dưới dạng mảng 2 chiều 
        self.che_do = "2P" # Chế độ chơi: "2P" (2 người) hoặc "AI" (đấu máy)
        self.luot_nguoi_choi = "X" # Lượt hiện tại: "X" hoặc "O"
        self.khoa_nguoi_choi = False # Biến cờ để chặn click khi máy đang tính
        
        # Các thành phần giao diện
        self.view_board = None # Quản lý giao diện bàn cờ
        self.lbl_status = None # Nhãn hiển thị lượt đi

        self.tao_giao_dien_chinh() # Bắt đầu hiển thị Menu chính

    # ====== 1. CÁC HÀM TẠO GIAO DIỆN (MENU) ======
    def xoa_giao_dien(self):
        """Xóa sạch mọi thứ trên cửa sổ để vẽ màn hình mới"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def tao_giao_dien_chinh(self):
        """Màn hình 1: Menu chính"""
        self.xoa_giao_dien()
        f = tk.Frame(self.root)
        f.pack(pady=50) # Tạo khoảng cách lề trên
        
        tk.Label(f, text="🎮 GAME CARO 🎮", font=FONT_TITLE).pack(pady=10) # Tiêu đề game 
        # Chọn chế độ chơi 
        tk.Button(f, text="2 Người", width=15, height=2, command=lambda: self.menu_chon_size("2P")).pack(pady=5)
        tk.Button(f, text="Đấu Máy", width=15, height=2, command=lambda: self.menu_chon_size("AI")).pack(pady=5)
        tk.Button(f, text="Thoát", width=15, height=2, command=self.root.quit).pack(pady=5)

    def menu_chon_size(self, mode):
        """Màn hình 2: Chọn kích thước bàn cờ"""
        self.che_do = mode
        self.xoa_giao_dien()
        f = tk.Frame(self.root)
        f.pack(pady=50)
        
        tk.Label(f, text="Chọn kích thước", font=FONT_SUBTITLE).pack(pady=10)
        tk.Button(f, text="3x3", width=15, height=2, command=lambda: self.bat_dau_game(3)).pack(pady=5)
        tk.Button(f, text="24x24", width=15, height=2, command=lambda: self.bat_dau_game(24)).pack(pady=5)
        tk.Button(f, text="Trở về", width=15, height=2, command=self.tao_giao_dien_chinh).pack(pady=5)

    def bat_dau_game(self, size):
        """Khởi tạo dữ liệu cho ván mới"""
        self.kich_thuoc = size
        self.Bang = Tao_Bang(size, size) # Tạo bảng logic rỗng
        self.luot_nguoi_choi = "X"
        self.khoa_nguoi_choi = False
        self.tao_man_hinh_game() # Vẽ bàn cờ

    def tao_man_hinh_game(self):
        """Màn hình 3: Bàn cờ đang chơi"""
        self.xoa_giao_dien()

        # 1. Vẽ thanh công cụ phía trên (Menu + Status)
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)
        
        tk.Button(top_frame, text="Menu", command=self.hien_menu_popup).pack(side="left", padx=10)
        self.lbl_status = tk.Label(top_frame, text="Lượt của X", font=FONT_NORMAL)
        self.lbl_status.pack(side="left", padx=10)

        # 2. Vẽ bàn cờ phía dưới
        board_frame = tk.Frame(self.root)
        board_frame.pack(fill="both", expand=True)
        
        # Khởi tạo BoardView, truyền hàm self.xu_ly_click vào để nhận sự kiện click
        self.view_board = BoardView(board_frame, self.kich_thuoc, self.xu_ly_click)

    # ====== 2. XỬ LÝ LOGIC TRONG GAME ======
    def hien_menu_popup(self):
        """Gọi PopupManager để hiện menu tạm dừng"""
        PopupManager.hien_menu_trong_tran(
            self.root, 
            lambda: None, # Hàm Tiếp tục: không làm gì, chỉ đóng popup
            lambda: self.bat_dau_game(self.kich_thuoc), # Hàm Chơi lại: reset game
            self.tao_giao_dien_chinh # Hàm Về menu chính
        )

    def xu_ly_click(self, r, c):
        """Hàm quan trọng nhất: Xử lý khi người chơi bấm vào ô (r, c)"""

        # 1. Kiểm tra hợp lệ:
        # - Nếu đang khóa (máy đang đánh) -> Bỏ qua
        # - Nếu ô đó đã đánh rồi (hàm danh_dau trả về False) -> Bỏ qua
        if self.khoa_nguoi_choi or not danh_dau(self.Bang, r, c, self.luot_nguoi_choi):
            return

        # 2. Cập nhật giao diện: Hiện chữ X/O lên ô vừa bấm
        color = COLOR_TEXT_X if self.luot_nguoi_choi == "X" else COLOR_TEXT_O
        self.view_board.cap_nhat_o(r, c, self.luot_nguoi_choi, color)

        self.view_board.highlight_nuoc_di(r, c) # Highlight nước đi vừa rồi

        # 3. Kiểm tra Thắng/Thua ngay lập tức
        if self.kiem_tra_ket_thuc(r, c):
            return # Nếu game xong thì dừng luôn

        # 4. Đổi lượt chơi (X -> O hoặc O -> X)
        self.luot_nguoi_choi = "O" if self.luot_nguoi_choi == "X" else "X"
        self.lbl_status.config(text=f"Lượt của {self.luot_nguoi_choi}")

        # 5. Nếu đang chế độ Đấu Máy và đến lượt O, gọi AI đánh 
        if self.che_do == "AI" and self.luot_nguoi_choi == "O":
            self.khoa_nguoi_choi = True # Khóa bàn cờ, không cho người bấm lung tung
            self.lbl_status.config(text="🤖 Máy đang nghĩ...")
            
            # Dùng after(500) để tạo độ trễ 0.5s cho cảm giác máy đang "suy nghĩ"
            self.root.after(500, self.luot_may)

    def luot_may(self):
        """Hàm xử lý lượt đi của AI"""

        # Gọi thuật toán AI tìm nước đi tốt nhất
        mx, my = AI_nuoc_di(self.Bang, "O")

        # [DEBUG] In thử bàn cờ ra xem có bị đầy nhóc quân cờ không
        print("--- Bàn cờ sau khi AI tính xong ---")
        for hang in self.Bang:
            print(hang)
        print("-----------------------------------")

        # Cập nhật dữ liệu logic để máy tính biết ô này đã có chủ
        self.Bang[mx][my] = "O"

        # Cập nhật UI cho nước đi của máy
        self.view_board.cap_nhat_o(mx, my, "O", COLOR_TEXT_O)

        self.view_board.highlight_nuoc_di(mx, my) # Highlight nước đi của máy
        
        # Kiểm tra máy có thắng không
        if not self.kiem_tra_ket_thuc(mx, my):
            # Nếu chưa xong, trả lượt về cho người chơi
            self.luot_nguoi_choi = "X"
            self.khoa_nguoi_choi = False # Mở khóa bàn cờ cho người chơi
            self.lbl_status.config(text="Lượt của bạn (X)")

    def kiem_tra_ket_thuc(self, r, c):
        """Kiểm tra xem nước đi tại (r,c) có kết thúc ván đấu không"""
        player = self.Bang[r][c]
        win_path = None # Biến lưu danh sách các ô tạo thành đường thắng
        
        # Gọi hàm kiểm tra từ file Logic_Caro
        if self.kich_thuoc == 3:
            win_path = kiem_tra_thang_Bang3x3(self.Bang, player)
        else:
            win_path = kiem_tra_thang_Bang24x24(self.Bang, player, r, c)

        # TRƯỜNG HỢP 1: Có người thắng
        if win_path:
            self.view_board.to_mau_thang(win_path) # Tô màu vàng
            self.view_board.khoa_ban_co() # Khóa bàn cờ
            # Hiện popup thông báo
            PopupManager.hien_ket_thuc(self.root, f"{player} CHIẾN THẮNG!", lambda: self.khoa_nguoi_choi == False,lambda: self.bat_dau_game(self.kich_thuoc))
            return True
        
        # TRƯỜNG HỢP 2: Hòa cờ
        if kiem_tra_hoa(self.Bang):
            self.view_board.khoa_ban_co()
            PopupManager.hien_ket_thuc(self.root, "HÒA CỜ!", lambda: self.khoa_nguoi_choi == False, lambda: self.bat_dau_game(self.kich_thuoc))
            return True
            
        return False # Ván đấu vẫn tiếp tục