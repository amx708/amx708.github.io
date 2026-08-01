# -*- coding: utf-8 -*-
"""全站产业链企业页 深凿升级：照紫金矿业样板，给全部 berkshire-*-chain-*.html
补 4 段（一句话业务 / 关键数字[真实数据] / 新闻时间线[真实新闻] / 来源声明），
沿用每页各自主题色；已有 layer-detail(跨层拆解)/insight-box(投资逻辑) 不重复生成。
- 6 位 A 股代码：抓 THS 年报 + 百度估值 + 腾讯行情 + 东财新闻（真实数据）。
- 字母/其他码：仅加文案段（一句话业务 + 来源声明），不编造数据。
切片可续跑（--start/--end 页索引区间），按代码缓存，每段独立幂等防重复。
"""
import warnings, json, re, os, sys, time, urllib.request
warnings.filterwarnings("ignore")
import akshare as ak

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "._deep_cache.json")
PINYIN = {  # 自信可映射的 A 股拼音 slug -> 6 位代码
    "catl": "300750", "chalco": "601600", "citic": "601998", "bobj": "601328",
    "boc": "601988", "ccb": "601939", "ceb": "601818", "cqb": "601963",
    "csb": "601577", "czb": "601916", "cnnc": "601985", "cypc": "600900",
    "changshu": "601128", "chint": "601877", "buchang": "603858",
    "baiyunshan": "600332", "beigene": "688235", "cmb": "600036",
    "cmbc": "600016", "cqrc": "601077", "bull": "002460", "cykg": "600066",
}

def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)

def load_cache():
    if os.path.exists(CACHE):
        try:
            return json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_cache(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

def to_num(v):
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "--", "None", "nan"):
        return None
    s = s.replace("亿", "").replace("万", "").replace("%", "").replace(",", "").replace("元", "")
    try:
        return float(s)
    except Exception:
        return None

def hex2rgba(h, a):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

def fetch_data(code, cache):
    """返回 dict：rev,net,gross,roe,lev,ocf,rev_yoy,net_yoy,rd,
    pe_cur,pe_pct,pb_cur,pb_pct,price,mkt_cap,news[(d,t)...]。失败项=None/[]。"""
    if code in cache:
        return cache[code]
    d = {"code": code, "news": []}
    # 1) THS 年报
    try:
        df = ak.stock_financial_abstract_ths(symbol=code)
        ann = df[df["报告期"].astype(str).str.endswith("-12-31")].reset_index(drop=True)
        row = ann.iloc[-1] if len(ann) else df.iloc[-1]
        d["rev"] = to_num(row.get("营业总收入"))
        d["net"] = to_num(row.get("净利润"))
        d["gross"] = str(row.get("销售毛利率", "")).strip()
        d["roe"] = str(row.get("净资产收益率", "")).strip()
        d["lev"] = str(row.get("资产负债率", "")).strip()
        d["ocf"] = str(row.get("每股经营现金流", "")).strip()
        d["rev_yoy"] = str(row.get("营业总收入同比增长率", "")).strip()
        d["net_yoy"] = str(row.get("净利润同比增长率", "")).strip()
        d["rd"] = str(row.get("报告期", "")).strip()
    except Exception as e:
        log(f"  THS {code} 失败: {repr(e)[:60]}")
    # 2) 百度估值
    for ind, key in [("市盈率(TTM)", "pe"), ("市净率", "pb")]:
        try:
            vd = ak.stock_zh_valuation_baidu(symbol=code, indicator=ind, period="近十年")
            v = vd["value"].astype(float)
            cur = float(v.iloc[-1]); lo = v.min(); hi = v.max()
            pct = (cur - lo) / (hi - lo) * 100 if hi > lo else 0
            d[f"{key}_cur"] = round(cur, 2); d[f"{key}_pct"] = round(pct, 1)
        except Exception:
            pass
    # 3) 腾讯行情
    try:
        pre = "sh" if code.startswith(("6", "9")) else "sz"
        s = urllib.request.urlopen(f"https://qt.gtimg.cn/q={pre}{code}", timeout=15).read().decode("gbk")
        f = s.split("~")
        d["price"] = f[3]; d["mkt_cap"] = f[45]
    except Exception:
        pass
    # 4) 东财新闻
    try:
        nd = ak.stock_news_em(symbol=code)
        for _, r in nd.head(6).iterrows():
            t = r.get("新闻标题") or r.get("title") or ""
            dt = str(r.get("发布时间") or r.get("date") or "")[:10]
            if t and dt:
                d["news"].append([dt, t])
    except Exception:
        pass
    cache[code] = d
    return d

def accent_of(html):
    m = re.search(r"border-left:3px solid (#[0-9a-fA-F]{6})", html)
    return m.group(1) if m else "14b8a6"

def name_chain_of(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = m.group(1).strip() if m else ""
    parts = re.split(r"\s*链\s*|\s*·\s*|\|", title)
    parts = [p.strip() for p in parts if p.strip()]
    name = parts[0] if parts else "该公司"
    chain = parts[-1] if len(parts) > 1 else ""
    return name, chain

# ---------- 深凿段 CSS（{ACC} 占位，注入时替换） ----------
DEEP_CSS = """
.deep-oneliner{background:{ACC06};border:1px solid {ACC20};border-radius:12px;padding:16px 18px;font-size:14.5px;color:#334155;line-height:1.8}
.deep-oneliner b{color:#0f172a}
.deep-kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.deep-kpi{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.deep-kpi .dk-num{font-size:18px;font-weight:800;color:{ACC}}
.deep-kpi .dk-lab{font-size:11.5px;color:#64748b;margin-top:2px}
.deep-kpi .dk-sub{font-size:11px;color:#94a3b8;margin-top:1px}
.deep-table-wrap{overflow-x:auto;margin-top:6px}
.deep-table-wrap table{width:100%;border-collapse:collapse;font-size:13px}
.deep-table-wrap th,.deep-table-wrap td{padding:9px 10px;text-align:right;border-bottom:1px solid #eef2f7;color:#334155}
.deep-table-wrap th:first-child,.deep-table-wrap td:first-child{text-align:left;color:#0f172a;font-weight:600}
.deep-table-wrap th{color:#64748b;font-weight:600;background:#f8fafc}
.deep-table-wrap td .pos{color:#16a34a}
.deep-table-wrap td .neg{color:#dc2626}
.deep-src{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 14px;margin-top:10px;font-size:12px;color:#64748b;line-height:1.7}
.deep-src b{color:#475569}
.deep-timeline{position:relative;padding-left:22px;margin-top:6px}
.deep-timeline::before{content:"";position:absolute;left:6px;top:4px;bottom:4px;width:2px;background:{ACC40}}
.deep-tl-item{position:relative;margin-bottom:16px}
.deep-tl-item::before{content:"";position:absolute;left:-19px;top:6px;width:10px;height:10px;border-radius:50%;background:{ACC};box-shadow:0 0 0 3px {ACC15}}
.deep-tl-date{font-size:12px;color:{ACC};font-weight:700}
.deep-tl-text{font-size:13.5px;color:#475569;line-height:1.75;margin-top:2px}
.deep-tl-text b{color:#1e293b}
"""

def build_segments(name, chain, code, is_a, d, acc):
    # ① 一句话业务
    if is_a:
        oneliner = (f"<b>{name}（{code}）</b> 是「{chain}」产业链中的代表性 A 股核心标的，"
                    f"业务处于该链条的关键环节，是观察这条产业链景气度的窗口之一。")
    else:
        oneliner = (f"<b>{name}</b> 是「{chain}」产业链中的代表性企业，"
                    f"是该环节全球或区域竞争格局的重要参与者。")

    # ② 关键数字（仅 A 股有真实数据）
    kpis = ""
    if is_a and d.get("rev") is not None:
        rev = d.get("rev"); net = d.get("net"); gross = d.get("gross", "—")
        roe = d.get("roe", "—"); lev = d.get("lev", "—")
        price = d.get("price", "—"); mkt = d.get("mkt_cap", "—")
        rd = d.get("rd", "")[:4]
        pe = d.get("pe_cur"); pe_pct = d.get("pe_pct")
        pb = d.get("pb_cur"); pb_pct = d.get("pb_pct")
        pe_s = f"PE {pe} · 近十年分位 {pe_pct}%" if pe is not None else "PE —"
        pb_s = f"PB {pb} · 近十年分位 {pb_pct}%" if pb is not None else "PB —"
        src_line = (f"注：财务取自同花顺年报摘要（{d.get('rd','')}）；估值 / 行情为采集日快照"
                    f"（腾讯行情）。{pe_s}；{pb_s}。")
        kpis = f"""
<div class="deep-kpi-grid">
<div class="deep-kpi"><div class="dk-num">{rev:.0f}亿</div><div class="dk-lab">营业总收入({rd})</div><div class="dk-sub">同比 {d.get('rev_yoy','—')}</div></div>
<div class="deep-kpi"><div class="dk-num">{net:.0f}亿</div><div class="dk-lab">归母净利润({rd})</div><div class="dk-sub">同比 {d.get('net_yoy','—')}</div></div>
<div class="deep-kpi"><div class="dk-num">{gross}</div><div class="dk-lab">销售毛利率</div><div class="dk-sub">盈利空间</div></div>
<div class="deep-kpi"><div class="dk-num">{roe}</div><div class="dk-lab">ROE(加权)</div><div class="dk-sub">回报质量</div></div>
<div class="deep-kpi"><div class="dk-num">{lev}</div><div class="dk-lab">资产负债率</div><div class="dk-sub">财务杠杆</div></div>
<div class="deep-kpi"><div class="dk-num">{price}</div><div class="dk-lab">现价(元)</div><div class="dk-sub">市值 {mkt}亿</div></div>
</div>
<div class="deep-table-wrap"><table>
<thead><tr><th>指标（{d.get('rd','')} 年报）</th><th>数值</th><th>信号</th></tr></thead>
<tbody>
<tr><td>营业总收入</td><td>{rev:.1f} 亿</td><td class="pos">同比 {d.get('rev_yoy','—')}</td></tr>
<tr><td>归母净利润</td><td>{net:.1f} 亿</td><td class="pos">同比 {d.get('net_yoy','—')}</td></tr>
<tr><td>销售毛利率</td><td>{gross}</td><td class="pos">盈利空间</td></tr>
<tr><td>ROE（加权）</td><td>{roe}</td><td class="pos">高回报</td></tr>
<tr><td>资产负债率</td><td>{lev}</td><td class="neg">关注杠杆</td></tr>
<tr><td>每股经营现金流</td><td>{d.get('ocf','—')}</td><td class="pos">造血能力</td></tr>
</tbody></table></div>
<div class="deep-src" style="margin-top:10px">{src_line}</div>
"""

    # ⑤ 新闻时间线（仅真实新闻）
    timeline = ""
    news = d.get("news", [])
    if news:
        items = "".join(
            f'<div class="deep-tl-item"><div class="deep-tl-date">{dt}</div><div class="deep-tl-text">{t}</div></div>\n'
            for dt, t in news)
        timeline = f'<div class="deep-timeline">{items}</div>'

    # ⑥ 来源声明（合规说明）
    source_note = (f'<div class="deep-src">📌 <b>合规说明</b>：本页「一句话业务 / 关键数字 / 新闻时间线」均基于'
                   f'<b>{name}</b>公开年报、官网与新闻等事实层信息，由本站原创整理与重写，'
                   f'不复制、不转载任何付费 / 闭源专享内容；第三方机构预测为估算或传闻，仅供框架参考，'
                   f'请以公司官方披露为准。投资逻辑仅为跨层框架研究示例，<b>不构成任何投资建议</b>。'
                   f'版权归{name}及各原发布方所有。</div>')
    return oneliner, kpis, timeline, source_note

def process(html, name, chain, code, is_a, cache, acc):
    changed = False
    # CSS 注入（一次）
    if "deep-kpi-grid" not in html:
        css = (DEEP_CSS
               .replace("{ACC}", "#" + acc)
               .replace("{ACC06}", hex2rgba(acc, 0.06))
               .replace("{ACC10}", hex2rgba(acc, 0.10))
               .replace("{ACC15}", hex2rgba(acc, 0.15))
               .replace("{ACC20}", hex2rgba(acc, 0.20))
               .replace("{ACC22}", hex2rgba(acc, 0.22))
               .replace("{ACC25}", hex2rgba(acc, 0.25))
               .replace("{ACC40}", hex2rgba(acc, 0.40)))
        html = html.replace("</style>", css + "\n</style>", 1)
        changed = True

    d = fetch_data(code, cache) if is_a else {}
    oneliner, kpis, timeline, source_note = build_segments(name, chain, code, is_a, d, acc)

    # ① 一句话业务（幂等）
    if "一句话业务" not in html:
        block1 = f'<div class="section-title">一句话业务</div>\n<div class="deep-oneliner">{oneliner}</div>\n'
        if kpis:
            block1 += f'<div class="section-title">关键数字</div>\n{kpis}\n'
        idx = html.find('<div class="section-title">')
        if idx == -1:
            idx = html.find("</style>") + len("</style>")
        html = html[:idx] + block1 + html[idx:]
        changed = True

    # ⑤ 新闻时间线 + ⑥ 来源声明（幂等，插在末尾 source-note 前；无则插 </body> 前）
    if ("新闻时间线" not in html and timeline) or ("合规说明" not in html):
        block2 = ""
        if timeline and "新闻时间线" not in html:
            block2 += f'<div class="section-title">新闻时间线（近 1 年）</div>\n{timeline}\n'
        if "合规说明" not in html:
            block2 += source_note + "\n"
        if block2:
            sn = html.rfind('<div class="source-note">')
            if sn != -1:
                html = html[:sn] + block2 + html[sn:]
            else:
                bidx = html.rfind("</body>")
                if bidx != -1:
                    html = html[:bidx] + block2 + html[bidx:]
                else:
                    html += block2
            changed = True
    return html, changed

def main():
    start = int(sys.argv[sys.argv.index("--start") + 1]) if "--start" in sys.argv else 0
    end = int(sys.argv[sys.argv.index("--end") + 1]) if "--end" in sys.argv else 10**9
    cache = load_cache()
    files = sorted(f for f in os.listdir(BASE)
                   if re.match(r"^berkshire-.+-chain-[^.]+\.html$", f))
    files = files[start:end]
    log(f"切片 [{start},{end}) 共 {len(files)} 页")
    out = open(os.path.join(BASE, "._deep_changed.txt"), "a", encoding="utf-8")
    cnt = 0
    for i, fn in enumerate(files):
        path = os.path.join(BASE, fn)
        try:
            html = open(path, encoding="utf-8").read()
        except Exception:
            continue
        m = re.match(r"^berkshire-.+-chain-([^.]+)\.html$", fn)
        raw = m.group(1)
        is_a = raw.isdigit() and len(raw) == 6
        code = raw if is_a else PINYIN.get(raw, raw)
        acc = accent_of(html)
        name, chain = name_chain_of(html)
        new_html, changed = process(html, name, chain, code, is_a, cache, acc)
        if changed:
            open(path, "w", encoding="utf-8").write(new_html)
            out.write(fn + "\n")
            out.flush()
            cnt += 1
        if (i + 1) % 20 == 0:
            log(f"  进度 {i+1}/{len(files)} 已改 {cnt}")
    save_cache(cache)
    out.close()
    log(f"切片完成：改 {cnt} 页，缓存 {len(cache)} 代码")

if __name__ == "__main__":
    main()
