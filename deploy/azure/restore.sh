#!/bin/bash
# ==============================================================================
# Script khôi phục dữ liệu Frappe LMS từ bản sao lưu
# Sử dụng: ./restore.sh <đường_dẫn_tệp_sql_gz>
# ==============================================================================

set -e

if [ -z "$1" ]; then
    echo "Lỗi: Vui lòng cung cấp đường dẫn đến file sao lưu .sql.gz!"
    echo "Ví dụ: ./restore.sh /opt/lms/backups/backup_20261111_020000/xxx-database.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"
CONTAINER_NAME="lms-prod-frappe-1"

if ! docker ps --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    CONTAINER_NAME="lms-frappe-1"
fi

echo "=== Đang sao chép file backup vào container ==="
docker cp "$BACKUP_FILE" "$CONTAINER_NAME":/tmp/restore_db.sql.gz

echo "=== Đang khôi phục cơ sở dữ liệu ==="
docker exec -it "$CONTAINER_NAME" bench --site lms.localhost restore /tmp/restore_db.sql.gz --mariadb-root-password 123

echo "=== Đang xóa cache và khởi động lại ==="
docker exec "$CONTAINER_NAME" bench --site lms.localhost migrate
docker exec "$CONTAINER_NAME" bench --site lms.localhost clear-cache

echo "=== KHÔI PHỤC DỮ LIỆU THÀNH CÔNG! ==="
