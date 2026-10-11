# --====== [Functions] ======-- Là nơi định nghĩa các hàm

# Hàm tạo bảng ban đầu
def Tao_Bang(so_hang, so_cot):
    """Tạo bàn cờ trống với kích thước so_hang x so_cot"""
    Bang = []
    for hang in range(so_hang):
        dong = [""] * so_cot  # Tạo dòng mới nhanh gọn
        Bang.append(dong)
    return Bang

# Hàm đánh dấu nước đi
def danh_dau(Bang, hang, cot, ky_tu):
    """Đánh dấu ô nếu ô đó còn trống"""
    if 0 <= hang < len(Bang) and 0 <= cot < len(Bang[0]):
        if Bang[hang][cot] == "":
            Bang[hang][cot] = ky_tu
            return True
    return False

# Hàm kiểm tra hòa
def kiem_tra_hoa(Bang):
    """Trả về True nếu bàn cờ đã đầy và không còn ô trống"""
    for hang in Bang:
        if "" in hang: # Cách kiểm tra nhanh hơn
            return False
    return True

# --- [LOGIC 3x3] ---
def kiem_tra_thang_Bang3x3(Bang, ky_tu):
    """
    Kiểm tra thắng trên bảng 3x3 (Tic-Tac-Toe).
    Luật: Cứ đủ 3 con thẳng hàng là thắng, không quan tâm bị chặn.
    Trả về: Danh sách các ô thắng [(r1,c1), (r2,c2),...] hoặc None.
    """
    kich_thuoc = len(Bang)
    
    # Kiểm tra Hàng
    for i in range(kich_thuoc):
        if all(Bang[i][j] == ky_tu for j in range(kich_thuoc)):
            return [(i, j) for j in range(kich_thuoc)]
            
    # Kiểm tra Cột
    for j in range(kich_thuoc):
        if all(Bang[i][j] == ky_tu for i in range(kich_thuoc)):
            return [(i, j) for i in range(kich_thuoc)]
            
    # Kiểm tra Chéo Chính
    if all(Bang[i][i] == ky_tu for i in range(kich_thuoc)):
        return [(i, i) for i in range(kich_thuoc)]
        
    # Kiểm tra Chéo Phụ
    if all(Bang[i][kich_thuoc - 1 - i] == ky_tu for i in range(kich_thuoc)):
        return [(i, kich_thuoc - 1 - i) for i in range(kich_thuoc)]
    
    return None

# --- [LOGIC 24x24 - ĐÃ NÂNG CẤP LUẬT CHẶN 2 ĐẦU] ---
def kiem_tra_thang_Bang24x24(Bang, ky_tu, hang, cot):
    """
    Kiểm tra thắng trên bảng 24x24 (Gomoku).
    Luật: 
    1. Phải có ít nhất 5 quân liên tiếp.
    2. Nếu bị chặn 2 đầu bởi quân đối thủ -> KHÔNG TÍNH THẮNG.
       (Ví dụ: O X X X X X O -> X chưa thắng).
    """
    kich_thuoc = len(Bang)
    huong = [
        (0, 1),   # Ngang
        (1, 0),   # Dọc
        (1, 1),   # Chéo chính
        (1, -1)   # Chéo phụ
    ]
    
    # Xác định đối thủ để kiểm tra chặn
    doi_thu = "O" if ky_tu == "X" else "X"

    for dx, dy in huong:
        duong_thang = [(hang, cot)]
        bi_chan_dau = 0 # Đếm số đầu bị chặn

        # 1. Kiểm tra xuôi (Positive direction)
        i, j = hang + dx, cot + dy
        while 0 <= i < kich_thuoc and 0 <= j < kich_thuoc:
            if Bang[i][j] == ky_tu:
                duong_thang.append((i, j))
                i += dx
                j += dy
            elif Bang[i][j] == doi_thu:
                bi_chan_dau += 1
                break
            else: # Gặp ô trống
                break

        # 2. Kiểm tra ngược (Negative direction)
        i, j = hang - dx, cot - dy
        while 0 <= i < kich_thuoc and 0 <= j < kich_thuoc:
            if Bang[i][j] == ky_tu:
                duong_thang.append((i, j))
                i -= dx
                j -= dy
            elif Bang[i][j] == doi_thu:
                bi_chan_dau += 1
                break
            else: # Gặp ô trống
                break

        # 3. KẾT LUẬN
        # Đủ 5 con TRỞ LÊN và KHÔNG bị chặn 2 đầu
        if len(duong_thang) >= 5:
            if bi_chan_dau < 2:
                return duong_thang
            else:
                # Nếu bị chặn 2 đầu (bi_chan_dau == 2), bỏ qua hàng này
                continue 
        
    return None