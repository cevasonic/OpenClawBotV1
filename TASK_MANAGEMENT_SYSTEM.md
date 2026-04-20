# Hệ thống Quản lý Công việc (Task Management)

## 🎯 Mục tiêu
Hệ thống quản lý công việc cao cấp, tập trung vào:
- **Cuộc họp/ sự kiện** → sinh ra các **task cần prepare**
- **Task** → có cấu trúc chi tiết, theo dõi tiến độ
- **Nhắc việc thông minh** dựa trên timeline

---

## 📁 Cấu trúc thư mục

```
/root/.openclaw/workspace/
├── tasks/
│   ├── active/          # Tasks đang active
│   ├── completed/       # Tasks đã hoàn thành
│   ├── archived/        # Tasks đã lưu trữ
│   └── templates/       # Templates cho các loại task
├── meetings/
│   └── [meeting-files]  # Files meeting (đã có)
├── taskflow/            # Workflow definitions (nếu dùng taskflow skill)
└── task_report.md       # Báo cáo tổng hợp hàng ngày
```

---

## 🗂️ Schema Task (JSON/YAML)

```yaml
id: "TASK-20250421-001"           # Unique ID
title: "Chuẩn bị báo giá cho cuộc họp"
description: |
  Chi tiết công việc cần làm...
meeting_id: "MTG-20250421"        # Link đến meeting (nếu có)
parent_task: null                 # Task cha (nếu có sub-task)
sub_tasks:                       # Danh sách sub-tasks
  - id: "SUB-001"
    title: "Lấy báo giá từ nhà cung cấp"
    status: "pending"
    assignee: "Anh A"
    due_date: "2025-04-20"
    priority: "high"
    checklist:                    # Checklist con
      - "Liên hệ nhà cung cấp X"
      - "Yêu cầu báo giá 3 PA"
      - "Xác nhận giá cả, chính sách"

assignee: "Dương Quang Trường"    # Người phụ trách chính
co_assignees:                     # Người phụ trách phụ
  - "Nguyễn Văn B"
priority: "high"                  # low | medium | high | critical
status: "in_progress"             # pending | in_progress | review | done | blocked
due_date: "2025-04-20"            # Deadline
start_date: "2025-04-19"          # Ngày bắt đầu (nếu có)
estimated_hours: 4                # Thời gian ước tính
actual_hours: null                # Thời gian thực tế
tags:                             # Tags để filter
  - "pre-meeting"
  - "báo giá"
  - "VNPT"
dependencies:                     # Các task phụ thuộc
  - "TASK-20250420-005"
blockers:                         # Điều cần giải quyết trước
  - "Chưa có spec camera cụ thể"
notes:                            # Ghi chú
  - "Cần xác nhận model camera với kỹ thuật"
created_at: "2025-04-19T10:30:00"
updated_at: "2025-04-19T10:30:00"
completed_at: null
version: 1                        # Version để conflict resolution
```

---

## 🔄 Workflow States

```
PENDING → IN_PROGRESS → REVIEW → DONE
                ↓
            BLOCKED (cần giải quyết blocker)
```

---

## 📋 Task Types

| Type | Mô tả | Template |
|------|-------|---------|
| **pre-meeting** | Chuẩn bị trước cuộc họp | prep-meeting.yaml |
| **follow-up** | Việc cần làm sau cuộc họp | followup.yaml |
| **research** | Nghiên cứu, thu thập thông tin | research.yaml |
| **document** | Soạn thảo tài liệu | document.yaml |
| **review** | Review, phê duyệt | review.yaml |
| **approval** | Cần phê duyệt từ cấp trên | approval.yaml |

---

## 🏷️ Priority Levels

| Level | Màu | Khi nào dùng |
|-------|-----|-------------|
| **Critical** | 🔴 | Coi trọng, ảnh hưởng lớn nếu không làm |
| **High** | 🟠 | Quan trọng, cần làm sớm |
| **Medium** | 🟡 | Bình thường, có thể linh hoạt |
| **Low** | ⚪ | Có thể làm sau |

---

## 🔔 Cơ chế Nhắc việc

### Theo thời gian:
- **Due date approaches** (1 ngày, 3 ngày, 7 ngày trước)
- **Overdue** (đã quá hạn)
- **Daily standup** (danh sách task hôm nay)

### Theo sự kiện:
- **Khi meeting được tạo** → Tự động sinh task prepare
- **Khi task cha thay đổi** → Nhắc sub-tasks
- **Khi blocker được resolves** → Thông báo

---

## 📊 Báo cáo

### Daily Report (6h sáng)
```markdown
📅 **19/04/2026 - NHM 3/2025**

🔴 **Tasks cần làm hôm nay (3):**
1. [HIGH] TASK-001: Liên hệ nhà cung cấp camera
2. [MED] TASK-002: Chuẩn bị slide trình bày
3. [LOW] TASK-003: Đặt phòng họp

⏳ **Tasks đang blocked (1):**
- TASK-004: Chưa có spec kỹ thuật (liên hệ anh Cường)

✅ **Tasks hoàn thành hôm qua (2):**
- TASK-005: Lấy báo giá từ nhà cung cấp A
- TASK-006: Soạn thảo Nội dung họp

📊 **Tiến độ tuần này: 40%**
```

### Meeting Prep Report (1 ngày trước)
```markdown
🔔 **NHẮC: Cuộc họp VNPT - UBND Cần Giuộc (21/04)**

📌 **Tasks chưa hoàn thành (2):**
- [ ] Chuẩn bị bảng so sánh 3 PA (due: 20/04) 🟠
- [ ] Test tích hợp camera với hệ thống HIK (due: 20/04) 🔴

⏱ **Còn 1 ngày nữa!**
```

---

## 🛠️ Commands (Khi triển khai)

```bash
# Task Management Commands
task list                    # Liệt kê tasks theo filter
task add "title" --due 2025-04-20 --priority high --meeting MTG-001
task show TASK-001           # Chi tiết task
task update TASK-001 --status in_progress
task assign TASK-001 --to "Dương Quang Trường"
task check TASK-001 --add "Hoàn thành báo giá"
task overdue                 # Hiển thị tasks quá hạn
task today                  # Tasks cần làm hôm nay
task meeting-prep MTG-001   # Xem tasks cho cuộc họp
```

---

## 🔄 Integration với Meeting

Khi tạo meeting file (`meetings/YYYY-MM-DD_MeetingName.md`):
1. **Tự động sinh** các task prepare dựa trên template
2. **Link ngược** từ task về meeting
3. **Khi meeting diễn ra** → Đánh dấu tasks liên quan là `done` hoặc `review`

---

## 📈 Metrics & Insights

- **Task Completion Rate** (%)
- **Average Time to Complete** (hours/days)
- **Blocked Time** (thời gian task bị block)
- **Assignee workload** (số task/người)
- **Meeting Prep Score** (% tasks hoàn thành trước meeting)

---

## 🚀 Triển khai giai đoạn

### Phase 1 (Ngay): Manual với Markdown
- Tạo file `tasks/active/TASK-YYYYMMDD-NNN.md` cho mỗi task
- Dùng frontmatter YAML để metadata
- Search qua `memory_search` để tìm task

### Phase 2 (Tuần sau): Script automation
- Tạo script `task.sh` để quản lý (list, add, update)
- Tích hợp với heartbeat để nhắc việc
- Report tự động hàng ngày

### Phase 3 (Tháng sau): TaskFlow integration
- Dùng skill `taskflow` để quản lý workflow
- Tích hợp với calendar
- Dashboard web đơn giản

---

## 💡 Benefits

1. **Không bao giờ quên** công việc quan trọng
2. **Biết rõ** cần làm gì trước mỗi cuộc họp
3. **Theo dõi tiến độ** rõ ràng
4. **Phân công** trách nhiệm rõ ràng
5. **Báo cáo** tự động, tiết kiệm thời gian
6. **Lưu trữ** knowledge base cho các meeting type

---

**Đây là proposal hệ thống. Anh Bình muốn mình triển khai theo hướng nào, hay có ý tưởng chỉnh sửa gì không ạ?** 🚀
