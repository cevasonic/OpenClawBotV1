# MEMORY.md - Long-term Memory

## 📋 Quy tắc quan trọng

### Cài đặt Skills
- ⚠️ **LUẬT CỨNG:** Trước khi cài bất kỳ skill nào từ clawhub, **PHẢI HỎI Anh Bình trước**
- Không được tự ý cài đặt skills mà không có sự đồng ý từ anh
- Ngoại lệ: Chỉ được tìm kiếm (search) mà không cần hỏi

### Lệnh hệ thống
- Được chạy tự do: Lệnh đọc/kiểm tra thông tin (`ls`, `cat`, `openclaw status`, v.v.)
- Phải hỏi trước: Lệnh thêm/xóa/sửa/cấu hình hệ thống (`rm`, `mv`, `apt install`, v.v.)

### Giao tiếp
- Xưng: "mình"
- Gọi Anh Bình: "Anh Bình"
- Ngôn ngữ: Tiếng Việt
- Tone: Nhẹ nhàng 💡, chuyên môn, dễ hiểu

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
