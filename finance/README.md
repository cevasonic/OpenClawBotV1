# Hệ Thống Theo Dõi Chi Tiêu Cá Nhân

Hệ thống theo dõi chi tiêu cá nhân với khả năng tổng hợp theo ngày, tuần, tháng và phân loại theo nguồn/mục chi phí.

## 📁 Cấu Trúc Thư Mục

```
finance/
├── config.yaml              # Cấu hình nguồn, mục chi phí
├── daily/                   # Chi tiết từng ngày (YAML)
│   ├── 2025-06-17.yaml
│   └── 2025-06-18.yaml
├── summaries/               # Báo cáo tổng hợp (tự động)
│   ├── daily_2025-06-17.yaml
│   ├── weekly_2025-06-17.yaml
│   └── ...
└── scripts/
    ├── add_expense.py       # Thêm chi tiêu mới
    ├── summarize.py         # Tổng hợp báo cáo
    └── backup_to_github.sh  # Backup lên GitHub
```

## 🚀 Cách Sử Dụng

### 1. Thêm Chi Tiêu Mới

```bash
# Thêm một khoản chi mới
python finance/scripts/add_expense.py \
  --date 2025-06-17 \
  --time "12:30" \
  --category "Ăn trưa" \
  --amount 165000 \
  --source "Cơ quan" \
  --note "Nhà hàng ABC"
```

**Tham số:**
- `--date`: Ngày chi (YYYY-MM-DD), bắt buộc
- `--time`: Thời gian (HH:MM), bắt buộc
- `--category`: Mục chi phí, bắt buộc
- `--amount`: Số tiền (VNĐ), bắt buộc
- `--source`: Nguồn chi phí, bắt buộc
- `--note`: Ghi chú (tùy chọn)

**Lưu ý:**
- Nếu `category` hoặc `source` chưa có trong danh sách mặc định, hệ thống sẽ hỏi xác nhận để thêm mới.
- File chi tiêu sẽ được tạo/tự động cập nhật tại `finance/daily/YYYY-MM-DD.yaml`.

### 2. Xem Tổng Hợp

#### Theo Ngày
```bash
python finance/scripts/summarize.py --date 2025-06-17
```

Output:
```
=== CHI TIÊU NGÀY 2025-06-17 ===
Thời gian   Mục             Số tiền       Nguồn
-------------------------------------------------------
08:00       Ăn sáng         150,000       Cơ quan
09:30       Cafe sáng       84,000        Cơ quan
12:30       Ăn trưa         165,000       Cơ quan
-------------------------------------------------------
TỔNG                              399,000 VNĐ
```

#### Theo Tuần
```bash
# Tổng hợp tuần chứa ngày 2025-06-17
python finance/scripts/summarize.py --week 2025-06-17
```

#### Theo Tháng
```bash
python finance/scripts/summarize.py --month 2025-06
```

#### Theo Nguồn Chi Phí
```bash
python finance/scripts/summarize.py --source "Cơ quan"
```

#### Theo Mục Chi Phí
```bash
python finance/scripts/summarize.py --category "Ăn sáng"
```

### 3. Lưu Báo Cáo

Thêm cờ `--save` để lưu báo cáo tổng hợp vào thư mục `summaries/`:

```bash
# Lưu báo cáo ngày
python finance/scripts/summarize.py --date 2025-06-17 --save

# Lưu báo cáo tuần
python finance/scripts/summarize.py --week 2025-06-17 --save

# Lưu báo cáo tháng
python finance/scripts/summarize.py --month 2025-06 --save
```

Báo cáo sẽ được lưu dưới dạng YAML tại `finance/summaries/`.

### 4. Backup Lên GitHub

Backup toàn bộ dữ liệu chi tiêu lên repository GitHub:

```bash
bash finance/scripts/backup_to_github.sh
```

**Lưu ý:**
- Script này sẽ tự động commit và push tất cả thay đổi trong thư mục `finance/`.
- Repository mặc định: `https://github.com/cevasonic/OpenClawBotV1.git`
- Commit message có dạng: `[Finance] Backup chi tiêu ngày YYYY-MM-DD HH:MM:SS`
- Nếu không có thay đổi, sẽ không commit.

**Để backup tự động hàng ngày:**
Có thể thêm cron job (xem phần dưới).

## ⚙️ Cấu Hình

File `finance/config.yaml` cho phép tùy chỉnh:

```yaml
sources:      # Danh sách nguồn chi phí
  - "Cơ quan"
  - "Cá nhân"
  - "Dự án"
  - "Khác"

categories:   # Danh sách mục chi phí
  - "Ăn sáng"
  - "Ăn trưa"
  - "Cafe"
  - "Xăng xe"
  - ...
```

Có thể thêm/sửa/xóa các giá trị tùy ý. Khi thêm chi tiêu với `category` hoặc `source` mới, hệ thống sẽ hỏi xác nhận.

## 📊 Báo Cáo Tự Động

### Tạo Cron Job Backup Hàng Ngày

Thêm vào crontab (cách 1 - dùng file):

```bash
# Sửa file crontab
crontab -e
```

Thêm dòng (backup lúc 23:30 mỗi ngày):
```
30 23 * * * /root/.openclaw/workspace/finance/scripts/backup_to_github.sh >> /var/log/finance_backup.log 2>&1
```

**Lưu ý quan trọng về OpenClaw Cron:**
- OpenClaw Gateway lưu cron jobs tại: `/opt/openclaw/.openclaw/cron/jobs.json`
- Cần kiểm tra file này nếu cron không chạy.

Hoặc dùng cron job của hệ thống (cách 2 - dùng `crontab` trực tiếp):
```
# Kiểm tra crontab hiện tại
crontab -l

# Thêm crontab mới
(crontab -l 2>/dev/null; echo "30 23 * * * /root/.openclaw/workspace/finance/scripts/backup_to_github.sh") | crontab -
```

### Tạo Cron Job Tổng Hợp Tự Động

Có thể tạo thêm cron job để tổng hợp báo cáo hàng ngày:

```bash
# Tạo script tổng hợp hàng ngày
cat > /root/.openclaw/workspace/finance/scripts/daily_summary.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y-%m-%d)
python /root/.openclaw/workspace/finance/scripts/summarize.py --date $DATE --save
EOF
chmod +x /root/.openclaw/workspace/finance/scripts/daily_summary.sh

# Thêm vào crontab (chạy lúc 23:45 mỗi ngày)
(crontab -l 2>/dev/null; echo "45 23 * * * /root/.openclaw/workspace/finance/scripts/daily_summary.sh") | crontab -
```

## 🔧 Xử Lý Lỗi

### Lỗi "file không tồn tại"
Hệ thống sẽ tự động tạo file mới khi thêm chi tiêu đầu tiên cho ngày đó.

### Lỗi "ngày không hợp lệ"
Đảm bảo format ngày là `YYYY-MM-DD` (ví dụ: `2025-06-17`).

### Lỗi "số tiền âm"
Số tiền phải là số dương.

## 📝 Ghi Chú

- Dữ liệu được lưu dưới dạng YAML, dễ đọc và chỉnh sửa thủ công.
- Có thể mở rộng thêm các trường tùy ý (ví dụ: `payment_method`, `receipt`, etc.).
- Hệ thống có thể mở rộng để tích hợp với Google Sheets, database, hoặc API bên ngoài.

## 🔄 Lịch Sử Thay Đổi

- **2025-06-17**: Tạo hệ thống ban đầu với các chức năng cơ bản.
