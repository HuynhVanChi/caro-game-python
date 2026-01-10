# --====== [Imports] ======--
import random
from Logic_Caro import kiem_tra_thang_Bang3x3, kiem_tra_thang_Bang24x24

# --====== [AI CLASS] ======--
class MasterAI:
    def __init__(self):
        self.ung_vien = set() # Bộ nhớ lưu các ô cần quan tâm
        self.first_turn = True # Biến kiểm tra xem có phải lượt đầu không

    def khoi_tao_ung_vien(self, Bang):
        """Quét toàn bộ bàn cờ để tìm các ô xung quanh những quân đã đánh"""
        self.ung_vien.clear()
        so_hang = len(Bang)
        so_cot = len(Bang[0])
        co_quan_co = False

        for r in range(so_hang):
            for c in range(so_cot):
                if Bang[r][c] != "": 
                    co_quan_co = True
                    self.them_vung_lan_can(Bang, r, c)
        
        # Nếu bàn cờ trắng tinh, thêm tâm bàn cờ vào
        if not co_quan_co:
            mid = so_hang // 2
            self.ung_vien.add((mid, mid))

    def them_vung_lan_can(self, Bang, x, y):
        """Thêm 8 ô xung quanh (x, y) vào danh sách ứng viên"""
        so_hang = len(Bang)
        so_cot = len(Bang[0])
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < so_hang and 0 <= ny < so_cot:
                    if Bang[nx][ny] == "":
                        self.ung_vien.add((nx, ny))

    def cap_nhat_lai_ung_vien(self, Bang):
        """
        AI tự quét lại danh sách ứng viên để loại bỏ các ô đã bị đánh.
        """
        cac_o_can_xoa = set()
        
        # Dùng list(self.ung_vien) để tạo bản sao, tránh lỗi "Set changed size"
        danh_sach_copy = list(self.ung_vien) 

        for r, c in danh_sach_copy:
            if Bang[r][c] != "": # Nếu ô này không còn trống
                cac_o_can_xoa.add((r, c))
                # Mở rộng vùng tìm kiếm xung quanh ô vừa bị đánh
                self.them_vung_lan_can(Bang, r, c)
        
        self.ung_vien -= cac_o_can_xoa

        if not self.ung_vien:
            self.khoi_tao_ung_vien(Bang)

    def tim_nuoc_di(self, Bang, ky_tu):
        # 1. Cập nhật danh sách ứng viên
        if self.first_turn:
            self.khoi_tao_ung_vien(Bang)
            self.first_turn = False
        else:
            self.cap_nhat_lai_ung_vien(Bang)

        nguoi = "X" if ky_tu == "O" else "O"
        so_hang = len(Bang)

        # Lấy danh sách cần duyệt
        danh_sach_can_tinh = list(self.ung_vien)
        
        # Debug: In ra số lượng ô cần tính
        print(f"🔍 Số ô tính toán: {len(danh_sach_can_tinh)}")

        # ===== Ưu tiên 1: Thử thắng ngay =====
        for r, c in danh_sach_can_tinh:
            Bang[r][c] = ky_tu
            is_win = False
            if so_hang == 3: is_win = kiem_tra_thang_Bang3x3(Bang, ky_tu)
            else: is_win = kiem_tra_thang_Bang24x24(Bang, ky_tu, r, c)
            
            Bang[r][c] = "" # Trả lại hiện trạng
            
            if is_win:
                print("🤖 AI: Thắng!")
                return (r, c)

        # ===== Ưu tiên 2: Chặn người chơi =====
        for r, c in danh_sach_can_tinh:
            Bang[r][c] = nguoi
            is_lose = False
            if so_hang == 3: is_lose = kiem_tra_thang_Bang3x3(Bang, nguoi)
            else: is_lose = kiem_tra_thang_Bang24x24(Bang, nguoi, r, c)
            
            Bang[r][c] = "" # Trả lại hiện trạng

            if is_lose:
                print("🛡️ AI: Chặn!")
                return (r, c)

        # ===== Ưu tiên 3: Random =====
        if danh_sach_can_tinh:
            return random.choice(danh_sach_can_tinh)
        
        return (so_hang//2, so_hang//2)

# --====== [GLOBAL OBJECT] ======--
bot = MasterAI()

# --====== [INTERFACE FUNCTION] ======--
def AI_nuoc_di(Bang, ky_tu):
    return bot.tim_nuoc_di(Bang, ky_tu)