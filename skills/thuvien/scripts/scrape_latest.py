#!/usr/bin/env python3
"""
Scrape văn bản mới nhất từ thuvienphapluat.vn
Chỉ lấy các văn bản MỚI so với lần xem trước (Delta tracking).
Kết hợp AI phân loại (Feedback loop).
"""

import requests, re, sys, json, time, os
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
from nlp_classifier import SimpleTextClassifier

URL = "https://thuvienphapluat.vn/van-ban-moi"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
}
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MODEL_FILE = os.path.join(DATA_DIR, 'nlp_model.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'scrape_history.json') # Lưu danh sách hiển thị để nhận feedback
SEEN_FILE = os.path.join(DATA_DIR, 'seen_docs.json') # Lưu danh sách URL đã xem (Delta tracking)

def load_json(filepath, default_val):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception: pass
    return default_val

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_with_retry(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            return r.content
        except Exception as e:
            if attempt < MAX_RETRIES: time.sleep(RETRY_DELAY)
            else: raise
    return None

def parse_documents(soup):
    """Trích xuất VB"""
    documents = []
    # Lấy các thẻ a có vẻ là link văn bản
    for a in soup.find_all('a'):
        title = a.get_text(strip=True)
        href = a.get('href', '')
        if href and 'van-ban' in href and len(title) > 15:
            link = "https://thuvienphapluat.vn" + href if href.startswith('/') else href
            documents.append({"title": title, "url": link})
            
    # Dedup
    seen_urls = set()
    unique_docs = []
    for doc in documents:
        if doc['url'] not in seen_urls:
            seen_urls.add(doc['url'])
            unique_docs.append(doc)
    return unique_docs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--feedback', type=str, help='Gửi feedback. VD: "1,3,4" hoặc "0" (nếu không quan tâm cái nào).')
    args = parser.parse_args()
    
    classifier = SimpleTextClassifier(MODEL_FILE)
    
    # ---------------- FEEDBACK MODE ----------------
    if args.feedback is not None:
        history = load_json(HISTORY_FILE, [])
        if not history:
            print("❌ Không có lịch sử scrape gần đây để feedback.")
            sys.exit(1)
            
        interested_indices = []
        if args.feedback.strip() not in ["0", "", "none"]:
            try:
                parts = [p.strip() for p in args.feedback.replace(' ', '').split(',') if p.strip()]
                for p in parts:
                    if '-' in p:
                        start, end = map(int, p.split('-'))
                        interested_indices.extend(range(start, end + 1))
                    else:
                        interested_indices.append(int(p))
            except ValueError:
                print("❌ Định dạng feedback không hợp lệ. Ví dụ đúng: --feedback '1,3,5' hoặc '0'")
                sys.exit(1)
            
        train_docs, train_labels = [], []
        for i, doc in enumerate(history, 1):
            train_docs.append(doc['title'])
            if i in interested_indices: train_labels.append('positive')
            else: train_labels.append('negative')
                
        classifier.train(train_docs, train_labels)
        print(f"✅ Đã học: {len([l for l in train_labels if l == 'positive'])} VB quan tâm, {len([l for l in train_labels if l == 'negative'])} VB KHÔNG quan tâm.")
        sys.exit(0)

    # ---------------- SCRAPE & PREDICT MODE ----------------
    print("🕷️  Thư viện Pháp luật - Cập nhật Văn bản MỚI")
    print("-" * 50)
    
    html_content = fetch_with_retry(URL)
    soup = BeautifulSoup(html_content, 'html.parser')
    all_docs = parse_documents(soup)
    
    # Lọc VB hợp lệ
    valid_docs = []
    pat = re.compile(r'(?i)(Quyết định|Nghị định|Luật|Thông tư|Công văn|Nghị quyết|Chỉ thị)\s+\d+|\d+[/-][A-Z0-9]')
    for doc in all_docs:
        if pat.search(doc["title"]):
            valid_docs.append(doc)

    # Lọc ra VB mới (chưa từng xem)
    seen_urls = load_json(SEEN_FILE, [])
    new_docs = [d for d in valid_docs if d['url'] not in seen_urls]
    
    if not new_docs:
        print("✅ Không có văn bản nào mới so với lần kiểm tra trước.")
        sys.exit(0)

    # Cập nhật danh sách đã xem (Giữ tối đa 1000 link gần nhất để tránh phình file)
    updated_seen = seen_urls + [d['url'] for d in new_docs]
    save_json(SEEN_FILE, updated_seen[-1000:])

    # Chấm điểm
    for doc in new_docs:
        doc['score'] = classifier.predict(doc['title'])
        
    interested_docs = sorted([d for d in new_docs if d['score'] >= 0.5], key=lambda x: x['score'], reverse=True)
    other_docs = sorted([d for d in new_docs if d['score'] < 0.5], key=lambda x: x['score'], reverse=True)
    
    display_list = interested_docs + other_docs
    save_json(HISTORY_FILE, display_list)
    
    total_docs_trained = sum(classifier.doc_counts.values())

    print(f"🔔 Có {len(new_docs)} VĂN BẢN MỚI vừa được cập nhật!\n")
    
    if total_docs_trained == 0:
        for i, doc in enumerate(display_list, 1):
            print(f"{i}. {doc['title']}")
    else:
        print(f"⭐ DỰ ĐOÁN ANH QUAN TÂM:")
        if not interested_docs: print("   (Không có văn bản nào thuộc chủ đề của anh)")
        for i, doc in enumerate(interested_docs, 1):
            print(f"{i}. {doc['title']} (Match: {doc['score']*100:.1f}%)")
            
        print(f"\n📄 CÁC VĂN BẢN KHÁC:")
        start_idx = len(interested_docs) + 1
        if not other_docs: print("   (Không có)")
        for i, doc in enumerate(other_docs, start_idx):
            print(f"{i}. {doc['title']} (Match: {doc['score']*100:.1f}%)")
            
    print("\n--------------------------------------------------")
    print("🎯 Hãy nhắn số thứ tự VB anh quan tâm (vd: 1, 3). Nếu không quan tâm cái nào, nhắn '0'.")

if __name__ == "__main__":
    main()
