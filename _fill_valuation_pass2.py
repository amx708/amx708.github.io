# -*- coding: utf-8 -*-
"""第二遍：回填 42 个用 slug 命名的旧模板深链页（mil-electronics/consumer-electronics/
rare-earth/semiconductor-equip）+ 重试 300114。这些页文件名是拼音 slug 而非 6 位代码，
但数据文件里有 code。复用 _valuation_cache.json，只补未填入的页。
"""
import os, re, json, time, subprocess

DS = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DS, "_valuation_cache.json")
PY = r"C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"

DATA_FILES = [
    "_mil_electronics_data.py",
    "_consumer_electronics_data.py",
    "_rare_earth_data.py",
    "_semiconductor_equip_data.py",
]

VAL_BLOCK_RE = re.compile(
    r'(<div class="fin-head"><div class="fin-title"><span class="icon">💰</span> 估值快照</div>)'
    r'<span class="fin-tag">待采集</span>(</div>\s*<table class="fin-table">)(.*?)(</table>\s*</div>)',
    re.DOTALL,
)

def build_slug_code():
    sc = {}
    for df in DATA_FILES:
        path = os.path.join(DS, df)
        if not os.path.exists(path):
            continue
        txt = open(path, encoding="utf-8").read()
        for m in re.finditer(r"'slug':\s*'(\w+)'.*?'code':\s*'(\d{6})'", txt, re.DOTALL):
            # 宽松匹配：slug 与 code 在同一 dict 行附近（单行 dict）
            pass
        # 单行 dict 更可靠：逐行找同时含 slug 和 code 的行
        for line in txt.splitlines():
            sm = re.search(r"'slug':\s*'(\w+)'", line)
            cm = re.search(r"'code':\s*'(\d{6})'", line)
            if sm and cm:
                sc[sm.group(1)] = cm.group(1)
    return sc

def fetch_code(code):
    src = (
        "import sys,json\n"
        "import akshare as ak\n"
        "def pct(series, cur):\n"
        "    vs=[x for x in series if x==x and x is not None]\n"
        "    if not vs: return None\n"
        "    return round(sum(1 for v in vs if v<=cur)/len(vs)*100,1)\n"
        "out={}\n"
        "for ind in ['市盈率(TTM)','市净率']:\n"
        "    try:\n"
        "        df=ak.stock_zh_valuation_baidu(symbol=%r, indicator=ind, period='近十年')\n"
        "        df=df.dropna(subset=['value'])\n"
        "        if len(df)==0: continue\n"
        "        last=df.iloc[-1]; cur=float(last['value'])\n"
        "        out[ind]={'v':cur,'p':pct(df['value'].tolist(),cur),'d':str(last['date'])}\n"
        "    except Exception as e:\n"
        "        out[ind]={'err':str(e)[:120]}\n"
        "print(json.dumps(out, ensure_ascii=False))\n" % code
    )
    for _ in range(3):
        try:
            p = subprocess.run([PY, "-c", src], capture_output=True, text=True, timeout=90)
            if p.returncode == 0 and p.stdout.strip():
                return json.loads(p.stdout.strip())
        except Exception:
            pass
        time.sleep(1.5)
    return None

def main():
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))
    sc = build_slug_code()
    print("slug->code 映射数:", len(sc))
    # 需要补取数的 code（缓存无有效值）
    need = set(c for c in sc.values()) | {"300114"}
    for code in sorted(need):
        res = cache.get(code)
        if res and "v" in res.get("市盈率(TTM)", {}) and "v" in res.get("市净率", {}):
            continue
        res = fetch_code(code)
        cache[code] = res
        if res:
            pe = res.get("市盈率(TTM)", {}); pb = res.get("市净率", {})
            print(f"fetch {code}: PE={pe.get('v')}(P{pe.get('p')}%) PB={pb.get('v')}(P{pb.get('p')}%)")
        else:
            print(f"fetch {code}: FAILED")
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    files = [f for f in os.listdir(DS) if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
    pat = re.compile(r'估值快照</div><span class="fin-tag">待采集</span>')
    digit = re.compile(r"-chain-(\d{6})\.html$")
    filled = 0
    skip = []
    for f in files:
        t = open(os.path.join(DS, f), encoding="utf-8").read()
        if not pat.search(t):
            continue
        m = digit.search(f)
        if m:
            code = m.group(1)
        else:
            # 取 slug 段
            sm = re.search(r"-chain-([\w]+)\.html$", f)
            slug = sm.group(1) if sm else None
            code = sc.get(slug)
            if not code:
                skip.append((f, "no-code-map"))
                continue
        res = cache.get(code)
        if not res:
            skip.append((f, "no-cache"))
            continue
        pe = res.get("市盈率(TTM)", {})
        pb = res.get("市净率", {})
        if "v" not in pe or "v" not in pb:
            skip.append((f, "no-value"))
            continue
        pe_v, pe_p, pe_d = pe["v"], pe["p"], pe["d"]
        pb_v, pb_p, pb_d = pb["v"], pb["p"], pb["d"]
        date = pe_d or pb_d or "—"
        new_rows = (
            '    <tr><td>总市值</td><td class="val">— 待采集</td></tr>\n'
            f'    <tr><td>PE（TTM）</td><td class="val">{pe_v:.2f} · 近十年 {pe_p}%</td></tr>\n'
            f'    <tr><td>PB</td><td class="val">{pb_v:.2f} · 近十年 {pb_p}%</td></tr>\n'
            '    <tr><td>股息率</td><td class="val">— 待采集</td></tr>\n'
        )
        new_tag = f"百度分位 · {date}"

        def sub(m):
            return m.group(1) + f'<span class="fin-tag">{new_tag}</span>' + m.group(2) + new_rows + m.group(4)
        new_t, n = VAL_BLOCK_RE.subn(sub, t)
        if n == 0:
            skip.append((f, "regex-miss"))
            continue
        open(os.path.join(DS, f), "w", encoding="utf-8").write(new_t)
        filled += 1
    print(f"第二遍填充: filled={filled} skip={len(skip)} {skip}")

if __name__ == "__main__":
    main()
