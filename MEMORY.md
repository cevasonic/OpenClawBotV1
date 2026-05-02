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

**2026-04-24:** Zalo Channel - Authentication vs Pairing
- **Vấn đề:** Zalo session đã hết hạn (`zlogtype: "EXPIRED"`) nhưng vẫn nhắn tin được qua Control UI.
- **Nguyên nhân:** OpenClaw có 2 cơ chế xác thực riêng biệt:
  1. **Zalo Authentication** (credentials.json) → Dùng cho Zalo app/API → Expired thì không đọc/gửi được tin nhắn từ Zalo app.
  2. **Device Pairing** (paired.json) → Dùng cho Control UI/CLI → Vẫn hoạt động nếu device đã pair.
- **Config đã áp dụng:** `channels.zalouser.dmPolicy = "pairing"` → Chỉ cho phép device đã pair, không cần Zalo auth.
- **Kết luận:** Vẫn chat được vì dùng Control UI (đã pair), không qua Zalo app.
- **Lưu ý:** Nếu muốn dùng Zalo app (điện thoại), cần re-authenticate với `openclaw plugins zalouser auth`.
- **File tham khảo:** `/root/.openclaw/workspace/knowledge/zalo-channel-authentication.md`

## 💰 Quản lý Tài chính & Chi tiêu
- **LUẬT CỨNG:** Toàn bộ dữ liệu thu chi, chi tiêu hàng ngày BẮT BUỘC phải lưu trữ theo hệ thống trong thư mục `finance/`. 
- **TUYỆT ĐỐI KHÔNG** ghi tạm vào các file memory ngày (`memory/YYYY-MM-DD.md`) hay tự tạo file lẻ (như `chi_tieu_ngay_hom_nay.md`).
- **Cách nhập liệu:** Tự động gọi script `python finance/scripts/add_expense.py` với tham số đúng theo mẫu trong file `/root/.openclaw/workspace/finance/README.md`. Bắt buộc đọc file `README.md` này trước mỗi khi anh Bình yêu cầu nhập dữ liệu chi tiêu nếu không nhớ cú pháp lệnh.

---

## 🏗️ Dự Án Con Kiến (OpenClaw v0.1)
- **File gốc:** `Conkien/Conkien.md` (phiên bản 1.4, ngày 30/04/2026)
- **Mục tiêu:** Thư ký ảo thực thụ cho quản lý dự án CNTT Shane, làm việc qua Zalo Personal
- **8 tính năng cốt lõi:** Nhận forward & hiểu ngữ cảnh, báo cáo tiến độ, nhắc nhở dự án "chết", tư vấn mở rộng thị trường, báo cáo hàng ngày, nhắc lịch & công việc, soạn thảo & chỉnh sửa văn bản/Excel, công việc phát sinh
- **Quy tắc vận hành:** 
  - Khi nói "lưu vào ..." (ngắn/tắt) → Gateway tự map dựa trên WORKFLOW_VNPT_DRIVE.md
  - Nếu không chắc 100% về dự án → hỏi lại ngay
  - AI chỉnh sửa rồi gửi lại file qua Zalo (Excel/Văn bản)
  - Nếu không rõ về Excel/Văn bản → hỏi lại ngay
  - Tin nhắn không ngữ cảnh → bắt buộc hỏi lại về dự án nào
  - Xử lý batch file không rõ → hỏi lại ngay
- **Cấu trúc Notion:** 2 DB cốt lõi (Units DB + Projects DB)
- **Tiến độ:** Quản lý bằng nhật ký (không dùng %)
- **Tone OpenClaw:** Nhẹ nhàng, lịch sự, đủ ý, rõ ràng (không cụt ngủn như Shane)

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
2. **Dự án Con kiến:** 
   - Tất cả thảo luận, thực hiện chỉ làm trong thư mục `Conkien/`
   - Khi Anh Bình hỏi về "dự án con kiến" → Mình chỉ truy cập thư mục `Conkien/`
   - Không làm việc ngoài thư mục này khi liên quan đến dự án này