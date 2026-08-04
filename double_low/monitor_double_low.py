#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
双低轮动策略 · 信号监测器
================================
目的：判断「何时该重排双低数据」。
策略是【信号触发型】而非日历型——只有当市场温度进入观察/入场区，
才需要重排候选池、更新各双低页面。本脚本拉取全市场可转债实时行情，
计算双低指标并对 5 个触发条件打分，输出信号灯。

数据源：东方财富 可转债比价表 (push2delay.eastmoney.com, 行情延迟 ~15s)
       字段 f2=转债最新价 f237=转股溢价率 f236=转股价值 f235=转股价
       双低 = 转债最新价 + 转股溢价率(%)   （与站点既有口径一致）

输出：
  - monitor_signal.json   机器可读信号灯
  - monitor.html          自包含可视化看板（数据内联，可直接部署 GitHub Pages）

用法：
  python monitor_double_low.py            # 拉实时数据 + 生成看板
  python monitor_double_low.py --quiet    # 只写 json，不打印

候选池定义（双低可投标的，透明可比对）：
  转债最新价 ∈ [95, 200] 且 转股溢价率 ≤ 80%
  排除：未上市/停牌(无价)、极端高价(>200)、极端高溢(>80%，股性尽失)
"""
import sys, os, json, ssl, urllib.request, urllib.error, statistics, datetime, argparse

# ---------- 路径 ----------
BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = BASE  # 脚本放在 double_low/ 下，直接输出到同目录
SIGNAL_JSON = os.path.join(OUT_DIR, "monitor_signal.json")
MONITOR_HTML = os.path.join(OUT_DIR, "monitor.html")

# ---------- 阈值（与站点作战手册一致）----------
TH_OBSERVE = 135.0   # 双低中位 ≤ 135 → 准备观察区
TH_ENTRY   = 125.0   # 双低中位 ≤ 125 → 入场线
TH_PCT125  = 15.0    # 双低<125 占比 ≥ 15% → 强信号

# ---------- 候选池过滤 ----------
POOL_PRICE_MIN, POOL_PRICE_MAX = 95.0, 200.0
POOL_PREM_MAX = 80.0

HOST = "https://push2delay.eastmoney.com/api/qt/clist/get"
UT = "bd1d9ddb04089700cf9c27f6f7426281"
FIELDS = ("f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,"
          "f235,f236,f237,f238,f239,f240,f241,f242,f26,f243")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Referer": "https://quote.eastmoney.com/center/fullscreenlist.html#convertible_comparison",
}


def fetch_board():
    """分页拉取 MK0354 全部可转债（push2delay 每页封顶 100）。"""
    rows = []
    for pn in range(1, 6):
        url = (f"{HOST}?pn={pn}&pz=100&po=1&np=1&ut={UT}&fltt=2&invt=2"
               f"&fid=f243&fs=b:MK0354&fields={FIELDS}")
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HDR),
                                        timeout=25, context=CTX) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            print(f"  [warn] 第{pn}页拉取失败: {e}", file=sys.stderr)
            break
        data = d.get("data") or {}
        diff = data.get("diff") or []
        if not diff:
            break
        rows.extend(diff)
        if len(diff) < 100:
            break
    return rows


def parse(rows):
    """解析为 (code, name, price, premium, double_low, convert_value)。"""
    out = []
    for x in rows:
        try:
            price = float(x.get("f2"))
            prem = float(x.get("f237"))
        except (TypeError, ValueError):
            continue  # 未上市/停牌，无价
        code = x.get("f12")
        name = x.get("f14")
        try:
            cv = float(x.get("f236"))
        except (TypeError, ValueError):
            cv = None
        out.append({
            "code": code, "name": name,
            "price": price, "premium": prem,
            "double_low": price + prem, "convert_value": cv,
        })
    return out


def in_pool(b):
    return (POOL_PRICE_MIN <= b["price"] <= POOL_PRICE_MAX) and (b["premium"] <= POOL_PREM_MAX)


def compute(rows):
    bonds = parse(rows)
    tradable = [b for b in bonds if b["price"] > 0]
    pool = [b for b in tradable if in_pool(b)]
    dl_pool = sorted(b["double_low"] for b in pool)
    dl_all = sorted(b["double_low"] for b in tradable)

    def med(lst):
        return round(statistics.median(lst), 1) if lst else None

    n125 = sum(1 for v in dl_pool if v < 125)
    n135 = sum(1 for v in dl_pool if v < 135)
    npool = len(dl_pool)
    pct125 = round(n125 / npool * 100, 1) if npool else 0.0
    pct135 = round(n135 / npool * 100, 1) if npool else 0.0

    # ----- 触发条件 -----
    # 1 双低中位 ≤ 135（准备观察区）
    med_pool = med(dl_pool)
    t_observe = (med_pool is not None) and (med_pool <= TH_OBSERVE)
    # 2 双低中位 ≤ 125（入场线）
    t_entry = (med_pool is not None) and (med_pool <= TH_ENTRY)
    # 3 双低<125 占比 ≥ 15%
    t_pct = pct125 >= TH_PCT125
    # 4 正股单月 -10%+（事件类，需人工核对）
    t_stock = None  # 人工核对
    # 5 转债规则/违约事件（事件类，需人工核对）
    t_event = None  # 人工核对

    auto_hits = [t_observe, t_entry, t_pct]
    any_auto = any(auto_hits)

    # ----- 信号等级 -----
    if t_entry or t_pct:
        level, label = "green", "可入场"
    elif t_observe:
        level, label = "yellow", "观察区"
    else:
        level, label = "red", "空仓防守"

    recommend_update = bool(any_auto)  # 任一自动触发条件命中 → 建议重排

    return {
        "checked_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": "东方财富 可转债比价表 (push2delay, 行情延迟约15秒)",
        "market": {
            "total_scanned": len(rows),
            "tradable": len(tradable),
            "candidate_pool": npool,
            "pool_def": f"价∈[{POOL_PRICE_MIN:.0f},{POOL_PRICE_MAX:.0f}] 且 溢价率≤{POOL_PREM_MAX:.0f}%",
        },
        "indicators": {
            "double_low_median": med_pool,
            "double_low_median_all": med(dl_all),
            "below_125_count": n125,
            "below_125_pct": pct125,
            "below_135_pct": pct135,
        },
        "thresholds": {"observe": TH_OBSERVE, "entry": TH_ENTRY, "pct125": TH_PCT125},
        "triggers": {
            "median_le_135": bool(t_observe),
            "median_le_125": bool(t_entry),
            "pct125_ge_15": bool(t_pct),
            "stock_monthly_down10": t_stock,   # None=人工核对
            "cb_rule_default_event": t_event,  # None=人工核对
        },
        "signal": {"level": level, "label": label},
        "recommend_update": recommend_update,
        "top_cheap": sorted(
            [{"code": b["code"], "name": b["name"], "price": b["price"],
              "premium": b["premium"], "double_low": round(b["double_low"], 1)}
             for b in pool if b["double_low"] < 130],
            key=lambda x: x["double_low"])[:15],
    }


def render_html(sig):
    lvl = sig["signal"]["level"]
    label = sig["signal"]["label"]
    ind = sig["indicators"]
    mkt = sig["market"]
    trg = sig["triggers"]
    rc = sig["recommend_update"]
    badge = {"green": "🟢", "yellow": "🟡", "red": "🔴"}[lvl]

    def tri(v):
        if v is True: return ("✅ 命中", "hit")
        if v is False: return ("⬜ 未命中", "miss")
        return ("🔍 需人工核对", "manual")

    t1 = tri(trg["median_le_135"]); t2 = tri(trg["median_le_125"])
    t3 = tri(trg["pct125_ge_15"]); t4 = tri(trg["stock_monthly_down10"])
    t5 = tri(trg["cb_rule_default_event"])

    rows_cheap = ""
    for c in sig["top_cheap"]:
        rows_cheap += (f"<tr><td>{c['code']}</td><td>{c['name']}</td>"
                       f"<td>{c['price']:.2f}</td><td>{c['premium']:.1f}%</td>"
                       f"<td><b>{c['double_low']:.1f}</b></td></tr>")

    med = ind["double_low_median"]
    med_txt = f"{med:.1f}" if med is not None else "—"
    obser = sig["thresholds"]["observe"]; entry = sig["thresholds"]["entry"]

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>双低轮动 · 信号监测</title>
<style>
  :root {{
    --bg:#0a0e1a; --card:rgba(20,28,48,.72); --line:rgba(120,160,255,.18);
    --cyan:#22d3ee; --green:#34d399; --yellow:#fbbf24; --red:#f87171;
    --blue:#60a5fa; --text:#e2e8f0; --muted:#94a3b8;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:radial-gradient(1200px 600px at 80% -10%,rgba(34,211,238,.08),transparent),var(--bg);
    color:var(--text); font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; line-height:1.65;
    padding:36px 16px 60px; }}
  .wrap {{ max-width:920px; margin:0 auto; }}
  .head {{ border-left:4px solid var(--cyan); padding:8px 18px; margin-bottom:22px; }}
  .head h1 {{ font-size:24px; }}
  .head .sub {{ color:var(--muted); font-size:12px; margin-top:6px; }}
  .signal {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
    padding:26px; text-align:center; margin-bottom:20px; box-shadow:0 8px 30px rgba(0,0,0,.35); }}
  .signal .big {{ font-size:44px; font-weight:800; letter-spacing:1px; }}
  .signal .lv-green {{ color:var(--green); }} .signal .lv-yellow {{ color:var(--yellow); }}
  .signal .lv-red {{ color:var(--red); }}
  .signal .rec {{ margin-top:12px; font-size:14px; padding:8px 14px; border-radius:20px; display:inline-block; }}
  .rec-yes {{ background:rgba(52,211,153,.18); color:var(--green); }}
  .rec-no {{ background:rgba(148,163,184,.15); color:var(--muted); }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:20px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; }}
  .card .k {{ font-size:12px; color:var(--muted); }}
  .card .v {{ font-size:26px; font-weight:700; margin-top:4px; }}
  .card .note {{ font-size:11px; color:var(--muted); margin-top:4px; }}
  .sec {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px 20px; margin-bottom:20px; }}
  .sec h2 {{ font-size:16px; margin-bottom:12px; color:var(--cyan); }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:7px 8px; border-bottom:1px solid var(--line); }}
  th {{ color:var(--muted); font-weight:600; }}
  .t-hit {{ color:var(--green); }} .t-miss {{ color:var(--muted); }} .t-manual {{ color:var(--yellow); }}
  .bar {{ height:8px; border-radius:6px; background:rgba(148,163,184,.2); position:relative; margin-top:8px; overflow:hidden; }}
  .bar > i {{ position:absolute; top:0; left:0; height:100%; background:var(--cyan); border-radius:6px; }}
  .mark {{ position:absolute; top:-3px; width:2px; height:14px; background:var(--yellow); }}
  .mark2 {{ position:absolute; top:-3px; width:2px; height:14px; background:var(--red); }}
  .how {{ font-size:13px; color:var(--muted); line-height:1.9; }}
  .how b {{ color:var(--text); }}
  footer {{ text-align:center; color:var(--muted); font-size:11px; margin-top:30px; line-height:1.8; }}
  @media(max-width:680px){{ .grid{{grid-template-columns:1fr 1fr}} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="head">
    <h1>双低轮动 · 信号监测</h1>
    <div class="sub">数据基准 {sig['checked_at']} · 来源：{sig['source']}</div>
  </div>

  <div class="signal">
    <div class="big lv-{lvl}">{badge} {label}</div>
    <div class="rec {'rec-yes' if rc else 'rec-no'}">
      {'⚠️ 触发条件命中 — 建议重排双低数据' if rc else '✓ 暂无触发 — 维持现有持仓/空仓，无需重排'}
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="k">双低中位数（候选池）</div>
      <div class="v">{med_txt}</div>
      <div class="note">观察线 {obser:.0f} · 入场线 {entry:.0f}</div>
      <div class="bar">
        <i style="width:{min(med/250*100,100):.0f}%"></i>
        <span class="mark" style="left:{obser/250*100:.0f}%"></span>
        <span class="mark2" style="left:{entry/250*100:.0f}%"></span>
      </div>
    </div>
    <div class="card">
      <div class="k">候选池数量</div>
      <div class="v">{mkt['candidate_pool']}</div>
      <div class="note">{mkt['pool_def']}</div>
    </div>
    <div class="card">
      <div class="k">双低 &lt; 125 只数</div>
      <div class="v">{ind['below_125_count']}</div>
      <div class="note">占比 {ind['below_125_pct']}% · 阈值 ≥15%</div>
    </div>
  </div>

  <div class="sec">
    <h2>触发条件清单（任一命中即重排）</h2>
    <table>
      <tr><th>条件</th><th>阈值</th><th>状态</th></tr>
      <tr><td>① 双低中位 ≤ 135</td><td>准备观察区</td><td class="t-{t1[1]}">{t1[0]}</td></tr>
      <tr><td>② 双低中位 ≤ 125</td><td>入场线</td><td class="t-{t2[1]}">{t2[0]}</td></tr>
      <tr><td>③ 双低&lt;125 占比 ≥ 15%</td><td>强信号</td><td class="t-{t3[1]}">{t3[0]}</td></tr>
      <tr><td>④ 正股单月 −10%+</td><td>可能跌出机会</td><td class="t-{t4[1]}">{t4[0]}</td></tr>
      <tr><td>⑤ 转债规则/违约事件</td><td>事件驱动</td><td class="t-{t5[1]}">{t5[0]}</td></tr>
    </table>
  </div>

  <div class="sec">
    <h2>当前最便宜的双低标的（候选池内 双低&lt;130）</h2>
    <table>
      <tr><th>代码</th><th>名称</th><th>现价</th><th>溢价率</th><th>双低</th></tr>
      {rows_cheap or '<tr><td colspan="5" style="text-align:center;color:var(--muted)">当前无 双低&lt;130 标的</td></tr>'}
    </table>
  </div>

  <div class="sec">
    <h2>怎么用（信号触发型更新）</h2>
    <div class="how">
      ① <b>何时看这个页</b>：每周扫一次，或市场大跌后顺手跑一次信号监测脚本。<br>
      ② <b>看到什么算触发</b>：信号灯变 <b>🟡观察区</b> 或 <b>🟢可入场</b>，且「建议重排」亮起 → 就该重排双低候选池、更新各双低页面了。<br>
      ③ <b>怎么重排</b>：重跑选债/轮动脚本刷新 <code>double_low_terminal.html</code> 等数据，照常部署。<br>
      ④ <b>日常空仓期</b>：信号灯 🔴空仓防守 → 不动，省去无效盯盘。<br>
      ⑤ <b>条件④⑤</b> 是事件类（正股急跌、下修/违约），脚本自动算不出，需你人工扫一眼新闻。<br>
      <span style="color:var(--muted)">注：行情来自东财延迟数据，仅作温度参考；不构成投资建议。</span>
    </div>
  </div>

  <footer>
    本页由 monitor_double_low.py 生成 · 数据内联 · 离线可读<br>
    双低 = 转债价格 + 转股溢价率(%) · 与站点其他双低页面口径一致
  </footer>
</div>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.quiet:
        print("拉取全市场可转债行情…")
    rows = fetch_board()
    if not args.quiet:
        print(f"  扫描 {len(rows)} 只，解析中…")
    sig = compute(rows)

    with open(SIGNAL_JSON, "w", encoding="utf-8") as f:
        json.dump(sig, f, ensure_ascii=False, indent=2)
    with open(MONITOR_HTML, "w", encoding="utf-8") as f:
        f.write(render_html(sig))

    if not args.quiet:
        ind = sig["indicators"]; mkt = sig["market"]
        print(f"  候选池 {mkt['candidate_pool']} · 双低中位 {ind['double_low_median']} · "
              f"<125 {ind['below_125_count']}只({ind['below_125_pct']}%)")
        print(f"  信号：{sig['signal']['label']} · 建议重排：{sig['recommend_update']}")
        print(f"  已写出 {os.path.basename(SIGNAL_JSON)} 与 {os.path.basename(MONITOR_HTML)}")
    return sig


if __name__ == "__main__":
    main()
