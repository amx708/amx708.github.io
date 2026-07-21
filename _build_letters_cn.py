#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 pzponge/Yestoday 批量下载伯克希尔股东信中英对照 Markdown，
转换为站内单文件 HTML（letters_content/cn/<year>.html）。
"""
import os, re, textwrap, urllib.request
from markdown import markdown

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "letters_content", "cn")
BASE_URL = "https://raw.githubusercontent.com/pzponge/Yestoday/main/Warren_Buffett/"
os.makedirs(OUT_DIR, exist_ok=True)

# 1971-2024 股东信：默认与特殊文件名
SPECIAL = {
    2025: "Berkshire_Hathaway_Letters/2025_Annual_Thanksgiving_Message_2.md",
}

# 1957-1970 合伙基金时期年度信（芒格书院共读群友 ChengMing 整理版）
PARTNERSHIP_FILES = {
    1957: "Buffett_Partnership_Letters/ChengMing/1957_Letter_to_Limited_Partners_CM.md",
    1958: "Buffett_Partnership_Letters/ChengMing/1958_Letter_to_Limited_Partners_CM.md",
    1959: "Buffett_Partnership_Letters/ChengMing/1959_Letter_to_Limited_Partners_CM.md",
    1960: "Buffett_Partnership_Letters/ChengMing/1960_Letter_to_Limited_Partners_CM.md",
    1961: "Buffett_Partnership_Letters/ChengMing/1961_Letter_to_Limited_Partners_CM.md",
    1962: "Buffett_Partnership_Letters/ChengMing/1962_Letter_to_Limited_Partners_CM.md",
    1963: "Buffett_Partnership_Letters/ChengMing/1963_Letter_to_Limited_Partners_CM.md",
    1964: "Buffett_Partnership_Letters/ChengMing/1964_Letter_to_Limited_Partners_CM.md",
    1965: "Buffett_Partnership_Letters/ChengMing/1965_Letter_to_Limited_Partners_CM.md",
    1966: "Buffett_Partnership_Letters/ChengMing/1966_Letter_to_Limited_Partners_CM.md",
    1967: "Buffett_Partnership_Letters/ChengMing/1967_Letter_to_Limited_Partners_CM.md",
    1968: "Buffett_Partnership_Letters/ChengMing/1968_Letter_to_Limited_Partners_CM.md",
    1969: "Buffett_Partnership_Letters/ChengMing/1969_May_Letter_to_Limited_Partners_CM.md",
    1970: "Buffett_Partnership_Letters/ChengMing/1970_February_25th_Letter_to_Limited_Partners_CM.md",
}

def filename_for(year):
    if 1957 <= year <= 1970:
        return PARTNERSHIP_FILES[year]
    return SPECIAL.get(year, f"Berkshire_Hathaway_Letters/{year}_Letter_to_Berkshire_Shareholders.md")

YEARS = list(range(1957, 2025))  # 1957-2024
# 2025 可选；先不做，因为页面标题只到 2024

def fetch(year):
    fn = filename_for(year)
    url = BASE_URL + fn
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            md = r.read().decode("utf-8")
            # 修复源 md 中偶见的错误标签（1988 年表格中的孤立 </be>）
            md = md.replace("</be>", "")
            return md, fn
    except Exception as e:
        print(f"[ERR] {year} {fn}: {e}")
        return None, fn

META_RE = re.compile(r"^-\s*(标题|作者|发表时间|链接|中文翻译参考|整理|修订|中文翻译)\s*[:：]\s*(.*)$", re.M)

def parse_meta(md):
    meta = {}
    body = md
    if "原文信息：" in md:
        parts = md.split("原文信息：", 1)
        rest = parts[1].lstrip()
        # 元信息块结束于第一个空行、--- 分隔符或正文标题
        end_pos = len(rest)
        for sep in ("\n\n", "\n---\n", "\n# "):
            idx = rest.find(sep)
            if idx != -1 and idx < end_pos:
                end_pos = idx
        head = rest[:end_pos]
        body = rest[end_pos:].lstrip()
        # 去除可能残留的 --- 分隔线
        body = re.sub(r"^---+\s*\n+", "", body)
        for k, v in META_RE.findall(head):
            meta[k] = v.strip()
    return meta, body

def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def fix_links(html, year):
    # 外部 PDF 链接保留，相对 .md 链接改为站内或移除
    # 1) 相对 md 链接（如 伯克希尔哈撒韦股东信翻译更新日志.md）改为 # 或去掉 href
    html = re.sub(r'href="([^"]+\.md)"', r'href="#"', html)
    # 2) 外部 http(s) 链接加 target="_blank" rel="noopener"
    def ext(m):
        url = m.group(1)
        if url.startswith(("http://", "https://")):
            return f'href="{html_escape(url)}" target="_blank" rel="noopener"'
        return m.group(0)
    html = re.sub(r'href="([^"]+)"', ext, html)
    return html

def build_html(year, meta, body_html, prev_year, next_year):
    title = meta.get("标题", f"{year} Letter to Berkshire Shareholders")
    author = meta.get("作者", "Warren Buffett")
    date = meta.get("发表时间", "")
    trans = meta.get("中文翻译参考", meta.get("中文翻译", ""))
    editor = meta.get("整理", "")
    reviser = meta.get("修订", "")
    source_link = meta.get("链接", "")

    meta_items = []
    if title:
        meta_items.append(("标题", title))
    if author:
        meta_items.append(("作者", author))
    if date:
        meta_items.append(("发表时间", date))
    if trans:
        meta_items.append(("中文翻译", trans))
    if editor:
        meta_items.append(("整理", editor))
    if reviser:
        meta_items.append(("修订", reviser))
    if source_link:
        # 提取 markdown 链接文本和 URL
        m = re.search(r'\[([^\]]+)\]\(([^\)]+)\)', source_link)
        if m:
            meta_items.append(("原文", f'<a href="{html_escape(m.group(2))}" target="_blank" rel="noopener">{html_escape(m.group(1))}</a>'))
        else:
            meta_items.append(("原文", source_link))

    meta_html = "\n".join(f'<div class="m-row"><span class="m-k">{k}</span><span class="m-v">{v}</span></div>' for k, v in meta_items)

    nav_prev = f'<a class="nav-link" href="{prev_year}.html">← {prev_year}</a>' if prev_year else '<span class="nav-link disabled">←</span>'
    nav_next = f'<a class="nav-link" href="{next_year}.html">{next_year} →</a>' if next_year else '<span class="nav-link disabled">→</span>'

    if 1957 <= year <= 1970:
        display_title = f"{year} 年致合伙人的信"
    elif year == 2025:
        display_title = "2025 年感恩节致股东信"
    else:
        display_title = f"{year} 年致伯克希尔股东的信"

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{display_title} | 伯克希尔投资数据中心</title>
<style>
:root{{--navy:#0b1f3a;--navy2:#102a4c;--orange:#f5a623;--orange2:#ffb84d;--ink:#1a2433;--muted:#6b7a90;--line:#e3e9f2;--bg:#f4f7fb;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.75}}
a{{color:var(--navy2)}}
a:hover{{color:var(--orange)}}
header.top{{position:sticky;top:0;z-index:30;background:rgba(11,31,58,.85);backdrop-filter:blur(10px);border-bottom:1px solid rgba(245,166,35,.35)}}
.top-in{{max-width:980px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}}
.crumb{{color:#9fb3cf;font-size:13px}}
.crumb a{{color:#9fb3cf;text-decoration:none}}
.crumb a:hover{{color:var(--orange2)}}
.top h1{{margin:0;font-size:18px;color:#fff;font-weight:700}}
.top h1 b{{color:var(--orange)}}
.wrap{{max-width:980px;margin:0 auto;padding:28px 20px 60px}}
.page-title{{margin:0 0 6px;font-size:28px;color:var(--navy)}}
.page-sub{{margin:0 0 20px;color:var(--muted);font-size:15px}}
.meta-card{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:24px}}
.m-row{{display:flex;gap:12px;padding:5px 0;font-size:14px;border-bottom:1px solid #f0f3f8}}
.m-row:last-child{{border-bottom:none}}
.m-k{{color:var(--muted);min-width:80px;flex-shrink:0}}
.m-v{{color:var(--ink);flex:1}}
.m-v a{{color:var(--navy2)}}
.body{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:28px 32px}}
.body h1{{font-size:20px;color:var(--navy);margin:28px 0 14px;padding-left:12px;border-left:4px solid var(--orange)}}
.body h1:first-child{{margin-top:0}}
.body h2{{font-size:17px;color:var(--navy2);margin:24px 0 10px}}
.body p{{margin:0 0 14px}}
.body p.en{{color:#4a5568;background:#f8fafc;padding:10px 14px;border-radius:8px;font-style:italic}}
.body p.zh{{color:var(--ink);padding:0 14px}}
.body ul,.body ol{{padding-left:24px;margin:0 0 14px}}
.body li{{margin:6px 0}}
.body hr{{border:none;border-top:1px solid var(--line);margin:24px 0}}
.body blockquote{{margin:14px 0;padding:12px 16px;background:#f8fafc;border-left:3px solid var(--orange);color:#4a5568}}
.body sup{{color:var(--orange);font-weight:700}}
.view-bar{{display:flex;align-items:center;gap:10px;margin:0 0 18px;flex-wrap:wrap}}
.view-label{{color:var(--muted);font-size:14px}}
.view-btn{{padding:8px 16px;border:1px solid var(--line);background:#fff;color:var(--navy2);border-radius:20px;font-size:14px;cursor:pointer;transition:.15s;font-family:inherit}}
.view-btn:hover{{border-color:var(--orange)}}
.view-btn.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.body.view-zh .en{{display:none}}
.body.view-en .zh{{display:none}}
.nav{{display:flex;justify-content:space-between;align-items:center;margin-top:28px}}
.nav-link{{display:inline-block;padding:10px 18px;background:var(--navy);color:#fff;text-decoration:none;border-radius:10px;font-size:14px;transition:.15s}}
.nav-link:hover{{background:var(--orange);color:#fff}}
.nav-link.disabled{{background:#d1d9e6;color:#fff;cursor:default}}
footer{{max-width:980px;margin:0 auto;padding:24px 20px 50px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line)}}
@media(max-width:640px){{.body{{padding:18px 16px}}.top h1{{font-size:16px}}}}
</style>
</head>
<body>
<header class="top">
  <div class="top-in">
    <h1>伯克希尔·<b>投资数据中心</b></h1>
    <div class="crumb"><a href="../../berkshire-standalone.html">首页</a> / <a href="../../berkshire-letters.html">历年致股东的信</a> / {year}</div>
  </div>
</header>
<div class="wrap">
  <h1 class="page-title">{display_title}</h1>
  <div class="view-bar">
    <span class="view-label">阅读版本：</span>
    <button class="view-btn active" data-v="zh" onclick="setView('zh')">中文</button>
    <button class="view-btn" data-v="both" onclick="setView('both')">中英文对照</button>
    <button class="view-btn" data-v="en" onclick="setView('en')">英文原文</button>
  </div>
  <p class="page-sub">中文 · 中英文对照 · 英文原文（中文为首选）· 来源：芒格书院共读群友整理</p>
  <div class="meta-card">{meta_html}</div>
  <article class="body letter-body view-zh" id="letter-body">
{body_html}
  </article>
  <div class="nav">
    {nav_prev}
    <a class="nav-link" href="../../berkshire-letters.html">返回年份列表</a>
    {nav_next}
  </div>
</div>
<footer>
  本页中文翻译来自芒格书院共读群友整理，仅供学习交流。英文原文版权归 Berkshire Hathaway Inc. 所有。
</footer>
<script>
var CJK = /[一-鿿㐀-䶿]/;
function isCJK(ch){{ return CJK.test(ch); }}
function setView(v){{
  var b = document.getElementById('letter-body');
  b.classList.remove('view-zh','view-both','view-en');
  b.classList.add('view-' + v);
  document.querySelectorAll('.view-btn').forEach(function(x){{ x.classList.toggle('active', x.dataset.v === v); }});
}}
// 段落与列表项：按是否含中文归类为 zh / en
document.querySelectorAll('#letter-body p, #letter-body li').forEach(function(p){{
  p.classList.add(CJK.test(p.textContent) ? 'zh' : 'en');
}});
// 标题：把中文与英文拆成不同 span，便于按版本显隐
document.querySelectorAll('#letter-body h1, #letter-body h2, #letter-body h3').forEach(function(h){{
  var txt = h.textContent, runs = [], cur = '', curCJK = null;
  for (var i = 0; i < txt.length; i++){{
    var c = txt[i], cjk = isCJK(c);
    if (curCJK === null) {{ cur = c; curCJK = cjk; }}
    else if (cjk === curCJK) {{ cur += c; }}
    else {{ runs.push([curCJK, cur]); cur = c; curCJK = cjk; }}
  }}
  if (cur) runs.push([curCJK, cur]);
  h.innerHTML = '';
  runs.forEach(function(r){{
    var s = document.createElement('span');
    s.className = r[0] ? 'zh' : 'en';
    s.textContent = r[1];
    h.appendChild(s);
  }});
}});
setView('zh');
</script>
</body>
</html>'''
    return html

def main():
    for i, year in enumerate(YEARS):
        print(f"[{year}] downloading...")
        md, fn = fetch(year)
        if md is None:
            continue
        meta, body = parse_meta(md)
        body_md = body.strip()
        # markdown 转换
        body_html = markdown(body_md, extensions=['fenced_code', 'tables', 'toc'])
        body_html = fix_links(body_html, year)
        # 增加缩进
        body_html = textwrap.indent(body_html, '    ')
        prev_year = YEARS[i-1] if i > 0 else None
        next_year = YEARS[i+1] if i < len(YEARS)-1 else None
        html = build_html(year, meta, body_html, prev_year, next_year)
        out_path = os.path.join(OUT_DIR, f"{year}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[{year}] wrote {out_path}")

if __name__ == "__main__":
    main()
