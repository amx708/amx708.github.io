# -*- coding: utf-8 -*-
"""给重点页追加「我的结话（示例·待你定稿）」块。
锚点：插在 </footer> 之前（commodity-co 页的 masters-outro 块本就在 footer 前；
链 co 页无 outro 块，同样落在所有内容之后、footer 之前）。
幂等标记：<!--my-conclusion-sample-->。
注意：本块是 AI 按真实数据起草的【模板示例】，明确标注待用户定稿替换，不冒充真实结论。
"""
import os, re

DS = os.path.dirname(os.path.abspath(__file__))
MARK = "<!--my-conclusion-sample-->"

# 每页示例结话正文（HTML 片段，可用 <b>/<br>）。数据取自各页 .snap 真实快照。
SAMPLES = {
"berkshire-commodity-co-603993.html":
 "铜钴双轮。ROE <b>26.6%</b>、经营现金流 <b>207 亿</b>、负债率 <b>50.3%</b> 可控；PE <b>17.3</b> / PB <b>4.7</b>，在资源股里算合理偏低。<br>"
 "我的判断（示例）：这是「量增 + 价格弹性」的生意，护城河在刚果金铜钴矿的稀缺资源位与低成本，不是品牌。买点要等铜价预期悲观、或 PB 回到 3 以下给安全边际；现在不算贵，但也还没到「捡便宜」的位置。<br>"
 "<b>我的红灯</b>：铜钴价格连续两季下行 + 负债率突破 55%——那就是周期顶点信号，我会减。",

"berkshire-commodity-co-601088.html":
 "现金牛范本。负债率仅 <b>23.3%</b>、经营现金流 <b>751 亿</b>、股息率 <b>2.25%</b>、ROE <b>12.8%</b> 稳定；PE <b>19.2</b> / PB <b>2.06</b>。<br>"
 "我的判断（示例）：施洛斯式「硬资产 + 稳定分红」标的，护城河是煤矿资源 + 长协 + 一体化，现金流可验证。缺点是没有高增长想象，别用成长股 PEG 框它。<br>"
 "<b>我的买点</b>：PB 跌破 1.8 或股息率破 3% 时加；<b>红灯</b>：长协煤价政策压制 + 分红率下调。",

"berkshire-commodity-co-600188.html":
 "ROE <b>9.95%</b>、负债率 <b>62.2%</b> 偏高，是典型的「高杠杆周期煤」。PE <b>21</b> / PB <b>2.65</b> 看着不贵，但杠杆吞掉了安全边际。<br>"
 "我的判断（示例）：这票弹性大但睡不踏实——62% 负债率在煤价下行期会放大利润波动。我只会在煤价极度悲观、PB 跌到 1.5 以下、且确认分红不砍时，用观察仓博反弹，绝不满仓。<br>"
 "<b>红灯</b>：负债率继续升 + 分红削减 = 立刻撤。",

"berkshire-commodity-co-002460.html":
 "锂价下行期的「受伤者」：毛利率压到 <b>15.7%</b>、ROE <b>3.8%</b>、股息率 <b>0.3%</b> 近乎没有；PE <b>27</b> 看着高是因为利润薄。<br>"
 "我的判断（示例）：现在不是价值陷阱就是黄金坑，关键看锂周期位置。护城河是锂盐加工产能与资源布局，但周期股买在「最惨」才安全。<br>"
 "<b>我的态度</b>：等毛利回到 25%+、ROE 转正双位数、且锂价止跌——之前只看不买。这里我不下结论，只记观察。",

"berkshire-commodity-co-002466.html":
 "有意思的反差：ROE 只剩 <b>1.1%</b>、利润薄，但负债率 <b>28%</b>（低）、毛利率 <b>39.5%</b>（高）、股息率 <b>2.98%</b>（反而高）。<br>"
 "我的判断（示例）：低负债 + 高毛利说明家底还在，高额分红像是「用分红维持信心」。这是资产型标的，PB <b>1.68</b> 贴近重置成本。<br>"
 "<b>买点（示例）</b>：锂周期反转信号出现 + PB 不高于 1.5；<b>红灯</b>：锂价再破位且被迫砍分红。",

"berkshire-commodity-co-601168.html":
 "PE <b>15.4</b> 是全组最便宜，ROE <b>20.5%</b> 不差，但负债率 <b>57.5%</b>、股息率仅 <b>0.16%</b>——赚了钱不怎么分。铜价弹性标的。<br>"
 "我的判断（示例）：便宜有便宜的道理，低分红说明钱还在扩产/还债。护城河是玉龙铜矿等资源。<br>"
 "<b>买点</b>：铜价悲观 + PE 低于 12；<b>红灯</b>：负债率破 60% 且铜价下行双杀。",

"berkshire-commodity-co-603969.html":
 "小盘金矿：营收 <b>32 亿</b>、经营现金流仅 <b>1.28 亿</b>（偏弱）、ROE <b>13.8%</b>、市值 <b>62 亿</b>。<br>"
 "我的判断（示例）：黄金股的「弹性小票」，现金流薄是硬伤（不符合我「可验证现金流」的底线）。更像主题博弈而非收息资产。<br>"
 "<b>我的态度</b>：只用小仓位跟金价趋势，不作为核心持有；<b>红灯</b>：现金流持续为负 + 克金成本失控。",

"berkshire-gold-mine-co-601899.html":
 "全站含金量最高的硬资产之一：ROE <b>31.8%</b>、经营现金流 <b>754 亿</b>、股息率 <b>4.5%</b>（高）、PE <b>16.3</b> / PB <b>4.55</b>。铜金双核，量增逻辑清晰。<br>"
 "我的判断（示例）：少数同时满足「高 ROE + 强现金流 + 真分红 + 资源护城河」的标的，长期持有逻辑通顺。估值上 PB 4.5 不算便宜，但量增摊薄后 PE 有吸引力。<br>"
 "<b>买点</b>：铜金价格不狂热时、或 PB 回到 3.8 以内加；<b>红灯</b>：负债率破 55% + 海外矿政治风险事件 + 分红率下调——任一出现我重新评估仓位。",
}

def build_block(body):
    return (
        MARK + "\n"
        '<section style="margin:20px 0;padding:16px 18px;border:1.5px dashed #b8860b;border-radius:12px;background:#fffaf0">'
        '<div style="font-size:14px;font-weight:700;color:#9a6a00;margin-bottom:4px">我的结话（示例 · 待你定稿替换）</div>'
        '<div style="font-size:11.5px;color:#a07840;margin-bottom:10px">【AI 按本页真实财务/估值数据起草的模板示例，不代表你的真实观点；请用自己的话替换这一块】</div>'
        '<div style="font-size:13.5px;line-height:1.75;color:#374151">' + body + '</div>'
        '</section>'
    )

def inject(html, body):
    if MARK in html:
        return html, False
    block = build_block(body)
    # 插在 </footer> 之前；若不存在则追加到末尾
    if "</footer>" in html:
        html = html.replace("</footer>", block + "</footer>", 1)
    else:
        html = html + block
    return html, True

def main():
    changed = []
    for fn, body in SAMPLES.items():
        p = os.path.join(DS, fn)
        if not os.path.exists(p):
            print("MISSING", fn); continue
        h = open(p, encoding="utf-8").read()
        nh, ok = inject(h, body)
        if ok:
            open(p, "w", encoding="utf-8").write(nh)
            changed.append(fn)
        print(("CHANGED " if ok else "skip    ") + fn)
    # 关键：仅当有改动才重写清单，避免幂等复跑把清单清空（旧坑）
    if changed:
        with open(os.path.join(DS, "_my_conclusion_changed.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(changed) + "\n")
    print("scanned=%d  changed=%d" % (len(SAMPLES), len(changed)))

if __name__ == "__main__":
    main()
