# KẾ HOẠCH CẢI TIẾN & DANH SÁCH CÔNG VIỆC (ROADMAP)
## Dự án: Caro Game Python (Tkinter + Heuristic/Minimax AI)

> **Mục tiêu:** Khắc phục triệt để các xung đột logic, tối ưu hóa bộ nhớ AI, cải thiện trải nghiệm người dùng (UX) và nâng cao hiệu năng giao diện đồ họa.  
> **Cách sử dụng:** Đánh dấu `[X]` vào ô vuông khi đã hoàn thành từng mục công việc.

---

## 📊 BẢNG TỔNG QUAN TIẾN ĐỘ

- [X] **Giai đoạn 1:** Sửa lỗi cốt lõi & Xung đột logic (P0 - Cấp bách)
- [ ] **Giai đoạn 2:** Nâng cấp trải nghiệm người dùng & Luật chơi (P1 - Ưu tiên cao)
- [ ] **Giai đoạn 3:** Nâng cấp trí tuệ nhân tạo AI (P2 - Nâng cao)
- [ ] **Giai đoạn 4:** Tối ưu hóa hiệu năng & Thẩm mỹ giao diện (P3 - Hoàn thiện)

---

## 🛠️ CHI TIẾT CÁC HẠNG MỤC THEO THỨ TỰ THỰC HIỆN

### GIAI ĐOẠN 1: SỬA LỖI CỐT LÕI & XUNG ĐỘT LOGIC (P0 - BẮT BUỘC SỬA TRƯỚC)
*Giai đoạn này tập trung loại bỏ các lỗi khiến game chạy sai luật hoặc AI có hành vi bất thường.*

- [X] **1.1. Đồng bộ luật chặn 2 đầu giữa Trọng tài và AI**
  - **Hiện trạng:** `Logic_Caro.py` quy định 5 quân bị chặn 2 đầu thì *không tính thắng*, nhưng `AI_Logic.py` lại định nghĩa: *5 quân thắng luôn bất chấp bị chặn 2 đầu*. AI sẽ tự sát vào các thế cờ bị chặn 2 đầu vì tưởng mình đã thắng.
  - **Giải pháp:** Cập nhật hàm `tinh_diem_24x24()` trong `AI_Logic.py`: Nếu `block == 2` thì trả về điểm `0`, không cho ăn điểm thắng.
  - **File ảnh hưởng:** `AI_Logic.py`

- [X] **1.2. Khắc phục lỗi ô nhiễm trạng thái và rò rỉ bộ nhớ của AI**
  - **Hiện trạng:** Đối tượng `bot = MasterAI()` là biến toàn cục. Khi bấm "Chơi lại" cùng kích thước bàn cờ, biến `self.ung_vien` và cờ `self.first_turn` không được dọn dẹp. AI ván mới vẫn giữ nước đi của ván cũ và đánh vào các vị trí vô nghĩa.
  - **Giải pháp:** Bổ sung phương thức `reset()` trong class `MasterAI` để xóa sạch `ung_vien` và đặt `first_turn = True`. Gọi `bot.reset()` trong hàm `bat_dau_game()` ở `ui_main.py`.
  - **File ảnh hưởng:** `AI_Logic.py`, `UI_caro/ui_main.py`

- [X] **1.3. Sửa lỗi kiểm tra bàn cờ trống ở chế độ 3x3**
  - **Hiện trạng:** Hàm `tim_nuoc_di()` kiểm tra `if self.kiem_tra_full(Bang) and self.first_turn:`. Bàn cờ lúc mới bắt đầu thì trống (`""`), không bao giờ `full`, dẫn tới việc AI lập tức bị gán `first_turn = False` ngay từ nước đầu tiên.
  - **Giải pháp:** Sửa điều kiện thành kiểm tra bàn cờ trống (`kiem_tra_empty`) hoặc đếm số quân đã đánh.
  - **File ảnh hưởng:** `AI_Logic.py`

- [X] **1.4. Chuẩn hóa luật chạm mép bàn cờ (Edge Rule)**
  - **Hiện trạng:** Trong `Logic_Caro.py`, việc chạm rìa ngoài bàn cờ đang bị coi như gặp 1 quân chặn của đối thủ (`bi_chan_dau += 1`). Dẫn tới người chơi có 5 quân sát mép và 1 đầu kia bị chặn thì bị tính là chặn 2 đầu và không được thắng.
  - **Giải pháp:** Tách biệt khái niệm "chạm mép bàn cờ" và "bị quân đối phương chặn". Theo luật Caro chuẩn, chỉ tính là chặn khi đầu mút có quân đối phương.
  - **File ảnh hưởng:** `Logic_Caro.py`

---

### GIAI ĐOẠN 2: TRẢI NGHIỆM NGƯỜI DÙNG & TÍNH NĂNG CỐT LÕI (P1)
*Giai đoạn này giúp người chơi cảm thấy thuận tiện, kiểm soát ván đấu tốt hơn và giảm ức chế khi thao tác.*

- [ ] **2.1. Bổ sung kích thước chuẩn 15x15 (Gomoku/Caro tiêu chuẩn)**
  - **Hiện trạng:** Bàn cờ chỉ có 3x3 (quá bé, nhanh chán) và 24x24 (quá to, phải cuộn scrollbar mỏi tay).
  - **Giải pháp:** Thêm tùy chọn kích thước 15x15 vào menu chọn bàn cờ. Bàn 15x15 hiển thị vừa khít toàn màn hình mà không cần thanh cuộn.
  - **File ảnh hưởng:** `UI_caro/ui_main.py`, `UI_caro/ui_board.py`

- [ ] **2.2. Cho phép người chơi chọn quân cờ / Lượt đi trước - sau**
  - **Hiện trạng:** Người chơi luôn bị gán là X (đi trước) và AI luôn là O (đi sau).
  - **Giải pháp:** Thêm màn hình hoặc nút chọn: Cầm X (Đi trước) hoặc Cầm O (Đi sau). Nếu người chơi chọn O, AI sẽ tự động đi nước đầu tiên ở giữa bàn cờ.
  - **File ảnh hưởng:** `UI_caro/ui_main.py`, `AI_Logic.py`

- [ ] **2.3. Bổ sung tính năng Hoàn tác (Undo / Đi lại)**
  - **Hiện trạng:** Bấm nhầm một ô là không thể sửa sai, hỏng cả ván cờ.
  - **Giải pháp:** Tạo stack lưu lịch sử nước đi `[(r, c, player)]`. Khi bấm "Undo", xóa 1 nước (ở chế độ 2 người) hoặc 2 nước (ở chế độ đấu máy) và cập nhật lại giao diện + tập ứng viên của AI.
  - **File ảnh hưởng:** `UI_caro/ui_main.py`, `UI_caro/ui_board.py`, `AI_Logic.py`

- [ ] **2.4. Thêm nút "Chơi lại nhanh" và "Đầu hàng / Cầu hòa"**
  - **Hiện trạng:** Muốn chơi lại phải bấm nút `Menu` rồi mới bấm `Chơi lại` trên popup.
  - **Giải pháp:** Bổ sung thanh nút thao tác nhanh trên top bar: `[Chơi lại]` `[Đi lại]` `[Menu]` `[Đầu hàng]`.
  - **File ảnh hưởng:** `UI_caro/ui_main.py`

- [ ] **2.5. Hiển thị tọa độ bàn cờ (A-O, 1-15)**
  - **Hiện trạng:** Bàn cờ là các ô trống trơn không có nhãn định vị.
  - **Giải pháp:** Vẽ nhãn cột (A, B, C...) và nhãn hàng (1, 2, 3...) ở mép bàn cờ giúp người chơi định vị và trao đổi nước đi dễ dàng.
  - **File ảnh hưởng:** `UI_caro/ui_board.py`

---

### GIAI ĐOẠN 3: NÂNG CẤP CHIỀU SÂU THUẬT TOÁN AI (P2)
*Giai đoạn này giúp AI đánh thông minh, có tính chiến thuật và không bị rơi vào các bẫy cơ bản.*

- [ ] **3.1. Nhận diện các thế cờ ngắt quãng (Broken Patterns / Gaps)**
  - **Hiện trạng:** AI chỉ quét các quân liền kề liên tục (`else: break`). Không nhận diện được các thế nguy hiểm như `X_XX`, `XX_X`, `X_X_X`.
  - **Giải pháp:** Cải tiến hàm duyệt tia: Cho phép quét qua tối đa 1 ô trống để nhận biết các chuỗi hở nguy hiểm và chấm điểm tương ứng.
  - **File ảnh hưởng:** `AI_Logic.py`

- [ ] **3.2. Nhận diện và hóa giải nước đôi (Double Threats: 3-3, 4-3)**
  - **Hiện trạng:** AI chỉ cộng dồn điểm `diem_tan_cong + diem_phong_thu`, dễ bị ảo giác điểm số thay vì chặn các vị trí tạo nĩa đôi.
  - **Giải pháp:** Đếm số lượng đường 3 hở (`open_3_count`) và đường 4 (`four_count`) tạo ra sau mỗi nước đi. Nếu phát hiện đối thủ có thể tạo ra nước đôi (vừa 3 vừa 4, hoặc hai đường 3), gán trọng số ưu tiên chặn khẩn cấp.
  - **File ảnh hưởng:** `AI_Logic.py`

- [ ] **3.3. Tổng quát hóa Minimax 3x3**
  - **Hiện trạng:** Minimax đang gán cứng `O` tối đa hóa và `X` tối thiểu hóa.
  - **Giải pháp:** Tham số hóa quân của AI (`ai_player`, `human_player`) để Minimax chạy chính xác bất kể AI cầm quân nào.
  - **File ảnh hưởng:** `AI_Logic.py`

- [ ] **3.4. Thêm các mức độ khó cho AI (Dễ / Vừa / Khó)**
  - **Hiện trạng:** Chỉ có 1 mức chơi duy nhất.
  - **Giải pháp:** 
    - *Dễ:* AI ngẫu nhiên chọn trong top 5 nước có điểm khá, đôi khi bỏ qua nước phòng thủ.
    - *Vừa:* AI đánh Heuristic cơ bản hiện tại.
    - *Khó:* AI Heuristic nâng cao có nhận diện nước đôi + khoảng trống.
  - **File ảnh hưởng:** `AI_Logic.py`, `UI_caro/ui_main.py`

---

### GIAI ĐOẠN 4: HIỆU NĂNG & THẨM MỸ GIAO DIỆN (P3)
*Giai đoạn này nâng tầm dự án thành một sản phẩm chỉn chu, chuyên nghiệp.*

- [ ] **4.1. Chuyển đổi cách dựng bàn cờ sang 1 Canvas duy nhất (Canvas-based Board)**
  - **Hiện trạng:** Sử dụng hàng trăm widget `tk.Button` gây tốn bộ nhớ, giật lag khi tải lại bàn cờ lớn.
  - **Giải pháp:** Dùng 1 đối tượng `tk.Canvas` duy nhất, bắt sự kiện click chuột `<Button-1>` tính tọa độ `(r, c) = (y // cell_size, x // cell_size)`, sau đó vẽ đường kẻ và hình tròn quân cờ.
  - **File ảnh hưởng:** `UI_caro/ui_board.py`

- [ ] **4.2. Hiện đại hóa phong cách đồ họa (UI Theme)**
  - **Hiện trạng:** Màu sắc mặc định Windows (`SystemButtonFace`), nút chữ nhật cũ kỹ.
  - **Giải pháp:** Thiết kế lại bảng màu theo phong cách cờ gỗ (Wood theme) hoặc Modern Flat (Dark/Light mode); vẽ quân cờ hình tròn nổi bật với hiệu ứng bóng đổ hoặc viền tinh tế.
  - **File ảnh hưởng:** `UI_caro/config.py`, `UI_caro/ui_board.py`

- [ ] **4.3. Bảng điểm (Scoreboard) và Đồng hồ đếm giờ (Timer)**
  - **Hiện trạng:** Không lưu số trận thắng/thua, không giới hạn thời gian suy nghĩ.
  - **Giải pháp:** Thêm hiển thị tỉ số tích lũy (Người 1 vs Người 2, hoặc Người vs Máy) và đồng hồ đếm ngược cho mỗi lượt đi (ví dụ: 30s/lượt).
  - **File ảnh hưởng:** `UI_caro/ui_main.py`

- [ ] **4.4. Hiệu ứng âm thanh (Audio Feedback)**
  - **Hiện trạng:** Trò chơi hoàn toàn im lặng.
  - **Giải pháp:** Tích hợp module phát âm thanh (dùng thư viện nhẹ như `winsound` trên Windows hoặc `pygame.mixer`): tiếng đặt cờ lách cách, tiếng chuông thắng cuộc, âm thanh báo thua.
  - **File ảnh hưởng:** `UI_caro/ui_main.py`, tạo thư mục `assets/sounds/`

---

## 📋 BẢNG ĐỐI CHIẾU KIỂM THỬ (TEST MATRIX)

Sau khi hoàn thành từng phần, tích `[X]` vào các kịch bản kiểm thử tương ứng:

- [ ] **Test Case 1:** Người chơi xếp 5 quân X nhưng bị 2 quân O chặn 2 đầu -> Game KHÔNG công nhận thắng (đúng luật VN).
- [ ] **Test Case 2:** Bắt đầu ván mới sau khi chơi xong ván trước trên cùng bàn 24x24 -> AI không đánh vào tọa độ của ván cũ.
- [ ] **Test Case 3:** Chơi chế độ 3x3 nhiều ván liên tiếp -> AI vẫn đánh đúng Minimax từ nước đầu.
- [ ] **Test Case 4:** Bấm Undo liên tục -> Trạng thái bàn cờ và lượt đi lùi lại chính xác.
- [ ] **Test Case 5:** Kéo giãn kích thước cửa sổ -> Giao diện không bị tràn hoặc vỡ layout.
