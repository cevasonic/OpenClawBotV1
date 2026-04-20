# Hệ thống theo dõi chi tiêu

## 🎯 Mục Tiêu
Xây dựng hệ thống theo dõi chi tiêu cá nhân, cho phép:
- Ghi chép chi tiêu hàng ngày với các mục và nguồn
- Tổng hợp theo ngày/tuần/tháng
- Phân tích theo nguồn và mục chi phí
- Backup tự động lên GitHub

## 📋 Yêu cầu chức năng
- ✅ Thêm chi tiêu mới (date, time, category, amount, source, note)
- ✅ Tự động tính tổng ngày
- ✅ Tổng hợp theo ngày/tuần/tháng/nguồn/mục
- ✅ Lưu trữ file YAML (dễ đọc, dễ edit)
- ✅ Backup thủ công lên GitHub
- ✅ Tự động mở rộng category/source khi thêm mới
- 🔄 Cron job tự động backup hàng ngày (đã có job chung)

## 🏗️ Thiết kế

### Cấu trúc thư mục
```
finance/
├── config.yaml          # Danh sách nguồn, mục chi
├── daily/              # File YAML từng ngày
│   └── YYYY-MM-DD.yaml
├── summaries/          # Báo cáo tổng hợp
│   └── summary_*.yaml
└── scripts/
    ├── add_expense.py
    ├── summarize.py
    └── backup_to_github.sh
```

### File daily structure
```yaml
date: "2025-06-17"
expenses:
  - time: "08:00"
    category: "Ăn sáng"
    amount: 150000
    source: "Cơ quan"
    note: "Ghi chú (optional)"
total: 399000
```

### Config structure
```yaml
sources: ["Cơ quan", "Cá nhân", "Dự án", "Khác"]
categories: ["Ăn sáng", "Ăn trưa", "Cafe", ...]
```

## 🛠️ Tech Stack
- **Backend:** Python 3
- **Storage:** YAML files
- **Version control:** Git/GitHub
- **Automation:** Bash scripts

## 📅 Timeline ước tính
- Phân tích/Research: 1 ngày ✅
- Development: 2 ngày ✅
- Testing: 0.5 ngày ✅
- Deployment: 0.5 ngày ✅
- **Total:** 4 ngày ✅

## 🔗 Tham khảo
- YAML: https://yaml.org/
- OpenClaw cron jobs: `/opt/openclaw/.openclaw/cron/jobs.json`

## 💡 Ghi chú
- Đã triển khai xong, đang vận hành
- Có thể mở rộng với:
  - Web UI để nhập chi tiêu
  - Export sang Google Sheets
  - Thống kê biểu đồ
  - Budget planning và alert

---

**Trạng thái:** ✅ Completed

**Cập nhật lần cuối:** 2025-06-17
