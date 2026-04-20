# Notion Database Schemas

## 📅 Database: Meetings

**Purpose:** Track all meetings and events

**Properties:**
```json
{
  "Name": {"title": {}},
  "Date": {"date": {}},
  "Status": {
    "select": {
      "options": [
        {"name": "Planned", "color": "blue"},
        {"name": "In Progress", "color": "yellow"},
        {"name": "Done", "color": "green"},
        {"name": "Cancelled", "color": "red"}
      ]
    }
  },
  "Type": {
    "select": {
      "options": [
        {"name": "Internal", "color": "purple"},
        {"name": "Client", "color": "blue"},
        {"name": "Vendor", "color": "orange"},
        {"name": "Government", "color": "red"}
      ]
    }
  },
  "Partners": {"multi_select": {
    "options": [
      {"name": "UBND xã", "color": "blue"},
      {"name": "VNPT", "color": "red"},
      {"name": "Khách hàng", "color": "green"},
      {"name": "Nhà cung cấp", "color": "orange"}
    ]
  }},
  "Location": {"rich_text": {}},
  "Description": {"rich_text": {}},
  "Tasks": {"relation": {"database_id": "[TASKS_DATABASE_ID]"}},
  "Notes": {"relation": {"database_id": "[NOTES_DATABASE_ID]"}},
  "Created By": {"people": {}},
  "Last Updated": {"last_edited_time": {}}
}
```

**Sample Page Template:**
```
Name: Cuộc họp VNPT - UBND xã Cần Giuộc
Date: 2026-04-21
Status: Planned
Type: Government
Partners: UBND xã, VNPT
Location: UBND xã Cần Giuộc, Long An
Description: Trình bày phương án camera giám sát...
```

---

## ✅ Database: Tasks

**Purpose:** Manage all tasks with full tracking

**Properties:**
```json
{
  "Name": {"title": {}},
  "Status": {
    "select": {
      "options": [
        {"name": "Todo", "color": "red"},
        {"name": "In Progress", "color": "yellow"},
        {"name": "Review", "color": "blue"},
        {"name": "Done", "color": "green"},
        {"name": "Blocked", "color": "gray"}
      ]
    }
  },
  "Priority": {
    "select": {
      "options": [
        {"name": "Low", "color": "blue"},
        {"name": "Medium", "color": "yellow"},
        {"name": "High", "color": "orange"},
        {"name": "Critical", "color": "red"}
      ]
    }
  },
  "Assignee": {"people": {}},
  "Due Date": {"date": {}},
  "Meeting": {"relation": {"database_id": "[MEETINGS_DATABASE_ID]"}},
  "Parent Task": {"relation": {"database_id": "[TASKS_DATABASE_ID]"}},
  "Sub-tasks": {"relation": {"database_id": "[TASKS_DATABASE_ID]"}},
  "Description": {"rich_text": {}},
  "Checklist": {"to_do": {}},  // Notion built-in
  "Tags": {"multi_select": {
    "options": [
      {"name": "pre-meeting", "color": "purple"},
      {"name": "follow-up", "color": "blue"},
      {"name": "research", "color": "green"},
      {"name": "documentation", "color": "yellow"},
      {"name": "bug", "color": "red"}
    ]
  }},
  "Estimated Hours": {"number": {}},
  "Actual Hours": {"number": {}},
  "Blocker": {"rich_text": {}},
  "Created": {"created_time": {}},
  "Completed": {"last_edited_time": {}}
}
```

**Task Template (from Meeting):**
```
Name: Chuẩn bị 3 phương án giá cho cuộc họp VNPT
Status: Todo
Priority: High
Assignee: Dương Quang Trường
Due Date: 2026-04-20
Meeting: [Link to meeting page]
Description: So sánh chi phí, ưu nhược điểm 3 PA
Checklist:
  [ ] Lấy báo giá từ nhà cung cấp
  [ ] Tính toán TCO 3 năm
  [ ] Lập bảng so sánh
Tags: pre-meeting, VNPT
```

---

## 📝 Database: Notes

**Purpose:** Store meeting notes, decisions, research

**Properties:**
```json
{
  "Title": {"title": {}},
  "Content": {"rich_text": {}},  // Or use blocks for rich content
  "Meeting": {"relation": {"database_id": "[MEETINGS_DATABASE_ID]"}},
  "Tasks": {"relation": {"database_id": "[TASKS_DATABASE_ID]"}},
  "Tags": {"multi_select": {
    "options": [
      {"name": "meeting-note", "color": "blue"},
      {"name": "decision", "color": "green"},
      {"name": "research", "color": "purple"},
      {"name": "reference", "color": "yellow"}
    ]
  }},
  "Category": {
    "select": {
      "options": [
        {"name": "Meeting Note", "color": "blue"},
        {"name": "Decision", "color": "green"},
        {"name": "Research", "color": "purple"},
        {"name": "Other", "color": "gray"}
      ]
    }
  },
  "Created": {"created_time": {}},
  "Last Modified": {"last_edited_time": {}}
}
```

---

## 🔔 Database: Reminders (Optional)

**Purpose:** Track automated reminders sent

**Properties:**
```json
{
  "Task": {"relation": {"database_id": "[TASKS_DATABASE_ID]"}},
  "Remind Before": {"select": {
    "options": [
      {"name": "1 day", "color": "red"},
      {"name": "3 days", "color": "orange"},
      {"name": "1 week", "color": "yellow"},
      {"name": "custom", "color": "blue"}
    ]
  }},
  "Scheduled For": {"date": {}},
  "Sent At": {"date": {}},
  "Channel": {"select": {"options": [{"name": "Zalo"}, {"name": "Email"}, {"name": "Telegram"}]}},
  "Status": {"select": {"options": [{"name": "Pending"}, {"name": "Sent"}, {"name": "Failed"}]}}
}
```

---

## 🔄 Sync Strategy

### Local ↔ Notion Sync Rules

| Action | Local | Notion |
|--------|-------|--------|
| Create task in Notion | Update | CREATE |
| Update task in Notion | Update | UPDATE |
| Complete task (local) | UPDATE | UPDATE |
| Delete task | Archive | Archive |

### Conflict Resolution
- **Last write wins** (based on `last_edited_time`)
- If conflict detected, prompt user to choose

---

## 📋 Pre-Meeting Template

When creating a meeting, auto-generate these tasks:

```yaml
meeting: "Cuộc họp VNPT - UBND Cần Giuộc"
due_date: "2026-04-21"
tasks:
  - title: "Chuẩn bị 3 phương án giá"
    description: "So sánh chi phí, ưu nhược điểm PA1/PA2/PA3"
    priority: "High"
    due_days_before: 2

  - title: "Chuẩn bị hồ sơ thiết bị"
    description: "Catalog, chứng nhận, xuất xứ camera"
    priority: "Critical"
    due_days_before: 2

  - title: "Test tích hợp hệ thống"
    description: "Đảm bảo camera mới tích hợp với HIK và Công an tỉnh"
    priority: "High"
    due_days_before: 3

  - title: "Chuẩn bị slide trình bày"
    description: "PPT hoặc tài liệu trình bày"
    priority: "Medium"
    due_days_before: 1

  - title: "Xác nhận phòng họp/địa điểm"
    description: "Đặt phòng nếu cần"
    priority: "Low"
    due_days_before: 1
```

---

## 📊 Sample Queries

### Get all tasks due today
```bash
curl -g "https://gateway.maton.ai/notion/v1/data_sources/{tasks_ds_id}/query" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "filter": {
      "property": "Due Date",
      "date": {"equals": "2026-04-19"}
    },
    "sorts": [{"property": "Priority", "direction": "descending"}]
  }'
```

### Get tasks for a meeting
```bash
curl -g "https://gateway.maton.ai/notion/v1/data_sources/{tasks_ds_id}/query" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -d '{
    "filter": {
      "property": "Meeting",
      "relation": {"contains": "MEETING_PAGE_ID"}
    }
  }'
```

### Update task status
```bash
curl -X PATCH "https://gateway.maton.ai/notion/v1/pages/TASK_PAGE_ID" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Status": {"select": {"name": "Done"}}
    }
  }'
```

---

## 🗂️ Suggested Notion Workspace Structure

```
Notion Workspace
├── 📁 Work (Top-level page)
│   ├── 📅 Meetings (Database)
│   │   ├── 2026-04-21 - VNPT Cần Giuộc (Page)
│   │   │   ├── Description
│   │   │   ├── Tasks (linked to Tasks DB)
│   │   │   └── Notes (linked to Notes DB)
│   │   └── ...
│   │
│   ├── ✅ Tasks (Database)
│   │   ├── TASK-001 - Prepare pricing (Page)
│   │   ├── TASK-002 - Device documentation
│   │   └── ...
│   │
│   ├── 📝 Notes (Database)
│   │   ├── Meeting notes - 2026-04-19
│   │   ├── Research - Camera models
│   │   └── ...
│   │
│   └── 🔔 Reminders (Database) [optional]
```

---

**Next:**
1. Run `./scripts/setup-notion.sh` to connect Notion
2. Create databases in Notion manually or via API
3. Update `config/notion_config.json` with database IDs
4. Start creating tasks and meetings!
