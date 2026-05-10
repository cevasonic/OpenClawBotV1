# Báo cáo Lỗi Nghiêm trọng: Hallucination & Vi phạm Protocol

## 1. Mô tả lỗi
Hệ thống OpenClaw trên Zalo liên tục vi phạm quy tắc "Passive Mode". Khi nhận ảnh không kèm lệnh, thay vì chỉ hỏi người dùng, hệ thống tự ý phân tích ảnh chi tiết và sử dụng ngôn ngữ hỗn hợp (Hàn, Nga, Đức, Việt).

## 2. Các triệu chứng (Symptoms)
- Model mô tả phong cách ảnh (Kawaii, Low-poly).
- Dùng từ ngữ lạ: 디지털 (Korean), sercevina (Russian), Herzen (German).
- Bỏ qua các quy tắc trong `SKILL.md`.

## 3. Nguyên nhân dự đoán
- **Orchestrator Level:** Có thể bộ điều hướng của bot đang ép model phải mô tả ảnh.
- **Model Level:** Model đang dùng (có thể là một bản fine-tune hoặc model Vision) có xu hướng tự động giải thích hình ảnh.

## 4. Hành động khẩn cấp
- Cập nhật `conkien-core/SKILL.md` với **NUCLEAR GUARDRAIL**.
- Yêu cầu người dùng kiểm tra cấu trúc mã nguồn nếu lỗi vẫn tiếp diễn.

## 5. Đề xuất can thiệp mã nguồn (Code Intervention)
Cần thêm một tầng lọc (Filter Layer) ở mức code:
```python
if message.has_file and not message.text:
    return "Dạ, anh Bình muốn em làm gì với file này trên OneDrive ạ?"
```
*Lưu ý: Không gửi file sang LLM trong trường hợp này để tiết kiệm Token và tránh lỗi.*
