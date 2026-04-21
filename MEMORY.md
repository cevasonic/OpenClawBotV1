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

**2026-04-15 22:55:** Vị trí lưu trữ Cron Jobs của OpenClaw
- Các lệnh CLI như `openclaw cron list` chạy dưới user root (`/root/.openclaw/`) sẽ không thấy các cron jobs nếu dịch vụ OpenClaw Gateway dùng môi trường khác.
- Dịch vụ OpenClaw Gateway thực tế đang lưu cron jobs tại file: `/opt/openclaw/.openclaw/cron/jobs.json`.
- Khi cần kiểm tra, thêm, xóa hoặc sửa cron job, **bắt buộc** phải kiểm tra và thao tác trên file này thay vì tìm kiếm lung tung.

**2026-06-17:** Quy trình làm việc phát triển tính năng mới
- Khi phát triển chức năng/tính năng/skill mới: Trước tiên phác thảo ý tưởng lên file `.md` (ví dụ: `finance.md`, `skill.md`).
- Mỗi lần có hướng mới/ý tưởng mới: Lôi file `.md` đó ra và chỉnh sửa bổ sung liên tục.
- Chỉ khi file `.md` hoàn tất (đã rõ ràng, đầy đủ) thì mới bắt đầu build thành sản phẩm hoàn chỉnh.
- **Ưu điểm:** Dễ theo dõi tiến độ, dễ chỉnh sửa, tránh code sớm quá khi ý tưởng chưa ổn định.

## 💰 Quản lý Tài chính & Chi tiêu
- **LUẬT CỨNG:** Toàn bộ dữ liệu thu chi, chi tiêu hàng ngày BẮT BUỘC phải lưu trữ theo hệ thống trong thư mục `finance/`. 
- **TUYỆT ĐỐI KHÔNG** ghi tạm vào các file memory ngày (`memory/YYYY-MM-DD.md`) hay tự tạo file lẻ (như `chi_tieu_ngay_hom_nay.md`).
- **Cách nhập liệu:** Tự động gọi script `python finance/scripts/add_expense.py` với tham số đúng theo mẫu trong file `/root/.openclaw/workspace/finance/README.md`. Bắt buộc đọc file `README.md` này trước mỗi khi anh Bình yêu cầu nhập dữ liệu chi tiêu nếu không nhớ cú pháp lệnh.
