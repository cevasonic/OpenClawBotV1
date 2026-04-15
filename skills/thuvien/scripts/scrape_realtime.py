#!/usr/bin/env python3
"""
Script để scrape realtime từ thuvienphapluat.vn và lấy TIÊU ĐỀ SẠCH
Lần 3: Clean text thừa hoàn toàn
"""

import subprocess
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time

def scrape_with_retry(max_retries=3, timeout_seconds=120):
    """Scrape với retry logic"""
    
    url = "https://www.thuvienphapluat.vn/"
    output_file = "/tmp/thuvien_realtime.html"
    
    print("🕷️  SCRAPING THUVIENPHAPLUAT.VN (REALTIME)")
    print("=" * 90)
    print(f"⏱️  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print()
    
    for attempt in range(max_retries):
        print(f"📥 Attempt {attempt + 1}/{max_retries}: Fetching HTML...")
        
        try:
            cmd = [
                "scrapling", "extract", "get",
                url,
                output_file,
                "--timeout", str(timeout_seconds)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds + 30)
            
            if result.returncode == 0:
                print("   ✅ Success!")
                return output_file
            else:
                print(f"   ❌ Failed")
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 5)
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ Timeout")
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 5)
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    return None

def clean_title(text):
    """Clean text để chỉ lấy tiêu đề"""
    
    # Bỏ tất cả link text (Tiếng Anh|Văn bản gốc|Lược đồ|Liên quan|Tải về...)
    text = re.sub(r'\|.*$', '', text)
    text = re.sub(r'Tiếng Anh.*$', '', text)
    text = re.sub(r'Văn bản gốc.*$', '', text)
    text = re.sub(r'Lược đồ.*$', '', text)
    text = re.sub(r'Liên quan.*$', '', text)
    text = re.sub(r'Tải về.*$', '', text)
    
    # Bỏ số đơn lẻ ở đầu (1, 2, 3, 4, 5)
    text = re.sub(r'^\d+\s+', '', text)
    
    # Bỏ metadata
    text = re.sub(r'Ban hành:.*?(?=\d{1,2}/\d{1,2}/\d{4})', '', text)
    text = re.sub(r'Hiệu lực:.*?(?=Tình trạng:|Cập nhật:|$)', '', text)
    text = re.sub(r'Tình trạng:.*?(?=Cập nhật:|$)', '', text)
    text = re.sub(r'Cập nhật:.*', '', text)
    
    # Clean whitespace
    text = ' '.join(text.split())
    text = text.strip()
    
    return text

def parse_html_to_documents(html_file):
    """Parse HTML và lấy danh sách văn bản với tiêu đề sạch"""
    
    print("\n📝 Parsing HTML và trích xuất TIÊU ĐỀ SẠCH...\n")
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        documents = []
        
        # Tìm tất cả text chứa "Ban hành:"
        for element in soup.find_all(string=re.compile(r'Ban hành:')):
            parent = element.parent
            
            # Di chuyển lên để tìm context
            for _ in range(20):
                if parent is None:
                    break
                parent = parent.parent
                text_len = len(parent.get_text(strip=True))
                if 80 < text_len < 1000:
                    break
            
            if parent:
                full_text = parent.get_text(strip=True)
                
                # Extract date
                dates = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', full_text)
                if not dates:
                    continue
                
                date = dates[0]
                
                # Lấy tiêu đề (phần trước "Ban hành:")
                parts = full_text.split('Ban hành:')
                title_text = parts[0]
                
                # Clean title
                title = clean_title(title_text)
                
                if title and len(title) > 15:
                    documents.append({
                        'date': date,
                        'title': title
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
        print("📋 **10 VĂN BẢN PHÁP LUẬT MỚI NHẤT - TIÊU ĐỀ SẠCH:**\n")
        
        for idx, doc in enumerate(top_10, 1):
            print(f"{idx}. 📄 [{doc['date']}]")
            print(f"   📌 {doc['title']}")
            print()
        
        return top_10
        
    except Exception as e:
        print(f"❌ Parse error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def main():
    """Main function"""
    
    # Step 1: Scrape
    html_file = scrape_with_retry(max_retries=3, timeout_seconds=120)
    
    if not html_file:
        print("\n❌ Scraping failed")
        return False
    
    # Step 2: Parse
    documents = parse_html_to_documents(html_file)
    
    if not documents:
        print("\n❌ No documents found")
        return False
    
    # Step 3: Save JSON
    output = {
        'timestamp': datetime.now().isoformat(),
        'source': 'https://www.thuvienphapluat.vn',
        'total': len(documents),
        'documents': documents
    }
    
    with open('/tmp/thuvien_realtime.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("=" * 90)
    print(f"✅ Success! {len(documents)} documents fetched")
    print("=" * 90)
    print("\n💾 Results saved:")
    print("   - JSON: /tmp/thuvien_realtime.json")
    print("   - HTML: /tmp/thuvien_realtime.html")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
