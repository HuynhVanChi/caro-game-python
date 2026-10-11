# --====== [Imports] ======--
import random
from Logic_Caro import kiem_tra_thang_Bang3x3, kiem_tra_thang_Bang24x24, kiem_tra_hoa

# --====== [BẢNG ĐIỂM] ======--
SCORES = {
    'WIN': 100000000,
    'OPEN_4': 10000000,
    'CLOSED_4': 1000000,
    'OPEN_3': 1000000,
    'CLOSED_3': 1000,
    'OPEN_2': 100,
    'CLOSED_2': 10
}

# --====== [AI CLASS] ======--
class MasterAI:
    def __init__(self):
        self.reset()

    def reset(self):
        """Xóa sạch bộ nhớ ứng viên và đặt lại trạng thái ban đầu cho ván mới"""
        self.ung_vien = set()
        self.first_turn = True
        self.size_ban_co = 0

    # ==========================================
    # PHẦN 1: MINIMAX 3x3 (GIỮ NGUYÊN)
    # ==========================================
    def kiem_tra_full(self, Bang):
        for r in range(3):
            for c in range(3):
                if Bang[r][c] == "": return False
        return True

    def minimax(self, Bang, depth, is_maximizing):
        if kiem_tra_thang_Bang3x3(Bang, "O"): return 10 - depth
        if kiem_tra_thang_Bang3x3(Bang, "X"): return depth - 10
        if self.kiem_tra_full(Bang): return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if Bang[r][c] == "":
                        Bang[r][c] = "O"
                        score = self.minimax(Bang, depth + 1, False)
                        Bang[r][c] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if Bang[r][c] == "":
                        Bang[r][c] = "X"
                        score = self.minimax(Bang, depth + 1, True)
                        Bang[r][c] = ""
                        best_score = min(score, best_score)
            return best_score

    def find_best_move_3x3(self, Bang):
        # Đếm số quân đã đánh trên bàn cờ
        so_quan = sum(1 for r in range(3) for c in range(3) if Bang[r][c] != "")

        # 1. Nước đầu tiên (so_quan == 0): Máy đi trước -> Chiếm ngay ô giữa (1, 1)
        if so_quan == 0:
            return (1, 1)

        # 2. Nước thứ hai (so_quan == 1): Người đi trước 1 nước
        if so_quan == 1:
            # Nếu người chưa chiếm ô giữa -> Máy chiếm ngay ô giữa
            if Bang[1][1] == "":
                return (1, 1)
            # Nếu người đã chiếm ô giữa -> Máy chiếm góc (0, 0)
            return (0, 0)

        # 3. Từ nước thứ 2 trở đi: Không gian tìm kiếm hẹp, chạy Minimax tìm nước tối ưu
        best_score = -float('inf')
        best_move = None

        for r in range(3):
            for c in range(3):
                if Bang[r][c] == "":
                    Bang[r][c] = "O"
                    score = self.minimax(Bang, 0, False)
                    Bang[r][c] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    # ==========================================
    # PHẦN 2: HEURISTIC 24x24 (ĐÃ SỬA LỖI)
    # ==========================================
    def khoi_tao_ung_vien(self, Bang):
        self.ung_vien.clear()
        so_hang = len(Bang)
        so_cot = len(Bang[0])
        co_quan_co = False
        for r in range(so_hang):
            for c in range(so_cot):
                if Bang[r][c] != "": 
                    co_quan_co = True
                    self.them_vung_lan_can(Bang, r, c)
        if not co_quan_co:
            mid = so_hang // 2
            self.ung_vien.add((mid, mid))

    def them_vung_lan_can(self, Bang, x, y):
        so_hang = len(Bang)
        so_cot = len(Bang[0])
        # [NÂNG CẤP] Mở rộng bán kính lên 2 ô để không bị sót nước
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < so_hang and 0 <= ny < so_cot:
                    if Bang[nx][ny] == "":
                        self.ung_vien.add((nx, ny))

    def cap_nhat_lai_ung_vien(self, Bang):
        cac_o_can_xoa = set()
        danh_sach_copy = list(self.ung_vien)
        for r, c in danh_sach_copy:
            if Bang[r][c] != "":
                cac_o_can_xoa.add((r, c))
                self.them_vung_lan_can(Bang, r, c)
        self.ung_vien -= cac_o_can_xoa
        if not self.ung_vien: self.khoi_tao_ung_vien(Bang)

    def tinh_diem_24x24(self, count, enemy_block, wall_block=0):
        # 1. Đủ 5 con trở lên: Luật VN chỉ xử thua nếu bị 2 QUÂN ĐỐI THỦ chặn cả 2 đầu
        if count >= 5:
            if enemy_block < 2:
                return SCORES['WIN']
            return 0
        
        # 2. Dưới 5 con: Cả quân đối thủ lẫn mép bàn cờ đều cản trở mở rộng
        total_block = enemy_block + wall_block
        if total_block >= 2:
            return 0
        
        # 3. Các thế cờ tấn công khác
        if count == 4: return SCORES['OPEN_4'] if total_block == 0 else SCORES['CLOSED_4']
        if count == 3: return SCORES['OPEN_3'] if total_block == 0 else SCORES['CLOSED_3']
        if count == 2: return SCORES['OPEN_2'] if total_block == 0 else SCORES['CLOSED_2']
        return 0

    def danh_gia_o(self, Bang, r, c, player):
        so_hang = len(Bang)
        tong_diem = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        
        for dr, dc in directions:
            count = 1; enemy_block = 0; wall_block = 0
            # Xuôi
            i = 1
            while True:
                nr, nc = r + dr*i, c + dc*i
                if 0 <= nr < so_hang and 0 <= nc < so_hang:
                    if Bang[nr][nc] == player: count += 1
                    elif Bang[nr][nc] != "": enemy_block += 1; break
                    else: break
                else: wall_block += 1; break
                i += 1
            # Ngược
            i = 1
            while True:
                nr, nc = r - dr*i, c - dc*i
                if 0 <= nr < so_hang and 0 <= nc < so_hang:
                    if Bang[nr][nc] == player: count += 1
                    elif Bang[nr][nc] != "": enemy_block += 1; break
                    else: break
                else: wall_block += 1; break
                i += 1
            
            tong_diem += self.tinh_diem_24x24(count, enemy_block, wall_block)
                
        return tong_diem

    def find_best_move_24x24(self, Bang, ky_tu):
        if self.first_turn:
            self.khoi_tao_ung_vien(Bang)
            self.first_turn = False
        else:
            self.cap_nhat_lai_ung_vien(Bang)

        nguoi = "X" if ky_tu == "O" else "O"
        best_score = -1
        best_move = None
        danh_sach_can_tinh = list(self.ung_vien)

        for r, c in danh_sach_can_tinh:
            diem_tan_cong = self.danh_gia_o(Bang, r, c, ky_tu)
            diem_phong_thu = self.danh_gia_o(Bang, r, c, nguoi)
            diem_cuoi = diem_tan_cong + diem_phong_thu

            if diem_cuoi > best_score:
                best_score = diem_cuoi
                best_move = (r, c)
            
            # Ưu tiên thắng ngay lập tức
            if diem_tan_cong >= SCORES['WIN']: return (r, c)

        if best_move: return best_move
        return list(self.ung_vien)[0] if self.ung_vien else (len(Bang)//2, len(Bang)//2)

    # ==========================================
    # MAIN
    # ==========================================
    def tim_nuoc_di(self, Bang, ky_tu):
        current_size = len(Bang)
        if current_size != self.size_ban_co:
            self.size_ban_co = current_size
            self.ung_vien.clear()
            self.first_turn = True

        if current_size == 3:
            return self.find_best_move_3x3(Bang)
        else:
            return self.find_best_move_24x24(Bang, ky_tu)

# --====== [GLOBAL] ======--
bot = MasterAI()
def AI_nuoc_di(Bang, ky_tu):
    return bot.tim_nuoc_di(Bang, ky_tu)

def AI_reset():
    bot.reset()