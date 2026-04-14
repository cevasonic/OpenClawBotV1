#!/usr/bin/env python3
"""
Script để lấy 10 văn bản pháp luật mới nhất từ HTML đã scrape
"""

from bs4 import BeautifulSoup
from datetime import datetime
import re

def parse_thuvienphapluat_html(html_file):
    """Parse HTML file và lấy danh sách 10 văn bản mới nhất"""
    
    print("🕷️  PHÂN TÍCH DANH SÁCH VĂN BẢN TỪ THUVIENPHAPLUAT.VN")
    print("=" * 70)
    print(f"⏱️  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Tìm các section chứa "Ban hành" text
        van_ban_list = []
        
        # Phương pháp 1: Tìm tất cả text nodes chứa "Ban hành:"
        for element in soup.find_all(string=re.compile(r'Ban hành:')):
            # Lấy parent element để có context
            parent = element.parent
            while parent and len(parent.get_text(strip=True)) < 500:
                parent = parent.parent
                if parent is None:
                    break
            
            if parent:
                text = parent.get_text(strip=True)
                # Tìm pattern ngày tháng
                dates = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)
                if dates:
                    van_ban_list.append({
                        'text': text[:200],  # Lấy 200 ký tự đầu
                        'date': dates[0],
                        'full_text': text
                    })
        
        # Loại bỏ duplicates và sort by date
        unique_list = {}
        for item in van_ban_list:
            date_key = item['date']
            if date_key not in unique_list:
                unique_list[date_key] = item
        
        # Sort by date descending (mới nhất trước)
        sorted_list = sorted(unique_list.values(), 
                           key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'),
                           reverse=True)
        
        # Lấy 10 mục đầu tiên
        top_10 = sorted_list[:10]
        
        if not top_10:
            print("⚠️  Không tìm thấy danh sách văn bản cụ thể")
            print("\n💡 GỢI Ý: Website có thể sử dụng JavaScript dynamic")
            print("📝 Hãy dùng Scrapling fetch mode hoặc Playwright")
            return False
        
        print("📋 **10 VĂN BẢN MỚI NHẤT:**\n")
        
        for idx, item in enumerate(top_10, 1):
            print(f"{idx}. 📄 Ngày ban hành: {item['date']}")
            print(f"   Nội dung: {item['text'][:100]}...")
            print()
        
        print("=" * 70)
        print(f"✅ Tìm thấy {len(top_10)} văn bản!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return False

if __name__ == "__main__":
    html_file = "/tmp/thuvienphapluat_content.html"
    success = parse_thuvienphapluat_html(html_file)
    exit(0 if success else 1)
