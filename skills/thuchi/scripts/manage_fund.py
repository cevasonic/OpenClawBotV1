#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# manage_fund.py - Deterministic fund management script for OpenClaw

import os
import json
import sys
import re
import datetime

DATA_PATH = "/opt/openclaw/data/fund_management.json"

def init_db():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        default_data = {
            "config": {
                "low_balance_threshold": 300000,
                "report_day": "Friday",
                "report_time": "17:00"
            },
            "current_balance": 0,
            "members": {},
            "income_log": [],
            "expense_log": []
        }
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
        return True
    return False

def load_db():
    init_db()
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def format_vnd(amount):
    return f"{amount:,.0f}đ".replace(",", ".")

def parse_amount(text):
    # Standardize writing: e.g. "85 ngàn" -> "85ngàn"
    text = re.sub(r'\s*(trieu|triệu|tr|ngàn|nghìn|ngan|k)\b', r'\1', text, flags=re.IGNORECASE)
    
    # Match pattern XtrY (e.g. 1tr5)
    match_try = re.search(r'\b(\d+)\s*(?:tr|triệu|trieu)\s*(\d+)\b', text, re.IGNORECASE)
    if match_try:
        tr = int(match_try.group(1))
        le = match_try.group(2)
        scale = 10 ** (6 - len(le))
        amount = tr * 1000000 + int(le) * scale
        return amount

    # Match numbers with optional units
    pattern = r'\b(\d+[\.,]?\d*)\s*(trieu|triệu|tr|ngàn|nghìn|ngan|k)?\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    for match in matches:
        val_str = match.group(1).replace(',', '.')
        
        if val_str.count('.') > 1:
            val_str = val_str.replace('.', '')
        elif val_str.count('.') == 1:
            parts = val_str.split('.')
            if len(parts[1]) == 3 and not match.group(2):
                val_str = val_str.replace('.', '')
                
        try:
            val = float(val_str)
        except ValueError:
            continue
            
        unit = match.group(2)
        if unit:
            unit = unit.lower()
            if unit in ['tr', 'triệu', 'trieu']:
                val *= 1000000
            elif unit in ['k', 'ngàn', 'nghìn', 'ngan']:
                val *= 1000
        
        return int(val)
    return None

def parse_date(text):
    today = datetime.date.today()
    
    if "hôm qua" in text.lower():
        return today - datetime.timedelta(days=1), "hôm qua"
        
    if "hôm nay" in text.lower():
        return today, "hôm nay"
        
    match_thang = re.search(r'(?:ng\xe0y|ngay)\s+(\d+)\s+(?:th\xe1ng|thang)\s+(\d+)', text, re.IGNORECASE)
    if match_thang:
        day = int(match_thang.group(1))
        month = int(match_thang.group(2))
        try:
            d = datetime.date(today.year, month, day)
            return d, f"{day:02d}/{month:02d}"
        except ValueError:
            pass

    match_slash = re.search(r'(?:(?:ng\xe0y|ngay)\s+)?(\d{1,2})[/-](\d{1,2})', text, re.IGNORECASE)
    if match_slash:
        day = int(match_slash.group(1))
        month = int(match_slash.group(2))
        try:
            d = datetime.date(today.year, month, day)
            return d, f"{day:02d}/{month:02d}"
        except ValueError:
            pass
            
    match_day_only = re.search(r'(?:ng\xe0y|ngay)\s+(\d+)\b', text, re.IGNORECASE)
    if match_day_only:
        day = int(match_day_only.group(1))
        try:
            d = datetime.date(today.year, today.month, day)
            return d, f"{day:02d}/{today.month:02d}"
        except ValueError:
            pass
            
    return today, "hôm nay"

def clean_text_for_amount(text):
    text_clean = text
    # 1. ngày DD tháng MM
    text_clean = re.sub(r'(?:ng\xe0y|ngay)\s+\d{1,2}\s+(?:th\xe1ng|thang)\s+\d{1,2}', '', text_clean, flags=re.IGNORECASE)
    # 2. ngày DD/MM or ngày DD-MM
    text_clean = re.sub(r'(?:ng\xe0y|ngay)\s+\d{1,2}[/-]\d{1,2}', '', text_clean, flags=re.IGNORECASE)
    # 3. DD/MM or DD-MM
    text_clean = re.sub(r'\b\d{1,2}[/-]\d{1,2}\b', '', text_clean)
    # 4. ngày DD
    text_clean = re.sub(r'(?:ng\xe0y|ngay)\s+\d{1,2}\b', '', text_clean, flags=re.IGNORECASE)
    # 5. hôm qua / hôm nay
    text_clean = re.sub(r'\b(h\xf4m qua|h\xf4m nay|hôm qua|hôm nay)\b', '', text_clean, flags=re.IGNORECASE)
    return text_clean

def classify_intent(text):
    text_lower = text.lower()
    
    report_keywords = ["báo cáo tuần", "báo cáo quỹ", "tổng kết", "summary", "báo cáo"]
    if any(k in text_lower for k in report_keywords):
        return "report"
        
    balance_keywords = ["quỹ còn bao nhiêu", "số dư", "tồn quỹ", "check quỹ", "quỹ còn", "còn bao nhiêu"]
    if any(k in text_lower for k in balance_keywords):
        return "balance"
        
    income_keywords = ["đóng quỹ", "nộp tiền", "góp quỹ", "bổ sung quỹ"]
    if any(k in text_lower for k in income_keywords):
        return "income"
        
    if any(k in text_lower for k in ["đóng", "nộp", "góp"]):
        expense_indicators = ["ăn sáng", "cà phê", "cafe", "coffee", "ăn trưa", "ăn tối", "chi", "mua", "tiêu", "hết", "tiền điện", "tiền nước", "tiền mạng"]
        if not any(ei in text_lower for ei in expense_indicators):
            return "income"
            
    return "expense"

def extract_income_details(text):
    text_clean = clean_text_for_amount(text)
    amount = parse_amount(text_clean)
    if not amount:
        return None, None
        
    pattern_verb = r'(?:đóng\s+quỹ|nộp\s+tiền|góp\s+quỹ|bổ\s+sung\s+quỹ|đóng|nộp|góp)'
    
    match_full = re.search(r'\b((?:anh|chị|chi|bạn|ban|em)?\s*[A-ZÀ-Ỹa-zà-ỹ][A-Za-zÀ-ỹ\s]{0,20})\s+' + pattern_verb, text, re.IGNORECASE)
    if match_full:
        return match_full.group(1).strip().title(), amount
        
    match_end = re.search(r'(?:-|by|của|cua)\s*([A-Za-zÀ-ỹ\s]+)$', text, re.IGNORECASE)
    if match_end:
        return match_end.group(1).strip().title(), amount
        
    parts = re.split(pattern_verb, text, flags=re.IGNORECASE)
    if len(parts) > 0 and parts[0].strip():
        candidate = parts[0].strip()
        candidate_clean = clean_text_for_amount(candidate)
        candidate_clean = re.sub(r'[,;\-\s]+', ' ', candidate_clean).strip()
        if candidate_clean:
            return candidate_clean.title(), amount
            
    return None, amount

def extract_expense_details(text):
    date_obj, date_display = parse_date(text)
    text_clean = clean_text_for_amount(text)
    amount = parse_amount(text_clean)
    if not amount:
        return None, None, None, None, None
        
    text_lower = text.lower()
    category = "Khác"
    if any(k in text_lower for k in ["sáng", "breakfast"]):
        category = "Ăn sáng"
    elif any(k in text_lower for k in ["cà phê", "cafe", "coffee"]):
        category = "Cà phê"
    elif any(k in text_lower for k in ["trưa", "lunch"]):
        category = "Ăn trưa"
    elif any(k in text_lower for k in ["tối", "dinner"]):
        category = "Ăn tối"
        
    note = text
    # Remove amount match
    try_match = re.search(r'\b(\d+)\s*(?:tr|triệu|trieu)\s*(\d+)\b', note, re.IGNORECASE)
    if try_match:
        note = note.replace(try_match.group(0), "")
    else:
        amount_match = re.search(r'\b(\d+[\.,]?\d*)\s*(trieu|triệu|tr|ngàn|nghìn|ngan|k)?\b', note, re.IGNORECASE)
        if amount_match:
            note = note.replace(amount_match.group(0), "")
            
    note = clean_text_for_amount(note)
    note = re.sub(r'\b(hết|chi|cho|bổ sung|ăn sáng|cà phê|cafe|coffee|ăn trưa|ăn tối|ăn|uống|quỹ|tiền)\b', '', note, flags=re.IGNORECASE)
    note = re.sub(r'[,;\-\s]+', ' ', note).strip()
    
    return amount, category, date_obj, date_display, note

def generate_report(db):
    today = datetime.date.today()
    current_month_str = today.strftime("%Y-%m")
    current_month_display = today.strftime("%m/%Y")
    
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    
    total_month_expense = 0
    categories_total = {
        "Ăn sáng": 0,
        "Cà phê": 0,
        "Ăn trưa": 0,
        "Ăn tối": 0,
        "Khác": 0
    }
    
    for exp in db.get("expense_log", []):
        if exp.get("date", "").startswith(current_month_str):
            amount = exp.get("amount", 0)
            total_month_expense += amount
            cat = exp.get("category", "Khác")
            if cat in categories_total:
                categories_total[cat] += amount
            else:
                categories_total["Khác"] += amount
                
    member_incomes = {}
    for inc in db.get("income_log", []):
        date_part = inc.get("date", "").split(" ")[0]
        if date_part.startswith(current_month_str):
            member = inc.get("member_name", "Ẩn danh")
            amount = inc.get("amount", 0)
            member_incomes[member] = member_incomes.get(member, 0) + amount
            
    lines = []
    lines.append(f"📊 BÁO CÁO QUỸ CƠ QUAN — Tuần [{start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m/%Y')}]")
    lines.append("")
    lines.append(f"💰 Quỹ tồn hiện tại: {format_vnd(db.get('current_balance', 0))}")
    lines.append("")
    lines.append(f"📤 TỔNG CHI THÁNG [{current_month_display}]: {format_vnd(total_month_expense)}")
    lines.append(f"  • Ăn sáng  : {format_vnd(categories_total['Ăn sáng'])}")
    lines.append(f"  • Cà phê   : {format_vnd(categories_total['Cà phê'])}")
    lines.append(f"  • Ăn trưa  : {format_vnd(categories_total['Ăn trưa'])}")
    lines.append(f"  • Ăn tối   : {format_vnd(categories_total['Ăn tối'])}")
    lines.append(f"  • Khác     : {format_vnd(categories_total['Khác'])}")
    lines.append("")
    lines.append(f"📥 ĐÓNG QUỸ THÁNG [{current_month_display}]:")
    
    if member_incomes:
        for member, amount in member_incomes.items():
            lines.append(f"  • {member}    : {format_vnd(amount)}")
    else:
        lines.append("  (Chưa có thành viên nào đóng quỹ tháng này)")
        
    lines.append("")
    lines.append("---")
    lines.append("Báo cáo tự động bởi Openclaw 🐾")
    
    return "\n".join(lines)

def process_message(text):
    if not text or not text.strip():
        db = load_db()
        return f"Quỹ tồn hiện tại: {format_vnd(db.get('current_balance', 0))} anh ơi."
        
    is_new = init_db()
    db = load_db()
    
    # Check if database is empty and notify user (can prepend if database was just created)
    bootstrap_msg = ""
    if is_new:
        bootstrap_msg = "Em vừa khởi tạo file quỹ mới. Anh bắt đầu nhập liệu được rồi nhé!\n"
            
    intent = classify_intent(text)
    
    if intent == "report":
        return bootstrap_msg + generate_report(db)
        
    elif intent == "balance":
        return bootstrap_msg + f"Quỹ tồn hiện tại: {format_vnd(db.get('current_balance', 0))} anh ơi."
        
    elif intent == "income":
        member, amount = extract_income_details(text)
        if not amount:
            return bootstrap_msg + "Anh Bình ơi, em không nhận diện được số tiền đóng quỹ. Anh nhắn rõ số tiền giúp em nhé!"
        if not member:
            return bootstrap_msg + f"Anh Bình ơi, ai đóng {format_vnd(amount)} vậy anh? Nhắn em tên người đóng nhé."
            
        # Update balance
        db["current_balance"] = db.get("current_balance", 0) + amount
        # Update members
        if "members" not in db:
            db["members"] = {}
        db["members"][member] = db["members"].get(member, 0) + amount
        # Log income
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.setdefault("income_log", []).append({
            "date": timestamp,
            "member_name": member,
            "amount": amount
        })
        save_db(db)
        
        return bootstrap_msg + f"✅ {member} đóng {format_vnd(amount)}. Quỹ tồn: {format_vnd(db['current_balance'])}"
        
    elif intent == "expense":
        amount, category, date_obj, date_display, note = extract_expense_details(text)
        if not amount:
            return bootstrap_msg + "Anh Bình ơi, em không nhận diện được số tiền chi tiêu. Anh nhắn rõ số tiền giúp em nhé!"
            
        # Update balance
        db["current_balance"] = db.get("current_balance", 0) - amount
        # Log expense
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.setdefault("expense_log", []).append({
            "date": date_obj.strftime("%Y-%m-%d"),
            "created_at": created_at,
            "category": category,
            "amount": amount,
            "note": note
        })
        save_db(db)
        
        date_str = f" ({date_display})" if date_display else ""
        response = f"✅ Chi {category.lower()} {format_vnd(amount)}{date_str}. Quỹ tồn: {format_vnd(db['current_balance'])}"
        
        # Check warning threshold
        if db["current_balance"] < db.get("config", {}).get("low_balance_threshold", 300000):
            response += "\n⚠️ Anh Bình ơi, quỹ còn dưới 300k, anh nhớ nhắc mọi người chuẩn bị đóng quỹ nhé!"
            
        return bootstrap_msg + response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        res = process_message(query)
        if res:
            print(res)
    else:
        db = load_db()
        print(f"Quỹ tồn hiện tại: {format_vnd(db.get('current_balance', 0))} anh ơi.")
