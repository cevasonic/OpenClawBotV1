# Zalo Channel - Authentication & Pairing

> **Ngày cập nhật:** 2026-04-24  
> **Tình huống:** Session Zalo hết hạn nhưng vẫn nhắn tin được qua Control UI

---

## 📋 Tổng quan

OpenClaw Zalo channel có **2 cơ chế xác thực riêng biệt**:

| Mechanism | Mục đích | File | Status khi expired |
|-----------|----------|------|-------------------|
| **Authentication** (Zalo Login) | Đăng nhập vào Zalo app/API | `credentials/zalouser/credentials.json` | ❌ Không gửi/nhận được tin nhắn từ Zalo app |
| **Pairing** (Device Linking) | Liên kết device với OpenClaw | `devices/paired.json` | ✅ Vẫn điều khiển bot qua Control UI/CLI |

---

## 🔄 Cơ chế chi tiết

### 1. **Zalo Authentication (credentials.json)**

**Làm gì:** Lưu trữ cookies và session token để đăng nhập vào Zalo API.

**File:** `/opt/openclaw/.openclaw/credentials/zalouser/credentials.json`

**Trạng thái:**
```json
{
  "cookie": [...],
  "lastUsedAt": "2026-04-24T08:05:38.722Z",
  "zlogtype": "EXPIRED"  // ← Session đã hết hạn
}
```

**Ảnh hưởng khi expired:**
- ❌ **Không đọc được tin nhắn** từ Zalo app (điện thoại)
- ❌ **Không gửi được tin nhắn** qua Zalo API (số điện thoại)
- ⚠️ Channel hiển thị `Not authenticated` trong `openclaw status`

---

### 2. **Device Pairing (paired.json)**

**Làm gì:** Xác thực device (Control UI, CLI, gateway) để điều khiển bot.

**File:** `/opt/openclaw/.openclaw/devices/paired.json`

**Cấu trúc:**
```json
{
  "DEVICE_ID": {
    "deviceId": "...",
    "platform": "linux/mac/win32",
    "clientMode": "cli/webchat/backend",
    "role": "operator",
    "tokens": {
      "operator": {
        "token": "OPERATOR_TOKEN",
        "scopes": ["operator.admin", "operator.read", ...]
      }
    }
  }
}
```

**Ảnh hưởng khi active:**
- ✅ **Vẫn nhắn tin được** qua Control UI (web chat)
- ✅ **Vẫn điều khiển bot** qua CLI
- ✅ **Gateway/client** vẫn hoạt động

---

## 🤔 Tại sao vẫn chat được?

**Scenario thực tế:**

```
User (Anh Bình) 
    ↓ Gửi tin nhắn qua Zalo Personal (Zalo Web/App)
    
OpenClaw Gateway 
    ↓ Nhận tin nhắn
    ↓ Kiểm tra dmPolicy: "pairing"
    ↓ Kiểm tra device token từ Control UI session
    ↓ ✓ Đã pair → Chấp nhận
    ↓ Xử lý tin nhắn → Bot trả lời
```

**Điểm then chốt:**
- Tin nhắn đi qua **OpenClaw Gateway**, không phải trực tiếp Zalo API
- Gateway đã **pair với device** nên có operator token
- `dmPolicy: "pairing"` chỉ check **device pairing**, không check **Zalo auth**

---

## ⚠️ Cảnh báo & Giới hạn

### **Zalo Authentication expired leads to:**

1. **Tin nhắn từ Zalo app (điện thoại) sẽ KHÔNG đọc được**
   - Bot không thấy tin nhắn mới từ Zalo app
   - Bot không gửi được tin nhắn về số điện thoại

2. **Channel state:** `Not authenticated` trong status
   - Đây là **cảnh báo bình thường** khi session hết hạn
   - Không ảnh hưởng đến Control UI/CLI

3. **Tương lai:** Zalo có thể logout hoàn toàn → cần re-login

---

## 🔧 Cách khắc phục

### **Re-authenticate Zalo (nếu cần dùng Zalo app):**

```bash
# Trigger Zalo login flow (quét QR từ điện thoại)
openclaw plugins zalouser auth
```

**Lưu ý:** Chỉ cần làm khi thực sự cần Zalo app. Nếu chỉ dùng Control UI/CLI, không cần thiết.

---

## 📊 Config đã áp dụng

```json
{
  "channels": {
    "zalouser": {
      "enabled": true,
      "dmPolicy": "pairing"  // ← Chỉ cho phép device đã pair
    }
  }
}
```

**Hiệu quả:**
- ✅ Người lạ không thể nhắn tin (cần pairing)
- ✅ Device đã pair vẫn hoạt động (qua Control UI)
- ✅ Zalo app không làm ảnh hưởng đến Control UI

---

## 🎯 Best Practice

1. ** pairing luôn giữ** → Dùng Control UI/CLI chính
2. **Zalo auth chỉ cần khi** → Muốn tích hợp với Zalo app/điện thoại
3. **Giám sát `lastUsedAt`** trong credentials → Biết khi nào cần re-login
4. **Backup paired.json** → Để khôi phục device tokens nếu cần

---

## 📝 Log tham khảo

**File đã đọc:**
- `/opt/openclaw/.openclaw/credentials/zalouser/credentials.json` — Zalo cookies (expired)
- `/opt/openclaw/.openclaw/devices/paired.json` — Device pairing (active)
- `/opt/openclaw/.openclaw/openclaw.json` — Config với `dmPolicy: "pairing"`

**Thời gian phân tích:** 2026-04-24 15:09 ICT

---

## 🔗 Related

- OpenClaw docs: https://docs.openclaw.ai
- Security audit: `openclaw security audit`
- Update config: `openclaw config edit`
