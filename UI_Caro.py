# ================= [UI_Caro.py] =================
import tkinter as tk
from tkinter import messagebox, Canvas , Toplevel
from Logic_Caro import Tao_Bang, danh_dau, kiem_tra_thang_Bang3x3, kiem_tra_thang_Bang24x24, kiem_tra_hoa
from AI_Logic import AI_nuoc_di

class CaroUI:
    def __init__(self, root, kich_thuoc):
        """
        Hàm khởi tạo lớp CaroUI (giao diện người dùng)
        - root: cửa sổ chính Tkinter
        - kich_thuoc: kích thước bảng (ví dụ 3x3 hoặc 24x24)
        """
        self.root = root
        self.kich_thuoc = kich_thuoc

        # Các biến giao diện
        self.che_do = None # AI hoặc 2P
        self.frame_game = None
        self.canvas = None
        self.scroll_y = None
        self.scroll_x = None

        # Dữ liệu logic của bàn cờ (2 chiều)
        self.Bang = Tao_Bang(kich_thuoc, kich_thuoc)
        self.luot_nguoi_choi = "X" # Người chơi bắt đầu là X
        self.khoa_nguoi_choi = False
        self.nut = [] # Lưu danh sách nút (ô bàn cờ)

        # Gọi hàm để tạo giao diện menu chính đầu tiên
        self.tao_giao_dien_chinh()

    # ====== MENU CHÍNH ======
    def tao_giao_dien_chinh(self):
        """ Giao diện đầu tiên: Hiện thị tên game + nút Start và Exit"""
        self.xoa_giao_dien() # Xóa giao diện cũ nếu có

        frame = tk.Frame(self.root)
        frame.pack(pady=50)
        
        # Tiêu đề chính
        tk.Label(frame, text="🎮 GAME CARO 🎮", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Tiêu đề phụ
        tk.Label(frame, text="Chọn chế độ", font=("Arial", 16, "bold")).pack(pady=10)

        # Nút chọn chế độ 
        tk.Button(frame, text="2 Người", width=15, height=2, command=lambda: self.tao_giao_dien_chon_kich_thuoc("2P")).pack(pady=5)
        
        # Nút chọn chế độ máy
        tk.Button(frame, text="Đấu vs Máy",width=15, height=2, command=lambda: self.tao_giao_dien_chon_kich_thuoc("AI")).pack(pady=5)

        # Nút thoát khỏi trò chơi
        tk.Button(frame, text="Exit", width=15, height=2, command=self.root.quit).pack(pady=5)

    # ====== CHỌN KÍCH THƯỚC ======
    def tao_giao_dien_chon_kich_thuoc(self,che_do):
        """Giao diện chọn kích thước bàn cờ: 3x3 hoặc 24x24"""
        self.che_do = che_do 
        self.xoa_giao_dien()
        frame = tk.Frame(self.root)
        frame.pack(pady=50)
        
        # Tiêu đề 
        tk.Label(frame, text="Chọn kích thước bàn cờ", font=("Arial", 16, "bold")).pack(pady=10)
        # Nút chọn bảng 3x3
        tk.Button(frame, text="3x3", width=15, height=2, command=self.Bat_dau_game3x3).pack(pady=5)
        # Nút chọn bảng 24x24
        tk.Button(frame, text="24x24", width=15, height=2, command=self.Bat_dau_game24x24).pack(pady=5)
        # Nút trở về Giao diện chính
        tk.Button(frame, text="Trở về", width=15, height=2, command=self.tao_giao_dien_chinh).pack(pady=5)

    # ====== KHỞI ĐỘNG GAME ======
    def Bat_dau_game3x3(self):
        """Bắt đầu game Caro 3x3"""
        self.kich_thuoc = 3 
        self.Bang = Tao_Bang(3, 3) 
        self.luot_nguoi_choi = "X"
        self.tao_giao_dien_bang()

    def Bat_dau_game24x24(self):
        """Bắt đầu game Caro 24x24"""
        self.kich_thuoc = 24
        self.Bang = Tao_Bang(24, 24)
        self.luot_nguoi_choi = "X"
        self.tao_giao_dien_bang()

    # ====== TẠO BẢNG CARO ======
    def tao_giao_dien_bang(self):
        # Xóa giao diện trước đó
        self.xoa_giao_dien()

        frame = tk.Frame(self.root)
        frame.pack()

        # NÚT MENU
        frame_menu = tk.Frame(self.root)
        frame_menu.pack(pady=10)

        self.lbl_trang_thai = tk.Label(self.root, text="", font=("Arial", 12))
        self.lbl_trang_thai.pack(pady=5)

        # Bảng lớn:  dùng Canvas + Scrollbar
        if self.kich_thuoc == 24:
            self.canvas = Canvas(frame)
            self.scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
            self.scroll_x = tk.Scrollbar(frame, orient="horizontal", command=self.canvas.xview)

            # Đặt vị trí các thành phần
            self.scroll_y.pack(side="right", fill="y")
            self.scroll_x.pack(side="bottom", fill="x")
            self.canvas.pack(side="left", fill="both", expand=True)
            
            # Liên kết thanh cuộn với canvas
            self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

            # Frame chứa các nút bàn cờ
            self.frame_game = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame_game, anchor="nw")

            # Cập nhật vùng cuộn khi kích thước thay đổi
            self.frame_game.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        else:
            # Nếu bảng nhỏ thì không cần scroll
            self.frame_game = frame

        # Thiết lập kích thước nút phù hợp với từng loại bảng
        w = 6 if self.kich_thuoc == 3 else 2
        h = 3 if self.kich_thuoc == 3 else 1
        font_size = 18 if self.kich_thuoc == 3 else 10
        
        # Tạo lưới nút (ô bàn cờ)
        self.nut = []
        for i in range(self.kich_thuoc):
            hang = []
            for j in range(self.kich_thuoc):
                # Mỗi ô là 1 Button
                nut = tk.Button(self.frame_game, text=" ", width=w, height=h,
                                font=("Arial", font_size, "bold"),
                                command=lambda x=i, y=j: self.xu_ly_nuoc_di(x, y))
                nut.grid(row=i, column=j)
                hang.append(nut)
            self.nut.append(hang)

        # Nút Menu trong trận đấu
        tk.Button(frame_menu, text="Menu", width=10, height=3, command=self.hien_menu_trong_tran).pack()

    # Hàm tạo giao diện menu trong trận
    def hien_menu_trong_tran(self):
        """Hiện menu poppup trong khi đang chơi"""
        menu_popup = tk.Toplevel(self.root)
        menu_popup.title("Menu trong trận")
        self.can_giua_cua_so(menu_popup, 300, 200) # Căn giữa
        menu_popup.resizable(False, False)
        menu_popup.grab_set() # Chặn tương tác ngoài popup

        # Hiển thị thông báo
        tk.Label(menu_popup, text="Tạm dừng", font=("Arial", 14, "bold")).pack(pady=10)

        # Nút tiếp tục
        tk.Button(menu_popup, text="Tiếp tục", width=17,height=2,command=menu_popup.destroy).pack(pady=5)
        # Nút Chơi lại
        tk.Button(menu_popup, text="Chơi lại", width=17,height=2,command=lambda: [menu_popup.destroy(),self.Bat_dau_game3x3() if self.kich_thuoc == 3 else self.Bat_dau_game24x24()]).pack(pady=5)

        # Nút Trở về menu chính
        tk.Button(menu_popup, text="Trở về Menu chính", width=17,height=2,command=lambda: [menu_popup.destroy(),self.tao_giao_dien_chinh()]).pack(pady=5)

    # ====== XỬ LÝ NƯỚC ĐI ======
    def xu_ly_nuoc_di(self, hang, cot):
        """Khi người chơi click vào ô (hang, cot)"""

        # Nếu đang khóa (máy đang đánh) thì không cho người chơi click
        if getattr(self, "khoa_nguoi_choi", False):
            return

        # Kiểm tra ô đã đánh chưa nếu đánh rồi thì return 
        if not danh_dau(self.Bang, hang, cot, self.luot_nguoi_choi): 
            return  # Ô đã đánh rồi

        # Hiển thị ký tự X hoặc O lên giao diện
        self.nut[hang][cot].config(text=self.luot_nguoi_choi)

        # Kiểm tra thắng / hòa
        if self.kich_thuoc == 3:
            duong_thang = kiem_tra_thang_Bang3x3(self.Bang, self.luot_nguoi_choi)
        else:
            duong_thang = kiem_tra_thang_Bang24x24(self.Bang, self.luot_nguoi_choi, hang, cot)
        # Đưa ra kết quả và khóa b
        if duong_thang:
            self.to_mau_o_thang(duong_thang)
            self.khoa_ban_co()
            self.popup_ket_thuc(f"Người chơi {self.luot_nguoi_choi} thắng!")
            return
    
        if kiem_tra_hoa(self.Bang):
            self.khoa_ban_co() # Khóa bàn cờ lại sau khi thắng
            self.popup_ket_thuc("Trò chơi hòa!")
            return
        
        # Đổi lượt
        self.luot_nguoi_choi = "O" if self.luot_nguoi_choi == "X" else "X"

        # Nếu chơi với máy và đến lượt máy
        if self.che_do == "AI" and self.luot_nguoi_choi == "O":
            self.khoa_nguoi_choi = True # Khóa người chơi
            self.lbl_trang_thai.config(text="🤖 Máy đang đánh...") 
            self.root.after(500, self.luot_AI_danh)

    # ====== AI ĐÁNH ======
    def luot_AI_danh(self):
        # Máy đi và nhận lại vị trí
        may_x, may_y = AI_nuoc_di(self.Bang, "O") 
        self.nut[may_x][may_y].config(text="O")

        # Kiểm tra thắng / hòa
        duong_thang = (
            kiem_tra_thang_Bang3x3(self.Bang, "O")
            if self.kich_thuoc == 3
            else kiem_tra_thang_Bang24x24(self.Bang, "O", may_x, may_y)
        )

        if duong_thang:
            self.to_mau_o_thang(duong_thang)
            self.khoa_ban_co()
            self.popup_ket_thuc("Máy thắng!")
            return

        if kiem_tra_hoa(self.Bang):
            self.khoa_ban_co()
            self.popup_ket_thuc("Trò chơi hòa!")
            return
        
        # Trả lượt cho người chơi
        self.lbl_trang_thai.config(text="Lượt của bạn")
        self.khoa_nguoi_choi = False # Mở khóa người chơi
        self.luot_nguoi_choi = "X"

    # ====== TÔ MÀU ĐƯỜNG THẮNG ======
    def to_mau_o_thang(self, duong_thang):
        """Tô màu vàng cho các ô thắng"""
        for hang, cot in duong_thang:
            self.nut[hang][cot].config(bg="yellow")

    # ====== GIAO DIỆN KẾT THÚC ======
    # Hàm hiển thị thông báo kết thúc
    def popup_ket_thuc(self, thong_bao):
        # Tạo cửa sổ mới (Không phá bàn cờ hiện tại)
        popup = tk.Toplevel(self.root)
        popup.title("Kết thúc trận đấu")
        self.can_giua_cua_so(popup, 300, 200) # Căn giữa màn hình
        popup.resizable(False, False)
        popup.grab_set() # Chặn tương tác ngoài popup

        # Hiển thị thông báo
        tk.Label(popup, text="🎉 KẾT THÚC TRẬN ĐẤU 🎉", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(popup,text=thong_bao,font=("Arial",12)).pack(pady=10)
        
        # Nút OK : chỉ đóng popup
        self.khoa_nguoi_choi = False # Mở khóa người chơi
        tk.Button(popup, text="OK",width=10, height=1 ,command=popup.destroy).pack(pady=10)

    # Hàm khóa bàn cờ 
    def khoa_ban_co(self):
        """Khóa toàn bộ các ô bàn cờ (sau khi thắng hoặc hòa)"""
        for i in range(self.kich_thuoc):
            for j in range(self.kich_thuoc):
                self.nut[i][j].config(state="disabled")

    # ====== XÓA GIAO DIỆN HIỆN TẠI ======
    def xoa_giao_dien(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ======= CĂN GIỮA CỬA SỔ ======
    def can_giua_cua_so(self, window, width, height):
        """ Đặt cửa sổ (popup) ra giữa màn hình"""
        window.update_idletasks()
        screen_width = (window.winfo_screenwidth() // 2) - (width // 2)
        screen_height = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{screen_width}+{screen_height}")

