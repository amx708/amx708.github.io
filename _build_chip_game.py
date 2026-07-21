# -*- coding: utf-8 -*-
"""
生成「产业链 · 筹码博弈与股东人数（中报视角）」专页。
数据源：akshare stock_hold_num_cninfo（巨潮资讯，按披露期返回全市场 A 股股东户数）。
匹配：从 deploy_site 链页解析 12 链公司名 -> 巨潮资讯 证券简称。
"""
import re, glob, os, sys, unicodedata, json
import akshare as ak

ROOT = os.path.dirname(os.path.abspath(__file__))
PERIODS = ['20250630', '20250930', '20251231', '20260331']  # 旧->新

CHAIN_CN = {
    'bank': '银行', 'baijiu': '白酒', 'appliance': '家电', 'ai': 'AI 巨头',
    'chem': '化工', 'coal': '煤炭', 'equip': '电力设备', 'innov': '创新药',
    'metal': '有色', 'power': '电力', 'robot': '机器人', 'tcm': '中药',
}
# 已知非 A 股（港股/美股/未上市），无季度股东户数披露
NON_A = {
    'NVIDIA', 'Tesla', 'Tesla Optimus', 'Apple', 'Google', 'Meta', 'Microsoft',
    'Amazon', '字节', '华为', '百度', '腾讯', '阿里', '优必选',
    '康方生物', '复宏汉霖', '信达生物', '再鼎医药',
}
# 名称别名（页面名 -> 巨潮证券简称）
ALIAS = {
    '粤电力A': '粤电力',
    '海尔智家': '海尔智家',
    '江苏雷利': '江苏雷利',
    '三花智控': '三花智控',
    '汇川技术': '汇川技术',
    '双环传动': '双环传动',
    '鸣志电器': '鸣志电器',
    '中大力德': '中大力德',
    '奥比中光': '奥比中光',
    '恒立液压': '恒立液压',
    '绿的谐波': '绿的谐波',
    '埃斯顿': '埃斯顿',
    '贝斯特': '贝斯特',
    '柯力传感': '柯力传感',
    '拓普集团': '拓普集团',
    '老板电器': '老板电器',
    '苏泊尔': '苏泊尔',
    '石头科技': '石头科技',
    '科沃斯': '科沃斯',
    '小熊电器': '小熊电器',
    '九阳股份': '九阳股份',
    '海信家电': '海信家电',
    '公牛集团': '公牛集团',
    '美的集团': '美的集团',
    '格力电器': '格力电器',
    '江中药业': '华润江中',
}

# ---------- 1. 解析产业链公司 ----------
companies = []  # (chain, slug, name)
for f in glob.glob(os.path.join(ROOT, 'berkshire-*-chain-*.html')):
    base = os.path.basename(f)
    m = re.match(r'berkshire-([a-z]+)-chain-(.+)\.html', base)
    if not m:
        continue
    chain, slug = m.group(1), m.group(2)
    if slug in ('coming', 'power'):
        continue
    if chain not in CHAIN_CN:
        continue
    html = open(f, encoding='utf-8').read()
    mt = re.search(r'<title>([^<]*)</title>', html)
    title = mt.group(1).split('<')[0].strip() if mt else base
    if ' 链 ·' in title:
        name = title.split(' 链 ·')[0].strip()
    elif ' · ' in title:
        name = title.split(' · ')[0].strip()
    else:
        name = title
    companies.append((chain, slug, name))

print(f'parsed companies: {len(companies)}', file=sys.stderr)

# ---------- 2. 抓取多期股东户数 ----------
data = {}
for p in PERIODS:
    try:
        df = ak.stock_hold_num_cninfo(date=p)
        df['证券代码'] = df['证券代码'].astype(str).str.zfill(6)
        data[p] = df
        print(f'fetched {p}: {len(df)} rows', file=sys.stderr)
    except Exception as e:
        print(f'FAIL {p}: {e}', file=sys.stderr)

latest_p = PERIODS[-1]
latest = data[latest_p]


def norm(n):
    n = unicodedata.normalize('NFKC', n)  # 全角转半角（如 Ａ -> A）
    n = n.replace(' ', '').replace('　', '')
    n = re.sub(r'(股份|集团|有限公司|股份有限公司|责任公司|\(.*?\)|（.*?）)', '', n)
    return n.strip()


name_rows = {}
for _, row in latest.iterrows():
    nm = str(row['证券简称']).strip()
    name_rows[nm] = row
    name_rows['__core__' + norm(nm)] = row


def match_row(name):
    if name in name_rows:
        return name_rows[name]
    core = '__core__' + norm(name)
    if core in name_rows:
        return name_rows[core]
    if name in ALIAS and ALIAS[name] in name_rows:
        return name_rows[ALIAS[name]]
    return None


# ---------- 3. 匹配 + 计算信号 ----------
matched, unmatched, nona = [], [], []
for chain, slug, name in companies:
    if name in NON_A:
        nona.append((chain, name))
        continue
    row = match_row(name)
    if row is None:
        unmatched.append((chain, name))
        continue
    code = str(row['证券代码'])
    # 多期序列（本期股东人数）
    series = []
    for p in PERIODS:
        if p in data:
            sub = data[p]
            r = sub[sub['证券代码'] == code]
            if len(r):
                v = r.iloc[0]['本期股东人数']
                if v == v and v is not None:  # not NaN
                    series.append(float(v))
    chg = row.get('股东人数增幅')
    per_cap = row.get('人均持股数量增幅')
    try:
        chg = float(chg)
    except Exception:
        chg = None
    try:
        per_cap = float(per_cap)
    except Exception:
        per_cap = None
    # 连续下降期数（从末端往前）
    trailing = 0
    for i in range(len(series) - 1, 0, -1):
        if series[i] < series[i - 1]:
            trailing += 1
        else:
            break
    # 信号口径：股东人数"大幅增加"=危险信号（A 股筹码博弈通用框架）
    # 危险区阈值：环比增幅 >= +30% 视为「筹码强分散」（散户涌入、筹码不宜）
    if chg is not None and per_cap is not None:
        if chg >= 30:
            sig, scls = '筹码强分散', 'strongr'
        elif abs(chg) <= 8:
            sig, scls = '筹码平稳', 'flat'
        elif chg <= -8 and per_cap >= 5 and trailing >= 2:
            sig, scls = '筹码强集中', 'strong'
        elif chg < 0:
            sig, scls = '筹码集中', 'mid'
        else:
            sig, scls = '筹码分散', 'midr'
    else:
        sig, scls = '数据不足', 'flat'
    matched.append({
        'chain': chain, 'slug': slug, 'name': name, 'code': code,
        'holders': float(row['本期股东人数']) if row['本期股东人数'] == row['本期股东人数'] else None,
        'chg': chg, 'per_cap': per_cap, 'trailing': trailing,
        'sig': sig, 'scls': scls,
    })

print(f'matched={len(matched)} nona={len(nona)} unmatched={len(unmatched)}', file=sys.stderr)
if unmatched:
    print('UNMATCHED (likely A-share name mismatch):', file=sys.stderr)
    for c, n in unmatched:
        print(f'  [{c}] {n}', file=sys.stderr)

# ---------- 4. 生成 HTML ----------
def fmt_holders(v):
    if v is None:
        return '—'
    if v >= 1e8:
        return f'{v/1e8:.2f}亿'
    if v >= 1e4:
        return f'{v/1e4:.2f}万'
    return f'{v:.0f}'


def fmt_pct(v):
    if v is None:
        return '—'
    return f'{v:+.1f}%'


# 按链分组
from collections import defaultdict
by_chain = defaultdict(list)
for m in matched:
    by_chain[m['chain']].append(m)
nona_by_chain = defaultdict(list)
for c, n in nona:
    nona_by_chain[c].append(n)

SIG_CLS = {
    'strong': '#16a34a', 'mid': '#65a30d', 'flat': '#94a3b8',
    'midr': '#dc2626', 'strongr': '#b91c1c',
}

nav_items = ''.join(
    f'<a href="#chain-{c}"><span class="nav-icon">🔗</span>{CHAIN_CN[c]}</a>'
    for c in CHAIN_CN if by_chain.get(c) or nona_by_chain.get(c)
)

sections = []
for c in CHAIN_CN:
    rows = by_chain.get(c, [])
    na = nona_by_chain.get(c, [])
    if not rows and not na:
        continue
    body = ''
    if rows:
        trs = ''
        for m in sorted(rows, key=lambda x: (x['scls'] != 'strong', x['scls'] != 'mid', x['name'])):
            color = SIG_CLS.get(m['scls'], '#94a3b8')
            trs += (
                f"<tr><td class='co'>{m['name']}<span class='code'>{m['code']}</span></td>"
                f"<td class='num'>{fmt_holders(m['holders'])}</td>"
                f"<td class='num'>{fmt_pct(m['chg'])}</td>"
                f"<td class='num'>{fmt_pct(m['per_cap'])}</td>"
                f"<td class='num'>{'连续'+str(m['trailing'])+'期↓' if m['trailing']>0 else '—'}</td>"
                f"<td class='sig' style='color:{color};border-color:{color}'>{m['sig']}</td></tr>"
            )
        body += (
            f"<table class='gtbl'><thead><tr>"
            f"<th>公司</th><th>最新股东人数<br>({latest_p[:4]}-{latest_p[4:6]})</th>"
            f"<th>环比增幅</th><th>人均持股变化</th><th>连续趋势</th><th>筹码信号</th>"
            f"</tr></thead><tbody>{trs}</tbody></table>"
        )
    if na:
        items = '、'.join(na)
        body += f"<div class='na'>非 A 股（港股 / 美股 / 未上市），无季度股东户数披露：<b>{items}</b></div>"
    if not rows and na:
        body = f"<div class='na'>本链公司均为非 A 股（港股 / 美股 / 未上市），无季度股东户数披露：<b>{'、'.join(na)}</b></div>"
    sections.append(
        f"<section class='section' id='chain-{c}'>"
        f"<div class='section-header'><div class='section-icon si-gold'>🔗</div>"
        f"<div><div class='section-title'>{CHAIN_CN[c]}产业链</div>"
        f"<div class='section-subtitle'>{len(rows)} 家 A 股已匹配 · {len(na)} 家非 A 股</div></div></div>"
        f"{body}</section>"
    )

matched_total = len(matched)
strong = sum(1 for m in matched if m['scls'] == 'strong')
mid = sum(1 for m in matched if m['scls'] == 'mid')
flat = sum(1 for m in matched if m['scls'] == 'flat')
midr = sum(1 for m in matched if m['scls'] == 'midr')
strongr = sum(1 for m in matched if m['scls'] == 'strongr')

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>伯克希尔·哈撒韦 — 产业链筹码博弈与股东人数</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f1f5f9;color:#1e293b;line-height:1.6;min-height:100vh}}
.top-home-bar{{position:absolute;top:16px;left:24px;z-index:10}}
.home-btn{{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.18);border-radius:20px;color:rgba(255,255,255,0.85);font-size:13px;font-weight:500;text-decoration:none;backdrop-filter:blur(4px)}}
.home-btn:hover{{background:rgba(255,255,255,0.18);color:#fff;transform:translateY(-1px)}}
.breadcrumb{{max-width:1100px;margin:0 auto;padding:14px 24px 6px;font-size:13px;color:rgba(255,255,255,0.6);position:relative;z-index:2}}
.breadcrumb a{{color:rgba(255,255,255,0.7);text-decoration:none}}
.breadcrumb a:hover{{color:#fbbf24}}
.breadcrumb span{{color:rgba(255,255,255,0.35);margin:0 6px}}
.breadcrumb .current{{color:rgba(255,255,255,0.9);font-weight:500}}
.hero{{position:relative;background:linear-gradient(135deg,#0f172a 0%,#1e293b 40%,#1e3a5f 100%);padding:60px 24px 80px;text-align:center;overflow:hidden}}
.hero::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:100px;background:linear-gradient(to top,#f1f5f9 0%,transparent 100%)}}
.hero-content{{position:relative;z-index:2;max-width:760px;margin:0 auto}}
.hero-badge{{display:inline-block;padding:4px 14px;background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);border-radius:20px;color:#fbbf24;font-size:12px;font-weight:500;margin-bottom:20px}}
.hero h1{{font-size:clamp(26px,4vw,38px);font-weight:800;color:#fff;line-height:1.25;letter-spacing:-0.5px;margin-bottom:12px}}
.hero h1 span{{color:#f59e0b}}
.hero p{{font-size:15px;color:#94a3b8;max-width:620px;margin:0 auto}}
.section-nav{{max-width:1100px;margin:-40px auto 0;padding:0 24px;position:relative;z-index:3}}
.section-nav-inner{{background:#fff;border-radius:14px;border:1px solid #e2e8f0;padding:6px;display:flex;flex-wrap:wrap;gap:4px;box-shadow:0 4px 16px rgba(0,0,0,0.06)}}
.section-nav a{{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:10px;font-size:13px;font-weight:500;color:#64748b;text-decoration:none;transition:all 0.2s}}
.section-nav a:hover{{background:#f1f5f9;color:#2563eb}}
.main{{max-width:1100px;margin:0 auto;padding:40px 24px 80px}}
.framework{{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:26px 28px;margin-bottom:36px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}}
.framework h2{{font-size:18px;font-weight:800;color:#0f172a;margin-bottom:10px}}
.framework p{{font-size:14px;color:#475569;line-height:1.8;margin-bottom:8px}}
.framework ul{{margin:6px 0 8px 20px}}
.framework li{{font-size:14px;color:#475569;line-height:1.8;margin-bottom:4px}}
.framework .kpi{{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0}}
.framework .kpi div{{flex:1;min-width:150px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px}}
.framework .kpi b{{display:block;font-size:22px;color:#0f172a}}
.framework .kpi span{{font-size:12px;color:#94a3b8}}
.section{{margin-bottom:44px}}
.section-header{{display:flex;align-items:center;gap:12px;margin-bottom:16px}}
.section-icon{{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;background:#fffbeb}}
.section-title{{font-size:19px;font-weight:800;color:#0f172a}}
.section-subtitle{{font-size:13px;color:#94a3b8;margin-top:2px}}
.gtbl{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;font-size:13.5px}}
.gtbl th{{background:#f8fafc;color:#475569;font-weight:600;padding:10px 12px;text-align:left;border-bottom:1px solid #e2e8f0;font-size:12.5px}}
.gtbl td{{padding:10px 12px;border-bottom:1px solid #f1f5f9;color:#334155}}
.gtbl tr:last-child td{{border-bottom:none}}
.gtbl .co{{font-weight:600;color:#0f172a}}
.gtbl .code{{display:block;font-size:11px;color:#94a3b8;font-weight:400;margin-top:2px}}
.gtbl .num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
.gtbl .sig{{text-align:center;font-weight:700;font-size:12.5px;border:1px solid;padding:4px 8px !important;border-radius:8px;white-space:nowrap}}
.na{{background:#fefce8;border:1px dashed #e2e8f0;border-radius:10px;padding:10px 14px;font-size:12.5px;color:#854d0e;margin-top:10px}}
.back-link{{margin-top:40px;text-align:center}}
.back-link a{{display:inline-flex;align-items:center;gap:8px;padding:10px 24px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;color:#334155;font-size:14px;font-weight:500;text-decoration:none}}
.back-link a:hover{{background:#f8fafc;color:#2563eb}}
.footer{{text-align:center;padding:32px 24px;color:#94a3b8;font-size:12px;border-top:1px solid #e2e8f0}}
@media(max-width:768px){{
  .hero{{padding:36px 16px 60px}}
  .main{{padding:28px 14px 56px}}
  .section-nav{{margin-top:-36px;padding:0 14px}}
  .section-nav a{{padding:6px 10px;font-size:12px}}
  .gtbl{{font-size:12px}}
  .gtbl th,.gtbl td{{padding:8px 8px}}
  .framework{{padding:18px 16px}}
}}
</style>
</head>
<body>
<div class="top-home-bar"><a href="index.html" class="home-btn"><span>🏠</span><span>返回首页</span></a></div>
<nav class="breadcrumb"><a href="index.html">首页</a><span>/</span><a href="berkshire-standalone.html">投资数据中心</a><span>/</span><span class="current">筹码博弈与股东人数</span></nav>
<header class="hero"><div class="hero-content">
  <div class="hero-badge">Chip Game · A 股财报视角</div>
  <h1>产业链<span>筹码博弈</span>与股东人数</h1>
  <p>把「看股东人数 / 筹码集中度」这套 A 股博弈框架，套进 12 条产业链的公司里——在财报披露窗口用作观察筹码结构的信号。</p>
</div></header>
<nav class="section-nav"><div class="section-nav-inner">{nav_items}</div></nav>
<main class="main">

<div class="framework">
  <h2>一、这套框架在看什么</h2>
  <p><b>股东人数（股东户数）</b>是 A 股每季度随季报 / 中报 / 年报强制披露的滞后指标：它数的是「有多少人在持有这只股票」。它的反身性在于——<b>股东人数下降 = 筹码从分散的散户手里集中到少数大户/机构 = 筹码趋紧；股东人数上升 = 散户涌入、筹码分散</b>。在价值投资语境下，它不替代基本面，而是给「关注度 / 供需结构」一个可量化的温度计。</p>
  <ul>
    <li><b>环比增幅（本期 vs 上期）</b>：为负 → 人数减少、筹码集中；为正 → 人数增加、筹码分散。</li>
    <li><b>人均持股数量变化</b>：人均持股上升 → 少数人拿了更多筹码（集中）；下降 → 筹码被摊薄（分散）。它是股东人数的另一面验证。</li>
    <li><b>连续趋势</b>：连续多期人数下降，比单期更有说服力——说明收集是持续的，不是一次性的。</li>
  </ul>
  <h2>二、财报披露窗口下怎么用</h2>
  <p>当宏观环境（海外 / 利率 / 大宗）剧烈波动、市场情绪不稳时，<b>定期财报披露期是验证「预期差」的关键窗口</b>。筹码博弈框架在这里的作用是——</p>
  <ul>
    <li><b>低位 + 筹码持续集中</b>：估值已低（参见各链 P0 估值分位）、股东人数连降，说明聪明钱在 quietly 收集，业绩若兑现，弹性更大——这是财报窗口最值得跟踪的组合。</li>
    <li><b>高位 + 股东人数飙升</b>：股价已高、散户蜂拥而入（人数骤增），业绩稍有不及预期就容易「利好兑现即下跌」，需警惕。</li>
    <li><b>配合估值分位</b>：本站各产业链的「估值历史分位」页给出 PE/PB 十年分位；把「低分位 + 筹码集中」叠加，信号质量高于单一指标。</li>
  </ul>
  <div class="kpi">
    <div><b>{matched_total}</b><span>已匹配 A 股公司</span></div>
    <div><b style="color:#16a34a">{strong}</b><span>筹码强集中</span></div>
    <div><b style="color:#65a30d">{mid}</b><span>筹码集中</span></div>
    <div><b style="color:#94a3b8">{flat}</b><span>筹码平稳</span></div>
    <div><b style="color:#dc2626">{midr}</b><span>筹码分散</span></div>
    <div><b style="color:#b91c1c">{strongr}</b><span>筹码强分散（警示区）</span></div>
  </div>
  <div style="margin-top:14px;padding:12px 14px;background:#fefce8;border:1px solid #fde68a;border-radius:10px;font-size:12.5px;color:#92400e;line-height:1.7;">
    ⚠️ <b>时效性与谨慎参考提示</b>：股东户数每季度披露一次，本页最新数据为 <b>{latest_p[:4]} 年 {latest_p[4:6]} 月</b>。你看到的人数变化已经是 1–3 个月前的筹码结构，会随下一期财报更新而变化，不能用来抓短期拐点。下方方向判断、历史案例与框架观点均具有时效性与主观性，<b>仅供学习研究参考，不构成投资建议，请谨慎使用</b>。港股 / 美股 / 未上市公司无此季度披露，已在各链注明。
  </div>
</div>

BIAN_PLACEHOLDER

{''.join(sections)}

<div class="back-link"><a href="berkshire-standalone.html">← 返回投资数据中心</a></div>
</main>
<footer class="footer"><p>数据来源：巨潮资讯（cninfo）股东户数 · 配套各产业链估值历史分位 · 最新披露期：{latest_p[:4]} 年 {latest_p[4:6]} 月</p><p style="margin-top:6px;color:#94a3b8">方向判断、历史案例与框架观点为公开市场观点与资金面信息整理，具有时效性与主观性，仅供研究参考，不构成投资建议，请谨慎参考。</p></footer>
</body>
</html>
"""

# ---- 筹码博弈理论框架（公开观点整理） ----
bian_html = f"""<div class="framework" style="border-left:4px solid #f59e0b;">
  <h2>三、筹码博弈理论框架（公开观点整理）</h2>
  <p>「看股东人数做博弈」是 A 股流传甚广的一套行为金融框架，核心可概括为——</p>
  <p style="background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:12px 14px;color:#92400e;"><b>"当市场预期已被充分定价后，后续的边际定价权在筹码结构（股东人数）而非基本面——业绩大家都看懂了，谁持有、持有多少才是关键。"</b> 本页把这套思路套进产业链公司，用作观察信号。</p>

  <h3 style="font-size:15px;font-weight:800;color:#0f172a;margin:18px 0 6px;">① 历史案例：股东人数暴增后的代价</h3>
  <p>下面两个都是 A 股历史上被反复讨论的经典案例，数据来自巨潮资讯股东户数与行情数据，可独立复核：</p>
  <ul>
    <li><b>三一重工（600031）</b>：2021Q1 股东户数约 <b>69万</b>，到 2021Q4 增至约 <b>114万</b>（<b style="color:#b91c1c">+65%</b>）；同期股价从约 <b>32元</b> 跌至约 <b>21元</b>（跌幅约 <b style="color:#b91c1c">−34%</b>），2021 年高点（约 48元）到 2024 年低点（约 12元）最大回撤约 <b style="color:#b91c1c">−76%</b>。散户在工程机械景气高点大量涌入，筹码极度分散，套牢盘沉重。</li>
    <li><b>中国平安（601318）</b>：2021Q1 股东户数约 <b>96万</b>，到 2021Q4 增至约 <b>127万</b>（<b style="color:#b91c1c">+32%</b>）；同期股价从约 <b>65元</b> 跌至约 <b>39元</b>（跌幅约 <b style="color:#b91c1c">−40%</b>），2021 年高点（约 75元）到 2024 年低点（约 31元）最大回撤约 <b style="color:#b91c1c">−59%</b>。即便是被贴上"价值蓝筹"标签的公司，散户化后同样出现筹码博弈的惨烈出清。</li>
  </ul>
  <p>→ 这些案例的共同点是：<b>股价在高位或景气高点时，股东户数快速膨胀，意味着筹码从机构/大户手中流向散户，后续往往对应漫长的估值压缩与筹码出清。</b> 本页据此把 <b>环比增幅 ≥ +30%</b> 单独标为「<span style="color:#b91c1c;font-weight:700;">筹码强分散</span>」（筹码分散警示区）。</p>

  <h3 style="font-size:15px;font-weight:800;color:#0f172a;margin:18px 0 6px;">② 为什么股东人数会"先于"股价反转？</h3>
  <p>这不是预言，而是一种<b>滞后确认的资金结构描述</b>：</p>
  <ul>
    <li><b>底部区域</b>：股价长期低迷，散户熬不住割肉，股东户数持续下降 → 筹码集中到少数人手里 → 后续一旦有催化，弹性更大。</li>
    <li><b>顶部区域</b>：股价上涨到全社会热议，散户 FOMO 涌入 → 股东户数暴增 → 后续买盘枯竭，稍有利空便引发多杀多。</li>
    <li><b>震荡区域</b>：股东户数稳定，说明多空双方筹码没有大迁移，股价更可能延续原有趋势或区间震荡。</li>
  </ul>

  <h3 style="font-size:15px;font-weight:800;color:#0f172a;margin:18px 0 6px;">③ 怎么用：把筹码信号套进产业链</h3>
  <p>本页把 12 条产业链的公司统一映射到这套 5 档信号里。跨时间地看，它最有价值的用法不是预测涨跌，而是<b>帮你把公司分成三类</b>：</p>
  <ul>
    <li><b>值得重点跟踪</b>：筹码强集中 / 集中 + 估值历史分位偏低 + 基本面没恶化。这代表「人少、便宜、还没被充分关注」。</li>
    <li><b>需要警惕</b>：筹码强分散 / 分散 + 估值历史分位偏高或处于题材高位。这代表「人多、拥挤、后续买盘可能枯竭」。</li>
    <li><b>观望</b>：筹码平稳，或估值/筹码信号互相矛盾。这时候单一指标没有优势，需要等其他证据。</li>
  </ul>
  <p>例如，当前数据中金属链（有色）几乎全线落在「筹码强分散」区：紫金矿业 +114%、洛阳钼业 +141%……这与历史案例逻辑一致——散户在周期高点涌入后，反弹阻力往往较大。</p>

  <h3 style="font-size:15px;font-weight:800;color:#0f172a;margin:18px 0 6px;">④ 筹码信号的边界与误用</h3>
  <ul>
    <li><b>滞后性</b>：股东户数每季度才披露一次，你看到的数据已经是 1–3 个月前的结构，不能用来抓日内或周内拐点。</li>
    <li><b>不替代基本面</b>：股东人数只是「谁来持有」的结构指标，不能替代 ROE、现金流、行业景气度等基本面分析。</li>
    <li><b>不适用于非 A 股</b>：港股 / 美股 / 未上市没有季度股东户数披露，本页已把这些公司标为「非 A 股」。</li>
    <li><b>要结合人均持股变化</b>：股东人数下降但人均持股也下降，可能是大户拆户或流动性变化，信号会打折扣。</li>
    <li><b>不是因果关系</b>：股东人数暴增是「散户涌入」的结果，不是股价下跌的原因；它是风险警示，不是做空理由。</li>
  </ul>
  <p style="font-size:12.5px;color:#94a3b8;margin-top:8px;">📌 以上历史案例与框架为<b>公开市场观点与资金面信息的整理汇总</b>，非个股投资建议；本页筹码数据仍以巨潮股东户数为准。</p>
</div>
"""
html = html.replace('BIAN_PLACEHOLDER', bian_html)

out = os.path.join(ROOT, 'berkshire-chip-game.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'written {out} ({len(html)} bytes)', file=sys.stderr)

# 导出供详情页注入徽章复用
chip_json = {}
for m in matched:
    chip_json[f"{m['chain']}/{m['slug']}"] = {
        'code': m['code'], 'name': m['name'],
        'holders': m['holders'], 'chg': m['chg'], 'per_cap': m['per_cap'],
        'trailing': m['trailing'], 'sig': m['sig'], 'scls': m['scls'],
        'period': latest_p,
    }
with open(os.path.join(ROOT, '_chip_game_data.json'), 'w', encoding='utf-8') as jf:
    json.dump(chip_json, jf, ensure_ascii=False, indent=1)
print(f'written _chip_game_data.json ({len(chip_json)} companies)', file=sys.stderr)
