# -*- coding: utf-8 -*-
"""
_inject_dividend_compound.py —— 伯克希尔数据中心 · P2-D 增强
把 data/chain_dividend_compound.json 的「分红再投 10 年复利」注入现金牛链(煤炭/银行/电力)详情页估值段。

锚点：<div class="section-title">R15 三维评级</div> 之前（全 12 链通用）。
幂等：已含 `div-compound-block` 标记则跳过。
样式复用 .fin-block/.fin-head/.fin-title/.fin-table/.fin-note。
"""
import os, re, json
import inject_annual_reports as ia

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
DIV = os.path.join(DATA, "chain_dividend_compound.json")


def pct(x):
    return ("%.1f%%" % (x * 100)) if x is not None else "—"


def block(d):
    hfq = d.get("hfq_ret")
    price = d.get("price_ret")
    contrib = d.get("div_contrib")
    ann_h = d.get("ann_hfq")
    ann_p = d.get("ann_price")
    years = d.get("years", 10)
    pv = 10000 * (1 + hfq) if hfq is not None else None
    rows = (
        '<tr><td>统计区间</td><td>2016 → 2026（约 %d 年）</td></tr>'
        '<tr><td>分红再投年化</td><td><b style="color:#15803d">%s</b></td></tr>'
        '<tr><td>纯价回报年化</td><td><b>%s</b></td></tr>'
        '<tr><td>分红再投贡献</td><td><b>+%s</b>（总回报差额）</td></tr>'
        '<tr><td>情景</td><td>10 年前投 1 万元并分红再投 → 现值约 <b>%s 元</b></td></tr>'
    ) % (years, pct(ann_h), pct(ann_p), pct(contrib),
         ("{:,}".format(int(pv)) if pv is not None else "—"))
    return (
        '<div class="section-title">分红再投 10 年复利（现金牛情景）</div>\n'
        '<div class="fin-block" id="div-compound-block" style="border-left:3px solid #84cc16">\n'
        '  <div class="fin-head"><div class="fin-title"><span class="icon">💰</span> 分红再投 vs 纯价回报</div>'
        '<span class="fin-tag">复利透镜</span></div>\n'
        '  <table class="fin-table"><tbody>%s</tbody></table>\n'
        '  <div class="fin-note">后复权(hfq)口径已内含分红再投与送转（数据源：新浪日线，2016-01 至 2026-07）。'
        '分红贡献 = 后复权总回报 − 纯价回报。框架级情景、随行情与分红政策变动，<b>非买卖建议</b>。</div>\n'
        '</div>\n'
    ) % rows


def main():
    data = json.load(open(DIV, encoding="utf-8"))
    cmap = ia.extract_chain_slug_code()
    code2page = {code: "berkshire-%s-chain-%s.html" % (chain, slug)
                 for (chain, slug), code in cmap.items()}
    done, skipped, noanchor, nopage = 0, 0, 0, 0
    for code, d in sorted(data.items()):
        page = code2page.get(code)
        if not page or not os.path.exists(os.path.join(ROOT, page)):
            nopage += 1
            continue
        p = os.path.join(ROOT, page)
        html = open(p, encoding="utf-8").read()
        if "div-compound-block" in html:
            skipped += 1
            continue
        # 通用锚点：估值历史分位段之后、下一个 section-title 之前（覆盖银行无R15的页）
        idx = html.find("估值历史分位")
        if idx < 0:
            noanchor += 1
            continue
        nxt = html.find('<div class="section-title">', idx)
        if nxt < 0:
            noanchor += 1
            continue
        b = block(d)
        open(p, "w", encoding="utf-8").write(html[:nxt] + b + html[nxt:])
        done += 1
    print("=== 分红再投复利注入完成 ===")
    print("注入:", done, " 跳过:", skipped, " 无R15锚点:", noanchor, " 无页面:", nopage)


if __name__ == "__main__":
    main()
