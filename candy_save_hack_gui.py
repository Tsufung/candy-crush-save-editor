"""
=============================================================================
CANDY CRUSH SAGA - BỘ CÔNG CỤ CHỈNH SỬA FILE SAVE (SAVE GAME EDITOR)
Dựa trên kiến trúc Hex Offset chuẩn của King Digital Entertainment
Hỗ trợ file save_*.dat trên:
  - Windows PC (Microsoft Store / Windows App)
  - Android (Root / ADB / Note 10+)
  - iOS (iFunbox / Filza / Documents)
=============================================================================
"""

import os
import sys
import struct
import shutil
import subprocess
import glob
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Bảng danh mục Booster và vị trí Byte Offset chuẩn (16-bit Unsigned Little-Endian)
BOOSTER_DEFINITIONS = [
    {
        "id": "lives",
        "name_vi": "Mạng sống (Lives)",
        "name_en": "Lives",
        "icon": "❤️",
        "offset": 656,      # 0x290
        "hex": "0x0290",
        "desc": "Số lượt chơi bất tử, không cần chờ hồi mạng",
        "default": 65535,
        "color": "#FF4D6D"
    },
    {
        "id": "color_bomb",
        "name_vi": "Kẹo Bom Màu (Color Bomb)",
        "name_en": "Color Bomb",
        "icon": "💣",
        "offset": 80,       # 0x50
        "hex": "0x0050",
        "desc": "Kẹo sô cô la hạt màu nổ toàn bộ kẹo cùng màu",
        "default": 65535,
        "color": "#845EC2"
    },
    {
        "id": "jelly_fish",
        "name_vi": "Cá Thạch (Jelly Fish)",
        "name_en": "Jelly Fish",
        "icon": "🐟",
        "offset": 92,       # 0x5C
        "hex": "0x005C",
        "desc": "Thả 3 chú cá bơi đi ăn các ô thạch khó nhất",
        "default": 65535,
        "color": "#00C9A7"
    },
    {
        "id": "coconut_wheel",
        "name_vi": "Bánh Xe Dừa (Coconut Wheel)",
        "name_en": "Coconut Wheel / Roller",
        "icon": "🥥",
        "offset": 104,      # 0x68
        "hex": "0x0068",
        "desc": "Bánh lăn biến 3 kẹo tiếp theo thành kẹo sọc",
        "default": 65535,
        "color": "#C34A36"
    },
    {
        "id": "lollipop_hammer",
        "name_vi": "Búa Kẹo Mút (Lollipop Hammer)",
        "name_en": "Lollipop Hammer",
        "icon": "🍭",
        "offset": 116,      # 0x74
        "hex": "0x0074",
        "desc": "Đập tan lập tức bất kỳ 1 ô kẹo hoặc chướng ngại vật nào",
        "default": 65535,
        "color": "#FF8066"
    },
    {
        "id": "freeze_time",
        "name_vi": "Đóng Băng / Thêm Nước Đi (Extra Moves)",
        "name_en": "Freeze Time / Extra Moves",
        "icon": "⏳",
        "offset": 128,      # 0x80
        "hex": "0x0080",
        "desc": "Thêm +5 lượt đi hoặc đóng băng thời gian trong màn chơi",
        "default": 65535,
        "color": "#4D8076"
    },
    {
        "id": "lucky_candy",
        "name_vi": "Kẹo May Mắn (Lucky Candy)",
        "name_en": "Lucky Candy",
        "icon": "🍬",
        "offset": 152,      # 0x98
        "hex": "0x0098",
        "desc": "Khi ghép sẽ biến thành đúng loại kẹo mục tiêu cần thu thập",
        "default": 65535,
        "color": "#FFC75F"
    },
    {
        "id": "wrapped_striped",
        "name_vi": "Kẹo Gói & Kẹo Sọc (Wrapped & Striped)",
        "name_en": "Wrapped & Striped",
        "icon": "🎁",
        "offset": 164,      # 0xA4
        "hex": "0x00A4",
        "desc": "Bắt đầu màn chơi với sẵn 1 kẹo sọc và 1 kẹo gói",
        "default": 65535,
        "color": "#F9F871"
    },
    {
        "id": "hand_swaps",
        "name_vi": "Bàn Tay Đổi Kẹo (Free Switch)",
        "name_en": "Hand Swaps / Free Switch",
        "icon": "🖐️",
        "offset": 176,      # 0xB0
        "hex": "0x00B0",
        "desc": "Đổi vị trí 2 viên kẹo bất kỳ mà không tốn lượt đi",
        "default": 65535,
        "color": "#0081CF"
    },
    {
        "id": "moonstruck",
        "name_vi": "Bùa Mặt Trăng (Moonstruck)",
        "name_en": "Moonstruck Booster",
        "icon": "🌙",
        "offset": 188,      # 0xBC
        "hex": "0x00BC",
        "desc": "Loại bỏ hoàn toàn một số màu kẹo trên bàn cờ",
        "default": 65535,
        "color": "#9B51E0"
    },
    {
        "id": "ufo_drops",
        "name_vi": "Đĩa Bay UFO (UFO Drops)",
        "name_en": "UFO Drops",
        "icon": "🛸",
        "offset": 212,      # 0xD4
        "hex": "0x00D4",
        "desc": "Thả đĩa bay tạo ra ngay 3 viên kẹo gói phát nổ dọn sàn",
        "default": 65535,
        "color": "#2C73D2"
    },
    {
        "id": "paint_brush",
        "name_vi": "Cọ Sơn Kẹo (Sweet Teeth / Paint)",
        "name_en": "Paint Brush / Sweet Teeth",
        "icon": "🎨",
        "offset": 224,      # 0xE0
        "hex": "0x00E0",
        "desc": "Tô màu hoặc ăn chướng ngại vật sô-cô-la nhanh chóng",
        "default": 65535,
        "color": "#D65DB1"
    }
]

MAX_VAL = 65535
MIN_FILE_SIZE = 658

class CandyCrushSaveEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Candy Crush Saga - Save Game Hack & Booster Editor v2.0")
        self.root.geometry("1060x860")
        self.root.minsize(920, 720)
        
        # Đường dẫn thư mục công cụ
        self.base_dir = Path(__file__).resolve().parent
        self.bundled_adb = self.base_dir / "platform-tools" / "adb.exe"
        self.adb_bin = str(self.bundled_adb) if self.bundled_adb.exists() else "adb"

        # Dữ liệu file hiện tại
        self.current_filepath = None
        self.raw_data = None
        self.entries = {}
        self.original_values = {}

        self._init_theme()
        self._build_ui()

        # Tự động quét xem có file save trên máy tính không
        self.root.after(400, self.auto_detect_pc_save)

    def _init_theme(self):
        # Tone màu giao diện tối hiện đại (Modern Dark Candy)
        self.c_bg = "#12141C"
        self.c_card = "#1C2030"
        self.c_card_border = "#2B3248"
        self.c_card_hover = "#252C42"
        self.c_text = "#FFFFFF"
        self.c_text_sub = "#A0ABC0"
        self.c_accent = "#FF3366"
        self.c_accent_hover = "#E02857"
        self.c_success = "#00D26A"
        self.c_warning = "#FFB300"
        self.c_info = "#00B4D8"
        self.c_input_bg = "#0F1118"
        self.c_input_border = "#3A4562"

        self.root.configure(bg=self.c_bg)

        # Style cho ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar", background=self.c_card, troughcolor=self.c_bg, bordercolor=self.c_card_border)

    def _build_ui(self):
        # Container chính
        main_frame = tk.Frame(self.root, bg=self.c_bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        # === 1. HEADER BANNER ===
        header_frame = tk.Frame(main_frame, bg=self.c_card, relief=tk.FLAT, bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 14), ipady=12, ipadx=16)

        # Viền gradient hoặc thanh màu nhỏ trên top
        accent_bar = tk.Frame(header_frame, bg=self.c_accent, height=4)
        accent_bar.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="🍬 CANDY CRUSH SAGA - BỘ HACK LƯỢT CHƠI & BÙA HỖ TRỢ",
            font=("Segoe UI", 16, "bold"),
            fg=self.c_text,
            bg=self.c_card
        )
        title_lbl.pack(anchor="w", padx=16, pady=(10, 2))

        sub_lbl = tk.Label(
            header_frame,
            text="Trực tiếp chỉnh sửa file save_*.dat | Bơm 65,535 Lượt Mạng & Bùa không giới hạn | Hỗ trợ PC, Android & iOS",
            font=("Segoe UI", 10),
            fg=self.c_text_sub,
            bg=self.c_card
        )
        sub_lbl.pack(anchor="w", padx=16)

        # === 2. THANH CHỌN FILE SAVE ===
        file_card = tk.Frame(main_frame, bg=self.c_card, bd=1, relief=tk.SOLID)
        file_card.configure(highlightbackground=self.c_card_border, highlightthickness=1)
        file_card.pack(fill=tk.X, pady=(0, 14), padx=0, ipady=8, ipadx=12)

        file_top_box = tk.Frame(file_card, bg=self.c_card)
        file_top_box.pack(fill=tk.X, padx=12, pady=6)

        tk.Label(file_top_box, text="📂 File Save Đang Mở:", font=("Segoe UI", 10, "bold"), fg=self.c_text, bg=self.c_card).pack(side=tk.LEFT)
        
        self.path_var = tk.StringVar(value="Chưa chọn file save_*.dat nào. Hãy bấm 'Chọn File...' hoặc 'Tự Tìm Save PC' bên dưới!")
        self.path_entry = tk.Entry(
            file_top_box,
            textvariable=self.path_var,
            font=("Consolas", 10),
            fg="#90CDF4",
            bg=self.c_input_bg,
            relief=tk.FLAT,
            insertbackground=self.c_text,
            highlightthickness=1,
            highlightbackground=self.c_input_border
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=4)

        # Các nút bấm chọn file
        btn_bar = tk.Frame(file_card, bg=self.c_card)
        btn_bar.pack(fill=tk.X, padx=12, pady=(4, 6))

        self._create_btn(btn_bar, "📁 Chọn File .dat", self.choose_file, bg=self.c_info, fg="#000000").pack(side=tk.LEFT, padx=(0, 6))
        self._create_btn(btn_bar, "🔍 Tự Tìm Save PC", self.auto_detect_pc_save, bg="#6C5CE7", fg="#FFFFFF").pack(side=tk.LEFT, padx=3)
        self._create_btn(btn_bar, "🌟 Bơm Tất Cả Tài Khoản (9,999)", lambda: self.hack_all_pc_accounts(9999), bg="#E17055", fg="#FFFFFF", bold=True).pack(side=tk.LEFT, padx=3)
        self._create_btn(btn_bar, "📱 Kéo từ Android (ADB)", self.pull_save_from_android, bg="#00B894", fg="#000000").pack(side=tk.LEFT, padx=3)
        self._create_btn(btn_bar, "✨ Mẫu Test", self.create_sample_file, bg="#4A5568", fg="#FFFFFF").pack(side=tk.LEFT, padx=3)

        # Thông tin file hiện tại
        self.file_info_lbl = tk.Label(btn_bar, text="Kích thước: 0 bytes | Trạng thái: Chưa tải", font=("Segoe UI", 9), fg=self.c_text_sub, bg=self.c_card)
        self.file_info_lbl.pack(side=tk.RIGHT, padx=4)

        # === 3. KHU VỰC THAO TÁC NHANH (PRESET BUTTONS) ===
        preset_bar = tk.Frame(main_frame, bg=self.c_bg)
        preset_bar.pack(fill=tk.X, pady=(0, 12))

        tk.Label(preset_bar, text="⚡ Cấu hình nhanh:", font=("Segoe UI", 10, "bold"), fg=self.c_text, bg=self.c_bg).pack(side=tk.LEFT, padx=(0, 10))
        self._create_btn(preset_bar, "⚡ MAX TẤT CẢ (65,535)", self.action_max_all, bg=self.c_accent, fg="#FFFFFF", bold=True).pack(side=tk.LEFT, padx=4)
        self._create_btn(preset_bar, "💎 Khủng (9,999)", lambda: self.set_all_values(9999), bg="#F39C12", fg="#000000").pack(side=tk.LEFT, padx=4)
        self._create_btn(preset_bar, "🎯 Chuẩn (500)", lambda: self.set_all_values(500), bg="#2ECC71", fg="#000000").pack(side=tk.LEFT, padx=4)
        self._create_btn(preset_bar, "❤️ Chỉ Bất Tử Mạng", self.action_max_lives_only, bg="#E84393", fg="#FFFFFF").pack(side=tk.LEFT, padx=4)
        self._create_btn(preset_bar, "🔄 Đặt lại (Reset)", self.action_reset_original, bg="#4A5568", fg="#FFFFFF").pack(side=tk.LEFT, padx=4)

        # === 4. BẢNG DANH SÁCH 12 LOẠI BÙA & MẠNG (SCROLLABLE GRID) ===
        container = tk.Frame(main_frame, bg=self.c_bg)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg=self.c_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=self.c_bg)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Đảm bảo scroll_frame mở rộng đúng chiều ngang canvas
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        # Hỗ trợ cuộn chuột
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._render_booster_cards()

        # === 5. FOOTER & NÚT LƯU FILE ===
        footer = tk.Frame(main_frame, bg=self.c_card, bd=1, relief=tk.SOLID)
        footer.configure(highlightbackground=self.c_card_border, highlightthickness=1)
        footer.pack(fill=tk.X, pady=(14, 0), ipady=8, ipadx=14)

        save_btn = self._create_btn(footer, "💾 LƯU FILE SAVE (TỰ ĐỘNG TẠO BẢN SAO .BAK)", self.save_file, bg=self.c_success, fg="#000000", bold=True, pad_y=8)
        save_btn.pack(side=tk.LEFT, padx=8)

        push_adb_btn = self._create_btn(footer, "📤 ĐẨY NGAY VÀO ANDROID (ADB)", self.push_save_to_android, bg="#0984E3", fg="#FFFFFF", bold=True, pad_y=8)
        push_adb_btn.pack(side=tk.LEFT, padx=8)

        open_folder_btn = self._create_btn(footer, "📂 Mở Thư Mục File", self.open_current_folder, bg="#4A5568", fg="#FFFFFF", pad_y=8)
        open_folder_btn.pack(side=tk.LEFT, padx=8)

        self.status_var = tk.StringVar(value="Sẵn sàng. Hãy chọn file save để bắt đầu!")
        status_lbl = tk.Label(footer, textvariable=self.status_var, font=("Segoe UI", 9, "italic"), fg=self.c_text_sub, bg=self.c_card)
        status_lbl.pack(side=tk.RIGHT, padx=12)

    def _create_btn(self, parent, text, command, bg="#3A4562", fg="#FFFFFF", bold=False, pad_y=4):
        font_weight = "bold" if bold else "normal"
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 9, font_weight),
            bg=bg,
            fg=fg,
            activebackground=fg,
            activeforeground=bg,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=pad_y,
            cursor="hand2"
        )
        return btn

    def _render_booster_cards(self):
        # Tạo lưới card 2 cột
        cols = 2
        for idx, item in enumerate(BOOSTER_DEFINITIONS):
            r = idx // cols
            c = idx % cols

            card = tk.Frame(self.scroll_frame, bg=self.c_card, bd=1, relief=tk.SOLID)
            card.configure(highlightbackground=self.c_card_border, highlightthickness=1)
            card.grid(row=r, column=c, padx=8, pady=6, sticky="nsew")
            self.scroll_frame.grid_columnconfigure(c, weight=1)

            # Header card (Icon + Tên + Badge Offset)
            top_box = tk.Frame(card, bg=self.c_card)
            top_box.pack(fill=tk.X, padx=12, pady=(10, 4))

            icon_lbl = tk.Label(top_box, text=item["icon"], font=("Segoe UI Emoji", 18), bg=self.c_card)
            icon_lbl.pack(side=tk.LEFT, padx=(0, 8))

            name_box = tk.Frame(top_box, bg=self.c_card)
            name_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

            tk.Label(name_box, text=item["name_vi"], font=("Segoe UI", 10, "bold"), fg=self.c_text, bg=self.c_card).pack(anchor="w")
            tk.Label(name_box, text=f"{item['name_en']}  •  Offset: {item['hex']} ({item['offset']})", font=("Segoe UI", 8), fg=self.c_text_sub, bg=self.c_card).pack(anchor="w")

            # Input và nút tăng nhanh
            action_box = tk.Frame(card, bg=self.c_card)
            action_box.pack(fill=tk.X, padx=12, pady=(4, 10))

            tk.Label(action_box, text="Số lượng:", font=("Segoe UI", 9), fg=self.c_text_sub, bg=self.c_card).pack(side=tk.LEFT, padx=(0, 6))

            val_var = tk.StringVar(value="0")
            entry = tk.Entry(
                action_box,
                textvariable=val_var,
                font=("Consolas", 12, "bold"),
                width=8,
                justify="center",
                bg=self.c_input_bg,
                fg="#F6E05E",
                relief=tk.FLAT,
                insertbackground=self.c_text,
                highlightthickness=1,
                highlightbackground=self.c_input_border
            )
            entry.pack(side=tk.LEFT, padx=(0, 8), ipady=3)
            self.entries[item["id"]] = val_var

            # Các nút chỉnh nhanh
            self._create_btn(action_box, "+100", lambda i=item["id"]: self.add_to_val(i, 100), bg="#2D3748").pack(side=tk.LEFT, padx=2)
            self._create_btn(action_box, "+1K", lambda i=item["id"]: self.add_to_val(i, 1000), bg="#2D3748").pack(side=tk.LEFT, padx=2)
            self._create_btn(action_box, "Max 65K", lambda i=item["id"]: self.set_val(i, 65535), bg=self.c_accent, bold=True).pack(side=tk.LEFT, padx=2)
            self._create_btn(action_box, "0", lambda i=item["id"]: self.set_val(i, 0), bg="#1A202C").pack(side=tk.LEFT, padx=2)

    def add_to_val(self, item_id, amount):
        if item_id in self.entries:
            try:
                curr = int(self.entries[item_id].get())
            except ValueError:
                curr = 0
            new_val = min(MAX_VAL, curr + amount)
            self.entries[item_id].set(str(new_val))

    def set_val(self, item_id, value):
        if item_id in self.entries:
            self.entries[item_id].set(str(max(0, min(MAX_VAL, int(value)))))

    def set_all_values(self, val):
        for item in BOOSTER_DEFINITIONS:
            self.set_val(item["id"], val)
        self.set_status(f"Đã đặt tất cả các loại bùa về {val:,}!")

    def action_max_all(self):
        self.set_all_values(65535)
        self.set_status("🚀 ĐÃ BẬT MAX 65,535 CHO TẤT CẢ BÙA & LƯỢT CHƠI!")

    def action_max_lives_only(self):
        self.set_val("lives", 65535)
        self.set_status("💖 Đã bật Max 65,535 Lượt Chơi (Mạng)!")

    def action_reset_original(self):
        if not self.original_values:
            self.set_all_values(0)
            return
        for item_id, val in self.original_values.items():
            self.set_val(item_id, val)
        self.set_status("🔄 Đã khôi phục về các giá trị ban đầu của file save!")

    def set_status(self, msg, is_error=False):
        self.status_var.set(msg)

    def choose_file(self):
        initial_dir = str(Path.home() / "Desktop")
        filetypes = [
            ("Candy Crush Save Files", "save_*.dat;*.dat"),
            ("All Files", "*.*")
        ]
        chosen = filedialog.askopenfilename(
            title="Chọn file save Candy Crush (.dat)",
            initialdir=initial_dir,
            filetypes=filetypes
        )
        if chosen:
            self.load_save_file(chosen)

    def auto_detect_pc_save(self):
        """Tự động quét tìm file save trong thư mục cài đặt Candy Crush Saga của Windows"""
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        pkg_root = Path(local_appdata) / "Packages"
        
        candidates = []
        if pkg_root.exists():
            for candy_dir in pkg_root.glob("*CandyCrush*"):
                local_state = candy_dir / "LocalState"
                if local_state.exists():
                    # Tìm đệ quy trong LocalState (thường nằm trong LocalState/Documents/)
                    for dat in local_state.rglob("save_*.dat"):
                        if not dat.name.endswith(".bak"):
                            candidates.append(dat)
                    if not candidates:
                        for dat in local_state.rglob("*.dat"):
                            if not dat.name.endswith(".bak"):
                                candidates.append(dat)

        if candidates:
            # Ưu tiên file có ID tài khoản (khác save_0.dat) và được chỉnh sửa mới nhất
            user_candidates = [c for c in candidates if c.name != "save_0.dat"]
            target = max(user_candidates if user_candidates else candidates, key=os.path.getmtime)
            self.load_save_file(str(target))
            self.set_status(f"✅ Đã tự động phát hiện file save PC: {target.name}")
        else:
            self.set_status("Chưa tìm thấy save Candy Crush PC trong Windows Store. Hãy bấm 'Chọn File .dat' thủ công.")

    def hack_all_pc_accounts(self, target_val=9999):
        """Bơm giá trị (mặc định 9,999) cho toàn bộ các tài khoản Candy Crush tìm thấy trên máy tính (King, Facebook, Khách)"""
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        pkg_root = Path(local_appdata) / "Packages"
        
        candidates = []
        if pkg_root.exists():
            for candy_dir in pkg_root.glob("*CandyCrush*"):
                local_state = candy_dir / "LocalState"
                if local_state.exists():
                    for dat in local_state.rglob("save_*.dat"):
                        if not dat.name.endswith(".bak"):
                            candidates.append(dat)

        if not candidates:
            messagebox.showwarning("Không Tìm Thấy", "Không tìm thấy thư mục lưu game Candy Crush trên máy tính!")
            return

        confirm = messagebox.askyesno(
            "Xác Nhận Bơm Tất Cả Tài Khoản",
            f"Tìm thấy {len(candidates)} file tài khoản trên máy:\n" +
            "\n".join([f"• {c.name}" for c in candidates]) +
            f"\n\nBạn có muốn tự động sao lưu và BƠM {target_val:,} BÙA VÀ MẠNG vào TẤT CẢ các tài khoản này (bao gồm cả King, Facebook và Khách) không?\n(Vàng tài khoản giữ nguyên 100%, không bị ảnh hưởng)"
        )
        if not confirm:
            return

        success_count = 0
        for dat_path in candidates:
            try:
                bak = dat_path.with_suffix(dat_path.suffix + ".bak")
                shutil.copy2(dat_path, bak)

                with open(dat_path, "rb") as f:
                    data = bytearray(f.read())

                if len(data) < MIN_FILE_SIZE:
                    data.extend(b'\x00' * (1024 - len(data)))

                for item in BOOSTER_DEFINITIONS:
                    offset = item["offset"]
                    if offset + 2 > len(data):
                        data.extend(b'\x00' * (offset + 2 - len(data)))
                    struct.pack_into("<H", data, offset, target_val)

                with open(dat_path, "wb") as f:
                    f.write(data)
                success_count += 1
            except Exception as e:
                print(f"Lỗi khi xử lý {dat_path}: {e}")

        self.auto_detect_pc_save()
        messagebox.showinfo(
            "Thành Công Rực Rỡ!",
            f"🎉 ĐÃ BƠM THÀNH CÔNG CHO {success_count}/{len(candidates)} TÀI KHOẢN!\n\n"
            f"Mỗi loại bùa & mạng đều đã được đặt thành {target_val:,}:\n" +
            "\n".join([f"✅ {c.name}" for c in candidates]) +
            "\n\n👉 Vàng giữ nguyên 100%. Dù bạn đăng nhập tài khoản KING, FACEBOOK hay CHƠI KHÁCH thì vào game ĐỀU CÓ SẴN 9,999 BÙA!"
        )
        self.set_status(f"🎉 Đã bơm full {target_val:,} cho toàn bộ {success_count} tài khoản trên máy!")

    def load_save_file(self, filepath):
        path = Path(filepath)
        if not path.exists():
            messagebox.showerror("Lỗi", f"Không tìm thấy file:\n{filepath}")
            return

        try:
            with open(path, "rb") as f:
                data = bytearray(f.read())
        except Exception as e:
            messagebox.showerror("Lỗi Đọc File", f"Không thể đọc file save:\n{e}")
            return

        if len(data) < MIN_FILE_SIZE:
            confirm = messagebox.askyesno(
                "Kích Thước Nhỏ",
                f"File này chỉ có {len(data)} bytes (chuẩn Candy Crush yêu cầu tối thiểu {MIN_FILE_SIZE} bytes để chứa hết các offset).\n\n"
                "Bạn có muốn tự động mở rộng vùng nhớ lên 1024 bytes để nạp đầy đủ bùa không?"
            )
            if confirm:
                data.extend(b'\x00' * (1024 - len(data)))
            else:
                return

        self.current_filepath = path
        self.raw_data = data
        self.path_var.set(str(path))
        self.file_info_lbl.configure(text=f"Kích thước: {len(data):,} bytes | File: {path.name}")

        # Đọc các giá trị tại từng offset (Unsigned Little-Endian 16-bit)
        self.original_values = {}
        for item in BOOSTER_DEFINITIONS:
            offset = item["offset"]
            if offset + 1 < len(data):
                val = struct.unpack_from("<H", data, offset)[0]
                self.entries[item["id"]].set(str(val))
                self.original_values[item["id"]] = val
            else:
                self.entries[item["id"]].set("0")
                self.original_values[item["id"]] = 0

        self.set_status(f"🎉 Đã nạp thành công file: {path.name} ({len(data):,} bytes)")

    def save_file(self):
        if not self.current_filepath or not self.raw_data:
            messagebox.showwarning("Chưa Chọn File", "Vui lòng chọn hoặc tạo file save trước khi bấm Lưu!")
            return

        # 1. Tạo file Backup an toàn (.bak)
        backup_path = self.current_filepath.with_suffix(self.current_filepath.suffix + ".bak")
        try:
            shutil.copy2(self.current_filepath, backup_path)
        except Exception as e:
            messagebox.showerror("Lỗi Tạo Backup", f"Không thể tạo file sao lưu .bak:\n{e}")
            return

        # 2. Ghi đè các giá trị mới vào mảng byte
        for item in BOOSTER_DEFINITIONS:
            offset = item["offset"]
            try:
                val = int(self.entries[item["id"]].get())
            except ValueError:
                val = 0
            val = max(0, min(MAX_VAL, val))
            
            # Đảm bảo buffer đủ dài
            if offset + 2 > len(self.raw_data):
                self.raw_data.extend(b'\x00' * (offset + 2 - len(self.raw_data)))

            struct.pack_into("<H", self.raw_data, offset, val)

        # 3. Ghi ra đĩa
        try:
            with open(self.current_filepath, "wb") as f:
                f.write(self.raw_data)
        except Exception as e:
            messagebox.showerror("Lỗi Ghi File", f"Không thể ghi file save:\n{e}")
            return

        # Cập nhật giá trị gốc
        for item in BOOSTER_DEFINITIONS:
            self.original_values[item["id"]] = int(self.entries[item["id"]].get())

        messagebox.showinfo(
            "Thành Công!",
            f"✅ ĐÃ LƯU FILE SAVE THÀNH CÔNG!\n\n"
            f"📁 File đã chỉnh sửa: {self.current_filepath.name}\n"
            f"🛡️ File sao lưu bảo vệ: {backup_path.name}\n\n"
            "Bây giờ bạn chỉ cần mở game Candy Crush Saga lên và tận hưởng 65,535 bùa & mạng vô hạn!"
        )
        self.set_status(f"✅ Đã lưu thành công! (Bản sao lưu tại {backup_path.name})")

    def create_sample_file(self):
        """Tạo file save_sample.dat mẫu 1024 bytes với tất cả bùa max 65535 để người dùng test ngay"""
        save_dest = filedialog.asksaveasfilename(
            title="Lưu file save mẫu",
            initialdir=str(self.base_dir),
            initialfile="save_sample_65535.dat",
            filetypes=[("DAT files", "*.dat")]
        )
        if not save_dest:
            return

        data = bytearray(1024)
        for item in BOOSTER_DEFINITIONS:
            struct.pack_into("<H", data, item["offset"], 65535)

        with open(save_dest, "wb") as f:
            f.write(data)

        self.load_save_file(save_dest)
        messagebox.showinfo("Thành Công", f"Đã tạo file save mẫu cực chuẩn:\n{save_dest}\nTất cả bùa đã được nạp sẵn 65,535!")

    def pull_save_from_android(self):
        """Kết nối ADB lấy file save từ điện thoại Android hoặc giả lập LDPlayer"""
        try:
            # 1. Tự động kết nối tới các cổng giả lập nếu có LDPlayer đang chạy
            for port in ["5555", "5554", "62001", "7555"]:
                subprocess.run([self.adb_bin, "connect", f"127.0.0.1:{port}"], capture_output=True, timeout=1)

            res = subprocess.run([self.adb_bin, "devices"], capture_output=True, text=True)
            lines = res.stdout.strip().split("\n")[1:]
            devices = [l.split()[0] for l in lines if len(l.split()) >= 2 and l.split()[1] == "device"]
            if not devices:
                messagebox.showwarning("Không Tìm Thấy Thiết Bị", "Chưa phát hiện điện thoại Android hoặc giả lập LDPlayer đang chạy!\nHãy bật LDPlayer 9 (hoặc cắm cáp USB vào điện thoại) rồi thử lại.")
                return

            dev = devices[0]
            # Bật adb root nếu thiết bị hỗ trợ (như LDPlayer)
            subprocess.run([self.adb_bin, "-s", dev, "root"], capture_output=True, timeout=2)

            remote_dirs = [
                "/data/data/com.king.candycrushsaga/app_storage/",
                "/data/data/com.king.candycrushsaga/files/"
            ]

            target_remote_file = None
            for rdir in remote_dirs:
                check_cmd = [self.adb_bin, "-s", dev, "shell", f"ls {rdir}save_*.dat"]
                r_res = subprocess.run(check_cmd, capture_output=True, text=True)
                if r_res.returncode == 0 and "save_" in r_res.stdout:
                    files = [f.strip() for f in r_res.stdout.split() if "save_" in f]
                    if files:
                        target_remote_file = files[-1]
                        break

            # Thử qua quyền root su nếu bị permission denied
            if not target_remote_file:
                for rdir in remote_dirs:
                    check_cmd = [self.adb_bin, "-s", dev, "shell", f"su -c 'ls {rdir}save_*.dat'"]
                    r_res = subprocess.run(check_cmd, capture_output=True, text=True)
                    if r_res.returncode == 0 and "save_" in r_res.stdout:
                        files = [f.strip() for f in r_res.stdout.split() if "save_" in f]
                        if files:
                            src_file = files[-1]
                            fname = Path(src_file).name
                            subprocess.run([self.adb_bin, "-s", dev, "shell", f"su -c 'cp {src_file} /sdcard/Download/{fname}'"], capture_output=True)
                            target_remote_file = f"/sdcard/Download/{fname}"
                            break

            if not target_remote_file:
                msg = (
                    f"Đã phát hiện thiết bị Android / Giả lập ({dev}), nhưng chưa tìm thấy file save Candy Crush.\n\n"
                    "👉 Lưu ý:\n"
                    "1. Trên LDPlayer: Bật Quyền Root trong Cài đặt giả lập -> Cài đặt khác -> Bật Root.\n"
                    "2. Mở Candy Crush lên, đăng nhập Facebook và chơi ít nhất 1 nước để game tạo file save."
                )
                messagebox.showinfo("Thông Tin Thiết Bị", msg)
                return

            local_save = self.base_dir / Path(target_remote_file).name
            pull_cmd = [self.adb_bin, "-s", dev, "pull", target_remote_file, str(local_save)]
            subprocess.run(pull_cmd, capture_output=True, text=True)

            if local_save.exists():
                self.load_save_file(str(local_save))
                messagebox.showinfo("Kéo File Thành Công", f"🎉 Đã lấy file save từ thiết bị Android/LDPlayer về máy tính:\n{local_save.name}\n\n👉 Bạn hãy chỉnh sửa / bấm '🌟 Bơm Tất Cả Tài Khoản' rồi bấm '📤 ĐẨY NGAY VÀO ANDROID (ADB)' nhé!")
        except Exception as e:
            messagebox.showerror("Lỗi ADB", f"Không thể thực thi lệnh ADB:\n{e}")

    def push_save_to_android(self):
        """Đẩy file save đã chỉnh sửa vào điện thoại Android hoặc giả lập LDPlayer qua ADB"""
        if not self.current_filepath or not self.current_filepath.exists():
            messagebox.showwarning("Lỗi", "Vui lòng chọn và lưu file save trước khi đẩy vào máy!")
            return

        try:
            # Tự động kết nối lại cổng giả lập nếu cần
            for port in ["5555", "5554", "62001", "7555"]:
                subprocess.run([self.adb_bin, "connect", f"127.0.0.1:{port}"], capture_output=True, timeout=1)

            res = subprocess.run([self.adb_bin, "devices"], capture_output=True, text=True)
            lines = res.stdout.strip().split("\n")[1:]
            devices = [l.split()[0] for l in lines if len(l.split()) >= 2 and l.split()[1] == "device"]
            if not devices:
                messagebox.showwarning("Không Tìm Thấy", "Chưa kết nối điện thoại Android hoặc giả lập LDPlayer!")
                return

            dev = devices[0]
            filename = self.current_filepath.name
            
            # 1. Đẩy vào /sdcard/Download/
            target_sdcard = f"/sdcard/Download/{filename}"
            push_cmd = [self.adb_bin, "-s", dev, "push", str(self.current_filepath), target_sdcard]
            subprocess.run(push_cmd, capture_output=True, text=True)

            # 2. Tự động chép đè thẳng vào thư mục Candy Crush nếu có quyền Root (như LDPlayer)
            app_storage = f"/data/data/com.king.candycrushsaga/app_storage/{filename}"
            su_cmd = f"su -c 'cp {target_sdcard} {app_storage} && chmod 660 {app_storage}'"
            su_res = subprocess.run([self.adb_bin, "-s", dev, "shell", su_cmd], capture_output=True, text=True)

            if su_res.returncode == 0:
                messagebox.showinfo(
                    "Đẩy File Trực Tiếp Thành Công!",
                    f"🎉 XUẤT SẮC! Đã nạp thẳng file save vào Candy Crush trên LDPlayer/Android:\n{filename}\n\n"
                    "👉 Bây giờ bạn chỉ cần mở lại game Candy Crush trên LDPlayer là ĐÃ CÓ ĐẦY ĐỦ 9,999 BÙA & MẠNG!"
                )
            else:
                messagebox.showinfo(
                    "Đẩy File Vào Bộ Nhớ Thành Công",
                    f"✅ Đã nạp file save đã hack vào thiết bị tại:\n{target_sdcard}\n\n"
                    "Bạn dùng MT Manager hoặc trình quản lý file dán file này vào:\n/data/data/com.king.candycrushsaga/app_storage/ là hoàn tất!"
                )
        except Exception as e:
            messagebox.showerror("Lỗi ADB", f"Lỗi khi đẩy file:\n{e}")

    def open_current_folder(self):
        folder = self.current_filepath.parent if self.current_filepath else self.base_dir
        if sys.platform == "win32":
            os.startfile(folder)
        else:
            subprocess.run(["xdg-open", str(folder)])

def main():
    root = tk.Tk()
    app = CandyCrushSaveEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
