---
name: thuvien
description: Scrape and parse Vietnamese legal documents from thuvienphapluat.vn. Extract the latest published legal texts (Quyết định, Công văn, Dự thảo, etc.) with dates and summaries. Use when asked to retrieve, search, or analyze Vietnamese legal documents; get updates from the legal library; or monitor new regulations.
version: "1.0.0"
license: MIT
metadata:
  homepage: "https://www.thuvienphapluat.vn"
  openclaw:
    emoji: "⚖️"
    homepage: "https://www.thuvienphapluat.vn"
    requires:
      bins:
        - python3
      packages:
        - pip3
      python:
        - requests>=2.28.0
        - beautifulsoup4>=4.11.0
        - scrapling>=0.4.6
---

# Thư Viện Pháp Luật Scraper

Scrape and parse Vietnamese legal documents from **thuvienphapluat.vn** (the official Vietnamese Legal Library).

This skill provides tools to:
- 📜 Extract the latest published legal texts
- 📅 Get documents by date or type (Quyết định, Công văn, Dự thảo, etc.)
- 🔍 Search for specific regulations
- 📊 Parse and analyze legal document metadata

**Perfect for:** Monitoring Vietnamese regulations, tracking legal updates, researching specific laws.

## Setup

### Install Dependencies (Once)

```bash
pip3 install --break-system-packages requests beautifulsoup4 scrapling[all]>=0.4.6
```

Or if using venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 scrapling[all]>=0.4.6
```

### Download Browsers (For Scrapling)

```bash
python3 -m playwright install
```

## Usage

### Get Latest 10 Legal Documents

```bash
python3 scripts/scrape_latest.py
```

Output:
```
📋 10 VĂN BẢN MỚI NHẤT:

1. 📄 Quyết định 2113/QĐ-BKHCN (14/04/2026)
   Công bố thủ tục hành chính mới, bị bãi bỏ trong lĩnh vực Sở hữu trí tuệ

2. 📄 Công văn 1988/VKSTC-V8 (13/04/2026)
   Triển khai thi hành Quyết định 457/2026/QĐ-CTN về đặc xá năm 2026
...
```

### Search for Specific Documents

```bash
python3 scripts/search_documents.py "luật lao động"
```

### Parse HTML Output

```bash
python3 scripts/parse_html.py /path/to/downloaded.html
```

## How It Works

### Step 1: Scrape HTML

The skill uses **Scrapling** to fetch HTML from thuvienphapluat.vn:

```python
scrapling extract get https://www.thuvienphapluat.vn/ output.html
```

- **GET mode**: Simple HTTP requests (fast, no browser needed)
- **FETCH mode**: Browser-based (handles JavaScript)
- **STEALTHY-FETCH mode**: Anti-bot bypass (for protected sites)

### Step 2: Parse with BeautifulSoup

Extract structured data from HTML:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
# Find "Ban hành: DD/MM/YYYY" patterns
# Extract text, dates, document types
```

### Step 3: Format & Output

Return as JSON, CSV, or formatted text:

```json
{
  "documents": [
    {
      "type": "Quyết định",
      "number": "2113/QĐ-BKHCN",
      "date": "2026-04-14",
      "summary": "Công bố thủ tục hành chính mới...",
      "url": "https://..."
    }
  ]
}
```

## Key Patterns

### Extract Documents by Type

```bash
# Quyết định (Decisions)
python3 scripts/search_documents.py --type "Quyết định"

# Công văn (Official Letters)
python3 scripts/search_documents.py --type "Công văn"

# Dự thảo (Drafts)
python3 scripts/search_documents.py --type "Dự thảo"
```

### Filter by Date Range

```bash
python3 scripts/search_documents.py --from "2026-04-01" --to "2026-04-15"
```

### Export Results

```bash
# JSON
python3 scripts/scrape_latest.py --format json > documents.json

# CSV
python3 scripts/scrape_latest.py --format csv > documents.csv

# Markdown
python3 scripts/scrape_latest.py --format markdown > documents.md
```

## Troubleshooting

### "Timeout" Errors

Website may be slow or blocking requests. Try:

```bash
# Increase timeout
python3 scripts/scrape_latest.py --timeout 60

# Use browser mode instead of GET
python3 scripts/scrape_latest.py --mode fetch
```

### "No documents found"

The website may have updated its HTML structure. Check:

```bash
# View raw HTML
curl -s https://www.thuvienphapluat.vn/ | head -100

# Update parser patterns in scripts/parse_html.py
```

### SSL Certificate Errors

Disable SSL verification (not recommended for production):

```bash
python3 scripts/scrape_latest.py --no-verify-ssl
```

## Performance

- **GET mode**: ~5-10 seconds (fastest)
- **FETCH mode**: ~15-30 seconds (medium)
- **STEALTHY-FETCH mode**: ~30-60 seconds (slowest, most reliable)

For best results, use **GET mode** first. If it returns empty results, escalate to **FETCH**, then **STEALTHY-FETCH**.

## Legal Notice

- Always respect **thuvienphapluat.vn's robots.txt and Terms of Service**
- This skill is for informational purposes only
- Not official legal advice—consult attorneys for important matters
- Do not use for spamming or excessive scraping

## References

- thuvienphapluat.vn: https://www.thuvienphapluat.vn
- Scrapling docs: https://scrapling.readthedocs.io
- BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/
- Vietnamese legal system: https://en.wikipedia.org/wiki/Law_of_Vietnam
