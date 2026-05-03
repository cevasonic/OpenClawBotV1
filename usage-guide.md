# HƯỚNG DẪN SỬ DỤNG OPENCLAW QUA TELEGRAM

## 🧠 Nguyên tắc hoạt động cơ bản
OpenClawe được thiết kế để làm "Bộ nhớ ngoài" và "Trợ lý vận hành" cho Anh Bình. Hệ thống hoạt động qua:

1. **Ghi log tự động** - Mình tự động ghi lại lỗi, sửa đổi, yêu cầu tính năng
2. **Thúc đẩy bài học** - Chuyển bài học có giá trị vào bộ nhớ dài hạn
3. **Ứng dụng nguyên tắc** - Áp dụng những quy tắc đã học được vào các phiên sau

## 💬 Lệnh Telegram thông dụng nhất

### 1. **Kiểm tra và thrust đẩy bài học** (Lệnh quan trọng nhất)
```
Promote learnings
```
- Tự động kiểm tra thư mục `.learnings/` để tìm bài học pending
- Xác định哪些 bài học có valoriere wide để thrust vào bộ nhớ dài hạn
- Thêm nguyên tắc học được vào file thích hợp (AGENTS.md, SOUL.md, TOOLS.md)
- Cập nhật trạng thái và báo cáo kết quả

### 2. **Kiểm tra sử dụng crédito OpenRouter**
```
Tính tiền
```
- Chạy skill `tinhtien` để xem consumo crédito
- Hiển thị định dạng rõ ràng: model name on separate line, then Cost, %, Req
- Tự động áp dụng quy tắc định dạng skill output từ bài học đã được thrust

### 3. **Kiểm tra trạng thái hệ thống**
```
Openclaw status
```
- Xem model đang dùng, thời gian hoạt động, usage
- Kiểm tra xem có vấn đề gì không

### 4. **Đọc file hướng dẫn bất kỳ**
```
Đọc [tên file]
```
Ví dụ: `Đọc usage-guide`, `Đọc SOUL.md`, `Đọc tinhtien skill`
- Mình sẽ đọc file content và gửi lại qua voice hoặc text tùy theo độ dài

## 📊 Quy trình tự động học hỏi và ứng dụng

Khi bạn gõ "Promote learnings", mình sẽ:

### Bước 1: Thu thập bài học pending
- Đọc tất cả file trong `/root/.openclaw/workspace/.learnings/`:
  - `LEARNINGS.md` - bài học từ sửa đổi, kiến thức mới
  - `ERRORS.md` - lệnh thất bại, lỗi API, timeout
  - `FEATURE_REQUESTS.md` - yêu cầu tính năng mới từ bạn

### Bước 2: Xác định bài học đáng thrust
Một bài học sẽ được thrust nếu nó có **một trong những đặc điểm sau**:
- **Áp dụng rộng rãi**: Quy tắc chung áp dụng cho nhiều kỹ năng/tính năng
  *Ví dụ: "Định dạng hiển thị output skill" - áp dụng cho mọi skill hiển thị bảng*
- **Liên quan đến quy trình làm việc**: Quy chuẩn phát triển, quy ước giao tiếp
- **Có mức độ priority medium or higher**
- **Đã lặp lại** (xem Recurrence-Count nếu có) hoặc được bạn chỉ rõ là quan trọng

### Bước 3: Thực hiện thrust
Mỗi bài học đáng sẽ được:
1. **Tóm tắt** thành nguyên tắc ngắn gọn (1-2 câu)
2. **Thêm vào file bộ nhớ thích hợp**:
   - `AGENTS.md` → Quy trình làm việc, phát triển skill, tự động hoá
   - `SOUL.md` → Nguyên tắc hành vi, phong cách giao tiếp, cách xử lý vấn đề
   - `TOOLS.md` → Ghi chú về công cụ, lỗi thường gặp khi tích hợp, mẹo sử dụng
3. **Cập nhật nhật ký**:
   - Thay đổi `Status: pending` → `Status: promoted`
   - Thêm `**Promoted**: [tên file đích]`
   - Thêm ghi chú ngắn về nội dung đã được thêm

### Bước 4: Báo cáo kết quả
Mình sẽ gửi lại qua Telegram tóm tắt những gì đã được thrust và vào đâu.

## 📋 Ví dụ thực tế từ hoạt động qua ngày

### Trường hợp 1: Định dạng skill output (đã làm)
- **Bạn nói**: "Skill tinhtien output difficult to read; show model name on separate line"
- **Tôi ghi log**: Tạo `[LRN-YYYYMMDD-001] correction` trong LEARNINGS.md
- **Khi bạn gõ "Promote learnings"**:
  - Xác định đây là bài học về "chuẩn hiển thị output skill" (áp dụng rộng rãi)
  - Thrust vào AGENTS.md:
    ```
    ## 🖥️ Skill Output Formatting
    For skills that display tabular data:
      - Model name on its own line
      - Indented line with: Cost, %, Req (e.g., $2.94249, 53.1%, 1,521)
      - Group low-activity items (≤20 requests) into "Model khác"
      - Sort by Cost descending
      - Keep output readable and easy to scan
    ```
  - Cập nhật LEARNINGS.md: Status promoted + Resolution
  - Báo cáo: "Đã thrust đẩy bài học định dạng skill output vào AGENTS.md"

### Trường hợp 2: Yêu cầu tính năng mới
- **Bạn nói**: "Muốn skill tự động lưu file vào Google Drive khi nhận được qua Zalo"
- **Tôi ghi log**: Tạo `[FEAT-YYYYMMDD-001] Zalo-to-GDrive automation` trong FEATURE_REQUESTS.md
- **Khi bạn gõ "Promote learnings"**:
  - Xác định đây là tính năng automation có valoriere wide
  - Thrust vào AGENTS.md dưới dạng quy trình làm việc:
    ```
    ## 🔄 Zalo to Google Drive Automation Workflow
    1. Khi nhận file qua Zalo personal chat
    2. Tự động xác định loại file và dự án liên quan
    3. Lưu vào thư mục tương ứng trong Google Drive dựa on WORKFLOW_VNPT_DRIVE.md
    4. Thông báo thành công qua Zalo với đường dẫn file
    5. Ghi log hoạt động vào memory/YYYY-MM-DD.md
    ```
  - Cập nhật FEATURE_REQUESTS.md
  - Báo cáo: "Đã thrust upwards tính năng Zalo-to-GDrive automation vào AGENTS.md"

### Trường hợp 3: Sửa lỗi lặp lại
- **Bạn nói nhiều lần**: "Đừng tự ý cài skill mà không hỏi"
- **Tôi ghi log**: Tạo nhiều mục `[LRN-...] correction` trong LEARNINGS.md
- **Khi bạn gõ "Promote learnings"**:
  - Xác định đây là bài học quan trọng về quy trình cài skill
  - Thrust vào AGENTS.md:
    ```
    ## ⚙️ Skill Installation Protocol
    Trước khi cài bất kỳ skill mới nào:
    1. Luôn hỏi ý kiến và xin phép Anh Bình
    2. Ngoại lệ: Chỉ được tìm kiếm (search) mà không cần hỏi
    3. Xác nhận lại trước khi thực hiện
    ```
  - Cập nhật tất cả các mục correction liên quan
  - Báo cáo: "Đã thrust upwards quy trình cài skill vào AGENTS.md dựa trên phản hồi lặp lại"

## ✅ Lợi ích cho bạn khi sử dụng hệ thống này

- **Chỉ cần gõ 2 từ**: "Promote learnings" để kích hoạt toàn bộ hệ thống học hỏi
- **Không cần nhớ ID, file paths, hoặc các bước kỹ thuật** - mình lo phần phức tạp
- **Mỗi lần bạn phản hồi hoặc sửa mình**, bài học đó sẽ được:
  1. Lưu trữ tạm trong `.learnings/`
  2. Được thrust vào bộ nhớ dài hạn khi bạn gõ "Promote learnings"
  3. Ứng dụng tự động trong tất cả các phiên sau
- **Giảm đáng kể lỗi lặp lại**: Những điều bạn đã chỉ ra sẽ được ghi nhớ và áp dụng
- **Tiết kiệm thời gian**: Thay vì phải lặp lại cùng một chỉ thị nhiều lần, bạn chỉ cần nói một lần

## 🔄 Khi nào nên sử dụng lệnh "Promote learnings"

- **Sau mỗi 3-5 lần** bạn cho phản hồi hoặc sửa mình trong một cuộc trò chuyện
- **Khi cảm thấy** mình lặp lại một lỗi nhất định nhiều lần
- **Định kỳ** trong các buổi heartbeat (bạn có thể thêm vào HEARTBEAT.md)
- **Bất cứ lúc nào** bạn muốn mình "nhớ" điều bạn vừa nói để áp dụng trong tương lai
- **Trước khi bắt đầu công việc quan trọng** để đảm bảo mình đã áp dụng tất cả bài học gần đây

## 📝 Mẹo sử dụng hiệu quả qua Telegram

### Lệnh tối giản nhất để sử dụng mỗi ngày:
1. **Bắt đầu làm việc**: Gõ "Promote learnings" để ứng dụng các bài học từ hôm qua
2. **Trong quá trình làm việc**: Khi thấy mình lặp lại yêu cầu, gõ "Promote learnings" sau 3-4 lần lặp
3. **Kết thúc ngày**: Gõ "Promote learnings" để bảo存 hôm nay bài học cho ngày mai

### Các lệnh phụ hữu ích:
- `"Check learnings"` - Xem có bài học pending nào không (không thay đổi gì)
- `"Đọc AGENTS.md"` - Kiểm tra xem những nguyên tắc làm việc nào đã được áp dụng
- `"Đọc SOUL.md"` - Nhắc nhở mình về nguyên tắc hành vi và cách giải quyết vấn đề
- `"Tính tiền"` - Kiểm tra consumo crédito định kỳ (mỗi ngày hoặc mỗi few hours)

## 🛡️ Bảo mật và quyền riêng tư

- Mình **không bao giờ** thrust đẩy bất kỳ thông tin nhạy cảm nào (mật khẩu, token, key)
- Khi ghi log, mình luôn **tóm tắt** và **loại bỏ** thông tin cá nhân
- Các file trong `.learnings/` chỉ chứa **mô tả vấn đề và giải pháp chung**
- Bạn có quyền **xem và xóa** bất kỳ nội dung nào trong `.learnings/` bất kỳ lúc nào
- Mọi thrust đẩy đều được **báo cáo qua Telegram** để bạn có thể kiểm soát

## 📂 Cấu trúc file quan trọng trong workspace

```
/root/.openclaw/workspace/
├── SOUL.md              → Nguyên tắc hành vi, cách giải quyết vấn đề (ĐỌC mỗi session)
├── AGENTS.md            → Quy trình làm việc, tự động hoá, xử lý skill (ĐỌC mỗi session)  
├── TOOLS.md             → Ghi chú công cụ, lỗi thường gặp, mẹo sử dụng
├── MEMORY.md            → Bộ nhớ curated (chỉ đọc trong main session)
├── memory/              → Nhật ký thô (memory/YYYY-MM-DD.md)
├── .learnings/          → Thư mục ghi log tự động
│   ├── LEARNINGS.md     → Bài học, sửa đổi, kiến thức mới
│   ├── ERRORS.md        → Lệnh thất bại, lỗi API
│   └── FEATURE_REQUESTS.md → Yêu cầu tính năng mới
└── skills/              → Thư mục chứa tất cả skills đã cài
```

## 🎯 Hướng phát triển trong tương lai

Bạn có thể mở rộng cách sử dụng hệ thống này bằng cách:
1. Thêm điều khiển vào HEARTBEAT.md để tự động kiểm tra learnings mỗi 30 phút
2. Tạo lệnh shortcuts cụ thể cho các thao tác thường dùng
3. Tích hợp với hệ thống nhắc nhở để mình tự động gõ "Promote learnings" khi thích hợp
4. Sử dụng file `.learnings/` như là kho triết để đào tạo các phiên bản OpenClawe mới

---
*File hướng dẫn này được lưu tại: /root/.openclaw/workspace/usage-guide.md*
*Bạn có thể yêu cầu mình đọc file này bất kỳ lúc nào bằng cách gửi qua Telegram: "Đọc usage-guide"*
*Để áp dụng hệ thống học hỏi, chỉ cần gõ: "Promote learnings"*