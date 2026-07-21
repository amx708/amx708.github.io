# -*- coding: utf-8 -*-
"""生成 电力 / 煤炭 / 有色 / 化工 / 电力设备 五条产业链地图（浅色风 + 12链互通导航）。
用法：python _build_five_chains.py
产出写入 deploy_site/ 根目录（站点源），再 cp 到 repo/amx708.github.io/。"""
import os
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f0f2f5;color:#1e293b;line-height:1.75}
.top-bar{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(__ACC_RGB__,0.18);padding:12px 20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.home-btn{display:inline-flex;align-items:center;gap:6px;background:rgba(__ACC_RGB__,0.10);color:#__ACC__;border:1px solid rgba(__ACC_RGB__,0.3);border-radius:20px;padding:6px 14px;font-size:13px;cursor:pointer;text-decoration:none;transition:all .2s}
.home-btn:hover{background:#__ACC__;color:#fff}
.breadcrumb{font-size:13px;color:#64748b;display:flex;gap:4px;align-items:center}
.breadcrumb a{color:#64748b;text-decoration:none}
.breadcrumb a:hover{color:#__ACC__}
.crumb-sep{color:#cbd5e1}
.container{max-width:980px;margin:0 auto;padding:24px 16px 48px}
.hero{background:linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);border-radius:14px;padding:32px 28px;margin-bottom:20px;border:1px solid rgba(__ACC_RGB__,0.25);box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.hero-title{font-size:26px;font-weight:800;color:#0f172a;margin-bottom:6px;letter-spacing:.5px}
.hero-sub{font-size:14px;color:#64748b;margin-bottom:18px}
.hero-stats{display:flex;gap:12px;flex-wrap:wrap}
.stat-item{background:rgba(__ACC_RGB__,0.08);border:1px solid rgba(__ACC_RGB__,0.15);border-radius:10px;padding:10px 18px;text-align:center}
.stat-num{font-size:20px;font-weight:800;color:#__ACC__}
.stat-label{font-size:11px;color:#64748b;margin-top:2px;white-space:nowrap}
.explain-banner{display:flex;gap:16px;align-items:flex-start;background:linear-gradient(135deg,#ffffff,#f8fafc);border:1px solid rgba(__ACC_RGB__,0.25);border-radius:12px;padding:18px 20px;margin-bottom:22px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.explain-banner .eb-icon{font-size:24px;flex-shrink:0}
.explain-banner .eb-body{flex:1;min-width:0}
.explain-banner .eb-title{font-size:15px;font-weight:700;color:#0f172a;margin-bottom:8px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.explain-banner .eb-tag{font-size:11px;color:#__ACC__;background:rgba(__ACC_RGB__,0.12);padding:2px 9px;border-radius:10px}
.explain-banner .eb-text{font-size:13px;color:#475569;line-height:1.8}
.explain-banner .eb-text b{color:#0f172a;font-weight:600}
.section-title{font-size:18px;font-weight:700;color:#0f172a;margin:28px 0 14px;padding-left:12px;border-left:3px solid #__ACC__}
.layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:8px}
.layer-card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px 14px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.layer-num{font-size:12px;color:#__ACC__;font-weight:700}
.layer-name{font-size:14px;color:#0f172a;font-weight:600;margin:4px 0 4px}
.layer-desc{font-size:12px;color:#64748b;line-height:1.6}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.giant-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;transition:all .2s;text-decoration:none;display:block;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.giant-card:hover{border-color:#__ACC__;background:rgba(__ACC_RGB__,0.05);transform:translateY(-2px);box-shadow:0 4px 14px rgba(__ACC_RGB__,0.12)}
.giant-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.giant-name{font-size:16px;font-weight:700;color:#0f172a}
.region-tag{font-size:11px;padding:2px 9px;border-radius:10px;font-weight:600}
.region-cn{background:rgba(220,38,38,0.12);color:#dc2626;border:1px solid rgba(220,38,38,0.25)}
.region-hk{background:rgba(234,179,8,0.14);color:#b45309;border:1px solid rgba(234,179,8,0.3)}
.giant-desc{font-size:12.5px;color:#64748b;line-height:1.65;margin-bottom:10px}
.giant-foot{font-size:12px;display:flex;align-items:center;justify-content:space-between}
.giant-link{color:#__ACC__;font-weight:600}
.source-note{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px 16px;margin-top:24px;font-size:12.5px;color:#64748b;line-height:1.7;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.source-note b{color:#475569}
@media(max-width:640px){.hero{padding:22px 16px}.hero-title{font-size:21px}.grid{grid-template-columns:1fr}.explain-banner{flex-direction:column;padding:16px}}
.region-tag-mini{font-size:11px;padding:2px 10px;border-radius:10px;font-weight:600;display:inline-block;margin-top:8px}
.overview{background:rgba(__ACC_RGB__,0.05);border:1px solid rgba(__ACC_RGB__,0.14);border-radius:12px;padding:18px 20px;margin-bottom:8px;font-size:14px;color:#334155;line-height:1.85}
.overview b{color:#0f172a;font-weight:600}
.layer-detail{background:#fff;border:1px solid #e2e8f0;border-left:3px solid #__ACC__;border-radius:12px;padding:16px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.layer-detail-title{font-size:15px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:10px;margin-bottom:8px}
.layer-detail-body{font-size:13.5px;color:#475569;line-height:1.8}
.layer-detail-body b{color:#334155}
.info-table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-top:8px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.info-table tr{border-bottom:1px solid #eef2f7}
.info-table tr:last-child{border-bottom:none}
.info-table td{padding:12px 16px;font-size:13.5px;color:#334155}
.info-table td:first-child{width:160px;color:#64748b;background:#f8fafc}
.insight-box{background:linear-gradient(135deg,#f8fafc,#ffffff);border:1px solid rgba(__ACC_RGB__,0.2);border-radius:12px;padding:18px 20px;margin-top:16px}
.insight-title{font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.insight-title .icon{color:#__ACC__}
.insight-body{font-size:13.5px;color:#475569;line-height:1.8}
.back-bar{margin-top:20px}
.back-btn{display:inline-flex;align-items:center;gap:6px;background:rgba(__ACC_RGB__,0.08);color:#__ACC__;border:1px solid rgba(__ACC_RGB__,0.25);border-radius:20px;padding:8px 16px;font-size:13px;text-decoration:none;transition:all .2s}
.back-btn:hover{background:rgba(__ACC_RGB__,0.16)}
.data-banner{background:rgba(__ACC_RGB__,0.07);border:1px solid rgba(__ACC_RGB__,0.22);border-left:4px solid #__ACC__;border-radius:10px;padding:12px 16px;margin-bottom:20px;font-size:12.5px;color:#334155;line-height:1.7}
.data-banner b{color:#0f172a;font-weight:600}
.data-banner .upd{color:#__ACC__;font-weight:600}
.cycle-block{background:linear-gradient(135deg,#f8fafc,#ffffff);border:1px solid rgba(__ACC_RGB__,0.22);border-radius:12px;padding:18px 20px;margin-bottom:8px}
.cycle-title{font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.cycle-title .icon{color:#__ACC__}
.cycle-body{font-size:13.5px;color:#475569;line-height:1.85}
.cycle-body b{color:#0f172a;font-weight:600}
.cycle-body p{margin-bottom:8px}
.cycle-body ul{margin:8px 0 0 18px;padding:0}
.cycle-body li{margin-bottom:6px}
.cycle-current{margin-top:12px;font-size:12.5px;color:#64748b;border-left:3px solid #__ACC__;padding:8px 12px;background:rgba(__ACC_RGB__,0.06);line-height:1.7}
.cycle-current b{color:#334155}
.cycle-current a{text-decoration:none}
.fin-block{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.fin-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.fin-title{font-size:15px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:8px}
.fin-title .icon{color:#__ACC__}
.fin-tag{font-size:11px;color:#b45309;background:rgba(251,191,36,0.14);border:1px solid rgba(251,191,36,0.35);padding:2px 9px;border-radius:10px}
.fin-table{width:100%;border-collapse:collapse;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden}
.fin-table tr{border-bottom:1px solid #eef2f7}
.fin-table tr:last-child{border-bottom:none}
.fin-table td{padding:10px 14px;font-size:13px;color:#334155}
.fin-table td:first-child{width:130px;color:#64748b}
.fin-table .val{color:#b45309;font-weight:600}
.fin-note{font-size:12px;color:#64748b;margin-top:8px;line-height:1.6}
"""

CHAIN_LINKS = [
    ("银行", "berkshire-bank-chains.html"),
    ("白酒", "berkshire-baijiu-chains.html"),
    ("AI", "berkshire-ai-chains.html"),
    ("机器人", "berkshire-robot-chains.html"),
    ("中药", "berkshire-tcm-chains.html"),
    ("创新药", "berkshire-innov-chains.html"),
    ("家电", "berkshire-appliance-chains.html"),
    ("电力", "berkshire-power-chains.html"),
    ("煤炭", "berkshire-coal-chains.html"),
    ("有色", "berkshire-metal-chains.html"),
    ("化工", "berkshire-chem-chains.html"),
    ("电力设备", "berkshire-equip-chains.html"),
]


def nav_span(accent, current):
    parts = []
    for label, href in CHAIN_LINKS:
        bold = ";font-weight:700" if label == current else ""
        parts.append('<a href="%s" style="color:%s;text-decoration:none;font-size:13px%s">%s</a>' % (href, accent, bold, label))
    return '<span style="display:inline-flex;gap:12px;align-items:center;margin-left:10px;flex-wrap:wrap">' + ''.join(parts) + '</span>'


def top_bar(accent, current, breadcrumb_html):
    return ('<div class="top-bar">\n'
            '<a href="berkshire-standalone.html" class="home-btn">← 数据中心</a>\n'
            + nav_span(accent, current) + '\n'
            '<div class="breadcrumb">\n' + breadcrumb_html + '\n</div>\n</div>')


def css_for(accent, rgb, dark):
    return CSS.replace('__ACC__', accent).replace('__ACC_RGB__', rgb).replace('__ACC_DARK__', dark)


# ============ 产业周期判断标准（定性框架，写实；非数据结论） ============
CYCLE = {
    'power': {
        'criteria': '''<p><b>驱动变量</b>：全社会用电量增速（宏观晴雨表）、发电设备<b>利用小时数</b>（供需松紧）、<b>煤价</b>（火电成本）、来水（水电）、风光装机与消纳、容量电价政策。</p>
<ul>
<li><b>利用小时数</b>：低位企稳回升 → 供需改善、景气拐点；持续下行 → 过剩。</li>
<li><b>煤价（秦皇岛港 Q5500）</b>：下行 + 利用小时回升 → 火电盈利双击；暴涨 → 成本压制。</li>
<li><b>来水</b>：偏丰 → 水电大年；偏枯 → 水电承压、火电补位。</li>
<li><b>新能源消纳</b>：装机高增但弃风弃光率抬升 → 瓶颈；强配储能缓解。</li>
<li><b>政策</b>：容量电价机制 → 火电从"电量"转向"容量+调节"盈利，弱化周期波动。</li>
</ul>''',
        'current': '电力呈"弱周期+公用事业化"：容量电价弱化火电波动，利用小时与煤价是核心观察变量；当前火电盈利稳定性提升，水电看丰枯，新能源重消纳与电价机制落地。'
    },
    'coal': {
        'criteria': '''<p><b>驱动变量</b>：宏观经济与用电/粗钢/水泥产量（需求）、产地安监与保供（供给）、进口煤性价比、港口与电厂库存、长协价 vs 市场价。</p>
<ul>
<li><b>库存</b>（环渤海港/秦皇岛、电厂库存天数）：高位累库+煤价跌 → 供给宽松/需求弱；低位去库+煤价涨 → 紧平衡。</li>
<li><b>煤价</b>（CCI/Q5500）：长协价 570–770 元/吨区间托底，市场价围绕波动；突破上沿 → 供需偏紧信号。</li>
<li><b>安监</b>：矿难/环保督察趋严 → 供给收缩、价格支撑。</li>
<li><b>进口价差</b>：印尼/澳煤到岸价低于内贸 → 进口补充、压制内价。</li>
</ul>''',
        'current': '煤炭周期看"库存+煤价+安监"三角：当前长协占比高、供给受控，波动收敛，投资逻辑从周期弹性转向高分红与现金回报，周期属性弱化。'
    },
    'metal': {
        'criteria': '''<p><b>分品种逻辑</b>：工业金属（铜/铝）看全球宏观与美元、LME/SHFE 库存、铜冶炼费 TC/RC；贵金属（金）看实际利率与美元、央行购金；能源金属（锂/钴/镍）看供需平衡与成本曲线。</p>
<ul>
<li><b>工业金属</b>：LME+SHFE 库存持续去化+价升 → 景气；铜精矿 TC 跌破低位 → 矿端紧张、冶炼利润承压；铝看能耗双控与水电铝成本。</li>
<li><b>贵金属</b>：美债实际收益率下行、美元走弱、央行购金 → 金价支撑。</li>
<li><b>能源金属</b>：锂价跌破高成本矿现金成本 → 底部锚；过剩出清+需求放量 → 回升。</li>
<li><b>美元与实际利率</b>：美元走弱/实际利率下行 → 工业金属与黄金皆受益。</li>
</ul>''',
        'current': '有色按品种判周期：工业金属看库存+美元+TC，贵金属看实际利率+央行购金，能源金属看成本曲线与过剩出清；当前铜强、金稳、锂处产能出清寻底阶段。'
    },
    'chem': {
        'criteria': '''<p><b>驱动变量</b>：原油/煤炭（成本端）、PPI 与制造业景气（需求）、地产/汽车/纺服/农业（下游）、产能投放节奏、产品价差。</p>
<ul>
<li><b>价差</b>（单位利润）：触底回升 + 资本开支见顶 → 景气反转；价差新高+产能集中投放 → 见顶回落。</li>
<li><b>产能利用率/投产周期</b>：大规模新装置集中投产 → 供给过剩、降价；投产尾声+老旧产能出清 → 拐点。</li>
<li><b>PPI</b>：同比回升 → 化工品价格中枢上移、补库需求。</li>
<li><b>油价</b>：成本推动 + 库存收益（涨价时库存增值）。</li>
</ul>''',
        'current': '化工周期核心是"价差+产能投放"：当前多子行业经历产能扩张后进入出清与价差磨底，具备"剩者为王"逻辑的龙头更具韧性，关注资本开支见顶信号。'
    },
    'equip': {
        'criteria': '''<p><b>驱动变量</b>：光伏新增装机（全球）、锂价（电池成本）、电网投资与特高压、储能装机、海外（逆变器/储能出海看利率与电网改造）。</p>
<ul>
<li><b>产业链价格</b>（硅料→硅片→电池→组件）：价格见底企稳+需求放量 → 盈利修复；持续下跌 → 内卷、产能出清中。</li>
<li><b>产能出清</b>：二三线厂商现金流断裂/停产 → 供给收缩；行业 CR 提升。</li>
<li><b>储能与出海</b>：海外利率下行 → 储能需求释放；电网投资加速 → 特高压/变压器订单。</li>
<li><b>电池</b>：碳酸锂价格企稳 → 库存减值压力缓解。</li>
</ul>''',
        'current': '电力设备（光储锂网）周期看"价格底+产能出清+出海"：当前光伏链深度内卷、产能过剩，处于价格底与出清观察期；储能与电网侧呈结构性景气。'
    },
    'tcm': {
        'criteria': '''<p><b>驱动变量</b>：医保/基药目录调整、OTC 提价能力、中药材价格周期（成本）、国企改革与机制理顺、消费属性（保健品/养生）。</p>
<ul>
<li><b>中药材价格指数</b>（如康美·中国中药材价格指数）：上行 → 成本压力、考验提价传导；回落 → 毛利修复。</li>
<li><b>政策</b>：中医药振兴、基药/医保放量、国企改革（混改/激励）释放经营活力。</li>
<li><b>消费</b>：可选消费景气影响保健品与礼品属性品种。</li>
<li><b>提价权</b>：品牌 OTC（独家品种）具备定价权，可对冲成本。</li>
</ul>''',
        'current': '中药周期看"药材价格+政策+消费+提价权"：当前药材价格高位波动、消费偏弱，具备定价权与改革红利的龙头更稳，关注基药目录与国企改革催化。'
    },
    'innov': {
        'criteria': '''<p><b>驱动变量</b>：临床管线进展（Ph1/2/3 读出）、BD（license-out/引进）交易、医保谈判降幅、biotech 融资环境、海外利率（美股/港股流动性）。</p>
<ul>
<li><b>管线读出</b>：关键临床数据阳性 → 估值重估；失败 → 回撤（非传统产能周期，而是"研发—商业化—估值"三段）。</li>
<li><b>BD 大年</b>：重磅 license-out 首付款/里程碑 → 验证研发价值、现金流改善。</li>
<li><b>医保谈判</b>：降幅温和 → 放量可期；降幅大 → 以价换量。</li>
<li><b>融资/利率</b>：海外降息 → 港股 18A/biotech 估值修复；美元基金回流。</li>
</ul>''',
        'current': '创新药无传统产能周期，看"管线读出+BD出海+利率/融资"：当前处出海 BD 大年与港股估值修复期，行业逻辑从融资寒冬转向兑现期，关注重磅数据与安全边际。'
    },
    'appliance': {
        'criteria': '''<p><b>驱动变量</b>：地产（新房+二手房装修）、以旧换新/补贴政策、出口（海外去库/补库）、原材料（铜铝钢塑料）、份额集中与高端化。</p>
<ul>
<li><b>内销</b>：地产竣工链 + 以旧换新补贴 → 拉动更新需求；地产下行靠存量更新对冲。</li>
<li><b>出口</b>：海外去库存尾声→补库 → 外销回暖；汇率与海运影响。</li>
<li><b>原材料</b>：铜铝钢塑料价格 → 影响毛利率（成本传导有滞后）。</li>
<li><b>份额</b>：CR 提升、高端化 → 均价与利润上行，弱化行业周期。</li>
</ul>''',
        'current': '家电周期看"地产+补贴+出口+原材料"：当前以旧换新政策托底内销、出口韧性强，龙头凭份额集中与高端化穿越周期，关注补贴延续与外销补库。'
    },
}


# 财务 / 估值占位框架（不编造数字，待逐家抓取真实数据后填充）
FIN_PLACEHOLDER = '''
<div class="section-title">财务数据（待采集）</div>
<div class="fin-block">
  <div class="fin-head"><div class="fin-title"><span class="icon">📊</span> 关键财务（最新可得年报）</div><span class="fin-tag">待采集</span></div>
  <table class="fin-table">
    <tr><td>营业总收入</td><td class="val">— 待采集</td></tr>
    <tr><td>归母净利润</td><td class="val">— 待采集</td></tr>
    <tr><td>毛利率</td><td class="val">— 待采集</td></tr>
    <tr><td>ROE（加权）</td><td class="val">— 待采集</td></tr>
    <tr><td>资产负债率</td><td class="val">— 待采集</td></tr>
    <tr><td>经营现金流净额</td><td class="val">— 待采集</td></tr>
  </table>
  <div class="fin-note">占位框架：待逐家抓取最新年报（以 2025 年报为主）后填充真实数值，并标注报告期与数据来源。</div>
</div>

<div class="section-title">估值指标（待采集）</div>
<div class="fin-block">
  <div class="fin-head"><div class="fin-title"><span class="icon">💰</span> 估值快照</div><span class="fin-tag">待采集</span></div>
  <table class="fin-table">
    <tr><td>总市值</td><td class="val">— 待采集</td></tr>
    <tr><td>PE（TTM）</td><td class="val">— 待采集</td></tr>
    <tr><td>PB</td><td class="val">— 待采集</td></tr>
    <tr><td>股息率</td><td class="val">— 待采集</td></tr>
  </table>
</div>
'''


def detail_extra(c, accent):
    cyc = CYCLE.get(c['key'], {'criteria': '', 'current': ''})
    return FIN_PLACEHOLDER + '''
<div class="section-title">产业周期判断标准（%s）</div>
<div class="cycle-block">
<div class="cycle-title"><span class="icon">🔄</span> 本行业周期怎么看</div>
<div class="cycle-body">%s</div>
<div class="cycle-current">完整判断标准与指标清单见<a href="berkshire-%s-chains.html#cycle" style="color:#%s">《%s》索引页 →</a></div>
</div>''' % (c['name'], cyc['current'], c['key'], accent, c['name'])


# ============ 数据 ============
CHAINS = []


# ---------- 电力 ----------
power = {
    'key': 'power', 'name': '电力产业链', 'short': '电力龙头', 'icon': '⚡',
    'accent': '0ea5e9', 'accent_rgb': '14,165,233', 'accent_dark': '08263b', 'nav_label': '电力',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 燃料与资源', 'desc': '煤、天然气、铀、水能、风能与光照——发电的「原料」与资源禀赋，决定成本与可持续性'},
        {'n': '02', 'name': '中游 · 发电运营', 'desc': '火电 / 水电 / 核电 / 风电 / 光伏等多种电源，把资源转化为电力，利用小时与电价是核心'},
        {'n': '03', 'name': '下游 · 电网与售电', 'desc': '输配电网络、调度与售电侧，连接电厂与终端用户，受管制电价影响大'},
        {'n': '04', 'name': '消费与场景', 'desc': '工商业、居民、数据中心与电动车充电——电力是经济活动的底层能源'},
        {'n': '05', 'name': '投资逻辑', 'desc': '公用事业属性、稳定现金流与高股息；风险在煤价 / 来水 / 利用小时 / 电价管制与新能源挤压'},
    ],
    'companies': [
        {'slug': 'cypc', 'name': '长江电力', 'code': '600900', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '全球最大水电上市公司，运营三峡 / 葛洲坝 / 溪洛渡等巨型水电站。',
         'stats': [('水电', '全球最大'), ('三峡', '核心资产'), ('高股息', '防御属性')],
         'overview': '长江电力是三峡集团水电运营平台，管理三峡、葛洲坝、溪洛渡、向家坝、乌东德、白鹤滩六座巨型水电站，总装机规模全球第一。水电成本极低（无燃料）、现金流高度稳定，是A股稀缺的「类债」高股息资产。公司通过资产注入持续做大，并以投资收益平滑来水波动。',
         'layers': [
             '水资源依托长江上游梯级电站群，流域联合调度兼顾发电与防洪。来水丰枯决定发电量，是公司最核心的自然变量。',
             '巨型水轮机组运营，无燃料成本、变动成本极低。折旧完成后经营现金流近乎纯利，盈利质量极高。',
             '电量经特高压外送华东 / 华南，并参与市场化交易。作为优先调度电源，消纳与电价均有保障。',
             '工商业与居民基础用电的压舱石，也是西电东送骨干。用电需求刚性且随经济长期增长，波动小。',
             '护城河 = 稀缺流域资源 + 极低边际成本 + 稳定现金流。风险 = 来水波动、电价政策调整、新能源挤压调峰价值。'],
         'info': [('核心资产', '三峡等六大水电站'), ('属性', '纯水电 / 高股息'), ('装机', '全球第一'), ('看点', '来水 + 外送 + 资产注入')],
         'moat': '长江上游稀缺水电资源独家运营，近乎零边际成本与极强现金流构成天然护城河。',
         'risks': '1）来水偏枯拖累发电量；2）上网电价政策调整；3）特高压外送与消纳波动；4）新能源装机增长挤压水电调峰价值。'},
        {'slug': 'huaneng', 'name': '华能国际', 'code': '600011', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '火电龙头，煤电为主、新能源转型加速。',
         'stats': [('火电', '装机龙头'), ('转型', '风光并进'), ('A+H', '两地上市')],
         'overview': '华能国际是国内最大火电上市公司之一，以煤电、燃机为主，同时大力布局风电与光伏，新能源装机占比快速提升。火电盈利高度依赖煤价与利用小时，煤价下行与容量电价机制改善盈利弹性；公司正从「纯火电」向「火 + 绿」综合电力运营商转型。',
         'layers': [
             '燃料以动力煤为主，长协煤 + 现货采购，煤价是利润核心变量。燃料成本约占火电变动成本七成以上。',
             '燃煤 / 燃气机组发电，煤电灵活性改造支撑电网调峰。利用小时与电价共同决定度电利润。',
             '电量送电网统购统销 + 市场化交易，容量电价提供托底。辅助服务收益随调峰需求上升。',
             '工商业与居民用电、迎峰度夏 / 冬保供主力电源。负荷中心机组利用效率高、电价承受力强。',
             '护城河 = 规模与区位 + 调峰能力。风险 = 煤价波动、利用小时下滑、新能源挤压、电价管制。'],
         'info': [('主业', '煤电 + 新能源'), ('转型', '风光占比提升'), ('盈利变量', '煤价 / 利用小时'), ('看点', '容量电价 + 绿电成长')],
         'moat': '庞大装机规模、优质负荷中心区位与火电调峰能力，构成转型期的过渡性壁垒。',
         'risks': '1）煤价大幅上行侵蚀利润；2）利用小时下滑；3）新能源平价挤压火电空间；4）环保与容量成本上升。'},
        {'slug': 'sxor', 'name': '三峡能源', 'code': '600905', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '三峡集团新能源旗舰，风光发电运营龙头。',
         'stats': [('风光', '装机领先'), ('三峡系', '集团旗舰'), ('绿电', '纯新能源')],
         'overview': '三峡能源是三峡集团新能源业务平台，专注风电（海风 + 陆风）与光伏发电的开发运营，装机规模在国内新能源运营商中居前。公司依托集团资源与资金优势，项目储备丰富，受益于「双碳」目标下的风光高景气，但电价市场化与弃风弃光是关注点。',
         'layers': [
             '风光资源获取（海风海域、西北风光大基地）是扩张前提。资源区位决定利用小时与度电成本。',
             '风电场 / 光伏电站建设运营，发电成本随技术进步持续下降。初始资本开支大、负债率偏高。',
             '并网消纳经电网，市场化交易比例上升，电价承压。绿电环境价值（绿证）是增量收入来源。',
             '替代化石能源的清洁电力，工商业绿电需求增长。海风贴近负荷中心、消纳条件优于三北陆风。',
             '护城河 = 资源获取 + 集团资金。风险 = 电价下行、弃风弃光、补贴退坡、资本开支大。'],
         'info': [('主业', '风电 + 光伏'), ('属性', '纯绿电运营商'), ('优势', '集团资源 / 资金'), ('关注', '电价 / 消纳')],
         'moat': '集团背书下的优质风光资源获取能力与低成本资金，构成规模扩张壁垒。',
         'risks': '1）新能源电价市场化下行；2）局部弃风弃光；3）补贴回收与退坡；4）重资产扩张推高负债。'},
        {'slug': 'cnnc', 'name': '中国核电', 'code': '601985', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '核电运营双寡头之一，机组稳健发电 + 新能源补充。',
         'stats': [('核电', '双寡头'), ('机组', '批量化'), ('稳健', '基荷电源')],
         'overview': '中国核电是中核集团旗下核电运营平台，与中广核同为国内核电双寡头。核电作为稳定基荷电源，利用小时高、成本稳定（燃料占比低），在「双碳」下审批提速。公司同时在运风光项目，打造「核电 + 新能源」组合，但安全与审批节奏是核心变量。',
         'layers': [
             '铀燃料供给（国内 + 进口），核燃料成本高占比低且长期稳定。燃料成本对利润影响远小于煤電。',
             '压水堆机组批量化运营，建造与运维壁垒极高。单机组投资大、建设周期长，先发者优势明显。',
             '并网作为基荷电源，优先调度，电量经电网统销。利用小时高且稳定，现金流可预测性强。',
             '清洁基荷电力，替代煤电、支撑电网稳定。在新能源高占比下，核电的调峰补充价值上升。',
             '护城河 = 核电牌照 + 技术 / 安全壁垒。风险 = 审批节奏、安全事故、电价、核燃料。'],
         'info': [('主业', '核电 + 新能源'), ('地位', '双寡头之一'), ('特性', '高利用小时'), ('关注', '新机组审批')],
         'moat': '核电运营牌照稀缺、建造运维技术壁垒与安全文化，构成极强进入壁垒。',
         'risks': '1）新机组审批不及预期；2）核安全事件（极低概率高影响）；3）电价与消纳；4）在建资本开支庞大。'},
        {'slug': 'guodian', 'name': '国电电力', 'code': '600795', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '国家能源集团旗舰，水火风光多元发电。',
         'stats': [('多元', '水火风光'), ('国能', '集团旗舰'), ('转型', '绿电提速')],
         'overview': '国电电力是国家能源集团电力上市平台，资产涵盖火电、水电、风电、光伏，装机结构多元。依托集团煤炭与运输协同，火电燃料保障强；新能源转型持续推进，整体盈利随煤价与来水波动。',
         'layers': [
             '集团煤电路港航一体化协同，燃料供给与成本可控。长协煤覆盖度高，平滑煤价冲击。',
             '多元电源运营（煤电 / 水电 / 新能源），组合平滑单一电源波动。水电与新能源占比提升改善盈利质量。',
             '电网统销 + 市场化交易，煤电托底保供。容量电价与辅助服务拓展收入。',
             '工商业 / 居民用电，综合能源供应商角色。多电源结构适配不同负荷与季节。',
             '护城河 = 集团协同 + 多元结构。风险 = 煤价、利用小时、新能源电价、整合。'],
         'info': [('结构', '水火风光多元'), ('背景', '国家能源集团'), ('优势', '煤电路协同'), ('看点', '绿电占比提升')],
         'moat': '集团煤电路港一体化协同与多元电源组合，形成成本与稳定性优势。',
         'risks': '1）煤价波动；2）利用小时变化；3）新能源电价下行；4）多业务整合管理难度。'},
        {'slug': 'datang', 'name': '大唐发电', 'code': '601991', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '火电为主的老牌发电央企，转型绿电。',
         'stats': [('火电', '老牌央企'), ('转型', '新能源'), ('A+H', '两地上市')],
         'overview': '大唐发电是五大发电集团之一大唐集团的旗舰，以火电为主，近年加速风光布局。历史上受煤价高企与高负债拖累，盈利波动大；在煤价回落与新能源发力下修复，但仍需关注债务与利用小时。',
         'layers': [
             '动力煤采购为主，长协覆盖度影响成本。燃料成本波动直接传导至利润。',
             '燃煤机组为主，部分燃机与新能源。存量机组役龄较长，改造升级影响效率。',
             '电网统销 + 市场化，容量机制改善。新能源电量市场化交易比例上升。',
             '工商业 / 居民保供电源。作为老牌央企，区域保供责任与政策约束并存。',
             '护城河 = 规模与央企资质。风险 = 煤价、负债、利用小时、新能源竞争。'],
         'info': [('主业', '煤电 + 新能源'), ('属性', '五大发电央企'), ('修复', '煤价回落'), ('关注', '债务 / 利用小时')],
         'moat': '央企发电资质与规模装机，提供转型期的基本盘。',
         'risks': '1）煤价上行；2）历史高负债与财务费；3）利用小时下滑；4）新能源挤压。'},
        {'slug': 'huadian', 'name': '华电国际', 'code': '600027', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '华电集团火电平台，煤电为主 + 新能源。',
         'stats': [('火电', '华电平台'), ('A+H', '两地上市'), ('转型', '绿电')],
         'overview': '华电国际是华电集团核心电力上市平台，以煤电、燃机为主，新能源逐步补充。盈利随煤价与利用小时波动，煤价下行与容量电价改善弹性；公司推进向综合能源运营商转型。',
         'layers': [
             '动力煤长协 + 现货，燃料成本敏感。长协占比与煤价走势决定度电毛利。',
             '燃煤 / 燃机发电，灵活性改造支撑调峰。燃机启停快、适合峰谷调节。',
             '电网统购统销 + 市场电，容量电价托底。辅助服务收益贡献提升。',
             '工商业 / 居民保供主力。负荷中心机组利用小时与电价较优。',
             '护城河 = 规模 + 区位。风险 = 煤价、利用小时、电价、新能源。'],
         'info': [('主业', '煤电 + 新能源'), ('背景', '华电集团'), ('弹性', '煤价敏感'), ('看点', '容量电价')],
         'moat': '规模装机与负荷中心区位，构成区域供电壁垒。',
         'risks': '1）煤价波动；2）利用小时下滑；3）电价管制；4）新能源挤压。'},
        {'slug': 'shenergy', 'name': '申能股份', 'code': '600642', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '上海能源平台，电力 + 燃气双主业。',
         'stats': [('上海', '区域龙头'), ('电+气', '双主业'), ('稳健', '现金流好')],
         'overview': '申能股份是上海国资能源平台，业务涵盖电力（煤电 / 气电 / 新能源）与城市燃气，区域垄断性强、现金流稳健。受益上海高电价与燃气刚需，盈利波动小于纯火电，是防御性电力标的。',
         'layers': [
             '本地煤 / 气采购，气电依赖进口 LNG 与管道气。气价与煤价双因素共同影响电力成本。',
             '煤电 / 气电 / 新能源本地运营，保障城市供应。气电启停灵活、适合调峰与应急。',
             '电网统销 + 本地燃气管网直供，价格机制稳定。管网资产沉没成本高、区域排他。',
             '上海工商业 / 居民用电用气，刚需强。高电价环境支撑较好的度电利润。',
             '护城河 = 区域牌照 + 管网。风险 = 燃料价、电价、气量、政策。'],
         'info': [('主业', '电力 + 燃气'), ('区域', '上海国资'), ('特性', '防御稳健'), ('看点', '本地垄断')],
         'moat': '上海区域电力与燃气特许经营权及管网资产，构成稳定区域壁垒。',
         'risks': '1）煤 / 气燃料价格上行；2）电价政策；3）气量波动；4）本地项目空间有限。'},
        {'slug': 'zheenergy', 'name': '浙能电力', 'code': '600023', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '浙江火电龙头，煤电为主 + 新能源。',
         'stats': [('浙江', '区域龙头'), ('煤电', '主力'), ('分红', '稳健')],
         'overview': '浙能电力是浙江能源集团电力平台，以煤电为主、新能源补充，服务浙江高负荷用电省份。盈利随煤价改善，利用小时受省内用电支撑；分红稳定，具防御属性。',
         'layers': [
             '动力煤采购，省内港口物流便利。沿海布局运力与库存管理占优。',
             '燃煤机组为主，清洁化改造推进。高参数机组煤耗低、效率高。',
             '电网统销 + 市场电，省内消纳好。浙江电力供需偏紧、利用小时有支撑。',
             '浙江工商业 / 居民高用电，需求旺。外向型经济使用电与出口景气相关。',
             '护城河 = 区域负荷 + 规模。风险 = 煤价、利用小时、电价、新能源。'],
         'info': [('主业', '煤电 + 新能源'), ('区域', '浙江'), ('特性', '高利用小时'), ('看点', '分红稳健')],
         'moat': '高负荷省份规模装机与稳定消纳，提供区域供电壁垒。',
         'risks': '1）煤价波动；2）利用小时变化；3）电价市场化；4）新能源挤压。'},
        {'slug': 'yuedian', 'name': '粤电力A', 'code': '000539', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '广东电力平台，火电 + 新能源。',
         'stats': [('广东', '区域平台'), ('转型', '绿电'), ('A+B', '两地')],
         'overview': '粤电力是广东省能源集团电力上市平台，以火电为主并大力发展海上风电等新能源。广东用电需求旺盛、电价较高，但煤价与利用小时影响盈利；海风资源优质是成长看点。',
         'layers': [
             '动力煤采购，部分进口煤。广东本地煤价受进口与运费影响。',
             '燃煤 / 燃机 + 海上风电运营。海风资源优质、利用小时高，是成长主力。',
             '电网统销 + 市场电，省内高电价。市场化交易比例高、电价弹性大。',
             '广东工商业 / 居民高需求，海风绿电。制造业大省用电韧性强。',
             '护城河 = 区域资源 + 海风。风险 = 煤价、利用小时、电价、投产节奏。'],
         'info': [('主业', '火电 + 海风'), ('区域', '广东'), ('看点', '海上风电'), ('特性', '高电价')],
         'moat': '广东高电价市场与优质海上风电资源，构成区域成长壁垒。',
         'risks': '1）煤价上行；2）利用小时波动；3）海风投产不及预期；4）电价政策。'},
        {'slug': 'longyuan', 'name': '龙源电力', 'code': '001289', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '全球最大风电运营商，国家能源集团新能源平台。',
         'stats': [('风电', '全球最大'), ('国能', '集团平台'), ('A+H', '回A')],
         'overview': '龙源电力是国家能源集团新能源旗舰，长期为全球最大风电运营商，陆风 + 海风并举，并布局光伏。由H股回A后融资能力增强，受益于风光高景气，但电价市场化与弃风是关注点。',
         'layers': [
             '风资源获取（三北 / 海风），资源禀赋决定项目质量。风参数是项目IRR的核心输入。',
             '风电场建设运营，发电成本随风机大型化下降。利用小时与风速直接相关。',
             '并网消纳经电网，市场电比例上升。特高压外送改善三北弃风。',
             '清洁电力替代化石能源，绿电需求增长。海风贴近负荷中心、消纳更佳。',
             '护城河 = 资源 + 集团资金。风险 = 电价下行、弃风、补贴、资本开支。'],
         'info': [('主业', '风电 + 光伏'), ('地位', '全球风电领先'), ('优势', '集团资源'), ('关注', '电价 / 消纳')],
         'moat': '龙头风资源获取能力与集团资金优势，构筑规模壁垒。',
         'risks': '1）新能源电价下行；2）弃风限电；3）补贴回收；4）重资产扩张负债。'},
    ],
}
CHAINS.append(power)


# ---------- 煤炭 ----------
coal = {
    'key': 'coal', 'name': '煤炭产业链', 'short': '煤炭龙头', 'icon': '🪨',
    'accent': 'a8a29e', 'accent_rgb': '168,162,158', 'accent_dark': '1c1a17', 'nav_label': '煤炭',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 勘探与开采', 'desc': '地质勘探、井工 / 露天开采，资源储量与煤质是根本'},
        {'n': '02', 'name': '中游 · 洗选与煤化工', 'desc': '原煤洗选提质、焦化与煤制烯烃等转化'},
        {'n': '03', 'name': '下游 · 运输与销售', 'desc': '铁路 / 港口 / 航运发运，长协 + 市场煤销售'},
        {'n': '04', 'name': '消费与场景', 'desc': '电煤（火电）、炼焦煤（钢铁）、建材与化工原料'},
        {'n': '05', 'name': '投资逻辑', 'desc': '高分红 / 资源储量 / 煤价周期；风险在能源转型、价格与政策'},
    ],
    'companies': [
        {'slug': 'shenhua', 'name': '中国神华', 'code': '601088', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '煤电运一体化龙头，现金牛 + 高分红标杆。',
         'stats': [('一体化', '煤电路港'), ('高分红', '现金牛'), ('央企', '龙头')],
         'overview': '中国神华是国能集团旗下煤炭龙头，拥有「煤—电—路—港—航」一体化产业链，自产煤成本低、长协占比高、现金流极优，长期高分红，是A股稀缺的防御型现金牛。在能源转型背景下，其低成本与高分红提供安全边际。',
         'layers': [
             '陕北 / 蒙东等优质动力煤矿区，储量大、开采成本低。资源禀赋与井工露天协同开采，决定单位开采成本优势。',
             '原煤洗选 + 自营坑口电厂（煤电一体），转化增值。洗选提质提高商品煤热值，坑口电厂就近消纳原煤、平滑煤价波动。',
             '自营铁路（神朔 / 朔黄）+ 黄骅港 + 航运，运力自主管控。自营运输网络锁定运费，保障长协煤稳定发运、降低外运依赖。',
             '电煤（长协保供火电）、煤化工原料，下游刚性。长协电煤绑定重点电厂、履约稳定，需求受电力与化工刚需支撑。',
             '护城河 = 一体化低成本 + 运输自控；风险 = 煤价周期、能源转型、长协政策。低成本与高分红提供安全边际；核心变量在煤价中枢与转型节奏。'],
         'info': [('模式', '煤电运一体化'), ('特性', '低成本高分红'), ('资产', '矿 + 路 + 港'), ('看点', '分红确定性')],
         'moat': '煤电路港航一体化带来的成本与运力掌控，构成极深护城河。',
         'risks': '1）煤炭价格下行；2）长期能源转型压制需求；3）长协电价联动；4）安全生产与环保。'},
        {'slug': 'shaanxi', 'name': '陕西煤业', 'code': '601225', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '优质动力煤龙头，高分红高 ROE。',
         'stats': [('动力煤', '优质'), ('高ROE', '盈利强'), ('分红', '优厚')],
         'overview': '陕西煤业拥有陕北优质动力煤资源，煤质好、开采成本低、机械化程度高，盈利能力与ROE长期居行业前列。公司高分红、高现金流，是动力煤板块的标杆，但受煤价周期与陕北运力影响。',
         'layers': [
             '陕北亿吨级矿区，煤质优、剥采比低、成本低。优质动力煤资源禀赋与低剥采比，是开采成本领先的根本。',
             '大型现代化矿井开采，洗选提质。大型机械化矿井提升单井效率，洗选提高商品煤附加值。',
             '经浩吉等铁路外运，销售覆盖华中 / 华北。铁路干线运力决定外销半径，华中与华北是核心消纳市场。',
             '电煤为主，下游火电刚需。电煤需求随火电出力波动，长协机制稳定销售基本盘。',
             '护城河 = 优质低成本资源；风险 = 煤价、运力、安监、转型。高 ROE 来自低本高效，变量在煤价与运力瓶颈。'],
         'info': [('资源', '陕北优质动力煤'), ('特性', '低本高ROE'), ('销售', '铁路外运'), ('看点', '高分红')],
         'moat': '极优的资源禀赋与低成本开采，构成强盈利护城河。',
         'risks': '1）煤价大幅下行；2）运力瓶颈；3）安全监管限产；4）能源转型。'},
        {'slug': 'yanzhou', 'name': '兖矿能源', 'code': '600188', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '华东煤炭龙头，煤化一体 + 海外资产。',
         'stats': [('煤化', '一体'), ('A+H', '两地'), ('海外', '资产广')],
         'overview': '兖矿能源是华东地区煤炭龙头，煤炭开采与煤化工（甲醇、醋酸、煤制烯烃）一体化，并拥有澳大利亚等海外煤矿资产。规模大、产业链延伸深，但化工景气与海外运营是变量。',
         'layers': [
             '山东 / 陕蒙 / 澳洲多基地开采，资源多元。多区域资源布局分散单一矿区风险，海外资产贡献增量储量。',
             '煤炭洗选 + 煤化工转化（甲醇 / 烯烃），延伸价值链。煤化一体将原料煤转化为化工品，提升吨煤增值。',
             '铁路 + 港口 + 海运发运，内外贸并行。港口与海运打通内外贸渠道，出口煤对冲国内周期。',
             '电煤、化工原料煤、焦化多用途。煤种多元适配电煤与化工多场景，需求结构更均衡。',
             '护城河 = 煤化一体 + 海外资源；风险 = 煤价、化工景气、汇率、海外政策。煤化协同增强抗周期，变量在化工景气与汇率。'],
         'info': [('模式', '煤化一体化'), ('资产', '国内 + 澳洲'), ('看点', '化工延伸'), ('关注', '海外运营')],
         'moat': '煤化一体与跨国产线布局，形成产业链与资源壁垒。',
         'risks': '1）煤价与化工品下行；2）海外资产政策 / 汇率；3）安监限产；4）资本开支。'},
        {'slug': 'zhongmei', 'name': '中煤能源', 'code': '601898', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '央企煤炭龙头，煤化一体 + 煤电。',
         'stats': [('央企', '煤炭龙头'), ('煤化', '一体'), ('A+H', '两地')],
         'overview': '中煤能源是央企煤炭骨干企业，煤炭生产为主，配套煤化工（烯烃、尿素、甲醇）与坑口电力。资源储量丰富、长协占比高，盈利随煤价波动，煤化一体增强抗周期。',
         'layers': [
             '山西 / 内蒙 / 江苏等矿区，动力煤与炼焦煤兼具。煤种多元兼顾动力与冶炼需求，资源组合更具弹性。',
             '煤炭洗选 + 煤化工（煤制烯烃 / 化肥），产业链延伸。坑口煤化工就地转化，降低外运依赖并提升附加值。',
             '铁路 + 港口发运，长协为主。长协销售为主，铁路港口保障重点客户履约。',
             '电煤、化工煤、冶炼煤多下游。下游覆盖电力、化工、钢铁，需求分散降低单一周期冲击。',
             '护城河 = 资源 + 煤化一体；风险 = 煤价、化工景气、安监、转型。央企资源储备提供规模底盘，变量在化工景气。'],
         'info': [('背景', '央企煤炭'), ('模式', '煤化一体'), ('产品', '动力 + 炼焦 + 化工'), ('看点', '长协稳定')],
         'moat': '央企资源储备与煤化一体布局，提供规模与抗周期能力。',
         'risks': '1）煤价周期；2）煤化工景气下行；3）安监限产；4）转型压力。'},
        {'slug': 'sxjk', 'name': '山西焦煤', 'code': '000983', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '焦煤龙头，炼焦精煤核心供应商。',
         'stats': [('焦煤', '龙头'), ('精煤', '焦化原料'), ('山西', '资源大省')],
         'overview': '山西焦煤是国内炼焦煤龙头，主产焦精煤、肥精煤等，是钢铁冶炼不可或缺的原料。焦煤资源稀缺、区位集中，盈利随钢价与焦煤价格联动，与宏观周期高度相关。',
         'layers': [
             '山西优质焦煤矿区，主焦煤资源稀缺。主焦煤资源禀赋稀缺，区位集中决定议价能力。',
             '原煤洗选产出焦精煤 / 肥精煤，提质增值。洗选决定精煤回收率与品质，是焦煤价值核心环节。',
             '铁路发运至华北 / 华东钢厂。铁路直达钢厂，运输半径与运力影响销售节奏。',
             '下游钢铁冶炼（焦炭原料），强周期。焦煤需求绑定钢铁景气，钢厂开工是核心变量。',
             '护城河 = 稀缺焦煤资源；风险 = 钢价、焦煤价、安监、需求。稀缺煤种提供安全边际，变量在钢价与进口煤冲击。'],
         'info': [('主业', '炼焦精煤'), ('资源', '山西焦煤'), ('下游', '钢铁'), ('看点', '稀缺煤种')],
         'moat': '稀缺主焦煤资源与区位，构成强周期资源壁垒。',
         'risks': '1）钢铁需求下滑；2）焦煤价格下行；3）安监限产；4）进口焦煤冲击。'},
        {'slug': 'luan', 'name': '潞安环能', 'code': '601699', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '喷吹煤龙头，焦煤喷吹一体化。',
         'stats': [('喷吹煤', '龙头'), ('焦煤', '资源'), ('山西', '基地')],
         'overview': '潞安环能是喷吹煤细分龙头，喷吹煤可替代焦炭、降本增效，在钢厂中需求稳定；同时拥有焦煤资源。盈利随煤价与钢铁景气波动，资源与品种优势明显。',
         'layers': [
             '山西矿区，贫煤 / 瘦煤为主，适合作喷吹煤。煤种适配喷吹用途，品种差异化构筑需求粘性。',
             '洗选产出喷吹煤与炼焦配煤。洗选决定喷吹煤指标，配煤能力影响钢厂采购偏好。',
             '铁路发运至钢厂。铁路直供钢厂，运力与合同绑定销售。',
             '钢铁喷吹与冶炼，降本原料。喷吹煤替代部分焦炭降本，需求随钢厂降本意愿波动。',
             '护城河 = 喷吹煤品种 + 资源；风险 = 钢价、煤价、安监、需求。品种壁垒提供溢价，变量在钢价与替代技术。'],
         'info': [('品种', '喷吹煤'), ('下游', '钢铁'), ('资源', '山西'), ('看点', '品种优势')],
         'moat': '喷吹煤细分品种壁垒与焦煤资源，构成差异化优势。',
         'risks': '1）钢铁周期下行；2）喷吹煤价格回落；3）安监限产；4）替代技术。'},
        {'slug': 'huaibei', 'name': '淮北矿业', 'code': '600985', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '华东焦煤 + 煤化工，煤焦化一体。',
         'stats': [('焦煤', '华东'), ('煤化', '焦化'), ('安徽', '基地')],
         'overview': '淮北矿业地处华东，主产炼焦煤并配套焦炭与煤化工（甲醇、焦油），煤—焦—化一体化贴近华东钢铁市场，区位与产业链协同强，但焦炭与化工景气影响利润。',
         'layers': [
             '安徽矿区，炼焦煤资源。华东焦煤资源贴近钢铁市场，区位降低运输成本。',
             '洗选 + 焦化 + 煤化工（甲醇等）产业链。煤—焦—化一体将原煤转化为焦炭与化工品，延伸增值。',
             '铁路 / 水运至华东钢厂与化工厂。铁水联运直达华东客户，区位协同缩短交付半径。',
             '钢铁焦炭、化工原料多下游。焦炭与化工品双下游，需求随钢焦与化工景气联动。',
             '护城河 = 区位 + 焦化一体；风险 = 钢价、焦化景气、煤价、安监。华东区位与一体化协同稳固基本盘，变量在焦化利润。'],
         'info': [('模式', '煤焦化一体'), ('区位', '华东'), ('产品', '焦煤 + 焦炭 + 化工'), ('看点', '区位协同')],
         'moat': '华东区位与煤焦化产业链协同，形成市场与成本优势。',
         'risks': '1）钢铁 / 焦炭景气下行；2）煤价波动；3）安监限产；4）化工价差收窄。'},
        {'slug': 'jizhong', 'name': '冀中能源', 'code': '000937', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '河北煤炭，煤种齐全 + 化工。',
         'stats': [('河北', '煤企'), ('多元', '煤种'), ('冶金', '原料')],
         'overview': '冀中能源是河北骨干煤炭企业，煤种涵盖炼焦与动力煤，并涉足化工与医药，区域保供角色明显。盈利随煤价波动，多元业务平抑但管理复杂度高。',
         'layers': [
             '河北 / 山西矿区，焦煤与动力煤兼具。煤种多元兼顾冶炼与电煤，区域资源提供保供角色。',
             '洗选 + 煤化工（PVC等）延伸。洗选与煤化工延伸，提升资源综合利用率。',
             '铁路 / 公路发运至华北钢企与电厂。铁公联运覆盖华北客户，区域保供属性强。',
             '电煤、冶炼煤、化工原料。下游覆盖电力、钢铁、化工，需求结构多元。',
             '护城河 = 区域资源 + 多元；风险 = 煤价、化工景气、安监、整合。区域资源提供基本盘，变量在多元业务整合。'],
         'info': [('区域', '河北'), ('煤种', '焦 + 动'), ('延伸', '化工 / 医药'), ('看点', '区域保供')],
         'moat': '河北区域资源与多元业务，提供基本盘与协同。',
         'risks': '1）煤价周期；2）化工景气；3）安监限产；4）多业务整合。'},
        {'slug': 'pingmei', 'name': '平煤股份', 'code': '601666', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '主焦煤龙头，冶炼精煤核心。',
         'stats': [('主焦煤', '龙头'), ('冶炼', '精煤'), ('河南', '基地')],
         'overview': '平煤股份（平煤神马）是国内优质主焦煤供应商，主焦煤资源稀缺，是大型钢厂核心配料。盈利随钢价与焦煤价联动，资源稀缺性提供安全边际，但强周期属性明显。',
         'layers': [
             '河南矿区，主焦煤资源稀缺优质。稀缺主焦煤资源禀赋，是钢企核心配料来源。',
             '洗选产出冶炼精煤，提质增值。洗选决定精煤品质与回收率，是价值创造核心。',
             '铁路发运至华中 / 华东钢厂。铁路直达重点钢厂，运力影响销售半径。',
             '钢铁冶炼主焦煤料，强周期。需求绑定钢铁景气，钢厂开工是核心变量。',
             '护城河 = 主焦煤稀缺资源；风险 = 钢价、煤价、安监、需求。稀缺资源提供安全边际，变量在钢价与进口冲击。'],
         'info': [('主业', '主焦煤'), ('资源', '稀缺'), ('下游', '钢铁'), ('看点', '稀缺煤种')],
         'moat': '稀缺主焦煤资源与钢企粘性，构成资源壁垒。',
         'risks': '1）钢铁需求下滑；2）焦煤价格回落；3）安监限产；4）进口煤冲击。'},
        {'slug': 'shanmei', 'name': '山煤国际', 'code': '600546', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '煤炭贸易 + 自产，海运销一体。',
         'stats': [('贸易', '煤炭'), ('自产', '矿井'), ('海运', '销一体')],
         'overview': '山煤国际兼具煤炭贸易与自产矿井，拥有港口与海运销售网络，贸易量庞大、周转快。自产煤成本低，贸易贡献流量；盈利受煤价与贸易价差影响，模式灵活但波动较大。',
         'layers': [
             '山西自产矿井 + 外购煤源。自产 + 外购双源，灵活调节贸易量与成本。',
             '洗选 + 贸易中转，港口堆存。港口堆存与洗选中转，支撑贸易周转效率。',
             '自有港口 + 海运，销往沿海终端。自有港口海运锁定物流，辐射沿海终端市场。',
             '电煤、化工煤贸易与自产并行。贸易与自产并行，需求随电煤与化工煤景气波动。',
             '护城河 = 贸易网络 + 港口；风险 = 煤价、贸易价差、库存、政策。流通网络提供周转优势，变量在煤价与贸易价差。'],
         'info': [('模式', '贸易 + 自产'), ('资产', '港口海运'), ('特性', '周转快'), ('关注', '煤价 / 价差')],
         'moat': '煤炭贸易网络与港口海运资产，形成流通壁垒。',
         'risks': '1）煤价大幅波动；2）贸易价差收窄；3）库存跌价；4）政策调控。'},
        {'slug': 'sxjh', 'name': '山西焦化', 'code': '600740', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '焦炭龙头，焦煤焦化一体。',
         'stats': [('焦炭', '龙头'), ('焦化', '为主'), ('山西', '基地')],
         'overview': '山西焦化以焦炭生产为主，配套焦炉煤气制甲醇等化产，处于「焦煤—焦炭—钢铁」链条中游。盈利受焦煤成本与焦炭价差（焦化利润）驱动，强周期、波动大。',
         'layers': [
             '采购炼焦煤（山西本地 + 外购）。焦煤采购成本与来源稳定性，决定焦化利润空间。',
             '焦炉炼焦 + 化产（甲醇 / 焦油）回收。焦炉副产化产回收，提升吨焦综合收益。',
             '铁路 / 公路供周边钢厂。直供周边钢厂，运力与钢焦博弈影响出货。',
             '钢铁冶炼焦炭原料，强周期。焦炭需求绑定钢厂生产，钢焦利润博弈是核心。',
             '护城河 = 焦化产能 + 化产回收；风险 = 焦化利润、煤价、钢价、环保。化产回收增厚利润，变量在焦化利润与环保限产。'],
         'info': [('主业', '焦炭'), ('化产', '甲醇等'), ('下游', '钢铁'), ('看点', '焦化利润')],
         'moat': '焦化产能与化产回收能力，构成中游加工壁垒。',
         'risks': '1）焦化利润（钢焦博弈）收窄；2）焦煤成本上行；3）环保限产；4）钢铁需求。'},
    ],
}
CHAINS.append(coal)


# ---------- 有色 ----------
metal = {
    'key': 'metal', 'name': '有色产业链', 'short': '有色龙头', 'icon': '🪙',
    'accent': 'a78bfa', 'accent_rgb': '167,139,250', 'accent_dark': '1c1430', 'nav_label': '有色',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 勘探与采矿', 'desc': '地质勘探、矿山开采（露天 / 地下），资源储量与品位是根本'},
        {'n': '02', 'name': '中游 · 冶炼与精炼', 'desc': '矿石冶炼、电解精炼，能耗与工艺决定成本'},
        {'n': '03', 'name': '下游 · 加工与材料', 'desc': '铜铝加工、合金、锂电材料等深加工'},
        {'n': '04', 'name': '消费与场景', 'desc': '新能源（电车 / 储能）、电子、建筑、电力、珠宝首饰'},
        {'n': '05', 'name': '投资逻辑', 'desc': '资源储量 / 价格周期 / 供需格局；风险在金属价格、宏观与地缘'},
    ],
    'companies': [
        {'slug': 'zijin', 'name': '紫金矿业', 'code': '601899', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '金铜锂多元矿业龙头，逆周期并购扩张。',
         'stats': [('金铜', '双核心'), ('锂', '新增长'), ('并购', '逆周期')],
         'overview': '紫金矿业从紫金山金矿起家，发展为金、铜、锂多元矿业龙头，以逆周期并购（如刚果金卡莫阿铜矿、西藏巨龙铜矿）和低品位矿高效开发著称。规模与资源储量快速扩张，受益于金价与铜价上行，但海外运营与价格波动是变量。',
         'layers': [
             '全球布局矿山（中国 / 非洲 / 南美 / 中亚），勘探与并购并举。逆周期并购与低品位矿高效开发，是资源储量扩张的核心。',
             '露天 / 地下开采 + 选矿冶炼，低品位矿石利用技术强。选冶技术决定低品位矿经济可采性，摊薄单位成本。',
             '阴极铜、金锭等冶炼精炼，副产品回收。冶炼精炼回收多金属副产品，提升综合收率与收益。',
             '新能源（铜锂）、电子、珠宝、基建多场景。铜锂需求受新能源与基建拉动，珠宝投资支撑金价。',
             '护城河 = 资源储量 + 低成本开发 + 并购能力；风险 = 金属价、海外政治、汇率、安环。低成本开发 + 并购构成成长壁垒，变量在金价铜价与地缘。'],
         'info': [('品类', '金 / 铜 / 锂'), ('特质', '逆周期并购'), ('资源', '全球布局'), ('看点', '铜金价格')],
         'moat': '全球资源储量与低品位高效开发 + 逆周期并购能力，构成成长型矿业壁垒。',
         'risks': '1）金价 / 铜价下行；2）海外资产政治与社区风险；3）汇率波动；4）安全环保。'},
        {'slug': 'jiangxi', 'name': '江西铜业', 'code': '600362', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '国内铜业龙头，采选冶加一体化。',
         'stats': [('阴极铜', '产量大'), ('一体化', '采选冶'), ('A+H', '两地')],
         'overview': '江西铜业是国内最大铜生产商之一，拥有德兴铜矿等自有资源并进口矿补充，业务涵盖采矿、冶炼、加工（铜杆、线、箔）全链条。盈利受铜价与冶炼费（TC/RC）影响，加工端向高端（锂电铜箔）延伸。',
         'layers': [
             '自有矿山（德兴等）+ 进口矿，资源保障部分自给。自有矿部分自给、进口矿补充，原料保障影响冶炼规模。',
             '闪速熔炼等冶炼，阴极铜产量居前。闪速熔炼工艺与规模决定阴极铜成本与产量。',
             '铜加工（杆 / 线 / 箔），拓展新能源用铜。加工端向铜箔等高端延伸，提升吨铜附加值。',
             '电力、新能源、电子、建筑用铜。铜需求覆盖电力新能源与建筑，新能源用铜增长快。',
             '护城河 = 规模 + 全链条 + 资源；风险 = 铜价、冶炼费、需求、环保。全链条规模提供壁垒，变量在铜价与冶炼费TC/RC。'],
         'info': [('主业', '铜采选冶加'), ('资源', '自有 + 进口'), ('延伸', '铜箔 / 新能源'), ('关注', '铜价 / TC')],
         'moat': '国内铜业规模与采选冶加一体化，构成产业链壁垒。',
         'risks': '1）铜价波动；2）冶炼费（TC/RC）下行；3）下游需求走弱；4）环保与能耗。'},
        {'slug': 'chalco', 'name': '中国铝业', 'code': '601600', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '氧化铝与电解铝龙头，央企背景。',
         'stats': [('氧化铝', '领先'), ('电解铝', '规模'), ('央企', '中铝')],
         'overview': '中国铝业是中铝集团核心上市平台，业务覆盖铝土矿、氧化铝、电解铝及铝加工，氧化铝产能全球领先。盈利受铝价与氧化铝价格、能源成本（电解耗电大）影响显著，绿电铝是转型方向。',
         'layers': [
             '铝土矿（国内 + 海外几内亚等）资源保障。铝土矿资源布局决定原料自给与成本安全。',
             '氧化铝冶炼 + 电解铝（高耗电），能源成本是关键。电解铝耗电高，电价是吨铝成本的核心变量。',
             '铝加工材（板带箔），拓展交通 / 包装。加工材向交通包装延伸，提升铝材附加值。',
             '建筑、交通、电力、包装用铝。铝需求覆盖建筑交通电力，绿电铝契合低碳趋势。',
             '护城河 = 资源 + 规模 + 央企；风险 = 铝价、电价、产能过剩、碳约束。全产业链规模提供壁垒，变量在铝价与电价。'],
         'info': [('主业', '铝土 / 氧化铝 / 电解铝'), ('背景', '中铝集团'), ('变量', '铝价 / 电价'), ('看点', '绿电铝')],
         'moat': '铝土矿资源与全产业链规模，构成铝业龙头壁垒。',
         'risks': '1）铝价与氧化铝价下行；2）电价上行（电解耗电）；3）行业产能过剩；4）碳关税与能耗约束。'},
        {'slug': 'lomo', 'name': '洛阳钼业', 'code': '603993', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '铜钴钼多元龙头，刚果金核心资产。',
         'stats': [('铜钴', '刚果金'), ('钼', '龙头'), ('多元', '金属组合')],
         'overview': '洛阳钼业是铜、钴、钼、铌、磷多元矿业公司，核心资产为刚果金 Tenke 铜钴矿（全球重要钴来源）与国内钼钨。新能源（钴、铜）需求提振估值，但刚果金运营与金属价格是关键变量。',
         'layers': [
             '刚果金铜钴矿 + 国内钼钨矿，勘探扩产。Tenke 铜钴矿资源储量决定全球钴供给地位。',
             '铜钴矿开采冶炼，钴为新能源电池关键原料。钴冶炼产能绑定新能源电池链，需求受电车拉动。',
             '阴极铜、钴盐等精炼产品。精炼钴盐直供电池材料厂，客户结构集中。',
             '新能源电池、特钢、合金多场景。钴铜需求受新能源与特钢驱动，电池是核心增量。',
             '护城河 = 优质铜钴资源 + 多元组合；风险 = 钴铜价、刚果政治、汇率、供给。顶级铜钴资源提供壁垒，变量在金属价与刚果政局。'],
         'info': [('主业', '铜 / 钴 / 钼'), ('核心', '刚果金Tenke'), ('需求', '新能源'), ('关注', '金属价')],
         'moat': '全球级铜钴资源与多元金属组合，构成新能源金属壁垒。',
         'risks': '1）铜钴价格下行；2）刚果金政治与物流；3）汇率波动；4）供给过剩（钴）。'},
        {'slug': 'sdgold', 'name': '山东黄金', 'code': '600547', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '黄金龙头，资源增储提速。',
         'stats': [('黄金', '龙头'), ('增储', '提速'), ('A+H', '两地')],
         'overview': '山东黄金是国内黄金开采龙头，拥有胶东半岛核心金矿，通过并购（如内蒙、海外）持续增储。盈利与金价高度正相关，避险与通胀预期下弹性大，但资源品位与开采成本影响利润。',
         'layers': [
             '胶东金矿带核心资源，勘探与并购增储。胶东金矿带资源禀赋与增储，决定长期可采储量。',
             '地下开采 + 选矿冶炼，产金锭 / 金精矿。地下开采与选冶回收率，决定克金成本。',
             '黄金冶炼与精炼，标准金锭交付。标准金锭交付上期所品牌，流通渠道畅通。',
             '投资避险、珠宝首饰、央行储备。黄金需求来自避险、首饰与央行购金，金价弹性大。',
             '护城河 = 优质金矿资源 + 增储能力；风险 = 金价、品位、成本、安监。优质金矿 + 增储提供壁垒，变量在金价与品位。'],
         'info': [('主业', '黄金开采'), ('资源', '胶东核心'), ('弹性', '金价'), ('看点', '增储并购')],
         'moat': '胶东半岛优质黄金资源与持续增储，构成贵金属壁垒。',
         'risks': '1）金价大幅下行；2）矿石品位下降；3）开采成本上升；4）安全与环保监管。'},
        {'slug': 'zhongjin', 'name': '中金黄金', 'code': '600489', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '央企黄金平台，金铜并举。',
         'stats': [('黄金', '央企'), ('铜', '补充'), ('中金', '集团')],
         'overview': '中金黄金是中国黄金集团旗下上市平台，以黄金开采冶炼为主，并拥有部分铜钼资源。受益金价上行，集团资产注入预期提供增储空间，但同样受金价与成本驱动。',
         'layers': [
             '国内多省金矿，集团资源注入预期。集团资产注入预期，是储量增长的关键来源。',
             '地下开采 + 冶炼，产金锭与金精矿。采冶规模与回收率，决定产量与成本。',
             '黄金精炼与标准金交付。标准金交付渠道稳定，变现便捷。',
             '避险投资、首饰、工业用金。需求受避险与首饰拉动，金价驱动弹性。',
             '护城河 = 央企资源 + 增储预期；风险 = 金价、成本、品位、安监。央企资源 + 注入预期提供壁垒，变量在金价。'],
         'info': [('背景', '中国黄金集团'), ('主业', '黄金 + 铜'), ('看点', '资产注入'), ('关注', '金价')],
         'moat': '央企背景与集团资源注入预期，构成增储潜力壁垒。',
         'risks': '1）金价波动；2）开采成本；3）品位变化；4）安全监管限产。'},
        {'slug': 'yunlu', 'name': '云铝股份', 'code': '000807', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '绿电铝标杆，水电铝一体化。',
         'stats': [('绿电铝', '标杆'), ('水电', '云南'), ('低碳', '优势')],
         'overview': '云铝股份地处云南，依托水电的绿色能源生产电解铝，碳足迹低，「绿电铝」在碳约束与出口场景中具备溢价。盈利随铝价与电价（水电成本低）波动，中铝集团协同。',
         'layers': [
             '云南铝土矿 + 中铝集团氧化铝供应。集团氧化铝供应保障原料，区位决定能源结构。',
             '水电电解铝，低碳排放是核心优势。水电电解铝碳足迹低，绿电是成本与溢价核心。',
             '铝加工（板带箔），交通 / 包装方向。加工材向交通包装延伸，提升附加值。',
             '建筑、交通、电力、包装用铝。铝需求覆盖多领域，绿电铝契合出口碳要求。',
             '护城河 = 绿电低成本 + 低碳溢价；风险 = 铝价、来水、电价、需求。绿电低碳构成差异化壁垒，变量在铝价与来水。'],
         'info': [('属性', '绿电铝'), ('能源', '云南水电'), ('优势', '低碳'), ('看点', '碳溢价')],
         'moat': '水电绿电铝的低成本与低碳属性，构成差异化壁垒。',
         'risks': '1）铝价下行；2）来水波动影响水电；3）限电与能耗；4）下游需求。'},
        {'slug': 'shenhuo', 'name': '神火股份', 'code': '000933', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '煤铝双主业，低成本电解铝。',
         'stats': [('煤铝', '双业'), ('低成本', '铝'), ('分红', '较好')],
         'overview': '神火股份以「煤电 + 电解铝」双主业运营，电解铝布局云南（水电绿电）享低成本，煤炭提供稳定现金流。铝价与煤价共同驱动业绩，分红稳健，但周期属性强。',
         'layers': [
             '自有煤矿 + 云南绿电铝产能。煤电自给 + 云南水电铝，双源锁定能源成本。',
             '电解铝（低成本）+ 煤炭开采。云南绿电铝低成本，煤炭贡献稳定现金流。',
             '铝加工与煤炭销售。铝加工与煤炭销售双线，分散周期风险。',
             '建筑、交通用铝 + 电力用煤。铝与煤双下游，需求随地产与电力波动。',
             '护城河 = 煤铝协同 + 低成本铝；风险 = 铝价、煤价、电价、需求。煤铝协同对冲周期，变量在铝价与云南电价。'],
         'info': [('模式', '煤铝一体'), ('特性', '低成本铝'), ('现金流', '煤炭托底'), ('看点', '双周期')],
         'moat': '煤铝一体与低成本绿电铝，构成周期对冲壁垒。',
         'risks': '1）铝价下行；2）煤价波动；3）云南电价 / 来水；4）需求走弱。'},
        {'slug': 'tianqi', 'name': '天齐锂业', 'code': '002466', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '锂资源龙头，控股格林布什矿。',
         'stats': [('锂矿', '顶级'), ('格林布什', '控股'), ('高弹性', '锂价')],
         'overview': '天齐锂业通过控股全球顶级锂辉石矿格林布什（澳洲）与参股盐湖，掌握上游锂资源，中游做锂盐加工。业绩与锂价高度相关，曾因高杠杆并购承压，修复后资源属性突出，但锂价周期剧烈。',
         'layers': [
             '格林布什锂辉石矿（顶级）+ 盐湖参股，资源为王。格林布什顶级锂辉石，决定锂盐成本与资源壁垒。',
             '锂盐（碳酸锂 / 氢氧化锂）冶炼加工。锂盐冶炼规模与品位，决定吨锂成本。',
             '锂盐销售给正极材料与电池厂。锂盐直供正极与电池厂，客户集中度高。',
             '动力电池、储能电池核心原料。锂需求受动力电池与储能拉动，景气波动剧烈。',
             '护城河 = 顶级锂资源 + 成本优势；风险 = 锂价暴跌、需求、负债、供给过剩。顶级资源提供成本壁垒，变量在锂价与供需。'],
         'info': [('主业', '锂矿 + 锂盐'), ('核心', '格林布什'), ('弹性', '锂价'), ('关注', '供需')],
         'moat': '全球顶级锂辉石资源控股，构成锂资源端壁垒。',
         'risks': '1）锂价大幅下行；2）新能源汽车需求放缓；3）历史高杠杆；4）供给过剩。'},
        {'slug': 'ganfeng', 'name': '赣锋锂业', 'code': '002460', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '锂盐加工龙头，资源全球布局。',
         'stats': [('锂盐', '龙头'), ('资源', '全球布'), ('全链', '锂生态')],
         'overview': '赣锋锂业是锂盐加工龙头，业务覆盖锂矿（全球多处布局）、锂盐冶炼、金属锂与电池回收，构建「资源—冶炼—回收」闭环。业绩随锂价与加工价差波动，产业链完整但周期剧烈。',
         'layers': [
             '全球锂资源布局（矿石 + 盐湖 + 回收）。多元资源 + 回收布局，保障锂原料弹性。',
             '锂盐冶炼（碳酸锂 / 氢氧化锂）+ 金属锂。锂盐冶炼规模与加工价差，决定盈利。',
             '电池回收与深加工，闭环增效。回收闭环提升资源利用率，降低原料依赖。',
             '动力电池、储能、消费电子原料。锂需求覆盖动力储能与消费电子，景气联动。',
             '护城河 = 全产业链 + 资源布局；风险 = 锂价、加工价差、需求、供给。全产业链提供壁垒，变量在锂价与加工价差。'],
         'info': [('主业', '锂盐加工'), ('布局', '全球资源'), ('闭环', '回收'), ('关注', '锂价')],
         'moat': '锂盐全产业链与全球资源布局，构成加工与资源壁垒。',
         'risks': '1）锂价下行；2）加工价差收窄；3）需求放缓；4）资源开发不及预期。'},
        {'slug': 'huayou', 'name': '华友钴业', 'code': '603799', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '钴镍锂电材料龙头，一体化布局。',
         'stats': [('钴镍', '龙头'), ('一体化', '镍钴锂'), ('新能源', '材料')],
         'overview': '华友钴业从钴产品起家，向上游镍钴资源（印尼）与下游三元前驱体、正极材料延伸，打造「镍钴锂—前驱体—正极」一体化。受益新能源车，但镍钴价与产能释放是变量。',
         'layers': [
             '印尼镍钴资源开发 + 非洲钴布局。印尼镍钴资源布局，决定原料自给与成本。',
             '镍钴冶炼 + 三元前驱体 / 正极材料。前驱体正极一体化，提升镍钴增值深度。',
             '材料销售给电池与车企。材料直供电池与车企，客户绑定深。',
             '动力电池、储能材料核心。三元材料需求受新能源拉动，景气度高。',
             '护城河 = 镍钴资源 + 一体化材料；风险 = 镍钴价、产能、需求、竞争。资源 + 材料一体化壁垒，变量在镍钴价与产能。'],
         'info': [('主业', '钴镍 + 前驱体'), ('资源', '印尼镍'), ('延伸', '正极材料'), ('关注', '新能源')],
         'moat': '镍钴资源与锂电材料一体化，构成新能源材料壁垒。',
         'risks': '1）镍钴价格下行；2）产能释放不及预期；3）需求放缓；4）行业竞争加剧。'},
    ],
}
CHAINS.append(metal)


# ---------- 化工 ----------
chem = {
    'key': 'chem', 'name': '化工产业链', 'short': '化工龙头', 'icon': '🧪',
    'accent': '84cc16', 'accent_rgb': '132,204,22', 'accent_dark': '1a2408', 'nav_label': '化工',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 原料', 'desc': '原油 / 天然气 / 煤炭等化石原料，成本之锚'},
        {'n': '02', 'name': '中游 · 基础与炼化', 'desc': '乙烯 / 丙烯 / 芳烃、炼化一体化、煤化工'},
        {'n': '03', 'name': '下游 · 精细与材料', 'desc': '农药、钛白、聚酯、改性塑料等深加工'},
        {'n': '04', 'name': '消费与场景', 'desc': '地产 / 汽车 / 农业 / 消费 / 电子等终端需求'},
        {'n': '05', 'name': '投资逻辑', 'desc': '成本优势 / 产能周期 / 技术壁垒；风险在油价、产能过剩、景气'},
    ],
    'companies': [
        {'slug': 'wanhua', 'name': '万华化学', 'code': '600309', 'region': '中国', 'region_cls': 'region-cn',
         'desc': 'MDI 全球龙头，「化工茅」一体化典范。',
         'stats': [('MDI', '全球龙头'), ('一体化', '石化+精细'), ('研发', '驱动')],
         'overview': '万华化学以 MDI（聚氨酯核心原料）起家，全球产能与成本领先，并向上游石化（乙烯）与下游精细化学品、新材料延伸，形成一体化与研发驱动的护城河。盈利随 MDI 价格与石化景气波动，但成本与技术壁垒深厚。',
         'layers': [
             '苯胺等原料自制 + 石化乙烯项目供副产。关键原料自制与乙烯副产，支撑一体化成本。',
             'MDI 装置（技术壁垒极高）+ 石化 / 新材料。MDI 技术壁垒与单套规模，决定全球成本领先。',
             '聚氨酯、ADI、改性材料等多产品线。多产品线延伸，分散单一品种周期风险。',
             '家电、建材、汽车、鞋服等广泛用途。需求覆盖地产家电与汽车，宏观景气敏感。',
             '护城河 = MDI 技术 + 一体化成本 + 研发；风险 = MDI 价、石化景气、产能、需求。技术与研发构成深壁垒，变量在MDI价与石化景气。'],
         'info': [('主业', 'MDI+石化+新材料'), ('地位', '全球MDI领先'), ('优势', '一体化研发'), ('看点', '新材料')],
         'moat': 'MDI 技术壁垒与石化一体化低成本 + 持续研发，构成化工龙头护城河。',
         'risks': '1）MDI 价格下行；2）石化景气走弱；3）新产能投放；4）宏观需求。'},
        {'slug': 'rongsheng', 'name': '荣盛石化', 'code': '002493', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '炼化一体化龙头，浙石化核心资产。',
         'stats': [('炼化', '一体化'), ('浙石化', '巨无霸'), ('民营', '龙头')],
         'overview': '荣盛石化控股浙石化（4000万吨/年炼化一体化），是国内民营炼化龙头。炼化一体化带来成本与产品结构优势，盈利随油价与化工品价差波动，芳烃、烯烃及下游新材料是重点。',
         'layers': [
             '原油进口，大型码头与储罐保障。大型码头储罐保障原油接卸，原料适应性关键。',
             '炼化一体化（常减压 + 乙烯 + 芳烃）深加工。一体化装置提升重油转化与化工品收率。',
             '成品油、芳烃、烯烃及下游化工品。芳烃烯烃及下游延伸，产品矩阵丰富。',
             '纺织、包装、汽车等广泛下游。需求覆盖纺织包装汽车，宏观与油价联动。',
             '护城河 = 大型炼化一体化 + 规模；风险 = 油价、炼油价差、产能、需求。超大一体化规模构成成本壁垒，变量在油价与价差。'],
         'info': [('主业', '炼化一体化'), ('核心', '浙石化'), ('属性', '民营炼化'), ('关注', '油价 / 价差')],
         'moat': '超大炼化一体化规模与原料适应性，构成成本壁垒。',
         'risks': '1）油价剧烈波动；2）炼化价差收窄；3）新产能投放；4）需求走弱。'},
        {'slug': 'hengli', 'name': '恒力石化', 'code': '600346', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '炼化化纤一体化龙头，大连长兴岛基地。',
         'stats': [('炼化', '一体化'), ('化纤', '龙头'), ('民营', '炼化')],
         'overview': '恒力石化以「炼化—PTA—聚酯」一体化著称，大连长兴岛炼化项目打通全产业链，成本与效率领先。盈利受油价、PTA 与聚酯价差驱动，向下游新材料延伸。',
         'layers': [
             '原油炼化供 PTA 原料，自给率高。炼化供 PTA 原料自给，锁定上游成本。',
             '炼化 + PTA + 聚酯纤维一体化。全产业链一体化提升效率与单吨成本优势。',
             '涤纶长丝、薄膜、工程塑料。长丝薄膜塑料延伸，丰富产品组合。',
             '纺织服装、包装、电子材料。需求覆盖纺织包装电子，宏观敏感。',
             '护城河 = 全产业链一体化 + 规模效率；风险 = 油价、价差、产能、需求。一体化规模效率构成壁垒，变量在油价与价差。'],
         'info': [('模式', '炼化-PTA-聚酯'), ('基地', '长兴岛'), ('延伸', '新材料'), ('关注', '价差')],
         'moat': '炼化到聚酯全产业链一体化与规模效率，构成壁垒。',
         'risks': '1）油价波动；2）PTA / 聚酯价差收窄；3）产能投放；4）需求疲软。'},
        {'slug': 'weixing', 'name': '卫星化学', 'code': '002648', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '轻烃一体化龙头，C2/C3 产业链。',
         'stats': [('轻烃', '一体化'), ('C2/C3', '双链'), ('民营', '化工')],
         'overview': '卫星化学以轻烃（乙烷 / 丙烷）裂解制乙烯、丙烯的一体化模式见长，成本较油头路线低且清洁。连云港基地扩产，盈利随轻烃与产品价格价差波动，向新材料延伸。',
         'layers': [
             '进口乙烷 / 丙烷原料，码头与低温储运。自建码头低温储运，保障轻烃原料供应。',
             '轻烃裂解（乙烯 / 丙烯）+ 下游丙烯酸等。轻烃裂解成本低于油头，工艺清洁。',
             '高分子材料、SAP、电解液原料。下游延伸高分子与电解液料，提升增值。',
             '包装、卫生用品、新能源材料。需求覆盖包装卫材与新能源，景气分化。',
             '护城河 = 轻烃一体化低成本 + 码头；风险 = 原料价、价差、投产、需求。轻烃低成本 + 码头构成壁垒，变量在原料价与价差。'],
         'info': [('模式', '轻烃一体化'), ('双链', 'C2/C3'), ('优势', '低成本清洁'), ('看点', '新材料')],
         'moat': '轻烃一体化低成本与自建码头储运，构成成本壁垒。',
         'risks': '1）乙烷 / 丙烷价格上行；2）产品价差收窄；3）投产不及预期；4）需求走弱。'},
        {'slug': 'hualu', 'name': '华鲁恒升', 'code': '600426', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '煤化工标杆，多联产低成本。',
         'stats': [('煤化工', '标杆'), ('多联产', '协同'), ('低成本', '优势')],
         'overview': '华鲁恒升是煤化工标杆企业，以洁净煤气化平台实现尿素、DMF、醋酸、己二酸、乙二醇等多产品联产，柔性调节与低成本著称。盈利随产品价格与煤价差波动，管理水平行业领先。',
         'layers': [
             '烟煤原料，洁净煤气化平台统一供合成气。洁净煤气化平台统一供合成气，是低成本根源。',
             '多联产（尿素 / 醋酸 / DMF / 己二酸等）柔性切换。多联产柔性切换，按需调节产品结构与利润。',
             '肥料、胺类、羰基化产品多线。多线产品覆盖农业与化工，需求分散。',
             '农业、化工、材料广泛用途。需求覆盖农业化工材料，农化与工业景气分化。',
             '护城河 = 多联产协同 + 低成本 + 管理；风险 = 煤价、产品价格、产能、需求。多联产协同 + 极致管控构成壁垒，变量在煤化价差。'],
         'info': [('模式', '煤化工多联产'), ('优势', '低成本柔性'), ('管理', '领先'), ('关注', '煤化价差')],
         'moat': '洁净煤气化多联产平台与极致成本管控，构成煤化工壁垒。',
         'risks': '1）煤价上行；2）化工品价格下行；3）新产能；4）需求疲软。'},
        {'slug': 'baofeng', 'name': '宝丰能源', 'code': '600989', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '煤制烯烃龙头，绿氢耦合降本。',
         'stats': [('煤制烯烃', '龙头'), ('绿氢', '耦合'), ('低成本', '优势')],
         'overview': '宝丰能源以煤替代石油生产聚乙烯、聚丙烯（煤制烯烃），内蒙、宁夏基地规模大，成本低于油头路线；并布局太阳能电解水制绿氢耦合减排。盈利随聚烯烃价与煤价差波动。',
         'layers': [
             '本地烟煤原料，坑口就近。坑口就近用煤，运输成本低、供应稳定。',
             '煤制甲醇 + 甲醇制烯烃（CTO）装置。CTO 装置将煤转化为聚烯烃，成本低于油头。',
             '聚乙烯、聚丙烯等聚烯烃产品。聚烯烃产品覆盖包装建材，应用广泛。',
             '包装、建材、汽车等塑料用途。需求受包装建材汽车拉动，宏观敏感。',
             '护城河 = 煤制烯烃低成本 + 绿氢；风险 = 煤价、聚烯烃价、投产、碳约束。煤制烯烃低成本 + 绿氢构成壁垒，变量在煤烯价差。'],
         'info': [('主业', '煤制烯烃'), ('优势', '低成本'), ('看点', '绿氢耦合'), ('关注', '煤烯价差')],
         'moat': '煤制烯烃低成本与绿氢耦合减排，构成成本与低碳壁垒。',
         'risks': '1）煤价上行；2）聚烯烃价格下行；3）新产能投放；4）碳排放约束。'},
        {'slug': 'yangnong', 'name': '扬农化工', 'code': '600486', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '菊酯农药龙头，拟除虫菊酯领先。',
         'stats': [('农药', '菊酯龙头'), ('创制', '能力'), ('先正达', '系')],
         'overview': '扬农化工是拟除虫菊酯类农药龙头，产品涵盖杀虫剂、除草剂、杀菌剂，具备创制能力，并入先正达集团体系。盈利随农化景气与农产品周期波动，但技术壁垒与渠道稳固。',
         'layers': [
             '中间体部分自制，原料配套。中间体自配制套，保障原药供应稳定。',
             '菊酯原药 + 制剂，创制品种储备。创制品种储备与制剂能力，构筑技术壁垒。',
             '农药原药与制剂销售全球。原药制剂销全球，渠道覆盖广。',
             '农业病虫害防治，粮食安全相关。需求绑定农业病虫害防治，粮食安全支撑。',
             '护城河 = 菊酯技术 + 创制 + 渠道；风险 = 农化景气、原药价、政策、天气。菊酯技术 + 创制 + 渠道构成壁垒，变量在农化景气。'],
         'info': [('主业', '农药原药 / 制剂'), ('地位', '菊酯领先'), ('背景', '先正达系'), ('看点', '创制品种')],
         'moat': '拟除虫菊酯技术领先与创制能力 + 先正达渠道，构成壁垒。',
         'risks': '1）农化景气下行；2）原药价格回落；3）转基因 / 替代技术；4）环保与登记。'},
        {'slug': 'longbai', 'name': '龙佰集团', 'code': '002601', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '钛白粉龙头，氯化法技术领先。',
         'stats': [('钛白粉', '龙头'), ('氯化法', '领先'), ('钛', '全产业链')],
         'overview': '龙佰集团是钛白粉龙头，兼具硫酸法（传统）与氯化法（高端）工艺，并向上游钛矿、下游钛金属延伸。盈利随钛白粉价格与钛矿成本波动，氯化法技术构成差异化。',
         'layers': [
             '钛矿资源（国内 + 海外）保障原料。钛矿资源布局，决定原料自给与成本。',
             '硫酸法 + 氯化法钛白粉，氯化法壁垒高。氯化法工艺高端壁垒高，产品附加值优。',
             '钛白粉（涂料 / 塑料用）+ 钛金属延伸。钛白粉覆盖涂料塑料，向钛金属延伸。',
             '涂料、塑料、造纸、航天材料。需求覆盖涂料塑料造纸，地产与消费联动。',
             '护城河 = 氯化法技术 + 钛矿资源；风险 = 钛白粉价、矿价、需求、环保。氯化法 + 钛矿资源构成壁垒，变量在钛白粉价。'],
         'info': [('主业', '钛白粉'), ('工艺', '硫酸 + 氯化'), ('延伸', '钛矿 / 钛金属'), ('看点', '氯化法')],
         'moat': '氯化法高端工艺与钛矿资源，构成技术 + 资源壁垒。',
         'risks': '1）钛白粉价格下行；2）钛矿成本上行；3）下游需求走弱；4）环保。'},
        {'slug': 'tongkun', 'name': '桐昆股份', 'code': '601233', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '涤纶长丝龙头，PTA-聚酯一体。',
         'stats': [('长丝', '龙头'), ('聚酯', '规模'), ('民营', '化纤')],
         'overview': '桐昆股份是涤纶长丝龙头，桐乡基地规模领先，并向上游 PTA 延伸一体化。盈利随长丝与 PTA 价差波动，行业产能集中度高，龙头成本优势明显。',
         'layers': [
             'PTA 自供 + 外采，原料保障。PTA 自供保障原料，锁定上游成本。',
             'PTA + 涤纶长丝一体化生产。长丝一体化提升单吨效率与成本优势。',
             'POY / DTY / FDY 等长丝品种。多品种长丝覆盖不同织造需求。',
             '纺织服装面料核心原料。需求绑定纺织服装，出口与消费联动。',
             '护城河 = 长丝规模 + 一体化成本；风险 = 价差、产能、需求、油价。长丝规模 + 一体化构成壁垒，变量在长丝价差。'],
         'info': [('主业', '涤纶长丝'), ('模式', 'PTA-聚酯'), ('地位', '规模领先'), ('关注', '长丝价差')],
         'moat': '涤纶长丝规模与 PTA 一体化成本，构成化纤壁垒。',
         'risks': '1）长丝 / PTA 价差收窄；2）产能投放；3）纺织需求疲软；4）油价波动。'},
        {'slug': 'hengyi', 'name': '恒逸石化', 'code': '000703', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '炼化化纤龙头，文莱项目示范。',
         'stats': [('炼化', '文莱'), ('PTA', '规模'), ('一体化', '全产业链')],
         'overview': '恒逸石化以「炼油—PX—PTA—涤纶」一体化布局，文莱炼化项目打通上游，国内 PTA 产能规模大。盈利随炼化与 PTA 价差、油价波动，产业链完整但周期强。',
         'layers': [
             '文莱原油炼化供芳烃，PX 自给。文莱炼化供芳烃，PX 自给锁定原料。',
             'PTA + 聚酯纤维一体化。PTA 聚酯一体化提升效率与成本优势。',
             '涤纶长丝与瓶片。长丝瓶片双线，覆盖纺织与包装。',
             '纺织服装、包装。需求覆盖纺织包装，宏观敏感。',
             '护城河 = 全产业链 + 文莱炼化；风险 = 油价、价差、产能、需求。全产业链 + 文莱项目构成壁垒，变量在油价与价差。'],
         'info': [('模式', '炼化-PTA-聚酯'), ('海外', '文莱项目'), ('规模', 'PTA大'), ('关注', '价差')],
         'moat': '全产业链一体化与文莱炼化项目，构成成本壁垒。',
         'risks': '1）油价波动；2）PTA / 聚酯价差收窄；3）产能投放；4）需求走弱。'},
        {'slug': 'kingfa', 'name': '金发科技', 'code': '600143', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '改性塑料龙头，新材料平台。',
         'stats': [('改性塑料', '龙头'), ('新材料', '平台'), ('车', '轻量化')],
         'overview': '金发科技是改性塑料龙头，产品覆盖改性塑料、完全生物降解塑料、特种工程塑料，广泛服务于汽车、家电、电子。盈利随原料（石化树脂）价格与下游需求波动，研发与定制能力是壁垒。',
         'layers': [
             '石化树脂（PP / ABS 等）外采改性。树脂外采改性，原料价影响成本。',
             '改性塑料（增强 / 阻燃 / 增韧）配方与造粒。配方研发与造粒工艺，决定材料性能。',
             '车用、家电、电子、可降解材料。覆盖车家电电子，客户结构多元。',
             '汽车轻量化、家电外壳、包装。需求受汽车家电拉动，轻量化趋势支撑。',
             '护城河 = 配方研发 + 客户粘性；风险 = 树脂价、需求、竞争、可降解政策。配方研发 + 客户粘性构成壁垒，变量在树脂价与需求。'],
         'info': [('主业', '改性塑料'), ('延伸', '可降解 / 特塑'), ('客户', '车 / 家电'), ('看点', '新材料')],
         'moat': '改性塑料配方研发与头部客户粘性，构成材料壁垒。',
         'risks': '1）树脂原料价格上行；2）汽车 / 家电需求走弱；3）竞争加剧；4）可降解政策不及预期。'},
    ],
}
CHAINS.append(chem)


# ---------- 电力设备 ----------
equip = {
    'key': 'equip', 'name': '电力设备产业链', 'short': '电力设备龙头', 'icon': '🔋',
    'accent': '2dd4bf', 'accent_rgb': '45,212,191', 'accent_dark': '08251f', 'nav_label': '电力设备',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 材料与部件', 'desc': '锂盐 / 硅料 / 钢材 / 电子元器件，核心原料'},
        {'n': '02', 'name': '中游 · 设备制造', 'desc': '电池 / 组件 / 逆变器 / 变压器，制造壁垒'},
        {'n': '03', 'name': '下游 · 电站与电网', 'desc': '电站 EPC、电网建设、车企配套'},
        {'n': '04', 'name': '消费与场景', 'desc': '新能源车、光伏风电电站、储能、电网升级'},
        {'n': '05', 'name': '投资逻辑', 'desc': '技术迭代 / 规模 / 政策；风险在技术路线、价格战、产能过剩'},
    ],
    'companies': [
        {'slug': 'catl', 'name': '宁德时代', 'code': '300750', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '动力电池与储能全球龙头，技术规模双领先。',
         'stats': [('动力电池', '全球第一'), ('储能', '高增'), ('研发', '领先')],
         'overview': '宁德时代是全球动力电池与储能电池龙头，凭借麒麟 / 神行等电池技术与规模成本，绑定国内外主流车企与储能客户。盈利随动力电池装机与锂价波动，技术迭代与产能利用率是核心。',
         'layers': [
             '锂盐 / 正极 / 隔膜等外采 + 部分参股保供。关键材料外采 + 参股保供，保障供应链安全。',
             '电芯与电池包制造，技术迭代快（铁锂 / 三元）。电芯制造与快迭代技术，决定能量密度与成本。',
             '动力电池配套车企 + 储能系统出货。深度绑定车企与储能客户，出货量规模领先。',
             '新能源车、电网侧 / 工商业储能。需求受新能源车与储能装机拉动，景气高。',
             '护城河 = 技术 + 规模 + 客户绑定；风险 = 技术路线、价格战、锂价、竞争。技术规模 + 客户绑定构成壁垒，变量在技术路线与价格战。'],
         'info': [('主业', '动力电池 / 储能'), ('地位', '全球领先'), ('优势', '技术规模'), ('关注', '份额 / 毛利')],
         'moat': '电池技术领先、规模成本与深度客户绑定，构成极强壁垒。',
         'risks': '1）技术路线颠覆；2）价格战压缩毛利；3）锂价剧烈波动；4）二三线抢份额。'},
        {'slug': 'longi', 'name': '隆基绿能', 'code': '601012', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '单晶硅与组件龙头，BC 技术引领。',
         'stats': [('单晶', '硅片龙头'), ('组件', '领先'), ('BC', '技术')],
         'overview': '隆基绿能是单晶硅片与组件龙头，曾主导单晶 PERC 路线，现推进 HPBC 等新型电池技术。盈利受硅料 / 组件价格与行业产能过剩影响剧烈，技术领先但量价承压。',
         'layers': [
             '硅料外采 + 硅片拉棒切片自制。硅片拉棒切片自制，掌握核心环节成本。',
             '电池片（HPBC）+ 组件封装。HPBC 电池技术领先，组件效率决定溢价。',
             '组件销往电站 EPC 与分布式。组件直供电站与分布式，渠道覆盖广。',
             '光伏电站、分布式屋顶发电。需求受装机与电价政策拉动，波动大。',
             '护城河 = 单晶技术 + 品牌渠道；风险 = 价格战、产能过剩、技术迭代、硅价。单晶技术 + 渠道构成壁垒（同质化减弱），变量在硅价与产能。'],
         'info': [('主业', '硅片 / 电池 / 组件'), ('技术', 'HPBC'), ('地位', '单晶领先'), ('关注', '硅价 / 产能')],
         'moat': '单晶硅技术与品牌渠道积累，构成光伏壁垒（但壁垒随同质化减弱）。',
         'risks': '1）组件价格战；2）行业产能过剩；3）电池技术被超越；4）硅料价格剧烈。'},
        {'slug': 'sungrow', 'name': '阳光电源', 'code': '300274', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '逆变器与储能系统龙头。',
         'stats': [('逆变器', '全球领先'), ('储能', '系统'), ('光储', '协同')],
         'overview': '阳光电源是光伏逆变器与储能系统（PCS + 系统集成）龙头，受益于全球光储装机高增。盈利随装机与价格竞争波动，但逆变器技术品牌与储能集成能力构成差异化。',
         'layers': [
             '功率半导体等电子件外采。功率器件外采，供应链影响交付与成本。',
             '逆变器制造 + 储能 PCS / 系统集成。逆变器与储能集成技术，决定系统效率。',
             '销往电站、工商业与户用储能。覆盖电站工商与户用，渠道全球。',
             '光伏电站、电网侧 / 用户侧储能。需求受光储装机拉动，景气高。',
             '护城河 = 逆变器技术品牌 + 储能集成；风险 = 价格战、竞争、需求、毛利。逆变器品牌 + 储能集成构成壁垒，变量在价格战与毛利。'],
         'info': [('主业', '逆变器 / 储能'), ('地位', '全球领先'), ('协同', '光储'), ('关注', '毛利率')],
         'moat': '逆变器技术品牌与储能系统集成能力，构成差异化壁垒。',
         'risks': '1）逆变器价格战；2）储能竞争加剧；3）海外需求波动；4）毛利下滑。'},
        {'slug': 'tongwei', 'name': '通威股份', 'code': '600438', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '硅料与电池片双龙头，农牧起家。',
         'stats': [('硅料', '龙头'), ('电池片', '领先'), ('农牧', '起家')],
         'overview': '通威股份以饲料起家，后切入光伏，成为高纯晶硅（硅料）与太阳能电池片双龙头，并向下游组件延伸。盈利随硅料与电池片价格剧烈波动，垂直一体化但周期属性强。',
         'layers': [
             '工业硅外采制高纯晶硅（硅料）。高纯晶硅自制，掌握硅料成本核心。',
             '硅料 + 电池片（PERC / TOPCon）+ 组件。硅料电池组件一体，电池规模领先。',
             '组件销电站与分布式。组件直供电站分布式，渠道覆盖。',
             '光伏电站发电。需求受装机拉动，波动剧烈。',
             '护城河 = 硅料成本 + 电池规模；风险 = 价格战、产能过剩、技术、硅价。硅料成本 + 电池规模构成壁垒，变量在硅料价与产能。'],
         'info': [('主业', '硅料 / 电池 / 组件'), ('优势', '硅料成本'), ('延伸', '组件'), ('关注', '硅价')],
         'moat': '高纯晶硅成本领先与电池片规模，构成光伏中上游壁垒。',
         'risks': '1）硅料 / 电池价格战；2）产能过剩；3）技术迭代；4）下游需求。'},
        {'slug': 'jinko', 'name': '晶科能源', 'code': '688223', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '组件龙头，TOPCon 技术先行。',
         'stats': [('组件', '龙头'), ('TOPCon', '先行'), ('全球', '布局')],
         'overview': '晶科能源是全球光伏组件龙头之一，率先大规模量产 TOPCon 电池，海外渠道强。盈利随组件价格与行业产能波动，技术迭代与全球化是关键词。',
         'layers': [
             '硅片 / 电池外采或自制。硅片电池自制或外采，灵活调节产能。',
             'TOPCon 电池 + 组件封装。TOPCon 技术先行，组件效率领先。',
             '组件销全球电站与分布式。组件销全球，海外渠道强。',
             '光伏电站发电。需求受全球装机拉动，贸易影响大。',
             '护城河 = TOPCon 技术 + 全球渠道；风险 = 价格战、产能过剩、技术、贸易。TOPCon + 全球渠道构成壁垒，变量在组件价与贸易。'],
         'info': [('主业', '电池 / 组件'), ('技术', 'TOPCon'), ('渠道', '全球'), ('关注', '组件价')],
         'moat': 'TOPCon 技术先行与全球化渠道，构成组件壁垒。',
         'risks': '1）组件价格战；2）产能过剩；3）技术被超越；4）海外贸易壁垒。'},
        {'slug': 'trina', 'name': '天合光能', 'code': '688599', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '组件与跟踪支架龙头，一体化延伸。',
         'stats': [('组件', '领先'), ('支架', '跟踪'), ('一体化', '延伸')],
         'overview': '天合光能是光伏组件与跟踪支架龙头，布局硅片、电池、组件一体化，并拓展分布式与储能。盈利随组件价格与行业周期波动，渠道与品牌稳固。',
         'layers': [
             '硅片 / 电池自制 + 外采。硅片电池自制 + 外采，一体化灵活。',
             '电池 + 组件 + 跟踪支架制造。组件 + 跟踪支架协同，提升系统方案能力。',
             '组件与支架销电站、分布式。销电站与分布式，渠道品牌稳。',
             '光伏电站、工商业分布式。需求受装机与电价拉动。',
             '护城河 = 渠道品牌 + 一体化；风险 = 价格战、产能、技术、需求。渠道品牌 + 一体化构成壁垒，变量在组件价与需求。'],
         'info': [('主业', '组件 / 支架'), ('延伸', '硅片电池'), ('渠道', '全球'), ('关注', '组件价')],
         'moat': '组件渠道品牌与跟踪支架技术，构成差异化壁垒。',
         'risks': '1）组件价格战；2）产能过剩；3）技术迭代；4）需求走弱。'},
        {'slug': 'tebian', 'name': '特变电工', 'code': '600089', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '变压器与输变电龙头，硅料协同。',
         'stats': [('变压器', '龙头'), ('输变电', '设备'), ('硅料', '曾布局')],
         'overview': '特变电工是国内变压器、电线电缆与输变电成套设备龙头，受益电网投资与新能源外送；曾布局多晶硅，煤电热辅业。盈利随电网订单与硅料价格（历史）波动，输变电主业稳健。',
         'layers': [
             '铜铝 / 硅钢等原材料外采。铜铝硅钢外采，原材料价影响成本。',
             '变压器、电缆、换流阀等输变电设备。输变电设备制造，技术壁垒较高。',
             '电网 / 新能源电站设备供应与 EPC。供电网与新能源电站，订单绑定投资。',
             '电网升级、风光外送、海外电力。需求受电网投资与风光外送拉动。',
             '护城河 = 输变电技术 + 电网客户；风险 = 订单节奏、原材料、硅价、竞争。输变电技术 + 电网客户构成壁垒，变量在电网投资节奏。'],
         'info': [('主业', '变压器 / 输变电'), ('客户', '电网'), ('协同', '新能源'), ('关注', '电网投资')],
         'moat': '输变电设备技术与电网客户粘性，构成电力设备壁垒。',
         'risks': '1）电网投资不及预期；2）铜铝原材料价；3）硅料等业务波动；4）竞争。'},
        {'slug': 'nari', 'name': '国电南瑞', 'code': '600406', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '电网自动化与特高压龙头。',
         'stats': [('电网', '自动化'), ('特高压', '核心'), ('南瑞', '系')],
         'overview': '国电南瑞是电网自动化、调度、特高压直流控制保护龙头，背靠国网系，受益新型电力系统与电网数字化投资。盈利稳健、订单可见度高，但成长性受电网投资节奏影响。',
         'layers': [
             '电子元器件 / 软件自研为主。核心软硬件自研，技术自主可控。',
             '调度自动化、继电保护、直流控保设备。电网控保与调度软件，技术门槛高。',
             '电网 / 新能源并网系统交付。系统交付电网与新能源，订单可见度高。',
             '电网升级、新能源消纳、储能调控。需求受新型电力系统投资拉动。',
             '护城河 = 电网核心软硬件 + 国网系；风险 = 投资节奏、招标、毛利、技术。电网核心软件 + 国网系构成深壁垒，变量在投资节奏。'],
         'info': [('主业', '电网自动化'), ('地位', '特高压核心'), ('背景', '国网系'), ('看点', '新型电力系统')],
         'moat': '电网核心控制保护软件与国网体系壁垒，构成强护城河。',
         'risks': '1）电网投资节奏放缓；2）招标价格下行；3）毛利率压力；4）技术迭代。'},
        {'slug': 'dongfang', 'name': '东方电气', 'code': '600875', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '发电设备龙头，水电火电核电风光。',
         'stats': [('发电设备', '龙头'), ('多电', '源'), ('央企', '东方')],
         'overview': '东方电气是发电设备综合龙头，覆盖水电、火电、核电、风电、光伏设备，受益电源建设与新能源装机。盈利随电源投资与订单波动，设备制造壁垒高。',
         'layers': [
             '钢材 / 铸件等原材料外采。钢材铸件外采，原材料价影响成本。',
             '水轮 / 汽轮 / 风电机组等装备制造。全谱系发电设备制造，技术壁垒高。',
             '设备供电厂与电站 EPC。供各类电源建设，订单绑定电源投资。',
             '各类电源建设、风光装机。需求受电源与风光装机拉动。',
             '护城河 = 发电设备技术 + 多电源；风险 = 订单节奏、原材料、竞争、毛利。全谱系设备技术构成壁垒，变量在电源投资节奏。'],
         'info': [('主业', '发电设备'), ('覆盖', '水火核风光'), ('属性', '央企'), ('关注', '电源投资')],
         'moat': '全谱系发电设备技术与制造能力，构成设备壁垒。',
         'risks': '1）电源投资不及预期；2）原材料价；3）价格竞争；4）毛利率。'},
        {'slug': 'chint', 'name': '正泰电器', 'code': '601877', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '低压电器龙头，光伏分布式协同。',
         'stats': [('低压电器', '龙头'), ('户用', '光伏'), ('双业', '协同')],
         'overview': '正泰电器是低压电器龙头，并运营户用光伏（正泰安能）分布式电站，形成「低压电器 + 光伏」双主业。盈利随地产工控与户用光伏政策波动，渠道下沉优势明显。',
         'layers': [
             '铜 / 塑料等原材料外采。铜塑外采，原材料价影响成本。',
             '低压电器（断路器 / 接触器）+ 户用光伏系统。低压电器 + 户用光伏系统，双线制造。',
             '经销商网络 + 户用光伏开发。下沉经销商网络，渠道覆盖广。',
             '建筑、工控、户用屋顶发电。需求受地产工控与户用光伏政策拉动。',
             '护城河 = 低压渠道 + 户用光伏；风险 = 地产、原材料、补贴、竞争。低压渠道 + 户用开发构成壁垒，变量在地产与政策。'],
         'info': [('主业', '低压电器 + 户用光伏'), ('渠道', '下沉'), ('双业', '协同'), ('关注', '地产 / 政策')],
         'moat': '低压电器下沉渠道与户用光伏开发能力，构成双业壁垒。',
         'risks': '1）地产 / 工控需求走弱；2）原材料价；3）户用光伏政策；4）竞争。'},
        {'slug': 'goldwind', 'name': '金风科技', 'code': '002202', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '风电整机龙头，风光储一体。',
         'stats': [('风电', '整机龙头'), ('海风', '布局'), ('制造', '设备')],
         'overview': '金风科技是国内风电整机龙头，直驱永磁机组见长，布局陆风与海风，并拓展风电场运营与储能。盈利随风电装机与价格竞争波动，海风与运维是成长点。',
         'layers': [
             '钢材 / 叶片材料等外采。钢材叶片外采，原材料影响成本。',
             '风电机组制造（直驱永磁）+ 风场运营。直驱永磁机组技术，运行业绩背书。',
             '机组供开发商，自营风电场发电。供开发商 + 自营风场，双轮驱动。',
             '陆风 / 海风电站、绿电。需求受陆风海风装机拉动。',
             '护城河 = 整机技术 + 运行业绩；风险 = 价格战、装机节奏、海风、毛利。整机技术 + 运营经验构成壁垒，变量在装机节奏。'],
         'info': [('主业', '风电整机'), ('技术', '直驱永磁'), ('延伸', '风场 / 储能'), ('关注', '装机')],
         'moat': '风电整机技术与风场运营经验，构成设备 + 运营壁垒。',
         'risks': '1）风机价格战；2）风电装机不及预期；3）海风节奏；4）毛利率。'},
    ],
}
CHAINS.append(equip)


def render_index(c):
    accent = c['accent']; rgb = c['accent_rgb']; dark = c['accent_dark']
    css = css_for(accent, rgb, dark)
    layers_html = ''.join(
        '<div class="layer-card"><div class="layer-num">%s</div><div class="layer-name">%s</div><div class="layer-desc">%s</div></div>' % (L['n'], L['name'], L['desc'])
        for L in c['layers'])
    cards_html = ''.join(
        '<a class="giant-card" href="berkshire-%s-chain-%s.html"><div class="giant-head"><span class="giant-name">%s 链</span><span class="region-tag %s">%s</span></div><div class="giant-desc">%s</div><div class="giant-foot"><span class="giant-link">查看跨层分析 →</span></div></a>' % (c['key'], co['slug'], co['name'], co['region_cls'], co['region'], co['desc'])
        for co in c['companies'])
    breadcrumb = '<a href="berkshire-standalone.html">数据中心</a><span class="crumb-sep">/</span><span>%s</span>' % c['name']
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="initial-scale=1">
<title>%s · 价值投资视角</title>
<style>
%s
</style>
</head>
<body>
%s
<div class="container">

<div class="hero">
<div class="hero-title">%s</div>
<div class="hero-sub">%s</div>
<div class="hero-stats">
<div class="stat-item"><div class="stat-num">%s</div><div class="stat-label">上市公司</div></div>
<div class="stat-item"><div class="stat-num">5</div><div class="stat-label">产业层级</div></div>
<div class="stat-item"><div class="stat-num">原创</div><div class="stat-label">公开源整理</div></div>
</div>
</div>

<div class="data-banner">📊 <b>数据口径</b>：财务数据以各公司<b>最新可得年报</b>为准；估值 / 行情为<b>采集日快照</b>（实时行情接口当前环境不可用）。本页为框架级原创整理，<b>不构成投资建议</b>。最后更新：<span class="upd">2026-07-12</span></div>

<div class="explain-banner">
<div class="eb-icon">%s</div>
<div class="eb-body">
<div class="eb-title"><span class="eb-tag">资料说明</span> 这份「%s地图」是怎么来的</div>
<div class="eb-text">
本页是<b>借鉴产业链分析方法、用公开资料自行整理</b>的知识框架，把%s按「层级」拆解，便于从投资视角理解其护城河与周期风险。<br>
<b>资料来源</b>：各公司年报 / 官网 / 公开新闻 / 行业研报摘要——均为公开事实层；文中为框架级定性梳理，不编造具体财务数字，最新数据以公司公告为准。
</div>
</div>
</div>

<div class="section-title">跨层分析框架（5 层）</div>
<div class="layers">
%s
</div>

<div class="section-title">产业周期判断标准</div>
<div class="cycle-block" id="cycle"><div class="cycle-title"><span class="icon">🔄</span> %s 产业周期怎么看</div><div class="cycle-body">%s</div><div class="cycle-current"><b>当前位置（定性框架，非数据结论）</b>：%s</div></div>

<div class="section-title">%s索引（上市公司 %s 家）</div>
<div class="grid">
%s
</div>

<div class="source-note">
📌 <b>资料与合规</b>：本页所有分析均基于各公司<b>公开年报、官网、产品发布与新闻</b>等事实层信息，由本站原创整理与重写；不复制、不转载任何付费 / 闭源专享内容。文中对具体公司的判断仅作研究框架示例，<b>不构成投资建议</b>。
</div>

</div>
</body>
</html>''' % (c['name'], css, top_bar(accent, c['nav_label'], breadcrumb), c['name'], c['hero_sub'], c['n_companies'], c['icon'], c['name'], c['short'], layers_html, c['name'], CYCLE[c['key']]['criteria'], CYCLE[c['key']]['current'], c['short'], c['n_companies'], cards_html)


def render_detail(c, co):
    accent = c['accent']; rgb = c['accent_rgb']; dark = c['accent_dark']
    css = css_for(accent, rgb, dark)
    stats_html = ''.join(
        '<div class="stat-item"><div class="stat-num">%s</div><div class="stat-label">%s</div></div>' % (s[0], s[1])
        for s in co['stats'])
    layers_html = ''.join(
        '<div class="layer-detail"><div class="layer-detail-title"><span class="layer-num">%02d</span>%s</div><div class="layer-detail-body">%s</div></div>' % (i + 1, c['layers'][i]['name'], body)
        for i, body in enumerate(co['layers']))
    info_html = ''.join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (k, v) for k, v in co['info'])
    breadcrumb = '<a href="berkshire-standalone.html">数据中心</a><span class="crumb-sep">/</span><a href="berkshire-%s-chains.html">%s</a><span class="crumb-sep">/</span><span>%s 链</span>' % (c['key'], c['name'], co['name'])
    extra = detail_extra(c, accent)
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="initial-scale=1">
<title>%s 链 · %s</title>
<style>
%s
</style>
</head>
<body>
%s
<div class="container">

<div class="hero">
<div class="hero-title">%s 链</div>
<div class="hero-sub">%s</div>
<span class="region-tag region-tag-mini %s">%s</span>
<div class="hero-stats" style="margin-top:14px">
%s
</div>
</div>

<div class="data-banner">📊 <b>数据口径</b>：财务数据以各公司<b>最新可得年报</b>为准；估值 / 行情为<b>采集日快照</b>（实时行情接口当前环境不可用）。本页为框架级原创整理，<b>不构成投资建议</b>。最后更新：<span class="upd">2026-07-12</span></div>

<div class="section-title">公司 / 主题概述</div>
<div class="overview">
%s
</div>

<div class="section-title">跨层全栈分析（5 层）</div>
%s

<div class="section-title">关键信息一览</div>
<table class="info-table">
%s
</table>

<div class="insight-box">
<div class="insight-title"><span class="icon">🛡️</span> 护城河</div>
<div class="insight-body">%s</div>
</div>

<div class="insight-box">
<div class="insight-title"><span class="icon">⚠️</span> 主要风险</div>
<div class="insight-body">%s</div>
</div>

%s

<div class="back-bar">
<a href="berkshire-%s-chains.html" class="back-btn">← 返回%s</a>
</div>

<div class="source-note">
📌 <b>资料与合规</b>：本页所有分析均基于各公司<b>公开年报、官网、产品发布与新闻</b>等事实层信息，由本站原创整理与重写；不复制、不转载任何付费 / 闭源专享内容。文中对具体公司的判断仅作研究框架示例，<b>不构成投资建议</b>。
</div>

</div>
</body>
</html>''' % (co['name'], c['name'], css, top_bar(accent, c['nav_label'], breadcrumb), co['name'], co['desc'], co['region_cls'], co['region'], stats_html, co['overview'], layers_html, info_html, co['moat'], co['risks'], extra, c['key'], c['name'])


def main():
    for c in CHAINS:
        idx = render_index(c)
        with open(os.path.join(ROOT, 'berkshire-%s-chains.html' % c['key']), 'w', encoding='utf-8') as f:
            f.write(idx)
        for co in c['companies']:
            det = render_detail(c, co)
            with open(os.path.join(ROOT, 'berkshire-%s-chain-%s.html' % (c['key'], co['slug'])), 'w', encoding='utf-8') as f:
                f.write(det)
        print('generated chain:', c['name'], '(%d companies)' % len(c['companies']))


if __name__ == '__main__':
    main()
