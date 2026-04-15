#!/usr/bin/env python3
"""
Script scrape realtime từ thuvienphapluat.vn - Lấy tiêu đề ĐẦY ĐỦ SẠCH
KHÔNG dùng cache, KHÔNG cắt bỏ tiêu đề
"""

import subprocess
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time

def scrape_realtime_html(max_retries=3, timeout_seconds=120):
    """Scrape HTML realtime từ website"""
    
    url = "https://www.thuvienphapluat.vn/"
    
    print("🕷️  SCRAPING REALTIME TỪ THUVIENPHAPLUAT.VN")
    print("=" * 100)
    print(f"⏱️  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: {url}")
    print("=" * 100)
    print()
    
    for attempt in range(max_retries):
        print(f"📥 Attempt {attempt + 1}/{max_retries}: Fetching HTML realtime...")
        
        try:
            cmd = [
                "scrapling", "extract", "get",
                url,
                "/tmp/thuvien_temp.html",  # File tạm, sẽ xóa sau khi đọc
                "--timeout", str(timeout_seconds)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds + 30)
            
            if result.returncode == 0:
                print("   ✅ HTML fetched successfully!")
                # Đọc file rồi xóa ngay để không lưu
                with open("/tmp/thuvien_temp.html", 'r', encoding='utf-8') as f:
                    html_content = f.read()
                # Xóa file tạm
                subprocess.run(["rm", "-f", "/tmp/thuvien_temp.html"], capture_output=True)
                return html_content
            else:
                print(f"   ❌ Scrapling failed")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"   ⏱️  Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ Timeout")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"   ⏱️  Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n❌ All scraping attempts failed")
    return None

def clean_title_text(text):
    """Clean tiêu đề: bỏ tất cả thứ thừa"""
    
    # Bỏ số đơn lẻ ở đầu (1, 2, 3, 4, 5)
    text = re.sub(r'^(HOT|\d)\s*', '', text)
    
    # Bỏ "Tiếng Anh" và tất cả sau nó
    text = re.sub(r'Tiếng Anh.*$', '', text, flags=re.DOTALL)
    
    # Bỏ "|" và tất cả sau nó
    if '|' in text:
        text = text.split('|')[0]
    
    # Clean whitespace
    text = ' '.join(text.split())
    text = text.strip()
    
    return text

def parse_html_full_titles(html_content):
    """Parse HTML và lấy tiêu đề ĐẦY ĐỦ - KHÔNG CẮT BỎ, KHÔNG TÓM TẮT"""
    
    print("\n📝 Parsing HTML để lấy tiêu đề ĐẦY ĐỦ (100% nguyên bản)...\n")
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        documents = []
        
        # Tìm tất cả text chứa "Ban hành:"
        for element in soup.find_all(string=re.compile(r'Ban hành:')):
            parent = element.parent
            
            # Di chuyển lên để tìm context (tối đa 25 cấp)
            for _ in range(25):
                if parent is None:
                    break
                parent = parent.parent
                text_len = len(parent.get_text(strip=True))
                if 100 < text_len < 2000:  # Mở rộng giới hạn lên 2000
                    break
            
            if parent:
                full_text = parent.get_text(strip=True)
                
                # Extract date (chỉ để sắp xếp, không dùng cho title)
                dates = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', full_text)
                if not dates:
                    continue
                
                date = dates[0]
                
                # **CHỈ LẤY PHẦN TIÊU ĐỀ CHÍNH**
                # 1. Bỏ phần links phía sau (Tiếng Anh|Văn bản gốc|...)
                if 'Tiếng Anh' in full_text:
                    full_text = full_text.split('Tiếng Anh')[0]
                
                # 2. Bỏ số thứ tự ở đầu (1, 2, 3...) từ HTML
                full_text = re.sub(r'^([1-9])\s*', '', full_text)
                
                # 3. Clean khoảng trắng thừa (GIỮ NGUYÊN TẤT CẢ TỪ)
                title = ' '.join(full_text.split())
                
                # Chỉ lấy nếu tiêu đề đủ dài
                if len(title) >= 20:
                    documents.append({
                        'date': date,
                        'title_full': title,
                        'title_length': len(title)
                    })
        
        # Deduplicate theo date
        unique = {}
        for doc in documents:
            key = doc['date']
            if key not in unique:
                unique[key] = doc
        
        # Sort by date descending
        sorted_docs = sorted(unique.values(),
                            key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'),
                            reverse=True)
        
        top_10 = sorted_docs[:10]
        
        if not top_10:
            print("⚠️  Không tìm thấy văn bản")
            return []
        
        print(f"✅ Tìm thấy {len(top_10)} văn bản!\n")
        print("=" * 100)
        print("📋 **10 VĂN BẢN PHÁP LUẬT MỚI NHẤT - TIÊU ĐỀ ĐẦY ĐỦ 100% (KHÔNG CẮT BỎ, KHÔNG TÓM TẮT):**")
        print("=" * 100)
        print()
        
        for idx, doc in enumerate(top_10, 1):
            print(f"{idx}. 📄 [{doc['date']}]")
            print(f"   {doc['title_full']}")
            print()
        
        return top_10
        
    except Exception as e:
        print(f"❌ Parse error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def main():
    """Main function"""
    
    # Step 1: Scrape realtime
    html_content = scrape_realtime_html(max_retries=3, timeout_seconds=120)
    
    if not html_content:
        print("\n❌ Scraping failed")
        return False
    
    # Step 2: Parse
    documents = parse_html_full_titles(html_content)
    
    if not documents:
        print("\n❌ No documents found")
        return False
    
    # Step 3: Chỉ hiển thị kết quả, KHÔNG lưu file
    print("=" * 100)
    print(f"✅ Success! {len(documents)} documents fetched")
    print("=" * 100)
    print("\n📄 Kết quả đã hiển thị ở trên - không lưu vào file để tiết kiệm bộ nhớ.")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
