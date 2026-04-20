#!/usr/bin/env python3
"""
Script thêm chi tiêu mới vào hệ thống theo dõi tài chính.
Usage: python add_expense.py --date 2025-06-17 --time "12:30" --category "Ăn trưa" --amount 165000 --source "Cơ quan" --note "Nhà hàng ABC"
"""

import os
import sys
import argparse
from datetime import datetime, date
import yaml
from pathlib import Path

# Đọc config
BASE_DIR = Path(__file__).parent.parent.parent
FINANCE_DIR = BASE_DIR / "finance"
CONFIG_PATH = FINANCE_DIR / "config.yaml"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

DAILY_DIR = FINANCE_DIR / config['paths']['daily']

def load_daily_file(filepath):
    """Đọc file daily, tạo mới nếu chưa tồn tại"""
    if not filepath.exists():
        return {
            'date': filepath.stem,
            'expenses': [],
            'total': 0
        }
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if data is None:
            return {'date': filepath.stem, 'expenses': [], 'total': 0}
        # Đảm bảo có total
        if 'total' not in data:
            data['total'] = sum(e.get('amount', 0) for e in data.get('expenses', []))
        return data

def save_daily_file(filepath, data):
    """Lưu file daily"""
    # Sắp xếp expenses theo thời gian
    data['expenses'] = sorted(data['expenses'], key=lambda x: x.get('time', '00:00'))
    # Tính lại total
    data['total'] = sum(e.get('amount', 0) for e in data['expenses'])

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def add_expense(args):
    """Thêm một khoản chi mới"""
    # Validate date
    try:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError:
        print(f"Lỗi: Ngày không hợp lệ. Dùng format YYYY-MM-DD (ví dụ: 2025-06-17)")
        sys.exit(1)

    # Validate amount
    if args.amount <= 0:
        print("Lỗi: Số tiền phải lớn hơn 0")
        sys.exit(1)

    # Validate category and source (cho phép thêm mới)
    valid_categories = config['categories']
    if args.category not in valid_categories:
        print(f"Cảnh báo: Mục '{args.category}' chưa có trong danh sách mặc định. Tự động thêm...")
        valid_categories.append(args.category)
        config['categories'] = valid_categories
        # Ghi lại config
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        print(f"✅ Đã thêm mục '{args.category}' vào config.yaml")

    valid_sources = config['sources']
    if args.source not in valid_sources:
        print(f"Cảnh báo: Nguồn '{args.source}' chưa có trong danh sách mặc định. Tự động thêm...")
        valid_sources.append(args.source)
        config['sources'] = valid_sources
        # Ghi lại config
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        print(f"✅ Đã thêm nguồn '{args.source}' vào config.yaml")

    # Tạo file path
    filename = f"{target_date.strftime('%Y-%m-%d')}.yaml"
    filepath = DAILY_DIR / filename

    # Đọc data hiện tại
    data = load_daily_file(filepath)

    # Tạo expense entry
    expense = {
        'time': args.time,
        'category': args.category,
        'amount': args.amount,
        'source': args.source
    }
    if args.note:
        expense['note'] = args.note

    # Thêm vào danh sách
    data['expenses'].append(expense)

    # Lưu file
    save_daily_file(filepath, data)

    print(f"✅ Đã thêm chi tiêu vào {filename}")
    print(f"   Thời gian: {args.time}")
    print(f"   Mục: {args.category}")
    print(f"   Số tiền: {args.amount:,} VNĐ")
    print(f"   Nguồn: {args.source}")
    print(f"   Tổng ngày: {data['total']:,} VNĐ")

def main():
    parser = argparse.ArgumentParser(description="Thêm chi tiêu mới")
    parser.add_argument('--date', required=True, help="Ngày chi (YYYY-MM-DD)")
    parser.add_argument('--time', required=True, help="Thời gian (HH:MM)")
    parser.add_argument('--category', required=True, help="Mục chi phí")
    parser.add_argument('--amount', type=int, required=True, help="Số tiền (VNĐ)")
    parser.add_argument('--source', required=True, help="Nguồn chi phí")
    parser.add_argument('--note', help="Ghi chú (tùy chọn)")

    args = parser.parse_args()
    add_expense(args)

if __name__ == '__main__':
    main()
