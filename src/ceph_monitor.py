import subprocess
import json
import requests
import os
import time
from dotenv import load_dotenv

# --- CẤU HÌNH ---
# Load biến môi trường từ file cùng thư mục
load_dotenv("ceph_secrets.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATE_FILE = "/tmp/ceph_last_state_py"

if not BOT_TOKEN or not CHAT_ID:
    print(" Lỗi: Không tìm thấy Token hoặc Chat ID trong .env")
    exit(1)

def send_telegram(message):
    """Gửi tin nhắn cảnh báo"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def get_ceph_status():
    """Chạy lệnh ceph status và trả về JSON"""
    try:
        # -f json: Yêu cầu Ceph trả về định dạng máy đọc
        result = subprocess.run(
            ["sudo", "ceph", "status", "-f", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Lỗi lấy trạng thái Ceph: {e}")
        return None

def main():
    print(" Ceph Monitor (Python) đang chạy...")

    while True:
        data = get_ceph_status()

        if data:
            current_status = data['health']['status']  # HEALTH_OK hoặc HEALTH_WARN

            # Đọc trạng thái cũ
            last_status = "UNKNOWN"
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r") as f:
                    last_status = f.read().strip()

            # So sánh
            if current_status != last_status:
                print(f" Trạng thái đổi: {last_status} -> {current_status}")

                # Tạo nội dung tin nhắn
                icon = "" if current_status == "HEALTH_OK" else ""

                # Lấy chi tiết lỗi (nếu có)
                detail_msg = ""
                if current_status != "HEALTH_OK":
                    # Lấy danh sách các cảnh báo từ JSON
                    checks = data['health'].get('checks', {})
                    for code, info in checks.items():
                        detail_msg += f"- <b>{code}</b>: {info['summary']['message']}\n"

                message = (
                    f"{icon} <b>CEPH STATUS CHANGE</b>\n"
                    f"Status: <b>{current_status}</b>\n"
                    f"----------------\n"
                    f"{detail_msg}"
                )

                send_telegram(message)

                # Lưu trạng thái mới
                with open(STATE_FILE, "w") as f:
                    f.write(current_status)

        # Nghỉ 5 giây trước khi quét lại
        time.sleep(5)

if __name__ == "__main__":
    main()
