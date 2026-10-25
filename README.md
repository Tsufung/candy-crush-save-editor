# 🍬 Candy Crush Saga - Save Game Editor (Web & Desktop)

[![GitHub Pages](https://img.shields.io/badge/Web%20Editor-Trực%20Tiếp%20Online-FF2A85?style=for-the-badge&logo=googlechrome&logoColor=white)](https://tsufung.github.io/candy-crush-save-editor/)
[![Platform](https://img.shields.io/badge/Hỗ%20Trợ-Windows%20|%20Android%20|%20iOS-00D2FC?style=for-the-badge)](https://tsufung.github.io/candy-crush-save-editor/)
[![Safety](https://img.shields.io/badge/An%20Toàn-100%25%20Không%20Mất%20Dữ%20Liệu-00F090?style=for-the-badge)](#-cơ-chế-sao-lưu-an-toàn)

> **Bộ công cụ mã nguồn mở chỉnh sửa file lưu dữ liệu game (`save_*.dat`) của Candy Crush Saga.**  
> Hỗ trợ **Web Editor trực tuyến trên trình duyệt (điện thoại & máy tính)** và **Ứng dụng Desktop GUI** hiện đại.

👉 **MỞ WEB TOOL DÙNG TRỰC TIẾP (KHÔNG CẦN CÀI ĐẶT):**  
🔗 [**https://tsufung.github.io/candy-crush-save-editor/**](https://tsufung.github.io/candy-crush-save-editor/)

---

## ⚠️ LƯU Ý BẮT BUỘC (VUI LÒNG ĐỌC KỸ TRƯỚC KHI DÙNG)

Để tránh hiểu nhầm về cơ chế hoạt động của game Candy Crush Saga, xin lưu ý:

| Mục | Hỗ Trợ | Giải Thích Chi Tiết |
| :--- | :---: | :--- |
| **❌ Vàng (Gold Bars)** | **KHÔNG HACK ĐƯỢC** | Thỏi vàng (Gold Bars) được **lưu trữ, mã hóa và kiểm soát 100% trên hệ thống máy chủ King (Server-side)**. Mỗi khi mở game, máy chủ sẽ đồng bộ số vàng về máy. Bất kỳ công cụ can thiệp offline nào cũng không thể sửa được số vàng. Những nơi quảng cáo "hack vàng Candy Crush" đều là lừa đảo. |
| **❌ Nước Đi (Moves trong ván)** | **KHÔNG HACK ĐƯỢC** | Số lượt đi của từng màn chơi được nạp động từ file cấu hình của game engine khi bắt đầu ván đấu, không lưu tĩnh trong file save inventory. |
| **✅ Vật Phẩm (Boosters)** | **HỖ TRỢ TỐI ĐA (65,535)** | Toàn bộ 12 loại bùa hỗ trợ trong kho đồ offline (Búa kẹo mút, Kẹo bom màu, Cá thạch, Đĩa bay UFO,...) đều lưu trữ dưới dạng byte offset chuẩn, có thể nạp tối đa **65,535 cái mỗi loại**! |
| **✅ Mạng Sống (Lives)** | **HỖ TRỢ BẤT TỬ (65,535)** | Mạng sống được nạp lên **65,535 lượt**, chơi thả ga không bao giờ phải chờ hồi tim hay xin mạng bạn bè! |

---

## 🎁 DANH MỤC CÁC VẬT PHẨM (BOOSTERS) ĐƯỢC HỖ TRỢ

Công cụ can thiệp chuẩn xác vào cấu trúc Byte Offset 16-bit Little-Endian của King Digital Entertainment:

1. ❤️ **Mạng Sống (Lives):** Bất tử 65,535 lượt chơi.
2. 💣 **Kẹo Bom Màu (Color Bomb):** Nổ sạch kẹo cùng màu được chọn trên bàn cờ.
3. 🍭 **Búa Kẹo Mút (Lollipop Hammer):** Đập vỡ ngay lập tức bất kỳ ô kẹo hay chướng ngại vật nào mà không tốn lượt đi.
4. 🐟 **Cá Thạch (Jelly Fish):** Thả cá bơi đi ăn các ô thạch khó nhất.
5. 🥥 **Bánh Xe Dừa (Coconut Wheel):** Lăn biến hàng loạt kẹo thành kẹo sọc.
6. 🖐️ **Bàn Tay Đổi Kẹo (Free Switch):** Hoán đổi vị trí 2 viên kẹo bất kỳ mà không tốn nước đi.
7. 🛸 **Đĩa Bay UFO (UFO Drops):** Bắn ra 3 kẹo bọc giấy và kích nổ diện rộng cực mạnh.
8. 🍬 **Kẹo May Mắn (Lucky Candy):** Biến thành đúng loại kẹo nhiệm vụ cần thu thập.
9. 🎁 **Kẹo Gói & Kẹo Sọc (Wrapped & Striped):** Khởi đầu ván đấu với combo kẹo đặc biệt.
10. 🎨 **Cọ Sơn Kẹo (Paint Brush / Sweet Teeth):** Tô màu kẹo hoặc ăn chướng ngại vật.
11. 🌙 **Bùa Mặt Trăng (Moonstruck):** Xóa bớt màu kẹo trên bàn để tạo chuỗi nổ liên hoàn.
12. ⏳ **Bùa Thêm Lượt Đi Trong Kho (+5 Extra Moves Booster):** Thêm 5 lượt đi khi bắt đầu màn.

---

## 🚀 HƯỚNG DẪN SỬ DỤNG

### CÁCH 1: DÙNG TRỰC TIẾP TRÊN WEB (ĐỀ XUẤT - DỄ NHẤT)
*Hoạt động trên mọi trình duyệt: Chrome, Safari, Edge, Cốc Cốc, trên cả điện thoại iPhone, Android và máy tính.*

1. Truy cập đường link: [**https://tsufung.github.io/candy-crush-save-editor/**](https://tsufung.github.io/candy-crush-save-editor/)
2. Kéo thả file **`save_*.dat`** của bạn vào ô màu hồng hoặc bấm nút **`[📁 Chọn File Save (.dat)]`**.
   *(Nếu chưa có file, bạn có thể bấm "✨ Tạo File Mẫu Test" để trải nghiệm trước).*
3. Bấm vào nút **`[⚡ MAX TẤT CẢ (65,535)]`** (hoặc tự gõ số lượng bùa mong muốn vào từng ô).
4. Bấm **`[💾 TẢI FILE SAVE ĐÃ HACK (.DAT)]`**.
5. Chép đè file vừa tải về vào đúng thư mục game trên thiết bị của bạn và mở Candy Crush Saga lên thưởng thức!

---

### CÁCH 2: DÙNG TOOL DESKTOP GUI (CHO MÁY TÍNH WINDOWS)
*Dành cho người chơi muốn quét tự động file save trên Windows hoặc kết nối điện thoại Android qua cáp USB.*

1. Tải toàn bộ mã nguồn của kho lưu trữ này về máy:
   - Bấm nút xanh **`Code`** > **`Download ZIP`** và giải nén.
2. Nhấp đúp chuột vào file **`CHAY_TOOL_HACK_SAVE_CANDY.bat`** (hoặc mở Terminal chạy: `python candy_save_hack_gui.py`).
3. Các tính năng độc quyền trên bản Desktop:
   - **`🔍 Tự Tìm Save PC`**: Tự động phát hiện thư mục lưu của game Candy Crush Saga cài từ Microsoft Store Windows.
   - **`🌟 Bơm Tất Cả Tài Khoản (King+FB)`**: 1 cú nhấp tự động quét, sao lưu và nạp full bùa cho mọi tài khoản (King, Facebook, Khách) có trên máy tính!
   - **`📱 Kéo từ Android (ADB)`** & **`📤 Đẩy ngay vào Android`**: Tự động rút file save từ điện thoại Android cắm cáp và nạp ngược lại chỉ bằng 1 nút bấm.

---

## 📍 VỊ TRÍ TÌM FILE `save_*.dat` TRÊN CÁC THIẾT BỊ

Tùy vào thiết bị bạn đang chơi game, file lưu dữ liệu có tên dạng `save_##########.dat`:

### 💻 1. Trên Máy Tính Windows (Cài qua Microsoft Store)
- Mở `File Explorer` (Windows + E), dán đường dẫn sau vào thanh địa chỉ:
  ```text
  %LOCALAPPDATA%\Packages\king.com.CandyCrushSaga_*\LocalState\
  ```
- *(Nếu dùng Tool Desktop GUI, bạn chỉ cần bấm nút "🔍 Tự Tìm Save PC" là tool sẽ tự mở ra ngay).*

### 📱 2. Trên Điện Thoại Android (Samsung, Xiaomi, Oppo,...)
File save nằm tại:
```text
/data/data/com.king.candycrushsaga/app_storage/save_*.dat
```
hoặc:
```text
/data/data/com.king.candycrushsaga/files/save_*.dat
```
- **Cách lấy:** Dùng các ứng dụng quản lý file như **MT Manager**, **MiXplorer** hoặc **ZArchiver** (yêu cầu quyền truy cập thư mục dữ liệu), copy file `save_*.dat` ra thư mục `/sdcard/Download/`, đưa lên Web Tool sửa xong dán đè ngược lại.

### 🍏 3. Trên iPhone / iPad (iOS)
- Kết nối iPhone/iPad với máy tính qua cáp Lightning/Type-C.
- Mở phần mềm quản lý miễn phí **3uTools** (hoặc iFunbox).
- Vào mục:
  ```text
  Apps > Candy Crush > View (Tài liệu ứng dụng) > Documents
  ```
- Copy file `save_*.dat` ra máy tính, mở [Web Editor](https://tsufung.github.io/candy-crush-save-editor/) chỉnh sửa rồi dán đè lại vào Documents.

---

## 🛡️ CƠ CHẾ SAO LƯU AN TOÀN
Công cụ được tích hợp sẵn cơ chế bảo vệ an toàn:
- Mỗi khi tải file save đã sửa, web tool luôn cho phép bạn tải kèm bản sao lưu **`.bak`** gốc.
- Tool Desktop sẽ tự động tạo file `save_*.dat.bak` trước khi ghi đè bất kỳ byte nào.
- Nếu muốn trở về trạng thái ban đầu, bạn chỉ cần xóa đuôi `.bak` và đổi tên lại thành `.dat`.

---

## 🔬 BẢNG TRA CỨU HEX OFFSET (CHO NHÀ PHÁT TRIỂN)

| Loại Bùa / Vật Phẩm | Tên Tiếng Anh | Địa chỉ Hex | Byte Offset | Định Dạng Dữ Liệu |
| :--- | :--- | :---: | :---: | :---: |
| **❤️ Mạng Sống (Lives)** | **Lives** | `0x0290` | **656** | 16-bit Unsigned Little-Endian |
| **💣 Kẹo Bom Màu** | Color Bomb | `0x0050` | **80** | 16-bit Unsigned Little-Endian |
| **🐟 Cá Thạch** | Jelly Fish | `0x005C` | **92** | 16-bit Unsigned Little-Endian |
| **🥥 Bánh Xe Dừa** | Coconut Wheel | `0x0068` | **104** | 16-bit Unsigned Little-Endian |
| **🍭 Búa Kẹo Mút** | Lollipop Hammer | `0x0074` | **116** | 16-bit Unsigned Little-Endian |
| **⏳ Bùa Thêm Lượt Đi** | Extra Moves Booster | `0x0080` | **128** | 16-bit Unsigned Little-Endian |
| **🍬 Kẹo May Mắn** | Lucky Candy | `0x0098` | **152** | 16-bit Unsigned Little-Endian |
| **🎁 Kẹo Gói & Kẹo Sọc** | Wrapped & Striped | `0x00A4` | **164** | 16-bit Unsigned Little-Endian |
| **🖐️ Bàn Tay Đổi Kẹo** | Free Switch / Hands | `0x00B0` | **176** | 16-bit Unsigned Little-Endian |
| **🌙 Kẹo Mặt Trăng** | Moonstruck | `0x00BC` | **188** | 16-bit Unsigned Little-Endian |
| **🛸 Đĩa Bay UFO** | UFO Drops | `0x00D4` | **212** | 16-bit Unsigned Little-Endian |
| **🎨 Cọ Sơn Kẹo** | Paint / Sweet Teeth | `0x00E0` | **224** | 16-bit Unsigned Little-Endian |

---

## ⚖️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM (DISCLAIMER)
- Dự án này được phát triển hoàn toàn vì mục đích giáo dục, nghiên cứu cấu trúc tập tin nhị phân và lưu trữ trò chơi ngoại tuyến.
- Mọi thương hiệu, nhãn hiệu dịch vụ, hình ảnh và tài sản trí tuệ liên quan đến *Candy Crush Saga* đều thuộc quyền sở hữu của **King Digital Entertainment plc** và **Activision Blizzard**.
- Tác giả không chịu trách nhiệm đối với bất kỳ vi phạm điều khoản dịch vụ nào do việc lạm dụng công cụ này gây ra.
