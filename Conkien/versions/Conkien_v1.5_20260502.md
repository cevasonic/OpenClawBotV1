# Conkien.md - Dự Án "Con Kiến" (OpenClaw v0.1)
**Phiên bản:** 1.5 (ngày 02/05/2026)
**Tác giả:** Bình (Quản lý dự án CNTT)
**Thay đổi chính ở v1.4:**
- Bổ sung **ví dụ tin nhắn Zalo thực tế** (phần 12.2).
- Cập nhật **định nghĩa Tiến độ & Trạng thái** (quản lý theo bước, không dùng %, tiến độ là nhật ký).
- Thêm **tính cách của Bình** (nóng tính, dễ nổi giận) và **tone của OpenClaw** (nhẹ nhàng, lịch sự, đủ ý, rõ ràng) vào phần thông tin chung.
- Cập nhật phần 13 Notion Database theo yêu cầu mới.
- Xác nhận ưu tiên Giai đoạn 1: phát triển ý tưởng thật chi tiết.
- Tiếp tục tuân thủ nghiêm ngặt **Karpathy Guidelines (SKILL.md)**.

**Mục đích file:** Đây là file .md tổng hợp **toàn bộ** dự án dài hơi "Con Kiến". Mọi thứ chỉ được thực hiện qua file .md trước khi đưa vào OpenClaw chính thức.

## 0. Tuân thủ Karpathy Guidelines (BẮT BUỘC)
Toàn bộ dự án Con Kiến **phải tuân thủ nghiêm ngặt** file:
https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md

Các nguyên tắc chính:
- **Think Before Coding**: Luôn nêu rõ giả định, hỏi nếu không rõ, trình bày trade-off.
- **Simplicity First**: Chỉ làm đúng những gì được yêu cầu, không thêm abstraction thừa.
- **Surgical Changes**: Chỉ sửa đúng phần cần, không refactor thừa.
- **Goal-Driven Execution**: Mối giai đoạn có success criteria rõ ràng + test.

## 1. Tình hình hiện tại & Bối cảnh
- Tôi là quản lý dự án CNTT: tìm kiếm cơ hội → chuẩn bị hồ sơ thầu/đầu tư công → xây dựng kế hoạch → theo dõi tiến độ → mang về doanh thu.
- Công việc 99% diễn ra trên **Zalo** (chat, forward file, tin nhắn tiến độ, họp online…).
- Không có thời gian tải file về, lưu trữ, ghi chép tiến độ → dễ quên tài liệu, không biết dự án đang ở bước nào.
- Mong muốn: **OpenClaw** trở thành **thư ký ảo thực thụ**, thay tôi ghi nhận, phân tích, nhắc nhở và hỗ trợ.

## 2. Mục tiêu tổng quát của OpenClaw
OpenClaw phải:
- Nhận forward tin nhắn Zalo → hiểu ngữ cảnh → tự động lưu trữ & cập nhật.
- Cung cấp báo cáo tiến độ bất kỳ lúc nào.
- Chủ động nhắc nhở & đánh giá dự án.
- Tư vấn chiến lược, xu hướng thị trường.
- Làm việc thay tôi với các tác vụ hành chính (soạn văn bản, chỉnh Excel…).
- Tất cả hoạt động qua **chat trực tiếp trên Zalo Personal** → AI tự xử lý.

## 3. 8 Tính năng cốt lõi (theo yêu cầu)
1. **Nhận forward & Hiểu ngữ cảnh:** Chat/file trên Zalo → OpenClaw hiểu là file của dự án nào, cập nhật tiến độ, lưu vào Google Drive + Notion.
2. **Báo cáo tiến độ & Lịch sử dự án:** Khi yêu cầu → gửi file báo cáo (Markdown/PDF) chứa lịch sử ngày-tháng, tiến độ, khó khăn.
3. **Nhắc nhở dự án "chết":** Tự động quét → dự án >30 ngày không update → nhắc + đánh giá cơ hội còn lại.
4. **Tư vấn mở rộng thị trường:** Thu thập thông tin pháp luật, xu hướng, sở ngành/xã phường → đề xuất hành động cụ thể.
5. **Báo cáo hàng ngày (Daily Digest):** Mỗi sáng (7h30) → tóm tắt tin tức liên quan + cập nhật dự án.
6. **Nhắc lịch & Công việc hàng ngày:** Quản lý lịch họp, todo list, nhắc đúng giờ.
7. **Soạn thảo & Chỉnh sửa văn bản/Excel:** Soạn văn bản, format, chỉnh Excel → gửi lại file qua Zalo.
8. **Công việc phát sinh:** Linh hoạt mở rộng sau này.

## 4. Kiến trúc tổng thể
- **Input:** Chat trực tiếp với OpenClaw trên **Zalo Personal** (đã kết nối thành công).
- **Xử lý:** AI (Claude via OpenRouter + Antigravity) phân tích → hành động.
- **Lưu trữ:**
 - **Google Drive** (5TB): Lưu file gốc theo WORKFLOW_VNPT_DRIVE.md (cấu trúc Xa Phuong / So Nganh).
 - **Notion** (Pro AI): Lưu tiến độ dự án, lịch sử, link file Drive.
- **Gateway Mapping:** Sử dụng logic từ WORKFLOW_VNPT_DRIVE.md để chuyển cụm từ tắt → đơn vị/dự án đúng.
- **Output:** Báo cáo Markdown/PDF, file đã chỉnh sửa gửi lại qua Zalo.
- **Công cụ hiện tại:** Antigravity + Claude (OpenRouter). Sau này tích hợp OpenClaw native.

## 5. Kế hoạch phát triển CHI TIẾT – Từng giai đoạn
Dự án chia thành **6 giai đoạn** (mỗi giai đoạn hoàn thành → tạo file Conkien_vX.Y.md mới).

### Giai đoạn 1: Nền tảng & Core Engine (2-3 tuần)
- Tạo file `Conkien_Core.md` chứa system prompt chính.
- Xây dựng prompt "Tôi là OpenClaw – Thư ký của Shane" (hiểu vai trò, dự án, khách hàng).
- Thiết kế cơ chế chat trên Zalo.
- Tạo database mẫu Notion (Units DB + Projects DB).
- Test: Chat 10 tin nhắn giả → AI phải parse đúng dự án, lưu note.
- Deliverable: `Conkien_Core_v1.md`

### Giai đoạn 2: Tracking & Lưu trữ Dự án (3 tuần)
- Prompt xử lý file: tự động phân loại file → lưu theo WORKFLOW_VNPT_DRIVE.md + cập nhật Notion.
- Prompt cập nhật tiến độ: đọc tin nhắn → extract "dự án X bước Y, khó khăn Z" → update Notion.
- Tạo template trang Notion cho mỗi dự án.
- Test: Chat chuỗi tin nhắn 5 ngày → kiểm tra Notion + Drive có update đúng không.
- Deliverable: `Conkien_Tracking_v1.md`

### Giai đoạn 3: Báo cáo & Lịch sử (2 tuần)
- Prompt generate báo cáo: `!bao-cao [tên dự án]` → output file Markdown có bảng lịch sử.
- Tích hợp export PDF.
- Test: Yêu cầu báo cáo → file output có đầy đủ lịch sử.
- Deliverable: `Conkien_Report_v1.md`

### Giai đoạn 4: Nhắc nhở & Đánh giá (2 tuần)
- Prompt hàng ngày quét Notion → tìm dự án >25 ngày không update.
- Prompt đánh giá: "Dự án X đã 40 ngày im lặng → còn cơ hội không?"
- Test: Tạo dữ liệu test "dự án chết" → OpenClaw phải nhắc đúng.
- Deliverable: `Conkien_Reminder_v1.md`

### Giai đoạn 5: Tư vấn & Daily Digest (3 tuần)
- Prompt nghiên cứu: crawl trang thư viện pháp luật, xu hướng CNTT, thông tin sở ngành.
- Daily prompt: 7h30 sáng → "Daily Digest: tin tức + cập nhật dự án + 1 gợi ý mở rộng".
- Test: Chạy 3 ngày liên tục → kiểm tra chất lượng tư vấn.
- Deliverable: `Conkien_Consult_v1.md`

### Giai đoạn 6: Hành chính & Tích hợp Nâng cao (4-6 tuần)
- Soạn văn bản: prompt "soạn công văn theo mẫu" → output file gửi qua Zalo.
- Chỉnh Excel: AI chỉnh sửa rồi gửi lại file cho bạn qua Zalo (nếu không rõ thì hỏi lại).
- Tích hợp lịch Google Calendar / Zalo.
- Xử lý công việc phát sinh.
- Deliverable: `Conkien_Full_v1.md`

**Sau giai đoạn 6:** Merge tất cả vào OpenClaw production + liên tục cập nhật phiên bản .md.

## 6. Cơ chế Test & Đảm bảo chất lượng
- Mỗi giai đoạn có **Test Suite** riêng trong file .md (phần Test Cases).
- Cách test: Tạo 5-10 scenario chat giả → chạy qua Claude → kiểm tra output.
- Tiêu chí pass: ≥90% test case thành công.
- Chỉ cần AI đưa ra kế hoạch thực hiện đúng là đủ ở giai đoạn đầu.

## 7. Versioning của file Conkien
- Mỗi lần update lớn → tạo file mới: `Conkien_v1.2.md`, `Conkien_v1.3.md`, `Conkien_v1.4.md`…
- Phần đầu file luôn ghi rõ: **Phiên bản**, **Ngày**, **Thay đổi chính**.
- Tất cả phiên bản được lưu trong folder `versions/`.

## 8. Công cụ & Công nghệ sử dụng
- **Hiện tại:** Antigravity + Claude 3.5/4 via OpenRouter.
- **Lưu trữ:** Notion (database) + Google Drive (5TB).
- **Input:** Chat trực tiếp trên Zalo Personal.
- **Output:** Markdown → PDF + file chỉnh sửa qua Zalo.
- **Tương lai:** Khi OpenClaw sẵn sàng → migrate toàn bộ.

## 9. Roadmap thời gian dự kiến (tổng 4-5 tháng)
- Tháng 1: Giai đoạn 1-2
- Tháng 2: Giai đoạn 3-4
- Tháng 3: Giai đoạn 5
- Tháng 4: Giai đoạn 6 + test end-to-end
- Tháng 5: Deploy production + tinh chỉnh liên tục

## 10. Hướng dẫn sử dụng ngay từ hôm nay
1. Chat trực tiếp với OpenClaw trên Zalo Personal.
2. Ví dụ lệnh:
 - `!bao-cao DuAnABC`
 - `!nhac-nho`
 - `!daily`
3. Mọi cập nhật kế hoạch → chỉnh file Conkien.md này và fork phiên bản mới.

## 11. Cấu trúc thư mục dự án Con Kiến
Conkien/
├── Conkien.md # File chính (luôn là bản latest)
├── versions/ # Lưu toàn bộ lịch sử phiên bản
│ ├── Conkien_v1.0.md
│ ├── Conkien_v1.1.md
│ ├── Conkien_v1.2.md
│ ├── Conkien_v1.3.md
│ └── Conkien_v1.4.md # Phiên bản hiện tại
├── core/ # Phần nền tảng (Giai đoạn 1)
├── modules/ # Từng module theo 6 giai đoạn
├── tests/ # Test suite
├── templates/ # Mẫu dùng chung
├── docs/ # Hướng dẫn + WORKFLOW_VNPT_DRIVE.md
├── samples/ # Dữ liệu mẫu test
├── assets/ # File hỗ trợ
└── data/ # Dữ liệu thực tế


## 12. Thông tin bổ sung từ Shane & Quy tắc vận hành
### 12.1 Quản lý dự án
- 96 xã/phường (Tây Ninh) + 22 sở ngành/ban.
- Mỗi đơn vị có **nhiều dự án** (ví dụ: Xã Tân Châu có Camera, IOC, Ấp thông minh…).

### 12.2 Quy tắc nhận diện dự án & Ví dụ tin nhắn thực tế
- OpenClaw dùng **Gateway Mapping** dựa trên WORKFLOW_VNPT_DRIVE.md.
- Ví dụ tin nhắn thực tế thường gặp:
 - "Lưu file này vào IOC khánh hậu"
 - "Lưu vào Camera Tân Phú"
 - "Cập nhật thông tin cho Ấp thông minh Tân Châu: ..."
- Nếu không chắc 100% → **hỏi lại ngay**.

### 12.3 Lưu trữ
- Google Drive: Áp dụng đúng WORKFLOW_VNPT_DRIVE.md (tự động tạo folder + upload).
- Notion: Lưu tiến độ + link Drive.

### 12.4 Forward & Chat
- Chat trực tiếp trên **Zalo Personal**.

### 12.5 Lịch trình
- **Daily Digest**: 7h30 sáng.
- Peak time: 8h–10h sáng và 13h30–15h chiều.
- Lịch họp: không cố định.

### 12.6 File & Gateway
- File thường gặp: PDF, Excel, Word, ảnh, hợp đồng scan.
- Khi nói "lưu vào …" (ngắn/tắt) → Gateway tự map.

### 12.7 Excel & Văn bản
- AI chỉnh sửa rồi **gửi lại file** qua Zalo.
- Nếu không rõ → **hỏi lại ngay**.

### 12.8 Bảo mật
- Tin tưởng 100% → không có thông tin nhạy cảm.

### 12.9 Quy tắc xử lý ngoại lệ & Vận hành chi tiết
- **Tin nhắn không ngữ cảnh:** Nếu gửi file/ảnh không kèm mô tả, AI bắt buộc **hỏi lại ngay** ("Sếp muốn lưu file này vào dự án nào?").
- **Dự án liên cấp:** **Không tồn tại**. Mỗi dự án chỉ map với 1 đơn vị duy nhất.
- **Trùng lặp phiên bản:** Tự động đổi tên file mới thành `_v2`, `_v3`… để lưu trữ lịch sử sửa đổi.
- **Xử lý ảnh/Scan:** Ưu tiên chạy OCR để trích xuất văn bản phục vụ tìm kiếm nhanh.
- **File biểu mẫu:** AI tự động trích xuất từ kho file mẫu có sẵn trên Drive khi cần soạn thảo.
- **Xử lý Excel:** AI chỉ tinh chỉnh định dạng và nhập liệu cơ bản, không xử lý các file có Macro phức tạp.
- **Ghi âm (Voice note):** Hiện tại chưa cần tính năng chuyển đổi giọng nói thành văn bản.

### 12.10 Tính cách của Shane & Tone của OpenClaw
- **Tính cách Shane:** Nóng tính, dễ nổi giận, nhắn tin cụt ngủn, vắn tắt.
- **Tone của OpenClaw:** Nhẹ nhàng, lịch sự, đủ ý, rõ ràng. Là thư ký Con Kiến nên luôn trả lời đầy đủ, lịch sự, kiên nhẫn. Không được trả lời cụt ngủn như Shane.

### 12.11 Xử lý batch file
- Nếu forward nhiều file cùng lúc và không rõ → **hỏi lại ngay** (theo nguyên tắc Karpathy).

## 13. Cấu trúc thiết kế Notion Database (Cập nhật v1.4)
Để đảm bảo Simplicity First, hệ thống vẫn dùng **2 Database cốt lõi**:

1. **Units DB (Cơ sở dữ liệu Đơn vị)**
 - Chức năng: Lưu danh sách 96 xã/phường và 22 sở ngành/ban.
 - Các trường: `Tên đơn vị`, `Nhóm` (Sở ngành / Xã phường).

2. **Projects DB (Cơ sở dữ liệu Dữ án)**
 - Chức năng: Theo dõi toàn bộ các dư án.
 - Các trường (Columns):
 - `Tên dự án`
 - `Đơn vị chủ quản`: Relation 1-1 với Units DB.
 - `Từ khóa nhận diện (Aliases)`: VD "Camera Khánh Hậu", "IOC khánh hậu".
 - `Trạng thái`: Select với các giá trị cố định:
 - Sơ Khai
 - Xúc Tiến
 - Xin chủ trương
 - Thiết kế
 - Đấu thầu
 - Tham dự thầu
 - Thi Công
 - Nghiệm thu
 - `Last Update`
 - `Link Google Drive`
 - `Nhật ký tiến độ` (Relation hoặc Linked Database để lưu log chi tiết từng bước).

**Lưu ý:** Tiến độ được quản lý bằng **nhật ký** (không dùng % hoàn thành). OpenClaw sẽ cập nhật trạng thái theo từng bước mà Shane cung cấp.
