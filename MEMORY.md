# MEMORY.md - Long-term Memory

## 📋 Quy tắc quan trọng

### Cài đặt Skills
- ⚠️ **LUẬT CỨ NG:** Khi Anh Bình yêu cầu cài skill, mình **CỨ CÀI LUÔN, KHÔNG PHẢI HỎI LẠI** !!!!
- Trước đây: Phải hỏi ý trước
- **UPDATE 2026-04-14:** Anh Bình thay đổi quy tắc - cứ cài khi anh nói ạ
- Ngoại lệ: Chỉ được tìm kiếm (search) mà không cần hỏi

### Lệnh hệ thống
- Được chạy tự do: Lệnh đọc/kiểm tra thông tin (`ls`, `cat`, `openclaw status`, v.v.)
- Phải hỏi trước: Lệnh thêm/xóa/sửa/cấu hình hệ thống (`rm`, `mv`, `apt install`, v.v.)

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
- **Cập nhật:** 2025-06-17

---

## 💼 Vai trò Thư ký Công việc

**Kênh Zalo chính** đã được chuyển thành kênh Thư ký công việc từ 2025-06-17.

### Trách nhiệm:
- Tổng hợp công việc từ các nguồn
- Nhắc việc theo lịch/task
- Theo dõi tiến độ và deadline

---

## 📅 Sự kiện sắp tới

| Ngày | Sự kiện | Trạng thái |
|------|----------|------------|
| 21/04/2026 | Cuộc họp VNPT - UBND xã Cần Giuộc | 🟡 Đang chuẩn bị |

---

## 📋 Công việc cần làm

### Cuộc họp VNPT với UBND xã Cần Giuộc
- **Ngày:** Thứ 3, 21/04/2026
- **File:** [`meetings/2025-04-21_VNPT_CongAnXa_Cangiuoc.md`](meetings/2025-04-21_VNPT_CongAnXa_Cangiuoc.md)
- **Trạng thái:** Đang chuẩn bị hồ sơ và tài liệu

---

## 📅 Lịch sử quyết định

**2026-04-13 21:39:** Anh Bình nhắc nhở quy tắc cài skill - phải hỏi ý trước khi cài
- Mình đã tự ý cài xiucheng-self-improving-agent mà không hỏi
- Nhận ra sai lầm và ghi nhận lại luật

**2026-04-13 22:12:** Setup backup lên GitHub
- Đã push tất cả file SOUL.md, MEMORY.md, skills, memories lên repo
- Cài đặt .gitignore để bỏ qua file không cần thiết
- Sẵn sàng restore trên OpenClaw khác lúc nào cần

**2026-04-13 23:50:** Setup Google Drive OAuth qua gog CLI
- Cài gog CLI từ source thành công (v0.12.0-dev)
- Thêm redirect URI: https://ntbinh.tino.page/oauth2/callback
- Đang xác thực qua domain của Anh Bình
- Client ID: 11969482380-pqhbu1d3cameps8tthv16kqmjkd1j3uk.apps.googleusercontent.com

**2026-04-14 00:46:** Anh Bình đổi OAuth Client từ Web app sang Desktop app
- Download file client_secret.json mới (Desktop app)
- Setup gog lại với Desktop app credentials
- Xác thực 2 lần nhưng vẫn gặp lỗi:
  - Lần 1: Keyring password issue (backend = file)
  - Lần 2: Timeout (context deadline exceeded)
- **Kết luận:** gog OAuth vẫn không hoạt động
- **Quyết định:** Chuyển sang rclone để backup

**Status hiện tại:**
✅ GitHub backup - Hoàn tất
⏳ Google Drive (rclone) - Sẵn sàng setup

**2026-04-15 22:55:** Vị trí lưu trữ Cron Jobs của OpenClaw
- Các lệnh CLI như `openclaw cron list` chạy dưới user root (`/root/.openclaw/`) sẽ không thấy các cron jobs nếu dịch vụ OpenClaw Gateway dùng môi trường khác.
- Dịch vụ OpenClaw Gateway thực tế đang lưu cron jobs tại file: `/opt/openclaw/.openclaw/cron/jobs.json`.
- Khi cần kiểm tra, thêm, xóa hoặc sửa cron job, **bắt buộc** phải kiểm tra và thao tác trên file này thay vì tìm kiếm lung tung.
