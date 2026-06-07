# MEMORY.md - Long-term Memory

## 📋 Quy tắc quan trọng

### Gửi File / Tài liệu
- ⚠️ **LUẬT CỨNG:** Khi Anh Bình yêu cầu "gửi file", "lấy file", BẮT BUỘC phải dùng tính năng đính kèm file (MEDIA directive). 
- **TUYỆT ĐỐI KHÔNG** in nội dung text của file ra khung chat dưới mọi hình thức, dù là file code, text hay markdown.

### Cài đặt Skills
- ⚠️ **LUẬT CỨ NG:** Khi Anh Bình yêu cầu cài skill, mình **CỨ CÀI LUÔN, KHÔNG PHẢI HỎI LẠI** !!!!
- Trước đây: Phải hỏi ý trước
- **UPDATE 2026-04-14:** Anh Bình thay đổi quy tắc - cứ cài khi anh nói ạ
- Ngoại lệ: Chỉ được tìm kiếm (search) mà không cần hỏi

### Anh Bình's Philosophy
- ⚠️ **LUẬT CỨNG:** Anh luôn quyết tâm làm việc gì tới cùng, không ngại phức tạp
- **KHINH CHI:** Chỉ sợ về lâu dài không hiệu quả
- Anh muốn giải pháp THỰC SỰ, không phải cách tạm thời
- Nên mình cần hướng tới các giải pháp bền vững, có thể tái sử dụng

## 🔐 GitHub Credentials

**Quan trọng:** Thông tin này để dùng cho backup lên GitHub

- **GitHub Username:** cevasonic
- **Email:** ntbinh.science@gmail.com
- **Repository:** https://github.com/cevasonic/OpenClawBotV1
- **Mục đích:** CHỈ dùng để backup cho OpenClaw này thôi

### Cách sử dụng:
- Backup: `git add . && git commit -m "..." && git push`
- Restore: `git clone https://github.com/cevasonic/OpenClawBotV1.git`

**Lưu ý:** Token được lưu trong git config, không lưu trong MEMORY.md (để bảo vệ)

---

## 📍 Vị trí hiện tại

- **Thành phố:** Tây Ninh
- **Cập nhật:** 2026-04-21

---

## 💼 Vai trò Thư ký Công việc

**Kênh Zalo chính** đã được chuyển thành kênh Thư ký công việc từ 2025-06-17.

### Trách nhiệm:
- Tổng hợp công việc từ các nguồn
- Nhắc việc theo lịch/task
- Theo dõi tiến độ và deadline

---

## 📋 Công việc cần làm

---

## 📅 Lịch sử & Quyết định quan trọng

- **2026-04-13:** Chốt quy tắc cài skill: Cứ cài luôn không cần hỏi lại Anh Bình. Thiết lập backup GitHub (Repo: `cevasonic/OpenClawBotV1`).
- **2026-04-15:** Xác định vị trí Cron Jobs thực tế: `/opt/openclaw/.openclaw/cron/jobs.json`.
- **2025-06-17:** Quy trình dev: Phác thảo ý tưởng vào file `.md` trước khi build code để tránh sửa đổi nhiều lần.
- **2026-04-24:** Làm rõ cơ chế Zalo Auth: Pairing (Control UI) khác with Zalo App Auth. Nếu Zalo App hết hạn, Control UI vẫn chat được qua pairing.
  - *Chi tiết:* [zalo-channel-authentication.md](file:///root/.openclaw/workspace/knowledge/zalo-channel-authentication.md)
- **2026-05-09:** Kích hoạt skill dự án Con Kiến bằng cách tạo symlink từ `Conkien/skills/` sang `skills/` gốc để OpenClaw có thể nạp được.
- **2026-05-31:** Khắc phục triệt để lỗi Cron Job Thư viện Pháp luật bằng cách: (1) đặt shebang `/usr/bin/python3` tuyệt đối cho các script, (2) dọn các tệp HTML debug lớn (>300 KB) ra ngoài workspace để tránh quá tải token, và (3) cấu hình model fallbacks cho OpenClaw để tăng độ bền bỉ khi gọi API.
- **2026-06-07:** Khắc phục triệt để lỗi Cron Job Thư viện Pháp luật (Agent timed out/returns empty response) bằng cách chuyển hẳn công việc sang chạy trực tiếp bằng **System Cron (crontab của Linux)** thay vì chạy qua OpenClaw Agent. Đã viết file script `skills/thuvien/scripts/cron_telegram.sh` để chạy Python cào và gửi kết quả trực tiếp lên Telegram thông qua `curl` (giúp tốn 0 tokens và cực kỳ ổn định). Đồng thời gỡ bỏ cron job cũ khỏi OpenClaw.

---

## 💰 Quản lý Tài chính & Chi tiêu
- **LUẬT CỨNG:** Toàn bộ dữ liệu thu chi, chi tiêu hàng ngày BẮT BUỘC phải lưu trữ theo hệ thống trong thư mục `finance/`. 
- **TUYỆT ĐỐI KHÔNG** ghi tạm vào các file memory ngày (`memory/YYYY-MM-DD.md`) hay tự tạo file lẻ (như `chi_tieu_ngay_hom_nay.md`).
- **Cách nhập liệu:** Tự động gọi script `python finance/scripts/add_expense.py` với tham số đúng theo mẫu trong file `/root/.openclaw/workspace/finance/README.md`. Bắt buộc đọc file `README.md` này trước mỗi khi anh Bình yêu cầu nhập dữ liệu chi tiêu nếu không nhớ cú pháp lệnh.

---

## 🏗️ Dự Án Con Kiến (OpenClaw v0.1)
- **File gốc:** [Conkien.md](file:///root/.openclaw/workspace/Conkien/Conkien.md) (v1.11 - 10/05/2026).
- **Mục tiêu:** Thư ký ảo cho quản lý dự án Shane (Anh Bình) qua Zalo Personal.
- **Cốt lõi:** Hiểu ngữ cảnh forward, báo cáo tiến độ, nhắc lịch, xử lý văn bản/Excel.
- **LUẬT SẮT (Passive Mode):** Tuyệt đối không đọc file khi không có lệnh. Luôn nhắc đến **OneDrive**. 
- **QUY TẮC (Lưu không đọc):** Chỉ upload file, không mở file xem nội dung.

---

## 💰 Tinhtien Skill (OpenRouter Usage Tracker)
- **Mô tả:** Kiểm tra và hiển thị chi tiết credit usage OpenRouter
- **Location:** `/root/.openclaw/workspace/skills/tinhtien/`
- **Scripts:**
  - `scripts/tinhtien.sh` - Script chính
  - `scripts/config.json` - Lưu Management Key
- **API:**
  - Tổng quan: `GET https://openrouter.ai/api/v1/credits`
  - Chi tiết: `GET https://openrouter.ai/api/v1/activity?limit=500` (30 ngày gần nhất)
- **Hiển thị:** Model → Chi phí → % → Requests → Tokens (kèm emoji, phân loại free/paid)

---

## 🔄 Quy tắc thống nhất (2026-05-02)
1. **Tinhtien:** Mỗi khi Anh Bình nói "tính tiền", "tính quota" hoặc tương đương → Mình sẽ chạy skill `tinhtien` ngay lập tức
2. **Dự án Con kiến (Primary):** 
   - Đây là dự án trọng tâm. Mọi tin nhắn trên Zalo mặc định được hiểu là liên quan đến dự án này.
   - Skill `conkien-core` PHẢI được nạp ngay khi bắt đầu session để xác định intent và gateway mapping.
   - Luôn ưu tiên tra cứu thông tin trong thư mục `Conkien/`.