
import os, json, datetime, re, random, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "_config.yml"
TOPIC_PATH  = PROJECT_ROOT / "scripts" / "topics.json"
POSTS_DIR   = PROJECT_ROOT / "_posts"

AMAZON_TAG = "countrysheduk-21"
CURRENCY = "£"

# Try reading from _config.yml (optional)
try:
    for line in open(CONFIG_PATH, encoding="utf-8"):
        if line.strip().startswith("amazon_tag:"):
            AMAZON_TAG = line.split(":", 1)[1].strip()
        if line.strip().startswith("currency:"):
            CURRENCY = line.split(":", 1)[1].strip().strip('"')
except FileNotFoundError:
    pass

def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]

def affiliate_link(search_term: str) -> str:
    import urllib.parse as up
    q = up.quote(search_term)
    return f"https://www.amazon.co.uk/s?k={q}&tag={AMAZON_TAG}"

def price_range_placeholder():
    bands = [
        (f"{CURRENCY}20-{CURRENCY}40", "Budget"),
        (f"{CURRENCY}40-{CURRENCY}80", "Mid-range"),
        (f"{CURRENCY}80+", "Premium"),
    ]
    return random.choice(bands)

TEMPLATE = """---
layout: post
title: "{title}"
categories: [{category}]
---

If you work on farms or enjoy country life in the UK, finding reliable {keyword} matters.
This faceless guide gives you straightforward, UK-focused buying advice with zero fluff.

## Top Picks (at a glance)

| Pick | Why it suits farm life | Typical price |
|---|---|---|
| Best Overall | A dependable option with solid build and year-round performance. | {price1} |
| Best Value | Great for tight budgets without cutting essentials. | {price2} |
| Heavy-Duty | Built to take a beating on busy yards. | {price3} |

Quick links: [Search Amazon UK]({aff1}) • [Alt option]({aff2}) • [Another search]({aff3})

## What to look for (UK perspective)
- Durability: Weather, mud and daily use demand tough construction.
- Comfort & Fit: If you are on your feet all day, prioritise comfort.
- Protection: Consider toe caps, waterproof ratings or shock protection where relevant.
- Warranty & Parts: UK spares and straightforward returns make life easier.

## Comparison Table

| Feature | Overall | Value | Heavy-Duty |
|---|---|---|---|
| Build quality | High | Medium | Very high |
| Ease of use | Easy | Easy | Moderate |
| Weight | Medium | Light | Heavy |
| Best for | Daily general use | Light/occasional work | Heavy workloads, bad weather |

## Buying advice
- Set a realistic budget and buy once, not twice.
- Try items on where possible; return policies vary by retailer.
- For equipment, consider maintenance access and parts availability in the UK.
- Read recent UK reviews before purchasing.

## Recommended options
1. A trusted all-rounder with consistent feedback. [See price]({aff1})
2. A wallet-friendly pick for lighter workloads. [See price]({aff2})
3. A tougher choice for heavy use and harsh conditions. [See price]({aff3})

---

We may earn a commission if you buy via links on this page. Prices and availability can change.
"""

def write_post(topic):
    today = datetime.date.today()
    title = topic["title"]
    keyword = topic["keyword"]
    category = topic["category"]
    slug = slugify(title)
    fname = f"{today.isoformat()}-{slug}.md"
    path = POSTS_DIR / fname

    variants = [keyword, f"{keyword} UK", f"best {keyword} UK"]
    aff1, aff2, aff3 = [affiliate_link(v) for v in variants]

    price1, _ = price_range_placeholder()
    price2, _ = price_range_placeholder()
    price3, _ = price_range_placeholder()

    content = TEMPLATE.format(
        title=title,
        category=category,
        keyword=keyword,
        aff1=aff1, aff2=aff2, aff3=aff3,
        price1=price1, price2=price2, price3=price3
    )

    path.write_text(content, encoding="utf-8")
    return path

def main(count=2):
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    topics = json.load(open(TOPIC_PATH, encoding="utf-8"))

    posted_slugs = set()
    for p in POSTS_DIR.glob("*.md"):
        parts = p.stem.split("-")
        if len(parts) > 3:
            posted_slugs.add("-".join(parts[3:]))
    remaining = [t for t in topics if slugify(t["title"]) not in posted_slugs]

    if not remaining:
        remaining = topics[:]
        random.shuffle(remaining)

    to_publish = remaining[:count]
    created = []
    for t in to_publish:
        created.append(str(write_post(t)))

    print("Created posts:")
    for c in created:
        print(c)

if __name__ == "__main__":
    count = 2
    if len(sys.argv) >= 3 and sys.argv[1] == "--count":
        try:
            count = int(sys.argv[2])
        except:
            pass
    main(count=count)
