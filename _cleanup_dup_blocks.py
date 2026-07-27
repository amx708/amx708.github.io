# -*- coding: utf-8 -*-
"""_cleanup_dup_blocks.py —— 一次性清理 PEG/分红再投 块的重复注入并补 id 标记。
原因：早期注入器幂等标记(peg-block/div-compound-block)未写入 HTML，导致分红注入器
两次运行(先R15锚点22页、后通用锚点64页)把 coal/power 22 页重复注入。
修复：每页每个块只保留第一份，并给保留块的 <div class="fin-block"> 加 id 标记。
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

BLOCKS = [
    # (section-title 前缀, fin-block 的 id 标记)
    ("PEG（林奇成长性估值）", "peg-block"),
    ("分红再投 10 年复利", "div-compound-block"),
]


def dedup_page(html, title_prefix, marker_id):
    # 匹配从本块 section-title 到下一个 section-title 之间的全部内容（含本块）
    pat = re.compile(r'<div class="section-title">' + re.escape(title_prefix) +
                     r'.*?(?=<div class="section-title">)', re.S)
    matches = list(pat.finditer(html))
    if not matches:
        return html, 0
    # 保留第一份，删除其余
    for m in matches[1:]:
        html = html[:m.start()] + html[m.end():]
    # 给保留块加 id 标记（若还没有）
    keep = matches[0]
    seg = html[keep.start():keep.end()]
    if marker_id not in seg:
        seg2 = seg.replace('<div class="fin-block"',
                            '<div class="fin-block" id="%s"' % marker_id, 1)
        html = html[:keep.start()] + seg2 + html[keep.end():]
    return html, len(matches)


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, "berkshire-*-chain-*.html")))
    total_dup = 0
    fixed = 0
    for p in pages:
        html = open(p, encoding="utf-8").read()
        orig = html
        for prefix, mid in BLOCKS:
            html, n = dedup_page(html, prefix, mid)
            if n > 1:
                total_dup += (n - 1)
        if html != orig:
            open(p, "w", encoding="utf-8").write(html)
            fixed += 1
    print("处理页数:", len(pages), " 修正(去重)页数:", fixed, " 移除重复块数:", total_dup)


if __name__ == "__main__":
    main()
