# -*- coding: utf-8 -*-
"""生成 机器人 产业链地图（浅色风 + 12链互通导航）。
用法：python _build_robot_chain_pages.py
产出写入 deploy_site/ 根目录（站点源），再 cp 到 repo/amx708.github.io/。

机器人是全球概念链（A股 / 港股 / 美股 / 非上市），跨市场 PE/PB 不可直接对比；
本页为框架级原创整理，财务数据仅对 A 股成分公司逐家抓取真实年报填充，
无 A 股代码的全球标的（Tesla / NVIDIA / 优必选）保留占位并诚实标注。"""
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
.region-us{background:rgba(59,130,246,0.14);color:#1d4ed8;border:1px solid rgba(59,130,246,0.3)}
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


# ============ 产业周期判断标准（机器人：全球概念链，无传统产能周期，定性框架） ============
CYCLE = {
    'robot': {
        'criteria': '''<p><b>驱动变量</b>：主机厂量产节奏（台数 / 良率 / 单位成本）、核心零部件订单与产能、政策支持（人形机器人 / 具身智能）、AI 大模型进展、估值水位（主题炒作 vs 业绩兑现）。</p>
<ul>
<li><b>量产爬坡</b>：小批量内部部署 → 千台 → 万台，良率与成本曲线是关键；从演示视频到"经济量产"是最大鸿沟。</li>
<li><b>订单与定点</b>：零部件厂商获 Tier1 / 主机厂定点 → 收入验证；特斯拉 / Figure / 优必选 / 宇树等出货节奏是风向标。</li>
<li><b>政策</b>：国家与地方"具身智能 / 人形机器人"行动方案、首台套补贴、制造业转型升级，提供需求与信心支撑。</li>
<li><b>技术</b>：大模型（VLM / 端到端）降低具身智能门槛；执行器降本（丝杠 / 减速器国产化）决定放量速度。</li>
<li><b>估值</b>：主题阶段 PE / PB 失真，多看 PS / 订单 / 量产指引；警惕"故事"与业绩背离、筹码过热。</li>
</ul>''',
        'current': '机器人处于"0→1 量产导入期"：2025–2026 全球主机厂密集发布与小规模部署，核心零部件（减速器 / 丝杠 / 电机 / 传感 / 视觉）率先兑现订单；A 股以"主题 + 订单"驱动，估值含较高预期，须盯量产实绩与业绩兑现，警惕过热与单一客户依赖。'
    },
}


# 财务 / 估值占位框架（不编造数字，待逐家抓取真实数据后填充；无 A 股代码者保持占位）
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
  <div class="fin-note">占位框架：待逐家抓取最新年报（以 2025 年报为主）后填充真实数值，并标注报告期与数据来源；无 A 股代码的公司（如 Tesla / NVIDIA / 优必选）本环境无法经 A 股接口取数，保留占位诚实标注。</div>
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

# ---------- 机器人（全球概念链） ----------
robot = {
    'key': 'robot', 'name': '机器人产业链', 'short': '机器人', 'icon': '🤖',
    'accent': '10b981', 'accent_rgb': '16,185,129', 'accent_dark': '064e3b', 'nav_label': '机器人',
    'n_companies': 16,
    'hero_sub': '价值投资视角下的「跨层全栈」梳理 · 全球概念链（A股 / 港股 / 美股），跨市场估值不可直接对比 · 用公开资料原创整理，不复制任何付费内容',
    'layers': [
        {'n': '01', 'name': '上游 · 核心零部件', 'desc': '减速器 / 丝杠 / 电机 / 传感器 / 视觉 / 控制器——机器人的"肌肉与感官"，价值量高、国产替代空间大'},
        {'n': '02', 'name': '中游 · 本体与执行器总成', 'desc': '整机厂 / 关节模组 / 结构件——把零件拼成"身体"，量产与工艺是核心壁垒'},
        {'n': '03', 'name': '软件与具身智能', 'desc': 'AI 大脑 / 运动控制算法 / 仿真训练——机器人的"神经与思维"，大模型降低具身智能门槛'},
        {'n': '04', 'name': '应用场景', 'desc': '工厂 / 商业服务 / 家庭 / 特种——落地的"用武之地"，先从结构化封闭场景跑通'},
        {'n': '05', 'name': '投资逻辑', 'desc': '量产进度 / 订单定点 / 估值水位 / 护城河与风险——价值投资视角下的框架判断'},
    ],
    'companies': [
        {'slug': 'lvharmonics', 'name': '绿的谐波', 'code': '688017', 'region': '中国', 'region_cls': 'region-cn', 'desc': '谐波减速器国产龙头，人形机器人旋转关节核心供应商。', 'stats': [('谐波', '国产龙头'), ('人形', '旋转关节'), ('替代', '主线')], 'overview': '绿的谐波是国内谐波减速器龙头，产品用于工业机器人、机床及人形机器人旋转关节。谐波减速器是机器人的"关节"，技术壁垒高、国产化率低，是人形机器人放量最受益的环节之一。公司打破日本 HD 垄断，绑定头部本体厂，受益于人形机器人量产与工业自动化双轮驱动。', 'layers': ['谐波减速器是机器人旋转关节核心，占整机成本比重高；公司技术对标日本 HD，是国产替代主力。', '作为上游零件供应商，不直接做本体；通过 Tier1 / 本体厂进入人形机器人供应链。', '减速器精度与寿命影响运动控制表现，是具身智能执行层的基础硬件。', '需求来自工业机器人（基本盘）＋人形机器人（增量）；后者从千台向万台爬坡拉动弹性。', '护城河 = 专利 + 工艺 + 客户认证；风险 = 人形量产不及预期、价格战、单一大客户依赖。'], 'info': [('主业', '谐波减速器'), ('地位', '国产龙头'), ('看点', '人形 + 工业双轮'), ('属性', '上游零件')], 'moat': '谐波减速器工艺与专利壁垒高，客户认证周期长，是国产替代核心标的。', 'risks': '1）人形机器人量产不及预期；2）行业扩产致价格战；3）大客户集中；4）技术迭代风险。'},
        {'slug': 'shuanghuan', 'name': '双环传动', 'code': '002472', 'region': '中国', 'region_cls': 'region-cn', 'desc': '高精度齿轮与 RV 减速器龙头，机器人 + 新能源车双主业。', 'stats': [('RV', '国内领先'), ('齿轮', '全球配套'), ('双主业', '机器人 + 车')], 'overview': '双环传动是精密齿轮与 RV 减速器龙头，主业覆盖新能源汽车电驱齿轮（全球配套）与机器人 RV 减速器。RV 减速器用于机器人重载关节，壁垒高、长期被纳博特斯克垄断；公司是国内少数实现批量配套的企业，受益人形机器人线性 / 旋转关节放量及工业自动化。', 'layers': ['RV 减速器用于机器人重载 / 大臂关节，精度寿命要求高；公司实现国产化突破，进入本体厂供应链。', '以齿轮与减速器供应为主，属上游核心零件；同时布局执行器总成能力。', '减速器性能决定关节出力与精度，是运动控制底层硬件。', '需求来自工业机器人（基本盘）＋人形机器人（增量弹性）＋新能源车齿轮（稳定现金流）。', '护城河 = 高精度齿轮工艺 + 车规级体系 + 客户；风险 = 人形进度、车市波动、价格战。'], 'info': [('主业', '齿轮 + RV 减速器'), ('地位', '国内领先'), ('双轮', '机器人 + 新能源车'), ('看点', '人形弹性')], 'moat': '高精度齿轮工艺积累与车规级质量体系，构成跨机器人 / 汽车的复用壁垒。', 'risks': '1）人形量产不及预期；2）新能源汽车价格战传导；3）RV 价格竞争；4）客户集中。'},
        {'slug': 'zhongdali', 'name': '中大力德', 'code': '002896', 'region': '中国', 'region_cls': 'region-cn', 'desc': '精密减速器与传动件供应商，覆盖谐波 / RV / 行星。', 'stats': [('减速器', '多品类'), ('传动', '精密件'), ('人形', '关节受益')], 'overview': '中大力德主营精密减速器（谐波 / RV / 行星）与传动部件，产品用于工业机器人、自动化设备及人形机器人关节。公司作为中小市值零部件标的，受益于人形机器人关节模组放量与国产替代，弹性较大但业绩兑现与订单可见度需跟踪。', 'layers': ['提供谐波 / RV / 行星多品类减速器，覆盖机器人各类关节；国产替代逻辑清晰。', '上游零件供应商，亦布局机电一体化模组，向"零件 → 模组"延伸。', '减速器是运动执行基础件，精度寿命影响整机表现。', '工业机器人为基本盘，人形机器人为增量；订单节奏决定业绩弹性。', '护城河 = 多品类减速器工艺；风险 = 规模不足、人形进度、盈利波动大。'], 'info': [('主业', '精密减速器'), ('品类', '谐波 / RV / 行星'), ('弹性', '中小市值'), ('看点', '人形关节')], 'moat': '多品类减速器技术与产线，可快速响应关节模组多样化需求。', 'risks': '1）人形量产节奏；2）规模效应不足致毛利波动；3）客户集中度；4）估值偏高。'},
        {'slug': 'henli', 'name': '恒立液压', 'code': '601100', 'region': '中国', 'region_cls': 'region-cn', 'desc': '液压件龙头，进军线性执行器与行星滚柱丝杠。', 'stats': [('液压', '全球龙头'), ('丝杠', '新增长极'), ('制造', '精密')], 'overview': '恒立液压是工程机械液压件全球龙头，近年切入线性执行器与行星滚柱丝杠（机器人直线关节核心）。丝杠是人形机器人线性关节关键，长期被海外垄断；公司凭精密制造能力进军，若导入人形供应链将打开第二曲线，但当前机器人收入占比仍小。', 'layers': ['行星滚柱丝杠是机器人直线关节核心传动件，壁垒高；公司精密制造延伸布局。', '以液压件为主业，丝杠 / 执行器为新切入；属上游核心零件"补短板"。', '丝杠精度与负载直接决定线性关节性能，是执行层硬件。', '工程机械为基本盘（周期波动），人形机器人为远期增量，尚处导入期。', '护城河 = 精密制造 + 规模 + 客户；风险 = 丝杠导入不及预期、工程机械周期下行。'], 'info': [('主业', '液压件'), ('新极', '丝杠 / 执行器'), ('属性', '上游零件'), ('看点', '第二曲线')], 'moat': '液压精密制造与规模化能力外溢至丝杠，形成高端传动件复用壁垒。', 'risks': '1）丝杠 / 执行器导入人形供应链进度；2）工程机械周期下行；3）新业务投入大。'},
        {'slug': 'beisite', 'name': '贝斯特', 'code': '300580', 'region': '中国', 'region_cls': 'region-cn', 'desc': '精密零部件与涡轮增压件，拓展行星滚柱丝杠。', 'stats': [('丝杠', '行星滚柱'), ('精密', '制造能力'), ('增量', '人形关节')], 'overview': '贝斯特主营涡轮增压器精密零部件，近年布局行星滚柱丝杠与人形机器人直线关节执行器。丝杠是直线关节核心，国产替代空间大；公司凭精密机加工能力切入，机器人业务处早期，弹性取决于量产导入与产能释放。', 'layers': ['行星滚柱丝杠用于机器人直线关节，壁垒高；公司精密加工延伸布局。', '以精密零部件供应为主，向"丝杠 + 执行器"延伸，属上游补链。', '丝杠精度与刚性影响直线关节出力与寿命。', '汽车精密件为基本盘，人形机器人为增量；订单与良率决定弹性。', '护城河 = 精密机加工工艺；风险 = 丝杠客户导入、汽车业务波动、产能爬坡。'], 'info': [('主业', '精密零部件'), ('新极', '行星滚柱丝杠'), ('属性', '上游零件'), ('看点', '人形增量')], 'moat': '高精度机加工工艺与自动化产线，可复用至丝杠等机器人精密件。', 'risks': '1）丝杠量产导入不及预期；2）汽车业务周期波动；3）新业务毛利率爬坡。'},
        {'slug': 'mingzhi', 'name': '鸣志电器', 'code': '603728', 'region': '中国', 'region_cls': 'region-cn', 'desc': '步进 / 无框力矩电机与驱动龙头，人形灵巧手受益。', 'stats': [('电机', '步进龙头'), ('力矩', '无框电机'), ('灵巧手', '受益')], 'overview': '鸣志电器是步进电机与运动控制龙头，产品涵盖步进 / 伺服 / 无框力矩电机，广泛用于工业自动化、半导体设备及人形机器人关节与灵巧手。无框力矩电机是机器人旋转 / 腕部关节核心，公司技术积累深，受益人形机器人关节电机放量。', 'layers': ['无框力矩电机 / 步进电机是机器人关节与灵巧手驱动核心，公司技术领先。', '以电机与驱动供应为主，属上游"肌肉"；亦提供运动控制模组。', '电机扭矩密度与响应速度决定关节灵活度，是具身执行层关键。', '工业自动化 / 半导体为基本盘，人形机器人为高弹性增量。', '护城河 = 电机 + 驱动一体化 + 客户；风险 = 人形进度、价格战、海外业务波动。'], 'info': [('主业', '电机 + 驱动'), ('核心', '无框力矩电机'), ('看点', '灵巧手'), ('属性', '上游零件')], 'moat': '电机与运动控制一体化能力及长期客户积累，构成执行器壁垒。', 'risks': '1）人形量产不及预期；2）电机价格竞争；3）海外（美 / 欧）业务与贸易摩擦。'},
        {'slug': 'huichuan', 'name': '汇川技术', 'code': '300124', 'region': '中国', 'region_cls': 'region-cn', 'desc': '工业自动化与伺服龙头，机器人"大脑 + 神经"供应商。', 'stats': [('伺服', '国产第一'), ('工控', '龙头'), ('控制', '运动控制')], 'overview': '汇川技术是工业自动化与伺服系统国产龙头，产品涵盖伺服、变频器、PLC 与运动控制器，广泛用于工业机器人及产线自动化。在机器人产业链中，公司是"控制 + 驱动"核心供应商，亦布局机器人本体与具身智能控制系统，平台化优势明显。', 'layers': ['伺服 / 控制器是机器人关节驱动与控制核心；公司国产替代主力。', '提供驱动 + 控制，并布局本体；属"控制神经"层关键供应商。', '运动控制算法与控制器是具身智能执行层软件基础。', '工业自动化为基本盘（稳健），机器人 / 新能源车 / 储能多极增长。', '护城河 = 工控平台 + 算法 + 客户；风险 = 工控周期、竞争加剧、人形进展。'], 'info': [('主业', '工控 / 伺服'), ('地位', '国产龙头'), ('平台', '多极增长'), ('看点', '控制层')], 'moat': '工业自动化平台化（驱动 + 控制 + 软件）与客户壁垒，难以被单点突破。', 'risks': '1）工业自动化周期下行；2）伺服 / 变频器竞争加剧；3）人形布局兑现慢。'},
        {'slug': 'jiangsuleili', 'name': '江苏雷利', 'code': '300660', 'region': '中国', 'region_cls': 'region-cn', 'desc': '微特电机与执行器供应商，人形关节 / 灵巧手受益。', 'stats': [('电机', '微特龙头'), ('执行器', '关节模组'), ('灵巧手', '受益')], 'overview': '江苏雷利主营微特电机（步进 / 无刷 / 空心杯）与执行器，产品用于家电、汽车及人形机器人关节与灵巧手。空心杯电机是灵巧手驱动核心，壁垒高；公司凭电机与精密制造切入机器人，弹性取决于人形供应链导入。', 'layers': ['空心杯 / 无刷电机用于灵巧手与微型关节，公司微特电机技术积累深。', '以电机与执行器模组供应为主，属上游"肌肉"；布局关节总成。', '微型电机扭矩密度影响灵巧手灵活度，是执行层关键硬件。', '家电 / 汽车为基本盘，人形机器人为增量；订单决定弹性。', '护城河 = 微特电机工艺 + 客户；风险 = 人形导入、家电波动、价格竞争。'], 'info': [('主业', '微特电机'), ('核心', '空心杯电机'), ('看点', '灵巧手'), ('属性', '上游零件')], 'moat': '空心杯等微特电机精密工艺，构成灵巧手驱动细分壁垒。', 'risks': '1）人形供应链导入不及预期；2）家电需求波动；3）微电机价格竞争。'},
        {'slug': 'keli', 'name': '柯力传感', 'code': '603662', 'region': '中国', 'region_cls': 'region-cn', 'desc': '应变式传感器龙头，布局力矩 / 六维力传感器。', 'stats': [('传感', '应变式龙头'), ('六维力', '机器人核心'), ('国产', '替代')], 'overview': '柯力传感是应变式传感器（称重 / 测力）龙头，并布局力矩传感器与六维力传感器，后者是人形机器人关节力控与灵巧手核心。力控是机器人安全交互的关键，技术壁垒高、国产化率低；公司受益人形机器人力传感放量。', 'layers': ['六维力 / 力矩传感器是机器人力控核心，公司应变式传感技术延伸布局。', '以传感器供应为主，属上游"感官"；亦探索传感 + 算法方案。', '力反馈是具身智能安全交互与精细操作的基础感知。', '工业称重为基本盘，人形机器人力传感为高弹性增量。', '护城河 = 传感工艺 + 标定能力；风险 = 六维力量产、人形进度、价格战。'], 'info': [('主业', '应变式传感器'), ('核心', '六维力传感器'), ('看点', '力控'), ('属性', '上游零件')], 'moat': '应变式传感工艺与标定数据积累，构成力传感器细分壁垒。', 'risks': '1）六维力传感器量产良率；2）人形进度；3）工业传感价格竞争。'},
        {'slug': 'orbbec', 'name': '奥比中光', 'code': '688322', 'region': '中国', 'region_cls': 'region-cn', 'desc': '3D 视觉传感龙头，机器人"眼睛"核心供应商。', 'stats': [('3D视觉', '龙头'), ('感知', '机器人之眼'), ('AI', '端侧')], 'overview': '奥比中光是国内 3D 视觉传感龙头，提供结构光 / ToF 等 3D 摄像头，用于机器人导航、避障与抓取识别。3D 视觉是机器人"眼睛"，是具身智能感知层核心；公司受益人形机器人与服务机器人放量，但当前仍处亏损扭亏阶段。', 'layers': ['3D 视觉摄像头是机器人环境感知核心，公司国产 3D 传感龙头。', '以视觉传感器供应为主，属上游"感官"；提供感知模组方案。', '视觉数据是具身智能空间理解与抓取决策的输入基础。', '服务机器人 / 手机 / 刷脸为基本盘，人形机器人为增量。', '护城河 = 3D 传感专利 + 算法；风险 = 仍亏损、人形进度、视觉路线竞争。'], 'info': [('主业', '3D 视觉传感'), ('核心', '机器人之眼'), ('看点', '具身感知'), ('属性', '上游零件')], 'moat': '3D 视觉全栈（光学 + 芯片 + 算法）专利与量产能力，构成感知壁垒。', 'risks': '1）持续亏损与盈利兑现；2）人形放量不及预期；3）视觉技术路线切换。'},
        {'slug': 'estun', 'name': '埃斯顿', 'code': '002747', 'region': '中国', 'region_cls': 'region-cn', 'desc': '国产工业机器人本体龙头，全产业链布局。', 'stats': [('本体', '国产龙头'), ('全栈', '核心部件'), ('自动化', '集成')], 'overview': '埃斯顿是国产工业机器人本体龙头，通过自研 + 并购（如 TRIO / Cloos）实现"控制器 + 伺服 + 本体"全自主，布局工业机器人与智能制造。在机器人产业链中属中游本体与系统集成，是国产替代主力；人形机器人为远期探索方向。', 'layers': ['自研控制器 / 伺服构成上游核心部件，降低对外依赖。', '工业机器人本体与系统集成商，属中游"身体"制造主体。', '运动控制与焊接等工艺软件是本体智能化关键。', '制造业自动化为基本盘（周期相关），新能源 / 汽车为重点行业。', '护城河 = 全自主产业链 + 行业 know-how；风险 = 制造业 capex 下行、价格战、人形慢。'], 'info': [('主业', '工业机器人本体'), ('优势', '全自主产业链'), ('行业', '新能源 / 汽车'), ('看点', '国产替代')], 'moat': '控制器 + 伺服 + 本体全自主闭环，构成国产工业机器人核心壁垒。', 'risks': '1）制造业资本开支下行；2）工业机器人价格战；3）人形布局兑现慢。'},
        {'slug': 'tuopu', 'name': '拓普集团', 'code': '601689', 'region': '中国', 'region_cls': 'region-cn', 'desc': '汽车底盘与执行器龙头，Tesla 机器人执行器核心供应商。', 'stats': [('执行器', '总成能力'), ('Tesla', '核心供应'), ('底盘', '汽车主业')], 'overview': '拓普集团是汽车底盘 / 内饰与执行器龙头，依托精密制造与总成能力，切入特斯拉 Optimus 旋转 / 线性执行器总成供应链。执行器是人形机器人价值量最高的环节之一；公司凭车规级制造与 Tier1 地位深度绑定头部客户，是人形机器人最纯正的"总成"标的之一。', 'layers': ['执行器内含电机 + 减速器 + 丝杠 + 传感，是上游零件集成者。', '旋转 / 线性执行器总成供应商，属中游"关节总成"核心环节。', '执行器需与控制算法匹配，是具身智能落地的硬件载体。', '汽车业务为基本盘（稳健），Tesla 机器人为高弹性增量。', '护城河 = 车规级总成 + Tier1 绑定；风险 = 单一大客户、人形进度、汽车周期。'], 'info': [('主业', '底盘 / 执行器'), ('核心', '机器人执行器'), ('绑定', 'Tesla 链'), ('看点', '总成价值量')], 'moat': '车规级执行器总成能力与头部客户深度绑定，构成关节总成壁垒。', 'risks': '1）特斯拉机器人量产不及预期；2）大客户集中；3）汽车业务周期波动。'},
        {'slug': 'sanhuayd', 'name': '三花智控', 'code': '002050', 'region': '中国', 'region_cls': 'region-cn', 'desc': '热管理全球龙头，切入机器人机电执行器。', 'stats': [('热管理', '全球龙头'), ('执行器', '机电总成'), ('Tesla', '深度绑定')], 'overview': '三花智控是热管理全球龙头（制冷控制件 / 汽车热管理），并依托机电与精密制造能力切入特斯拉 Optimus 机电执行器（如旋转关节）供应链。热管理为基本盘，机器人执行为远期增量；公司与特斯拉深度绑定，是人形机器人执行器环节重要标的。', 'layers': ['机电执行器含电机 + 传动 + 控制，公司是上游零件集成者。', '机电执行器供应商，属中游关节总成；热管理提供现金流支撑。', '执行器与控制匹配，是具身动作的执行硬件。', '制冷 / 汽车热管理为基本盘（稳健），机器人执行为增量。', '护城河 = 机电精密制造 + 客户绑定；风险 = 人形进度、单一大客户、热管理竞争。'], 'info': [('主业', '热管理 / 执行器'), ('核心', '机电执行器'), ('绑定', 'Tesla 链'), ('看点', '机电总成')], 'moat': '机电精密制造与全球客户绑定，构成执行器延伸壁垒。', 'risks': '1）特斯拉机器人量产不及预期；2）大客户集中；3）热管理价格竞争。'},
        {'slug': 'ubttech', 'name': '优必选', 'code': '', 'region': '中国香港', 'region_cls': 'region-hk', 'desc': '港股人形机器人第一股，Walker 系列本体厂。', 'stats': [('港股', '人形第一股'), ('Walker', '本体厂'), ('教育', '商用落地')], 'overview': '优必选是港股"人形机器人第一股"，主打 Walker 系列人形机器人，聚焦教育、商用服务与工业场景。公司是国内少数具备全栈人形本体研发与量产能力的企业，但当前仍处高投入亏损期，需跟踪出货量、订单与降本进度。（港股上市，财务口径与 A 股不同，本环境无法经 A 股接口取数）', 'layers': ['自研关节模组（电机 + 减速器 + 控制）构成上游核心部件能力。', '人形机器人本体厂，属中游"身体"制造与系统集成主体。', '具身智能算法（导航 / 交互 / 操作）是本体智能化核心。', '教育 / 商用服务 / 工业为落地场景，先从结构化场景切入。', '护城河 = 全栈本体 + 品牌先发；风险 = 持续亏损、出货 / 订单、人形竞争加剧。'], 'info': [('主业', '人形机器人本体'), ('上市', '港交所 09880'), ('场景', '教育 / 商用 / 工业'), ('看点', '全栈本体')], 'moat': '全栈人形本体研发与量产能力及先发品牌，构成本体厂壁垒。', 'risks': '1）持续高投入亏损；2）出货量 / 订单不及预期；3）人形赛道竞争升温。'},
        {'slug': 'tesla', 'name': 'Tesla Optimus', 'code': '', 'region': '美国', 'region_cls': 'region-us', 'desc': '全球人形机器人量产标杆，Optimus 跨层全栈。', 'stats': [('Optimus', '量产标杆'), ('跨层', '全栈自研'), ('AI', '车机同源')], 'overview': 'Tesla Optimus 是全球人形机器人量产标杆，采用"车—机器人共享 AI 栈 + 自有工厂量产"策略。执行器自研、复用汽车制造与端到端神经网络，目标把机器人做成规模品而非展品。量产爬坡与单位成本是核心观察变量。（美股上市，无 A 股代码，财务详见 Tesla 年报）', 'layers': ['自研旋转 / 线性执行器（电机 + 减速器 + 丝杠 + 传感），高度集成降本。', '本体在特斯拉工厂量产，复用汽车冲压 / 压铸 / 电驱 / 电池供应链。', '复用汽车端到端神经网络与 Dojo 训练，车—机器人共享 AI 栈。', '先在特斯拉工厂（搬运 / 分拣 / 拧螺丝）跑通，再外溢更复杂场景。', '护城河 = 制造迁移 + 数据闭环 + 自研；风险 = 量产爬坡、成本安全、竞争。'], 'info': [('主业', '人形机器人 Optimus'), ('上市', 'NASDAQ TSLA'), ('策略', '车机同源量产'), ('看点', '量产实绩')], 'moat': '汽车级制造能力迁移与车—机器人共享 AI / 数据闭环，构成独特杠杆。', 'risks': '1）从演示到经济量产的不确定性；2）成本与安全责任；3）监管与舆论；4）竞争升温。'},
        {'slug': 'nvidia', 'name': 'NVIDIA', 'code': '', 'region': '美国', 'region_cls': 'region-us', 'desc': '机器人"大脑"算力与平台供应商，Isaac / GR00T。', 'stats': [('算力', 'AI 底座'), ('Isaac', '机器人平台'), ('GR00T', '具身模型')], 'overview': 'NVIDIA 是机器人"大脑"的算力与软件平台供应商，提供 Jetson 边缘算力、Isaac 仿真训练平台与 GR00T 具身基础模型，赋能全球机器人公司。它不直接做本体，而是卖"铲子"——为人形 / 通用机器人提供训练与推理底座，是具身智能浪潮的核心卖水人。（美股上市，无 A 股代码）', 'layers': ['不直接做零件，但通过生态赋能传感器 / 算力硬件（如相机 / 模组合作）。', '不直接做本体；以算力与平台支撑本体厂研发与部署。', 'Isaac 仿真 + GR00T 具身模型是机器人"神经与思维"的训练底座。', '赋能工厂 / 服务 / 人形等全场景，降低具身智能开发门槛。', '护城河 = CUDA 生态 + 算力壁垒；风险 = 估值高、竞争（自研芯片）、地缘。'], 'info': [('主业', 'AI 算力 / 机器人平台'), ('上市', 'NASDAQ NVDA'), ('平台', 'Isaac / GR00T'), ('角色', '卖水人')], 'moat': 'CUDA 生态与算力壁垒，使其成为具身智能时代的基础设施卖水人。', 'risks': '1）估值含高预期；2）大厂自研芯片替代；3）地缘政治 / 出口管制；4）竞争。'},
    ],
}
CHAINS.append(robot)


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
<div class="stat-item"><div class="stat-num">%s</div><div class="stat-label">成分公司</div></div>
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
机器人是<b>全球概念链</b>（A股 / 港股 / 美股 / 非上市），跨市场 PE / PB <b>不可直接对比</b>；A 股成分公司的财务 / 估值经真实年报与行情快照填充，无 A 股代码的全球标的（Tesla / NVIDIA / 优必选）保留占位诚实标注。<br>
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

<div class="section-title">%s索引（成分公司 %s 家）</div>
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
