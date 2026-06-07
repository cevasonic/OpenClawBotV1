#!/bin/bash
# Script to run thuvienphapluat scraper and send results directly to Telegram

# Paths
WORKSPACE_DIR="/root/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE_DIR/skills/thuvien/scripts"
PYTHON_BIN="/usr/bin/python3"
BOT_TOKEN="8293379786:AAF7-_kLdnv9Qvb6It_RsRp3e-Bfe4MDoMY"
CHAT_ID="703003678"

# Run the python script and capture output
cd "$WORKSPACE_DIR"
OUTPUT=$("$PYTHON_BIN" "$SCRIPTS_DIR/scrape_latest.py" 2>&1)
EXIT_CODE=$?

# If there is an exit code error, we should report it to Telegram
if [ $EXIT_CODE -ne 0 ]; then
  ERROR_MSG="⚠️ *Lỗi khi chạy quét Thư viện Pháp luật:*\n\n\`\`\`\n$OUTPUT\n\`\`\`"
  curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$ERROR_MSG" \
    -d "parse_mode=Markdown" > /dev/null
  exit $EXIT_CODE
fi

# Send output to Telegram (using urlencode for plain text formatting to avoid markdown issues)
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
  --data-urlencode "chat_id=$CHAT_ID" \
  --data-urlencode "text=$OUTPUT" > /dev/null

echo "Cron check completed and sent to Telegram successfully."
