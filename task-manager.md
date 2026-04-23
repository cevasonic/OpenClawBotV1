# Ý Tưởng Skill Quản Lý Công Việc & Lịch Họp (Task & Meeting Manager)

**Ngày khởi tạo:** 2026-04-23
**Trạng thái:** Đang phác thảo ý tưởng (Drafting)

## 1. Mục tiêu cốt lõi
- Xây dựng một công cụ quản lý công việc (To-do list) kết hợp quản lý lịch họp.
- Tự động hóa việc nhắc nhở và cập nhật trạng thái để giảm thiểu thao tác thủ công.

## 2. Các tính năng chính (Core Features)

### 2.1. Ghi nhận & Nhắc nhở (Input & Reminder)
- **Tiếp nhận:** Người dùng gửi nội dung công việc/lịch họp qua chat. Hệ thống tự động phân tích và lưu lại.
- **Nhắc nhở:** Nếu nội dung có chứa thời hạn (deadline) hoặc thời gian cụ thể, hệ thống sẽ tự động lên lịch nhắc nhở.

### 2.2. Tự động hoàn thành lịch họp (Auto-completion for Meetings)
- Phân loại rõ ràng giữa "Công việc" (Task) và "Lịch họp" (Meeting).
- Đối với Lịch họp: Khi thời gian diễn ra cuộc họp kết thúc, hệ thống mặc định tự động chuyển trạng thái sang "Đã hoàn thành" (Done/Completed).

### 2.3. Truy vấn & Thống kê (Query & View)
- Khi người dùng yêu cầu xem danh sách công việc, hệ thống sẽ lọc và hiển thị:
  - Các công việc/lịch họp sắp tới (tính từ thời điểm truy vấn đến tương lai).
  - Các công việc đã được đánh dấu hoàn tất trước thời hạn (Early completed tasks).

### 2.4. Tích hợp Calendar (Calendar Integration)
- Nếu sự kiện được xác định là "Lịch họp", hệ thống không chỉ lưu vào To-do list cục bộ mà sẽ gọi API để tạo luôn sự kiện trên Lịch (Notion Calendar hoặc Google Calendar).

## 3. Các vấn đề cần làm rõ thêm (Open Questions)
1. Sử dụng Google Calendar hay Notion Calendar làm nền tảng chính?
2. Cơ chế nhắc việc: Gửi tin nhắn qua Telegram tại thời điểm deadline hay trước đó bao nhiêu phút?
3. Cấu trúc lưu trữ dữ liệu cục bộ (JSON, SQLite hay file Markdown)?
