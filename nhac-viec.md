# Skill: Task & Meeting Manager

Ngày khởi tạo: 2026-04-23
Trạng thái: Đang phác thảo ý tưởng (Drafting)

-----

## 1. Mục tiêu cốt lõi

Xây dựng một skill quản lý công việc (To-do list) kết hợp quản lý lịch họp, hoạt động hoàn toàn qua messaging channels. Tự động hóa việc nhắc nhở và cập nhật trạng thái để giảm thiểu thao tác thủ công.

-----

## 2. Nền tảng & Giao tiếp

- Nền tảng: OpenClaw
- Channels hỗ trợ: Telegram, Zalo, Discord (và các channel khác OpenClaw kết nối)
- Toàn bộ thao tác (tạo mới, xem, sửa, xóa) đều thực hiện qua chat — không có web UI riêng
- Ngôn ngữ phản hồi: Linh hoạt theo ngôn ngữ người dùng nhập vào (gõ tiếng Việt → trả tiếng Việt, gõ tiếng Anh → trả tiếng Anh)
- Đối tượng sử dụng: Cá nhân (single user)

-----

## 3. Phân loại dữ liệu

Hệ thống phân biệt rõ hai loại:

| | Task (Công việc) | Meeting (Lịch họp) |
|---|---|---|
| **Thời gian** | Deadline (hạn chót) | Thời điểm diễn ra cụ thể |
| **Auto-complete** | Không | Có (sau 23:59 ngày diễn ra) |
| **Reminder** | Không | Có (trước 1 ngày) |
| **Calendar sync** | Không | Có (tùy cấu hình) |

-----

## 4. CRUD qua Chat

### Triết lý thiết kế

AI tự hiểu ý định từ ngôn ngữ tự nhiên — người dùng không cần nhớ cú pháp lệnh cứng.

### 4.1 CREATE

- Người dùng gõ tự nhiên, AI tự trích xuất: loại (Task/Meeting), nội dung, thời gian
- Nếu thiếu thông tin quan trọng → AI hỏi lại đúng 1 câu
- Sau khi lưu, bot confirm ngắn gọn

Ví dụ:
> User: "Chiều nay 3h họp với team design"
> Bot: ✅ Đã thêm Meeting — Họp team design, hôm nay 15:00

### 4.2 READ

Hỗ trợ các kiểu query tự nhiên:

| Câu hỏi người dùng | Kết quả trả về |
|---|---|
| “Hôm nay tôi có gì?” | Tasks + Meetings trong ngày |
| “Tuần này bận gì chưa?” | Tất cả items trong 7 ngày tới |
| “Còn task nào chưa xong?” | Tasks đang pending |
| “Lịch họp tháng này” | Meetings trong tháng hiện tại |

### 4.3 UPDATE

- Nếu có nhiều items khớp với mô tả → AI liệt kê và hỏi “Bạn muốn sửa cái nào?” trước khi thực hiện

### 4.4 DELETE

- Luôn confirm trước khi xóa để tránh xóa nhầm

Ví dụ:
> User: "Xóa lịch họp chiều mai đi"
> Bot: Bạn muốn xóa Meeting — Họp team design, ngày mai 15:00? (có/không)

-----

## 5. Lưu trữ (Storage)

### 5.1 Kiến trúc tổng quan

- Source of truth: JSON local trong môi trường OpenClaw
- Mirror: Notion Database (để xem giao diện đẹp, filter, sort)
- Mọi thao tác CRUD đều thực hiện trên JSON trước, sau đó mới đẩy lên Notion

### 5.2 Flow đồng bộ (Sync Flow)

```text
User action (CRUD)
       ↓
Pull từ Notion → cập nhật JSON local (sync in)
       ↓
Thực hiện CRUD trên JSON local
       ↓
Push JSON → Notion (sync out)
       ↓
Confirm với user
```

Xử lý lỗi sync:
- Nếu sync Notion thất bại (pull hoặc push) → vẫn tiếp tục thao tác trên JSON local
- Item bị lỗi sync sẽ được đánh dấu "notion_sync": "pending"
- Hệ thống tự động retry sync ở lần thao tác tiếp theo
- Không block người dùng — tool vẫn hoạt động bình thường khi Notion có vấn đề

### 5.3 Cấu trúc JSON

```json
{
  "config": {
    "purge_after_days": 30
  },
  "tasks": [
    {
      "id": "t_001",
      "type": "task",
      "title": "Nộp báo cáo tháng",
      "deadline": "2026-04-25T17:00:00",
      "status": "pending",
      "notion_sync": "synced",
      "notion_page_id": "abc123",
      "created_at": "2026-04-23T09:00:00",
      "completed_at": null
    }
  ],
  "meetings": [
    {
      "id": "m_001",
      "type": "meeting",
      "title": "Họp team design",
      "start_time": "2026-04-23T15:00:00",
      "status": "pending",
      "notion_sync": "synced",
      "notion_page_id": "def456",
      "created_at": "2026-04-23T09:00:00",
      "completed_at": null
    }
  ]
}
```

### 5.4 Quy tắc lưu trữ

- status có thể là: pending | completed | cancelled
- notion_sync có thể là: synced | pending | failed
- notion_page_id lưu lại để update/delete đúng record trên Notion
- Meeting không cần end_time — mặc định kết thúc lúc 23:59 cùng ngày
- Auto-complete Meeting: hệ thống tự chuyển status → completed sau 23:59 ngày diễn ra
- Cleanup/Purge: Tự động xóa các items có status = completed sau 30 ngày kể từ completed_at

-----

## 6. Tích hợp Calendar (Calendar Integration)

*(Chưa được thảo luận chi tiết — sẽ bổ sung)*

- Nếu item được phân loại là Meeting → tự động tạo sự kiện trên calendar
- Các lựa chọn đang cân nhắc: Notion Calendar hoặc thông qua Maton.ai → Google Calendar

-----

## 7. Nhắc nhở (Reminder)

*(Chưa được thảo luận chi tiết — sẽ bổ sung)*

- Chỉ áp dụng cho Meeting
- Nhắc trước 1 ngày qua channel đang dùng (Telegram/Zalo/Discord)
- Task thông thường không có reminder, chỉ lưu deadline để theo dõi

-----

## 8. Các phần còn lại cần thảo luận

- [ ] Chi tiết Calendar Integration
- [ ] Chi tiết Reminder (trigger, format tin nhắn, xử lý edge case)
- [ ] Edge cases: meeting bị hoãn, task quá hạn chưa xong
- [ ] Format hiển thị danh sách (READ response)