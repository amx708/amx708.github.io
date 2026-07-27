# -*- coding: utf-8 -*-
"""生成「江苏农商行 · 5家横向比较」专题页 berkshire-rural-banks-compare.html。
数据：估值分位来自 deploy_site/data/_chain_valuation_data.json（as_of 2026-07-15，与详情页一致）；
财务/资金/评分来自 deliverables/a-share/sector-compare-rural-banks-5-2026-07-26.md（2026-07-25）。
幂等：重跑覆盖同名文件。风格复用银行链页面 CSS（accent=#2563eb/#3b82f6）。
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.join(os.path.dirname(ROOT), "_chain_valuation_data.json")
OUT = os.path.join(ROOT, "berkshire-rural-banks-compare.html")

# 估值（站点权威源，as_of 2026-07-15）
val = json.load(open(VAL, encoding="utf-8"))["bank"]
_items = val.values() if isinstance(val, dict) else (val if isinstance(val, list) else [])
vmap = {x["code"]: x for x in _items if isinstance(x, dict)}

# 5 家（顺序=优选排序：常熟>江阴≈张家港>苏农>无锡）
B = [
    dict(slug="changshu", code="601128", name="常熟银行",
         div=3.8, payout=21.0, npl=0.76, prov=451, nim=2.53, roe=14.05, score=89,
         verdict="🔵 分批 6–10%", rng="6.8–9.5",
         fund="长线共识（交行+社保+险资+国资），北向仅温和减",
         note="质量锚：息差 2.53% 护城河，ROE 14% 领先"),
    dict(slug="jiangyin", code="002807", name="江阴银行",
         div=5.2, payout=26.5, npl=0.82, prov=330, nim=1.60, roe=10.71, score=71,
         verdict="🟡 持有 3–5%", rng="4.4–5.5",
         fund="北向最稳（-0.06%），红利低波 ETF 增持，本地国资锁仓",
         note="稳定器：息差居中 + 高股息 5.2%"),
    dict(slug="zjg", code="002839", name="张家港行",
         div=5.0, payout=27.0, npl=0.94, prov=329, nim=1.39, roe=10.36, score=74,
         verdict="🟡 持有打底 8–12%", rng="4.4–5.5",
         fund="红利低波 ETF 被动托底（≈5.87%）+ 国资产业锁仓，主动零配",
         note="高息弹性：股息 5% + 结构优化"),
    dict(slug="wuxi", code="600908", name="无锡银行",
         div=4.7, payout=12.4, npl=0.77, prov=415, nim=1.35, roe=10.05, score=61,
         verdict="🟡 持有 5–8%", rng="5.2–6.3",
         fund="险资 + 国资锁仓 >26%，零拥挤低弹性",
         note="厚拨备防御：拨备 415% 极厚，治理折价待改善"),
    dict(slug="sunong", code="603323", name="苏农银行",
         div=5.0, payout=23.0, npl=0.88, prov=353, nim=1.27, roe=10.84, score=73,
         verdict="🔵 分批 5–8%", rng="4.5–5.8",
         fund="北向季环比 -17.7% 大幅减仓、主动公募仅 0.02%——三路回避，预期差最大",
         note="最便宜矛头：PB 0.48 最低"),
]

for b in B:
    v = vmap[b["code"]]
    b["pe"] = v["pe"]["cur"]; b["pe_pct"] = v["pe"]["pct"]
    b["pb"] = v["pb"]["cur"]; b["pb_pct"] = v["pb"]["pct"]
    b["avg_roe"] = v["quality"]["avg_roe"]; b["star"] = v["quality"]["star"]
    b["break"] = round((1 - b["pb"]) * 100)  # 破净程度

cols = [b["name"] for b in B]
codes = [b["code"] for b in B]

def pct_cls(p):
    return "lo" if p < 5 else ("mid" if p < 15 else "hi")

# 行定义：(label, 取值函数, 是否估值分位着色)
rows = [
    ("代码", lambda b: b["code"], None),
    ("PE(TTM)", lambda b: "%.2f" % b["pe"], None),
    ("PE 分位", lambda b: "%.1f%%" % b["pe_pct"], "pe"),
    ("PB(LF)", lambda b: "%.2f" % b["pb"], None),
    ("PB 分位", lambda b: "%.1f%%" % b["pb_pct"], "pb"),
    ("破净程度", lambda b: "%d%%" % b["break"], None),
    ("股息率", lambda b: "%.1f%%" % b["div"], None),
    ("分红率", lambda b: "%.1f%%" % b["payout"], None),
    ("不良率", lambda b: "%.2f%%" % b["npl"], None),
    ("拨备覆盖率", lambda b: "%d%%" % b["prov"], None),
    ("净息差", lambda b: "%.2f%%" % b["nim"], None),
    ("ROE", lambda b: "%.2f%%" % b["roe"], None),
    ("平均ROE(10y)", lambda b: "%.2f%%" % b["avg_roe"], None),
    ("质量星", lambda b: b["star"], None),
    ("综合质量分", lambda b: str(b["score"]), None),
    ("投资建议", lambda b: b["verdict"], None),
    ("合理区间(元)", lambda b: b["rng"], None),
]

# 子组合配置
weights = [
    ("常熟 601128", "28%", "核心多仓（质量锚）", "ROE 14% 护城河，长线共识；股息率仅 3.8% 偏低"),
    ("江阴 002807", "20%", "稳定器", "北向最稳 + 息差居中 + 高股息 5.2%"),
    ("张家港 002839", "18%", "高息弹性", "股息 5% + 结构优化 + 红利 ETF 托底"),
    ("苏农 603323", "17%", "最便宜矛头", "PB 0.48 最低、预期差最大，等北向放缓再加码"),
    ("无锡 600908", "17%", "厚拨备防御", "拨备 415% 极厚、锁仓强，待治理改善 + 分红率提升"),
]

CSS = """
:root{--bg:#f5f9ff;--soft:#eef5ff;--card:#ffffff;--ink:#0f172a;--mut:#475569;--line:rgba(59,130,246,.15);--red:#dc2626;--green:#16a34a;--accent:#2563eb;--accent-light:#3b82f6;--accent-ghost:rgba(59,130,246,.08);}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(180deg,#f8fbff 0%,#f0f7ff 100%);background-attachment:fixed;color:var(--ink);line-height:1.7;font-size:15px;-webkit-font-smoothing:antialiased}
.nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{max-width:1080px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.nav .brand{color:var(--ink);font-weight:600;font-size:15px;letter-spacing:.3px}
.nav .crumb{color:var(--mut);font-size:12.5px}
.nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:4px 9px;border-radius:6px;transition:.15s}
.nav a:hover{color:var(--accent);background:var(--soft)}
.hero{background:linear-gradient(135deg,#ffffff 0%,#e8f1ff 100%);border-bottom:1px solid var(--line);padding:42px 20px 32px;box-shadow:0 4px 20px rgba(37,99,235,.10)}
.hero-in{max-width:1080px;margin:0 auto}
.hero h1{margin:0 0 10px;font-size:28px;font-weight:700;letter-spacing:-.5px;color:#0f172a}
.hero p{margin:5px 0;color:var(--mut);max-width:780px;font-size:14.5px}
.hero .stat{display:flex;gap:38px;margin-top:22px;flex-wrap:wrap}
.hero .stat b{color:var(--accent);font-size:24px;display:block;font-weight:700}
.hero .stat span{font-size:12px;color:var(--mut)}
.wrap{max-width:1080px;margin:0 auto;padding:26px 20px 70px}
.section-title{font-size:18px;font-weight:700;margin:32px 0 14px;padding-left:12px;border-left:4px solid var(--accent);letter-spacing:-.2px;color:var(--ink)}
.note{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:12px;padding:14px 18px;margin:8px 0 4px;font-size:13.5px;color:var(--mut);line-height:1.7}
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card);box-shadow:0 3px 10px rgba(37,99,235,.06)}
table{border-collapse:collapse;width:100%;min-width:760px;font-size:13.5px}
th,td{padding:10px 12px;text-align:center;border-bottom:1px solid var(--line)}
thead th{background:var(--soft);color:var(--accent);font-weight:700;position:sticky;top:0}
tbody th{background:#fbfdff;text-align:left;color:var(--mut);font-weight:600;white-space:nowrap}
td.lo{color:var(--green);font-weight:700}
td.mid{color:#0d9488;font-weight:600}
td.hi{color:var(--mut)}
td.best{background:var(--accent-ghost);font-weight:700;color:var(--accent)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:8px}
.bcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:0 3px 10px rgba(37,99,235,.06)}
.bcard h4{margin:0 0 4px;font-size:15px;color:var(--ink)}
.bcard .code{font-size:11.5px;color:var(--mut)}
.bcard .row{font-size:12.5px;color:var(--mut);margin-top:6px;line-height:1.55}
.bcard a{display:inline-block;margin-top:8px;color:var(--accent);text-decoration:none;font-size:12.5px;font-weight:600}
.bcard a:hover{text-decoration:underline}
.cfg{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card);margin-top:8px}
.cfg table{min-width:640px}
.cfg td,.cfg th{padding:9px 12px;text-align:left}
.cfg td:first-child{font-weight:600;color:var(--ink)}
footer{text-align:center;color:#94a3b8;font-size:12px;padding:30px 20px 50px;line-height:1.7}
footer a{color:var(--mut);text-decoration:none}
"""

def cell_td(b, kind, val):
    if kind == "pe":
        return '<td class="%s">%s</td>' % (pct_cls(b["pe_pct"]), val)
    if kind == "pb":
        return '<td class="%s">%s</td>' % (pct_cls(b["pb_pct"]), val)
    return "<td>%s</td>" % val

rows_html = []
for label, fn, kind in rows:
    tds = "".join(cell_td(b, kind, fn(b)) for b in B)
    rows_html.append("<tr><th>%s</th>%s</tr>" % (label, tds))
rows_html = "\n".join(rows_html)

# 子组合表
cfg_rows = []
for name, w, role, logic in weights:
    cfg_rows.append("<tr><td>%s</td><td style='color:var(--accent);font-weight:700'>%s</td><td>%s</td><td>%s</td></tr>" % (name, w, role, logic))
cfg_html = "\n".join(cfg_rows)

# 5 家卡片（含回链详情页）
cards = []
for b in B:
    cards.append(
        '<div class="bcard"><h4>%s</h4><div class="code">%s</div>'
        '<div class="row">PE %.2f / PB %.2f（分位 %.1f%% / %.1f%%）<br>股息率 %.1f%% · 不良 %.2f%% · 拨备 %d%%<br>%s</div>'
        '<a href="berkshire-bank-chain-%s.html">查看详情 →</a></div>'
        % (b["name"], b["code"], b["pe"], b["pb"], b["pe_pct"], b["pb_pct"],
           b["div"], b["npl"], b["prov"], b["verdict"], b["slug"])
    )
cards_html = "\n".join(cards)

html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>江苏农商行 · 5家横向比较 | 伯克希尔数据中心</title><style>@@CSS@@</style></head>
<body>
<div class="nav"><div class="nav-in">
<span class="brand">伯克希尔数据中心</span>
<span class="crumb">银行链 / 农商行对比</span>
<a href="berkshire-bank-chains.html">← 银行链</a>
<a href="index.html">首页</a>
</div></div>

<div class="hero"><div class="hero-in">
<h1>江苏农商行 · 5 家横向比较</h1>
<p>常熟 / 江阴 / 张家港 / 无锡 / 苏农——全部处历史极低估值 + 深度破净 + 高股息 + 低增长的防御型资产带。
本页横向对比估值、质量、资金三维，给出优选排序与子组合配置建议，直接服务红利底仓构建。</p>
<div class="stat">
<b>5 家</b><span>江苏上市农商行全覆盖</span>
<b>PB 0.48–0.71</b><span>近十年 0.6%–3.3% 分位</span>
<b>股息 3.8%–5.2%</b><span>不良均 &lt;1% · 拨备均 &gt;300%</span>
</div>
</div></div>

<div class="wrap">

<div class="note"><b>核心结论：</b>按「质量—估值—治理」三维排序，优选结构为
<b>常熟（质量锚）&gt; 江阴（稳定器）≈ 张家港（高息）&gt; 苏农（最便宜）&gt; 无锡（厚拨备但治理折价）</b>。
建议以五家子组合分散单一区域与质量风险，总仓占权益仓 15–25%，常熟为核心多仓。</div>

<div class="section-title">一、五家横向矩阵</div>
<div class="tbl-wrap"><table>
<thead><tr><th>指标</th>@@COLS@@</tr></thead>
<tbody>
@@ROWS@@
</tbody></table></div>
<p style="font-size:12px;color:#94a3b8;margin:8px 2px 0">估值分位截至 2026-07-15（来源：站点估值库，与详情页一致）；财务/资金/评分截至 2026-07-25（来源：五家农商行深度研究合成）。绿色=估值分位极低（更便宜）。</p>

<div class="section-title">二、三维定位与优选逻辑</div>
<div class="cards">@@CARDS@@</div>

<div class="section-title">三、建议子组合配置（占权益仓 15–25%）</div>
<div class="cfg"><table>
<thead><tr><th>标的</th><th>权重</th><th>角色</th><th>逻辑</th></tr></thead>
<tbody>
@@CFG@@
</tbody></table></div>
<p style="font-size:12px;color:#94a3b8;margin:8px 2px 0">权重逻辑：质量倾斜常熟，平衡配置江阴/张家港/苏农，无锡控仓待治理催化。单一标的占权益仓不超过 10%，避免单一区域过度集中。</p>

<div class="note" style="margin-top:18px"><b>风险提示：</b>行业共性——净息差长期下行、区域集中度、破净长期化（板块系统性低估）。
个股红线——常熟（转债摊薄/异地不良）、张家港（红利退潮 ETF 赎回）、苏农（北向持续流出）、江阴（经营现金流波动）、无锡（治理折价/拨备降/零售失速）。
证伪信号：任一不良跳升破 1.2%、息差破位、红利 ETF 持续净赎回、社保/交行/险资战略减持。</div>

</div>

<footer>
伯克希尔数据中心 · 江苏农商行对比专题 &nbsp;|&nbsp;
<a href="berkshire-bank-chains.html">银行链总览</a> &nbsp;·&nbsp;
<a href="index.html">返回首页</a><br>
⚠️ 本页由 AI 基于公开信息整理生成，仅供参考，不构成任何投资建议或个股推荐。投资有风险，决策需谨慎。
</footer>
</body></html>"""
html = (html.replace("@@CSS@@", CSS)
            .replace("@@COLS@@", "".join("<th>%s</th>" % c for c in cols))
            .replace("@@ROWS@@", rows_html)
            .replace("@@CARDS@@", cards_html)
            .replace("@@CFG@@", cfg_html))

open(OUT, "w", encoding="utf-8").write(html)
print("已生成:", OUT, "(%d bytes)" % len(html))
print("覆盖银行:", ", ".join("%s(%s)" % (b["name"], b["code"]) for b in B))
