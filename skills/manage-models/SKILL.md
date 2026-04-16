---
name: manage-models
description: Thêm mới, cập nhật hoặc cấu hình mô hình AI (AI models) cho OpenClaw (như từ OpenRouter, OpenAI). Tự động cập nhật các file cấu hình openclaw.json, đăng ký model vào danh sách agent, thiết lập model mặc định và khởi động lại dịch vụ. Dùng khi người dùng yêu cầu "thêm model", "cập nhật api key", "đổi model mặc định".
---

# Cấu hình và Quản lý Models trong OpenClaw

Skill này tự động hóa quy trình thêm mới, cập nhật Provider (ví dụ: OpenRouter) và Model vào hệ thống OpenClaw, đảm bảo đồng bộ trên cả 3 file cấu hình quan trọng.

## Cách sử dụng

Khi Anh Bình yêu cầu thêm hoặc cập nhật model, hãy thu thập các thông tin sau (nếu chưa có):
1. **Provider ID** (ví dụ: `openrouter-step`, `openai`)
2. **API Key** (nếu là provider mới hoặc cần cập nhật)
3. **Model ID** (ví dụ: `stepfun/step-3.5-flash`)
4. **Tên Model** (tùy chọn)
5. **Có muốn đặt làm model mặc định không?**

Sau đó, chạy script Python đã được chuẩn bị sẵn:

```bash
python ~/.openclaw/workspace/skills/manage-models/scripts/update_model.py \
  --provider-id "openrouter-step" \
  --api-key "YOUR_API_KEY" \
  --model-id "stepfun/step-3.5-flash" \
  --model-name "Step 3.5 Flash" \
  --set-primary
```

*(Bỏ qua `--api-key` nếu chỉ thêm model vào provider đã có sẵn. Bỏ qua `--set-primary` nếu không muốn đặt làm mặc định)*

## Các bước tiếp theo (Bắt buộc)

Sau khi chạy script thành công, hãy thực hiện các bước sau để áp dụng cấu hình:

1. **Kiểm tra tính hợp lệ của cấu hình:**
   ```bash
   HOME=/opt/openclaw openclaw config validate
   ```

2. **Khởi động lại dịch vụ OpenClaw:**
   ```bash
   sudo systemctl restart openclaw
   # Hoặc dùng: openclaw gateway restart
   ```

3. **Kiểm tra lại danh sách models đã sẵn sàng:**
   ```bash
   HOME=/opt/openclaw openclaw models list
   ```

## Xử lý sự cố
- Nếu khởi động lại bị lỗi `EADDRINUSE` (cổng 18789 bị chiếm), hãy tìm PID và kill nó:
  ```bash
  ss -lptn 'sport = :18789'
  kill -9 <PID>
  ```
- Kiểm tra log nếu dịch vụ không lên: `journalctl -u openclaw -n 20 --no-pager`