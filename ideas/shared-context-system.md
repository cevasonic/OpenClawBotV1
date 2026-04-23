# Shared Context Across Platforms - Hệ Thống Ngữ Cảnh Xuyên Nền Tảng (v2)

## 🎯 Mục Tiêu
Xây dựng hệ thống cho phép assistant hiểu và nhớ ngữ cảnh cuộc trò chuyện **xuyên suốt giữa nhiều nền tảng** (Zalo, Telegram, Discord...).

## 📋 Yêu Cầu Chức Năng
- ✅ Context sharing đa nền tảng (Real-time).
- ✅ Không treo máy, không config gateway phức tạp.
- ✅ Dễ maintain, dễ extend, có khả năng Query.
- ❌ **Đã bỏ Daily Summary vì:** 
  - Context chỉ cần giữ 1-2 ngày.
  - Lượng chat nhỏ (~100-200 entries/ngày).
  - Dùng raw JSONL + fuzzy retrieval là đủ, tối ưu chi phí LLM, loại bỏ phụ thuộc vào cron job.

---

## 🏗️ Thiết Kế Tổng Quát

```
┌─────────────────────────────────────────────────────────────┐
│                     OpenClaw Sessions                      │
│  Zalo Session        Telegram Session      Other Session   │
│       │                      │                    │        │
│       └──────────────┬────────────────────────────┘        │
│                      ▼ Hook/Middleware                     │
├─────────────────────────────────────────────────────────────┤
│ 📦 MODULE: skills/shared-context/                          │
│                                                             │
│      ┌───────────────────────────────────────┐              │
│      │         src/ (Core Logic)             │              │
│      │  - logger.js, retriever.js, ...       │              │
│      └───────────────────┬───────────────────┘              │
│                          │                                  │
│            ┌─────────────┴─────────────┐                    │
│            ▼                           ▼                    │
│      data/memory/                data/knowledge/            │
│    YYYY-MM-DD.jsonl        {preferences, events, tasks}     │
│    (Raw JSONL logs)           (Structured YAML)             │
└─────────────────────────────────────────────────────────────┘
```

---

### **Component 1: Structured Memory Logger (JSONL + Atomic Write)**

**File:** `shared-context/data/memory/YYYY-MM-DD.jsonl`
- **Schema JSONL Entry:** Mỗi dòng trong file JSONL là một JSON object theo cấu trúc sau:
  ```json
  {
    "id": "uuid-v4",
    "timestamp": "2024-01-15T14:30:00.000Z",
    "platform": "zalo" | "telegram" | "discord",
    "thread_id": "zalo_self" | "tg_123456789",
    "role": "user" | "assistant",
    "content": "Nội dung tin nhắn gốc",
    "type": "chat" | "preference" | "schedule" | "task" | "topic_reset",
    "extracted": { ... },
    "confidence": 0.92,
    "method": "rule" | "llm"
  }
  ```
  *Lưu ý: Entry thuần chat (không match rule nào) vẫn được ghi với type: "chat", extracted: null, confidence: null. Đây là log thô phục vụ fuzzy search.*

- **Cơ chế:** Batch append (gom 10 entries hoặc 500ms flush 1 lần) + Lock file để chống Race Condition. Startup recovery bỏ qua dòng lỗi.
- **Rules extraction (Rule-based + LLM Fallback):**
  ```javascript
  const RULES = {
    preference: { patterns: [/thích/, /yêu/, /muốn/, /ghét/], extract: "item" },
    schedule: { patterns: [/họp/, /gặp/, /lúc/], extract: "event_time" },
    task: { patterns: [/cần/, /phải/, /nhắc/], extract: "action" },
    topic_reset: { patterns: [/chuyện khác/, /bỏ qua đi/, /chủ đề mới/, /thôi/], extract: "reset_flag" } // Phát hiện chuyển chủ đề
  };

  // Fallback LLM: Chỉ trigger khi tin nhắn > 100 ký tự VÀ có keyword nghi ngờ nhưng không match rule.
  const LLM_FALLBACK_PROMPT = `
    Phân tích tin nhắn sau và trả về JSON duy nhất, không thêm text nào khác.
    Tin nhắn: "{message}"
    Trả về: { "type": "preference" | "schedule" | "task" | "chat", "extracted": { ... }, "confidence": 0.0-1.0 }
  `;
  // Timeout: 3000ms. Nếu timeout hoặc lỗi parse JSON → fallback type = "chat".
  // Retry: 1 lần duy nhất sau 1000ms.
  // Chi phí ước tính: ~0.001 USD/call, trigger ~5-10% tổng entries.
  ```

---

### **Component 2: Knowledge Base Direct Update**

Extract trực tiếp từ Component 1 vào `shared-context/data/knowledge/` (`preferences.yaml`, `events.yaml`, `tasks.yaml`).
- **Schema Knowledge Base:**
  - `preferences.yaml`: Gồm id, item, sentiment (like/dislike/want/neutral), source_entry_id, status (confirmed/pending).
  - `events.yaml`: Gồm id, description, event_time, source_entry_id, status.
  - `tasks.yaml`: Gồm id, action, source_entry_id, status.

- **Confidence Threshold & Pending Confirmation:**
  - `confidence >= 0.85`: Ghi trực tiếp với `status: confirmed`.
  - `0.7 <= confidence < 0.85`: Ghi nhận `status: pending`. Confirm khi xuất hiện entry thứ 2 có content tương tự (Fuzzy similarity > 0.8) trong vòng 24h.
  - `confidence < 0.7`: Chỉ giữ trong JSONL làm log, không ghi vào KB.

---

### **Component 3: Context Injector (Retrieval-Augmented)**

**Đây là phần cốt lõi được tối ưu Token & Logic:**

**Định Nghĩa thread_id**
`thread_id` là định danh duy nhất cho một luồng hội thoại, được tạo theo quy tắc:
```javascript
const THREAD_ID_MAP = {
  zalo: () => `zalo_self`, // Single-user, 1 thread duy nhất
  telegram: (chatId) => `tg_${chatId}`, // Mỗi chat/group là 1 thread
  discord: (channelId) => `dc_${channelId}` // Mỗi channel là 1 thread
};
```

- **Truy vấn & Time Decay:** Fuzzy search (`fuse.js`). Ưu tiên tuyệt đối các entries MỚI NHẤT trên toàn bộ nền tảng (Time Decay: `adjusted_score = importance * e^(-λ * days_old)`). Entry cũ quá 7 ngày (`score < 0.4`) sẽ bị drop.
- **Token Optimization & Conditional Injection:**
  - **Giảm trần Token:** `MAX_TOTAL_CONTEXT_TOKENS = 1500` (giảm từ 2500 để tiết kiệm chi phí).
  - **Xử lý "Chủ đề mới":** Nếu phát hiện rule `topic_reset` từ Component 1, hệ thống chủ động bỏ qua context cũ, truyền prompt sạch để LLM tư duy luồng mới.
  - **Short Format:** Context inject được parse thành dạng cực ngắn (VD: `[14:30 Zalo] User: ... -> Bot: ...`) để giảm nhiễu.
  - **Caching:** Cache kết quả retrieval theo `thread_id` (TTL ~5 phút) để tránh search lại với các tin nhắn liên tiếp trong cùng 1 topic.

  ```javascript
  async function processMessage(channel, message, isNewTopic) {
      if (isNewTopic) {
          return await llmGenerate(message); // Conditional Injection: Bypass context
      }

      const cachedContext = await getThreadCache(thread_id);
      const context = cachedContext || await buildShortFormatContext(limit=1500_tokens);
      
      // Inject & Generate...
  }
  ```

---

### **Tech Stack & Error Handling**

- **Language & Storage:** Node.js / JSONL (Append) + YAML (Knowledge).
- **Error Handling:** Outer `try-catch` bảo vệ luồng chat. Nếu Memory Layer sập, fallback trả lời không context. Dùng `proper-lockfile` (stale 10s) chống Deadlock.
- **Token Optimization Strategy:** Áp dụng chặt chẽ Limit 1500 tokens + Conditional Injection (Topic Reset) + Short Format Logs để tối ưu hóa triệt để độ phình của Prompt.

---

### **Privacy & Security**

- **Encryption (Per-line):** Mã hóa `AES-256-GCM`. Thay vì file-level (dễ lỗi khi append), mã hóa từng dòng JSONL với IV random 12 bytes (`iv:authTag:ciphertext`). Có Decrypt cache (TTL 60s).
- **Phân quyền:** `chmod 600`. Hỗ trợ xóa theo `id` (Right to delete).

---

### **📅 Timeline Ước Tính (Đã tối ưu)**

| Phase | Nội Dung | Thời Gian |
|-------|----------|-----------|
| 1 | Schema (JSONL/KB), Queue/Lock, Batch append, Logger (Rules + Topic Reset) | 5.5h |
| 2 | Context Retriever (Fuzzy, Time Decay, Token Cap 1500, Conditional Injection) | 5h |
| 3 | Encryption per-line (AES-256-GCM), Test thực tế đa nền tảng, Tuning | 5.5h |
| **Tổng** | | **~16h** |

*(Lưu ý: CLI Tools & Auto-archive là scope của v3 (dài hạn), không ưu tiên trong giai đoạn này).*