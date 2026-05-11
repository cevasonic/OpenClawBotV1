---
name: conkien-tracking
version: 1.2.0
description: |
  Skill chuyên trách nhận forward file/tin nhắn từ Anh Bình (route từ conkien-core), 
  thực hiện Gateway Mapping (nếu cần), lưu trữ file vào OneDrive theo đúng cấu trúc 
  Section 14 Conkien.md, versioning file và confirm kết quả với tone core.
  (Lưu ý: Tác vụ cập nhật Notion đã được tách riêng và tạm dừng theo yêu cầu v1.10).
author: Bình (Quản lý dự án CNTT)
depends_on: ["conkien-core"]
date: 10/05/2026
reference: Conkien.md (Master Plan v1.10), ../conkien-core/SKILL.md v1.2.0
---

# conkien-tracking — Skill Lưu Trữ & Theo Dõi Tiến Độ OpenClaw

## 0. Tuân thủ Karpathy Guidelines (BẮT BUỘC)
Toàn bộ logic của skill này phải tuân thủ nghiêm ngặt Karpathy Guidelines như đã nêu trong `../conkien-core/SKILL.md` Section 0.

**Các nguyên tắc chính luôn áp dụng:**
- **Think Before Acting**: Xác định intent + unit/project mapping (từ conkien-core) trước khi lưu/upload/update.
- **Simplicity First**: Chỉ thực hiện đúng workflow Section 14, không thêm abstraction thừa.
- **Surgical Changes**: Chỉ chạm vào logic lưu trữ OneDrive.
- **Goal-Driven + No Silent Failures**: Luôn confirm rõ ràng hành động đã thực hiện.

**Ràng buộc phản hồi (BẮT BUỘC từ core):** Mọi câu trả lời liên quan đến lưu trữ hoặc hỏi lại về file PHẢI chứa từ khóa **OneDrive**.

## 1. Vai Trò & Trách Nhiệm
conkien-tracking là skill thứ 2 trong kiến trúc multi-skill (Conkien.md Section 4.5 & 5).

**Nhiệm vụ chính:**
1. Nhận context từ conkien-core (intent lưu trữ/cập nhật, unit/project đã map).
2. Thực thi **Workflow Quản lý Dữ liệu Thư mục VNPT trên OneDrive** theo đúng **Section 14 Conkien.md**.
3. Xử lý versioning file (_v2, _v3...). Tự động loại bỏ UUID hệ thống (---uuid) để giữ tên gốc của Anh Bình.
4. **QUY TẮC "LƯU KHÔNG ĐỌC":** Tuyệt đối không sử dụng tool đọc file (`view_file`, `read_url_content`) khi chỉ thực hiện lệnh lưu. Chỉ sử dụng thông tin meta (tên file) từ hệ thống.
5. OCR cho file scan/ảnh: **CHỈ** thực hiện khi có yêu cầu phân tích/đọc cụ thể từ Anh Bình.
6. Confirm kết quả cho Anh Bình (tone conkien-core).
7. **TÁCH BIỆT NOTION:** Không tự động cập nhật Notion khi lưu file. Nhiệm vụ này sẽ được xử lý riêng.

Skill này **không** tự detect intent ban đầu (conkien-core lo phần routing & mapping).

## 2. Tích hợp với conkien-core
- Luôn được gọi **sau** khi core đã:
  - Xác định intent = lưu trữ / cập nhật tiến độ.
  - Thực hiện Gateway Mapping (Xa Phuong / So Nganh + aliases dự án).
- Tone, quy tắc phản hồi và ràng buộc **OneDrive** phải tuân thủ 100% `../conkien-core/SKILL.md` (Section 2 & 3).
- Nếu core hỏi lại người dùng → skill tracking dừng.

## 3. Workflow Lưu Trữ OneDrive (TỐI ƯU HÓA v1.2.0)
Để đạt hiệu suất cao nhất và giảm độ trễ, OpenClaw thực hiện quy trình **Script-First**:

1. **BẮT BUỘC - SUY NGHĨ TÁCH BIỆT (Thinking Step)**:
   - Trước khi gọi lệnh, phải tự trả lời: "Đơn vị là gì? Dự án là gì?"
   - Ví dụ: "Camera Nhựt Tảo" -> Đơn vị = Nhựt Tảo, Dự án = Camera.
   - Ví dụ: "IOC Suối Đá" -> Đơn vị = Suối Đá, Dự án = IOC.
   - **KHÔNG ĐƯỢC** gộp chung tên dự án vào tên đơn vị.

2. **Phân tích yêu cầu (Sử dụng kiến thức có sẵn)**:
   - **Nhánh Xa Phuong**: Nếu tin nhắn chứa "Xã", "Phường", hoặc địa danh xã/phường.
   - **Nhánh So Nganh**: Nếu tin nhắn chứa "Sở", "Ngành", "Ban".
   - **Tên đơn vị**: Trích xuất tên địa danh (ví dụ: "Nhựt Tảo", "Tân Châu").
   - **Tên dự án (Subfolder)**: Trích xuất các từ khóa chuyên môn (ví dụ: "Camera", "IOC", "Ấp thông minh").

3. **Thực thi THAY VÌ Tra cứu (Script-First)**:
   - **TUYỆT ĐỐI KHÔNG** gọi tool `view_file` để đọc `vnpt_onedrive_structure.json`.
   - Gọi trực tiếp script: `python3 skills/conkien-tracking/onedrive_helper.py --file [path] --unit [unit] --branch [branch] --project [project]`
   - Script này tự động tra cứu/tạo folder đơn vị và subfolder dự án.

4. **Confirm kết quả**:
   - Lấy link OneDrive từ output JSON của script.
   - Trả lời Anh Bình kèm từ khóa **OneDrive**.

**Ví dụ lệnh tối ưu:**
- Yêu cầu: "Lưu vào Camera Nhựt Tảo"
- Trích xuất: `--unit "Xã Nhựt Tảo" --branch "Xa Phuong" --project "Camera"`
- Lệnh: `run_command(CommandLine="python3 skills/conkien-tracking/onedrive_helper.py --file /tmp/file.pdf --unit 'Xã Nhựt Tảo' --branch Xa Phuong --project 'Camera'", ...)`

## 4. [TẠM DỪNG] Cập Nhật Notion & Nhật Ký Tiến Độ
*(Phần này hiện đã được tạm dừng theo yêu cầu của Anh Bình để tách bạch việc lưu trữ và cập nhật thông tin).*

## 5. Xử Lý Đặc Biệt & Quy Tắc Vận Hành (Section 12)
- **Batch files**: Xử lý tất cả, confirm tổng hợp, không đọc nội dung từng file.
- **File scan/ảnh**: Lưu nguyên bản, không tự động OCR.
- **File trùng tên**: Tự động thêm _v2, _v3... vào cuối tên file.
- **Excel/Word**: Lưu nguyên bản (chỉnh sửa thuộc conkien-admin).
- **Không silent failure**: Luôn confirm link **OneDrive** và hành động.
- Mỗi dự án chỉ thuộc **1 đơn vị duy nhất**.

## 6. Workflow Chuẩn Mỗi Lượt Xử Lý
1. Nhận context từ core (intent + mapping).
2. Thực hiện lưu OneDrive (Section 14).
3. Ghi log hoạt động.
4. Trả confirm tone chuẩn + link **OneDrive**.

## 7. Test Cases (≥90% pass)
**TC-01:** Forward file + “Lưu vào Xã Tân Châu” → Tạo folder nếu cần → upload → confirm **OneDrive**.  
**TC-02:** “Lưu file này vào IOC khánh hậu” → Map đúng → lưu + log tiến độ.  
**TC-03:** Batch 3 files → Xử lý tất cả + confirm tổng hợp.  
**TC-04:** File scan PDF → OCR + lưu + note trong log.  
**TC-05:** Tên file trùng → Auto rename thành _v2, _v3...  
**TC-06:** “Cập nhật tiến độ Camera Tân Phú: Đã thiết kế” → Chỉ update nhật ký Notion.  
**TC-07:** Lưu vào Sở Y Tế → Xử lý nhánh So Nganh đúng.

## 8. References & Fast Lookup
- **OneDrive Root ID:** `C64D3600679F709F!32557` (VNPT)
- **Branch IDs:**
  - `Xa Phuong`: `C64D3600679F709F!sd6584d94bb5b4448b405414e4635c03b`
  - `So Nganh`: `C64D3600679F709F!s32028851411247148a471ed0f86ee74d`
- Master Plan: `Conkien.md` (v1.10)
- Config: `shared-references/vnpt_onedrive_structure.json` (Script handles this).
- Aliases: `shared-references/aliases.md` (Core mapping).

---

**File này là nguồn sự thật cho conkien-tracking.** Mọi thay đổi lớn phải update Conkien.md trước, sau đó mới chỉnh skill này.