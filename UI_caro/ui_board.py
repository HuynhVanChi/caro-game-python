import tkinter as tk
from tkinter import Canvas
from .config import *
import tkinter.font as tkfont # Import để chỉnh font động

class BoardView:
    def __init__(self, parent_frame, kich_thuoc, callback_click):
        self.frame = parent_frame
        self.kich_thuoc = kich_thuoc
        self.callback_click = callback_click
        self.buttons = [] 
        self.last_move_btn = None 
        self.tao_ban_co()

    def tao_ban_co(self):
        for widget in self.frame.winfo_children(): widget.destroy()

        # --- TRƯỜNG HỢP 1: BÀN CỜ LỚN (24x24) ---
        # Với bàn lớn, ta KHÔNG phóng to nút (vì sẽ rất xấu), mà ta phóng to VÙNG NHÌN (Canvas)
        if self.kich_thuoc > 10: 
            canvas = Canvas(self.frame, bg=COLOR_BG, highlightthickness=0)
            vsb = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
            hsb = tk.Scrollbar(self.frame, orient="horizontal", command=canvas.xview)
            canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            vsb.pack(side="right", fill="y")
            hsb.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)
            
            game_area = tk.Frame(canvas, bg=COLOR_BG) 
            canvas.create_window((0,0), window=game_area, anchor="nw")
            
            game_area.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            # Vẽ nút (Kích thước cố định, dùng thanh cuộn)
            self.buttons = []
            for i in range(self.kich_thuoc):
                row_btns = []
                for j in range(self.kich_thuoc):
                    btn = tk.Button(
                        game_area, text="", font=FONT_TEXT_BOARD,
                        width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg=COLOR_BTN_BG,
                        command=lambda x=i, y=j: self.callback_click(x, y)
                    )
                    btn.grid(row=i, column=j, padx=0, pady=0)
                    row_btns.append(btn)
                self.buttons.append(row_btns)

        # --- TRƯỜNG HỢP 2: BÀN CỜ NHỎ (3x3) ---
        # Bàn nhỏ cần co giãn (Responsive) toàn màn hình
        else:
            game_area = self.frame
            
            # 1. Cấu hình để lưới Grid tự động chia đều không gian
            for i in range(self.kich_thuoc):
                game_area.grid_rowconfigure(i, weight=1, uniform="row_group")
                game_area.grid_columnconfigure(i, weight=1, uniform="col_group")

            self.buttons = []
            for i in range(self.kich_thuoc):
                row_btns = []
                for j in range(self.kich_thuoc):
                    btn = tk.Button(
                        game_area, text="", font=FONT_TEXT_BOARD,
                        bg=COLOR_BTN_BG,
                        relief="raised", bd=2,
                        # Không set width/height cứng nữa để nó tự giãn
                        command=lambda x=i, y=j: self.callback_click(x, y)
                    )
                    # 2. sticky="nsew" -> để nút bám chặt vào 4 góc ô lưới
                    btn.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                    row_btns.append(btn)
                self.buttons.append(row_btns)

            # Tự động chỉnh cỡ chữ khi kéo thả cửa sổ
            game_area.bind("<Configure>", self.cap_nhat_co_chu)

    def cap_nhat_co_chu(self, event):
        """Hàm tính toán cỡ chữ dựa trên độ lớn cửa sổ"""
        if self.kich_thuoc > 10: return # Không áp dụng cho bàn 24x24

        # Lấy chiều cao mới của cửa sổ chia cho số ô
        new_height = event.height // self.kich_thuoc
        # Công thức ước lượng cỡ chữ (khoảng 1/3 chiều cao ô)
        new_size = max(10, int(new_height * 0.25)) 
        
        # Tạo font mới
        dynamic_font = tkfont.Font(family="Arial", size=new_size, weight="bold")
        
        # Cập nhật font cho toàn bộ nút
        for row in self.buttons:
            for btn in row:
                btn.config(font=dynamic_font)

    def cap_nhat_o(self, r, c, ky_tu, mau_sac):
        self.buttons[r][c].config(text=ky_tu, fg=mau_sac)

    def highlight_nuoc_di(self, r, c):
        if self.last_move_btn is not None:
            try:
                # Kiểm tra màu hiện tại, nếu không phải màu thắng thì trả về màu gốc
                if self.last_move_btn.cget("bg") != COLOR_WIN_BG:
                    self.last_move_btn.config(bg=COLOR_BTN_BG)
            except: pass 
        btn_moi = self.buttons[r][c]
        # Khi đổi màu nền, do đã set relief="raised" ở trên nên nút sẽ KHÔNG bị mất viền
        btn_moi.config(bg=COLOR_LAST_MOVE)
        self.last_move_btn = btn_moi

    def to_mau_thang(self, danh_sach_o_thang):
        if not danh_sach_o_thang: return
        for r, c in danh_sach_o_thang: self.buttons[r][c].config(bg=COLOR_WIN_BG)

    def khoa_ban_co(self):
        for hang in self.buttons:
            for btn in hang: btn.config(state="disabled")