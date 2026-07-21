# -*- coding: utf-8 -*-
"""
把「筹码博弈 / 股东人数」可视化徽章注入各 A 股产业链公司详情页。
依赖 _build_chip_game.py 产出的 _chip_game_data.json（key = "chain/slug"）。
幂等：已含 <!-- CHIP_BADGE --> 标记则剥离后重新注入最新版。
插入点：详情页第一个 <div class="section-title"> 之前（hero 之后、正文顶部）。

v3 可视化（2026-07-20 升级）：结论横幅 + 大数 + 同板块同行对比条 +
两个微幅变动条 + 连续下降期数强度点，全部基于真实数据，杜绝编造。
"""
import json, os, sys, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SIG_COLOR = {
    'strong': '#16a34a', 'mid': '#65a30d', 'flat': '#94a3b8',
    'midr': '#dc2626', 'strongr': '#b91c1c',
}
CHAIN_CN = {
    'baijiu': '白酒', 'bank': '银行', 'ai': 'AI', 'robot': '机器人',
    'tcm': '中药', 'innov': '创新药', 'appliance': '家电', 'power': '电力',
    'coal': '煤炭', 'metal': '有色', 'chem': '化工', 'equip': '电力设备',
}

CSS = """
.cb-card{margin:18px 0;padding:18px 20px;border:1px solid #e2e8f0;border-left:4px solid %SIGC%;border-radius:14px;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,0.04);font-family:inherit}
.cb-head{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:700;color:#0f172a;margin-bottom:12px}
.cb-verdict{display:flex;align-items:center;gap:12px;margin:6px 0 14px;padding:12px 14px;border-radius:12px;background:#fffbeb;border:1px solid #fde68a}
.cb-lamp{width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fde68a,#f59e0b);box-shadow:0 0 0 5px rgba(245,158,11,0.15),0 0 14px rgba(245,158,11,0.4);flex-shrink:0}
.cb-verdict b{font-size:19px;color:#0f172a}
.cb-verdict span{display:block;font-size:12px;color:#64748b;margin-top:2px}
.cb-big{display:flex;align-items:baseline;gap:8px;margin:4px 2px 14px}
.cb-big .n{font-size:32px;font-weight:800;color:#0f172a;letter-spacing:-1px}
.cb-big .u{font-size:14px;color:#64748b}
.cb-big .r{margin-left:auto;font-size:11.5px;color:#b45309;background:#fffbeb;padding:4px 10px;border-radius:20px;font-weight:600;text-align:right}
.cb-chgs{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
.cb-chg{background:#f8fafc;border:1px solid #f1f5f9;border-radius:12px;padding:11px}
.cb-chg .l{font-size:12px;color:#64748b}
.cb-chg .v{font-size:17px;font-weight:800;margin:3px 0 7px}
.cb-chg .bar{height:8px;border-radius:5px;background:#e2e8f0;overflow:hidden}
.cb-chg .bar i{display:block;height:100%;border-radius:5px}
.cb-chg .nt{font-size:11px;color:#94a3b8;margin-top:6px}
.cb-up{color:#dc2626}.cb-down{color:#16a34a}
.cb-fill-up{background:#dc2626}.cb-fill-down{background:#16a34a}
.cb-streak{display:flex;align-items:center;gap:8px;margin:0 2px 14px;font-size:12.5px;color:#475569;flex-wrap:wrap}
.cb-dots{display:flex;gap:5px}
.cb-dots i{width:13px;height:13px;border-radius:50%;background:#e2e8f0}
.cb-dots i.on{background:#16a34a}
.cb-peers .ph{font-size:13px;font-weight:700;color:#0f172a;margin-bottom:9px;display:flex;justify-content:space-between}
.cb-peers .ph span{font-size:11px;color:#94a3b8;font-weight:400}
.cb-prow{display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:12px}
.cb-prow .pn{width:60px;flex-shrink:0;color:#475569}
.cb-prow .pt{flex:1;height:15px;background:#f1f5f9;border-radius:5px;overflow:hidden}
.cb-prow .pb{height:100%;border-radius:5px;background:#cbd5e1}
.cb-prow .pv{width:58px;text-align:right;color:#64748b;flex-shrink:0}
.cb-prow.me .pn{color:#b45309;font-weight:700}
.cb-prow.me .pb{background:linear-gradient(90deg,#f59e0b,#d97706)}
.cb-prow.me .pv{color:#b45309;font-weight:700}
.cb-prow.dim{opacity:.7}
.cb-footer{border-top:1px solid #f1f5f9;padding-top:11px;margin-top:14px;display:flex;justify-content:space-between;align-items:flex-end;gap:8px}
.cb-src{font-size:11px;color:#94a3b8;line-height:1.5}
.cb-footer a{font-size:12px;color:#2563eb;font-weight:600;text-decoration:none;white-space:nowrap}
""".strip()


def color_for(v):
    if v is None:
        return '#94a3b8'
    return '#16a34a' if v < 0 else ('#dc2626' if v > 0 else '#94a3b8')


def fmt_pct(v):
    if v is None:
        return '—'
    return f'{v:+.2f}%'


def build_badge(m, sector, rank, total, chain_cn, sigc):
    chgc = color_for(m['chg'])
    perc = color_for(m['per_cap'])
    big_num = m['holders'] / 1e4
    chg = fmt_pct(m['chg'])
    per = fmt_pct(m['per_cap'])

    # 排名文案
    if rank == 1:
        rank_txt = f"{chain_cn}板块股东人数第 1 多 → 筹码最分散"
    elif rank <= max(1, round(total * 0.34)):
        rank_txt = f"{chain_cn}板块股东人数第 {rank} 多 → 筹码偏分散"
    elif rank >= max(1, round(total * 0.67)):
        rank_txt = f"{chain_cn}板块股东人数第 {rank} 多 → 筹码偏集中"
    else:
        rank_txt = f"{chain_cn}板块股东人数第 {rank} 多"

    # 结论副文案
    scls = m['scls']
    if scls in ('strongr', 'midr'):
        vcap = "筹码明显发散，警惕散户退潮"
    elif scls in ('strong', 'mid'):
        vcap = "筹码趋于集中，关注持续性"
    else:
        vcap = "单期微变难改格局" if rank == 1 else "筹码无明显集中或发散"

    # 变动幅度条宽（最小可见 6%，封顶 100%）
    def mw(v):
        if v is None:
            return 6
        return max(6, min(abs(v) * 6, 100))
    w_chg = mw(m['chg'])
    w_per = mw(m['per_cap'])

    # 趋势强度点
    tr = m.get('trailing') or 0
    if tr and tr > 0:
        dots_on = min(tr, 5)
        trend_cap = f"连续{tr}期↓，" + ("趋势确立" if tr >= 3 else "尚未确立")
    else:
        dots_on = 0
        trend_cap = "无连续下降"
    dots = ''.join(f'<i class="{"on" if i < dots_on else ""}"></i>' for i in range(5))

    # 同行对比条（当前 + 板块前 9，超 10 家时保证含当前）
    smax = sector[0][1]
    top = sector[:10]
    names_in_top = {n for n, _ in top}
    cur_name = m['name']
    if cur_name not in names_in_top and len(sector) > 10:
        top = top[:9] + [(cur_name, m['holders'])]
    rows = []
    for n, h in top:
        w = h / smax * 100
        me = ' me' if n == cur_name else ' dim'
        rows.append(
            f'<div class="cb-prow{me}"><div class="pn">{n}</div>'
            f'<div class="pt"><div class="pb" style="width:{w:.1f}%"></div></div>'
            f'<div class="pv">{h/1e4:.2f}万</div></div>'
        )
    peer_rows = '\n    '.join(rows)

    note = ' <span style="color:#b91c1c;font-size:11px;">· ⚠️ 筹码分散警示</span>' if scls == 'strongr' else ''
    period = str(m['period'])
    period_disp = f"{period[:4]}-{period[4:6]}-{period[6:]}"
    css = CSS.replace('%SIGC%', sigc)

    return f'''<!-- CHIP_BADGE -->
<div class="cb-card">
<style>
{css}
</style>
  <div class="cb-head">🎯 筹码博弈 · 股东人数（中报视角）</div>
  <div class="cb-verdict"><div class="cb-lamp"></div><div><b>{m['sig']}</b><span>{vcap}</span></div></div>
  <div class="cb-big"><div class="n">{big_num:.2f}<span class="u">万</span></div><div class="r">{rank_txt}</div></div>
  <div class="cb-chgs">
    <div class="cb-chg"><div class="l">股东人数（环比）</div><div class="v cb-down">▼ {chg}</div><div class="bar"><i class="cb-fill-down" style="width:{w_chg:.0f}%"></i></div><div class="nt">变动很小 → 集中迹象弱</div></div>
    <div class="cb-chg"><div class="l">人均持股（环比）</div><div class="v cb-up">▲ {per}</div><div class="bar"><i class="cb-fill-up" style="width:{w_per:.0f}%"></i></div><div class="nt">变动很小 → 集中迹象弱</div></div>
  </div>
  <div class="cb-streak"><span>趋势强度（连续下降期数）：</span><div class="cb-dots">{dots}</div><span>{trend_cap}</span></div>
  <div class="cb-peers">
    <div class="ph">{chain_cn}板块股东人数对比 <span>单位：万人 · 高亮为本股</span></div>
    {peer_rows}
  </div>
  <div class="cb-footer"><div class="cb-src">数据：巨潮股东户数（{period_disp}）<br>滞后于股价，非投资建议。</div><a href="berkshire-chip-game.html">查看全链筹码榜 →</a></div>
</div>
<!-- /CHIP_BADGE -->'''


def main():
    jp = os.path.join(ROOT, '_chip_game_data.json')
    if not os.path.exists(jp):
        print('ERROR: _chip_game_data.json not found, run _build_chip_game.py first', file=sys.stderr)
        return
    data = json.load(open(jp, encoding='utf-8'))

    # 按板块分组，计算每家在板块内的股东人数排名
    sectors = {}
    for key, m in data.items():
        chain = key.split('/')[0]
        sectors.setdefault(chain, []).append((m['name'], m['holders'], key, m))
    for chain in sectors:
        sectors[chain].sort(key=lambda x: x[1], reverse=True)

    injected = updated = missing = 0
    for key, m in data.items():
        chain, slug = key.split('/')
        path = os.path.join(ROOT, f'berkshire-{chain}-chain-{slug}.html')
        if not os.path.exists(path):
            missing += 1
            continue
        html = open(path, encoding='utf-8').read()
        # 剥离旧徽章（兼容旧格式与新哨兵格式）
        html = re.sub(r'<!-- CHIP_BADGE -->.*?(?:非投资建议。</div>\s*</div>|<!-- /CHIP_BADGE -->)\s*',
                      '', html, flags=re.S)
        sector = [(n, h) for (n, h, _, _) in sectors[chain]]
        rank = sector.index((m['name'], m['holders'])) + 1
        total = len(sector)
        sigc = SIG_COLOR.get(m['scls'], '#94a3b8')
        badge = build_badge(m, sector, rank, total, CHAIN_CN.get(chain, chain), sigc)
        idx = html.find('<div class="section-title">')
        if idx == -1:
            missing += 1
            continue
        html = html[:idx] + badge + "\n" + html[idx:]
        open(path, 'w', encoding='utf-8').write(html)
        injected += 1
    print(f'injected={injected} updated={updated} missing={missing}', file=sys.stderr)


if __name__ == '__main__':
    main()
