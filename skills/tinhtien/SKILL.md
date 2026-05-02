---
name: tinhtien
description: Kiểm tra và hiển thị chi tiết credit usage OpenRouter. Sử dụng API Management Key để lấy tổng credit, tổng đã dùng, số còn lại, và breakdown theo model (kèm số requests, prompt/completion tokens, chi phí từng model). Dùng khi người dùng hỏi "xem tiền", "credit", "usage openrouter", "đã xài bao nhiêu", "còn bao nhiêu".
---

# Tinhtiền - OpenRouter Usage Tracker

Kiểm tra số dư và chi tiết usage tài khoản OpenRouter bằng Management Key.

## API Key

Key lưu tại `scripts/config.json` — cập nhật khi cần.

## Scripts

- `scripts/tinhtien.sh` — Script chính, chạy để lấy tổng quan + chi tiết theo model.
- `scripts/config.json` — Lưu Management Key.

## Quy trình

### 1. Lấy tổng quan số dư

```
GET https://openrouter.ai/api/v1/credits
```

→ `total_credits`, `total_usage` → Tính số còn lại.

### 2. Lấy chi tiết theo model (30 ngày gần nhất)

```
GET https://openrouter.ai/api/v1/activity?limit=500
```

Mỗi bản ghi: `model`, `usage`, `requests`, `prompt_tokens`, `completion_tokens`, `reasoning_tokens`, `date`.

📌 **Lưu ý:** Endpoint `/activity` chỉ có 30 ngày gần nhất và trễ ~1-2 ngày.

→ Tổng hợp group by model, hiển thị: Model → Chi phí → % → Requests → Tokens.

### 3. Công thức

- Usage theo model: `sum(usage)` group by `model`
- Tỉ lệ %: `(model_cost / total_cost) * 100`
- Model free (cost = $0) vẫn hiển thị

## Hiển thị

Trình bày với emoji, phân loại free/paid, nhận xét model tốn nhất.
