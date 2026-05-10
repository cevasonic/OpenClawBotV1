# Kịch bản Kiểm thử Skill conkien-tracking

| Mã | Tên kịch bản | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Output) | Trạng thái |
|:---|:---|:---|:---|:---|
| **TC-01** | Lưu file đơn lẻ vào Xã/Phường | Forward `hop-dong.pdf` + chat: "Lưu vào Xã Tân Châu" | 1. Tạo folder "Xã Tân Châu" (nếu chưa có) trong nhánh `Xa Phuong`. <br> 2. Upload file lên OneDrive. <br> 3. Cập nhật Notion Projects DB: Last Update, Link OneDrive. <br> 4. Phản hồi: "Mình đã lưu file... vào **OneDrive**... [Link]" | ⚪ |
| **TC-02** | Lưu file vào Sở/Ngành | Forward `ke-hoach.xlsx` + chat: "Lưu vào Sở Y Tế" | 1. Nhận diện nhánh `So Nganh`. <br> 2. Upload file vào folder "Sở Y Tế". <br> 3. Cập nhật Notion. <br> 4. Phản hồi chứa từ khóa **OneDrive**. | ⚪ |
| **TC-03** | Xử lý trùng tên (Versioning) | Forward `bao-cao.pdf` (đã tồn tại) + chat: "Lưu vào Xã Tân Châu" | 1. Tự động đổi tên thành `bao-cao_v2.pdf`. <br> 2. Upload lên OneDrive. <br> 3. Phản hồi xác nhận đã lưu phiên bản mới. | ⚪ |
| **TC-04** | Xử lý Batch Files | Forward cùng lúc 3 file + chat: "Lưu hết vào Camera Tân Phú" | 1. Map "Camera Tân Phú" -> Đơn vị: Xã Tân Phú. <br> 2. Upload cả 3 file. <br> 3. Cập nhật 1 lần vào nhật ký Notion. <br> 4. Phản hồi tổng hợp. | ⚪ |
| **TC-05** | Cập nhật tiến độ không file | Chat: "Cập nhật tiến độ Camera Tân Phú: Đã thiết kế xong" | 1. Tìm project "Camera" tại Xã Tân Phú. <br> 2. Update trạng thái Notion thành "Thiết kế". <br> 3. Thêm entry vào nhật ký tiến độ. <br> 4. Phản hồi xác nhận. | ⚪ |
| **TC-06** | Xử lý file Scan/Ảnh (OCR) | Forward ảnh chụp biên bản + chat: "Lưu vào Xã Tân Châu" | 1. OCR trích xuất text. <br> 2. Upload ảnh lên OneDrive. <br> 3. Lưu text OCR vào metadata/note trong Notion. <br> 4. Phản hồi kèm xác nhận OCR. | ⚪ |
| **TC-07** | Gateway Mapping (Aliases) | Forward file + chat: "Lưu vào IOC khánh hậu" | 1. Map "IOC khánh hậu" -> Unit: Phường Khánh Hậu. <br> 2. Lưu vào nhánh `Xa Phuong/Phường Khánh Hậu`. <br> 3. Cập nhật Notion. | ⚪ |
| **TC-08** | File không có ngữ cảnh (Passive Mode) | Forward `tai-lieu.pdf` (không chat gì thêm) | 1. **KHÔNG** xử lý file. <br> 2. Phản hồi đúng câu mẫu: "Dạ, anh Bình muốn em làm gì với file này trên **OneDrive** ạ?" | ⚪ |
| **TC-09** | Sai Unit/Nhánh | Forward file + chat: "Lưu vào Phòng ABC" (không tồn tại) | 1. Core nhận diện không map được. <br> 2. Hỏi lại Anh Bình để làm rõ đơn vị. | ⚪ |

---
**Ghi chú vận hành:**
- Mọi phản hồi PHẢI có từ "OneDrive".
- Tone phải nhẹ nhàng, thư ký (không dùng "OK", "Xong").
- Kiểm tra link OneDrive có shareable public (hoặc theo cấu quyền) không.
