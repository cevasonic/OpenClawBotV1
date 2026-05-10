---
name: conkien-tracking
version: 1.0.0
description: |
  Skill chuyên trách nhận forward file/tin nhắn từ Anh Bình (route từ conkien-core), 
  thực hiện Gateway Mapping (nếu cần), lưu trữ file vào OneDrive theo đúng cấu trúc 
  Section 14 Conkien.md, cập nhật Notion Projects DB (link file, Last Update, nhật ký tiến độ), 
  versioning file và confirm kết quả với tone core.
author: Bình (Quản lý dự án CNTT)
depends_on: ["conkien-core"]
date: 09/05/2026
reference: Conkien.md (Master Plan v1.7), ../conkien-core/SKILL.md v1.1.0
---

# conkien-tracking — Skill Lưu Trữ & Theo Dõi Tiến Độ OpenClaw

## 0. Tuân thủ Karpathy Guidelines (BẮT BUỘC)
Toàn bộ logic của skill này phải tuân thủ nghiêm ngặt Karpathy Guidelines như đã nêu trong `../conkien-core/SKILL.md` Section 0.

**Các nguyên tắc chính luôn áp dụng:**
- **Think Before Acting**: Xác định intent + unit/project mapping (từ conkien-core) trước khi lưu/upload/update.
- **Simplicity First**: Chỉ thực hiện đúng workflow Section 14 + update Notion, không thêm abstraction thừa.
- **Surgical Changes**: Chỉ chạm vào logic lưu trữ và Notion update.
- **Goal-Driven + No Silent Failures**: Luôn confirm rõ ràng hành động đã thực hiện.

**Ràng buộc phản hồi (BẮT BUỘC từ core):** Mọi câu trả lời liên quan đến lưu trữ hoặc hỏi lại về file PHẢI chứa từ khóa **OneDrive**.

## 1. Vai Trò & Trách Nhiệm
conkien-tracking là skill thứ 2 trong kiến trúc multi-skill (Conkien.md Section 4.5 & 5).

**Nhiệm vụ chính:**
1. Nhận context từ conkien-core (intent lưu trữ/cập nhật, unit/project đã map).
2. Thực thi **Workflow Quản lý Dữ liệu Thư mục VNPT trên OneDrive** theo đúng **Section 14 Conkien.md**.
3. Cập nhật **Projects DB** trên Notion (Section 13): Last Update, Link OneDrive, nhật ký tiến độ.
4. Xử lý versioning file (_v2, _v3…), OCR cho file scan/ảnh.
5. Confirm kết quả cho Anh Bình (tone conkien-core).

Skill này **không** tự detect intent ban đầu (conkien-core lo phần routing & mapping).

## 2. Tích hợp với conkien-core
- Luôn được gọi **sau** khi core đã:
  - Xác định intent = lưu trữ / cập nhật tiến độ.
  - Thực hiện Gateway Mapping (Xa Phuong / So Nganh + aliases dự án).
- Tone, quy tắc phản hồi và ràng buộc **OneDrive** phải tuân thủ 100% `../conkien-core/SKILL.md` (Section 2 & 3).
- Nếu core hỏi lại người dùng → skill tracking dừng.

## 3. Workflow Lưu Trữ OneDrive (Theo Section 14 Conkien.md)
Khi nhận file + yêu cầu lưu (ví dụ: “Lưu vào Xã Tân Châu”, “Lưu file này vào IOC khánh hậu”):

1. **Phân tích yêu cầu & Mapping** (dùng output từ core):
   - Nhận diện nhánh: “Xã/Phường” → `Xa Phuong`; “Sở/Ngành/Ban” → `So Nganh`.
2. **Tra cứu ID**:
   - Đọc `shared-references/vnpt_onedrive_structure.json`.
   - Lấy ID nhánh tương ứng.
3. **Kiểm tra/Tạo thư mục**:
   - Tìm thư mục `{Tên đơn vị}` trong nhánh.
   - Nếu chưa có: Tạo mới → cập nhật `dynamic_folders` trong JSON.
4. **Upload file**:
   - Kiểm tra trùng tên → tự động rename `_v2`, `_v3`…
   - Upload vào ID thư mục đích (Base URL: https://gateway.maton.ai/onedrive/v1/, MATON_API_KEY).
   - Ưu tiên OCR cho file scan/ảnh.
5. **Post-upload**: Lấy link shareable.

**Ví dụ confirm:**
> “Mình đã lưu file báo-cao.pdf vào thư mục Xã Tân Châu trên **OneDrive** rồi anh ạ! ✅ Link OneDrive: [link]”

## 4. Cập Nhật Notion & Nhật Ký Tiến Độ (Section 13)
Sau khi lưu file thành công (hoặc chỉ cập nhật tiến độ):

- Tìm project trong **Projects DB** (dựa trên tên/aliases + đơn vị).
- Cập nhật:
  - `Last Update`: timestamp hiện tại.
  - `Link OneDrive`.
  - Thêm entry vào **Nhật ký tiến độ** (Relation/Linked DB): ngày + mô tả từ tin nhắn + link file.
- Nếu tin nhắn có thông tin trạng thái → update theo danh sách cố định (Sơ Khai → Nghiệm thu).

## 5. Xử Lý Đặc Biệt & Quy Tắc Vận Hành (Section 12)
- **Batch files**: Xử lý tất cả, confirm tổng hợp.
- **File scan/ảnh**: OCR + lưu text metadata.
- **File trùng tên**: Tự động versioning.
- **Excel/Word**: Lưu nguyên bản (chỉnh sửa thuộc conkien-admin).
- **Voice note**: Chưa hỗ trợ → core sẽ nhắc gõ text.
- **Không silent failure**: Luôn confirm link **OneDrive** và hành động.
- Mỗi dự án chỉ thuộc **1 đơn vị duy nhất**.

## 6. Workflow Chuẩn Mỗi Lượt Xử Lý
1. Nhận context từ core (intent + mapping).
2. Thực hiện lưu OneDrive (Section 14).
3. Cập nhật Notion (Section 13).
4. Ghi log hoạt động.
5. Trả confirm tone chuẩn + link **OneDrive**.

## 7. Test Cases (≥90% pass)
**TC-01:** Forward file + “Lưu vào Xã Tân Châu” → Tạo folder nếu cần → upload → update Notion → confirm **OneDrive**.  
**TC-02:** “Lưu file này vào IOC khánh hậu” → Map đúng → lưu + log tiến độ.  
**TC-03:** Batch 3 files → Xử lý tất cả + confirm tổng hợp.  
**TC-04:** File scan PDF → OCR + lưu + note trong log.  
**TC-05:** Tên file trùng → Auto rename _v2.  
**TC-06:** “Cập nhật tiến độ Camera Tân Phú: Đã thiết kế” → Chỉ update nhật ký Notion.  
**TC-07:** Lưu vào Sở Y Tế → Xử lý nhánh So Nganh đúng.

## 8. References
- Master Plan: `Conkien.md` (Section 4.5, 5, 12, 13, 14, 15)
- conkien-core (tone, gateway mapping, routing, **OneDrive** rule): `../conkien-core/SKILL.md`
- Cấu trúc OneDrive: `shared-references/vnpt_onedrive_structure.json`
- Danh sách đơn vị & aliases: `shared-references/units-list.md`, `shared-references/aliases.md`
- Notion: Units DB & Projects DB (Section 13)

---

**File này là nguồn sự thật cho conkien-tracking.** Mọi thay đổi lớn phải update Conkien.md trước, sau đó mới chỉnh skill này.