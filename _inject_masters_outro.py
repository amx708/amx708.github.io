# -*- coding: utf-8 -*-
"""给 44 个 commodity-co 页注入「七大师·结话」收口块（草稿占位，待用户定稿）。
幂等：标记 <!--masters-outro--> / /*masters-outro-css*/。
插入锚点：mv-grid 闭合 </div> 之后、detail 闭合 </div> 之前（紧邻 <footer> 前）。
"""
import os, re, glob

DS = os.path.dirname(os.path.abspath(__file__))
OUTRO_MARK = "<!--masters-outro-->"
CSS_MARK = "/*masters-outro-css*/"

CSS = """
%s
.mv-outro{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:16px 20px;margin:18px 0;font-size:14px;line-height:1.85;color:var(--ink)}
.mv-outro p{margin:0 0 12px}
.mv-outro p:last-of-type{margin-bottom:0}
.mv-outro .mv-outro-h{font-weight:700;color:var(--accent);margin:14px 0 4px}
.mv-check{margin:4px 0 0;padding-left:22px}
.mv-check li{margin:6px 0}
.mv-check b{color:var(--accent)}
""" % CSS_MARK

OUTRO = """
%s
<div class="section-title"><span class="dot"></span>七大师 · 结话（草稿占位 · 待你定稿）</div>
<div class="mv-outro">
  <p>七面透镜拼起来，背后其实是一句没吵架的共识：<b>先真懂这门生意，再用纪律性的价格去买，最后靠性情穿越周期</b>。他们争的只是「该看哪个指标」——巴菲特 / 芒格 / 段永平偏「质」（护城河、治理诚信、确定性），马克斯 / 达里奥偏「势」（周期位置、宏观机器、组合相关性），林奇 / 李录偏「匹配」（公司分类、结构性复利）。但没人会反驳「别让本金永久损失、别为故事付太贵的价格」。</p>
  <p>所以把这节当成一张<b>体检表，不是诊断书</b>：任何一面亮红灯——杠杆过高（芒格 invert）、治理有瑕疵（段永平）、估值分位极端（马克斯第二层思维）、与持仓高度相关（达里奥）——都值得你停下来多想一步；但没有任何一面单独构成买卖信号。真正的「结话」得你自己写：<b>把七面信号收敛成一句话，一句你愿意用真金白银背书的话。</b>本页只负责把事实摆齐（财务 / 估值分位 / 安全边际线 / 机械结论合成），七位大师的「你的结论」留白给你——这也是本工具不代下结论的边界。</p>
  <p class="mv-outro-h">收敛清单（写你自己的结话前，先过这三问）：</p>
  <ol class="mv-check">
    <li>它落在七面透镜的「共振区」还是「对冲区」？<b>共振</b>（质、势、匹配同时绿灯）才值重仓；<b>对冲</b>（比如质好但分位极端）只值观察仓。</li>
    <li>最让你睡不着的那个红灯是什么？把它写下来——它就是你的<b>卖出触发</b>，不是别人的。</li>
    <li>你能用一句话说清「为什么是这家、为什么是现在」吗？说不清，就还停在研究阶段。</li>
  </ol>
</div>
""" % OUTRO_MARK


def inject_css(html):
    if CSS_MARK in html:
        return html, False
    if "</style>" in html:
        return html.replace("</style>", CSS + "</style>", 1), True
    return html, False


def inject_outro(html):
    if OUTRO_MARK in html:
        return html, False
    # 锚点：mv-grid 闭合 </div> 之后 -> detail 闭合 </div> 之前 -> <footer> 之前
    # 整站 commodity-co 页结构唯一： ...mv-grid...</div>\n</div>\n<footer>
    new_html, n = re.subn(
        r'(</div>)\s*(</div>\s*<footer>)',
        lambda m: m.group(1) + "\n" + OUTRO + "\n" + m.group(2),
        html, count=1)
    return (new_html, True) if n else (html, False)


def main():
    files = sorted(glob.glob(os.path.join(DS, "berkshire-commodity-co-*.html")))
    changed = []
    css_changed = 0
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            html = f.read()
        html, c1 = inject_css(html)
        if c1:
            css_changed += 1
        html, c2 = inject_outro(html)
        if c1 or c2:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
        if c2:
            changed.append(os.path.basename(fp))
    # 幂等复跑时 changed 可能为空：仅当有改动才覆盖清单，避免清空已有清单
    if changed:
        with open(os.path.join(DS, "_masters_outro_changed.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(changed) + "\n")
    print("scanned=%d  css_changed=%d  outro_changed=%d" % (len(files), css_changed, len(changed)))


if __name__ == "__main__":
    main()
