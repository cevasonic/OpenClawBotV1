#!/usr/bin/env python3
"""
Script để lấy 10 văn bản pháp luật mới nhất từ thuvienphapluat.vn
Dùng Scrapling để bypass anti-bot và lấy dữ liệu
"""

import sys
import subprocess
import json
from datetime import datetime

def scrape_thuvienphapluat():
    """Lấy danh sách văn bản mới nhất từ thuvienphapluat.vn"""
    
    url = "https://www.thuvienphapluat.vn/"
    output_file = "/tmp/thuvienphapluat_content.html"
    
    print("🕷️  Đang scrape thuvienphapluat.vn...")
    print(f"⏱️  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # Dùng Scrapling GET - HTTP request đơn giản, không cần browser
    cmd = [
        "scrapling", "extract", "get",
        url,
        output_file,
        "--timeout", "30"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ Lỗi khi scrape: {result.stderr}")
            return False
        
        print(f"✅ Đã scrape thành công!")
        print(f"📁 Output file: {output_file}")
        
        # Đọc file và trích xuất thông tin
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Phân tích dữ liệu
        print("\n📋 **DANH SÁCH VĂN BẢN MỚI NHẤT:**\n")
        
        # Tìm các mục có ngày ban hành
        lines = content.split('\n')
        van_ban_list = []
        
        for i, line in enumerate(lines):
            if 'Ban hành:' in line and i+1 < len(lines):
                # Lấy thông tin văn bản
                ban_hanh_line = line.strip()
                
                # Tìm ngày
                if '/' in ban_hanh_line:
                    van_ban_list.append(ban_hanh_line)
        
        # Lấy 10 mục đầu tiên
        van_ban_list = van_ban_list[:10]
        
        if not van_ban_list:
            print("⚠️  Không tìm thấy danh sách văn bản cụ thể")
            print("\n📄 Nội dung HTML đã được lưu tại:", output_file)
            print("💡 Anh có thể mở file để xem chi tiết")
            return True
        
        for idx, item in enumerate(van_ban_list, 1):
            print(f"{idx}. {item}")
        
        print("\n✅ Hoàn tất!")
        print(f"💾 File HTML đầy đủ: {output_file}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout - Scraping quá lâu")
        return False
    except FileNotFoundError:
        print("❌ Lỗi: scrapling command không tìm thấy")
        print("💡 Vui lòng cài Scrapling: pip install 'scrapling[all]>=0.4.6'")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return False

if __name__ == "__main__":
    success = scrape_thuvienphapluat()
    sys.exit(0 if success else 1)
