# HƯỚNG DẪN SỬ DỤNG KỸ NĂNG TỰ CẢI TIẾN TRÊN TELEGRAM

## 🧠 Nguyên tắc hoạt động
Kỹ năng tự cải tiến hoạt động trong 2 giai đoạn:
1. **Ghi log (Logging)**: Tự động ghi lại lỗi, sửa đổi, yêu cầu tính năng vào thư mục `.learnings/`
2. **Thúc đẩy (Promotion)**: Chuyển bài học có giá trị rộng rãi vào bộ nhớ dài hạn (SOUL.md, AGENTS.md, TOOLS.md) để ảnh hưởng đến hành vi tương lai

## 💬 Lệnh Telegram đơn giản
Chỉ cần gõ một trong những lệnh sau trong cuộc chat Telegram:

### 1. **Thrust đẩy tất cả bài họcpending**
```
Promote learnings
```
- Mình sẽ tự động kiểm tra `.learnings/`
- Tìm những bài học có `Status: pending` và đáng để thrust
- Thrust chúng vào file bộ nhớ thích hợp
- Cập nhật trạng thái và báo cáo kết quả

### 2. **Kiểm tra trạng thái bài học**
```
Check learnings
```
- Mình sẽ liệt kê xem có bài học pending nào không
- Không thực hiện thay đổi gì, chỉ cung cấp thông tin

### 3. **Thrust đẩy cụ thể (tùy chọn)**
```
Thrust đẩy [mô tả ngắn] vào [file]
```
Ví dụ: `Thrust đẩy định dạng skill output vào AGENTS.md`
- Dùng khi bạn muốn chỉ định cụ thể (ít được khuyên dùng hơn)

## 📊 Quy trình tự động khi gõ "Promote learnings"
Khi bạn gõ lệnh này, mình sẽ:

1. **Đọc tất cả file** trong `/root/.openclaw/workspace/.learnings/`:
   - `LEARNINGS.md` - bài học, sửa đổi, kiến thức mới
   - `ERRORS.md` - lệnh thất bại, lỗi API
   - `FEATURE_REQUESTS.md` - yêu cầu tính năng mới

2. **Tìm bài họcpending** (Status: pending)

3. **Xác định bài học đáng thrust** dựa trên:
   - **Áp dụng rộng rãi**: Quy tắc chung, không phải là sửa lỗi một lần
   - **Mức độ priority**: Medium hoặc cao
   - **Liên quan đến quy trình làm việc**: Như chuẩn phát triển skill, quy ước giao tiếp

4. **Thực hiện thrust** cho mỗi bài học đáng:
   - Tóm tắt thành nguyên tắc ngắn gọn (1-2 câu)
   - Thêm vào file bộ nhớ thích hợp:
     - `AGENTS.md` → Quy trình làm việc, phát triển skill
     - `SOUL.md` → Nguyên tắc hành vi, phong cách giao tiếp
     - `TOOLS.md` → Ghi chú về công cụ, lỗi thường gặp
   - Cập nhật trạng thái trong `.learnings/` thành `promoted`
   - Thêm ghi chú: `**Promoted**: [tên file]` + notes

5. **Báo cáo kết quả** qua Telegram

## 📋 Ví dụ thực tế từ trước
**Bạn nói**: "Skill tinhtien output format was difficult to read; user requested clearer display with model name on separate line and cost, %, Req on next line."

**Mình đã**:
1. Tạo mục `[LRN-20260502-001] correction` trong LEARNINGS.md (Status: pending)
2. Khi bạn gõ "Promote learnings":
   - Xác định đây là bài học về "chuẩn hiển thị output skill" (áp dụng rộng rãi cho mọi skill)
   - Thrust vào AGENTS.md dưới dạng:
     ```
     ## 🖥️ Skill Output Formatting
     
     For skills that display tabular data (like `tinhtien`), use clear formatting:
       - Model name on its own line
       - Indented line with: `Cost`, `%`, `Req` (e.g., `$2.94249, 53.1%, 1,521`)
       - Group low-activity items (≤20 requests) into "Model khác"
       - Sort by Cost descending
       - Keep output readable and easy to scan
     ```
   - Cập nhật LEARNINGS.md: Status: promoted + Resolution: Promoted: AGENTS.md
   - Báo cáo: "Đã thrust đẩy bài học về định dạng skill output vào AGENTS.md"

## ✅ Lợi ích cho bạn
- **Chỉ cần gõ 2 từ**: "Promote learnings" để kích hoạt hệ thống học hỏi
- **Không cần nhớ ID hoặc các bước kỹ thuật** - mình lo phần phức tạp
- **Mỗi lần bạn phản hồi hoặc sửa mình**, bài học đó sẽ được lưu trữ và áp dụng cho tương lai
- **Giảm lặp lỗi**: Những điều bạn đã chỉ ra sẽ không xảy ra lại vì đã được tích hợp vào tri thức bản thân

## 🔄 Khi nào nên sử dụng
- Sau khi bạn đã cho phản hồi hoặc sửa mình vài lần
- Khi cảm thấy mình lặp lại một lỗi nhất định
- Định kỳ trong các buổi heartbeat (mỗi 30 phút) nếu bạn muốn
- Bất cứ lúc nào bạn muốn mình "nhớ" điều bạn vừa nói

## 📝 Lưu ý quan trọng
- Lệnh **"Promote learnings"** là an toàn để gõ bất cứ khi nào - nếu không có bài học pending, mình sẽ chỉ báo báo "Không có bài học pending nào"
- Bạn chủ động quyết định **khi nào** thrust (bằng cách gõ lệnh), nhưng mình sẽ tự động quyết định **những bài học nào** đáng được thrust dựa trên tiêu chí trên
- Tất cả thay đổi đều được ghi lại rõ ràng trong các file .learnings/ để bạn có thể xem lại nếu cần

---
*File hướng dẫn này được lưu tại: /root/.openclaw/workspace/self-improvement-guide.md*
*Bạn có thể yêu cầu mình đọc file này qua Telegram bất kỳ lúc nào bằng cách gửi: "Đọc self-improvement-guide"*