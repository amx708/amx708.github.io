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
.fin-block{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px 16px;margin-bottom:8px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.fin-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;gap:10px}
.fin-title{font-size:15px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:8px}
.fin-title .icon{color:#__ACC__}
.fin-tag{font-size:11px;color:#b45309;background:rgba(251,191,36,0.14);border:1px solid rgba(251,191,36,0.35);padding:2px 9px;border-radius:10px;white-space:nowrap}
.fin-table{width:100%;border-collapse:collapse;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden}
.fin-table tr{border-bottom:1px solid #eef2f7}
.fin-table tr:last-child{border-bottom:none}
.fin-table td{padding:9px 12px;font-size:13px;color:#334155}
.fin-table td:first-child{width:130px;color:#64748b}
.fin-table .val{color:#b45309;font-weight:600;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.fin-note{font-size:12px;color:#64748b;margin-top:8px;line-height:1.6}
.poisson-char{font-family:"Segoe UI","Microsoft YaHei",Arial,sans-serif;font-variant-emoji:text;-webkit-font-variant-emoji:text}
.poisson-pill{display:inline-block;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:700}
@media(max-width:640px){.fin-block{padding:10px 12px;margin-bottom:6px}.fin-head{flex-wrap:wrap;gap:6px;margin-bottom:8px}.fin-title{font-size:14px;gap:6px}.fin-tag{font-size:10px;padding:2px 7px}.fin-table td{padding:7px 10px;font-size:12px}.fin-table td:first-child{width:auto;min-width:90px}.fin-note{font-size:11px;line-height:1.55}}
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
    'semiconductor-design': {
        'criteria': '''<p><b>驱动变量</b>：下游需求（AI 算力 / 手机 / 汽车 / 物联网）、国产替代率、晶圆代工产能与价格、代工限制（先进制程）、库存周期、产品迭代（端侧 AI）。</p><ul><li><b>国产替代</b>：国产手机与 AI 算力链拉动设计公司转单，替代空间结构性增长。</li><li><b>代工产能</b>：台积电 / 中芯产能与代工价格是设计公司成本与供给核心变量。</li><li><b>库存周期</b>：芯片渠道库存去化到补库，是设计公司业绩弹性来源。</li><li><b>产品迭代</b>：端侧 AI（NPU/SoC）、汽车电子提升芯片价值量与用量。</li><li><b>代工限制</b>：先进制程受设备管制，倒逼成熟制程与架构创新。</li></ul>''',
        'current': '半导体设计呈「国产替代 + 端侧 AI + 汽车电子」三轮驱动：国产手机与 AI 算力链拉动 Fabless 转单，端侧 AI 与智驾提升芯片价值量；最大变量是代工产能与价格、库存周期、先进制程限制与产品迭代节奏，订单与毛利率是兑现信号。'
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
  <div class="fin-note">数据说明：本表数值取自各公司公开披露的年报/财报，已做原创整理；报告期与单位以各页标注为准。本页为价值研究素材，不构成投资建议。</div>
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
from _semiconductor_design_data import semiconductor_design

CHAINS = [semiconductor_design]

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
