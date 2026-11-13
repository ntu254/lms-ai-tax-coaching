# Hướng Dẫn Triển Khai Frappe LMS Lên Microsoft Azure VM (Ubuntu)

Tài liệu này hướng dẫn chi tiết từ A - Z cách chuẩn bị, cấu hình và triển khai hệ thống Frappe LMS (đã Việt hóa 100%, tích hợp tài khoản, tiền tệ VNĐ và múi giờ GMT+7) lên máy ảo **Microsoft Azure Virtual Machine**.

---

## Danh Mục Các Tệp Triển Khai Trong Thư Mục Này

| Tệp | Mục đích |
| :--- | :--- |
| [setup_vm.sh](setup_vm.sh) | Script tự động 1-click cài đặt Docker, Compose, Nginx, Certbot, Swap 4GB và tường lửa UFW trên máy ảo Ubuntu mới. |
| [docker-compose.prod.yml](docker-compose.prod.yml) | Cấu hình Docker Compose cho Production: tự động khởi động lại, bảo vệ dữ liệu với persistent volumes, bind cổng nội bộ 127.0.0.1. |
| [.env.example](.env.example) | Mẫu biến môi trường (Domain, Mật khẩu DB, Mật khẩu Admin). |
| [nginx/lms.conf](nginx/lms.conf) | Cấu hình Nginx Reverse Proxy chuẩn: WebSocket realtime, nén Gzip, cho phép upload tệp đến 100MB. |
| [backup.sh](backup.sh) | Script tự động sao lưu toàn bộ cơ sở dữ liệu và file tải lên của học viên. |
| [restore.sh](restore.sh) | Script khôi phục dữ liệu nhanh chóng khi cần. |

---

## BƯỚC 1: Tạo Máy Ảo (VM) Trên Azure Portal

1. Truy cập [portal.azure.com](https://portal.azure.com/) và tìm **Virtual machines** > chọn **Create** > **Azure virtual machine**.
2. **Cấu hình Cơ bản (Basics)**:
   - **Resource group**: Chọn hoặc tạo mới (ví dụ: `rg-lms-vietnam`).
   - **Virtual machine name**: `vm-lms-app`.
   - **Region**: Khuyên chọn **Southeast Asia (Singapore)** hoặc **East Asia (Hong Kong)** để học viên tại Việt Nam truy cập nhanh nhất.
   - **Image**: **Ubuntu Server 22.04 LTS - x64 Gen2** (hoặc 24.04 LTS).
   - **Size**: 
     - *Thử nghiệm*: **Standard_B2ms** (2 vCPU, 8 GiB RAM).
     - *Sản xuất (500 - 3.000 học viên)*: **Standard_B4ms** (4 vCPU, 16 GiB RAM).
   - **Authentication type**: Chọn **SSH public key** (hoặc Password).
3. **Cấu hình Ổ Đĩa (Disks)**:
   - **OS disk type**: **Premium SSD**.
   - **Size**: 64 GiB hoặc 128 GiB.
4. **Cấu hình Mạng (Networking)**:
   - **Public IP**: Chọn *Create new* với SKU **Standard** (IP tĩnh).
   - **NIC network security group**: Chọn **Advanced** hoặc **Basic**.
   - **Inbound ports**: Đánh dấu chọn **SSH (22)**.
5. **Mở Cổng Mạng (Inbound Security Rules)**:
   - Sau khi VM tạo xong, mở VM > **Networking** > **Add inbound security rule**:
     - Cổng **80** (HTTP): Port `80`, Protocol `TCP`, Action `Allow`, Priority `1010`.
     - Cổng **443** (HTTPS): Port `443`, Protocol `TCP`, Action `Allow`, Priority `1020`.

---

## BƯỚC 2: Cài Đặt Môi Trường Trên Máy Ảo (Tự Động 1-Click)

1. Mở Terminal trên máy tính của bạn và kết nối SSH vào máy ảo Azure:
```bash
ssh azureuser@<PUBLIC_IP_CUA_AZURE_VM>
```

2. Tải và chạy script cài đặt tự động môi trường (Docker, Swap 4GB, Nginx, Certbot):
```bash
# Tải script setup_vm.sh và phân quyền thực thi
curl -sSL https://raw.githubusercontent.com/<YOUR_REPO>/<BRANCH>/deploy/azure/setup_vm.sh -o setup_vm.sh
# Hoặc nếu đã copy mã nguồn lên máy ảo:
chmod +x /opt/lms/deploy/azure/setup_vm.sh
sudo /opt/lms/deploy/azure/setup_vm.sh
```

---

## BƯỚC 3: Đưa Mã Nguồn Dự Án Lên Máy Ảo & Khởi Chạy

1. Chuyển vào thư mục `/opt/lms`:
```bash
cd /opt/lms
# Clone repo của bạn về thư mục này:
git clone <URL_GIT_REPO_CUA_BAN> .
```

2. Khởi chạy hệ thống bằng Docker Compose:
```bash
cd /opt/lms/docker
docker compose up -d
```

3. Theo dõi tiến trình khởi tạo tự động (nạp ngôn ngữ tiếng Việt, múi giờ GMT+7, tạo user):
```bash
docker compose logs -f frappe
```
> Khi màn hình xuất hiện thông báo `bench serve --host 0.0.0.0 --port 8000` là hệ thống đã sẵn sàng hoạt động!

---

## BƯỚC 4: Trỏ Tên Miền (DNS) & Cài Đặt SSL HTTPS

1. **Trỏ bản ghi DNS**:
   - Truy cập trang quản lý tên miền của bạn (Cloudflare, Namecheap, v.v.).
   - Tạo bản ghi **A**:
     - **Host / Name**: `lms` (hoặc `@` nếu dùng domain chính)
     - **Value / IPv4**: `<PUBLIC_IP_AZURE_VM>`

2. **Cấu hình Nginx**:
   Sao chép file cấu hình Nginx mẫu vào thư mục Nginx của hệ thống:
   ```bash
   sudo cp /opt/lms/deploy/azure/nginx/lms.conf /etc/nginx/sites-available/lms.conf
   ```
   Mở file và sửa tên miền `lms.yourdomain.com` thành tên miền thật của bạn:
   ```bash
   sudo nano /etc/nginx/sites-available/lms.conf
   ```
   Kích hoạt và nạp lại Nginx:
   ```bash
   sudo ln -sf /etc/nginx/sites-available/lms.conf /etc/nginx/sites-enabled/
   sudo rm -f /etc/nginx/sites-enabled/default
   sudo nginx -t
   sudo systemctl reload nginx
   ```

3. **Cấp chứng chỉ SSL miễn phí (Let's Encrypt)**:
   ```bash
   sudo certbot --nginx -d lms.yourdomain.com
   ```
   Nhập email của bạn và chọn đồng ý. Certbot sẽ tự động cấu hình HTTPS và tự động gia hạn khi gần hết hạn.

---

## BƯỚC 5: Đăng Nhập & Quản Trị Hệ Thống

1. Mở trình duyệt và truy cập: `https://lms.yourdomain.com`
2. Đăng nhập bằng tài khoản Quản trị viên:
   - **Email / Username**: `Administrator`
   - **Password**: `admin` *(Hãy đổi ngay sau khi đăng nhập: nhấn vào avatar góc trên bên phải > Đổi mật khẩu)*
3. Các tài khoản kiểm thử đã tạo sẵn:
   - **Giảng viên**: `teacher@example.com` / `123456`
   - **Điều phối viên (Moderator)**: `jannat@example.com` / `123456`
   - **Người chấm thi (Evaluator)**: `ash@ipp.com` / `123456`
   - **Học viên**: `john.doe@example.com` / `123456`

---

## BƯỚC 6: Cấu Hình Email Gửi Đi (SMTP) Trên Azure

Azure chặn cổng SMTP 25 đi ra ngoài. Do đó, bạn cần sử dụng cổng **587** (TLS).
1. Đăng nhập với quyền `Administrator`.
2. Vào **Cài đặt** (Settings) > **Giao tiếp & Liên hệ** > **Tài khoản email** (`Email Accounts`).
3. Thêm tài khoản mới:
   - **Email**: `noreply@yourdomain.com` (hoặc Gmail của bạn).
   - **SMTP Server**: `smtp.sendgrid.net` (hoặc `smtp.gmail.com`).
   - **Port**: `587`.
   - **Use TLS**: Bật (Tích chọn).
   - **Password**: Mật khẩu ứng dụng (App Password).

---

## BƯỚC 7: Cấu Hình Sao Lưu Tự Động (Cronjob)

Để hệ thống tự động sao lưu dữ liệu mỗi đêm lúc 2:00 AM:
```bash
chmod +x /opt/lms/deploy/azure/backup.sh
crontab -e
```
Thêm dòng sau vào cuối file crontab:
```cron
0 2 * * * /opt/lms/deploy/azure/backup.sh >> /var/log/lms_backup.log 2>&1
```
Bản sao lưu sẽ được lưu tại `/opt/lms/backups/` và tự động giữ lại trong 7 ngày gần nhất.
