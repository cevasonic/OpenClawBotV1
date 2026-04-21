---
# Shared Context Across Platforms - Hệ Thống Ngữ Cảnh Xuyên Nền Tảng (v2)

## 🎯 Mục Tiêu
Xây dựng hệ thống cho phép assistant hiểu và nhớ ngữ cảnh cuộc trò chuyện **xuyên suốt giữa nhiều nền tảng** (Zalo, Telegram, Discord...), mà không cần config gateway phức tạp.

**Vấn đề hiện tại:**
- Mỗi channel có session riêng → context riêng
- Chat trên Zalo xong, sang Telegram không biết đang nói về gì
- Cần một "bộ nhớ chung" mà tất cả channel đều access được

**Giải pháp:**
- Dùng **shared memory files** (đã có sẵn trong OpenClaw)
- Kết hợp **rule-based extraction** (real-time) + **Light LLM Fallback**
- Tạo knowledge base có cấu trúc, dễ query

---

## 📋 Yêu Cầu Chức Năng

- ✅ Context sharing giữa Zalo và Telegram (và các channel khác)
- ✅ Realtime: Agent luôn biết context từ các chat khác
- ~~✅ Daily: Tóm tắt thông minh cuối ngày~~ → **Không cần** (xem ghi chú bên dưới)
- ✅ Không treo máy (không dùng ByteRover)
- ✅ Không cần config gateway phức tạp
- ✅ Dễ maintain, dễ extend
- ✅ Query được: "Mình đã nói gì về X?"

> **📝 Ghi chú — Tại sao bỏ Daily Summary:**
> Daily Summary chỉ có giá trị khi lượng data quá lớn để inject thẳng vào prompt (thường là vài nghìn entries/ngày hoặc cần nhớ ngữ cảnh từ nhiều tuần trước).
>
> Trong hệ thống này:
> - Context chỉ cần giữ trong **1-2 ngày**
> - Lượng chat ước tính **100-200 entries/ngày** — mỗi entry ~200-400 token, nhưng thực tế chỉ inject 10-15 entries liên quan nhờ fuzzy search (Component 4)
> - → Raw JSONL + fuzzy retrieval là **đủ**, không cần thêm lớp summarize
>
> Hệ quả: Bỏ luôn cron job, `conversation-summary.md`, human-in-the-loop flow, và `proposed-updates.yaml`. Knowledge Base được update trực tiếp từ rule-based extraction thay vì qua bước summarize.
> Nếu sau này lượng chat tăng đột biến hoặc cần nhớ context dài hơn 2 ngày, có thể bổ sung lại.

---

## 🏗️ Thiết Kế

### **Kiến Trúc Tổng Quát**

```
┌─────────────────────────────────────────────────────────────┐
│ OpenClaw Sessions │
│ Zalo Session Telegram Session Other Session │
│ │ │ │ │
│ └──────────────┬────────────────────────────┘ │
│ ▼ │
│ ┌─────────────────────┐ │
│ │ Memory Manager │ ← Central Knowledge Store │
│ │ (Node.js/TS Plugin)│ (Shared) │
│ └─────────────────────┘ │
│ │ │
│ ┌────────┴────────┐ │
│ ▼ ▼ │
│ memory/ knowledge/ │
│ YYYY-MM-DD.jsonl {preferences, │
│ (raw structured) events, tasks} │
└─────────────────────────────────────────────────────────────┘
```

---

### **Component 1: Structured Memory Logger (JSONL + Atomic Write)**

**File:** `memory/YYYY-MM-DD.jsonl` (Dùng JSONL để dễ append, tránh conflict khi chat song song, parse nhanh). Tích hợp cơ chế Queue/Lock (ví dụ: `proper-lockfile` hoặc ghi nguyên tử) để xử lý Race Condition.

**Batch append:** Queue không flush từng entry một mà gom theo batch (mỗi 500ms hoặc khi đủ 10 entries) rồi ghi một lần — giảm số lần I/O đáng kể khi nhiều channel active đồng thời.

**Startup recovery:** Khi process khởi động lại, scan file JSONL gần nhất, parse từng dòng trong `try-catch`. Dòng nào không parse được (JSON lỗi do crash giữa chừng) → bỏ qua và log warning, không làm crash toàn bộ load.

**Format (JSONL line):**
```json
{"id": "001", "timestamp": "2025-06-17T14:30:00Z", "channel": "zalo", "thread_id": "zalo_123", "user_id": "user_1", "user_input": "Mình thích phở", "assistant_response": "Phở là món ăn...", "extracted": {"type": "preference", "category": "food", "entity": "phở", "sentiment": "positive", "confidence": 0.9, "importance": 0.8}, "version": "1.0"}
```

**Rules extraction (rule-based mở rộng + Sentiment):**
```javascript
const RULES = {
 preference: {
 patterns: [/thích (.+)/i, /yêu (.+)/i, /muốn (.+)/i, /mê (.+)/i, /ghiền (.+)/i, /ghét (.+)/i],
 extract: "item"
 },
 schedule: {
 patterns: [/(.+) họp/i, /(.+) gặp/i, /(.+) lúc (\d+.+)/i],
 extract: "event_time"
 },
 task: {
 patterns: [/cần (.+)/i, /phải (.+)/i, /sẽ (.+)/i, /nhắc mình (.+)/i, /chốt (.+)/i],
 extract: "action"
 }
};

// Fallback: Nếu rule-based không bắt được gì quan trọng, dùng Light LLM (như gemini-flash)
// với prompt cực ngắn để extract.
//
// NGƯỠNG TRIGGER FALLBACK (cụ thể):
// - Tin nhắn dài hơn 100 ký tự, VÀ
// - Có chứa ít nhất một trong các keyword nghi ngờ: "ngon", "tệ", "tuyệt", "nhớ", "đừng",
// "quan trọng", "chú ý", "deadline", "hẹn", "xong", "cancel"
// - Không match bất kỳ rule nào ở trên
//
// LÝ DO chọn 100 ký tự: Tin nhắn ngắn hơn thường là small talk, ít mang thông tin cần extract.
// Dưới ngưỡng này, chi phí LLM call không xứng đáng.
//
// TRÁNH LẠM DỤNG: Fallback chỉ chiếm ~10-15% tổng lượng tin nhắn. Nếu vượt quá, cần review lại rules.
// MONITORING: Log số lần fallback mỗi ngày (vd: vào system log). Nếu tỷ lệ >20%, đó là tín hiệu
// cần mở rộng RULES thay vì tiếp tục dựa vào LLM fallback.
```

---

### ~~**Component 2: Daily AI Summarizer**~~ — Đã loại bỏ

> **Lý do bỏ:** Context chỉ cần 1-2 ngày, lượng chat ~100-200 entries/ngày. Fuzzy search trong Component 4 đã đủ để retrieve đúng context mà không cần nén qua bước summarize. Bỏ component này giúp tiết kiệm ~3h và loại bỏ hoàn toàn dependency vào cron job + LLM summarize call.
>
> **Kéo theo bỏ:** cron job `0 12,23 * * *`, file `conversation-summary.md`, `proposed-updates.yaml`, và toàn bộ human-in-the-loop review flow.

---

### **Component 2 (mới): Knowledge Base Direct Update**

Thay vì update Knowledge Base qua bước summarize, các entries được extract trực tiếp từ rule-based logger (Component 1) và ghi vào `knowledge/` ngay lập tức khi có đủ confidence.

**Điều kiện ghi vào Knowledge Base:**
- `confidence >= 0.85` → ghi trực tiếp, không cần xác nhận
- `0.7 <= confidence < 0.85` → ghi với flag `status: pending`, chờ entry tương tự xuất hiện lần 2 để confirm
- `confidence < 0.7` → chỉ giữ trong JSONL, không promote lên Knowledge Base

---

### **Component 3: Central Knowledge Base (Bắt buộc & Tự động)**

**Thư mục:** `knowledge/`

**Files:** `preferences.yaml`, `events.yaml`, `tasks.yaml`

**Cải tiến:**
- Cập nhật trực tiếp từ rule-based extraction (không qua summarize).
- Mỗi entry cần có `confidence` score và `source` rõ ràng (kèm channel và ID) để dễ debug.

---

### **Component 4: Context Injector (Retrieval-Augmented)**

**Cải tiến lớn để tránh quên context:**
- Bổ sung `queryKnowledgeBase(message)`: Dùng fuzzy search (như `fuse.js`) hoặc keyword matching để quét các file `knowledge/*.yaml`. Không cần quét `memory/` cũ vì context chỉ giữ 1-2 ngày — Knowledge Base đã là nơi tổng hợp thông tin quan trọng từ JSONL.
- Sử dụng `importance score` (0.0-1.0) kết hợp với **Time Decay** để ưu tiên context theo độ tươi của dữ liệu.

**Công thức Time Decay:**
```
adjusted_score = importance * e^(-λ * days_old)
```
Trong đó:
- `importance`: Score gốc (0.0-1.0) được gán khi extract
- `days_old`: Số ngày kể từ khi entry được tạo
- `λ` (lambda): Tham số decay, khuyến nghị bắt đầu với `λ = 0.1` (tương đương entry quan trọng 1.0 sau 7 ngày còn ~0.5). Có thể tuning theo thực tế.

Ví dụ với `λ = 0.1`:
| days_old | importance gốc | adjusted_score |
|----------|----------------|----------------|
| 0 | 0.9 | 0.90 |
| 3 | 0.9 | 0.67 |
| 7 | 0.9 | 0.45 |
| 7 | 0.8 (high) | 0.40 → bị drop |

Các entry cũ quá 7 ngày mà `adjusted_score < 0.4` sẽ bị drop khỏi context. Ngưỡng này có thể config.

- Nhóm ngữ cảnh theo `thread_id` hoặc `channel`. Khi retrieve, **ưu tiên entries từ cùng channel/thread** trước, sau đó mới lấy cross-platform — giúp context tự nhiên hơn và tránh nhiễu.
- **Giới hạn token:** Tổng context inject (recent + relevantKnowledge) phải `< 2500 token`. Nếu vượt, cắt bớt entries có `adjusted_score` thấp nhất trước. Không để prompt phình to làm chậm response và tốn chi phí LLM.

```javascript
async function processMessage(channel, message) {
 // 1. Load recent raw entries (1-2 ngày gần nhất, lọc theo importance score)
 // Không cần load summary — raw entries đã đủ nhỏ (~100-200 entries/ngày)
 const recent = await loadRecentEntries(limit=15, minImportance=0.5, maxDays=2);

 // 2. Relevant Retrieval: Truy vấn knowledge base dựa trên keyword của tin nhắn
 const relevantKnowledge = await queryKnowledgeBase(message); // Fuzzy search

 // 3. Build context
 const context = `
 INSTRUCTION: Chỉ dùng thông tin được cung cấp trong context bên dưới.
 Không tự bịa ra thông tin không có trong context.
 Nếu không tìm thấy thông tin liên quan, hãy nói rõ: "Mình không có thông tin về điều này."

 Relevant Knowledge (Từ quá khứ):
 ${relevantKnowledge}

 Recent conversation (all platforms, last 1-2 days):
 ${formatRecent(recent)}

 Current message (from ${channel}):
 ${message}
 `;

 // 4. Generate response
 const response = await llmGenerate(context);

 // 5. Log interaction (Queue + JSONL)
 await logInteractionToQueue(channel, message, response);

 return response;
}
```

---

## 🛠️ Tech Stack & Error Handling

- **Language:** Node.js / TypeScript (Native OpenClaw plugin)
- **Storage:** JSONL (cho Raw logs - append only) + YAML (cho Knowledge Base).
- **Concurrency:** Queue in-memory với batch append (flush mỗi 500ms hoặc 10 entries) + lock file để ngăn race condition khi nhiều channel ghi đồng thời.
- **Retrieval:** Fuzzy search (`fuse.js`) hoặc keyword index cơ bản.
- **Error Handling:**
 - Đặt `try-catch` toàn bộ block đọc/ghi.
 - **Outer try-catch cho `processMessage`:** Nếu memory layer fail (không đọc được JSONL, KB lỗi...), hệ thống vẫn phải trả về response — chỉ là không có context inject. Không để lỗi memory làm crash toàn bộ flow chat.
 ```javascript
 try {
 // load context, build prompt, generate...
 } catch (memoryError) {
 log.warn('Memory layer failed, responding without context', memoryError);
 return await llmGenerate(`Current message: ${message}`); // fallback không context
 }
 ```
 - Log error vào system log của OpenClaw.
 - Gắn schema version (vd: `version: "1.0"`) vào từng record/file để dễ migrate.

**Xử lý Lock / Deadlock:**
- Dùng `proper-lockfile` với option `{ retries: 5, retryWait: 200ms, stale: 10000 }` — lock tồn tại quá **10 giây** (stale) được coi là chết và tự động bị xóa. Đây là tình huống xảy ra khi process crash giữa chừng.
- Nếu vẫn không acquire được lock sau 5 lần retry: log warning, bỏ qua write lần này, **không throw exception** để tránh làm crash toàn bộ flow.
- Queue in-memory: Giới hạn tối đa **500 entries** đang chờ. Nếu vượt ngưỡng, drop entry cũ nhất và log cảnh báo để biết hệ thống đang bị quá tải.

---

## 📦 Scalability & CLI Tools

> **Ưu tiên:** Phần này là **dài hạn (sau v2)**, chưa nằm trong scope triển khai hiện tại. Xem chi tiết ở doc riêng nếu cần.

- **Auto-archive:** Kịch bản chạy hàng tháng chuyển `YYYY-MM-DD.jsonl` cũ vào thư mục `archive/YYYY-MM/`.
- **CLI Utilities:** Bổ cả các lệnh quản lý (Ví dụ: `openclaw memory validate`, `openclaw memory query "phở"`).

---

## 🔐 Privacy & Security

- **Encryption at rest:** Các file `*.jsonl` và `*.yaml` được mã hóa bằng **AES-256-GCM** qua module `crypto` native của Node.js. Key lưu trong biến môi trường (`OPENCLAW_MEMORY_KEY`), không hardcode trong source.

 **Quan trọng — IV per line:** Không encrypt cả file một lần (không append-friendly và dễ reuse IV). Thay vào đó, **encrypt từng JSON line riêng biệt**, lưu dạng `iv:authTag:ciphertext` trên mỗi dòng:
 ```
 a3f1...:9c2b...:4d7e... ← line 1 (mỗi field là hex, IV 12 bytes random)
 b8e2...:1a4f...:7c3d... ← line 2
 ```
 IV random 12 bytes mỗi lần encrypt (không reuse — reuse IV với GCM là lỗi bảo mật nghiêm trọng). Khi đọc, decrypt per-line, cache các entries gần đây trong memory với TTL ngắn (~60s) để tránh decrypt lặp lại.
- **Quyền đọc file:** Giới hạn permission `chmod 600` — chỉ user root và OpenClaw runtime mới đọc được.
- **Right to delete:** Khi user yêu cầu "Xóa tin nhắn", hệ thống phải cung cấp cơ chế tìm kiếm và xóa entry tương ứng theo `id` hoặc `timestamp` trong `YYYY-MM-DD.jsonl` và các file `knowledge/`. Cần rebuild lại file sau khi xóa (JSONL không hỗ trợ delete in-place).
- **Multi-user:** Việc thêm `user_id` vào mỗi entry mở đường cho việc phân chia context theo từng người dùng trong tương lai.

---

## 📅 Timeline Ước Tính

| Phase | Nội Dung | Thời Gian |
|-------|----------|-----------|
| 1 | Schema (JSONL, Knowledge) & Queue/Lock + Batch append + Startup recovery | 2.5h |
| 2 | Code Logger (Advanced rules + Sentiment + Queue + Direct KB update + Fallback monitoring) | 3h |
| 3 | Code Context Retriever (Fuzzy search + Time Decay + Token cap + Channel priority) | 3h |
| 4 | Integrate vào Assistant (Context Injector + Prompting nâng cấp) | 2h |
| 5 | Encryption per-line (AES-256-GCM IV per line + decrypt cache) | 1.5h |
| 6 | Test thực tế đa nền tảng, fix race condition, tuning rules | 4-5h |
| **Total** | | **~16-17h** |

> Phase 7 (CLI Tools, Auto-archive, migration path nếu scale) dự kiến **~5-6h**, thuộc scope v3 — chưa tính vào tổng trên.