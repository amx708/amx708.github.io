# -*- coding: utf-8 -*-
"""
_inject_peg.py —— 伯克希尔数据中心 · P2-C 增强
把 data/chain_peg.json 的 PEG 数据注入成长链(AI/创新药/机器人/有色)详情页估值段。

锚点：<div class="section-title">R15 三维评级</div> 之前（全 12 链通用，估值段紧邻）。
幂等：已含 `peg-block` 标记则跳过。
样式复用页面既有 .fin-block/.fin-head/.fin-title/.fin-table/.fin-note（全站通用）。
"""
import os, re, json, glob
import inject_annual_reports as ia

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
PEG = os.path.join(DATA, "chain_peg.json")


def peg_verdict(peg):
    if peg is None:
        return "不适用"
    if peg < 1:
        return "估值相对成长性偏低（林奇：便宜的成长）"
    if peg <= 2:
        return "估值与成长性大致匹配（合理区间）"
    return "成长已被较充分定价（偏贵）"


def block(d):
    pe = d.get("pe_ttm")
    g = d.get("g_cagr")
    peg = d.get("peg")
    note = d.get("note", "")
    name = d.get("name", "")
    pe_s = ("%.2f" % pe) if pe is not None else "—"
    g_s = ("%.1f%%" % g) if g is not None else "—"
    peg_s = ("%.2f" % peg) if peg is not None else "N/A"
    verdict = peg_verdict(peg)
    rows = (
        '<tr><td>PE（TTM）</td><td><b>%s</b> 倍</td></tr>'
        '<tr><td>净利近 3 年 CAGR</td><td><b>%s</b></td></tr>'
        '<tr><td>PEG（PE ÷ 增速）</td><td><b style="color:#1d4ed8">%s</b></td></tr>'
    ) % (pe_s, g_s, peg_s)
    if peg is None:
        rows += '<tr><td>说明</td><td>%s</td></tr>' % note
    else:
        rows += '<tr><td>林奇解读</td><td>%s</td></tr>' % verdict
    return (
        '<div class="section-title">PEG（林奇成长性估值）</div>\n'
        '<div class="fin-block" id="peg-block" style="border-left:3px solid #22d3ee">\n'
        '  <div class="fin-head"><div class="fin-title"><span class="icon">📈</span> PEG = PE ÷ 净利增速</div>'
        '<span class="fin-tag">林奇透镜</span></div>\n'
        '  <table class="fin-table"><tbody>%s</tbody></table>\n'
        '  <div class="fin-note">PEG 由本站用 PE(TTM) 与近 3 年扣非净利 CAGR 估算（数据源：百度股市通 / 东方财富财务分析），'
        '为框架级估值透镜、随行情与财报变动，<b>非买卖建议</b>。PEG&lt;1 偏便宜、1–2 合理、&gt;2 偏贵；'
        '亏损或增速为负的企业 PEG 不适用。</div>\n'
        '</div>\n'
    ) % rows


def main():
    data = json.load(open(PEG, encoding="utf-8"))
    cmap = ia.extract_chain_slug_code()
    code2page = {}
    for (chain, slug), code in cmap.items():
        code2page[code] = "berkshire-%s-chain-%s.html" % (chain, slug)
    done, skipped, noanchor, nopage = 0, 0, 0, 0
    for code, d in sorted(data.items()):
        page = code2page.get(code)
        if not page or not os.path.exists(os.path.join(ROOT, page)):
            nopage += 1
            continue
        p = os.path.join(ROOT, page)
        html = open(p, encoding="utf-8").read()
        if "peg-block" in html:
            skipped += 1
            continue
        anchor = '<div class="section-title">R15 三维评级</div>'
        if anchor not in html:
            noanchor += 1
            continue
        b = block(d)
        new = html.replace(anchor, b + anchor, 1)
        open(p, "w", encoding="utf-8").write(new)
        done += 1
    print("=== PEG 注入完成 ===")
    print("注入:", done, " 跳过(已存在):", skipped, " 无R15锚点:", noanchor, " 无页面:", nopage)


if __name__ == "__main__":
    main()
