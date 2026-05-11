# Kịch bản Kiểm thử Skill conkien-tracking

| Mã | Tên kịch bản | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Output) | Trạng thái |
|:---|:---|:---|:---|:---|
| **TC-01** | Lưu file đơn lẻ vào Xã/Phường | Forward `hop-dong.pdf` + chat: "Lưu vào Xã Tân Châu" | 1. Tạo folder "Xã Tân Châu" (nếu chưa có). <br> 2. Upload file. <br> 3. Cập nhật Notion. <br> 4. Phản hồi: "Mình đã lưu file... vào **OneDrive**... [Link]". <br> **Yêu cầu:** Không được mở file (`view_file`). | ⚪ |
| **TC-02** | Lưu file vào Sở/Ngành | Forward `ke-hoach.xlsx` + chat: "Lưu vào Sở Y Tế" | 1. Nhận diện nhánh `So Nganh`. <br> 2. Upload file vào folder "Sở Y Tế". <br> 3. Cập nhật Notion. <br> 4. Phản hồi chứa từ khóa **OneDrive**. | ⚪ |
| **TC-03** | Xử lý trùng tên (Versioning) | Forward `bao-cao.pdf` (đã tồn tại) + chat: "Lưu vào Xã Tân Châu" | 1. Tự động đổi tên thành `bao-cao_v2.pdf`. <br> 2. Upload lên OneDrive. <br> 3. Phản hồi xác nhận đã lưu phiên bản mới. | ⚪ |
| **TC-04** | Xử lý Batch Files | Forward cùng lúc 3 file + chat: "Lưu hết vào Camera Tân Phú" | 1. Map đúng đơn vị. <br> 2. Upload cả 3 file. <br> 3. Cập nhật Notion. <br> 4. Phản hồi tổng hợp. <br> **Yêu cầu:** Không đọc nội dung bất kỳ file nào. | ⚪ |
| **TC-05** | Cập nhật tiến độ không file | Chat: "Cập nhật tiến độ Camera Tân Phú: Đã thiết kế xong" | 1. Update trạng thái Notion thành "Thiết kế". <br> 2. Thêm entry nhật ký. <br> 3. Phản hồi xác nhận. | ⚪ |
| **TC-06** | Lưu file Scan/Ảnh (Save without Read) | Forward ảnh biên bản + chat: "Lưu vào Xã Tân Châu" | 1. Upload ảnh trực tiếp lên OneDrive. <br> 2. Cập nhật Notion. <br> 3. **CẤM** chạy OCR hoặc mô tả ảnh. <br> 4. Phản hồi nhẹ nhàng kèm link **OneDrive**. | ⚪ |
| **TC-07** | Gateway Mapping (Aliases) | Forward file + chat: "Lưu vào IOC khánh hậu" | 1. Map "IOC khánh hậu" -> Phường Khánh Hậu. <br> 2. Lưu đúng nhánh. <br> 3. Cập nhật Notion. | ⚪ |
| **TC-08** | Passive Mode (Không ngữ cảnh) | Forward `tai-lieu.pdf` (không chat gì thêm) | 1. **TUYỆT ĐỐI KHÔNG** mở file/đọc nội dung. <br> 2. Phản hồi DUY NHẤT: "Dạ, anh Bình muốn em làm gì với file này trên **OneDrive** ạ?" | ⚪ |
| **TC-09** | Sai Unit/Nhánh | Forward file + chat: "Lưu vào Phòng ABC" | 1. Không map được. <br> 2. Hỏi lại Anh Bình 1 câu duy nhất. | ⚪ |
| **TC-10** | Yêu cầu OCR cụ thể | Forward ảnh + chat: "Đọc nội dung ảnh này" | 1. Chạy OCR trích xuất văn bản. <br> 2. Phản hồi nội dung đã trích xuất cho Anh Bình. | ⚪ |

---
**Ghi chú vận hành:**
- Mọi phản hồi PHẢI có từ "OneDrive".
- Tone phải nhẹ nhàng, thư ký (không dùng "OK", "Xong").
- Kiểm tra link OneDrive có shareable public (hoặc theo cấu quyền) không.
