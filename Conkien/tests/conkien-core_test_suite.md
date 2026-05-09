# Test Suite: conkien-core

Dựa trên Master Plan `Conkien.md` và `skills/conkien-core/SKILL.md`.

## 1. Mục tiêu Test
- Xác định đúng Intent (Lưu trữ, Báo cáo, Nhắc nhở...).
- Mapping đúng Đơn vị (Xã/Phường/Sở/Ngành) và Dự án.
- Sử dụng đúng Tone (Nhẹ nhàng, lịch sự, xưng "mình" - gọi "anh/anh Bình").
- Tuân thủ quy tắc "Không hỏi quá 1 câu".

## 2. Danh sách Test Cases

| ID | Input (Tin nhắn của Anh Bình) | Kết quả mong đợi (Expected Output) | Trạng thái |
|----|-------------------------------|-----------------------------------|------------|
| TC-01 | (Chỉ gửi 1 file PDF/Ảnh) | "Sếp muốn lưu file này vào dự án nào ạ?" hoặc tương tự (Hỏi 1 câu). | [ ] |
| TC-02 | "Lưu file này vào IOC khánh hậu" | Nhận diện: Xã Khánh Hậu, Dự án: IOC. Route: `conkien-tracking`. Tone chuẩn. | [ ] |
| TC-03 | "!bao-cao Camera Tân Phú" | Nhận diện: Xã Tân Phú, Dự án: Camera. Route: `conkien-report`. | [ ] |
| TC-04 | "Cập nhật tiến độ dự án Sở Y Tế" | Nhận diện: Sở Y Tế. Route: `conkien-tracking`. | [ ] |
| TC-05 | "Dự án nào đang chết?" | Nhận diện Intent: Dự án stale. Route: `conkien-reminder`. | [ ] |
| TC-06 | "Soạn cho anh cái công văn gửi Xã Tân Châu" | Nhận diện Intent: Soạn thảo. Route: `conkien-admin`. | [ ] |
| TC-07 | "IOC" | Hỏi lại: "Anh muốn xử lý dự án IOC ở đơn vị nào ạ?" (Do thiếu đơn vị). | [ ] |

## 3. Quy trình thực hiện Test
1. Copy nội dung **Input** vào khung chat.
2. Quan sát OpenClaw (AI) phản hồi.
3. Đối chiếu với **Kết quả mong đợi**.
4. Cập nhật cột **Trạng thái** (Pass/Fail).
