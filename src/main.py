# main.py
import tkinter as tk
import time
from ui_manager import CarSimulatorUI
from can_manager import CanManager

class SmartCarApp:
    def __init__(self, root):
        self.root = root
        
        self.current_lang = "vi"
        
        # Các biến lưu trạng thái phần cứng của xe
        self.is_unlocked = False
        self.is_user_inside = False
        self.auth_state = "waiting"

        callbacks = {
            'toggle_lang': self.toggle_language,
            'clear_log': self.handle_clear_log
        }

        # 1. Khởi tạo Giao diện (Mặc định xe đang khóa)
        self.ui = CarSimulatorUI(root, callbacks, initial_lang=self.current_lang)
        self.ui.update_car_state(self.is_unlocked, self.is_user_inside, self.auth_state)

        # 2. Khởi tạo Trình quản lý CAN Bus
        self.can_manager = CanManager(
            on_message_received=self.route_can_message,
            on_log_update=self.safe_write_log
        )
        
        # Bắt đầu kết nối (Sửa COM11 thành cổng máy bạn nếu cần)
        self.can_manager.start(channel='COM11', bustype='slcan', bitrate=500000)

    def route_can_message(self, msg):
        """Hứng dữ liệu từ luồng nền và đưa vào luồng chính Tkinter an toàn"""
        self.root.after(0, self.process_can_logic, msg)

    def safe_write_log(self, message_key, **values):
        """Viết log hệ thống an toàn (Lỗi cáp, thông báo) lên UI"""
        self.root.after(0, self.ui.write_log, message_key, values)

    def process_can_logic(self, msg):
        """Phân rã gói tin CAN thành từng cột: Thời gian, ID, DLC, Data, Mô tả"""
        # 1. Lấy Thời gian
        current_time = time.strftime('%H:%M:%S.') + str(int(time.time() * 1000) % 1000).zfill(3)
        
        # 2. Lấy CAN ID (Định dạng HEX: 0x100)
        can_id_hex = hex(msg.arbitration_id).upper().replace('X', 'x')
        
        # 3. Lấy DLC (Số lượng byte dữ liệu, vd: 8)
        dlc = msg.dlc
        
        # 4. Lấy Data (Định dạng: 01 AA BB CC...)
        data_hex = " ".join(f"{b:02X}" for b in msg.data)
        
        # 5. Phân tích chức năng & Cập nhật trạng thái
        description_key = "desc_unknown_frame"
        
        if dlc > 0 and len(msg.data) > 0:
            frame_header = msg.data[0]

            if frame_header == 0x5A:
                self.is_unlocked = False
                self.is_user_inside = False
                self.auth_state = "no_connection"
                description_key = "desc_locked_no_connection"
            elif frame_header == 0xA5: 
                self.is_unlocked = True
                self.is_user_inside = False
                self.auth_state = "success"
                description_key = "desc_auth_success_open"
            elif frame_header == 0xAA: 
                self.is_unlocked = False
                self.is_user_inside = True
                description_key = "desc_user_inside_locked"
            else:
                if msg.arbitration_id == 0x101:
                    description_key = "desc_welcome_lighting"
                else:
                    description_key = "desc_keep_alive"
        elif msg.arbitration_id == 0x101:
            description_key = "desc_welcome_lighting"
        else:
            description_key = "desc_keep_alive"

        # 6. Truyền 5 tham số để in vào bảng CAN Log (Đúng cột, không bị lộn xộn)
        self.ui.write_can_log(current_time, can_id_hex, dlc, data_hex, description_key)
        
        # 7. Cập nhật Dashboard mô phỏng bên trên
        self.ui.update_car_state(self.is_unlocked, self.is_user_inside, self.auth_state)

    def toggle_language(self):
        """Hàm đổi ngôn ngữ"""
        self.current_lang = "en" if self.current_lang == "vi" else "vi"
        self.ui.update_language_texts(self.current_lang)
        self.safe_write_log("log_language_switched")

    def handle_clear_log(self):
        self.ui.clear_log()

    def on_closing(self):
        self.can_manager.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCarApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
