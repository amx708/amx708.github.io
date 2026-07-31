# -*- coding: utf-8 -*-
"""为「涨价逻辑监测清单」中 44 家缺失 co 页的标的，批量补建富集版「数据采集页」。

数据(沙箱可用，非东方财富)：
  - akshare.stock_financial_abstract_ths  -> 营业总收入/净利润/销售毛利率/净资产收益率/资产负债率/每股经营现金流(年报)
  - akshare.stock_zh_valuation_baidu      -> PE(TTM)/PB 近十年序列(算当前分位)
  - 腾讯行情 qt.gtimg.cn                  -> 总市值(亿)/现价
  - akshare.stock_fhps_detail_ths         -> 分红方案，结合现价算股息率

产出：
  - deploy_site/berkshire-commodity-co-<code>.html  （44 个，富集版：财务快照 + 估值分位 + 七大师视角 + 安全边际 + 结论合成）
  - _wl_co_changed.txt （改动清单，供部署器串行推送；每行一个 deploy_site 相对路径）

页面风格对齐框架 co 页（蓝主题 / 财务快照 snap / 估值历史分位 valband / 七位大师视角 masters-view / 安全边际量化线 / 结论合成）。
"""
import os, re, sys, json, warnings, urllib.request, time
warnings.filterwarnings("ignore")
import akshare as ak

DS = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-08-01"
SLUG = "commodity"
CHAIN_NAME = "涨价逻辑受益"

# (code, name) —— 44 家缺失（已与现有 co 页去重）
MISSING = [
    ("000060", "中金岭南"), ("000426", "兴业银锡"), ("000505", "京粮控股"),
    ("000603", "盛达资源"), ("000655", "金岭矿业"), ("000683", "远兴能源"),
    ("000751", "锌业股份"), ("000911", "南宁糖业"), ("000923", "河钢资源"),
    ("000933", "神火股份"), ("000960", "锡业股份"), ("000983", "山西焦煤"),
    ("002001", "新和成"), ("002092", "中泰化学"), ("002221", "东华能源"),
    ("002340", "格林美"), ("002460", "赣锋锂业"), ("002466", "天齐锂业"),
    ("002601", "龙佰集团"), ("002648", "卫星化学"), ("002852", "道道全"),
    ("300208", "青岛中程"), ("600075", "新疆天业"), ("600188", "兖矿能源"),
    ("600216", "浙江医药"), ("600359", "新农开发"), ("600426", "华鲁恒升"),
    ("600497", "驰宏锌锗"), ("600500", "中化国际"), ("600531", "豫光金铅"),
    ("600540", "新赛股份"), ("600546", "山煤国际"), ("600598", "北大荒"),
    ("600618", "氯碱化工"), ("600691", "阳煤化工"), ("600711", "盛屯矿业"),
    ("600722", "金牛化工"), ("600737", "中粮糖业"), ("600989", "宝丰能源"),
    ("601088", "中国神华"), ("601118", "海南橡胶"), ("601168", "西部矿业"),
    ("603969", "海南矿业"), ("603993", "洛阳钼业"),
]

# 从 watchlist 取每家公司对应的涨价品种 + 弹性备注，用于「公司概述」
def load_watch_context():
    p = os.path.join(DS, "..", "涨价逻辑监测系统", "watchlist.json")
    ctx = {}
    if not os.path.exists(p):
        return ctx
    wl = json.load(open(p, encoding="utf-8"))
    for prod in wl["products"]:
        for c in prod["companies"]:
            e = ctx.setdefault(c["code"], {"name": c["name"], "prods": [], "notes": []})
            e["prods"].append(prod["name"])
            e["notes"].append(c.get("note", ""))
    return ctx

WATCH = load_watch_context()


def retry(fn, n=3, wait=1.5):
    for i in range(n):
        try:
            return fn()
        except Exception:
            if i == n - 1:
                raise
            time.sleep(wait)


# ---------- 数值解析 ----------
def col(df, *keys):
    for k in keys:
        for c in df.columns:
            if c == k or k in c:
                return c
    return None

def num(x):
    if x is None:
        return None
    s = str(x).replace(",", "")
    m = re.search(r"-?\d+\.?\d*", s)
    return float(m.group()) if m else None

def to_yi(x):
    if x is None:
        return None
    s = str(x).replace(",", "")
    m = re.search(r"-?\d+\.?\d*", s)
    if not m:
        return None
    v = float(m.group())
    if "万" in s:
        return v / 1e4
    return v

def pick_annual(df):
    if "报告期" in df.columns:
        ann = df[df["报告期"].astype(str).str.endswith("12-31")]
        if len(ann):
            return ann.iloc[-1]
    return df.iloc[-1]


# ---------- 数据抓取 ----------
def fetch_fin(code):
    df = ak.stock_financial_abstract_ths(symbol=code)
    row = pick_annual(df)
    rev_c = col(df, "营业总收入")
    np_c = col(df, "净利润")
    gm_c = col(df, "销售毛利率")
    roe_c = col(df, "净资产收益率")
    debt_c = col(df, "资产负债率")
    eps_c = col(df, "基本每股收益")
    cfps_c = col(df, "每股经营现金流")
    rev = to_yi(row[rev_c]) if rev_c else None
    npv = to_yi(row[np_c]) if np_c else None
    gm = num(row[gm_c]) if gm_c else None
    roe = num(row[roe_c]) if roe_c else None
    debt = num(row[debt_c]) if debt_c else None
    eps = num(row[eps_c]) if eps_c else None
    cfps = num(row[cfps_c]) if cfps_c else None
    ocf = None
    if cfps is not None and npv is not None and eps not in (None, 0):
        ocf = cfps * npv / eps
    if npv is not None and rev is not None and (npv > rev or npv < -rev):
        npv = None
    if ocf is not None and rev is not None and abs(ocf) > rev * 5:
        ocf = None
    fy = str(row["报告期"])[:4] if "报告期" in df.columns else "2025"
    return dict(rev=rev, npv=npv, gm=gm, roe=roe, debt=debt, ocf=ocf, fy=fy)


def fetch_pepb(code):
    out = {"pe": None, "pb": None, "pe_pct": None, "pb_pct": None}
    for ind, key in [("市盈率(TTM)", "pe"), ("市净率", "pb")]:
        try:
            d = ak.stock_zh_valuation_baidu(symbol=code, indicator=ind, period="近十年")
            if len(d):
                vals = d["value"].astype(float)
                cur = float(vals.iloc[-1])
                lo, hi = vals.min(), vals.max()
                pct = (cur - lo) / (hi - lo) * 100 if hi > lo else 0.0
                out[key] = cur
                out[key + "_pct"] = round(pct, 1)
        except Exception:
            pass
    return out


def fetch_mv_price(code):
    pre = "sh" if code.startswith(("6", "9")) else "sz"
    url = "https://qt.gtimg.cn/q=%s%s" % (pre, code)
    s = urllib.request.urlopen(url, timeout=15).read().decode("gbk")
    f = s.split("~")
    return float(f[45]) if len(f) > 45 and f[45] not in ("", "--") else None, \
           float(f[3]) if len(f) > 3 and f[3] not in ("", "--") else None


def fetch_dividend_yield(code, price):
    if price in (None, 0):
        return None
    dd = ak.stock_fhps_detail_ths(symbol=code)
    if dd is None or not len(dd):
        return None
    plan_c = col(dd, "分红方案说明")
    prog_c = col(dd, "方案进度")
    if plan_c is None:
        return None
    best = None
    for _, r in dd.iterrows():
        plan = str(r[plan_c])
        prog = str(r[prog_c]) if prog_c else ""
        if "派" in plan and ("实施" in prog or "实施" in plan):
            m = re.search(r"派([\d.]+)元", plan)
            if m:
                x = float(m.group(1))          # 每10股派 X 元
                dps = x / 10.0
                cand = (str(r.get("报告期", "")), dps)
                if best is None or cand[0] > best[0]:
                    best = cand
    if best is None:
        return None
    return round(best[1] / price * 100, 2)


# ---------- 格式化 ----------
def f2(x):
    return ("%.2f" % x) if isinstance(x, (int, float)) else "待采集"


def pct_class(p):
    if p is None:
        return ("#64748b", "na")
    if p < 20:
        return ("#16a34a", "lo")
    if p > 80:
        return ("#dc2626", "hi")
    return ("#b45309", "mid")


# ---------- 页面拼装 ----------
CSS = """<style>
:root{--bg:#f5f9ff;--soft:#eef5ff;--card:#fff;--ink:#0f172a;--mut:#475569;--line:rgba(59,130,246,.15);--red:#dc2626;--green:#16a34a;--accent:#2563eb;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(180deg,#f8fbff 0%,#f0f7ff 100%);background-attachment:fixed;color:var(--ink);line-height:1.7;font-size:15px}
.topbar{position:sticky;top:0;z-index:50;background:rgba(11,31,58,.82);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08);color:#fff}
.topbar-in{max-width:1080px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.brand{font-weight:800;font-size:17px}.brand .ac{color:#f5a623}
.crumb{font-size:13px;color:#9fb2cf}.crumb a{color:#9fb2cf;text-decoration:none}.crumb a:hover{color:#f5a623}
.detail{max-width:920px;margin:0 auto;padding:28px 20px 70px}
.detail .back{color:var(--accent);text-decoration:none;font-size:13px}
.detail>h1{font-weight:700;letter-spacing:-.5px;margin:10px 0 2px}
.hero-sub{color:var(--mut);margin:0 0 6px;font-size:14px}
.section-title{font-size:18px;font-weight:700;margin:34px 0 16px;padding-left:12px;border-left:4px solid var(--accent);color:var(--ink)}
.note{background:var(--soft);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:12px 16px;margin:14px 0;font-size:13px;color:var(--mut);line-height:1.65}
.snap{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:16px 0}
.snap div{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:12px 10px;text-align:center}
.snap b{display:block;font-size:19px;color:var(--accent);font-weight:700}
.snap span{font-size:11px;color:var(--mut)}
.valband{margin:6px 0 2px}
.vrow{display:flex;align-items:center;gap:12px;margin:11px 0}
.vlab{width:78px;font-size:13px;font-weight:600;color:#334155;flex-shrink:0}
.vbar{position:relative;flex:1;height:12px;background:#f1f5f9;border-radius:6px;overflow:hidden}
.vfill{height:100%;border-radius:6px}
.vmark{position:absolute;top:-3px;width:3px;height:18px;background:#0f172a;border-radius:2px;transform:translateX(-50%)}
.vval{width:260px;font-size:12.5px;color:#475569;flex-shrink:0;text-align:right}
.vval b{color:#0f172a}
.vtag{font-weight:700;margin-left:4px}
.ovw{background:#eef5ff;border:1px solid rgba(59,130,246,.15);border-left:3px solid #2563eb;border-radius:8px;padding:12px 16px;margin:14px 0;font-size:13px;color:#475569;line-height:1.65}
.mv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.mv-card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;position:relative;overflow:hidden;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.mv-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent),#60a5fa)}
.mv-h{display:flex;align-items:baseline;gap:8px;margin:0 0 2px}
.mv-h b{font-size:15px;color:var(--ink)}
.mv-h .en{font-size:11px;color:#94a3b8;font-weight:500}
.mv-tag{font-size:11px;color:#1d4ed8;background:#eff6ff;border:1px solid rgba(59,130,246,.18);padding:2px 9px;border-radius:20px;display:inline-block;margin:4px 0 8px;font-weight:600}
.mv-read{font-size:12.5px;color:#334155;line-height:1.7;margin:6px 0}
.mv-read b{color:#0f172a}
.mv-q{font-size:12.5px;color:#475569;background:#f8fafc;border-radius:8px;padding:8px 10px;margin:8px 0;line-height:1.6}
.mv-q .lab{color:#b45309;font-weight:700}
.mg-viz{display:flex;flex-direction:column;gap:12px;margin:6px 0 10px}
.mg-row{display:grid;grid-template-columns:90px 1fr 130px;gap:10px;align-items:center;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 12px}
.mg-label{font-size:12px;color:#0f172a;font-weight:600;line-height:1.3}
.mg-val{font-size:13px;color:#64748b;font-weight:500}
.mg-track{position:relative;height:10px;background:#f1f5f9;border-radius:5px;overflow:visible}
.mg-bar{height:100%;background:#94a3b8;border-radius:5px;position:relative}
.mg-thr{position:absolute;top:-4px;width:2px;height:18px;background:#0f172a}
.mg-meta{display:flex;flex-direction:column;gap:3px;align-items:flex-end}
.mg-status{font-size:12px;font-weight:600;padding:2px 8px;border-radius:6px}
.mg-on{background:#dcfce7;color:#166534}.mg-off{background:#fef3c7;color:#92400e}.mg-na{background:#f1f5f9;color:#64748b}
.synth-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:15px 17px;margin:6px 0 14px;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.synth-tbl{width:100%;border-collapse:collapse;font-size:13px}
.synth-tbl td{border-bottom:1px solid #f1f5f9;padding:7px 8px;vertical-align:top;color:#334155}
.synth-tbl td.ax{color:#0f172a;font-weight:700;width:140px;white-space:nowrap}
.synth-verdict{margin-top:10px;padding:9px 12px;background:#f8fafc;border-left:3px solid #a8a29e;border-radius:6px;font-size:13px;line-height:1.6;color:#1e293b}
.fin-note{font-size:11.5px;color:#64748b;margin-top:8px;line-height:1.55}
footer{background:var(--soft);color:var(--mut);text-align:center;padding:26px 20px;font-size:12.5px;border-top:1px solid var(--line);margin-top:30px}
@media(max-width:600px){.mv-grid{grid-template-columns:1fr}.vval{width:auto}.mg-row{grid-template-columns:80px 1fr}.mg-meta{width:100px}}
</style>"""


def build_page(code, name, fin, pepb, mv, price, dy, ctx):
    fy = fin.get("fy", "2025")
    # snap
    snap = (
        f'<div><b>{f2(fin["rev"])}</b><span>营收(亿)</span></div>'
        f'<div><b>{f2(fin["npv"])}</b><span>归母净利(亿)</span></div>'
        f'<div><b>{f2(fin["gm"])}</b><span>毛利率(%)</span></div>'
        f'<div><b>{f2(fin["roe"])}</b><span>ROE(%)</span></div>'
        f'<div><b>{f2(fin["debt"])}</b><span>负债率(%)</span></div>'
        f'<div><b>{f2(fin["ocf"])}</b><span>经营现金流(亿)</span></div>'
        f'<div><b>{f2(mv)}</b><span>总市值(亿)</span></div>'
        f'<div><b>{f2(pepb.get("pe"))}</b><span>PE</span></div>'
        f'<div><b>{f2(pepb.get("pb"))}</b><span>PB</span></div>'
        f'<div><b>{f2(dy)}</b><span>股息率(%)</span></div>'
    )
    # 估值历史分位
    def vrow(label, cur, pct):
        if cur is None:
            return (f'<div class="vrow"><div class="vlab">{label}</div>'
                    f'<div class="vbar"><div class="vfill" style="width:0%;background:#cbd5e1"></div></div>'
                    f'<div class="vval">待采集</div></div>')
        color, cls = pct_class(pct)
        tag = {"lo": "低·便宜", "mid": "中", "hi": "高·贵", "na": ""}[cls]
        return (f'<div class="vrow"><div class="vlab">{label}</div>'
                f'<div class="vbar"><div class="vfill" style="width:{pct:.1f}%;background:{color}"></div>'
                f'<div class="vmark" style="left:{pct:.1f}%"></div></div>'
                f'<div class="vval"><b>{cur:.2f}</b> · 近十年分位 <span class="vtag" style="color:{color}">{pct:.1f}%</span> {tag}</div></div>')
    valband = vrow("PE（TTM）", pepb.get("pe"), pepb.get("pe_pct")) + vrow("PB", pepb.get("pb"), pepb.get("pb_pct"))

    pe_pct = pepb.get("pe_pct"); pb_pct = pepb.get("pb_pct")
    # 安全边际线
    def mg_row(label, val, thr, low_is_safe=True, unit="%"):
        if val is None:
            return (f'<div class="mg-row"><div class="mg-label">{label}<br><span class="mg-val">—</span></div>'
                    f'<div class="mg-track"><div class="mg-bar" style="width:0%"></div></div>'
                    f'<div class="mg-meta"><span class="mg-status mg-na">待采集</span></div></div>')
        triggered = (val <= thr) if low_is_safe else (val >= thr)
        cls = "mg-on" if triggered else "mg-off"
        status = "已触发" if triggered else "未触发"
        w = min(100.0, max(0.0, val if unit == "%" else val / 100.0 * 100)) if unit == "%" else min(100.0, val)
        return (f'<div class="mg-row"><div class="mg-label">{label}<br><span class="mg-val">{val:.1f}{unit}</span></div>'
                f'<div class="mg-track"><div class="mg-bar" style="width:{w:.1f}%"></div>'
                f'<div class="mg-thr" style="left:{thr:.1f}%"></div></div>'
                f'<div class="mg-meta"><span class="mg-status {cls}">{status}</span>'
                f'<span class="mg-note">阈值 {thr:.1f}{unit}</span></div></div>')
    mg = (mg_row("PE分位", pe_pct, 20.0) + mg_row("PB分位", pb_pct, 20.0)
          + mg_row("股息率线", dy, 3.1, low_is_safe=False, unit="%"))

    # 结论合成
    strong = (fin.get("roe") or 0) >= 15
    cheap = (pe_pct is not None and pe_pct < 20) or (pb_pct is not None and pb_pct < 20)
    if cheap and strong:
        verdict = "便宜的好生意（估值低 + 护城河强），安全边际充足"
    elif cheap and not strong:
        verdict = "警惕价值陷阱（估值低但 ROE 偏弱，需辨真伪）"
    elif (not cheap) and strong:
        verdict = "贵的好生意（护城河强但估值不便宜，宜等回调）"
    else:
        verdict = "中性 / 数据不足（估值与护城河均未显优势）"
    synth = (f'<table class="synth-tbl"><tr><td class="ax">护城河质量</td><td>{"强（ROE≥15%）" if strong else "弱 / 中性（ROE<15%）"}　·　ROE {f2(fin.get("roe"))}%</td></tr>'
             f'<tr><td class="ax">估值便宜度</td><td>{"便宜" if cheap else "不便宜 / 中性"}　·　PE分位 {f2(pe_pct)}% / PB分位 {f2(pb_pct)}%</td></tr>'
             f'<tr><td class="ax">现金回报</td><td>股息率 {f2(dy)}%</td></tr></table>'
             f'<div class="synth-verdict"><b>综合结论：</b>{verdict}。　本段为<b>机械合成</b>（护城河×估值透明规则），<b>非研究结论、不构成投资建议</b>。</div>')

    # 七位大师视角
    roe = f2(fin.get("roe")); debt = f2(fin.get("debt")); gm = f2(fin.get("gm"))
    pe = f2(pepb.get("pe")); pb = f2(pepb.get("pb")); mvv = f2(mv); dyy = f2(dy); rev = f2(fin.get("rev")); ocf = f2(fin.get("ocf"))
    masters = f"""
<div class="mv-grid">
<div class="mv-card"><div class="mv-h"><b>沃伦·巴菲特</b><span class="en">Buffett</span></div>
<div class="mv-tag">护城河 · 所有者收益 · 安全边际</div>
<div class="mv-read">ROE <b>{roe}</b>　负债率 <b>{debt}</b>　经营现金流 <b>{ocf}亿</b>　股息率 <b>{dyy}</b></div>
<div class="mv-q"><span class="lab">透镜：</span>这是「好生意 × 好价格」的闭环吗？护城河能否抵御竞争、价格是否低于内在价值？</div></div>
<div class="mv-card"><div class="mv-h"><b>查理·芒格</b><span class="en">Munger</span></div>
<div class="mv-tag">逆向 · 多元模型 · 避免愚蠢</div>
<div class="mv-read">负债率 <b>{debt}</b>（杠杆脆弱性）　ROE <b>{roe}</b>（盈利质量）</div>
<div class="mv-q"><span class="lab">invert：</span>什么情景下会永久损失资本？别被近 12 个月走势锚定。</div></div>
<div class="mv-card"><div class="mv-h"><b>段永平</b><span class="en">Duan</span></div>
<div class="mv-tag">买公司 · 本分 · 治理诚信</div>
<div class="mv-read">股息率 <b>{dyy}</b>（分红真实性代理）　负债率 <b>{debt}</b>（财务稳健）　ROE <b>{roe}</b></div>
<div class="mv-q"><span class="lab">透镜：</span>这是不是一门你真看得懂的生意？大股东占款/关联交易/审计意见如何？</div></div>
<div class="mv-card"><div class="mv-h"><b>李录</b><span class="en">Li Lu</span></div>
<div class="mv-tag">结构性机会 · 长期复利</div>
<div class="mv-read">ROE <b>{roe}</b>（复利引擎）　股息率 <b>{dyy}</b>（再投基础）　毛利率 <b>{gm}</b></div>
<div class="mv-q"><span class="lab">透镜：</span>这条宏观结构性机会为何 specifically 落到这家公司、且可持续？</div></div>
<div class="mv-card"><div class="mv-h"><b>霍华德·马克斯</b><span class="en">Marks</span></div>
<div class="mv-tag">周期 · 风险≠波动 · 第二层思维</div>
<div class="mv-read">PE <b>{pe}</b>　PB <b>{pb}</b>　负债率 <b>{debt}</b>（永久损失风险代理）</div>
<div class="mv-q"><span class="lab">透镜：</span>估值分位高 ≠ 风险高；市场一致预期是 X，第二层思维的机会在 Y 吗？</div></div>
<div class="mv-card"><div class="mv-h"><b>彼得·林奇</b><span class="en">Lynch</span></div>
<div class="mv-tag">自下而上 · PEG · 公司分类</div>
<div class="mv-read">PE <b>{pe}</b>　总市值 <b>{mvv}亿</b>（规模分类）　营收 <b>{rev}亿</b></div>
<div class="mv-q"><span class="lab">透镜：</span>PEG = PE ÷ 盈利增速（本页未取增速）；它是哪类公司（缓慢增长/周期/成长/困境/资产）？</div></div>
<div class="mv-card"><div class="mv-h"><b>雷·达里奥</b><span class="en">Dalio</span></div>
<div class="mv-tag">宏观机器 · 不相关分散 · 债务周期</div>
<div class="mv-read">负债率 <b>{debt}</b>（杠杆/债务周期信号）　毛利率 <b>{gm}</b></div>
<div class="mv-q"><span class="lab">透镜：</span>这家公司在「宏观机器」哪一环？与组合其他持仓的相关性如何？</div></div>
</div>"""

    # 公司概述
    prods = ctx.get(code, {}).get("prods", [])
    notes = [n for n in ctx.get(code, {}).get("notes", []) if n]
    ovw = (f"本页为「涨价逻辑监测」补建的<b>公司数据采集页</b>：{name}（{code}）是监测清单中"
           + ("、".join(prods[:4]) if prods else "大宗商品") + "涨价的受益标的之一。"
           + ("关键弹性：" + "；".join(notes[:2]) + "。" if notes else "")
           + "财务与估值基于 akshare 公开披露回填（截至 " + TODAY + "），仅供研究参考，不构成投资建议。")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} · 涨价逻辑受益</title>{CSS}</head><body>
<div class="topbar"><div class="topbar-in"><div class="brand">伯克希尔<span class="ac">投资数据中心</span></div><div class="crumb">/ <a href="berkshire-standalone.html">枢纽</a> / <a href="berkshire-chain-map.html">覆盖地图</a> / <a href="articles/price-hike-monitor.html">涨价逻辑监测</a> / {name}</div></div></div>
<div class="detail">
<a class="back" href="articles/price-hike-monitor.html">← 返回涨价逻辑监测看板</a>
<h1>{name} <span style="font-size:14px;color:var(--mut)">{code} · 数据采集页</span></h1>
<p class="hero-sub">{CHAIN_NAME}代表公司；财务快照与估值分位基于 akshare 公开行情回填（截至 {TODAY}）。以下数据仅供研究参考，不构成投资建议。</p>
<div class="section-title">公司概述</div><div class="ovw">{ovw}</div>
<h3 class="section-title">财务快照（{fy}-12-31 年报 / {TODAY} 估值）</h3>
<div class="snap">{snap}</div>
<div class="note">营收/归母净利/毛利率/ROE/负债率/经营现金流取自同花顺财务摘要年报；总市值取自腾讯行情；PE/PB 与近十年分位取自百度估值；股息率 = 最新实施方案每股股利 ÷ 现价。本页为补建数据采集页，叙事与五层框架为公开资料整理。</div>
<div class="section-title">估值历史分位</div><div class="valband">{valband}</div>
<div class="section-title"><span class="dot"></span>安全边际量化线（巴菲特式买点阈值）</div>
<div class="mg-viz">{mg}</div>
<div class="note">安全边际 = 价格显著低于内在价值的缓冲。本线为<b>透明规则触发</b>，非 DCF 精算；现金牛看股息率与低 PB，成长看兑现与分位。不构成买卖建议。</div>
<div class="section-title"><span class="dot"></span>结论合成 · 护城河 × 估值</div><div class="synth-card">{synth}</div>
<div class="section-title"><span class="dot"></span>七位大师视角（思维透镜）</div>
<div class="note">以下为七位价值投资大师的「思维透镜」。所有数字取自本页<b>财务快照</b>（事实层）；每位大师的「你的结论」需由你本人基于理解写定——本工具<b>不代下结论、不构成投资建议</b>。</div>
{masters}
</div>
<footer>伯克希尔投资数据中心 · 数据采集页（涨价逻辑监测补建）　|　数据来源：akshare（同花顺财务摘要 / 百度估值 / 腾讯行情）　|　仅供研究参考，不构成投资建议</footer>
</body></html>"""
    return html


def main():
    changed = []
    ok = 0
    for code, name in MISSING:
        print("=== %s %s ===" % (code, name))
        try:
            fin = retry(lambda: fetch_fin(code))
            pepb = retry(lambda: fetch_pepb(code))
            mv, price = retry(lambda: fetch_mv_price(code))
            dy = retry(lambda: fetch_dividend_yield(code, price))
            print("  fin:", {k: f2(v) for k, v in fin.items()})
            print("  pepb:", {k: f2(v) for k, v in pepb.items()}, "mv=", f2(mv), "price=", f2(price), "dy=", f2(dy))
            co_fn = "berkshire-%s-co-%s.html" % (SLUG, code)
            co_path = os.path.join(DS, co_fn)
            html = build_page(code, name, fin, pepb, mv, price, dy, WATCH)
            open(co_path, "w", encoding="utf-8").write(html)
            changed.append(co_fn)
            ok += 1
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("  !! %s 失败: %s" % (code, repr(e)))
    with open(os.path.join(DS, "_wl_co_changed.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(changed) + ("\n" if changed else ""))
    print("\nDONE ok=%d / %d -> _wl_co_changed.txt (%d files)" % (ok, len(MISSING), len(changed)))


if __name__ == "__main__":
    main()
