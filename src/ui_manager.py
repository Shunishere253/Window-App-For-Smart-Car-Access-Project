# ui_manager.py
import tkinter as tk
from tkinter import ttk
import os
import time
from config import LANGS, IMG_LOCKED_PATH, IMG_UNLOCKED_PATH

class CarSimulatorUI:
    def __init__(self, root, callbacks, initial_lang="vi"):
        self.root = root
        self.callbacks = callbacks
        self.current_lang = initial_lang
        
        self.root.configure(bg="white")
        
        # Load Ảnh
        self.img_car = None
        self.img_lock_green = None
        try:
            if os.path.exists(IMG_UNLOCKED_PATH):
                self.img_car = tk.PhotoImage(file=IMG_UNLOCKED_PATH)
            if os.path.exists(IMG_LOCKED_PATH):
                self.img_lock_green = tk.PhotoImage(file=IMG_LOCKED_PATH)
        except Exception as e:
            print(f"Lỗi load ảnh: {e}")

        # Khởi tạo biến lưu trạng thái Status Panel
        self.is_unlocked = False
        self.is_user_inside = False
        self.auth_state = "waiting"
        self.var_sys_status = tk.StringVar(value="")
        self.var_can_conn = tk.StringVar(value="")
        self.var_auth = tk.StringVar(value="")
        self.var_zone = tk.StringVar(value="")
        self.var_time = tk.StringVar(value=time.strftime('%H:%M:%S'))
        self.var_mcu_fw = tk.StringVar(value="S32K144")

        # Dictionary lưu các Label tiêu đề để đổi ngôn ngữ sau này
        self.labels_info_titles = []

        self.setup_ui()
        self.update_clock()
        self.update_language_texts(self.current_lang) # Nạp ngôn ngữ lần đầu

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#f0f0f0", foreground="black")
        style.configure("Treeview", font=('Arial', 10), rowheight=25)
        
        main_container = tk.Frame(self.root, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ==========================================
        # TOP FRAME
        # ==========================================
        top_frame = tk.Frame(main_container, bg="white")
        top_frame.pack(fill=tk.X, expand=False, pady=(0, 10))

        # --- 1. Vehicle Visualization Area ---
        frame_1 = tk.Frame(top_frame, bg="white", highlightbackground="#b0c4de", highlightthickness=2)
        frame_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.lbl_h1 = tk.Label(frame_1, font=("Arial", 12, "bold"), fg="#0033a0", bg="white")
        self.lbl_h1.pack(anchor=tk.W, padx=10, pady=10)

        self.canvas_vis = tk.Canvas(frame_1, width=250, height=200, bg="white", highlightthickness=0)
        self.canvas_vis.pack(pady=10)
        
        # LƯU ID CỦA ẢNH TRÊN CANVAS ĐỂ CẬP NHẬT ĐÚNG ĐỐI TƯỢNG
        self.img_on_canvas = None
        
        # Mặc định khởi động hệ thống đang KHÓA, nên dùng img_lock_green
        if self.img_lock_green:
            self.img_on_canvas = self.canvas_vis.create_image(125, 100, image=self.img_lock_green)
        else:
            self.canvas_vis.create_oval(75, 20, 175, 180, outline="#2ecc71", width=2, dash=(4, 4))
            self.canvas_vis.create_rectangle(100, 40, 150, 160, fill="#333333", outline="black")
            
        self.lbl_badge = tk.Label(frame_1, font=("Arial", 11, "bold"), bg="#d4edda", fg="#155724", relief=tk.SOLID, bd=1, padx=20, pady=5)
        self.lbl_badge.pack(pady=(0, 15))

        # --- 2. Status Panel ---
        frame_2 = tk.Frame(top_frame, bg="white", highlightbackground="#b0c4de", highlightthickness=2)
        frame_2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        header_frame_2 = tk.Frame(frame_2, bg="white")
        header_frame_2.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_h2 = tk.Label(header_frame_2, font=("Arial", 12, "bold"), fg="#0033a0", bg="white")
        self.lbl_h2.pack(side=tk.LEFT)

        self.btn_lang = tk.Button(header_frame_2, font=("Arial", 9), bg="#f0f0f0", command=self.callbacks.get('toggle_lang', self.dummy_cmd))
        self.btn_lang.pack(side=tk.RIGHT)

        grid_frame = tk.Frame(frame_2, bg="white")
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Lưu lại var để cập nhật ngôn ngữ sau
        self.status_vars_map = [
            ("sys_status", self.var_sys_status, "#008000"),
            ("can_conn", self.var_can_conn, "#008000"),
            ("auth", self.var_auth, "#008000"),
            ("curr_zone", self.var_zone, "#ff8c00"),
            ("time", self.var_time, "black"),
            ("mcu_fw", self.var_mcu_fw, "black")
        ]

        for i, (dict_key, var, color) in enumerate(self.status_vars_map):
            lbl_title = tk.Label(grid_frame, font=("Arial", 11, "bold"), bg="white", anchor=tk.W)
            lbl_title.grid(row=i, column=0, sticky=tk.W, pady=5)
            self.labels_info_titles.append((lbl_title, dict_key)) # Lưu label để dịch
            
            tk.Label(grid_frame, text=":", font=("Arial", 11, "bold"), bg="white").grid(row=i, column=1, padx=10)
            tk.Label(grid_frame, textvariable=var, font=("Arial", 11, "bold"), bg="white", fg=color, anchor=tk.W).grid(row=i, column=2, sticky=tk.W)

        # ==========================================
        # BOTTOM FRAME
        # ==========================================
        frame_3 = tk.Frame(main_container, bg="white", highlightbackground="#b0c4de", highlightthickness=2)
        frame_3.pack(fill=tk.BOTH, expand=True)

        self.lbl_h3 = tk.Label(frame_3, font=("Arial", 12, "bold"), fg="#0033a0", bg="white")
        self.lbl_h3.pack(anchor=tk.W, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_3, columns=("col1", "col2", "col3", "col4", "col5"), show="headings", height=8)
        
        self.tree.column("col1", width=120, anchor=tk.CENTER)
        self.tree.column("col2", width=80, anchor=tk.CENTER)
        self.tree.column("col3", width=50, anchor=tk.CENTER)
        self.tree.column("col4", width=250, anchor=tk.CENTER)
        self.tree.column("col5", width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame_3, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bottom_ctrl = tk.Frame(frame_3, bg="white")
        bottom_ctrl.pack(fill=tk.X, padx=10, pady=10)

        self.btn_clear = tk.Button(bottom_ctrl, font=("Arial", 10), bg="#f8f9fa", relief=tk.RAISED, command=self.clear_log)
        self.btn_clear.pack(side=tk.LEFT)

        self.var_autoscroll = tk.BooleanVar(value=True)
        self.chk_autoscroll = tk.Checkbutton(bottom_ctrl, font=("Arial", 10, "bold"), bg="white", variable=self.var_autoscroll)
        self.chk_autoscroll.pack(side=tk.RIGHT)

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.var_time.set(current_time)
        self.root.after(1000, self.update_clock)

    def write_can_log(self, t_time, can_id, dlc, data_hex, desc_key):
        """Hàm chính để ghi Log CAN từ thiết bị thật lên UI"""
        desc = LANGS[self.current_lang].get(desc_key, desc_key)
        self.tree.insert("", tk.END, values=(t_time, can_id, dlc, data_hex, desc))
        if self.var_autoscroll.get():
            self.tree.yview_moveto(1)

    def write_log(self, msg_key, values=None):
        """Hỗ trợ in lỗi hệ thống (như chưa cắm cáp COM) thẳng vào bảng CAN"""
        values = values or {}
        d = LANGS[self.current_lang]
        msg_template = d.get(msg_key, msg_key)
        try:
            msg = msg_template.format(**values)
        except (KeyError, IndexError):
            msg = msg_template
        current_time = time.strftime('%H:%M:%S.') + str(int(time.time() * 1000) % 1000).zfill(3)
        self.tree.insert("", tk.END, values=(current_time, "[SYS]", "-", msg, d["desc_system_alert"]))
        if self.var_autoscroll.get():
            self.tree.yview_moveto(1)

    def clear_log(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def update_language_texts(self, lang):
        """Thay đổi toàn bộ text trên giao diện theo từ điển"""
        self.current_lang = lang
        d = LANGS[lang]
        
        # Cập nhật Title ứng dụng
        self.root.title(d["app_title"])
        
        # Cập nhật các Header Khu vực
        self.lbl_h1.config(text=d["area_1"])
        self.lbl_h2.config(text=d["area_2"])
        self.lbl_h3.config(text=d["area_3"])
        
        # Cập nhật các Nút bấm
        self.btn_lang.config(text=d["btn_lang"])
        self.btn_clear.config(text=d["btn_clear"])
        self.chk_autoscroll.config(text=d["chk_autoscroll"])
        
        # Cập nhật cột bảng CAN
        self.tree.heading("col1", text=d["col_time"])
        self.tree.heading("col2", text=d["col_id"])
        self.tree.heading("col3", text=d["col_dlc"])
        self.tree.heading("col4", text=d["col_data"])
        self.tree.heading("col5", text=d["col_desc"])
        
        # Cập nhật các nhãn trong Status Panel
        for lbl, dict_key in self.labels_info_titles:
            lbl.config(text=d[dict_key])
            
        # Cập nhật Badge ảnh theo trạng thái hiện hành
        self._sync_car_state_texts()

    def update_car_state(self, is_unlocked, is_user_inside, auth_state):
        """Cập nhật trạng thái xe nhận từ mạch phần cứng"""
        self.is_unlocked = is_unlocked
        self.is_user_inside = is_user_inside
        self.auth_state = auth_state
        self._sync_car_state_texts()

    def _sync_car_state_texts(self):
        """Đồng bộ text trạng thái xe theo ngôn ngữ hiện tại."""
        d = LANGS[self.current_lang]
        if self.is_unlocked:
            self.lbl_badge.config(text=d["badge_unlocked"], bg="#d4edda", fg="#155724")
            self.var_sys_status.set(d["val_active"])
            # NẾU CÓ ẢNH TRÊN CANVAS, CẬP NHẬT SANG ẢNH XE MỞ
            if self.img_car and self.img_on_canvas:
                self.canvas_vis.itemconfig(self.img_on_canvas, image=self.img_car)
        else:
            self.lbl_badge.config(text=d["badge_locked"], bg="#f8d7da", fg="#721c24")
            self.var_sys_status.set(d["val_locked"])
            # NẾU CÓ ẢNH TRÊN CANVAS, CẬP NHẬT SANG ẢNH XE ĐÓNG
            if self.img_lock_green and self.img_on_canvas:
                self.canvas_vis.itemconfig(self.img_on_canvas, image=self.img_lock_green)

        if self.is_user_inside:
            self.var_zone.set(d["val_inside"])
        else:
            self.var_zone.set(d["val_outside"])

        self.var_can_conn.set(d["val_can_connected"])
        self.var_auth.set(d[f"val_auth_{self.auth_state}"])

    def dummy_cmd(self):
        pass
