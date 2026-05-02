## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

## Quản lý phiên bản Con Kiến (Versioning Rules)

### Cấu trúc file
- **Thư mục gốc `Conkien/`:** Chỉ chứa `Conkien.md` — đây là file chính, luôn là bản mới nhất (latest).
- **Thư mục `versions/`:** Lưu toàn bộ lịch sử phiên bản, đặt tên theo mẫu `Conkien_vX.Y.md`.

### Khi có phiên bản mới (ví dụ v1.5)
1. Soạn thảo trực tiếp trên `Conkien/Conkien.md`.
2. Khi hoàn tất, copy file đó vào `versions/` với tên `Conkien_v1.5.md`.
3. Ghi rõ thay đổi ở phần đầu file (mục "Thay đổi chính").

### Quy tắc bất di bất dịch
- Chỉ có một thư mục duy nhất cho dự án Con Kiến: **`Conkien/`** (viết hoa chữ C).
- Không tạo thêm thư mục `conkien/` hay bất kỳ biến thể nào khác.
- File latest luôn là `Conkien.md`, không đặt tên theo version ở thư mục gốc.
