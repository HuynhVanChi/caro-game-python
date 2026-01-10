# --====== [Imports] ======-- Là nơi chứa các thư viện cần thiết

# --====== [Constants] ======-- Là nơi chứa các hằng số

# --====== [Variables] ======-- Là nơi khai báo các biến toàn cục

# --====== [Functions] ======-- Là nơi định nghĩa các hàm

# Hàm tạo bảng ban đầu
def Tao_Bang(so_hang, so_cot):
    Bang = [] # Khởi tạo list trống
    for hang in range(so_hang):
        dong = []  # Tạo 1 hàng trống
        for cot in range(so_cot):
            dong.append("")  # Thêm ô trống vào hàng
        Bang.append(dong)  # Thêm hàng vào bảng
    return Bang

# Hàm dưới kiểm tra còn trống không
def danh_dau(Bang, hang,cot, ky_tu):
    if Bang[hang][cot] == "":
        Bang[hang][cot] = ky_tu
        return True
    else:
        return False

# Hàm kiểm tra thắng của Bảng 3x3
def kiem_tra_thang_Bang3x3(Bang,ky_tu):
    """Kiểm tra thắng trên bảng 3x3 và trả về danh sách ô thắng nếu có"""
    kich_thuoc = len(Bang)
    # Hàng
    for i in range(kich_thuoc):
        if all(Bang[i][j] == ky_tu for j in range(kich_thuoc)):
            return [(i, j) for j in range(kich_thuoc)]
    # Cột
    for j in range(kich_thuoc):
        if all(Bang[i][j] == ky_tu for i in range(kich_thuoc)):
            return [(i, j) for i in range(kich_thuoc)]
    # Đường chéo chính
    if all(Bang[i][i] == ky_tu for i in range(kich_thuoc)):
        return [(i, i) for i in range(kich_thuoc)]
    # Đường chéo phụ
    if all(Bang[i][kich_thuoc - 1 - i] == ky_tu for i in range(kich_thuoc)):
        return [(i, kich_thuoc - 1 - i) for i in range(kich_thuoc)]
    
    return None

# Hàm kiểm tra thắng Bảng 24x24
def kiem_tra_thang_Bang24x24(Bang,ky_tu,hang,cot):
    """
    Kiểm tra thắng trên bảng 24x24: thắng khi có 5 ô liên tiếp theo hàng, cột, hoặc chéo.
    Trả về danh sách ô thắng nếu có, ngược lại trả về None.
    """
    kich_thuoc = len(Bang)
    huong = [
        (0, 1),   # Ngang
        (1, 0),   # Dọc
        (1, 1),   # Chéo chính
        (1, -1)   # Chéo phụ
    ]

    for dx, dy in huong:
        duong_thang = [(hang, cot)]

        # Kiểm tra xuôi
        i, j = hang + dx, cot + dy
        while 0 <= i < kich_thuoc and 0 <= j < kich_thuoc and Bang[i][j] == ky_tu:
            duong_thang.append((i, j))
            i += dx
            j += dy

        # Kiểm tra ngược
        i, j = hang - dx, cot - dy
        while 0 <= i < kich_thuoc and 0 <= j < kich_thuoc and Bang[i][j] == ky_tu:
            duong_thang.append((i, j))
            i -= dx
            j -= dy

        # Nếu có 5 ô liên tiếp
        if len(duong_thang) >= 5:
            return duong_thang
        
    return None

# Hàm kiểm tra hòa
def kiem_tra_hoa(Bang):
    for hang in Bang:
        for o in hang:
            if o == "":
                return False
    return True

