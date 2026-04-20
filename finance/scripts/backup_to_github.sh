#!/bin/bash
# Backup dữ liệu tài chính lên GitHub mỗi ngày

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
FINANCE_DIR="$PROJECT_DIR/finance"
GIT_REPO="https://github.com/cevasonic/OpenClawBotV1.git"

echo "🔄 Đang backup dữ liệu chi tiêu lên GitHub..."

# Kiểm tra xem thư mục finance có dữ liệu không
if [ -z "$(ls -A $FINANCE_DIR/daily 2>/dev/null)" ]; then
    echo "⚠️  Không có dữ liệu chi tiêu nào để backup."
    exit 0
fi

# Commit message với ngày hiện tại
DATE=$(date +%Y-%m-%d)
HOUR=$(date +%H:%M:%S)
COMMIT_MSG="[Finance] Backup chi tiêu ngày $DATE $HOUR"

# Thêm tất cả file finance vào staging
cd "$PROJECT_DIR"
git add finance/

# Commit nếu có thay đổi
if git diff --cached --quiet; then
    echo "✅ Không có thay đổi nào trong dữ liệu chi tiêu."
else
    git commit -m "$COMMIT_MSG"
    git push origin main
    echo "✅ Đã backup dữ liệu chi tiêu lên GitHub."
fi

echo "📊 Dữ liệu đã được lưu tại: $FINANCE_DIR"
echo "🌐 Repository: $GIT_REPO"
