# Workflow Quản lý Dữ liệu Thư mục VNPT trên Google Drive

## 🎯 Mục tiêu
Tự động hóa việc phân loại và lưu trữ tài liệu vào Google Drive mà không cần người dùng chỉ dẫn chi tiết đường dẫn.

## 📂 Cấu trúc Thư mục Chuẩn
- **Root**: `VNPT` (ID lưu trong `vnpt_drive_structure.json`)
- **Nhánh 1**: `Xa Phuong` $\rightarrow$ `{Tên Xã/Phường}` (Ví dụ: Xã Tân Châu)
- **Nhánh 2**: `So Nganh` $\rightarrow$ `{Tên Sở/Ngành}` (Ví dụ: Sở Y Tế)

## 🛠 Quy trình Thao tác Tự động

Khi Anh Bình gửi một file và yêu cầu lưu (ví dụ: "Lưu vào Xã Tân Châu" hoặc "Lưu vào Sở Y Tế"):

1. **Phân tích yêu cầu**: 
   - Nhận diện từ khóa để chọn nhánh:
     - Nếu chứa "Xã" hoặc "Phường" $\rightarrow$ Chọn nhánh `Xa Phuong`.
     - Nếu chứa "Sở" hoặc "Ngành" $\rightarrow$ Chọn nhánh `So Nganh`.
   - Trích xuất tên đơn vị cụ thể (ví dụ: `Tan Chau`, `Y Te`).

2. **Tra cứu ID**: 
   - Đọc file `vnpt_drive_structure.json` để lấy ID của nhánh tương ứng (`Xa Phuong` hoặc `So Nganh`).

3. **Kiểm tra/Tạo Thư mục Đích**:
   - Truy cập vào thư mục nhánh.
   - Tìm kiếm thư mục có tên `{Tên đơn vị}`.
   - **Nếu tìm thấy**: Lấy ID thư mục đó.
   - **Nếu KHÔNG tìm thấy**: 
     - Tạo thư mục mới $\rightarrow$ Lưu ID mới vào `dynamic_folders` trong `vnpt_drive_structure.json` để dùng cho lần sau.
     - Lấy ID vừa tạo.

4. **Thực hiện Upload**:
   - Upload file vào ID cuối cùng.


## 📝 Ghi chú Kỹ thuật (API Gateway)
- **Base URL**: `https://gateway.maton.ai/google-drive/drive/v3/`
- **Authentication**: Sử dụng `MATON_API_KEY`.
- **MimeType Folder**: `application/vnd.google-apps.folder`.

## 🚀 Ví dụ Kịch bản
**User**: "Gửi file `bao-cao.pdf`, lưu vào Xã Tân Châu nhé."
**Agent**: 
- Check folder `Xa Phuong` $\rightarrow$ không thấy `Xã Tân Châu`.
- Tạo folder `Xã Tân Châu` $\rightarrow$ nhận ID `ABC-123`.
- Upload `bao-cao.pdf` vào `ABC-123`.
- **Reply**: "Mình đã tạo thư mục Xã Tân Châu và upload file báo-cao.pdf vào đó cho anh rồi ạ! 💡"
