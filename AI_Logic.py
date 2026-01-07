# --====== [Imports] ======--
from random import randint
from Logic_Caro import kiem_tra_thang_Bang3x3, kiem_tra_thang_Bang24x24

# --====== [Functions] ======--
def AI_nuoc_di(Bang, ky_tu):
    """
    AI cấp 2:
    - Ưu tiên 1: nếu có thể thắng thì đánh luôn
    - Ưu tiên 2: nếu người chơi sắp thắng thì chặn
    - Ưu tiên 3: nếu không có gì đặc biệt thì đánh ngẫu nhiên
    """

    so_hang = len(Bang)
    so_cot = len(Bang[0])

    # Xác định ký tự người chơi
    nguoi = "X" if ky_tu == "O" else "O"

    # ===== Ưu tiên 1: Thử thắng ngay =====
    for i in range(so_hang):
        for j in range(so_cot):
            if Bang[i][j] == "":
                Bang[i][j] = ky_tu
                if (so_hang == 3 and kiem_tra_thang_Bang3x3(Bang, ky_tu)) or \
                   (so_hang > 3 and kiem_tra_thang_Bang24x24(Bang, ky_tu, i, j)):
                    print("🤖 Máy đánh để thắng tại:", i, j)
                    return (i, j)
                Bang[i][j] = ""

    # ===== Ưu tiên 2: Chặn người chơi =====
    for i in range(so_hang):
        for j in range(so_cot):
            if Bang[i][j] == "":
                Bang[i][j] = nguoi
                if (so_hang == 3 and kiem_tra_thang_Bang3x3(Bang, nguoi)) or \
                   (so_hang > 3 and kiem_tra_thang_Bang24x24(Bang, nguoi, i, j)):
                    Bang[i][j] = ky_tu
                    print("🛡️  Máy chặn người chơi tại:", i, j)
                    return (i, j)
                Bang[i][j] = ""

    # ===== Ưu tiên 3: Random nếu không có nước tốt =====
    while True:
        may_x = randint(0, so_hang - 1)
        may_y = randint(0, so_cot - 1)
        if Bang[may_x][may_y] == "":
            Bang[may_x][may_y] = ky_tu
            print("🎲 Máy đánh ngẫu nhiên tại:", may_x, may_y)
            return (may_x, may_y)
    
    
