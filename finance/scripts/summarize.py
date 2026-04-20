#!/usr/bin/env python3
"""
Script tổng hợp chi tiêu theo ngày/tuần/tháng/nguồn/mục.
Usage: python summarize.py [--date YYYY-MM-DD | --week YYYY-MM-DD | --month YYYY-MM | --source "Nguồn" | --category "Mục"]
"""

import os
import sys
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).parent.parent.parent
FINANCE_DIR = BASE_DIR / "finance"
DAILY_DIR = FINANCE_DIR / "daily"
SUMMARIES_DIR = FINANCE_DIR / "summaries"
CONFIG_PATH = FINANCE_DIR / "config.yaml"

# Đọc config
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

def load_all_expenses():
    """Đọc tất cả expenses từ các file daily"""
    expenses = []
    for yaml_file in DAILY_DIR.glob("*.yaml"):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data and 'expenses' in data:
                for exp in data['expenses']:
                    exp['_file'] = yaml_file.stem  # Thêm ngày từ filename
                    expenses.append(exp)
    return expenses

def get_date_range_from_week(target_date):
    """Lấy start và end date của tuần chứa target_date (Thứ 2 - Chủ nhật)"""
    start = target_date - timedelta(days=target_date.weekday())  # Thứ 2
    end = start + timedelta(days=6)  # Chủ nhật
    return start, end

def summarize_by_date(target_date):
    """Tổng hợp theo ngày cụ thể"""
    target_str = target_date.strftime('%Y-%m-%d')
    filepath = DAILY_DIR / f"{target_str}.yaml"

    if not filepath.exists():
        print(f"Không có dữ liệu chi tiêu cho ngày {target_str}")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    print(f"\n=== CHI TIÊU NGÀY {target_str} ===")
    print(f"{'Thời gian':<10} {'Mục':<15} {'Số tiền':>12} {'Nguồn':<12}")
    print("-" * 55)
    for exp in sorted(data['expenses'], key=lambda x: x.get('time', '00:00')):
        print(f"{exp.get('time',''):<10} {exp.get('category',''):<15} {exp.get('amount',0):>12,} {exp.get('source',''):<12}")
    print("-" * 55)
    print(f"{'TỔNG':<35} {data.get('total',0):>12,} VNĐ")
    print()
    return data

def summarize_by_week(target_date):
    """Tổng hợp theo tuần chứa target_date"""
    start_date, end_date = get_date_range_from_week(target_date)
    expenses = load_all_expenses()

    # Lọc expenses trong tuần
    week_expenses = []
    for exp in expenses:
        exp_date = datetime.strptime(exp['_file'], '%Y-%m-%d').date()
        if start_date <= exp_date <= end_date:
            week_expenses.append(exp)

    total = sum(e.get('amount', 0) for e in week_expenses)

    print(f"\n=== CHI TIÊU TUẦN {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')} ===")
    print(f"Tổng số khoản chi: {len(week_expenses)}")
    print(f"Tổng chi tiêu: {total:,} VNĐ")
    print()

    # Chi tiết theo ngày trong tuần
    by_day = {}
    for exp in week_expenses:
        day = exp['_file']
        by_day.setdefault(day, []).append(exp)

    for day in sorted(by_day.keys()):
        day_total = sum(e['amount'] for e in by_day[day])
        print(f"  {day}: {day_total:,} VNĐ ({len(by_day[day])} khoản)")
    print()
    return week_expenses

def summarize_by_month(year, month):
    """Tổng hợp theo tháng"""
    expenses = load_all_expenses()

    # Lọc expenses trong tháng
    month_expenses = []
    for exp in expenses:
        exp_date = datetime.strptime(exp['_file'], '%Y-%m-%d').date()
        if exp_date.year == year and exp_date.month == month:
            month_expenses.append(exp)

    total = sum(e.get('amount', 0) for e in month_expenses)

    print(f"\n=== CHI TIÊU THÁNG {month}/{year} ===")
    print(f"Tổng số khoản chi: {len(month_expenses)}")
    print(f"Tổng chi tiêu: {total:,} VNĐ")
    print()

    # Chi tiết theo tuần (cách đơn giản)
    by_week = {}
    for exp in month_expenses:
        exp_date = datetime.strptime(exp['_file'], '%Y-%m-%d').date()
        # Tuần thứ mấy trong tháng (1-4/5)
        week_num = (exp_date.day - 1) // 7 + 1
        week_label = f"Tuần {week_num}"
        by_week.setdefault(week_label, []).append(exp)

    for week in sorted(by_week.keys()):
        week_total = sum(e['amount'] for e in by_week[week])
        print(f"  {week}: {week_total:,} VNĐ ({len(by_week[week])} khoản)")
    print()
    return month_expenses

def summarize_by_source(source_name):
    """Tổng hợp theo nguồn chi phí"""
    expenses = load_all_expenses()
    source_expenses = [e for e in expenses if e.get('source') == source_name]

    total = sum(e.get('amount', 0) for e in source_expenses)

    print(f"\n=== CHI TIÊU THEO NGUỒN '{source_name}' ===")
    print(f"Tổng số khoản chi: {len(source_expenses)}")
    print(f"Tổng chi tiêu: {total:,} VNĐ")
    print()

    # Chi tiết theo mục
    by_category = {}
    for exp in source_expenses:
        cat = exp.get('category', 'Khác')
        by_category.setdefault(cat, []).append(exp)

    for cat in sorted(by_category.keys()):
        cat_total = sum(e['amount'] for e in by_category[cat])
        print(f"  {cat}: {cat_total:,} VNĐ ({len(by_category[cat])} khoản)")
    print()
    return source_expenses

def summarize_by_category(category_name):
    """Tổng hợp theo mục chi phí"""
    expenses = load_all_expenses()
    category_expenses = [e for e in expenses if e.get('category') == category_name]

    total = sum(e.get('amount', 0) for e in category_expenses)

    print(f"\n=== CHI TIÊU THEO MỤC '{category_name}' ===")
    print(f"Tổng số khoản chi: {len(category_expenses)}")
    print(f"Tổng chi tiêu: {total:,} VNĐ")
    print()

    # Chi tiết theo nguồn
    by_source = {}
    for exp in category_expenses:
        src = exp.get('source', 'Khác')
        by_source.setdefault(src, []).append(exp)

    for src in sorted(by_source.keys()):
        src_total = sum(e['amount'] for e in by_source[src])
        print(f"  {src}: {src_total:,} VNĐ ({len(by_source[src])} khoản)")
    print()
    return category_expenses

def save_summary(data, filename):
    """Lưu báo cáo tổng hợp"""
    filepath = SUMMARIES_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print(f"✅ Đã lưu báo cáo: {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Tổng hợp chi tiêu")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--date', help="Ngày cụ thể (YYYY-MM-DD)")
    group.add_argument('--week', help="Tuần chứa ngày này (YYYY-MM-DD)")
    group.add_argument('--month', help="Tháng (YYYY-MM)")
    group.add_argument('--source', help="Nguồn chi phí")
    group.add_argument('--category', help="Mục chi phí")
    parser.add_argument('--save', action='store_true', help="Lưu báo cáo vào file")

    args = parser.parse_args()

    result = None

    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        result = summarize_by_date(target_date)
        if args.save and result:
            save_summary(result, f"summary_{args.date}.yaml")

    elif args.week:
        target_date = datetime.strptime(args.week, "%Y-%m-%d").date()
        result = summarize_by_week(target_date)
        if args.save and result:
            start, end = get_date_range_from_week(target_date)
            save_summary(
                {'week_start': start.strftime('%Y-%m-%d'), 'week_end': end.strftime('%Y-%m-%d'), 'expenses': result},
                f"summary_week_{start.strftime('%Y-%m-%d')}.yaml"
            )

    elif args.month:
        year, month = map(int, args.month.split('-'))
        result = summarize_by_month(year, month)
        if args.save and result:
            save_summary({'month': args.month, 'expenses': result}, f"summary_month_{args.month}.yaml")

    elif args.source:
        result = summarize_by_source(args.source)
        if args.save and result:
            save_summary({'source': args.source, 'expenses': result}, f"summary_source_{args.source.replace(' ', '_')}.yaml")

    elif args.category:
        result = summarize_by_category(args.category)
        if args.save and result:
            save_summary({'category': args.category, 'expenses': result}, f"summary_category_{args.category.replace(' ', '_')}.yaml")

if __name__ == '__main__':
    main()
