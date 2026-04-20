#!/bin/bash
# Notion Integration Setup Step-by-Step
# Follow these instructions carefully

set -e

echo "============================================"
echo "🔧 NOTION INTEGRATION SETUP - STEP BY STEP"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check API Key
echo "📋 STEP 1: Check MATON_API_KEY"
echo "----------------------------------------"
if [ -z "$MATON_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  MATON_API_KEY chưa được set.${NC}"
    echo ""
    echo "Có 2 cách lấy API key:"
    echo ""
    echo "🔵 Cách 1 (Khuyến nghị): Sau khi lấy key từ maton.ai, chạy:"
    echo "   export MATON_API_KEY=\"your-key-here\""
    echo ""
    echo "🔵 Cách 2: Lưu vào file Shell profile (tự động mỗi lần mở terminal):"
    echo "   echo 'export MATON_API_KEY=\"your-key-here\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo ""
    read -p "Bạn đã có MATON_API_KEY chưa? (y/n): " has_key
    if [ "$has_key" = "y" ] || [ "$has_key" = "Y" ]; then
        read -p "Nhập MATON_API_KEY của bạn: " api_key
        export MATON_API_KEY="$api_key"
        echo -e "${GREEN}✅ API key đã được set cho phiên này.${NC}"
        echo ""
    else
        echo -e "${RED}❌ Vui lòng lấy MATON_API_KEY từ https://maton.ai/settings${NC}"
        echo "Sau đó chạy lại script này."
        exit 1
    fi
else
    echo -e "${GREEN}✅ MATON_API_KEY đã được set.${NC}"
    echo "   Value: ${MATON_API_KEY:0:10}..."
    echo ""
fi

# Step 2: Test API key
echo "📋 STEP 2: Verify API key"
echo "----------------------------------------"
echo "Đang kiểm tra API key hợp lệ..."
response=$(python3 -c "
import urllib.request, os, json, sys
key = os.environ.get('MATON_API_KEY')
if not key:
    print('ERROR: MATON_API_KEY not set')
    sys.exit(1)

try:
    req = urllib.request.Request('https://ctrl.maton.ai/connections')
    req.add_header('Authorization', f'Bearer {key}')
    result = json.loads(urllib.request.urlopen(req).read())
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1)

if [ "$response" = "OK" ]; then
    echo -e "${GREEN}✅ API key hợp lệ!${NC}"
    echo ""
else
    echo -e "${RED}❌ API key không hợp lệ hoặc lỗi kết nối.${NC}"
    echo "Chi tiết: $response"
    echo "Vui lòng kiểm tra lại MATON_API_KEY."
    exit 1
fi

# Step 3: Create Notion OAuth connection
echo "📋 STEP 3: Tạo Notion OAuth Connection"
echo "----------------------------------------"
echo "Đang tạo kết nối OAuth với Notion..."
echo ""

response=$(python3 -c "
import urllib.request, os, json, sys
key = os.environ.get('MATON_API_KEY')
if not key:
    print('ERROR: MATON_API_KEY not set')
    sys.exit(1)

data = json.dumps({'app': 'notion'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {key}')
req.add_header('Content-Type', 'application/json')
try:
    result = json.loads(urllib.request.urlopen(req).read())
    print(json.dumps(result))
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1) || true

if echo "$response" | grep -q "connection_id"; then
    connection_id=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['connection']['connection_id'])")
    auth_url=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['connection']['url'])")

    echo -e "${GREEN}✅ OAuth connection đã được tạo!${NC}"
    echo ""
    echo "🔐 BƯỚC TIẾP THEO: Authorize Notion Access"
    echo "----------------------------------------"
    echo ""
    echo "Mở URL này trong trình duyệt để kết nối Notion workspace:"
    echo ""
    echo "  ${YELLOW}$auth_url${NC}"
    echo ""
    echo "📌 Lưu ý:"
    echo "  - URL này chỉ hiệu lực trong vài phút"
    echo "  - Bạn cần đăng nhập Notion và approve quyền truy cập"
    echo "  - Sau khi authorize, bạn sẽ thấy trang 'Authorization Successful'"
    echo ""
    read -p "Đã mở URL và hoàn tất authorize? (y/n khi xong): " done_auth

    if [ "$done_auth" != "y" ] && [ "$done_auth" != "Y" ]; then
        echo "Vui lòng hoàn tất authorization rồi chạy lại script."
        echo "Connection ID: $connection_id"
        exit 0
    fi

    # Verify connection
    echo ""
    echo "Đang xác minh connection..."
    verify=$(python3 -c "
import urllib.request, os, json, sys
key = os.environ.get('MATON_API_KEY')
cid = '$connection_id'
try:
    req = urllib.request.Request(f'https://ctrl.maton.ai/connections/{cid}')
    req.add_header('Authorization', f'Bearer {key}')
    result = json.loads(urllib.request.urlopen(req).read())
    print(result.get('connection', {}).get('status', 'UNKNOWN'))
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1) || true

    if [ "$verify" = "ACTIVE" ]; then
        echo -e "${GREEN}✅ Connection đã được kích hoạt!${NC}"
        echo ""
    else
        echo -e "${YELLOW}⚠️  Connection status: $verify${NC}"
        echo "Có thể cần vài giây để Notion xác nhận. Thử lại sau."
        echo ""
    fi

    # Save config
    echo "📋 STEP 4: Lưu configuration"
    echo "----------------------------------------"
    mkdir -p /root/.openclaw/workspace/config
    cat > /root/.openclaw/workspace/config/notion_config.json <<EOF
{
  "connection_id": "$connection_id",
  "api_key": "*** configured via env ***",
  "setup_date": "$(date -Iseconds)",
  "workspace_url": "https://gateway.maton.ai/notion/v1",
  "status": "active"
}
EOF

    # Also save to environment for current session
    echo "export MATON_API_KEY=\"$MATON_API_KEY\"" >> /root/.openclaw/workspace/config/env.sh
    echo "export NOTION_CONNECTION_ID=\"$connection_id\"" >> /root/.openclaw/workspace/config/env.sh

    echo -e "${GREEN}✅ Configuration đã được lưu!${NC}"
    echo ""
    echo "============================================"
    echo -e "${GREEN}🎉 SETUP HOÀN TẤT!${NC}"
    echo "============================================"
    echo ""
    echo "📁 Files đã tạo:"
    echo "   - config/notion_config.json (configuration)"
    echo "   - config/env.sh (environment variables)"
    echo ""
    echo "🔧 Bước tiếp theo:"
    echo "   1. Tạo 3 Databases trong Notion workspace (xem NOTION_SETUP.md)"
    echo "   2. Lấy Database IDs từ Notion"
    echo "   3. Cập nhật config/notion_config.json với Database IDs"
    echo "   4. Bắt đầu tạo meetings và tasks!"
    echo ""
    echo "📚 Tài liệu chi tiết: NOTION_SETUP.md"
    echo ""

else
    echo -e "${RED}❌ Không thể tạo OAuth connection.${NC}"
    echo "Response: $response"
    echo ""
    echo "Kiểm tra:"
    echo "  1. MATON_API_KEY có hợp lệ không?"
    echo "  2. Network connection?"
    echo ""
    exit 1
fi
