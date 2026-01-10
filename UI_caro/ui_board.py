# ui_board.py
import tkinter as tk
from tkinter import Canvas # Import Canvas để tạo(Vẽ) bàn cờ lớn với thanh cuộn
from UI_caro.config import *

class BoardView:
    # Hàm khởi tạo bàn cờ
    def __init__(self, parent_frame, kich_thuoc, callback_click):
        """
        Khởi tạo bàn cờ.
        - parent_frame: Frame cha chứa bàn cờ này
        - kich_thuoc: Số ô (3 hoặc 24)
        - callback_click: Hàm của ui_main sẽ chạy khi người dùng bấm vào ô
        """
        self.frame = parent_frame # Frame cha chứa bàn cờ
        self.kich_thuoc = kich_thuoc # Kích thước bàn cờ (3x3 hoặc 24x24)
        self.callback_click = callback_click # Hàm callback khi bấm ô
        self.buttons = [] # Mảng 2 chiều lưu trữ các đối tượng Button
        
        self.last_move_btn = None # Lưu nút của nước đi cuối cùng để đổi màu nền

        self.tao_ban_co()

    def highlight_nuoc_di(self, x, y):
        """Làm nổi bật ô tại (x,y) và trả ô cũ về bình thường"""
        
        # 1. Nếu đã có ô được highlight trước đó -> Trả về màu gốc
        if self.last_move_btn is not None:
            try:
                self.last_move_btn.config(bg=COLOR_DEFAULT_BG)
            except:
                pass # Phòng trường hợp game reset mà nút cũ không còn

        # 2. Lấy nút mới và tô màu highlight
        btn_moi = self.buttons[x][y]
        btn_moi.config(bg=COLOR_LAST_MOVE)

        # 3. Lưu nút mới làm "nút cũ" cho lượt sau
        self.last_move_btn = btn_moi

    def tao_ban_co(self):
        """Hàm dựng giao diện bàn cờ"""
        # Nếu là bàn cờ 24x24, tạo Canvas với thanh cuộn
        if self.kich_thuoc == 24:
            # Tạo Canvas (vùng vẽ) để có thể cuộn được
            canvas = Canvas(self.frame)

            # Tạo thanh cuộn dọc và ngang
            scroll_y = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
            scroll_x = tk.Scrollbar(self.frame, orient="horizontal", command=canvas.xview)
           
            # Đặt vị trí thanh cuộn
            scroll_y.pack(side="right", fill="y")
            scroll_x.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)

            # Kết nối Canvas với thanh cuộn
            canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            
            # Tạo một Frame con nằm TRONG Canvas (đây là nơi chứa các nút button)
            game_area = tk.Frame(canvas)
            
            # Vẽ Frame con lên Canvas tại tọa độ (0,0)
            canvas.create_window((0, 0), window=game_area, anchor="nw")
            
            # Kỹ thuật quan trọng: Khi kích thước Frame con thay đổi (do thêm nút),
            # cập nhật lại vùng cuộn (scrollregion) cho Canvas biết giới hạn cuộn.
            game_area.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        else:
            # TRƯỜNG HỢP 2: Bàn cờ nhỏ (3x3) -> Không cần thanh cuộn
            game_area = self.frame # Vẽ trực tiếp lên frame cha

        # VẼ LƯỚI NÚT
        # Lấy cấu hình font và size từ config.py
        font_size = FONT_GAME_BIG if self.kich_thuoc == 3 else FONT_GAME_SMALL
        w = SIZE_BTN_3X3['w'] if self.kich_thuoc == 3 else SIZE_BTN_24X24['w']
        h = SIZE_BTN_3X3['h'] if self.kich_thuoc == 3 else SIZE_BTN_24X24['h']

        self.buttons = [] # Reset mảng nút
        for i in range(self.kich_thuoc):
            row_btns = []
            for j in range(self.kich_thuoc):
                # Tạo nút
                # command=lambda x=i, y=j: ... dùng để truyền tọa độ i,j vào hàm xử lý
                btn = tk.Button(game_area, text=" ", width=w, height=h, font=font_size,
                                command=lambda x=i, y=j: self.callback_click(x, y))
                # Sắp xếp nút theo lưới (dòng i, cột j)
                btn.grid(row=i, column=j)
                row_btns.append(btn)
            self.buttons.append(row_btns)

    def cap_nhat_o(self, x, y, text, color="black"):
        """Thay đổi nội dung và màu sắc của một ô tại (x,y)"""
        self.buttons[x][y].config(text=text, fg=color)

    def to_mau_thang(self, danh_sach_o):
        """Tô màu nền vàng cho các ô trong danh sách thắng"""
        for r, c in danh_sach_o:
            self.buttons[r][c].config(bg=COLOR_BG_WIN)

    def khoa_ban_co(self):
        """Vô hiệu hóa toàn bộ bàn cờ (không cho bấm nữa)"""
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")