#!/bin/bash
# ==============================================================================
# Script cài đặt tự động máy ảo Azure VM (Ubuntu 22.04 / 24.04 LTS) cho Frappe LMS
# ==============================================================================

set -e

echo "=== [1/6] Cập nhật hệ thống Ubuntu ==="
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl wget git ufw htop net-tools ca-certificates gnupg lsb-release

echo "=== [2/6] Tạo 4GB Swap RAM (Chống tràn RAM trên Azure B-series) ==="
if [ ! -f /swapfile ]; then
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "Đã tạo và kích hoạt 4GB Swap thành công!"
else
    echo "Swapfile đã tồn tại, bỏ qua."
fi

echo "=== [3/6] Cài đặt Docker & Docker Compose ==="
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm -f get-docker.sh
    sudo usermod -aG docker "$USER"
    sudo systemctl enable docker
    sudo systemctl start docker
    echo "Đã cài đặt Docker thành công!"
else
    echo "Docker đã được cài đặt, bỏ qua."
fi

echo "=== [4/6] Cài đặt Nginx & Certbot (SSL Let's Encrypt) ==="
sudo apt-get install -y nginx certbot python3-certbot-nginx
sudo systemctl enable nginx
sudo systemctl start nginx

echo "=== [5/6] Cấu hình Firewall (UFW) ==="
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
# Tự động kích hoạt UFW nếu chưa bật
sudo ufw --force enable

echo "=== [6/6] Chuẩn bị thư mục triển khai /opt/lms ==="
sudo mkdir -p /opt/lms
sudo chown -R "$USER":"$USER" /opt/lms

echo ""
echo "=============================================================================="
echo " CHÚC MỪNG! MÁY ẢO AZURE ĐÃ SẴN SÀNG CHO FRAPPE LMS!"
echo "=============================================================================="
echo "Các bước tiếp theo:"
echo "1. Đưa mã nguồn LMS vào thư mục: /opt/lms"
echo "2. Chuyển vào thư mục docker: cd /opt/lms/docker"
echo "3. Khởi chạy: docker compose up -d"
echo "4. Cấu hình Nginx & SSL theo file hướng dẫn README.md"
echo "=============================================================================="
