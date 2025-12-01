import time
import os

FILE_PATH = "/mnt/ceph-storage/ha_proof.txt"

print(f" Bắt đầu ghi dữ liệu vào {FILE_PATH}...")
print(" Chuẩn bị tắt máy Node khác đi nào!")

i = 1
try:
    while True:
        # Ghi dòng dữ liệu kèm thời gian thực
        timestamp = time.strftime("%H:%M:%S")
        line = f"Dong {i}: Dữ liệu quan trọng tại {timestamp} - Server vẫn sống!\n"
        
        # Mở file chế độ append (thêm vào cuối)
        with open(FILE_PATH, "a") as f:
            f.write(line)
            # Quan trọng: flush để đẩy dữ liệu từ RAM xuống ổ cứng ngay lập tức
            f.flush()
            os.fsync(f.fileno())
        
        print(f" Đã ghi: {line.strip()}")
        i += 1
        time.sleep(2) # Ghi mỗi 2 giây
except KeyboardInterrupt:
    print("\n Dừng test.")
except Exception as e:
    print(f"\n LỖI GHI DỮ LIỆU: {e}")
