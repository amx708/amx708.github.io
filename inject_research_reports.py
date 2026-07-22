# -*- coding: utf-8 -*-
"""
inject_research_reports.py  ——  伯克希尔数据中心 · chain 管线步骤

把 data/chain_research_reports.json（各公司券商研报链接）注入到每家公司的
chain 详情页（berkshire-{chain}-chain-{slug}.html）的「研报」区。

设计要点：
1. 复用 inject_annual_reports.extract_chain_slug_code 建立 (chain, slug) -> code 映射；
2. 用 code 去研报 JSON 取研报列表；
3. 注入位置：若页面已有「年报区」(id="annual-reports")，则插在它之后；
   否则按 back-bar / footer / </body> 兜底锚点插入；
4. 幂等：页面已含 id="research-reports" 则跳过；
5. 港股在东方财富该接口取不到研报，JSON 中无对应条目 -> 按「无数据」跳过。

用法：
    python inject_research_reports.py
"""
import glob
import json
import os
import re

from inject_annual_reports import extract_chain_slug_code

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "chain_research_reports.json")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def build_section(entry):
    reports = entry.get("reports") or []
    if not reports:
        return ""
    name = entry.get("name", "")
    rows = []
    for r in reports:
        title = esc(r.get("title", ""))
        org = esc(r.get("org", ""))
        rating = esc(r.get("rating", ""))
        date = esc(r.get("date", ""))
        url = esc(r.get("url", ""))
        if not url:
            continue
        meta = " · ".join([x for x in [org, rating, date] if x])
        rows.append(
            '<a href="%s" target="_blank" rel="noopener" '
            'style="display:block;padding:9px 12px;background:#f8fafc;border:1px solid #e2e8f0;'
            'border-radius:8px;text-decoration:none;color:#0f172a;transition:.15s">'
            '<div style="font-size:13.5px;font-weight:600;line-height:1.45;margin-bottom:3px;'
            'color:#1e293b">%s</div>'
            '<div style="font-size:12px;color:#64748b">%s</div></a>' % (url, title, meta)
        )
    if not rows:
        return ""
    return (
        '<div id="research-reports" style="margin-top:28px;padding-top:10px">'
        '<div style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:10px;'
        'display:flex;align-items:center;gap:8px"><span style="font-size:18px">📊</span> '
        '券商研报（东方财富）</div>'
        '<p style="font-size:12.5px;color:#64748b;margin:0 0 12px;line-height:1.6">'
        '下方为机构近期研究报告（来源：东方财富网）。研报版权归原券商所有，本页仅作链接聚合、'
        '不托管文件，点击直达东方财富托管原文。仅供参考，不构成投资建议。</p>'
        '<div style="display:flex;flex-direction:column;gap:8px">%s</div></div>' % "".join(rows)
    )


def inject_into_page(path, html, section):
    if 'id="research-reports"' in html:
        return html, False
    # 优先插在年报区之后（按 div 嵌套深度精确找年报区真正闭合标签，
    # 避免误插进年报区内部的 chips 容器 div 里）
    if 'id="annual-reports"' in html:
        open_tag = '<div id="annual-reports"'
        i = html.find(open_tag)
        if i != -1:
            depth = 0
            j = i
            close_end = None
            while j < len(html):
                nxt_open = html.find("<div", j)
                nxt_close = html.find("</div>", j)
                if nxt_close == -1:
                    break
                if nxt_open != -1 and nxt_open < nxt_close:
                    depth += 1
                    j = nxt_open + 4
                else:
                    if depth == 0:
                        close_end = nxt_close + len("</div>")
                        break
                    depth -= 1
                    j = nxt_close + 6
            if close_end is not None:
                new_html = html[:close_end] + "\n" + section + html[close_end:]
                return new_html, True
    # 兜底锚点
    anchor = None
    if '<div class="back-bar">' in html:
        anchor = '<div class="back-bar">'
    elif '<footer>' in html:
        idx = html.rfind('<footer>')
        anchor = html[idx:idx + len('<footer>')]
    if anchor:
        new_html = html.replace(anchor, section + "\n" + anchor, 1)
    else:
        new_html = html.replace('</body>', section + "\n</body>", 1)
    return new_html, True


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    code2rep = {c["code"]: c for c in data}
    chain_slug_code = extract_chain_slug_code()

    pages = sorted(glob.glob(os.path.join(ROOT, "berkshire-*-chain-*.html")))
    done = skipped_no_data = skipped_existing = 0
    injected_list = []

    for p in pages:
        m = re.search(r"berkshire-([a-z]+)-chain-([A-Za-z0-9_\-]+)\.html$", p)
        if not m:
            continue
        chain, slug = m.group(1), m.group(2)
        code = chain_slug_code.get((chain, slug))
        rep = code2rep.get(code) if code else None
        html = open(p, encoding="utf-8").read()

        if not rep or not rep.get("reports"):
            skipped_no_data += 1
            continue

        section = build_section(rep)
        if not section:
            skipped_no_data += 1
            continue
        new_html, injected = inject_into_page(p, html, section)
        if injected:
            open(p, "w", encoding="utf-8").write(new_html)
            done += 1
            injected_list.append((os.path.basename(p), rep["name"], len(rep["reports"])))
        else:
            skipped_existing += 1

    print("=== 研报区注入完成 ===")
    print("成功注入页面数 :", done)
    print("已存在跳过     :", skipped_existing)
    print("无研报数据跳过 :", skipped_no_data)
    print()
    print("--- 已注入（前 25）---")
    for f, n, c in injected_list[:25]:
        print("  %-45s %s (%d条)" % (f, n, c))


if __name__ == "__main__":
    main()
