# can_manager.py
import threading
import time
try:
    import can
except ImportError:
    can = None

class CanManager:
    def __init__(self, on_message_received, on_log_update):
        self.can_bus = None
        self.is_running = False
        self.on_message_received = on_message_received
        self.on_log_update = on_log_update
        
        self.channel = 'COM11'
        self.bustype = 'slcan'
        self.bitrate = 500000

    def start(self, channel='COM11', bustype='slcan', bitrate=500000):
        if can is None:
            self.on_log_update("log_python_can_missing")
            return
            
        self.channel = channel
        self.bustype = bustype
        self.bitrate = bitrate
        self.is_running = True
        
        # Chạy luồng ngầm bất tử
        thread = threading.Thread(target=self._can_loop, daemon=True)
        thread.start()

    def _can_loop(self):
        """Vòng lặp ngầm liên tục kiểm tra phần cứng và đọc gói tin"""
        while self.is_running:
            # 1. Nếu chưa có kết nối -> Cố gắng kết nối
            if self.can_bus is None:
                try:
                    self.can_bus = can.interface.Bus(bustype=self.bustype, channel=self.channel, bitrate=self.bitrate)
                    self.on_log_update("log_can_connected", channel=self.channel)
                except Exception:
                    self.on_log_update("log_can_board_missing", channel=self.channel)
                    time.sleep(0.5)
                    continue

            # 2. Đã có kết nối -> Lắng nghe gói tin
            try:
                msg = self.can_bus.recv(1.0) # Timeout 1s
                if msg is not None:
                    self.on_message_received(msg)
            except Exception:
                # BỊ RÚT CÁP ĐỘT NGỘT: Luồng nhảy vào đây
                self.on_log_update("log_can_disconnected")
                
                if self.can_bus:
                    try:
                        # BẮT BUỘC PHẢI BỌC TRY-EXCEPT Ở ĐÂY
                        # Vì thư viện sẽ cố gửi lệnh tắt xuống cáp đã rút, gây ra lỗi thứ 2
                        self.can_bus.shutdown()
                    except Exception:
                        pass # Phớt lờ lỗi vì phần cứng đã mất
                
                self.can_bus = None # Xóa bus cũ để vòng lặp tự động kết nối lại
                time.sleep(0.5)

    def stop(self):
        """Đóng luồng và ngắt kết nối an toàn"""
        self.is_running = False
        if self.can_bus:
            try:
                self.can_bus.shutdown()
            except Exception:
                pass
