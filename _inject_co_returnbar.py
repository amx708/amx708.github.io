# -*- coding: utf-8 -*-
"""
给全站 co 页（企业总览页）注入 sticky 返回栏按钮组。
- 返回目标：产业链 co -> berkshire-<slug>-chains.html；commodity-co -> articles/price-hike-monitor.html
- 按钮组插进现有 .topbar-in（右侧，margin-left:auto），CSS 注入 <style> 前
- 幂等：已含 top-actions 标记则跳过
"""
import os, re, glob

WS = r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44"
DEPLOY = os.path.join(WS, "deploy_site")

CSS = """
/*co-sticky-return*/.top-actions{margin-left:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.top-actions .tret{text-decoration:none;font-size:13px;padding:5px 11px;border-radius:7px;font-weight:500;white-space:nowrap;border:1px solid var(--line);color:var(--mut);transition:.15s}
.top-actions .tret:hover{color:var(--accent);background:var(--soft);border-color:var(--accent)}
.top-actions .tret.back{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
.top-actions .tret.back:hover{background:var(--accent-light);color:#fff}
"""

MARK = "top-actions"  # 幂等标记


def derive_return(fname):
    base = fname[:-5]  # strip .html
    parts = base.split("-")  # berkshire, slug..., 'co', code
    idx = parts.index("co")
    slug = "-".join(parts[1:idx])
    if slug == "commodity":
        return "articles/price-hike-monitor.html"
    target = f"berkshire-{slug}-chains.html"
    if os.path.exists(os.path.join(DEPLOY, target)):
        return target
    return "berkshire-standalone.html"  # 兜底：父索引缺失则回枢纽


def inject(html, ret):
    if MARK in html:
        return html, False
    # 1) CSS 注入 <style> 前
    if "</style>" in html:
        html = html.replace("</style>", CSS + "</style>", 1)
    # 2) 按钮组注入 topbar-in（crumb 之后、topbar-in 闭合前）
    btns = ('<div class="top-actions">'
            f'<a class="tret back" href="{ret}">← 返回</a>'
            '<a class="tret" href="berkshire-standalone.html">站点枢纽</a>'
            '<a class="tret" href="index.html">首页</a>'
            '</div>')
    new_html, n = re.subn(
        r'(<div class="topbar-in">[\s\S]*?</div>)</div></div>',
        lambda m: m.group(1) + btns + '</div></div>',
        html, count=1)
    if n == 0:
        return html, False
    return new_html, True


def main():
    files = sorted(glob.glob(os.path.join(DEPLOY, "berkshire-*-co-*.html")))
    changed = []
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            html = f.read()
        ret = derive_return(os.path.basename(fp))
        new_html, ok = inject(html, ret)
        if ok:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_html)
            changed.append(os.path.relpath(fp, DEPLOY).replace("\\", "/"))
    out = os.path.join(DEPLOY, "_co_returnbar_changed.txt")
    with open(out, "w", encoding="utf-8") as f:
        for p in changed:
            f.write(p + "\n")
    print(f"total co pages scanned={len(files)}; changed={len(changed)}")
    print("list ->", out)


if __name__ == "__main__":
    main()
