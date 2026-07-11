#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build search-index.json for the Berkshire Hathaway research site.
Scans all HTML files under deploy_site and extracts title, description,
category, tags, and a snippet for client-side search.
"""
import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
SITE_ROOT = ROOT
OUTPUT = ROOT / "search-index.json"

# Directories to skip
SKIP_DIRS = {
    ".git", "_brk_src", ".workbuddy", "deploy_site"  # contains a duplicate pabrai-index
}

# File-level exclusions (relative to site root)
SKIP_FILES = {
    "deploy_site/berkshire-pabrai-index.html",
}


def extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    title = re.sub(r"<[^>]+>", " ", m.group(1))
    title = re.sub(r"\s+", " ", title).strip()
    return title


def strip_tags(html: str) -> str:
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;|&ensp;|&emsp;|&thinsp;", " ", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_headings(html: str) -> list:
    headings = []
    for tag in ["h1", "h2"]:
        for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.IGNORECASE | re.DOTALL):
            txt = strip_tags(m.group(1)).strip()
            if txt and txt not in headings:
                headings.append(txt)
    return headings


def extract_snippet(html: str, max_chars: int = 220) -> str:
    text = strip_tags(html)
    # Remove navigation/common boilerplate words if they appear at start
    text = re.sub(r"^(首页|返回| Berkshire Hathaway Research|投资数据中心)\s*", "", text)
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + "…"
    return text


def extract_search_text(html: str, max_chars: int = 1000) -> str:
    """Return a longer plain text for search matching (not display)."""
    text = strip_tags(html)
    # Remove very common boilerplate
    text = re.sub(r"^(首页|返回| Berkshire Hathaway Research|投资数据中心)\s*", "", text)
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + "…"
    return text


def categorize(rel_path: str, title: str) -> tuple:
    """Return (category, priority)."""
    p = rel_path.replace("\\", "/")
    lower = p.lower()

    if p == "index.html":
        return "首页", 1
    if "meetings_content/full_en/" in lower:
        return "年会实录（英文）", 10
    if "meetings_content/full/" in lower:
        return "年会实录（中文）", 10
    if "meetings_content/" in lower:
        return "年会实录", 10
    if "letters_content/" in lower:
        return "致股东的信", 11
    if "value-investors-content/" in lower:
        if "pabrai" in lower:
            return "帕伯莱演讲", 12
        if "li-lu" in lower or "lilu" in lower:
            return "李录演讲", 12
        if "guijiang" in lower:
            return "归江文章", 12
        return "价值投资演讲", 12
    if "articles/" in lower:
        return "深度文章", 13
    if "index-investing-content/" in lower:
        return "指数投资", 28

    # Root-level special pages
    page_map = {
        "berkshire-meetings.html": ("年会实录", 10),
        "berkshire-letters.html": ("致股东的信", 11),
        "berkshire-partnership-letters.html": ("致股东的信", 11),
        "buffett-partnership-showcase.html": ("致股东的信", 11),
        "berkshire-concepts.html": ("概念知识", 14),
        "berkshire-methodology.html": ("投资方法论", 15),
        "berkshire-financial-terms.html": ("金融术语", 16),
        "berkshire-articles.html": ("深度文章", 13),
        "berkshire-index-investing.html": ("指数投资", 28),
        "berkshire-stress-test.html": ("指数投资", 1),
        "berkshire-value-investors.html": ("价值投资人物", 17),
        "berkshire-pabrai-index.html": ("帕伯莱演讲", 12),
        "berkshire-guijiang-index.html": ("归江文章", 12),
        "berkshire-munger-speeches.html": ("芒格演讲", 18),
        "berkshire-buffett-quotes.html": ("巴菲特演讲与名言", 19),
        "berkshire-munger-quotes.html": ("芒格名言", 19),
        "berkshire-business-map.html": ("伯克希尔业务", 20),
        "berkshire-business-map-full.html": ("伯克希尔业务", 20),
        "berkshire-investments.html": ("伯克希尔投资", 21),
        "berkshire-acquisitions.html": ("伯克希尔收购", 22),
        "berkshire-calculators.html": ("投资工具", 30),
        "berkshire-standalone.html": ("投资数据中心", 2),
        "berkshire-abel-letters.html": ("致股东的信", 11),
        "berkshire-speeches.html": ("演讲访谈", 18),
        "curated36.html": ("投资清单", 23),
        "investments/berkshire.html": ("伯克希尔投资", 21),
    }
    if p in page_map:
        return page_map[p]

    return "其他", 50


def build_tags(title: str, snippet: str, headings: list, rel_path: str) -> list:
    tags = []
    # Year tags
    years = re.findall(r"20\d{2}|19\d{2}", title + " " + " ".join(headings[:3]))
    for y in sorted(set(years), reverse=True):
        tags.append(y + "年")

    # Person / company tags from title
    keywords = ["巴菲特", "芒格", "阿贝尔", "格雷格", "李录", "帕伯莱", "莫尼什", "归江", "信璞投资",
                "伯克希尔", "比亚迪", "苹果", "可口可乐", "美国银行", "西方石油",
                "保险", "浮存金", "护城河", "安全边际", "内在价值", "股息",
                "复利", "定投", "持仓", "补仓", "仓位", "PE", "PB", "ROE"]
    combined = (title + snippet).lower()
    for kw in keywords:
        if kw in combined and kw not in tags:
            tags.append(kw)
    return tags[:10]


def main():
    entries = []

    for path in sorted(SITE_ROOT.rglob("*.html")):
        rel = path.relative_to(SITE_ROOT).as_posix()

        # Skip hidden/tool dirs and explicit exclusions
        if any(part in SKIP_DIRS for part in path.relative_to(SITE_ROOT).parts):
            continue
        if rel in SKIP_FILES:
            continue

        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            try:
                html = path.read_text(encoding="gbk")
            except Exception:
                continue

        title = extract_title(html)
        if not title:
            title = path.stem

        headings = extract_headings(html)

        # For long transcripts, limit snippet length to keep index small
        if any(x in rel.lower() for x in ["meetings_content/full", "letters_content/cn", "value-investors-content"]):
            snippet = extract_snippet(html, max_chars=180)
            search_text = extract_search_text(html, max_chars=1000)
        else:
            snippet = extract_snippet(html, max_chars=260)
            search_text = extract_search_text(html, max_chars=800)

        category, priority = categorize(rel, title)
        tags = build_tags(title, snippet, headings, rel)

        # Make URL relative to site root (keep as-is for GitHub Pages)
        url = rel

        entry = {
            "title": title,
            "url": url,
            "category": category,
            "priority": priority,
            "description": snippet,
            "searchText": search_text,
            "headings": headings[:6],
            "tags": tags,
        }
        entries.append(entry)

    # Sort by priority then title
    entries.sort(key=lambda x: (x["priority"], x["title"]))

    data = {
        "generated_at": "",
        "total": len(entries),
        "categories": sorted({e["category"] for e in entries}),
        "entries": entries,
    }

    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUTPUT}: {len(entries)} entries")


if __name__ == "__main__":
    main()
