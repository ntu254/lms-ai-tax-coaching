#!/bin/bash
# ==============================================================================
# Script tự động sao lưu dữ liệu Frappe LMS (Database + File tải lên)
# Chạy thủ công: ./backup.sh
# Hoặc thêm vào Crontab: 0 2 * * * /opt/lms/deploy/azure/backup.sh
# ==============================================================================

set -e

BACKUP_DIR="/opt/lms/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CONTAINER_NAME="lms-prod-frappe-1"

# Kiểm tra nếu đang chạy compose thường thì đổi tên container tương ứng
if ! docker ps --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    CONTAINER_NAME="lms-frappe-1"
fi

echo "=== Đang bắt đầu sao lưu hệ thống LMS ($TIMESTAMP) ==="
mkdir -p "$BACKUP_DIR"

# 1. Thực hiện lệnh bench backup bên trong container
docker exec "$CONTAINER_NAME" bench --site lms.localhost backup --with-files

# 2. Sao chép file backup ra thư mục an toàn trên máy chủ Azure
docker cp "$CONTAINER_NAME":/home/frappe/frappe-bench/sites/lms.localhost/private/backups/ "$BACKUP_DIR/backup_$TIMESTAMP"

echo "=== Sao lưu hoàn tất vào: $BACKUP_DIR/backup_$TIMESTAMP ==="

# 3. Tự động dọn dẹp các bản sao lưu cũ hơn 7 ngày để tiết kiệm dung lượng đĩa
find "$BACKUP_DIR" -maxdepth 1 -type d -name "backup_*" -mtime +7 -exec rm -rf {} +
echo "=== Đã dọn dẹp các bản sao lưu cũ hơn 7 ngày ==="
