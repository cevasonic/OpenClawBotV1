#!/bin/bash
# tinhtien.sh - Check OpenRouter credit usage
# Usage: bash tinhtien.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_KEY=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/config.json'))['api_key'])" 2>/dev/null)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
  echo "❌ Lỗi: API key không tìm thấy trong config.json"
  exit 1
fi

echo "📊 KIỂM TRA CREDIT OPENROUTER"
echo "================================"
echo ""

# 1. Tổng quan
echo "🔍 Lấy tổng quan..."
CREDITS=$(curl -s -H "Authorization: Bearer $API_KEY" "https://openrouter.ai/api/v1/credits")
TOTAL_CREDITS=$(echo "$CREDITS" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['total_credits'])")
TOTAL_USAGE=$(echo "$CREDITS" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['total_usage'])")

python3 << EOF
credits = $TOTAL_CREDITS
usage_val = $TOTAL_USAGE
remaining = credits - usage_val
print(f"💰 Tổng đã nạp:    \${credits}")
print(f"📉 Đã dùng:        \${usage_val:.6f}")
print(f"✅ Còn lại:        \${remaining:.6f}")
EOF
echo ""

# 2. Chi tiết theo model
echo "🔍 Lấy chi tiết theo model..."
RESULT=$(curl -s -H "Authorization: Bearer $API_KEY" "https://openrouter.ai/api/v1/activity?limit=500")

echo "$RESULT" | python3 -c "
import json,sys
from collections import defaultdict

data = json.load(sys.stdin)['data']
models = defaultdict(lambda: {
    'cost': 0, 'requests': 0, 'prompt_tokens': 0,
    'completion_tokens': 0, 'reasoning_tokens': 0
})

for e in data:
    m = e['model']
    models[m]['cost'] += e['usage']
    models[m]['requests'] += e['requests']
    models[m]['prompt_tokens'] += e['prompt_tokens']
    models[m]['completion_tokens'] += e['completion_tokens']
    models[m]['reasoning_tokens'] += e['reasoning_tokens']

total_cost = sum(m['cost'] for m in models.values())
total_usage = $TOTAL_USAGE

# Filter models with >20 requests and group others
filtered_models = {}
other_cost = 0
other_requests = 0

for model, m in models.items():
    if m['requests'] > 20:
        filtered_models[model] = m
    else:
        other_cost += m['cost']
        other_requests += m['requests']

# Add 'Model khác' if there are any models with <=20 requests
if other_requests > 0:
    filtered_models['Model khác'] = {'cost': other_cost, 'requests': other_requests}

# Sort by cost descending
sorted_models = sorted(filtered_models.items(), key=lambda x: -x[1]['cost'])

print('📋 CHI TIẾT THEO MODEL (30 ngày gần nhất)')
print('-' * 40)

for model, m in sorted_models:
    cost = m['cost']
    requests = m['requests']
    pct = (cost / total_cost * 100) if total_cost > 0 else 0
    paid_icon = '💰' if cost > 0 else '🆓'
    model_display = f'{paid_icon} {model}'
    print(model_display)
    print(f'    \${cost:.5f}, {pct:>5.1f}%, {requests:,}')
    print()

print()
print(f'📊 Tổng activity: \${total_cost:.5f}')
diff = total_usage - total_cost
if diff > 0:
    print(f'⚠️  Chênh lệch với credits endpoint: \${diff:.5f} (dữ liệu ngoài 30 ngày)')
" 2>/dev/null