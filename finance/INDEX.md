# Hệ thống theo dõi chi tiêu

Hệ thống theo dõi chi tiêu cá nhân với khả năng tổng hợp theo ngày, tuần, tháng và phân loại theo nguồn/mục chi phí.

## 📁 Cấu Trúc Thư Mục

```
finance/
├── config.yaml              # Cấu hình hệ thống
├── daily/                   # Chi tiết từng ngày (YAML)
├── summaries/               # Báo cáo tổng hợp (tự động)
└── scripts/
    ├── add_expense.py       # Thêm chi tiêu mới
    ├── summarize.py         # Tổng hợp báo cáo
    └── backup_to_github.sh  # Backup lên GitHub
```

## 🚀 Cách Sử Dụng Nhanh

### Thêm chi tiêu mới
```bash
python finance/scripts/add_expense.py \
  --date 2025-06-17 \
  --time "12:30" \
  --category "Ăn trưa" \
  --amount 165000 \
  --source "Cơ quan"
```

### Xem tổng hợp
```bash
# Theo ngày
python finance/scripts/summarize.py --date 2025-06-17

# Theo tuần
python finance/scripts/summarize.py --week 2025-06-17

# Theo tháng
python finance/scripts/summarize.py --month 2025-06

# Theo nguồn
python finance/scripts/summarize.py --source "Cơ quan"

# Theo mục
python finance/scripts/summarize.py --category "Ăn sáng"
```

### Backup lên GitHub
```bash
bash finance/scripts/backup_to_github.sh
```

Để đọc chi tiết đầy đủ, mở file `finance/README.md`.
