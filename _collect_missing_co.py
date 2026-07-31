# -*- coding: utf-8 -*-
"""为 16 个「无 co 页、关键财务空白」的深页企业采集真实财务 + 估值，补建 co 页并回填深页。

数据源（沙箱可用，非东方财富）：
  - akshare.stock_financial_abstract_ths  -> 营业总收入/净利润/销售毛利率/净资产收益率/资产负债率/每股经营现金流/基本每股收益
  - akshare.stock_zh_valuation_baidu     -> PE(TTM)/PB 近十年最新值
经营现金流净额(亿) = 每股经营现金流(元) × 净利润(亿) ÷ 基本每股收益(元)（同一年报行，量纲自洽）。

产出：
  - berkshire-<slug>-co-<code>.html  （补建的公司数据采集页，含 10 项 snap；总市值/股息率因 EastMoney 墙暂留 待采集）
  - 回填对应 berkshire-<slug>-chain-<slugX>.html 的「关键财务」6 行 + 翻标签为 已采集（走 _upgrade_frames 的 get_fin_from_co+inject_financials）
  - _collect_changed.txt  （改动清单，供 deploy_bulk files 串行推送）
"""
import os, re, sys, glob, json, warnings
warnings.filterwarnings("ignore")
import akshare as ak

DS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DS)
import _upgrade_frames as uf  # 复用 get_fin_from_co / inject_financials / SNAP_MAP

TODAY = "2026-07-31"

# (slug, code, name) —— code 用于按代码全局找/建 co 页；chain 文件名用原 slug 片段
TARGETS = [
    # rare-earth（12，原 chain 页用字母 slug）
    ("rare-earth", "600111", "北方稀土"), ("rare-earth", "600010", "包钢股份"),
    ("rare-earth", "600259", "广晟有色"), ("rare-earth", "002056", "横店东磁"),
    ("rare-earth", "300748", "金力永磁"), ("rare-earth", "600366", "宁波韵升"),
    ("rare-earth", "600392", "盛和资源"), ("rare-earth", "600549", "厦门钨业"),
    ("rare-earth", "000795", "英洛华"),   ("rare-earth", "000831", "中国稀土"),
    ("rare-earth", "300224", "正海磁材"), ("rare-earth", "000970", "中科三环"),
    # semiconductor-chemical（2）
    ("semiconductor-chemical", "688106", "金宏气体"), ("semiconductor-chemical", "688138", "清溢光电"),
    # semiconductor-equip（2，原 chain 页用字母 slug）
    ("semiconductor-equip", "688409", "富创精密"), ("semiconductor-equip", "688596", "正帆科技"),
]

CHAIN_SLUG = {  # chain 页文件名里用的片段（与现有 chain 页一致）
    "rare-earth": {"600111": "bfxt", "600010": "bggf", "600259": "gsys", "002056": "hddc",
                   "300748": "jlcy", "600366": "nbys", "600392": "shhe", "600549": "xmwy",
                   "000795": "ylh", "000831": "zgxt", "300224": "zhmc", "000970": "zkth"},
    "semiconductor-chemical": {"688106": "688106", "688138": "688138"},
    "semiconductor-equip": {"688409": "fcjm", "688596": "zfkj"},
}


def col(df, *keys):
    for k in keys:
        for c in df.columns:
            if c == k or k in c:
                return c
    return None


def num(x):
    """从 '425.63亿' / '12.21%' / '0.31' / '1,234.5' 之类取出浮点（忽略单位）。"""
    if x is None:
        return None
    s = str(x).replace(",", "")
    m = re.search(r"-?\d+\.?\d*", s)
    return float(m.group()) if m else None


def to_yi(x):
    """金额类：解析并归一化到「亿」。'9131.86万'->0.913；'425.63亿'->425.63。"""
    if x is None:
        return None
    s = str(x).replace(",", "")
    m = re.search(r"-?\d+\.?\d*", s)
    if not m:
        return None
    v = float(m.group())
    if "万" in s:
        return v / 1e4
    return v  # 默认视为「亿」（THS 金额无单位时也按亿）


def to_num(x):
    """比率/每股类：取数值（忽略 % 等单位）。"""
    return num(x)


def pick_annual(df):
    """取最新年报行（报告期以 12-31 结尾）。"""
    if "报告期" in df.columns:
        ann = df[df["报告期"].astype(str).str.endswith("12-31")]
        if len(ann):
            return ann.iloc[-1]
    return df.iloc[-1]


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
    gm = to_num(row[gm_c]) if gm_c else None
    roe = to_num(row[roe_c]) if roe_c else None
    debt = to_num(row[debt_c]) if debt_c else None
    eps = to_num(row[eps_c]) if eps_c else None
    cfps = to_num(row[cfps_c]) if cfps_c else None
    ocf = None
    if cfps is not None and npv is not None and eps not in (None, 0):
        ocf = cfps * npv / eps  # 元 × 亿 ÷ 元 = 亿
    # 合理性护栏：净利>营收 / 经营现金流绝对值>营收5倍 视为解析异常 -> 置空
    if npv is not None and rev is not None and (npv > rev or npv < -rev):
        npv = None
    if ocf is not None and rev is not None and abs(ocf) > rev * 5:
        ocf = None
    return dict(rev=rev, npv=npv, gm=gm, roe=roe, debt=debt, ocf=ocf,
                fy=str(row["报告期"])[:4] if "报告期" in df.columns else "2025")


def fetch_pepb(code):
    out = {}
    for ind, key in [("市盈率(TTM)", "pe"), ("市净率", "pb")]:
        try:
            d = ak.stock_zh_valuation_baidu(symbol=code, indicator=ind, period="近十年")
            if len(d):
                out[key] = float(d.iloc[-1]["value"])
        except Exception:
            pass
    return out


def f2(x):
    return ("%.2f" % x) if isinstance(x, (int, float)) else "待采集"


def build_co_page(slug, code, name, fin, pepb):
    chain = {"rare-earth": "稀土", "semiconductor-chemical": "半导体化学",
             "semiconductor-equip": "半导体设备"}[slug]
    fy = fin.get("fy", "2025")
    mv = "待采集"  # EastMoney 墙，暂缺总市值
    dy = "待采集"   # EastMoney 墙，暂缺股息率
    snap = (
        f'<div><b>{f2(fin["rev"])}</b><span>营收(亿)</span></div>'
        f'<div><b>{f2(fin["npv"])}</b><span>归母净利(亿)</span></div>'
        f'<div><b>{f2(fin["gm"])}</b><span>毛利率(%)</span></div>'
        f'<div><b>{f2(fin["roe"])}</b><span>ROE(%)</span></div>'
        f'<div><b>{f2(fin["debt"])}</b><span>负债率(%)</span></div>'
        f'<div><b>{f2(fin["ocf"])}</b><span>经营现金流(亿)</span></div>'
        f'<div><b>{mv}</b><span>总市值(亿)</span></div>'
        f'<div><b>{f2(pepb.get("pe"))}</b><span>PE</span></div>'
        f'<div><b>{f2(pepb.get("pb"))}</b><span>PB</span></div>'
        f'<div><b>{dy}</b><span>股息率(%)</span></div>'
    )
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} · {chain}产业链</title>
<style>
:root{{--bg:#f5f9ff;--soft:#eef5ff;--card:#fff;--ink:#0f172a;--mut:#475569;--line:rgba(59,130,246,.15);--accent:#2563eb;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f5f9ff;color:var(--ink);line-height:1.7}}
.topbar{{position:sticky;top:0;z-index:50;background:rgba(11,31,58,.82);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08);color:#fff}}
.topbar-in{{max-width:1080px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}}
.brand{{font-weight:800;font-size:17px}}.brand .ac{{color:#f5a623}}
.crumb{{font-size:13px;color:#9fb2cf}}.crumb a{{color:#9fb2cf;text-decoration:none}}
.detail{{max-width:920px;margin:0 auto;padding:28px 20px 70px}}
.detail h1{{font-weight:700}}
.snap{{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:16px 0}}
.snap div{{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:12px 10px;text-align:center}}
.snap b{{display:block;font-size:19px;color:var(--accent);font-weight:700}}
.snap span{{font-size:11px;color:var(--mut)}}
.section-title{{font-size:18px;font-weight:700;margin:34px 0 16px;padding-left:12px;border-left:4px solid var(--accent);color:var(--ink)}}
.note{{background:var(--soft);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:12px 16px;margin:14px 0;font-size:13px;color:var(--mut);line-height:1.65}}
</style></head>
<body>
<div class="topbar"><div class="topbar-in"><div class="brand">伯克希尔<span class="ac">投资数据中心</span></div><div class="crumb">/ <a href="berkshire-standalone.html">枢纽</a> / <a href="berkshire-chain-map.html">覆盖地图</a> / <a href="berkshire-{slug}-chains.html">{chain}产业链</a> / {name}</div></div></div>
<div class="detail">
<a class="back" href="berkshire-{slug}-chains.html">← 返回{chain}产业链</a>
<h1>{name} <span style="font-size:14px;color:var(--mut)">{code} · 数据采集页</span></h1>
<p style="color:var(--mut)">以下财务数据基于 akshare（同花顺财务摘要 + 百度估值）公开披露回填（截至 {TODAY}），仅供研究参考，不构成投资建议。</p>
<h3 class="section-title">财务快照（{fy}-12-31 年报）</h3>
<div class="snap">
{snap}
</div>
<div class="note">总市值 / 股息率：当前沙箱数据源（东方财富）不可用，暂以「待采集」占位，待源可用后回填。PE/PB 取自百度近十年分位口径最新值。本页为补建的「公司数据采集页」，财务以年报为准。</div>
</div>
</body></html>"""
    return html


def main():
    changed = []
    for slug, code, name in TARGETS:
        print("=== %s %s %s ===" % (slug, code, name))
        try:
            fin = fetch_fin(code)
            pepb = fetch_pepb(code)
            print("  fin:", {k: f2(v) for k, v in fin.items()})
            print("  pepb:", pepb)
            # 写 co 页
            co_fn = "berkshire-%s-co-%s.html" % (slug, code)
            co_path = os.path.join(DS, co_fn)
            if os.path.exists(co_path):
                print("  co 页已存在，覆盖:", co_fn)
            open(co_path, "w", encoding="utf-8").write(build_co_page(slug, code, name, fin, pepb))
            # 回填 chain 页（走 get_fin_from_co + inject_financials）
            cslug = CHAIN_SLUG[slug][code]
            chain_fn = "berkshire-%s-chain-%s.html" % (slug, cslug)
            chain_path = os.path.join(DS, chain_fn)
            if not os.path.exists(chain_path):
                print("  !! chain 页缺失:", chain_fn)
                continue
            f = uf.get_fin_from_co(slug, code)
            did = uf.inject_financials(chain_path, f)
            print("  inject did=", did)
            changed.append(chain_fn)
            changed.append(co_fn)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("  !! %s 失败: %s" % (code, repr(e)))
    with open(os.path.join(DS, "_collect_changed.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(changed) + ("\n" if changed else ""))
    print("\nDONE changed=%d -> _collect_changed.txt" % len(changed))


if __name__ == "__main__":
    main()
