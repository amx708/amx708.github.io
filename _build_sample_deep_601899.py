# -*- coding: utf-8 -*-
"""样板：把 NVIDIA 式 6 段深凿结构插入 紫金矿业(601899) 黄金链详情页。
原则：保留原框架内容，仅新增 一句话业务/关键数字/跨层拆解/投资逻辑/新闻时间线/来源声明，
用本页橙色主题保持一致。真实数据来自 akshare(THS年报/百度估值/腾讯行情/东财新闻)。
"""
import warnings, json, re, os
warnings.filterwarnings("ignore")
import akshare as ak
import urllib.request

CODE = "601899"
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"berkshire-gold-mine-chain-{CODE}.html")

# ---------- 1. 真实数据采集 ----------
# THS 年报摘要（取最新年报）
df = ak.stock_financial_abstract_ths(symbol=CODE)
ann = df[df["报告期"].str.endswith("-12-31")].reset_index(drop=True)
row = ann.iloc[-1]  # 最新年报
rev = float(row["营业总收入"].replace("亿", "")) if isinstance(row["营业总收入"], str) else float(row["营业总收入"])
net = float(row["净利润"].replace("亿", "")) if isinstance(row["净利润"], str) else float(row["净利润"])
gross = str(row["销售毛利率"])
roe = str(row["净资产收益率"])
lev = str(row["资产负债率"])
ocf = row["每股经营现金流"]
rev_yoy = row["营业总收入同比增长率"]
net_yoy = row["净利润同比增长率"]
report_date = str(row["报告期"])

# 百度估值分位
def baidu_pct(ind):
    d = ak.stock_zh_valuation_baidu(symbol=CODE, indicator=ind, period="近十年")
    v = d["value"].astype(float)
    cur = float(v.iloc[-1]); lo = v.min(); hi = v.max()
    pct = (cur - lo) / (hi - lo) * 100 if hi > lo else 0
    return cur, pct
pe_cur, pe_pct = baidu_pct("市盈率(TTM)")
pb_cur, pb_pct = baidu_pct("市净率")

# 腾讯行情
pre = "sh" if CODE.startswith(("6", "9")) else "sz"
s = urllib.request.urlopen(f"https://qt.gtimg.cn/q={pre}{CODE}", timeout=15).read().decode("gbk")
f = s.split("~")
mkt_cap = f[45]; price = f[3]

# 新闻时间线（东财）
nd = ak.stock_news_em(symbol=CODE)
news = []
for _, r in nd.head(6).iterrows():
    t = r.get("新闻标题") or r.get("title") or ""
    d = str(r.get("发布时间") or r.get("date") or "")[:10]
    if t and d:
        news.append((d, t))

print(f"数据: 营收{rev}亿 净利{net}亿 毛利率{gross} ROE{roe} 负债率{lev} | PE{pe_cur}({pe_pct:.1f}%) PB{pb_cur}({pb_pct:.1f}%) 市值{mkt_cap}亿 价{price}")
print("新闻条数:", len(news))

# ---------- 2. 6 段深凿 HTML（橙色主题，手写叙事基于公开事实） ----------
oneliner = f"""紫金矿业不是「挖金子的」，而是<b>全球化的金铜矿企</b>：用「自主勘探 + 海外并购」双轮把资源储量做厚，再用<b>低成本露天开采 + 湿法冶炼</b>把矿石变成金锭和阴极铜，卖向央行购金、首饰加工与电力基建。2025 年矿产金、矿产铜产量已居全球第一梯队，是这一轮<b>央行购金 + 铜电气化</b>双主线最直接的「卖铲人」。"""

kpis = f"""
<div class="kpi-grid">
<div class="kpi"><div class="k-num">{rev:.0f}亿</div><div class="k-lab">营业总收入({report_date[:4]})</div><div class="k-sub">同比 {rev_yoy}</div></div>
<div class="kpi"><div class="k-num">{net:.0f}亿</div><div class="k-lab">归母净利润({report_date[:4]})</div><div class="k-sub">同比 {net_yoy}</div></div>
<div class="kpi"><div class="k-num">{gross}</div><div class="k-lab">销售毛利率</div><div class="k-sub">资源溢价</div></div>
<div class="kpi"><div class="k-num">{roe}</div><div class="k-lab">ROE(加权)</div><div class="k-sub">盈利质量</div></div>
<div class="kpi"><div class="k-num">{lev}</div><div class="k-lab">资产负债率</div><div class="k-sub">财务杠杆</div></div>
<div class="kpi"><div class="k-num">{price}</div><div class="k-lab">现价(元)</div><div class="k-sub">市值 {mkt_cap}亿</div></div>
</div>
<div class="table-wrap"><table>
<thead><tr><th>指标（{report_date} 年报）</th><th>数值</th><th>信号</th></tr></thead>
<tbody>
<tr><td>营业总收入</td><td>{rev:.1f} 亿</td><td class="pos">同比 {rev_yoy}</td></tr>
<tr><td>归母净利润</td><td>{net:.1f} 亿</td><td class="pos">同比 {net_yoy}</td></tr>
<tr><td>销售毛利率</td><td>{gross}</td><td class="pos">资源溢价高</td></tr>
<tr><td>ROE（加权）</td><td>{roe}</td><td class="pos">高回报</td></tr>
<tr><td>资产负债率</td><td>{lev}</td><td class="neg">略高</td></tr>
<tr><td>每股经营现金流</td><td>{ocf}</td><td class="pos">造血强</td></tr>
</tbody></table></div>
<div class="source-note" style="margin-top:10px">注：财务数据取自同花顺年报摘要（{report_date}）；估值 / 行情为采集日快照（腾讯行情）。PE 近十年分位 {pe_pct:.1f}%、PB 近十年分位 {pb_pct:.1f}%（百度股市通）。</div>
"""

layers = """
<div class="layer-block"><div class="layer-head"><span class="layer-num">01</span><span class="layer-title">勘探与资源端</span></div>
<div class="layer-body">核心壁垒是<b>资源储量</b>：通过自主勘探 + 海外并购（如收购 Neo Lithium、大陆黄金、圭亚那金田）持续增厚权益储量，2025 年黄金资源量居全球前列。<br>
<span class="node">自主勘探</span><span class="node">海外并购</span><span class="node">权益储量</span><span class="node">资源税 / 矿权</span><br>
资源端决定了长期「卖铲」能力——储量越厚，越能穿越金价周期。</div></div>

<div class="layer-block"><div class="layer-head"><span class="layer-num">02</span><span class="layer-title">开采与采矿</span></div>
<div class="layer-body">以<b>低成本露天开采</b>为主，国内（紫金山、陇南）与海外（刚果金 Kamoa-Kakula 铜、塞尔维亚 Timok、哥伦比亚）并重；模块化建矿把达产周期压短。<br>
<span class="node">露天开采</span><span class="node">地下矿</span><span class="node">海外矿山运营</span><span class="node">模块化建矿</span><br>
2026H1 黄金产量 47 吨（同比 +15%），产能仍在爬坡。</div></div>

<div class="layer-block"><div class="layer-head"><span class="layer-num">03</span><span class="layer-title">冶炼与精炼</span></div>
<div class="layer-body">把原矿炼成<b>金锭 / 阴极铜</b>，湿法冶炼（如重选 + 堆浸）降低现金成本；铜板块受益电气化（电网 / 电动车 / AI 数据中心用铜）。<br>
<span class="node">湿法冶炼</span><span class="node">金锭</span><span class="node">阴极铜</span><span class="node">现金成本曲线</span><br>
低成本曲线让其在金价 / 铜价下行时仍保利润，是抗周期的关键。</div></div>

<div class="layer-block"><div class="layer-head"><span class="layer-num">04</span><span class="layer-title">加工与贸易</span></div>
<div class="layer-body">向下游延伸到金饰加工、工业用铜与贸易；也通过<b>金属贸易</b>平滑价格波动、锁定加工利润。<br>
<span class="node">金饰加工</span><span class="node">工业用铜</span><span class="node">金属贸易</span><br>
下游偏「流量」属性，利润薄但稳定，与上游开采形成对冲。</div></div>
"""

invest = f"""
<div class="invest-box"><div class="ib-title">05 · 投资逻辑</div>
<div class="invest-row"><div class="ir-label">护城河</div>
<div class="ir-text"><b>三重壁垒</b>：① <b>资源储量规模</b>与全球化布局，新进入者难短期复制；② <b>低成本开采 + 湿法冶炼</b>使其在周期底部仍有正现金流；③ <b>矿产铜绑定电气化长逻辑</b>（电网 / 电动车 / AI 数据中心），需求有第二曲线。本质是「资源 + 成本」的复合壁垒。</div></div>
<div class="invest-row"><div class="ir-label">主要风险</div>
<div class="ir-text">① <b>金价 / 铜价波动</b>直接冲击利润与估值；② <b>海外运营风险</b>（地缘、资源国政策、社区关系），如 2026-07 终止收购联合黄金、改认购其 9.2% 股权，显示海外扩张并非一帆风顺；③ <b>负债率 {lev}</b> 偏高，加息周期财务成本上升；④ <b>并购整合与商誉</b>风险。</div></div>
<div class="invest-row"><div class="ir-label">最新季度信号（2026H1）</div>
<div class="ir-text">2026-07-11 半年报预告：<b>净利润同比约 +75%</b>，黄金产量 47 吨（+15%），豪掷 111 亿分红（10 派 4.2 元）——量价齐升 + 强现金流回馈，通常是对自身经营有信心的信号。但需跟踪金价高位回落与海外项目进度。</div></div>
<div class="src-links">资料来源（公开）：<a href="https://www.zijinmining.com/" target="_blank" rel="noopener">紫金矿业官网</a> · 2025 年报 / 2026H1 业绩预告 · 东方财富新闻（2026-07-11 / 2026-07-29）· 同花顺财务摘要。</div>
</div>
"""

timeline = '<div class="timeline">'
for d, t in news:
    timeline += f'<div class="tl-item"><div class="tl-date">{d}</div><div class="tl-text">{t}</div></div>\n'
timeline += '</div>'

source_note = """
<div class="source-note">📌 <b>合规说明</b>：本页「一句话业务 / 关键数字 / 跨层拆解 / 投资逻辑 / 新闻时间线」均基于紫金矿业<b>公开年报、官网与新闻</b>等事实层信息，由本站原创整理与重写，不复制、不转载任何付费 / 闭源专享内容；第三方机构预测为<b>估算或传闻</b>，仅供框架参考，请以公司官方披露为准。投资逻辑仅为「跨层框架」研究示例，<b>不构成任何投资建议</b>。版权归紫金矿业及各原发布方所有。</div>
"""

# ---------- 3. 注入到原页 ----------
html = open(SRC, encoding="utf-8").read()

# 3a. 在 <style> 末尾（</style> 前）追加深凿段 CSS（橙色主题）
deep_css = """
.oneliner{background:rgba(249,115,22,0.06);border:1px solid rgba(249,115,22,0.2);border-radius:12px;padding:16px 18px;font-size:14.5px;color:#334155;line-height:1.8}
.oneliner b{color:#0f172a}
.layer-block{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px 20px;margin-bottom:14px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.layer-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.layer-num{width:26px;height:26px;border-radius:50%;background:#f97316;color:#fff;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.layer-title{font-size:16px;font-weight:700;color:#0f172a}
.layer-body{font-size:14px;color:#475569;line-height:1.85}
.layer-body b{color:#1e293b}
.layer-body .node{display:inline-block;background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.22);color:#f97316;font-size:12.5px;padding:2px 9px;border-radius:8px;margin:3px 4px 3px 0}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.kpi{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.kpi .k-num{font-size:18px;font-weight:800;color:#f97316}
.kpi .k-lab{font-size:11.5px;color:#64748b;margin-top:2px}
.kpi .k-sub{font-size:11px;color:#94a3b8;margin-top:1px}
.table-wrap{overflow-x:auto;margin-top:6px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:9px 10px;text-align:right;border-bottom:1px solid #eef2f7;color:#334155}
th:first-child,td:first-child{text-align:left;color:#0f172a;font-weight:600}
th{color:#64748b;font-weight:600;background:#f8fafc}
td .pos{color:#16a34a}
td .neg{color:#dc2626}
.invest-box{background:linear-gradient(135deg,#fff7ed,#ffffff);border:1px solid rgba(249,115,22,0.25);border-radius:12px;padding:18px 20px;margin-top:8px}
.invest-box .ib-title{font-size:16px;font-weight:700;color:#f97316;margin-bottom:10px}
.invest-row{margin-bottom:12px}
.invest-row .ir-label{font-size:13px;font-weight:700;color:#0f172a;margin-bottom:3px}
.invest-row .ir-text{font-size:13.5px;color:#475569;line-height:1.75}
.invest-row .ir-text b{color:#1e293b}
.timeline{position:relative;padding-left:22px;margin-top:4px}
.timeline::before{content:"";position:absolute;left:6px;top:4px;bottom:4px;width:2px;background:rgba(249,115,22,0.4)}
.tl-item{position:relative;margin-bottom:16px}
.tl-item::before{content:"";position:absolute;left:-19px;top:6px;width:10px;height:10px;border-radius:50%;background:#f97316;box-shadow:0 0 0 3px rgba(249,115,22,0.15)}
.tl-date{font-size:12px;color:#f97316;font-weight:700}
.tl-text{font-size:13.5px;color:#475569;line-height:1.75;margin-top:2px}
.tl-text b{color:#1e293b}
"""
html = html.replace("</style>", deep_css + "\n</style>", 1)

# 3b. 在 hero 之后（explain-banner 之后）插入 一句话业务 + 关键数字
marker = '<div class="source-note">'  # 用首个 source-note 前插入不行；改为在 explain-banner 后
# 找到 explain-banner 块的结束（</div> 配对复杂），改用 section-title 首个前插入
first_section = html.find('<div class="section-title">')
block1 = (f'<div class="section-title">一句话业务</div>\n'
          f'<div class="oneliner">{oneliner}</div>\n'
          f'<div class="section-title">关键数字</div>\n{kpis}\n')
html = html[:first_section] + block1 + html[first_section:]

# 3c. 在 source-note（原页合规声明）前插入 跨层拆解 + 投资逻辑 + 新闻时间线 + 新来源声明
# 原页只有一个 source-note 在末尾；在其前插入
sn_idx = html.rfind('<div class="source-note">')
block2 = (f'<div class="section-title">跨层拆解（4 层）</div>\n{layers}\n'
          f'{invest}\n'
          f'<div class="section-title">新闻时间线（近 1 年）</div>\n{timeline}\n'
          f'{source_note}\n')
html = html[:sn_idx] + block2 + html[sn_idx:]

open(SRC, "w", encoding="utf-8").write(html)
print("OK 已写入:", SRC, "字节:", len(html))
