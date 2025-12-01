#!/bin/bash

# --- NẠP BIẾN MÔI TRƯỜNG ---
# Lấy đường dẫn tuyệt đối của file script để tìm file .env nằm cùng thư mục
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/ceph_secrets.env"

# Kiểm tra file .env có tồn tại không
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"  # <--- Lệnh này sẽ load các biến trong file .env vào script
else
    echo " Lỗi: Không tìm thấy file cấu hình $ENV_FILE"
    exit 1
fi

# --- HÀM GỬI TIN NHẮN (Dùng biến đã load) ---
send_telegram() {
    local MSG="$1"
    # Biến $TELEGRAM_BOT_TOKEN và $TELEGRAM_CHAT_ID được lấy từ file .env
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d parse_mode="HTML" \
        --data-urlencode "text=$MSG" > /dev/null
}

# --- LOGIC CHÍNH (Giữ nguyên như cũ) ---

CURRENT_STATUS=$(sudo ceph health | awk '{print $1}')
DETAIL=$(sudo ceph status)

if [ -f "$STATE_FILE" ]; then
    LAST_STATUS=$(cat "$STATE_FILE")
else
    LAST_STATUS="UNKNOWN"
fi

if [ "$CURRENT_STATUS" != "$LAST_STATUS" ]; then
    echo "$(date): Trạng thái thay đổi từ $LAST_STATUS sang $CURRENT_STATUS"

    ICON="️"
    if [ "$CURRENT_STATUS" == "HEALTH_OK" ]; then
        ICON=""
        MSG="$ICON <b>CEPH CLUSTER KHÔI PHỤC</b>%0AStatus: <b>$CURRENT_STATUS</b>"
    else
        ICON=""
        SHORT_DETAIL=$(echo "$DETAIL" | head -n 10)
        MSG="$ICON <b>CEPH CLUSTER CẢNH BÁO</b>%0AStatus: <b>$CURRENT_STATUS</b>%0A----------------%0A<pre>$SHORT_DETAIL</pre>"
    fi

    send_telegram "$MSG"
    echo "$CURRENT_STATUS" > "$STATE_FILE"
else
    echo "$(date): Không đổi ($CURRENT_STATUS)"
fi
