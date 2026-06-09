import os

# --- ĐƯỜNG DẪN ẢNH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_LOCKED_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "figure", "close.png"))
IMG_UNLOCKED_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "figure", "open.png"))

# --- TỪ ĐIỂN ĐA NGÔN NGỮ (Cập nhật cho Dashboard) ---
LANGS = {
    "vi": {
        "app_title": "Bảng Điều Khiển Hệ Thống Xe",
        "area_1": "❶ Mô phỏng trạng thái xe",
        "area_2": "❷ Bảng thông số",
        "area_3": "❸ Cửa sổ Log CAN thời gian thực",
        "btn_lang": "🌐 Tiếng Anh (EN)",
        "btn_clear": "Xóa Log",
        "chk_autoscroll": "Tự động cuộn",
        
        # Tiêu đề thông số
        "sys_status": "Trạng thái hệ thống",
        "can_conn": "Kết nối CAN",
        "auth": "Xác thực",
        "curr_zone": "Trạng thái vào xe",
        "time": "Thời gian",
        "mcu_fw": "Phiên bản MCU",

        # Giá trị hiển thị
        "val_active": "MỞ KHÓA",
        "val_locked": "ĐÃ KHÓA",
        "val_can_connected": "ĐÃ KẾT NỐI",
        "val_auth_waiting": "CHỜ XÁC THỰC",
        "val_auth_success": "THÀNH CÔNG",
        "val_auth_no_connection": "KHÔNG KẾT NỐI",
        "val_inside": "ĐÃ VÀO TRONG XE",
        "val_outside": "CHƯA VÀO XE",
        "badge_unlocked": "MỞ KHÓA",
        "badge_locked": "ĐÃ KHÓA",

        # Bảng CAN
        "col_time": "Thời gian",
        "col_id": "ID CAN",
        "col_dlc": "DLC",
        "col_data": "Dữ liệu (Hex)",
        "col_desc": "Mô tả",

        # Mô tả log
        "desc_unknown_frame": "Gói tin chưa xác định",
        "desc_welcome_lighting": "Bật đèn chào mừng",
        "desc_keep_alive": "Bản tin định kỳ (Keep-alive)",
        "desc_locked_no_connection": "Xe đang khóa / không có kết nối",
        "desc_auth_success_open": "Xác thực thành công, mở cửa xe",
        "desc_user_inside_locked": "Người đã vào xe, khóa cửa",
        "desc_system_alert": "Cảnh báo hệ thống",

        # Log hệ thống
        "log_language_switched": "Đã chuyển sang Tiếng Việt",
        "log_python_can_missing": "[HỆ THỐNG] Chưa cài đặt thư viện python-can.",
        "log_can_connected": "[HỆ THỐNG] Kết nối USB-to-CAN thành công tại {channel}.",
        "log_can_board_missing": "[CẢNH BÁO] Không tìm thấy mạch ở {channel}. Đang thử lại...",
        "log_can_disconnected": "[HỆ THỐNG] Mất kết nối đột ngột. Đang chờ cắm cáp lại..."
    },
    "en": {
        "app_title": "Vehicle Access Control Dashboard",
        "area_1": "❶ Vehicle Visualization Area",
        "area_2": "❷ Status Panel",
        "area_3": "❸ Real-time CAN Log Window",
        "btn_lang": "🌐 Tiếng Việt (VI)",
        "btn_clear": "Clear Log",
        "chk_autoscroll": "Auto Scroll",
        
        "sys_status": "System Status",
        "can_conn": "CAN Connection",
        "auth": "Authentication",
        "curr_zone": "Vehicle Entry",
        "time": "Time",
        "mcu_fw": "MCU Firmware",

        "val_active": "UNLOCKED",
        "val_locked": "LOCKED",
        "val_can_connected": "CONNECTED",
        "val_auth_waiting": "WAITING",
        "val_auth_success": "SUCCESS",
        "val_auth_no_connection": "NO CONNECTION",
        "val_inside": "INSIDE VEHICLE",
        "val_outside": "OUTSIDE VEHICLE",
        "badge_unlocked": "UNLOCKED",
        "badge_locked": "LOCKED",

        "col_time": "Time",
        "col_id": "CAN ID",
        "col_dlc": "DLC",
        "col_data": "Data (Hex)",
        "col_desc": "Description",

        "desc_unknown_frame": "Unknown frame",
        "desc_welcome_lighting": "Welcome lighting ON",
        "desc_keep_alive": "Periodic frame (Keep-alive)",
        "desc_locked_no_connection": "Vehicle locked / no connection",
        "desc_auth_success_open": "Authentication success, door unlocked",
        "desc_user_inside_locked": "User entered vehicle, door locked",
        "desc_system_alert": "System Alert",

        "log_language_switched": "Switched to English",
        "log_python_can_missing": "[SYSTEM] python-can is not installed.",
        "log_can_connected": "[SYSTEM] USB-to-CAN connected successfully on {channel}.",
        "log_can_board_missing": "[WARNING] No device found on {channel}. Retrying...",
        "log_can_disconnected": "[SYSTEM] Connection lost unexpectedly. Waiting for the cable to be reconnected..."
    }
}
