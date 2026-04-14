# Thư Viện Pháp Luật Scraper Skill

Vietnamese Legal Library (thuvienphapluat.vn) document scraper and parser.

## Quick Start

```bash
# 1. Install dependencies
pip3 install --break-system-packages requests beautifulsoup4 scrapling[all]>=0.4.6

# 2. Download browsers
python3 -m playwright install

# 3. Scrape latest documents
python3 scripts/scrape_latest.py

# 4. Parse HTML results
python3 scripts/parse_html.py /tmp/thuvienphapluat_content.html
```

## Features

✅ Scrape latest legal documents from thuvienphapluat.vn  
✅ Parse document metadata (type, date, summary)  
✅ Filter by document type or date range  
✅ Export as JSON, CSV, or Markdown  
✅ Multi-mode support (GET, FETCH, STEALTHY-FETCH)  

## Usage Examples

### Get latest 10 documents
```bash
python3 scripts/scrape_latest.py
```

### Parse existing HTML file
```bash
python3 scripts/parse_html.py output.html
```

### Search specific documents
```bash
python3 scripts/search_documents.py "luật lao động"
```

## Output Example

```
📋 10 VĂN BẢN MỚI NHẤT:

1. 📄 Quyết định 2113/QĐ-BKHCN (14/04/2026)
   Công bố thủ tục hành chính mới, bị bãi bỏ trong lĩnh vực Sở hữu trí tuệ

2. 📄 Công văn 1988/VKSTC-V8 (13/04/2026)
   Triển khai thi hành Quyết định 457/2026/QĐ-CTN về đặc xá năm 2026
```

## Requirements

- Python 3.10+
- requests
- beautifulsoup4
- scrapling
- playwright (for browser modes)

## See Also

- SKILL.md: Complete documentation
- scripts/: Python scripts for scraping and parsing
- references/: Additional resources

## License

MIT
