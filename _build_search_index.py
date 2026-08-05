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


_CHAIN_NAMES = None


def chain_names() -> dict:
    """slug -> 中文链名，从各链索引页 <title> 自动推导（避免硬编码 119 条链）。"""
    global _CHAIN_NAMES
    if _CHAIN_NAMES is not None:
        return _CHAIN_NAMES
    m = {}
    for hub in SITE_ROOT.glob("berkshire-*-chains.html"):
        mm = re.match(r"berkshire-(.*)-chains\.html$", hub.name)
        if not mm:
            continue
        slug = mm.group(1)
        try:
            html = hub.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        t = extract_title(html)
        name = re.split(r"[—|]", t)[0].strip()
        # "银行业投资图谱 · 42家A股上市银行" / "家电产业链 · 价值投资视角" → 只保留主名
        head = re.split(r"\s+·\s+", name)[0].strip()
        if re.search(r"(产业链|图谱|地图|全景)$", head):
            name = head
        m[slug] = name or slug
    _CHAIN_NAMES = m
    return m


CHAIN_PAGE_RE = re.compile(
    r"^berkshire-(?P<slug>.+?)-(?:chains|chain-[^.]+|co-[^.]+|compare|thermometer)\.html$"
)


def chain_slug_of(rel_path: str):
    """若是产业链体系页面，返回 (slug, 链名, 页型)；否则 None。"""
    base = rel_path.replace("\\", "/").split("/")[-1]
    m = CHAIN_PAGE_RE.match(base)
    if not m:
        return None
    slug = m.group("slug")
    names = chain_names()
    if slug not in names:
        return None
    if base.endswith("-chains.html"):
        kind = "hub"
    elif base.endswith("-compare.html"):
        kind = "compare"
    elif base.endswith("-thermometer.html"):
        kind = "thermometer"
    elif re.search(r"-co-[^.]+\.html$", base):
        kind = "co"
    else:
        kind = "detail"
    return slug, names[slug], kind


def co_summary(html: str, chain_name: str, code: str) -> tuple:
    """公司页(-co-)：从 <div class="snap"> 指标块生成紧凑摘要。"""
    m = re.search(r"<h1[^>]*>([^<]+)", html)
    comp = (m.group(1).strip() if m else "")
    bits = []
    if comp:
        bits.append(f"{comp}（{code}）" if code else comp)
    bits.append(chain_name)
    snap = re.search(r'<div class="snap">(.*?)</div>\s*<h3', html, re.S)
    if snap:
        pairs = re.findall(r"<b>([^<]*)</b>\s*<span>([^<]*)</span>", snap.group(1))
        for val, label in pairs:
            val, label = val.strip(), label.strip()
            if val and val not in ("—", "待采集"):
                bits.append(f"{label} {val}")
    desc = " · ".join(bits)
    if len(desc) > 190:
        desc = desc[:190] + "…"
    stext = " ".join(filter(None, [
        comp, code, chain_name, re.sub(r"产业链$", "", chain_name),
        "公司 财务 估值 PE PB ROE 股息率 泊松信号 年报",
    ]))
    return comp, desc, stext[:300]


def _cell(html: str, label: str):
    m = re.search(re.escape(label) + r"</td>\s*<td[^>]*>(.*?)</td>", html, re.S)
    if not m:
        return None
    v = re.sub(r"<[^>]+>", "", m.group(1))
    v = re.sub(r"\s+", " ", v).strip()
    return v or None


def chain_detail_summary(html: str, chain_name: str, code: str) -> tuple:
    """为公司详情页生成「紧凑但信息量高」的摘要 + 搜索文本，替代 260 字正文截断。

    好处：索引体积从 ~2.8KB/条 降到 ~0.3KB/条，且搜索结果直接显示估值指标。
    """
    m = re.search(r'class="hero-title">([^<]+)', html)
    comp = (m.group(1).strip() if m else "").replace(" 链", "").strip()
    bits = []
    if comp:
        head = f"{comp}（{code}）" if code else comp
        bits.append(head)
    bits.append(chain_name)
    metric_map = [
        ("PE（TTM）", "PE"), ("PB", "PB"), ("ROE（加权）", "ROE"),
        ("股息率", "股息率"), ("总市值", "市值"),
        ("营业总收入", "营收"), ("归母净利润", "净利"), ("毛利率", "毛利率"),
    ]
    for label, short in metric_map:
        v = _cell(html, label)
        if v and v != "待采集":
            bits.append(f"{short} {v}")
    desc = " · ".join(bits)
    if len(desc) > 190:
        desc = desc[:190] + "…"
    stext = " ".join(filter(None, [
        comp, code, chain_name,
        re.sub(r"产业链$", "", chain_name),
        "估值分位 PE PB ROE 股息率 财务 年报 产业链",
    ]))
    return comp, desc, stext[:300]


def categorize(rel_path: str, title: str) -> tuple:
    """Return (category, priority)."""
    p = rel_path.replace("\\", "/")
    lower = p.lower()

    # 产业链体系（119 条链，自动分类，无需硬编码）
    ci = chain_slug_of(p)
    if ci:
        return ci[1], 40

    if "berkshire-ai-chain" in lower and "coming" not in lower:
        return "AI产业链", 40

    if "berkshire-robot-chain" in lower and "coming" not in lower:
        return "机器人产业链", 40
    if "berkshire-baijiu-methodology" in lower or "berkshire-baijiu-cycle" in lower or "berkshire-baijiu-backtest" in lower or "berkshire-baijiu-thermometer" in lower or "berkshire-baijiu-backtest-detail" in lower:
        return "白酒产业链", 40
    if "berkshire-baijiu-chain" in lower and "coming" not in lower:
        return "白酒产业链", 40
    if "berkshire-tcm-chain" in lower and "coming" not in lower:
        return "中药产业链", 40
    if "berkshire-innov-chain" in lower and "coming" not in lower:
        return "创新药产业链", 40
    if "berkshire-appliance-chain" in lower and "coming" not in lower:
        return "家电产业链", 40
    if "berkshire-power-chain" in lower and "coming" not in lower:
        return "电力产业链", 40
    if "berkshire-coal-chain" in lower and "coming" not in lower:
        return "煤炭产业链", 40
    if "berkshire-metal-chain" in lower and "coming" not in lower:
        return "有色产业链", 40
    if "berkshire-chem-chain" in lower and "coming" not in lower:
        return "化工产业链", 40
    if "berkshire-equip-chain" in lower and "coming" not in lower:
        return "电力设备产业链", 40
    if "berkshire-bank" in lower and "coming" not in lower:
        return "银行业图谱", 40
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
            if "booklist" in lower:
                return "归江书单", 12
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
        "berkshire-changying-booklist.html": ("指数投资", 28),
        "berkshire-stress-test.html": ("指数投资", 1),
        "berkshire-value-investors.html": ("价值投资人物", 17),
        "berkshire-pabrai-index.html": ("帕伯莱演讲", 12),
        "berkshire-guijiang-index.html": ("归江文章", 12),
        "berkshire-guijiang-booklist.html": ("归江书单", 12),
        "berkshire-duan-index.html": ("段永平思想", 12),
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
        "berkshire-ai-chains.html": ("AI产业链", 40),
        "berkshire-ai-chain-nvidia.html": ("AI产业链", 40),
        "berkshire-ai-chain-apple.html": ("AI产业链", 40),
        "berkshire-ai-chain-microsoft.html": ("AI产业链", 40),
        "berkshire-ai-chain-google.html": ("AI产业链", 40),
        "berkshire-ai-chain-amazon.html": ("AI产业链", 40),
        "berkshire-ai-chain-meta.html": ("AI产业链", 40),
        "berkshire-ai-chain-tesla.html": ("AI产业链", 40),
        "berkshire-ai-chain-ali.html": ("AI产业链", 40),
        "berkshire-ai-chain-tencent.html": ("AI产业链", 40),
        "berkshire-ai-chain-bytedance.html": ("AI产业链", 40),
        "berkshire-ai-chain-huawei.html": ("AI产业链", 40),
        "berkshire-ai-chain-baidu.html": ("AI产业链", 40),
        "berkshire-ai-chain-power.html": ("AI产业链", 40),
        "berkshire-robot-chains.html": ("机器人产业链", 40),
        "berkshire-robot-chain-tesla.html": ("机器人产业链", 40),
        "berkshire-baijiu-chains.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-maotai.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-wuliangye.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-luzhou.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-fenjiu.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-yanghe.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-gujing.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-jinshiyuan.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-shede.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-yingjia.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-shuijingfang.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-jiugui.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-kouzijiao.html": ("白酒产业链", 40),
        "berkshire-baijiu-chain-shunxin.html": ("白酒产业链", 40),
        "berkshire-baijiu-methodology.html": ("白酒产业链", 40),
        "berkshire-baijiu-cycle.html": ("白酒产业链", 40),
        "berkshire-baijiu-backtest.html": ("白酒产业链", 40),
        "berkshire-baijiu-thermometer.html": ("白酒产业链", 40),
        "berkshire-baijiu-backtest-detail.html": ("白酒产业链", 40),
        "berkshire-bank-chains.html": ("银行业图谱", 40),
        "berkshire-bank-chain-icbc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-ccb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-abc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-boc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-bocom.html": ("银行业图谱", 40),
        "berkshire-bank-chain-psbc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-cmb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-citic.html": ("银行业图谱", 40),
        "berkshire-bank-chain-spdb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-indy.html": ("银行业图谱", 40),
        "berkshire-bank-chain-cmbc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-ceb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-hxb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-pab.html": ("银行业图谱", 40),
        "berkshire-bank-chain-czb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-bobj.html": ("银行业图谱", 40),
        "berkshire-bank-chain-njcb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-nib.html": ("银行业图谱", 40),
        "berkshire-bank-chain-shb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-jsb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-hzb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-cdb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-csb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-cqb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-qdb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-zzb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-szb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-xab.html": ("银行业图谱", 40),
        "berkshire-bank-chain-xmb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-qlb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-gyb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-lzb.html": ("银行业图谱", 40),
        "berkshire-bank-chain-cqrc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-qrc.html": ("银行业图谱", 40),
        "berkshire-bank-chain-changshu.html": ("银行业图谱", 40),
        "berkshire-bank-chain-zijin.html": ("银行业图谱", 40),
        "berkshire-bank-chain-wuxi.html": ("银行业图谱", 40),
        "berkshire-bank-chain-zjg.html": ("银行业图谱", 40),
        "berkshire-bank-chain-sunong.html": ("银行业图谱", 40),
        "berkshire-bank-chain-jiangyin.html": ("银行业图谱", 40),
        "berkshire-bank-chain-ruifeng.html": ("银行业图谱", 40),
        "berkshire-bank-chain-shnc.html": ("银行业图谱", 40),
        "berkshire-bank-methodology.html": ("银行业图谱", 40),
        "berkshire-bank-cycle.html": ("银行业图谱", 40),
        "berkshire-bank-backtest.html": ("银行业图谱", 40),
        "berkshire-bank-thermometer.html": ("银行业图谱", 40),
        "berkshire-bank-backtest-detail.html": ("银行业图谱", 40),
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

        chain_info = chain_slug_of(rel)
        category, priority = categorize(rel, title)

        if chain_info and chain_info[2] in ("detail", "co"):
            # 公司页：用结构化指标摘要代替正文截断（体积 ↓90%，可读性 ↑）
            slug, cname, kind = chain_info
            sep = "chain" if kind == "detail" else "co"
            cm = re.match(rf"berkshire-{re.escape(slug)}-{sep}-(.+)\.html$", rel.split("/")[-1])
            code = cm.group(1) if cm else ""
            if kind == "detail":
                comp, snippet, search_text = chain_detail_summary(html, cname, code)
            else:
                comp, snippet, search_text = co_summary(html, cname, code)
            headings = []
            tags = [x for x in [code if code.isdigit() else None, cname, comp] if x]
            if comp:
                title = f"{comp}（{code}）· {cname}" if code.isdigit() else f"{comp} · {cname}"
            entries.append({
                "title": title, "url": rel, "category": category, "priority": priority,
                "description": snippet, "searchText": search_text,
                "headings": headings, "tags": tags,
            })
            continue

        headings = extract_headings(html)

        if chain_info and chain_info[2] in ("compare", "thermometer"):
            # 子工具页：短摘要即可
            snippet = extract_snippet(html, max_chars=140)
            search_text = extract_search_text(html, max_chars=260)
        elif any(x in rel.lower() for x in ["meetings_content/full", "letters_content/cn", "value-investors-content"]):
            snippet = extract_snippet(html, max_chars=180)
            search_text = extract_search_text(html, max_chars=1000)
        elif chain_info:
            snippet = extract_snippet(html, max_chars=200)
            search_text = extract_search_text(html, max_chars=400)
        else:
            snippet = extract_snippet(html, max_chars=260)
            search_text = extract_search_text(html, max_chars=800)

        tags = build_tags(title, snippet, headings, rel)
        if chain_info:
            headings = headings[:2]
            if chain_info[1] not in tags:
                tags = [chain_info[1]] + tags
            tags = tags[:6]

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

    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    print(f"Generated {OUTPUT}: {len(entries)} entries")


if __name__ == "__main__":
    main()
