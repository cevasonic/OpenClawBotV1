#!/bin/bash
# cron_report.sh - Run weekly report for thuchi skill and send to Zalo and Telegram

WORKSPACE_DIR="/root/.openclaw/workspace"
PYTHON_BIN="/usr/bin/python3"
OPENCLAW_BIN="/usr/bin/openclaw"

# 1. Generate report
OUTPUT=$("$PYTHON_BIN" "$WORKSPACE_DIR/skills/thuchi/scripts/manage_fund.py" "báo cáo tuần")

# 2. Send via Telegram (CLI)
"$OPENCLAW_BIN" message send --channel telegram --target "703003678" --message "$OUTPUT" > /dev/null 2>&1

# 3. Send via Zalo (zalouser CLI)
"$OPENCLAW_BIN" message send --channel zalouser --target "7462691176396418635" --message "$OUTPUT" > /dev/null 2>&1

echo "Weekly report sent successfully."
