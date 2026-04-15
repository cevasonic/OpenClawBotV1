#!/usr/bin/env python3
"""
Script để lấy tiêu đề đầy đủ của 10 văn bản pháp luật mới nhất từ thuvienphapluat.vn
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json

def scrape_and_parse_full_titles():
    """Scrape thuvienphapluat.vn và lấy tiêu đề đầy đủ"""
    
    url = "https://www.thuvienphapluat.vn/"
    
    print("🕷️  SCRAPING THUVIENPHAPLUAT.VN...")
    print("=" * 80)
    print(f"⏱️  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    try:
        # Fetch HTML
        print("📥 Fetching HTML từ thuvienphapluat.vn...")
        response = requests.get(url, timeout=30)
        response.encoding = 'utf-8'
        
        html_content = response.text
        
        # Save HTML for debugging
        with open('/tmp/thuvienphapluat_full.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("✅ HTML fetched successfully!")
        print("📝 Parsing document titles...\n")
        
        # Tìm tất cả các mục chứa thông tin văn bản
        # Pattern: <number> <title> Ban hành: DD/MM/YYYY
        
        documents = []
        
        # Tìm tất cả text nodes
        all_text = soup.get_text()
        
        # Split by "Ban hành:" để tìm các mục
        parts = all_text.split('Ban hành:')
        
        for i, part in enumerate(parts[1:]):  # Bỏ phần đầu
            lines = part.strip().split('\n')
            
            if not lines:
                continue
            
            # Lấy dòng đầu tiên chứa ngày
            date_line = lines[0].strip()
            
            # Extract date (DD/MM/YYYY)
            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', date_line)
            if not date_match:
                continue
            
            date_str = date_match.group(1)
            
            # Lấy tiêu đề từ phần trước "Ban hành:"
            # Tìm từ cuối cùng trong phần trước đó
            if i > 0:
                prev_part = parts[i]
                # Tách lấy các dòng cuối cùng
                prev_lines = prev_part.rstrip().split('\n')
                
                # Lấy những dòng cuối (là tiêu đề)
                title_lines = []
                for line in reversed(prev_lines):
                    line = line.strip()
                    if line and not re.match(r'^\d+$', line):  # Không phải số đơn lẻ
                        title_lines.insert(0, line)
                    else:
                        if title_lines:
                            break
                
                title = ' '.join(title_lines)
                
                if title and len(title) > 10:  # Title phải đủ dài
                    documents.append({
                        'date': date_str,
                        'title': title[:200],  # Giới hạn 200 ký tự
                        'full_title': title
                    })
        
        # Loại bỏ duplicates
        unique_docs = {}
        for doc in documents:
            key = (doc['date'], doc['title'][:50])
            if key not in unique_docs:
                unique_docs[key] = doc
        
        # Sort by date descending
        sorted_docs = sorted(unique_docs.values(),
                            key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'),
                            reverse=True)
        
        # Lấy 10 mục đầu tiên
        top_10 = sorted_docs[:10]
        
        if not top_10:
            print("⚠️  Không tìm thấy tiêu đề cụ thể")
            print("💡 Thử lại hoặc sử dụng Scrapling fetch mode")
            return False
        
        print("📋 **10 VĂN BẢN PHÁP LUẬT MỚI NHẤT - TIÊU ĐỀ ĐẦY ĐỦ:**\n")
        
        for idx, doc in enumerate(top_10, 1):
            print(f"{idx}. 📄 [{doc['date']}]")
            print(f"   📌 {doc['full_title']}")
            print()
        
        print("=" * 80)
        print(f"✅ Tìm thấy {len(top_10)} văn bản!")
        print("=" * 80)
        
        # Save to JSON
        output_json = {
            'timestamp': datetime.now().isoformat(),
            'total': len(top_10),
            'documents': top_10
        }
        
        with open('/tmp/documents.json', 'w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)
        
        print("\n💾 Kết quả đã lưu tại:")
        print("   - JSON: /tmp/documents.json")
        print("   - HTML: /tmp/thuvienphapluat_full.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = scrape_and_parse_full_titles()
    exit(0 if success else 1)
