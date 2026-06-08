#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# manage_fund.py - Deterministic fund management script for OpenClaw

import os
import json
import sys
import re
import datetime
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../data/fund_management.json"))

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
    text = unicodedata.normalize('NFC', text)
    today = datetime.date.today()
    
    if "hôm qua" in text.lower():
        return today - datetime.timedelta(days=1), "hôm qua"
        
    if "hôm nay" in text.lower():
        return today, "hôm nay"
        
    # Match DD tháng MM năm YYYY / DD tháng MM YYYY / DD tháng MM
    match_thang = re.search(r'(?:ngày|ngay)\s+(\d+)\s+(?:tháng|thang)\s+(\d+)(?:\s+(?:năm|nam)?\s*(\d{2,4}))?', text, re.IGNORECASE)
    if match_thang:
        day = int(match_thang.group(1))
        month = int(match_thang.group(2))
        year = today.year
        if match_thang.group(3):
            y_str = match_thang.group(3)
            if len(y_str) == 2:
                year = 2000 + int(y_str)
            else:
                year = int(y_str)
        try:
            d = datetime.date(year, month, day)
            if year == today.year:
                display = f"{day:02d}/{month:02d}"
            else:
                display = f"{day:02d}/{month:02d}/{year}"
            return d, display
        except ValueError:
            pass

    # Match DD/MM/YYYY or DD-MM-YYYY
    match_slash = re.search(r'(?:(?:ngày|ngay)\s+)?(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?', text, re.IGNORECASE)
    if match_slash:
        day = int(match_slash.group(1))
        month = int(match_slash.group(2))
        year = today.year
        if match_slash.group(3):
            y_str = match_slash.group(3)
            if len(y_str) == 2:
                year = 2000 + int(y_str)
            else:
                year = int(y_str)
        try:
            d = datetime.date(year, month, day)
            if year == today.year:
                display = f"{day:02d}/{month:02d}"
            else:
                display = f"{day:02d}/{month:02d}/{year}"
            return d, display
        except ValueError:
            pass
            
    match_day_only = re.search(r'(?:ngày|ngay)\s+(\d+)\b', text, re.IGNORECASE)
    if match_day_only:
        day = int(match_day_only.group(1))
        try:
            d = datetime.date(today.year, today.month, day)
            return d, f"{day:02d}/{today.month:02d}"
        except ValueError:
            pass
            
    return None, None

def clean_text_for_amount(text):
    text = unicodedata.normalize('NFC', text)
    text_clean = text
    # 1. ngày DD tháng MM năm YYYY / ngày DD tháng MM YYYY / ngày DD tháng MM
    text_clean = re.sub(
        r'(?:ngày|ngay)\s+\d{1,2}\s+(?:tháng|thang)\s+\d{1,2}(?:\s+(?:năm|nam)?\s*\d{2,4})?',
        '',
        text_clean,
        flags=re.IGNORECASE
    )
    # 2. ngày DD/MM/YYYY or ngày DD-MM-YYYY or ngày DD/MM/YY or ngày DD-MM-YY or ngày DD/MM
    text_clean = re.sub(
        r'(?:ngày|ngay)\s+\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?',
        '',
        text_clean,
        flags=re.IGNORECASE
    )
    # 3. DD/MM/YYYY or DD-MM-YYYY or DD/MM/YY or DD-MM-YY or DD/MM
    text_clean = re.sub(
        r'\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b',
        '',
        text_clean
    )
    # 4. ngày DD
    text_clean = re.sub(r'(?:ngày|ngay)\s+\d{1,2}\b', '', text_clean, flags=re.IGNORECASE)
    # 5. hôm qua / hôm nay
    text_clean = re.sub(r'\b(hôm qua|hôm nay)\b', '', text_clean, flags=re.IGNORECASE)
    return text_clean

def classify_intent(text):
    text_lower = text.lower()
    
    report_keywords = [
        "báo cáo tuần", "báo cáo quỹ", "tổng kết", "summary", "báo cáo",
        "chi tiêu", "tổng chi", "tổng chi tiêu", "thống kê", "lịch sử chi"
    ]
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

def extract_expense_details(text, current_date_ctx=None):
    date_obj, date_display = parse_date(text)
    if not date_obj:
        date_obj = current_date_ctx if current_date_ctx else datetime.date.today()
        date_display = ""
    text_clean = clean_text_for_amount(text)
    amount = parse_amount(text_clean)
    if not amount:
        return None, None, None, None, None
        
    text_lower = text.lower()
    category = "Khác"
    if any(k in text_lower for k in ["cà phê", "cafe", "coffee"]):
        category = "Cà phê"
    elif any(k in text_lower for k in ["sáng", "breakfast"]):
        category = "Ăn sáng"
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

def generate_report(db, text=""):
    today = datetime.date.today()
    current_month_str = today.strftime("%Y-%m")
    current_month_display = today.strftime("%m/%Y")
    
    # Check if report type is "from start of month"
    is_from_start_of_month = False
    if text:
        text_lower = text.lower()
        if "đầu tháng" in text_lower or "tháng này" in text_lower:
            is_from_start_of_month = True
            
    if is_from_start_of_month:
        start_date = datetime.date(today.year, today.month, 1)
        end_date = today
        header_date_range = f"Từ {start_date.strftime('%d/%m')} đến {end_date.strftime('%d/%m/%Y')}"
    else:
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        header_date_range = f"Tuần [{start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m/%Y')}]"
        
    total_month_expense = 0
    categories_total = {
        "Ăn sáng": 0,
        "Cà phê": 0,
        "Ăn trưa": 0,
        "Ăn tối": 0,
        "Khác": 0
    }
    
    for exp in db.get("expense_log", []):
        exp_date_str = exp.get("date", "")
        if not is_from_start_of_month:
            if not exp_date_str.startswith(current_month_str):
                continue
        else:
            try:
                exp_date = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            if not (start_date <= exp_date <= end_date):
                continue
                
        amount = exp.get("amount", 0)
        total_month_expense += amount
        cat = exp.get("category", "Khác")
        if cat in categories_total:
            categories_total[cat] += amount
        else:
            categories_total["Khác"] += amount
                
    member_incomes = {}
    for inc in db.get("income_log", []):
        inc_date_str = inc.get("date", "").split(" ")[0]
        if not is_from_start_of_month:
            if not inc_date_str.startswith(current_month_str):
                continue
        else:
            try:
                inc_date = datetime.datetime.strptime(inc_date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            if not (start_date <= inc_date <= end_date):
                continue
                
        member = inc.get("member_name", "Ẩn danh")
        amount = inc.get("amount", 0)
        member_incomes[member] = member_incomes.get(member, 0) + amount
            
    lines = []
    lines.append(f"📊 BÁO CÁO QUỸ CƠ QUAN — {header_date_range}")
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
        
    text = unicodedata.normalize('NFC', text)
    
    intent = classify_intent(text)
    if intent in ["report", "balance"]:
        is_new = init_db()
        db = load_db()
        bootstrap_msg = ""
        if is_new:
            bootstrap_msg = "Em vừa khởi tạo file quỹ mới. Anh bắt đầu nhập liệu được rồi nhé!\n"
        if intent == "report":
            return bootstrap_msg + generate_report(db, text)
        else:
            return bootstrap_msg + f"Quỹ tồn hiện tại: {format_vnd(db.get('current_balance', 0))} anh ơi."

    # Process transactions (could be single line or batch)
    is_new = init_db()
    db = load_db()
    
    bootstrap_msg = ""
    if is_new:
        bootstrap_msg = "Em vừa khởi tạo file quỹ mới. Anh bắt đầu nhập liệu được rồi nhé!\n"
        
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    current_date = datetime.date.today()
    transactions = []
    
    for line in lines:
        parsed_d, d_display = parse_date(line)
        cleaned_for_amt = clean_text_for_amount(line)
        amt = parse_amount(cleaned_for_amt)
        
        if parsed_d and amt is None:
            current_date = parsed_d
            continue
            
        line_intent = classify_intent(line)
        if line_intent == "income":
            member, amount = extract_income_details(line)
            if amount:
                tx_date, _ = parse_date(line)
                if not tx_date:
                    tx_date = current_date
                transactions.append({
                    "type": "income",
                    "member": member,
                    "amount": amount,
                    "date": tx_date
                })
        elif line_intent == "expense":
            amount, category, date_obj, date_display, note = extract_expense_details(line, current_date)
            if amount:
                transactions.append({
                    "type": "expense",
                    "category": category,
                    "amount": amount,
                    "date": date_obj,
                    "note": note
                })
                
    if not transactions:
        return bootstrap_msg + "Anh Bình ơi, em không nhận diện được giao dịch nào trong nội dung này. Anh nhắn rõ lại giúp em nhé!"
        
    # Process transactions in db
    if len(transactions) == 1:
        tx = transactions[0]
        amount = tx["amount"]
        tx_date = tx["date"]
        
        if tx["type"] == "income":
            member = tx["member"]
            if not member:
                return bootstrap_msg + f"Anh Bình ơi, ai đóng {format_vnd(amount)} vậy anh? Nhắn em tên người đóng nhé."
                
            db["current_balance"] = db.get("current_balance", 0) + amount
            if "members" not in db:
                db["members"] = {}
            db["members"][member] = db["members"].get(member, 0) + amount
            
            now = datetime.datetime.now()
            if tx_date == now.date():
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = f"{tx_date.strftime('%Y-%m-%d')} {now.strftime('%H:%M:%S')}"
                
            db.setdefault("income_log", []).append({
                "date": timestamp,
                "member_name": member,
                "amount": amount
            })
            save_db(db)
            return bootstrap_msg + f"✅ {member} đóng {format_vnd(amount)}. Quỹ tồn: {format_vnd(db['current_balance'])}"
            
        else:
            category = tx["category"]
            note = tx["note"]
            db["current_balance"] = db.get("current_balance", 0) - amount
            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.setdefault("expense_log", []).append({
                "date": tx_date.strftime("%Y-%m-%d"),
                "created_at": created_at,
                "category": category,
                "amount": amount,
                "note": note
            })
            save_db(db)
            
            if tx_date == datetime.date.today():
                rel_date = "hôm nay"
            elif tx_date == datetime.date.today() - datetime.timedelta(days=1):
                rel_date = "hôm qua"
            else:
                rel_date = tx_date.strftime("%d/%m")
            date_str = f" ({rel_date})"
            
            response = f"✅ Chi {category.lower()} {format_vnd(amount)}{date_str}. Quỹ tồn: {format_vnd(db['current_balance'])}"
            if db["current_balance"] < db.get("config", {}).get("low_balance_threshold", 300000):
                response += "\n⚠️ Anh Bình ơi, quỹ còn dưới 300k, anh nhớ nhắc mọi người chuẩn bị đóng quỹ nhé!"
            return bootstrap_msg + response
            
    # Process batch transactions
    log_responses = []
    for tx in transactions:
        amount = tx["amount"]
        tx_date = tx["date"]
        
        if tx["type"] == "income":
            member = tx["member"] or "Ẩn danh"
            db["current_balance"] = db.get("current_balance", 0) + amount
            if "members" not in db:
                db["members"] = {}
            db["members"][member] = db["members"].get(member, 0) + amount
            
            now = datetime.datetime.now()
            if tx_date == now.date():
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = f"{tx_date.strftime('%Y-%m-%d')} {now.strftime('%H:%M:%S')}"
                
            db.setdefault("income_log", []).append({
                "date": timestamp,
                "member_name": member,
                "amount": amount
            })
            log_responses.append(f"- Đóng quỹ: {member} nộp {format_vnd(amount)} ({tx_date.strftime('%d/%m')})")
            
        else:
            category = tx["category"]
            note = tx["note"]
            db["current_balance"] = db.get("current_balance", 0) - amount
            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.setdefault("expense_log", []).append({
                "date": tx_date.strftime("%Y-%m-%d"),
                "created_at": created_at,
                "category": category,
                "amount": amount,
                "note": note
            })
            note_str = f" ({note})" if note else ""
            log_responses.append(f"- Chi {category.lower()}{note_str}: {format_vnd(amount)} ({tx_date.strftime('%d/%m')})")
            
    save_db(db)
    
    res_lines = [bootstrap_msg + "✅ Đã ghi nhận thành công các giao dịch sau:"]
    res_lines.extend(log_responses)
    res_lines.append("")
    res_lines.append(f"💰 Quỹ tồn hiện tại: {format_vnd(db['current_balance'])}")
    
    if db["current_balance"] < db.get("config", {}).get("low_balance_threshold", 300000):
        res_lines.append("⚠️ Anh Bình ơi, quỹ còn dưới 300k, anh nhớ nhắc mọi người chuẩn bị đóng quỹ nhé!")
        
    return "\n".join(res_lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        res = process_message(query)
        if res:
            print(res)
    else:
        db = load_db()
        print(f"Quỹ tồn hiện tại: {format_vnd(db.get('current_balance', 0))} anh ơi.")
