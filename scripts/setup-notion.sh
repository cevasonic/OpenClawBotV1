#!/bin/bash
# Notion Integration Setup Script
# This script guides you through setting up Notion API integration via Maton

set -e

echo "============================================"
echo "🔧 NOTION INTEGRATION SETUP"
echo "============================================"
echo ""

# Check if MATON_API_KEY exists
if [ -z "$MATON_API_KEY" ]; then
    echo "⚠️  MATON_API_KEY not found in environment."
    echo ""
    echo "📋 Steps to get your API key:"
    echo "1. Go to https://maton.ai/settings"
    echo "2. Sign in or create an account"
    echo "3. Copy your API key"
    echo ""
    read -p "Please enter your MATON_API_KEY: " api_key
    export MATON_API_KEY="$api_key"
    echo ""
    echo "✅ API key set for this session."
    echo "💡 To make it permanent, add to your shell profile:"
    echo "   echo 'export MATON_API_KEY=\"$MATON_API_KEY\"' >> ~/.bashrc"
    echo ""
fi

echo "🔗 Creating Notion OAuth connection..."
echo ""

# Create connection via Maton API
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
" 2>/dev/null || true)

if [ $? -eq 0 ] && echo "$response" | grep -q "connection_id"; then
    connection_id=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['connection']['connection_id'])")
    auth_url=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['connection']['url'])")

    echo "✅ OAuth connection created!"
    echo ""
    echo "🔐 NEXT STEP: Authorize Notion access"
    echo "----------------------------------------"
    echo "Open this URL in your browser to connect your Notion workspace:"
    echo ""
    echo "  $auth_url"
    echo ""
    echo "After authorization, come back and continue setup."
    echo ""
    read -p "Press Enter after you've completed authorization..."
    echo ""

    # Save connection ID to config
    mkdir -p /root/.openclaw/workspace/config
    cat > /root/.openclaw/workspace/config/notion_config.json <<EOF
{
  "connection_id": "$connection_id",
  "api_key": "*** configured ***",
  "setup_date": "$(date -Iseconds)"
}
EOF

    echo "✅ Configuration saved to config/notion_config.json"
    echo ""
    echo "============================================"
    echo "🎉 NOTION SETUP COMPLETE!"
    echo "============================================"
    echo ""
    echo "Next steps:"
    echo "1. Create databases in your Notion workspace (Meetings, Tasks, Notes)"
    echo "2. Get the Database IDs from Notion"
    echo "3. Update config/notion_config.json with database IDs"
    echo ""
    echo "Or run: notion-setup-databases (if available)"
    echo ""
else
    echo "❌ Failed to create OAuth connection."
    echo "Response: $response"
    echo ""
    echo "Please check your MATON_API_KEY and try again."
    exit 1
fi
