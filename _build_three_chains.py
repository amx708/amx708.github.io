# -*- coding: utf-8 -*-
"""生成 中药 / 创新药 / 家电 三条产业链地图（浅色风 + 12链互通导航）。
用法：python _build_three_chains.py
产出直接写入 repo/amx708.github.io/ 对应 HTML。"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.resolve()  # 写入 deploy_site（站点源），再 cp 到 repo/amx708.github.io

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
.extend{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:14px}
.extend a{display:block;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:10px;padding:16px;text-decoration:none;color:#1e293b;transition:.18s;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.extend a:hover{border-color:#__ACC__;box-shadow:0 6px 18px rgba(0,0,0,.1)}
.extend b{color:#__ACC__;display:block;margin-bottom:5px;font-weight:700}
.extend span{font-size:12.5px;color:#64748b;line-height:1.55}
.card-cycle{margin-top:10px;padding:8px 10px;border-left:3px solid #ccc;border-radius:6px;font-size:12px;color:#475569;line-height:1.6}
.card-cycle .cc-label{display:block;font-weight:700;margin-bottom:3px;font-size:11.5px}
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
    return '<span style="display:inline-flex;gap:14px;align-items:center;margin-left:10px">' + ''.join(parts) + '</span>'


def top_bar(accent, current, breadcrumb_html):
    return ('<div class="top-bar">\n'
            '<a href="berkshire-standalone.html" class="home-btn">← 数据中心</a>\n'
            + nav_span(accent, current) + '\n'
            '<div class="breadcrumb">\n' + breadcrumb_html + '\n</div>\n</div>')


def css_for(accent, rgb, dark):
    return CSS.replace('__ACC__', accent).replace('__ACC_RGB__', rgb).replace('__ACC_DARK__', dark)


def extend_reading(c):
    """各链索引页的「延伸阅读」工具导航（横向对比/估值温度计/买点回报图）。"""
    k = c['key']
    items = [
        ('横向对比工具', '勾选多家公司并排比较 PE/PB/ROE/毛利率/负债率/股息率', 'compare'),
        ('估值温度计', '行业内 PB/PE 相对位置，一眼看清谁被低估', 'thermometer'),
        ('逐轮买点回报图', '三轮全市场大底买入并持有的后复权累计回报', 'buyback'),
    ]
    links = ''.join(
        '<a href="berkshire-%s-%s.html"><b>%s</b><span>%s</span></a>' % (k, t, name, desc)
        for name, desc, t in items)
    return '<div class="section-title">延伸阅读</div>\n<div class="extend">%s</div>' % links


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
</ul>
<p><b>举例说明</b>：百济神州的泽布替尼在 ALPINE 等 Ph3 中头对头击败伊布替尼，随后 FDA 获批、海外销售放量，是「管线读出 → 估值重估 → 商业化兑现」的完整案例；康方生物把依沃西单抗（PD-1/VEGF 双抗）授权给 Summit，首付款+里程碑累计达数十亿美元，验证研发价值并带来现金流；国内 PD-1 经过医保谈判从年费几十万降到 4–5 万区间，以价换量后渗透率大幅提升；2022–2023 年美联储高利率时港股 18A 融资困难、估值受压，2024–2025 年降息预期升温后板块估值明显修复。</p>''',
        'current': '创新药无传统产能周期，看"管线读出+BD出海+利率/融资"：当前处出海 BD 大年与港股估值修复期，行业逻辑从融资寒冬转向兑现期，关注重磅数据与安全边际。'
    },
    'appliance': {
        'criteria': '''<p><b>驱动变量</b>：家电是耐用可选消费品，景气周期由四个互相牵制的变量决定——<b>地产</b>、<b>政策补贴</b>、<b>出口</b>、<b>原材料</b>。地产弱时，补贴与存量更新托底；原材料降本时，龙头利润弹性大于小企业；出口强时，外需对冲内需。四者叠加，决定行业是“量价齐升—量升价跌—量缩价稳”中的哪一阶段。</p>
<ul>
<li><b>地产（需求β）</b>：新房竣工与二手房装修是白电、厨电、黑电的β来源。地产上行周期中，新增需求与精装配套拉动放量；地产下行周期中，存量房更新与局部装修成为对冲变量。看家电周期时，地产决定“水位”，而不是单一变量。</li>
<li><b>政策补贴（需求刺激）</b>：以旧换新、节能补贴、消费券是政府对冲地产下行的主要抓手。补贴力度大、覆盖品类广 → 短期刺激更新需求；补贴退坡或财政收紧 → 需求前置后回落。关键观测：补贴延续性、品类扩围（从白电到厨小电）、地方配套力度。</li>
<li><b>出口（外需缓冲）</b>：海外去库存尾声→补库 → 外销回暖；欧美地产销售、利率、海运价格、汇率共同影响出口利润率。新兴市场（东南亚、中东、拉美、非洲）是增量看点，但也面临当地竞争与关税壁垒。</li>
<li><b>原材料（成本端）</b>：铜、铝、钢、塑料是家电主要成本。原材料价格下降 → 毛利率修复；原材料上涨 → 成本传导有滞后，龙头凭借规模与套保能力更能转嫁。原油价格通过塑料成本影响整机。</li>
<li><b>份额集中与高端化（结构性α）</b>：行业β弱时，龙头凭借渠道、品牌、现金流份额逆势提升；高端化（卡萨帝/Colmo/方太集成烹饪中心等）提高均价与利润，是穿越周期的重要α。关键观测：行业CR3/CR5变化、高端品类增速、均价提升幅度。</li>
</ul>
<p><b>周期判断框架</b>：当四个变量中“需求（地产+补贴+出口）”与“成本（原材料）”同向向好时，行业景气上行；当需求与成本反向，行业进入分化阶段，龙头靠α跑赢；当需求与成本双弱，行业进入周期底部，此时出清与份额提升是观察重点。当前我们更关注“结构性α”而非“总量β”。</p>''',
        'current': '家电周期看“地产+补贴+出口+原材料”四角。当前阶段：地产竣工端仍偏弱，但以旧换新与存量更新托底内销；出口保持韧性，海外补库延续、新兴市场贡献增量；铜铝等原材料价格高位震荡，龙头用规模与套保对冲。行业整体处于“β弱但α强”的状态——龙头靠份额集中与高端化穿越周期，结构性机会大于总量机会。当前最值得跟踪：补贴延续性、外销补库节奏、原材料价格拐点、高端化渗透率能否继续提升。'
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
'''

_VALUATION_DATA = None

def _load_valuation_data():
    """懒加载三链估值数据（PE/PB 当前值），失败返回空字典。"""
    try:
        with open(ROOT.parent / '_chain_valuation_data.json', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def valuation_data():
    global _VALUATION_DATA
    if _VALUATION_DATA is None:
        _VALUATION_DATA = _load_valuation_data()
    return _VALUATION_DATA


def fin_snapshot_html(co, c):
    """估值快照：PE/PB 从已采集的分位数据回填；总市值暂无统一真实源，保留占位；股息率按用户要求不再展示。"""
    chain = c['key']
    slug = co['slug']
    data = valuation_data().get(chain, {}).get(slug, {})
    pe = data.get('pe', {})
    pb = data.get('pb', {})
    as_of = data.get('as_of', '—')
    if pe and 'cur' in pe:
        pe_val = f"{pe['cur']:.2f}<span class='fin-note'>（截至 {as_of}）</span>"
    else:
        pe_val = "— 待采集"
    if pb and 'cur' in pb:
        pb_val = f"{pb['cur']:.2f}<span class='fin-note'>（截至 {as_of}）</span>"
    else:
        pb_val = "— 待采集"
    tag = "PE/PB 已采" if (pe and pb) else "待采集"
    return '''
<div class="section-title">估值指标</div>
<div class="fin-block">
  <div class="fin-head"><div class="fin-title"><span class="icon">💰</span> 估值快照</div><span class="fin-tag">%s</span></div>
  <table class="fin-table">
    <tr><td>总市值</td><td class="val">— 待采集</td></tr>
    <tr><td>PE（TTM）</td><td class="val">%s</td></tr>
    <tr><td>PB</td><td class="val">%s</td></tr>
  </table>
</div>''' % (tag, pe_val, pb_val)



def detail_extra(c, co, accent):
    cyc = CYCLE.get(c['key'], {'criteria': '', 'current': ''})
    return FIN_PLACEHOLDER + fin_snapshot_html(co, c) + '''
<div class="section-title">产业周期判断标准（%s）</div>
<div class="cycle-block">
<div class="cycle-title"><span class="icon">🔄</span> 本行业周期怎么看</div>
<div class="cycle-body">%s</div>
<div class="cycle-current">完整判断标准与指标清单见<a href="berkshire-%s-chains.html#cycle" style="color:#%s">《%s》索引页 →</a></div>
</div>''' % (c['name'], cyc['current'], c['key'], accent, c['name'])


# ============ 数据 ============
CHAINS = []


# ---------- 中药 ----------
tcm = {
    'key': 'tcm', 'name': '中药产业链', 'short': '中药龙头', 'icon': '🌿',
    'accent': 'e0533d', 'accent_rgb': '224,83,61', 'accent_dark': '2a1410', 'nav_label': '中药',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 药材与种植', 'desc': '中药材种植 / GAP 基地 / 野生与稀缺资源（麝香、牛黄、驴皮），原料供给与质量是根基'},
        {'n': '02', 'name': '中游 · 炮制与制药', 'desc': '传统炮制工艺 / 保密与专利处方 / 多剂型（丸散膏丹、颗粒、注射），工艺壁垒显著'},
        {'n': '03', 'name': '下游 · 渠道与终端', 'desc': '医院处方 / 零售药店 / 电商 / 连锁，OTC 自我药疗占比高'},
        {'n': '04', 'name': '消费与场景', 'desc': '自我药疗、滋补保健、礼品社交与收藏，兼具「药」与「消费」双重属性'},
        {'n': '05', 'name': '投资逻辑', 'desc': '品牌 / 配方 / 老字号壁垒、消费化能力，风险在集采、医保、原材料与年轻化'},
    ],
    'companies': [
        {'slug': 'yunnanbaiyao', 'name': '云南白药', 'code': '002538', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '中药老字号 + 日化大健康双轮，白药保密配方是核心资产。',
         'stats': [('国家保密', '配方级'), ('牙膏', '市占领先'), ('A股', '中药市值前列')],
         'overview': '云南白药以保密方「云南白药」起家，是中药现代化与消费化的标杆。业务从药品（气雾剂、膏药、宫血宁）延伸到日化大健康（云南白药牙膏长期居国内牙膏市占前列、养元青洗发水、豹七三七），并以「药品 + 健康品 + 中药资源 + 省医药商业」四大板块协同。其护城河在于不可披露的国家保密配方、强品牌与渠道，以及把中药资产「消费化」的能力。',
        'layers': [
            '三七等道地药材，建 GAP 基地与豹七三七品牌，原料自给与质控是成本与品质基础。三七等药材价格波动直接传导至工业成本，自有基地可平抑上游供给与品质风险。',
            '保密配方工艺（散剂、气雾剂、膏贴）不可复制，工业大麻（CBD）曾布局，药品 + 健康品双线生产。配方受国家保密制度保护，构成无法被仿制的工艺壁垒。',
            '医药商业（云南省医药）配送网络 + 连锁药房 + 电商，日化走商超、便利店、抖音 / 天猫。商业板块贡献主要收入体量，渠道广度决定健康品铺货与复购效率。',
            '云南白药牙膏（口腔护理）、止血镇痛（运动 / 家庭药箱）、三七滋补，从「药」到「日常健康消费品」转化。牙膏等高频消费品贡献稳定现金流，弱化了单一药品的周期性。',
            '护城河 = 保密配方 + 品牌 + 大健康渠道，风险 = 主业增长放缓、日化竞争加剧、混改后激励与管理磨合、中药注射剂政策。配方壁垒与全渠道构成深护城河，但健康品赛道竞争与治理磨合是主要波动来源。'],
         'info': [('核心资产', '国家保密配方 · 云南白药'), ('主业板块', '药品 / 健康品 / 中药资源 / 医药商业'),
                  ('代表单品', '白药气雾剂、云南白药牙膏'), ('关键看点', '中药资产消费化 + 混改红利')],
         'moat': '国家保密配方不可披露、不可复制，叠加「白药」国民品牌与全渠道，构成深护城河。',
         'risks': '1）药品主业增长承压；2）日化赛道竞争激烈（牙膏、洗发）；3）混改后治理与激励兑现节奏；4）中药注射剂等监管政策变化。'},
        {'slug': 'pianzaihuang', 'name': '片仔癀', 'code': '600436', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '国家绝密配方 + 天然麝香，稀缺性驱动的「中药茅台」。',
         'stats': [('国家绝密', '处方+工艺'), ('天然麝香', '稀缺原料'), ('特效', '肝胆/消炎')],
         'overview': '片仔癀拥有国家级绝密处方与工艺（全国仅少数），核心成分含天然麝香、天然牛黄、三七、蛇胆，主治消炎、保肝、解毒，民间誉为「中药特效药」。其稀缺性来自原料（天然麝香受配额管制、牛黄昂贵）与配方壁垒，历史上多次提价且需求刚性，兼具医药与礼品 / 收藏属性，被称为「中药里的茅台」。',
        'layers': [
            '天然麝香（林麝养殖 + 配额）、天然牛黄、三七、蛇胆，原料稀缺且受政策配额约束，是成本与产能天花板。麝香与牛黄须凭国家配额获取，供给刚性直接决定可产销量与提价空间。',
            '绝密处方与工艺不可复制，锭剂为核心剂型，同时衍生出胶囊、软膏、化妆品（皇后牌珍珠膏）。配方与工艺同属国家级绝密，竞争对手无法合法仿制。',
            '体验馆 + 经销商 + 自营 + 电商，片仔癀体验馆承担品牌展示与销售，控价体系严格。体验馆既是渠道也是品牌触点，严格控价维护高端价格体系。',
            '保肝护肝、消炎解毒、商务礼品与收藏，高客单价、强复购与社交属性。礼品与收藏需求使消费兼具身份属性，弱化纯医药的疗程性。',
            '护城河 = 绝密配方 + 稀缺原料 + 提价权，风险 = 麝香 / 牛黄供给与价格、提价边际放缓、渠道库存、化妆品跨界投入回报不确定。配方与配额构成极深壁垒，但原料约束与提价边际是核心变量。'],
         'info': [('核心壁垒', '国家级绝密处方与工艺'), ('稀缺原料', '天然麝香、天然牛黄'),
                  ('代表单品', '片仔癀锭剂、珍珠膏'), ('关键逻辑', '稀缺 + 提价权，类消费品属性')],
         'moat': '绝密配方不可复制、天然麝香配额稀缺，提价权与品牌心智共同构成极深护城河。',
         'risks': '1）天然麝香 / 牛黄供给受配额与价格约束；2）持续提价后边际需求放缓；3）渠道库存与价格体系波动；4）日化跨界投入回报不确定。'},
        {'slug': 'tongrentang', 'name': '同仁堂', 'code': '600085', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '300 余年老字号，安宫牛黄丸与心脑血管中成药的金字招牌。',
         'stats': [('350+年', '老字号'), ('安宫牛黄', '核心大单品'), ('同仁堂', '国民品牌')],
         'overview': '同仁堂始创于 1669 年，是中药老字号的代表，品牌即资产。「安宫牛黄丸」是镇店之宝（含天然牛黄、麝香），在心脑血管急救与高端滋补礼赠中地位稳固。业务覆盖中成药工业（同仁堂股份、同仁堂科技、同仁堂国药）与商业零售（同仁堂商业连锁），「炮制虽繁必不敢省人工」的祖训构成质量心智。',
        'layers': [
            '自建与共建药材基地，强调地道药材，部分品种（天然牛黄、麝香）依赖稀缺资源。地道药材产地与年份决定药效与成本，稀缺资源抬高高端品种进入门槛。',
            '严守传统炮制工艺，安宫牛黄丸等手工制作工艺门槛高，工业体系分境内（股份 / 科技）与境外（国药 · 香港）。手工炮制经验积累形成难以速成的质量壁垒。',
            '自有零售药店网络（同仁堂商业）+ 院线 + 电商 + 海外（同仁堂国药国药城），终端掌控力强。自有终端既卖货又强化品牌，海外国药城承接华人需求。',
            '高端滋补与礼赠（安宫牛黄、虫草）、慢病调理、海外华人中药需求。礼赠与慢病属性带来高客单与长周期消费。',
            '护城河 = 百年品牌 + 安宫大单品 + 终端网络，风险 = 增长稳健但偏慢、体制效率、原材料价格、年轻化与消费场景拓展。品牌资产极深，但国企体制与年轻化渗透是主要瓶颈。'],
         'info': [('核心单品', '安宫牛黄丸'), ('品牌年龄', '始创 1669 年'),
                  ('业务结构', '工业 + 商业零售 + 海外'), ('关键看点', '品牌溢价与终端网络')],
         'moat': '350 余年品牌资产 + 安宫牛黄丸大单品 + 自有零售终端，形成难以模仿的中药老字号壁垒。',
         'risks': '1）经营风格稳健但增长偏慢；2）国企体制效率；3）天然牛黄等原料价格；4）年轻消费群体渗透不足。'},
        {'slug': 'dongejiao', 'name': '东阿阿胶', 'code': '000423', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '阿胶品类代名词，从「滋补国宝」到年轻化复兴。',
         'stats': [('阿胶', '品类代表'), ('OTC', '滋补龙头'), ('复兴', '年轻化')],
         'overview': '东阿阿胶是阿胶品类的代表品牌，「滋补国宝」心智深厚，核心产品阿胶块、复方阿胶浆、阿胶糕长期主导阿胶市场。曾因渠道压货与提价过度陷入库存危机，后通过去库存、控价、年轻化（阿胶粉、即食化、线上）实现复兴。其生意本质是「驴皮资源 + 品牌 + 滋补文化」。',
        'layers': [
            '驴皮是核心稀缺资源（国内驴存栏下降），原料供给与价格是成本关键，公司推「毛驴养殖」向上游延伸。驴皮供给长期偏紧，自有养殖可部分平抑成本波动。',
            '阿胶传统熬制工艺 + 标准化生产，复方阿胶浆为 OTC 独家品种。熬制经验与标准化工序共同保障品质一致性，独家品种受保护。',
            '药店（OTC 为主）+ 电商 + 直营，去库存后重建健康价盘与渠道利润。价盘修复是渠道愿意铺货与推荐的前提。',
            '女性滋补、产后 / 气血调理、年节礼赠，即食化拓展日常场景。即食化降低食用门槛，把节令礼品转化为日常高频消费。',
            '护城河 = 阿胶品类心智 + 资源壁垒，风险 = 驴皮供给与成本、滋补需求周期、年轻化成效、竞品（同仁堂 / 福牌）分流。品类心智深，但驴皮约束与竞品分流是核心风险。'],
         'info': [('核心品类', '阿胶'), ('代表产品', '阿胶块、复方阿胶浆、阿胶糕'),
                  ('关键转折', '去库存后复兴'), ('风险点', '驴皮资源约束')],
         'moat': '「东阿阿胶 = 阿胶」的品类心智 + 驴皮资源掌控，构成品类护城河。',
         'risks': '1）驴皮资源稀缺推高成本；2）滋补需求受经济与消费情绪影响；3）年轻化转型成效待验证；4）福牌等竞品分流。'},
        {'slug': 'baiyunshan', 'name': '白云山', 'code': '600332', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '大南药 + 大健康（王老吉）+ 大商业，广州医药集团旗舰。',
         'stats': [('王老吉', '凉茶龙头'), ('大南药', '中成药品种多'), ('广药', '集团旗舰')],
         'overview': '白云山是广州医药集团（广药）的上市旗舰，业务分大南药（中成西药，如板蓝根、复方丹参片、头孢系列）、大健康（王老吉凉茶，曾与加多宝争夺商标）、大商业（医药流通）。品种储备丰富、品牌矩阵广，但收入结构中流通占比大、整体利润率不高，投资更看重品种资产与王老吉复苏。',
        'layers': [
            '中药材 + 化药原料，依托广药集团产业链协同。集团内部资源调配降低采购与协同成本。',
            '中成药（板蓝根颗粒、消渴丸、复方丹参片）+ 化药（头孢、阿莫西林），老字号群（陈李济、奇星等）。多老字号品牌共享渠道与生产，品种储备厚。',
            '医药商业流通（批发）+ 零售（采芝林等）+ 王老吉快消渠道（商超 / 餐饮 / 电商）。流通业务贡献收入体量，快消渠道决定王老吉触达。',
            '凉茶（王老吉）日常饮品、OTC 自我药疗、医院处方。王老吉消费高频，弱化了药品的周期属性。',
            '护城河 = 老字号群 + 王老吉品牌，风险 = 流通业务低毛利、王老吉竞争、化药集采、整合效率。品牌组合厚，但流通低毛利与红海竞争拉低整体盈利。'],
         'info': [('核心品牌', '王老吉'), ('业务结构', '大南药 / 大健康 / 大商业'),
                  ('老字号群', '陈李济、奇星等'), ('关键看点', '王老吉复苏 + 品种资产')],
         'moat': '广药集团背书 + 王老吉国民凉茶品牌 + 众多老字号中成药品种，构成组合壁垒。',
         'risks': '1）医药流通低毛利拉低整体盈利；2）王老吉与加多宝红海竞争；3）化药集采；4）多业务整合效率。'},
        {'slug': 'yiling', 'name': '以岭药业', 'code': '002603', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '络病理论特色的专利中药龙头，连花清瘟打响名气。',
         'stats': [('络病理论', '独家学术体系'), ('连花清瘟', '感冒/流感大单品'), ('专利中药', '研发驱动')],
         'overview': '以岭药业以吴以岭院士「络病理论」为学术根基，走「理论—临床—新药」的专利中药路线。核心产品连花清瘟（感冒 / 流感 / 新冠相关）为其打响全国知名度，此外在心脑血管（通心络、参松养心、芪苈强心）也有专利大品种。研发驱动特征明显，但单品依赖与医保 / 集采是关注点。',
        'layers': [
            '中药材采购与基地，连花清瘟涉及金银花、连翘等多味药材，原料价格波动影响成本。多味药材组合使成本对单一品种价格不敏感，但整体受药市周期影响。',
            '专利中药工艺，围绕络病理论形成心脑血管 + 呼吸 + 神经多管线，连花清瘟为代表性大单品。络病理论支撑学术推广与医生认知，形成差异化壁垒。',
            '医院（处方）+ 零售药店（OTC）+ 电商，疫情后渠道铺货广。全渠道覆盖使大单品在流感季快速放量。',
            '感冒流感自我药疗、心脑血管慢病长期用药、家庭常备药箱。OTC 与慢病双属性带来即期与长期需求叠加。',
            '护城河 = 络病理论学术壁垒 + 专利品种，风险 = 连花清瘟需求回落、单品集中、医保谈判与集采、研发转化不确定性。学术与专利构成壁垒，但单品依赖与集采是主要风险。'],
         'info': [('学术根基', '络病理论'), ('代表产品', '连花清瘟、通心络'),
                  ('属性', '专利中药研发型'), ('关键风险', '单品依赖 + 集采')],
         'moat': '独有络病理论学术体系 + 多项专利中药大品种，形成差异化研发壁垒。',
         'risks': '1）连花清瘟需求随疫情退潮回落；2）核心单品收入集中；3）医保谈判与中成药集采；4）新药研发转化不确定。'},
        {'slug': 'huaren_sanjio', 'name': '华润三九', 'code': '000999', 'region': '中国', 'region_cls': 'region-cn',
         'desc': 'OTC 与配方颗粒龙头，CHC 自我诊疗 + 处方药双轮。',
         'stats': [('999', '国民OTC品牌'), ('配方颗粒', '行业领先'), ('华润', '央企背景')],
         'overview': '华润三九是华润系医药工业平台，定位「自我诊疗（CHC）+ 处方药（RX）」。CHC 端拥有「999」国民品牌（感冒灵、皮炎平、胃泰、正天丸等），渠道与品牌力极强；RX 端在中药注射剂、配方颗粒（昆药 / 天江等布局）有优势。央企背景带来资源与并购整合能力。',
        'layers': [
            '中药材与配方颗粒原料，推进标准化基地，华润系整合上游资源。标准化基地保障配方颗粒质量与供应稳定。',
            'CHC 多品种 OTC 生产线 + 处方药（中药注射、配方颗粒），并购（如昆药集团）扩充品种。并购是快速补齐管线与渠道的主要手段。',
            '零售药店（OTC 强势）+ 医院（处方）+ 基层 + 电商，「999」品牌自带流量。品牌认知降低终端陈列与推荐门槛。',
            '感冒、皮肤、肠胃等自我药疗，配方颗粒中医诊疗，家庭常备。多品类高频消费支撑品牌复购。',
            '护城河 = 999 品牌 + 渠道 + 央企并购，风险 = OTC 竞争、中药注射剂政策、集采、并购整合。品牌与渠道深，但注射剂政策与整合是变量。'],
         'info': [('核心品牌', '999'), ('业务', 'CHC 自我诊疗 + RX 处方'),
                  ('代表', '感冒灵、配方颗粒'), ('关键看点', '品牌 OTC + 并购整合')],
         'moat': '「999」国民 OTC 品牌 + 全渠道覆盖 + 华润央企并购平台，构成品牌与规模壁垒。',
         'risks': '1）OTC 赛道竞争白热化；2）中药注射剂监管政策；3）集采扩围；4）并购后整合风险。'},
        {'slug': 'buchang', 'name': '步长制药', 'code': '603858', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '心脑血管中成药大户，脑心通等专利品种见长。',
         'stats': [('脑心通', '心脑血管大单品'), ('专利中药', '品种储备'), ('OTC/RX', '双渠道')],
         'overview': '步长制药以心脑血管中成药为核心，代表品种脑心通胶囊、稳心颗粒、丹红注射液等，在院线与 OTC 均有布局。销售网络以学术推广见长。关注点在于中药注射剂（丹红）的政策压力、销售费用率偏高与产品迭代。',
        'layers': [
            '中药材采购，注射剂对原料与质控要求高。注射剂质控标准严，原料稳定性直接影响安全与批签发。',
            '心脑血管专利中成药品种群，含口服 + 注射剂型，丹红注射液为代表性注射品种。口服与注射组合覆盖院内外场景。',
            '医院（处方 / 学术推广）+ 零售，销售队伍庞大。学术推广网络是处方放量的核心抓手。',
            '心脑血管慢病长期用药，中老年群体为主。慢病长期用药带来持续复购。',
            '护城河 = 心脑血管品种群 + 学术网络，风险 = 中药注射剂政策、销售费用、单品依赖、集采。品种群与渠道构成壁垒，但注射剂政策与费用是主要风险。'],
         'info': [('核心品类', '心脑血管中成药'), ('代表', '脑心通、丹红注射液'),
                  ('销售', '学术推广网络'), ('关键风险', '注射剂政策 + 费用')],
         'moat': '心脑血管专利品种群 + 强学术推广网络，构成专科用药壁垒。',
         'risks': '1）中药注射剂（丹红）监管与医保限制；2）销售费用率偏高；3）核心品种增长乏力；4）集采。'},
        {'slug': 'jichuan', 'name': '济川药业', 'code': '600566', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '儿科与呼吸中成药特色，蒲地蓝消炎口碑品种。',
         'stats': [('蒲地蓝', '消炎口服大单品'), ('儿科', '特色赛道'), ('高分红', '现金流好')],
         'overview': '济川药业以儿科、呼吸、消化中成药为特色，蒲地蓝消炎口服液、小儿豉翘清热颗粒为代表性品种，在儿科与院边药房口碑强。公司经营稳健、现金流好、分红率高，被视为「现金牛」型中药企业，但存在大单品依赖与管线拓展的课题。',
        'layers': [
            '中药材采购与基地，儿科品种对安全性与口感要求高。儿科用药更重口感与依从性，配方调整空间有限。',
            '口服液、颗粒等剂型，蒲地蓝消炎 + 小儿豉翘为核心，生产标准化。核心品种工艺成熟，标准化保障一致性。',
            '医院（儿科 / 呼吸科）+ 零售药房 + 电商，院边与 OTC 并重。院边药房承接处方外流，OTC 覆盖日常需求。',
            '儿童感冒发热、咽喉消炎、家庭儿科常备。儿科常备属性带来高复购与口碑粘性。',
            '护城河 = 儿科口碑品种 + 渠道，风险 = 大单品依赖、儿科集采、增长天花板、管线拓展。儿科口碑深，但单品依赖与集采是核心变量。'],
         'info': [('核心品种', '蒲地蓝消炎、小儿豉翘'), ('特色', '儿科 / 呼吸'),
                  ('财务', '高分红现金流优'), ('关键风险', '单品依赖')],
         'moat': '儿科与呼吸口碑品种 + 院边与零售渠道，构成特色专科壁垒。',
         'risks': '1）蒲地蓝等大单品依赖；2）儿科 / 呼吸品种集采可能；3）增长天花板；4）新品管线接续。'},
        {'slug': 'lingrui', 'name': '羚锐制药', 'code': '600285', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '贴膏剂细分龙头，OTC 膏药「隐形冠军」。',
         'stats': [('贴膏剂', '细分龙头'), ('OTC', '膏药强势'), ('高分红', '稳健现金牛')],
         'overview': '羚锐制药是贴膏剂（外用透皮）细分龙头，核心品牌「羚锐牌」膏药（壮骨麝香止痛膏、通络祛痛膏、活血消痛酊等）在 OTC 膏药市场占据领先份额。生意模式轻、现金流好、分红稳定，属「小而美」的中药外用专科企业，受集采影响相对小于处方药。',
        'layers': [
            '中药材 + 透皮基质材料，贴膏对工艺与透气性要求高。透皮吸收效率取决于基质与工艺，构成技术门槛。',
            '橡胶膏、凝胶膏等贴膏剂型工艺成熟，OTC 贴膏为主，部分为处方。OTC 为主使终端可自由购买，复购便捷。',
            '零售药店（OTC 主力）+ 基层医疗 + 电商，贴膏复购属性强。高频复购降低获客成本。',
            '风湿骨痛、跌打损伤、颈肩腰腿痛的日常自我理疗。慢性疼痛管理带来长期消费。',
            '护城河 = 贴膏品牌 + 渠道 + 工艺，风险 = 贴膏竞争、提价空间有限、品种单一、原材料。细分品牌与工艺深，但品类单一与价格是约束。'],
         'info': [('核心品类', '外用贴膏剂'), ('代表', '壮骨麝香止痛膏'),
                  ('属性', 'OTC 细分龙头'), ('关键看点', '稳健分红 + 轻资产')],
         'moat': '贴膏剂细分龙头品牌 + OTC 渠道 + 透皮工艺，构成小而美壁垒。',
         'risks': '1）贴膏赛道参与者多；2）单价低、提价空间有限；3）品种结构偏单一；4）药材与基质成本。'},
        {'slug': 'jiangzhong', 'name': '江中药业', 'code': '600750', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '胃肠 OTC 龙头，健胃消食片家喻户晓。',
         'stats': [('健胃消食片', '国民单品'), ('OTC', '胃肠赛道'), ('华润', '央企赋能')],
         'overview': '江中药业以胃肠 OTC 见长，健胃消食片、乳酸菌素片、江中草珊瑚含片等为家喻户晓的品种，属「大消费」属性强的中药企业。后被华润收购，借助华润渠道与资源，向「家中常备药」平台化延伸。品牌即流量，但增长依赖大单品与品类拓展。',
        'layers': [
            '中药材与益生菌等原料，健胃消食片以山楂、麦芽等消食类药材为主。消食类药材来源广，成本相对可控。',
            'OTC 片剂 / 颗粒工艺成熟，健胃消食片为核心大单品，生产标准化。单品规模效应摊薄制造成本。',
            '零售药店（OTC 主力）+ 商超 + 电商，「家中常备」场景强。商超与电商拓宽了非药房消费场景。',
            '消化不良、肠胃调理、咽喉含片，家庭日常自我药疗。高频轻症消费带来稳定复购。',
            '护城河 = 国民品牌 + 渠道，风险 = 大单品依赖、OTC 竞争、品类拓展、华润整合节奏。品牌即流量，但单品依赖与拓展是变量。'],
         'info': [('核心单品', '健胃消食片'), ('特色', '胃肠 OTC'),
                  ('背景', '华润系'), ('关键看点', '品牌 OTC + 平台化')],
         'moat': '健胃消食片等国民 OTC 品牌 + 全渠道，构成消费型中药壁垒。',
         'risks': '1）健胃消食片等大单品依赖；2）OTC 竞争激烈；3）品类拓展成效；4）华润整合与激励节奏。'},
    ],
}
CHAINS.append(tcm)


# ---------- 创新药 ----------
innov = {
    'key': 'innov', 'name': '创新药产业链', 'short': '创新药企', 'icon': '💊',
    'accent': 'ec4899', 'accent_rgb': '236,72,153', 'accent_dark': '2a1020', 'nav_label': '创新药',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 研发与 CRO/CDMO', 'desc': '靶点发现 / 临床前 / 工艺开发，依赖 CRO 与 CDMO 外包生态'},
        {'n': '02', 'name': '中游 · 生产与工艺', 'desc': '生物药（单抗 / 双抗 / ADC）与小分子合成，质量体系接轨国际'},
        {'n': '03', 'name': '下游 · 商业化与出海', 'desc': '医保谈判 / 医院准入 / 海外授权（BD），出海是估值核心变量'},
        {'n': '04', 'name': '消费与场景', 'desc': '肿瘤 / 自免 / 慢病的高未满足临床需求，患者基数决定空间'},
        {'n': '05', 'name': '投资逻辑', 'desc': '管线价值 / 出海 BD / 医保集采，研发失败与商业化是主要风险'},
    ],
    'framework_story': '''<div class="section-title">人话版：这个框架怎么用</div>
<div class="insight-box">
<div class="insight-title"><span class="icon">💡</span> 一句话：创新药不是看谁药多，而是看「管线能不能跑通、卖爆、出海」</div>
<div class="insight-body">
<p>创新药没有家电、化工那样清晰的「原料→工厂→渠道」价格传导。它的核心是<strong>研发周期</strong>：从靶点发现、临床验证、获批上市到进医保放量，每个阶段估值逻辑都不一样。</p>
<p>5 层框架其实是回答三个问题：</p>
<ul>
<li><b>上游：公司有没有真本事搞研发？</b> 靶点选得准、临床设计强、CRO/CDMO 资源足，研发效率才高。比如百济神州的泽布替尼自己做全球 Ph3，就是上游研发能力强的体现。</li>
<li><b>中游：生产靠不靠谱？</b> 生物药工艺复杂，一致性、产能、质量体系决定商业化后能不能稳定供货。恒瑞从仿制车间转向创新药 GMP 生物药基地，是这一层的关键。</li>
<li><b>下游：能不能卖进医院、进医保、出海？</b> 这是估值最大变量。信达生物把 PD-1 授权给礼来，康方生物把双抗授权给 Summit，都属于「下游出海」提前兑现。</li>
<li><b>场景：病足够大、患者付得起、竞品少吗？</b> 肿瘤、自免、慢病是大市场；罕见病市场小但定价高。恒瑞的 HER2、ADC 管线主要押注乳腺癌/胃癌等大瘤种。</li>
<li><b>投资逻辑：管线值多少钱、风险在哪？</b> Biotech 可能一个药决定生死；大药企（恒瑞）看管线组合厚度。管线价值 ≈ 峰值销售额 × 成功概率 × 折现。</li>
</ul>
<p><b>实战信号</b>：临床数据阳性 → 估值重估；重磅 BD 交易 → 现金流改善 + 国际验证；医保谈判降幅超预期 → 以价换量；海外利率下行 → 港股 18A 估值修复。当前行业处于「出海 BD 大年 + 融资回暖」的兑现期，安全边际比故事更重要。</p>
</div>
</div>''',
    'companies': [
        {'slug': 'hengrui', 'name': '恒瑞医药', 'code': '600276', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '国产创新药一哥，从仿制到创新的转型标杆。',
         'stats': [('创新药', '收入占比过半'), ('管线', '肿瘤+自免广'), ('出海', '授权加速')],
         'overview': '恒瑞医药是中国创新药龙头，早年以仿制药（抗肿瘤、麻醉、造影）起家，近年完成「仿转创」转型，创新药收入已成主力。管线覆盖肿瘤（PD-1 卡瑞利珠单抗、HER2 ADC）、自免、代谢等多领域，并加速对外授权（BD）与国际化。其优势是研发体量、销售网络与丰富的在研管线；挑战是医保谈判降价与同质化竞争。',
        'layers': [
            '自建大规模研发体系 + 临床前 / CRO 合作，靶点覆盖广，研发投入行业领先。自研体系保证管线厚度，CRO 提速临床。',
            '小分子化药 + 生物药（单抗 / ADC）生产工艺，GMP 体系完善，产能持续扩张。国际接轨的质量体系是出海与授权的前提。',
            '自建肿瘤 / 综合销售铁军 + 医保谈判准入 + 海外授权（如与默沙东等合作），海外市场逐步打开。销售网络支撑医保放量，BD 打开海外估值。',
            '肿瘤（多癌种）、自免、麻醉镇痛、代谢慢病的高未满足需求。大适应症人群广，需求刚性支撑长期空间。',
            '护城河 = 研发体量 + 管线广度 + 销售网络，风险 = 医保降价、PD-1 内卷、出海兑现、研发失败。规模与管线构成壁垒，但医保内卷与兑现是风险。'],
         'info': [('定位', '国产创新药一哥'), ('代表', '卡瑞利珠单抗、ADC'),
                  ('模式', '自研 + BD 出海'), ('关键风险', '医保内卷 + 出海')],
         'moat': '国内最大研发管线之一 + 成熟商业化网络 + 持续 BD，构成创新药规模壁垒。',
         'risks': '1）医保谈判持续降价；2）PD-1 等靶点同质化内卷；3）海外授权里程碑兑现不确定；4）临床失败风险。'},
        {'slug': 'beigene', 'name': '百济神州', 'code': '688235', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '全球化标杆，泽布替尼（BTK）出海成功范例。',
         'stats': [('泽布替尼', '全球BTK重磅'), ('三地上市', '美股/港股/科创板'), ('全球化', '研发销售并重')],
         'overview': '百济神州是中国创新药全球化的代表，核心产品泽布替尼（BTK 抑制剂）在全球多国获批并成为重磅药物，证明中国原研可在欧美主流市场与跨国药企正面竞争。公司研发与商业化高度全球化（中美欧多中心），管线覆盖肿瘤（BCL-2、TIGIT 等）。特点是「烧钱换全球卡位」，盈利拐点与现金流是核心观察点。',
        'layers': [
            '全球多中心研发网络，自研为主 + 外部合作，BTK、BCL-2、PD-1 等多管线。中美欧同步临床加速海外获批。',
            '生物药与小分子自主生产 + CDMO 协作，全球供应链布局。自主产能保障供应，CDMO 补峰。',
            '自建全球肿瘤销售团队（美 / 欧 / 中），泽布替尼在欧美放量，适应症持续拓展。自营团队掌握定价与放量节奏。',
            '血液瘤（CLL/SLL、MCL 等）、实体瘤的高价值未满足需求。高价值适应症支付能力强。',
            '护城河 = 全球临床能力 + 泽布替尼标杆，风险 = 持续高研发投入、盈利兑现、竞争（阿卡替尼等）、地缘政治。全球化能力稀缺，但烧钱与地缘是核心变量。'],
         'info': [('标杆产品', '泽布替尼'), ('上市', '美股/港股/科创板'),
                  ('定位', '全球化创新药'), ('关键看点', '盈利拐点 + 出海')],
         'moat': '全球多中心研发与商业化能力 + 泽布替尼验证的海外放量，构成稀缺全球化壁垒。',
         'risks': '1）长期高额研发投入致盈利延迟；2）BTK 赛道竞争（阿卡替尼、pirtobrutinib）；3）地缘与出海政策；4）管线临床挫折。'},
        {'slug': 'innovent', 'name': '信达生物', 'code': '01801.HK', 'region': '中国香港', 'region_cls': 'region-hk',
         'desc': 'PD-1 头部 + 国际合作（礼来），平台型 biotech。',
         'stats': [('信迪利单抗', 'PD-1头部'), ('礼来', '深度合作'), ('平台', '多管线')],
         'overview': '信达生物是平台型创新药企，核心产品信迪利单抗（PD-1）国内领先，并与礼来（Eli Lilly）深度合作引入资金与海外权益。管线覆盖肿瘤、自免、代谢（GLP-1 等），并通过 license-in/out 构建组合。优势是国际化合作基因与量产能力；挑战是 PD-1 内卷与商业化盈利。',
        'layers': [
            '自建研发 + 外部引进（license-in）双轮，苏州基地为核心。引进提速管线，自研沉淀平台。',
            '大规模生物药产能（苏州基地），单抗 / 双抗生产工艺成熟。自有产能支撑商业化与出海供货。',
            '自建销售 + 礼来等合作出海，医保准入与医院覆盖。合作方分担海外开发与风险。',
            '肿瘤免疫、自免、代谢（减肥 / 糖尿病 GLP-1）需求。GLP-1 等热门赛道空间大但竞争也大。',
            '护城河 = 平台 + 国际合作 + 产能，风险 = PD-1 内卷、盈利、合作条款、研发。平台与产能厚，但内卷与盈利是瓶颈。'],
         'info': [('核心', '信迪利单抗PD-1'), ('合作', '礼来'),
                  ('管线', '肿瘤/自免/代谢'), ('关键风险', 'PD-1内卷+盈利')],
         'moat': '平台化管线 + 礼来级国际合作 + 自建产能，构成 biotech 平台壁垒。',
         'risks': '1）PD-1 同质化竞争；2）持续亏损与盈利节奏；3）合作方条款与分成；4）临床与监管风险。'},
        {'slug': 'junshi', 'name': '君实生物', 'code': '688180', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '特瑞普利单抗（PD-1）出海先行者。',
         'stats': [('特瑞普利', 'PD-1出海'), ('中和抗体', '新冠期间放量'), ('肿瘤免疫', '主线')],
         'overview': '君实生物以特瑞普利单抗（PD-1，国产首个获批 PD-1）为核心，并通过与 Coherus 等合作推动美国等海外获批，是 PD-1 出海先行者。新冠期间中和抗体（埃特司韦单抗）曾带来阶段放量。管线聚焦肿瘤免疫 + 自免 + 新冠相关。特点是研发有亮点但商业化与盈利承压。',
        'layers': [
            '自研为主，PD-1、BTLA、新冠中和抗体等多管线，临床前合作。自研保留核心权益，合作补能力。',
            '生物药自主生产 + CDMO，产能扩建中。产能扩充匹配放量与出海需求。',
            '国内自建销售 + 海外授权（Coherus 等），美国获批提振出海预期。授权换海外准入与现金流。',
            '黑色素瘤 / 鼻咽癌等肿瘤、自免、抗感染。差异化适应症避开最红海竞争。',
            '护城河 = PD-1 先发 + 出海，风险 = 商业化弱、盈利、竞争、疫情后需求退潮。先发出海是亮点，但商业化与盈利偏弱。'],
         'info': [('核心', '特瑞普利单抗'), ('出海', '美国获批'),
                  ('属性', '肿瘤免疫biotech'), ('关键风险', '盈利+竞争')],
         'moat': '国产首个 PD-1 先发 + 海外授权落地，构成肿瘤免疫出海壁垒。',
         'risks': '1）国内销售与盈利承压；2）PD-1 竞争；3）新冠相关收入退潮；4）研发高投入。'},
        {'slug': 'henlius', 'name': '复宏汉霖', 'code': '02696.HK', 'region': '中国香港', 'region_cls': 'region-hk',
         'desc': '生物类似药标杆，汉曲优（曲妥珠）全球化放量。',
         'stats': [('汉曲优', '曲妥珠生物类似药'), ('生物类似药', '出海标杆'), ('复星', '体系赋能')],
         'overview': '复宏汉霖是生物类似药（biosimilar）龙头，核心产品汉曲优（曲妥珠单抗生物类似药）在中欧等多国获批并放量，验证了中国生物药全球竞争力。管线从类似药（利妥昔、贝伐珠等）向创新药（PD-1、ADC）延伸，背靠复星医药体系。特点是「类似药现金流养创新」。',
        'layers': [
            '生物类似药成熟经验 + 创新药（PD-1、ADC）拓展，徐汇 / 松江基地。类似药现金流养创新。',
            '大规模单抗生物药产能，质量体系接轨国际（EMA/FDA）。国际质量体系是出海放行前提。',
            '国内 + 海外（欧洲 / 拉美等）授权与自营，汉曲优全球销售。海外授权扩大可及市场。',
            '乳腺癌（HER2）、淋巴瘤等肿瘤治疗。HER2 人群大且支付成熟。',
            '护城河 = 类似药产能 + 出海，风险 = 类似药降价、创新兑现、复星整合、盈利。产能与出海强，但类似药降价是压力。'],
         'info': [('标杆', '汉曲优'), ('定位', '生物类似药龙头'),
                  ('背景', '复星医药'), ('关键看点', '类似药现金流+创新')],
         'moat': '国际质量体系的生物药产能 + 汉曲优全球放量，构成类似药出海壁垒。',
         'risks': '1）生物类似药价格下行；2）创新药兑现慢；3）复星体系协同与债务；4）持续盈利。'},
        {'slug': 'akesobio', 'name': '康方生物', 'code': '09926.HK', 'region': '中国香港', 'region_cls': 'region-hk',
         'desc': '双抗平台明星，卡度尼利（PD-1/CTLA-4）破圈。',
         'stats': [('双抗', '平台特色'), ('卡度尼利', 'PD-1/CTLA-4'), ('依沃西', '授权Summit')],
         'overview': '康方生物以「双特异性抗体」平台为特色，核心产品卡度尼利（PD-1/CTLA-4 双抗）在宫颈癌等获批，依沃西（PD-1/VEGF 双抗）以高额授权（与 Summit 合作，数十亿美元级）成为国产创新药出海标志性交易。平台型 biotech 中临床与 BD 双强，估值弹性大但研发风险亦高。',
        'layers': [
            '自研双抗平台（Tetrabody），卡度尼利、依沃西等，靶点组合创新。平台决定可持续产出双抗分子。',
            '生物药自主生产 + CDMO，产能支撑商业化。产能匹配授权方供货需求。',
            '国内自建 + 海外授权（Summit 主导依沃西海外），里程碑 + 销售分成。授权换取大额里程碑与海外开发。',
            '宫颈癌、肺癌等肿瘤的高未满足需求。大癌种需求刚性且支付高。',
            '护城河 = 双抗平台 + BD 能力，风险 = 临床失败、授权兑现、竞争、盈利。平台与 BD 双强，但临床与兑现是风险。'],
         'info': [('平台', '双抗Tetrabody'), ('代表', '卡度尼利、依沃西'),
                  ('出海', 'Summit授权'), ('关键风险', '临床+兑现')],
         'moat': '自研双抗技术平台 + 标志性海外授权，构成差异化创新壁垒。',
         'risks': '1）双抗临床与安全性风险；2）海外授权里程碑兑现；3）肿瘤竞争；4）盈利周期长。'},
        {'slug': 'remgen', 'name': '荣昌生物', 'code': '688331', 'region': '中国', 'region_cls': 'region-cn',
         'desc': 'ADC 先锋，维迪西妥（HER2 ADC）授权 Seagen。',
         'stats': [('维迪西妥', 'HER2 ADC'), ('Seagen', '海外授权'), ('自免+肿瘤', '双线')],
         'overview': '荣昌生物是 ADC（抗体偶联药物）先锋，核心产品维迪西妥单抗（HER2 ADC）在国内获批胃癌 / 尿路上皮癌等，并以高价授权给 Seagen（后被辉瑞收购），是国产 ADC 出海早期范例。另在自免（泰它西普，BLyS/APRIL 双靶点）有布局。技术平台（ADC + 融合蛋白）是其核心资产。',
        'layers': [
            '自研 ADC 平台（桥接技术）+ 融合蛋白（泰它西普），靶点创新。桥接技术决定 ADC 稳定性与疗效。',
            '生物药与 ADC 自主生产，ADC 工艺复杂度高。ADC 偶联工艺门槛高，护城河在平台。',
            '国内自建 + 海外授权（Seagen/辉瑞），医保准入推进。授权打开海外，医保扩国内可及。',
            'HER2+ 胃癌 / 尿路上皮癌、自免（红斑狼疮等）。差异化适应症与自免双线布局。',
            '护城河 = ADC 平台 + 双靶点，风险 = ADC 竞争、授权兑现、盈利、研发。ADC 平台稀缺，但赛道拥挤与兑现是风险。'],
         'info': [('核心', '维迪西妥单抗ADC'), ('出海', '授权Seagen/辉瑞'),
                  ('自免', '泰它西普'), ('关键风险', 'ADC内卷+兑现')],
         'moat': '自研 ADC 偶联平台 + 双靶点融合蛋白，构成技术型创新壁垒。',
         'risks': '1）ADC 赛道快速拥挤；2）海外授权里程碑兑现；3）持续亏损；4）临床挫折。'},
        {'slug': 'zai-lab', 'name': '再鼎医药', 'code': '09688.HK', 'region': '中国香港', 'region_cls': 'region-hk',
         'desc': 'license-in 模式代表，引进全球好药中国落地。',
         'stats': [('引进模式', 'license-in'), ('多款', '已商业化'), ('全球', '合作网络')],
         'overview': '再鼎医药以「引进（license-in）+ 本土商业化」模式著称，将海外（如 Paratek、Turning Point、Novocure）优质创新药引入中国并负责开发上市，已商业化多款肿瘤 / 抗感染 / 电场疗法产品。优势是选品与注册能力；挑战是依赖外部管线、授权成本与盈利。',
        'layers': [
            '以外部引进为主，内部小规模研发，全球合作网络广。选品眼光决定管线质量。',
            '依赖 CDMO 与外部生产，本土化产能逐步建设。CDMO 降资本开支，本土化补短板。',
            '自建肿瘤 / 专科销售团队，国内注册与医保准入能力强。注册与商业化能力是引进模式的变现关键。',
            '肿瘤（肺癌、胃肠间质瘤等）、抗感染、脑胶质瘤电场疗法。差异化疗法填补空白适应症。',
            '护城河 = 选品 + 注册商业化，风险 = 授权成本、依赖外部、谈判、盈利。选品与商业化强，但外部依赖与成本高。'],
         'info': [('模式', 'license-in引进'), ('代表', '尼拉帕利、Optune'),
                  ('能力', '注册+商业化'), ('关键风险', '外部依赖')],
         'moat': '全球选品眼光 + 中国注册与商业化能力，构成引进型壁垒。',
         'risks': '1）高度依赖外部管线授权；2）授权与分成成本高；3）单品竞争；4）盈利周期。'},
        {'slug': 'innocare', 'name': '诺诚健华', 'code': '688428', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '血液瘤小分子特色，奥布替尼（BTK）核心。',
         'stats': [('奥布替尼', 'BTK抑制剂'), ('血液瘤', '特色'), ('创始', '知名团队')],
         'overview': '诺诚健华聚焦血液瘤与自身免疫的小分子创新药，核心产品奥布替尼（BTK 抑制剂）用于淋巴瘤等，并由知名科学家（施一公 / 崔霁松）团队创立，研发基因强。管线向自免（MS、SLE）延伸。特点是「小而精」的靶向外延，关注出海与适应症拓展。',
        'layers': [
            '自研小分子平台，BTK、TYK2 等靶点，创始团队学术背景强。团队决定靶点与分子质量。',
            '小分子化药自主 / 合作生产，工艺成熟。化药工艺成熟，成本可控。',
            '国内自建血液瘤销售 + 海外授权探索，医保准入。自建团队深耕血液瘤科室。',
            '淋巴瘤 / 白血病（血液瘤）、自免（多发性硬化、红斑狼疮）。血液瘤与自免双线延展空间。',
            '护城河 = 靶点能力 + 团队，风险 = BTK 竞争、适应症、盈利、研发。专精靶点能力强，但 BTK 内卷是风险。'],
         'info': [('核心', '奥布替尼BTK'), ('领域', '血液瘤+自免'),
                  ('背景', '科学家创立'), ('关键风险', 'BTK内卷')],
         'moat': '小分子靶向研发能力 + 顶尖创始团队，构成专精型创新壁垒。',
         'risks': '1）BTK 赛道竞争（百济、阿斯利康）；2）适应症拓展不及预期；3）盈利周期；4）临床失败。'},
        {'slug': 'betta', 'name': '贝达药业', 'code': '300558', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '国产小分子靶向药先驱，埃克替尼（EGFR-TKI）开篇。',
         'stats': [('埃克替尼', '国产EGFR-TKI先河'), ('肺癌', '靶向特色'), ('研发', '持续迭代')],
         'overview': '贝达药业以埃克替尼（国产首个小分子靶向抗癌药，EGFR-TKI）开篇，是中国肺癌靶向治疗的开拓者。后续有恩沙替尼（ALK）、贝福替尼（三代 EGFR）等迭代产品，形成肺癌靶向管线。优势是肺癌深耕与商业化；挑战是 TKI 迭代竞争与集采 / 医保降价。',
        'layers': [
            '自研小分子 TKI 平台，EGFR/ALK 等多代际产品，持续迭代。代际迭代延续专利与生命周期。',
            '小分子化药自主生产，工艺成熟可控。自主产能保障供应与毛利。',
            '肿瘤科医生网络 + 医保准入，肺癌专科医院渗透。医生网络是靶向药处方关键。',
            '非小细胞肺癌（EGFR/ALK 突变）靶向治疗。突变人群精准，检测驱动用药。',
            '护城河 = 肺癌靶向深耕，风险 = TKI 迭代竞争、医保降价、单品依赖。肺癌深耕深，但 TKI 内卷与降价是风险。'],
         'info': [('开篇', '埃克替尼'), ('领域', '肺癌靶向'),
                  ('迭代', '恩沙/贝福替尼'), ('关键风险', 'TKI内卷')],
         'moat': '肺癌靶向药先发 + 持续代际迭代，构成专科靶向壁垒。',
         'risks': '1）TKI 多代际同质竞争；2）医保谈判降价；3）核心单品依赖；4）研发兑现。'},
        {'slug': 'kelun', 'name': '科伦药业', 'code': '002422', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '大输液龙头转身创新药（科伦博泰 ADC）。',
         'stats': [('大输液', '行业龙头'), ('科伦博泰', 'ADC新锐'), ('默沙东', '授权出海')],
         'overview': '科伦药业起家于大输液（行业龙头），近年通过子公司科伦博泰切入创新药，尤其在 ADC 领域快速崛起，多个 ADC 分子授权给默沙东（数十亿美元级），成为「传统药企转型创新」的代表。业务呈「仿制药 / 输液现金流 + 创新药期权」结构。',
        'layers': [
            '科伦博泰自研 ADC 平台，多靶点（TROP2、CLDN18.2 等），传统业务研发稳定。ADC 平台是创新估值核心。',
            '大输液规模化生产 + 生物药 / ADC 产能，产业链完整。输液现金流反哺创新产能。',
            '输液 / 仿制药成熟渠道 + 创新药海外授权（默沙东主导）。传统渠道稳，授权开海外。',
            '肿瘤（ADC）、抗生素、输液治疗。输液基本盘提供稳定现金流。',
            '护城河 = 输液规模 + ADC 平台 + 默沙东合作，风险 = 输液集采、创新兑现、授权条款。规模与创新双轮，但集采与兑现是变量。'],
         'info': [('主业', '大输液龙头'), ('创新', '科伦博泰ADC'),
                  ('出海', '默沙东授权'), ('关键看点', '转型创新+现金流')],
         'moat': '输液规模壁垒 + 科伦博泰 ADC 平台 + 默沙东级授权，构成转型创新壁垒。',
         'risks': '1）大输液与仿制药集采；2）ADC 临床与授权兑现；3）创新药投入回报周期；4）整合风险。'},
    ],
}
CHAINS.append(innov)

# ---------- 创新药「公司级」周期定位（按 slug 查表，仅 innov 链渲染） ----------
INNOV_CYCLE = {
    'hengrui': '当前处于创新药收入兑现 + BD 出海加速期：卡瑞利珠、ADC 等管线持续读出，海外授权（如与默沙东等）把研发价值提前变现；医保谈判常态化降价是主要变量，估值从「仿制现金牛」转向「创新 + 出海」双轮。',
    'beigene': '当前处于全球放量 + 盈利拐点观察期：泽布替尼在欧美持续放量、适应症不断拓展，估值由「烧钱换卡位」转向「销售兑现金字塔」；BTK 竞争与地缘政治是核心变量，海外利率下行利好其港股 / 科创板估值修复。',
    'innovent': '当前处于平台化管线 + 国际化合作深化期：信迪利单抗国内承压但 GLP-1、自免管线接力，与礼来合作持续兑现；PD-1 内卷与盈利节奏是主要变量，海外利率下行利好其港股估值修复。',
    'junshi': '当前处于出海先行 + 商业化兑现期：特瑞普利单抗美国获批打开海外空间，但国内销售与盈利仍承压；PD-1 竞争与新冠相关收入退潮是风险，BD 与适应症拓展决定下一阶段估值。',
    'henlius': '当前处于生物类似药现金流 + 创新药接力期：汉曲优全球放量提供稳定现金，PD-1 / ADC 创新管线逐步兑现；类似药价格下行与创新兑现节奏是主要变量，利率环境改善利好港股估值。',
    'akesobio': '当前处于双抗平台 + 出海 BD 大年兑现期：依沃西授权 Summit 带来大额里程碑与销售分成，卡度尼利国内放量；临床安全性与海外授权里程碑兑现是核心变量，BD 大年直接改善现金流与国际验证。',
    'remgen': '当前处于 ADC 平台 + 授权出海验证期：维迪西妥授权 Seagen / 辉瑞验证技术价值，自免管线（泰它西普）接力；ADC 赛道拥挤与里程碑兑现是主要变量，利率下行利好港股估值修复。',
    'zai-lab': '当前处于 license-in 商业化兑现 + 盈利冲刺期：引进产品（尼拉帕利、Optune 等）国内逐步放量，注册与商业化能力是变现关键；高度依赖外部管线授权与分成成本，盈利节奏与单品竞争是核心变量。',
    'innocare': '当前处于血液瘤专精 + 适应症拓展期：奥布替尼在 BTK 赛道与百济、阿斯利康竞争，自免（MS / SLE）延伸打开空间；BTK 内卷与适应症拓展不及预期是风险，出海授权探索是估值弹性来源。',
    'betta': '当前处于肺癌靶向深耕 + 代际迭代期：埃克替尼开篇、恩沙 / 贝福替尼接力形成肺癌靶向管线，估值由单品依赖转向代际延续；TKI 多代际同质竞争与医保降价是主要变量。',
    'kelun': '当前处于输液现金流 + 科伦博泰 ADC 期权兑现期：多个 ADC 授权默沙东带来大额里程碑，传统输液 / 仿制药集采压估值但提供现金；ADC 临床与授权兑现、集采是双变量，利率下行利好创新药估值。',
}


def co_cycle_text(co):
    return co.get('cycle') or INNOV_CYCLE.get(co['slug'], '')


def co_cycle_html(co, c):
    text = co_cycle_text(co)
    if not text:
        return ''
    return '<div class="card-cycle" style="border-left-color:#%s;background:rgba(%s,0.06)"><span class="cc-label" style="color:#%s">🔄 周期定位</span>%s</div>' % (c['accent'], c['accent_rgb'], c['accent'], text)


def co_cycle_section(co, c):
    text = co_cycle_text(co)
    if not text:
        return ''
    return '<div class="section-title">周期定位（公司级）</div>\n<div class="insight-box"><div class="insight-title"><span class="icon">🔄</span> 这家公司在周期里的位置</div><div class="insight-body">%s</div></div>' % text



# ---------- 家电 ----------
appliance = {
    'key': 'appliance', 'name': '家电产业链', 'short': '家电龙头', 'icon': '🔌',
    'accent': 'f59e0b', 'accent_rgb': '245,158,11', 'accent_dark': '2a1e08', 'nav_label': '家电',
    'n_companies': 11,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 用公开年报 / 官网 / 新闻原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 零部件与材料', 'desc': '压缩机 / 电机 / 芯片 / 钢材 / 塑料，核心部件自研是成本壁垒'},
        {'n': '02', 'name': '中游 · 制造与品牌', 'desc': '整机制造 / 智能制造 / 多品牌矩阵，规模与效率定胜负'},
        {'n': '03', 'name': '下游 · 渠道与出海', 'desc': '线上 / 线下 / 工程渠道，出海（OBM）与跨境电商成第二曲线'},
        {'n': '04', 'name': '消费与场景', 'desc': '厨房 / 清洁 / 环境 / 个护等家庭场景，更新换代与换新需求'},
        {'n': '05', 'name': '投资逻辑', 'desc': '品牌 / 渠道 / 出海能力，风险在地产周期、价格战与原材料'},
    ],
    'companies': [
        {'slug': 'midea', 'name': '美的集团', 'code': '000333', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '综合家电龙头，ToC + ToB 双轮与全球出海。',
         'stats': [('全品类', '白电+小家电'), ('出海', 'OBM全球'), ('ToB', '工业技术/机器人')],
         'overview': '美的集团是中国综合家电龙头，覆盖空调、冰箱、洗衣机、小家电全品类，并通过收购（库卡机器人、东芝家电、美芝压缩机）构建「消费电器 + 暖通空调 + 机器人及自动化 + 工业技术」多元版图。近年推动「数智化 + 全球化 + ToB」转型，海外以自有品牌（OBM）与本土化制造并重，是家电出海标杆。',
        'layers': [
            '自研美芝压缩机、威灵电机等核心部件，垂直整合降低成本的护城河。核心部件自供摊薄整机成本、提升毛利。',
            '全品类整机制造 + 灯塔工厂智能制造，多品牌矩阵（美的、小天鹅、东芝、COLMO）。规模与智能制造提升效率。',
            '国内线上线下全覆盖 + 海外 OBM / 并购 / 电商，渠道下沉与全球化。OBM 出海掌握品牌与定价权。',
            '厨房、空气、洗护、环境全屋家电，ToB 楼宇 / 工业。全屋与 ToB 打开增量场景。',
            '护城河 = 全产业链 + 品牌 + 全球，风险 = 地产周期、出海地缘、价格战、ToB 投入。全链与全球深，但地产与地缘是变量。'],
         'info': [('定位', '综合家电龙头'), ('品牌', '美的/小天鹅/COLMO'),
                  ('出海', 'OBM+并购'), ('关键看点', '全球化+ToB')],
         'moat': '核心部件垂直整合 + 全品类品牌 + 全球本土化，构成规模与效率壁垒。',
         'risks': '1）地产后周期需求；2）海外地缘与贸易摩擦；3）行业价格战；4）ToB 转型投入回报。'},
        {'slug': 'gree', 'name': '格力电器', 'code': '000651', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '空调一哥，渠道与品牌护城河深。',
         'stats': [('空调', '品类绝对领先'), ('渠道', '自有网络强'), ('高分红', '现金牛')],
         'overview': '格力电器以空调为核心，「好空调格力造」深入人心，家用与中央空调均居前列。其护城河在于空调品类的品牌心智、过硬质量口碑与深度绑定的经销商渠道（历史上「股份制区域销售公司」模式）。近年尝试多元化（生活电器、新能源、芯片）但空调仍为主轴；高分红、低估值、强现金流是标签。',
        'layers': [
            '压缩机、电机等自研自产比例高，凌达压缩机为核心部件支撑。核心部件自供保障质量与成本。',
            '空调整机制造工艺领先，质量口碑强，多元化（小家电 / 新能源）尚在培育。空调工艺壁垒深，多元化仍早期。',
            '经典经销商网络 + 线上（董明珠店 / 直播）+ 工程机，渠道利益绑定深。渠道持股绑定保障推力。',
            '家用空调、中央空调、生活电器，toC + toB 工程。工程机绑定地产与基建。',
            '护城河 = 空调品牌 + 渠道 + 质量，风险 = 空调天花板、多元化、地产周期、渠道变革。空调心智深，但天花板与渠道变革是风险。'],
         'info': [('核心', '空调'), ('品牌', '格力'),
                  ('财务', '高分红现金牛'), ('关键风险', '单一品类')],
         'moat': '空调品类品牌心智 + 自研核心部件 + 深度渠道绑定，构成空调壁垒。',
         'risks': '1）空调需求见顶与地产周期；2）多元化成效有限；3）渠道模式变革冲击；4）价格竞争。'},
        {'slug': 'haier', 'name': '海尔智家', 'code': '600690', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '高端化（卡萨帝）+ 全球化最彻底的家电巨头。',
         'stats': [('卡萨帝', '高端品牌'), ('全球化', '自主品牌出海'), ('全品类', '冰洗空厨')],
         'overview': '海尔智家是全球化最彻底的家电巨头，通过并购（GE Appliances、斐雪派克、Candy）建立全球自主品牌矩阵，高端品牌「卡萨帝」在国内高端冰洗空处于引领地位。业务覆盖冰洗空厨卫全品类，海外以「本土化研发 + 制造 + 营销」而非单纯代工，盈利能力随高端化与提效改善。',
        'layers': [
            '自研芯片 / 压缩机等逐步突破，全球供应链协同。核心部件突破降低外购依赖。',
            '全球多基地产能（中 / 美 / 欧 / 东盟），高端制造与柔性生产。本土化制造规避贸易壁垒。',
            '国内苏宁 / 电商 + 海外自主品牌渠道（GEA 等），高端体验店。自主品牌出海掌握终端。',
            '全屋智能家电、高端套系（卡萨帝）、智慧家庭。套系化提升客单与粘性。',
            '护城河 = 全球品牌 + 高端化 + 智家生态，风险 = 海外整合、地缘、汇率、地产。全球与高端深，但整合与汇率是变量。'],
         'info': [('高端', '卡萨帝'), ('全球', 'GEA/斐雪派克'),
                  ('全品类', '冰洗空厨'), ('关键看点', '高端化+全球化')],
         'moat': '全球自主品牌矩阵 + 卡萨帝高端心智 + 智家生态，构成国际化壁垒。',
        'risks': '1）海外并购整合与地缘；2）汇率波动；3）地产周期；4）高端竞争。'},
        {'slug': 'hisense', 'name': '海信家电', 'code': '000921', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '空调+冰洗+中央空调，并购三电切入汽车热管理。',
         'stats': [('中央空调', '强势'), ('冰洗', '稳健'), ('三电', '汽车热管理')],
         'overview': '海信家电业务涵盖空调（含中央空调，日立 / 海信 / 约克多品牌）、冰箱、洗衣机，并通过收购日本三电（Sanden）切入新能源汽车热管理，打开第二曲线。背靠海信集团（视像、信芯等）在显示与芯片有协同。特点是「家电基本盘 + 汽车热管理期权」。',
        'layers': [
            '压缩机、芯片（海信系协同）与三电热管理部件。集团协同降采购与研发成本。',
            '空调 / 冰洗整机制造 + 中央空调（多联机领先）+ 汽车热管理部件。中央空调与热管理为增量。',
            '国内渠道 + 工程机 / 中央空调 + 海外，三电配套车企。工程与车企渠道绑定客户。',
            '家用空调冰洗、楼宇中央空调、新能源车热管理。热管理打开第二曲线。',
            '护城河 = 中央空调 + 三电协同，风险 = 地产、汽车周期、整合、价格战。中央空调与热管理双线，但周期与整合是风险。'],
         'info': [('核心', '中央空调+冰洗'), ('第二曲线', '三电热管理'),
                  ('背景', '海信集团'), ('关键看点', '家电+汽车')],
         'moat': '中央空调多品牌优势 + 三电汽车热管理协同，构成双曲线壁垒。',
         'risks': '1）地产后周期；2）汽车景气与三电整合；3）价格战；4）原材料成本。'},
        {'slug': 'robam', 'name': '老板电器', 'code': '002508', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '厨电龙头，高端烟灶消品牌心智强。',
         'stats': [('烟灶', '高端领先'), ('厨电', '品牌强'), ('工程', '地产绑定')],
         'overview': '老板电器是中国厨房电器龙头，在吸油烟机、燃气灶、消毒柜等品类长期居高端领先，品牌与渠道（尤其工程渠道绑定头部房企）优势明显。受地产周期影响大，近年拓展洗碗机、集成灶、蒸烤一体等第二品类以平滑周期。',
        'layers': [
            '电机、控制器等部件，自产与外协结合。核心部件自制保品质，外协灵活产能。',
            '烟灶消整机制造工艺成熟，高端定位质价比。工艺积累支撑高端溢价。',
            '零售 + 电商 + 工程（房企精装）三端，工程渠道受地产拖累。工程绑定头部房企但回款承压。',
            '厨房烹饪（吸排油烟、灶具）、洗碗 / 蒸烤、旧改换新。换新与旧改平滑新房周期。',
            '护城河 = 厨电品牌 + 渠道，风险 = 地产周期、工程坏账、品类拓展、价格战。品牌与渠道深，但地产强相关。'],
         'info': [('核心', '烟灶消'), ('定位', '高端厨电'),
                  ('渠道', '工程+零售'), ('关键风险', '地产强相关')],
         'moat': '高端厨电品牌心智 + 工程与零售双渠道，构成厨电壁垒。',
         'risks': '1）地产周期与工程回款；2）品类拓展成效；3）价格战；4）换新需求波动。'},
        {'slug': 'supor', 'name': '苏泊尔', 'code': '002032', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '炊具+小家电龙头，SEB 控股赋能全球。',
         'stats': [('炊具', '市占领先'), ('SEB', '法资控股'), ('小家电', '稳健')],
         'overview': '苏泊尔是炊具（压力锅、炒锅）与厨房小家电龙头，法国 SEB 集团控股后获得全球技术、品牌（如 Tefal）与出口订单协同，海外代工与自有品牌并重。业务稳健、分红好，受地产影响小但受消费景气与原材料（铝、钢）价格影响。',
        'layers': [
            '铝 / 钢 / 塑料等原材料，供应链成熟，SEB 全球采购协同。原材料价格与 SEB 采购影响成本。',
            '炊具 + 小家电（电饭煲、电磁炉、空气炸锅）制造，品质稳定。SEB 技术赋能产品力。',
            '国内线上线下 + 海外（SEB 订单 / 代工）+ 电商，出口占比高。出口订单稳收入但受贸易影响。',
            '厨房烹饪（锅具、电器）、个护小电。炊具刚需弱周期。',
            '护城河 = SEB 协同 + 炊具品牌，风险 = 出口摩擦、原材料、消费景气、汇率。SEB 协同深，但出口与成本是变量。'],
         'info': [('核心', '炊具+小家电'), ('背景', 'SEB控股'),
                  ('出口', '代工+自有'), ('关键看点', '稳健分红')],
         'moat': 'SEB 全球技术与订单协同 + 炊具龙头品牌，构成稳态壁垒。',
         'risks': '1）海外出口贸易摩擦；2）原材料价格；3）消费景气波动；4）汇率。'},
        {'slug': 'joyoung', 'name': '九阳股份', 'code': '002242', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '豆浆机开创者，深耕厨房小家电。',
         'stats': [('豆浆机', '品类开创'), ('小家电', '厨房场景'), ('膳魔师', '收购拓展')],
         'overview': '九阳以豆浆机起家并开创品类，后扩展至破壁机、电饭煲、空气炸锅、净水等厨房小家电。近年收购 SharkNinja（后分拆）相关业务、布局太空厨房等，尝试破圈。生意受小家电景气与均价竞争影响，主打「健康饮食」场景。',
        'layers': [
            '电机、加热件等，供应链成熟。成熟供应链支撑快迭代。',
            '厨房小家电制造，品类迭代快。快迭代应对红海竞争。',
            '线上为主（小家电电商占比高）+ 线下 + 内容种草。线上与内容驱动转化。',
            '早餐 / 健康饮食（豆浆、破壁、空气炸锅）。健康饮食场景高频。',
            '护城河 = 豆浆机心智 + 渠道，风险 = 小家电竞争、均价下行、景气、创新。豆浆机心智深，但红海与均价是风险。'],
         'info': [('开篇', '豆浆机'), ('场景', '健康厨房'),
                  ('属性', '厨房小家电'), ('关键风险', '红海竞争')],
         'moat': '豆浆机品类开创者心智 + 厨房小电渠道，构成细分壁垒。',
         'risks': '1）小家电赛道极度竞争；2）均价与利润下行；3）消费景气；4）品类创新节奏。'},
        {'slug': 'roborock', 'name': '石头科技', 'code': '688169', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '扫地机器人高端出海标杆。',
         'stats': [('扫地机', '高端技术'), ('出海', '全球品牌'), ('自研', '算法+激光')],
         'overview': '石头科技是扫地机器人高端代表，以自研激光导航（LDS）、避障算法与强产品力著称，海外（尤其欧洲、北美）自主品牌放量成功，单价与利润率高于行业。生意高毛利、强研发，但受消费电子周期与新品节奏影响，竞争（科沃斯、追觅等）激烈。',
        'layers': [
            '激光雷达、电机、电池、芯片，自研比例高。核心元器件自研提升性能与毛利。',
            '扫地机 / 洗地机整机制造，代工与自产结合，产品迭代快。快迭代维持高端定位。',
            '海外自营 + 电商（亚马逊等）+ 国内线上，高端定位。自营海外掌握品牌定价。',
            '家庭地面清洁（扫地 / 拖地 / 洗地），智能懒人经济。懒人经济需求高频升级。',
            '护城河 = 算法 + 品牌出海，风险 = 竞争、消费电子周期、新品、关税。算法与出海深，但竞争与关税是风险。'],
         'info': [('核心', '扫地机器人'), ('定位', '高端出海'),
                  ('技术', '激光导航自研'), ('关键风险', '红海+周期')],
         'moat': '自研导航算法 + 全球高端品牌，构成技术出海壁垒。',
         'risks': '1）扫地机竞争白热化；2）消费电子需求周期；3）关税与出海成本；4）新品不及预期。'},
        {'slug': 'ecovacs', 'name': '科沃斯', 'code': '603486', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '扫地机器人+洗地机双线，添可（TINECO）新锐。',
         'stats': [('扫地机', '国内领先'), ('添可', '洗地机新锐'), ('双品牌', '科沃斯+添可')],
         'overview': '科沃斯是扫地机器人国内龙头，并孵化洗地机品牌「添可（TINECO）」成为第二增长极，形成「科沃斯（扫地）+ 添可（洗地）」双品牌。研发与营销投入大，渠道线上线下并重，海外亦有布局。挑战是同质化竞争与营销费用。',
        'layers': [
            '电机、传感器、电池自研 / 外协，供应链成熟。核心部件自制提升差异化。',
            '扫地机 + 洗地机整机制造，代工与自产结合。双品类共线提效率。',
            '国内线上 / 线下 + 海外（添可出海强）+ 内容营销。内容营销驱动添可放量。',
            '家庭清洁（扫地、拖地、洗地），懒人经济。清洁全场景覆盖。',
            '护城河 = 双品牌 + 渠道，风险 = 竞争、营销费用、周期、出海。双品牌强，但营销内卷是压力。'],
         'info': [('双品牌', '科沃斯+添可'), ('核心', '扫地机+洗地机'),
                  ('属性', '清洁电器'), ('关键风险', '营销内卷')],
         'moat': '科沃斯+添可双品牌矩阵 + 清洁全场景渠道，构成清洁电器壁垒。',
         'risks': '1）清洁电器竞争红海；2）高营销费用；3）消费周期；4）出海摩擦。'},
        {'slug': 'bull', 'name': '公牛集团', 'code': '603195', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '插座转换器绝对龙头，向电工照明扩张。',
         'stats': [('转换器', '市占绝对'), ('安全', '品牌心智'), ('拓品类', '照明/新能源')],
         'overview': '公牛集团是插座 / 转换器绝对龙头，「公牛安全插座」国民心智极深，渠道（五金店、便利店、电商）下沉到极致。近年向墙壁开关、LED 照明、新能源（充电桩 / 储能）扩张，试图复制「安全 + 渠道」能力到新品类。生意轻资产、高毛利、强现金流。',
        'layers': [
            '铜材、塑料、电子件，供应链成熟可控。铜价等原材料影响成本。',
            '转换器 / 开关插座标准化制造，品控与规模优势强。规模摊薄制造成本。',
            '百万级五金 / 数码 / 电商终端，下沉渗透极致，新能源渠道共建。渠道密度构筑壁垒。',
            '家庭 / 办公用电连接、照明、新能源车充电。转换器刚需高频。',
            '护城河 = 安全品牌 + 渠道密度，风险 = 品类天花板、新能源拓展、价格战、地产。品牌与渠道极深，但品类天花板是约束。'],
         'info': [('核心', '转换器/插座'), ('心智', '安全插座'),
                  ('扩张', '照明/新能源'), ('关键看点', '渠道复用')],
         'moat': '「安全插座」国民品牌 + 极致下沉渠道，构成转换器壁垒。',
         'risks': '1）转换器品类天花板；2）新品类（新能源）拓展不确定；3）价格竞争；4）地产相关。'},
        {'slug': 'bear', 'name': '小熊电器', 'code': '002959', 'region': '中国', 'region_cls': 'region-cn',
         'desc': '创意小家电「萌系」品牌，长尾细分突围。',
         'stats': [('创意小电', '萌系定位'), ('长尾', '细分品类'), ('电商', '线上为主')],
         'overview': '小熊电器以「萌系」创意小家电（酸奶机、电炖盅、养生壶、加湿器等）切入长尾细分市场，避开与美的 / 九阳在主流品类的正面竞争，靠电商与内容营销崛起。特点是「多 SKU、小批量、快迭代」。受小家电景气与均价竞争影响，需持续推新维持增长。',
        'layers': [
            '小电机、塑料、加热件，供应链灵活。灵活供应链支撑多 SKU。',
            '多 SKU 小家电制造，代工 + 自产结合，柔性快反。柔性产线匹配长尾需求。',
            '线上电商为主（天猫 / 抖音 / 京东）+ 内容种草，线下补充。线上内容驱动爆款。',
            '单身 / 小家庭创意厨房、个护、生活小电。小家庭场景细分。',
            '护城河 = 萌系品牌 + 长尾SKU，风险 = 竞争、均价下行、景气、库存。萌系与快反深，但红海与库存是风险。'],
         'info': [('定位', '创意萌系小电'), ('策略', '长尾细分'),
                  ('渠道', '线上为主'), ('关键风险', '红海+快迭代')],
         'moat': '萌系创意品牌 + 长尾多 SKU 快反，构成差异化小电壁垒。',
         'risks': '1）小家电红海竞争；2）均价与利润压力；3）消费景气；4）SKU 迭代与库存。'},
    ],
}
CHAINS.append(appliance)


def render_index(c):
    accent = c['accent']; rgb = c['accent_rgb']; dark = c['accent_dark']
    css = css_for(accent, rgb, dark)
    layers_html = ''.join(
        '<div class="layer-card"><div class="layer-num">%s</div><div class="layer-name">%s</div><div class="layer-desc">%s</div></div>' % (L['n'], L['name'], L['desc'])
        for L in c['layers'])
    cards_html = ''.join(
        '<a class="giant-card" href="berkshire-%s-chain-%s.html"><div class="giant-head"><span class="giant-name">%s 链</span><span class="region-tag %s">%s</span></div><div class="giant-desc">%s</div>%s<div class="giant-foot"><span class="giant-link">查看跨层分析 →</span></div></a>' % (c['key'], co['slug'], co['name'], co['region_cls'], co['region'], co['desc'], co_cycle_html(co, c))
        for co in c['companies'])
    breadcrumb = '<a href="berkshire-standalone.html">数据中心</a><span class="crumb-sep">/</span><span>%s</span>' % c['name']
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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

%s

<div class="section-title">产业周期判断标准</div>
<div class="cycle-block" id="cycle"><div class="cycle-title"><span class="icon">🔄</span> %s 产业周期怎么看</div><div class="cycle-body">%s</div><div class="cycle-current"><b>当前位置（定性框架，非数据结论）</b>：%s</div></div>

<div class="section-title">%s索引（上市公司 %s 家）</div>
<div class="grid">
%s
</div>

%s

<div class="source-note">
📌 <b>资料与合规</b>：本页所有分析均基于各公司<b>公开年报、官网、产品发布与新闻</b>等事实层信息，由本站原创整理与重写；不复制、不转载任何付费 / 闭源专享内容。文中对具体公司的判断仅作研究框架示例，<b>不构成投资建议</b>。
</div>

</div>
</body>
</html>''' % (c['name'], css, top_bar(accent, c['nav_label'], breadcrumb), c['name'], c['hero_sub'], c['n_companies'], c['icon'], c['name'], c['short'], layers_html, c.get('framework_story', ''), c['name'], CYCLE[c['key']]['criteria'], CYCLE[c['key']]['current'], c['short'], c['n_companies'], cards_html, extend_reading(c))


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
    extra = detail_extra(c, co, accent)
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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

%s

<div class="back-bar">
<a href="berkshire-%s-chains.html" class="back-btn">← 返回%s</a>
</div>

<div class="source-note">
📌 <b>资料与合规</b>：本页所有分析均基于各公司<b>公开年报、官网、产品发布与新闻</b>等事实层信息，由本站原创整理与重写；不复制、不转载任何付费 / 闭源专享内容。文中对具体公司的判断仅作研究框架示例，<b>不构成投资建议</b>。
</div>

</div>
</body>
</html>''' % (co['name'], c['name'], css, top_bar(accent, c['nav_label'], breadcrumb), co['name'], co['desc'], co['region_cls'], co['region'], stats_html, co['overview'], layers_html, info_html, co['moat'], co['risks'], co_cycle_section(co, c), extra, c['key'], c['name'])


def main():
    for c in CHAINS:
        idx = render_index(c)
        with open(os.path.join(ROOT, 'berkshire-%s-chains.html' % c['key']), 'w', encoding='utf-8') as f:
            f.write(idx)
        for co in c['companies']:
            d = render_detail(c, co)
            with open(os.path.join(ROOT, 'berkshire-%s-chain-%s.html' % (c['key'], co['slug'])), 'w', encoding='utf-8') as f:
                f.write(d)
        print('chain %s: index + %d details written' % (c['key'], len(c['companies'])))


if __name__ == '__main__':
    main()