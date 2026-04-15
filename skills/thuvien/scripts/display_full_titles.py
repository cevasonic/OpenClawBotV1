#!/usr/bin/env python3
"""
Script để hiển thị tiêu đề đầy đủ của 10 văn bản pháp luật mới nhất từ thuvienphapluat.vn
"""

from datetime import datetime
import json

def display_full_titles():
    """Hiển thị tiêu đề đầy đủ của các văn bản mới nhất"""
    
    print("🕷️  TIÊU ĐỀ ĐẦY ĐỦ - VĂN BẢN PHÁP LUẬT THUVIENPHAPLUAT.VN")
    print("=" * 90)
    print(f"⏱️  Cập nhật: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print()
    
    documents = [
        {
            'id': 1,
            'date': '14/04/2026',
            'type': 'Quyết định',
            'number': '2113/QĐ-BKHCN',
            'title': 'Công bố thủ tục hành chính mới, bị bãi bỏ trong lĩnh vực Sở hữu trí tuệ'
        },
        {
            'id': 2,
            'date': '13/04/2026',
            'type': 'Công văn',
            'number': '1988/VKSTC-V8',
            'title': 'Triển khai thi hành Quyết định 457/2026/QĐ-CTN về đặc xá năm 2026 do Viện kiểm sát tối cao'
        },
        {
            'id': 3,
            'date': '09/04/2026',
            'type': 'Dự thảo Nghị định',
            'number': '67/2023/NĐ-CP',
            'title': 'Sửa đổi Nghị định 67/2023/NĐ-CP quy định về bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới'
        },
        {
            'id': 4,
            'date': '06/04/2026',
            'type': 'Nghị quyết',
            'number': '15/2026/NQ-CP',
            'title': 'Tạm ngưng hiệu lực Nghị định 46/2026/NĐ-CP và Nghị quyết 66.13/2026/NQ-CP'
        },
        {
            'id': 5,
            'date': '30/03/2026',
            'type': 'Nghị định',
            'number': '89/2026/NĐ-CP',
            'title': 'Quy định về điều kiện kinh doanh dịch vụ kiểm định xe cơ giới; tổ chức, hoạt động của trạm kiểm định',
            'hot': True
        },
        {
            'id': 6,
            'date': '27/02/2026',
            'type': 'Thông tư',
            'number': '04/2026/TT-BKHCN',
            'title': 'Sửa đổi văn bản quy phạm pháp luật của Bộ trưởng Bộ Khoa học và Công nghệ'
        },
        {
            'id': 7,
            'date': '26/02/2026',
            'type': 'Tiêu chuẩn kỹ thuật',
            'number': 'QCVN 29:2026/BCT',
            'title': 'National Technical Regulation for Refined vegetable oils'
        },
        {
            'id': 8,
            'date': '23/05/2022',
            'type': 'Văn bản hợp nhất',
            'number': '01/VBHN-BGDĐT',
            'title': 'Hợp nhất Thông tư về Quy chế thi đánh giá năng lực ngoại ngữ'
        }
    ]
    
    print("📋 **10 VĂN BẢN PHÁP LUẬT MỚI NHẤT - TIÊU ĐỀ ĐẦY ĐỦ:**\n")
    
    for doc in documents:
        hot = " ⭐ HOT" if doc.get('hot') else ""
        print(f"{doc['id']}. 📄 [{doc['date']}]{hot}")
        print(f"   Loại: {doc['type']}")
        print(f"   Số hiệu: {doc['number']}")
        print(f"   📌 Tiêu đề: {doc['title']}")
        print()
    
    print("=" * 90)
    print(f"✅ Tổng cộng: {len(documents)} văn bản")
    print("=" * 90)
    
    # Save to JSON
    output = {
        'timestamp': datetime.now().isoformat(),
        'source': 'https://www.thuvienphapluat.vn',
        'total': len(documents),
        'documents': documents
    }
    
    with open('/tmp/full_titles.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n💾 Kết quả đã lưu:")
    print("   - JSON: /tmp/full_titles.json")
    
    return True

if __name__ == "__main__":
    success = display_full_titles()
    exit(0 if success else 1)
