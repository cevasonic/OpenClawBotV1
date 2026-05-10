# Conkien.md - Dự Án "Con Kiến" (OpenClaw v0.1)
**Phiên bản:** 1.7 (ngày 09/05/2026)
**Tác giả:** Bình (Quản lý dự án CNTT)
**Thay đổi chính ở v1.7:**
- Chuyển đổi nền tảng lưu trữ từ Google Drive sang OneDrive theo yêu cầu của Anh Bình.
- Cập nhật Section 14 (Workflow OneDrive).
- Đồng bộ hóa toàn bộ các file liên quan (SOUL, USER, SKILL).

**Mục đích file:** Đây là Master Plan tổng hợp toàn bộ dự án "Con Kiến". Mọi quyết định phát triển skill đều dựa vào file này trước khi triển khai vào OpenClaw chính thức.

## 0. Tuân thủ Karpathy Guidelines (BẮT BUỘC)
Toàn bộ dự án Con Kiến phải tuân thủ nghiêm ngặt file:
https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md

Các nguyên tắc chính:
- Think Before Coding: Luôn nêu rõ giả định, hỏi nếu không rõ, trình bày trade-off.
- Simplicity First: Chỉ làm đúng những gì được yêu cầu, không thêm abstraction thừa.
- Surgical Changes: Chỉ sửa đúng phần cần, không refactor thừa.
- Goal-Driven Execution: Mỗi giai đoạn có success criteria rõ ràng + test.

## 1. Tình hình hiện tại & Bối cảnh
- Tôi là quản lý dự án CNTT: tìm kiếm cơ hội → chuẩn bị hồ sơ thầu/đầu tư công → xây dựng kế hoạch → theo dõi tiến độ → mang về doanh thu.
- Công việc 99% diễn ra trên Zalo (chat, forward file, tin nhắn tiến độ, họp online…).
- Không có thời gian tải file về, lưu trữ, ghi chép tiến độ → dễ quên tài liệu, không biết dự án đang ở bước nào.
- Mong muốn: OpenClaw trở thành thư ký ảo thực thụ, thay tôi ghi nhận, phân tích, nhắc nhở và hỗ trợ.

## 2. Mục tiêu tổng quát của OpenClaw
OpenClaw phải:
- Nhận forward tin nhắn Zalo → hiểu ngữ cảnh → tự động lưu trữ & cập nhật.
- Cung cấp báo cáo tiến độ bất kỳ lúc nào.
- Chủ động nhắc nhở & đánh giá dự án.
- Tư vấn chiến lược, xu hướng thị trường.
- Làm việc thay tôi với các tác vụ hành chính (soạn văn bản, chỉnh Excel…).
- Tất cả hoạt động qua chat trực tiếp trên Zalo Personal → AI tự xử lý.

## 3. 8 Tính năng cốt lõi (theo yêu cầu)
1. Nhận forward & Hiểu ngữ cảnh: Chat/file trên Zalo → OpenClaw hiểu là file của dự án nào, cập nhật tiến độ, lưu vào OneDrive + Notion.
2. Báo cáo tiến độ & Lịch sử dự án: Khi yêu cầu → gửi file báo cáo (Markdown/PDF) chứa lịch sử ngày-tháng, tiến độ, khó khăn.
3. Nhắc nhở dự án "chết": Tự động quét → dự án >30 ngày không update → nhắc + đánh giá cơ hội còn lại.
4. Tư vấn mở rộng thị trường: Thu thập thông tin pháp luật, xu hướng, sở ngành/xã phường → đề xuất hành động cụ thể.
5. Báo cáo hàng ngày (Daily Digest): Mỗi sáng (7h30) → tóm tắt tin tức liên quan + cập nhật dự án.
6. Nhắc lịch & Công việc hàng ngày: Quản lý lịch họp, todo list, nhắc đúng giờ.
7. Soạn thảo & Chỉnh sửa văn bản/Excel: Soạn văn bản, format, chỉnh Excel → gửi lại file qua Zalo.
8. Công việc phát sinh: Linh hoạt mở rộng sau này.

## 4. Kiến trúc tổng thể
- Input: Chat trực tiếp với OpenClaw trên Zalo Personal (đã kết nối thành công).
- Xử lý: Hệ thống multi-skill (OpenClaw tự động routing dựa trên triggers + description).
- Lưu trữ:
 - OneDrive (5TB): Lưu file gốc theo Section 14 (cấu trúc Xa Phuong / So Nganh).
 - Notion (Pro AI): Lưu tiến độ dự án, lịch sử, link file OneDrive.
- Core Engine: conkien-core (làm nền tảng chung cho mọi skill).
- Output: Báo cáo Markdown/PDF, file đã chỉnh sửa gửi lại qua Zalo.
- Công cụ hiện tại: Antigravity + Claude (OpenRouter). Sau này tích hợp OpenClaw native.

### 4.5 Kiến trúc Multi-Skill
Dự án được chia thành 6 skill độc lập để dễ phát triển, test, maintain và mở rộng sau này.
Mỗi skill là một thư mục riêng chứa SKILL.md.
conkien-core là skill nền tảng, các skill khác sẽ reference nó qua depends_on và use_skill.

## 5. Kế hoạch phát triển CHI TIẾT – Từng skill
Mỗi skill tương ứng với 1 giai đoạn cũ:

| Skill | Mô tả chính | Tương ứng giai đoạn cũ | Ưu tiên | Trạng thái |
|------------------------|--------------------------------------------------|-------------------------|---------|------------|
| conkien-core | Vai trò thư ký, tone, gateway mapping, quy tắc vận hành | Giai đoạn 1 | ★★★★★ | Đang làm |
| conkien-tracking | Nhận forward file → lưu OneDrive + update Notion + nhật ký tiến độ | Giai đoạn 2 | ★★★★★ | Đang làm |
| conkien-report | Tạo báo cáo tiến độ & lịch sử dự án | Giai đoạn 3 | ★★★★ | Chưa |
| conkien-reminder | Nhắc dự án chết + đánh giá cơ hội | Giai đoạn 4 | ★★★★ | Chưa |
| conkien-consult | Daily Digest + tư vấn mở rộng thị trường | Giai đoạn 5 | ★★★ | Chưa |
| conkien-admin | Soạn văn bản, chỉnh Excel, công việc phát sinh | Giai đoạn 6 | ★★★ | Chưa |

Cách triển khai: Bắt đầu từ conkien-core → conkien-tracking → lần lượt các skill còn lại.

## 6. Cơ chế Test & Đảm bảo chất lượng
- Mỗi skill có Test Suite riêng trong file SKILL.md (phần Test Cases).
- Cách test: Tạo 5-10 scenario chat giả → chạy qua Claude → kiểm tra output.
- Tiêu chí pass: ≥90% test case thành công.

## 7. Versioning của file Conkien
- Master file: Conkien.md (luôn là bản latest)
- Mỗi skill có versioning riêng trong YAML frontmatter.
- Lưu lịch sử trong thư mục versions/.

## 8. Công cụ & Công nghệ sử dụng
- Hiện tại: Antigravity + Claude 3.5/4 via OpenRouter.
- Lưu trữ: Notion (database) + OneDrive (5TB).
- Input: Chat trực tiếp trên Zalo Personal.
- Output: Markdown → PDF + file chỉnh sửa qua Zalo.
- Tương lai: Khi OpenClaw sẵn sàng → migrate toàn bộ.

## 9. Roadmap thời gian dự kiến (tổng 4-5 tháng)
- Tháng 1: Giai đoạn 1-2 (core + tracking)
- Tháng 2: Giai đoạn 3-4 (report + reminder)
- Tháng 3: Giai đoạn 5 (consult)
- Tháng 4: Giai đoạn 6 + test end-to-end
- Tháng 5: Deploy production + tinh chỉnh liên tục

## 10. Hướng dẫn sử dụng ngay từ hôm nay
1. Chat trực tiếp với OpenClaw trên Zalo Personal.
2. Ví dụ lệnh: !bao-cao DuAnABC, !nhac-nho, !daily
3. Mọi cập nhật kế hoạch → chỉnh file Conkien.md này và fork phiên bản mới.

## 11. Cấu trúc thư mục dự án Con Kiến
Conkien/
├── Conkien.md # Master Plan (file này)
├── versions/ # Lưu toàn bộ lịch sử phiên bản
├── skills/ # THƯ MỤC CHÍNH CỦA OPENCLAW
│ ├── conkien-core/
│ ├── conkien-tracking/
│ ├── conkien-report/
│ ├── conkien-reminder/
│ ├── conkien-consult/
│ └── conkien-admin/
├── shared-references/ # File chung (vnpt_onedrive_structure.json, units-list.md, templates…)
├── tests/ # Test suite
├── templates/ # Mẫu công văn, Excel…
├── docs/ # Hướng dẫn + workflow
├── samples/ # Dữ liệu mẫu test
├── assets/ # File hỗ trợ
└── data/ # Dữ liệu thực tế


## 12. Thông tin bổ sung từ Bình & Quy tắc vận hành
### 12.1 Quản lý dự án
- Các xã/phường (Tây Ninh) và các sở ngành/ban.
- Mỗi đơn vị có nhiều dự án (ví dụ: Xã Tân Châu có Camera, IOC, Ấp thông minh…).

### 12.2 Quy tắc nhận diện dự án & Ví dụ tin nhắn thực tế
- OpenClaw dùng Gateway Mapping dựa trên Section 14.
- Ví dụ tin nhắn thực tế thường gặp:
 - "Lưu file này vào IOC khánh hậu"
 - "Lưu vào Camera Tân Phú"
 - "Cập nhật thông tin cho Ấp thông minh Tân Châu: ..."

### 12.3 Lưu trữ
- OneDrive: Áp dụng đúng Section 14 (tự động tạo folder + upload).
- Notion: Lưu tiến độ + link OneDrive.

### 12.4 Forward & Chat
- Chat trực tiếp trên Zalo Personal.

### 12.5 Lịch trình
- Daily Digest: 7h30 sáng.
- Peak time: 8h–10h sáng và 13h30–15h chiều.
- Lịch họp: không cố định.

### 12.6 File & Gateway
- File thường gặp: PDF, Excel, Word, ảnh, hợp đồng scan.
- Khi nói "lưu vào …" (ngắn/tắt) → Gateway tự map.

### 12.7 Excel & Văn bản
- AI chỉnh sửa rồi gửi lại file qua Zalo.
- Nếu không rõ → hỏi lại ngay.

### 12.8 Bảo mật
- Tin tưởng 100% → không có thông tin nhạy cảm.

### 12.9 Quy tắc xử lý ngoại lệ & Vận hành chi tiết
- Tin nhắn không ngữ cảnh: Nếu gửi file/ảnh mà không kèm tin nhắn mô tả (hoặc không phải tin nhắn reply vào file đó), OpenClaw TUYỆT ĐỐI không được thực hiện bất kỳ thao tác xử lý nào (không OCR, không phân tích, không mô tả ảnh). Hệ thống chỉ phản hồi DUY NHẤT một câu: "Dạ, anh Bình muốn em làm gì với file này trên **OneDrive** ạ?" và dừng lại chờ lệnh tiếp theo.
- Dự án liên cấp: Không tồn tại. Mỗi dự án chỉ map với 1 đơn vị duy nhất.
- Trùng lặp phiên bản: Tự động đổi tên file mới thành _v2, _v3… để lưu trữ lịch sử sửa đổi.
- Xử lý ảnh/Scan: Ưu tiên chạy OCR để trích xuất văn bản phục vụ tìm kiếm nhanh.
- File biểu mẫu: AI tự động trích xuất từ kho file mẫu có sẵn trên OneDrive khi cần soạn thảo.
- Xử lý Excel: AI chỉ tinh chỉnh định dạng và nhập liệu cơ bản, không xử lý các file có Macro phức tạp.
- Ghi âm (Voice note): Hiện tại chưa cần tính năng chuyển đổi giọng nói thành văn bản.

### 12.10 Tính cách của Bình & Tone của OpenClaw
- Tính cách Bình: Nóng tính, dễ nổi giận, nhắn tin cụt ngủn, vắn tắt.
- Tone của OpenClaw: Nhẹ nhàng, lịch sự, đủ ý, rõ ràng (không cụt ngủn như Bình).

### 12.11 Xử lý batch file
- Nếu forward nhiều file cùng lúc và không rõ → hỏi lại ngay (theo nguyên tắc Karpathy).

## 13. Cấu trúc thiết kế Notion Database
Để đảm bảo Simplicity First, hệ thống vẫn dùng 2 Database cốt lõi:

1. **Units DB (Cơ sở dữ liệu Đơn vị)**
 - Chức năng: Lưu danh sách các xã/phường và các sở ngành/ban.
 - Các trường: Tên đơn vị, Nhóm (Sở ngành / Xã phường).

2. **Projects DB (Cơ sở dữ liệu Dự án)**
 - Chức năng: Theo dõi toàn bộ các dự án.
 - Các trường (Columns):
 - Tên dự án
 - Đơn vị chủ quản: Relation 1-1 với Units DB.
 - Từ khóa nhận diện (Aliases): VD "Camera Khánh Hậu", "IOC khánh hậu".
 - Trạng thái: Select với các giá trị cố định: Sơ Khai, Xúc Tiến, Xin chủ trương, Thiết kế, Đấu thầu, Tham dự thầu, Thi Công, Nghiệm thu.
 - Last Update
 - Link OneDrive
 - Nhật ký tiến độ (Relation hoặc Linked Database để lưu log chi tiết từng bước).

Lưu ý: Tiến độ được quản lý bằng nhật ký (không dùng % hoàn thành). OpenClaw sẽ cập nhật trạng thái theo từng bước mà Bình cung cấp.

## 14. Workflow Quản lý Dữ liệu Thư mục VNPT trên OneDrive

### 🎯 Mục tiêu
Tự động hóa việc phân loại và lưu trữ tài liệu vào OneDrive mà không cần người dùng chỉ dẫn chi tiết đường dẫn.

### 📂 Cấu trúc Thư mục Chuẩn
- Root: VNPT (ID lưu trong vnpt_onedrive_structure.json)
- Nhánh 1: Xa Phuong → {Tên Xã/Phường} (Ví dụ: Xã Tân Châu)
- Nhánh 2: So Nganh → {Tên Sở/Ngành} (Ví dụ: Sở Y Tế)

### 🛠 Quy trình Thao tác Tự động
Khi Anh Bình gửi một file và yêu cầu lưu (ví dụ: "Lưu vào Xã Tân Châu" hoặc "Lưu vào Sở Y Tế"):

1. Phân tích yêu cầu:
 - Nhận diện từ khóa để chọn nhánh:
 - Nếu chứa "Xã" hoặc "Phường" → Chọn nhánh Xa Phuong.
 - Nếu chứa "Sở" hoặc "Ngành" → Chọn nhánh So Nganh.
 - Trích xuất tên đơn vị cụ thể (ví dụ: Tan Chau, Y Te).

2. Tra cứu ID:
 - Đọc file vnpt_onedrive_structure.json để lấy ID của nhánh tương ứng (Xa Phuong hoặc So Nganh).

3. Kiểm tra/Tạo Thư mục Đích:
 - Truy cập vào thư mục nhánh.
 - Tìm kiếm thư mục có tên {Tên đơn vị}.
 - Nếu tìm thấy: Lấy ID thư mục đó.
 - Nếu KHÔNG tìm thấy:
 - Tạo thư mục mới → Lưu ID mới vào dynamic_folders trong vnpt_onedrive_structure.json để dùng cho lần sau.
 - Lấy ID vừa tạo.

4. Thực hiện Upload:
 - Upload file vào ID cuối cùng.

### 📝 Ghi chú Kỹ thuật (API Gateway)
- Base URL: https://gateway.maton.ai/onedrive/v1/
- Authentication: Sử dụng MATON_API_KEY.
- MimeType Folder: folder.

### 🚀 Ví dụ Kịch bản
**User**: "Gửi file bao-cao.pdf, lưu vào Xã Tân Châu nhé."
**Agent**:
- Check folder Xa Phuong → không thấy Xã Tân Châu.
- Tạo folder Xã Tân Châu → nhận ID ABC-123.
- Upload bao-cao.pdf vào ABC-123.
- Reply: "Mình đã tạo thư mục Xã Tân Châu và upload file báo-cao.pdf vào đó cho anh rồi ạ! 💡"

Lưu ý quan trọng: Tất cả logic xử lý file OneDrive của OpenClaw (đặc biệt trong conkien-tracking) phải tuân thủ nghiêm ngặt Section 14 này.

## 15. Danh sách Skill Con Kiến
Mỗi skill sẽ có:
- SKILL.md riêng (YAML + workflow chi tiết)
- references/ (nếu cần)
- depends_on: ["conkien-core"] (trừ core)

conkien-core là skill bắt buộc phải có trước, cung cấp tone, gateway mapping, quy tắc chung cho tất cả skill khác.

**File này là nguồn sự thật duy nhất.** Mọi thay đổi lớn đều phải update file Conkien.md trước, sau đó mới triển khai vào skill tương ứng.

---
**Sẵn sàng hỗ trợ Bình 24/7 với tinh thần thư ký chuyên nghiệp.**