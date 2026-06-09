import can

def listen_raw_can():
    # NHỚ ĐỔI 'COM3' THÀNH CỔNG COM BẠN ĐANG DÙNG
    port = 'COM11' 
    baudrate = 500000 # Tốc độ 500kbps (chuẩn ô tô)
    
    print(f"[*] Đang mở cổng {port} ở tốc độ {baudrate} bps...")
    try:
        bus = can.interface.Bus(bustype='slcan', channel=port, bitrate=baudrate)
        print("[*] Mở cổng THÀNH CÔNG! Đang lắng nghe dữ liệu (Bấm Ctrl+C để thoát)...")
        print("-" * 50)
        
        while True:
            # Đợi dữ liệu trong 1 giây
            msg = bus.recv(1.0) 
            if msg is not None:
                # Nếu có dữ liệu, in thẳng ra màn hình đen
                print(f"[CÓ TÍN HIỆU] ID: {hex(msg.arbitration_id)} | Data: {[hex(b) for b in msg.data]}")
            else:
                print("[...] Đường truyền CAN đang im lặng, chưa có gói tin nào...")
                
    except Exception as e:
        print(f"[LỖI] {e}")

if __name__ == "__main__":
    listen_raw_can()    