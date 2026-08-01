# -*- coding: utf-8 -*-
"""统一刷新：强制重取 akshare 百度 PE(TTM)/PB 近十年分位，幂等重写所有深链页
「估值指标」块（无论当前是待采集还是旧百度分位），再部署改动页。

- 数字代码页 + slug 命名旧模板页（4 个 data 文件映射）全部覆盖。
- 每次运行重取，session 缓存防中途 SIGKILL 后可续跑。
- 注入为幂等：按「估值快照」头定位块，重写 4 行 + 标签。
"""
import os, re, json, time, subprocess

DS = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"
CACHE = os.path.join(DS, "_valuation_cache.json")
DATA_FILES = ["_mil_electronics_data.py", "_consumer_electronics_data.py",
              "_rare_earth_data.py", "_semiconductor_equip_data.py"]

# 幂等：匹配「估值快照」块，标签任意（待采集/百度分位/…）
VAL_BLOCK_RE = re.compile(
    r'(<div class="fin-head"><div class="fin-title"><span class="icon">💰</span> 估值快照</div>)'
    r'<span class="fin-tag">[^<]*</span>(</div>\s*<table class="fin-table">)(.*?)(</table>\s*</div>)',
    re.DOTALL,
)

def fetch_code(code):
    src = (
        "import sys,json\n"
        "import akshare as ak\n"
        "def pct(s, c):\n"
        "    v=[x for x in s if x==x and x is not None]\n"
        "    return round(sum(1 for x in v if x<=c)/len(v)*100,1) if v else None\n"
        "out={}\n"
        "for ind in ['市盈率(TTM)','市净率']:\n"
        "    try:\n"
        "        df=ak.stock_zh_valuation_baidu(symbol=%r, indicator=ind, period='近十年')\n"
        "        df=df.dropna(subset=['value'])\n"
        "        if not len(df): continue\n"
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

def slug_code_map():
    sc = {}
    for df in DATA_FILES:
        path = os.path.join(DS, df)
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8").read().splitlines():
            sm = re.search(r"'slug':\s*'(\w+)'", line)
            cm = re.search(r"'code':\s*'(\d{6})'", line)
            if sm and cm:
                sc[sm.group(1)] = cm.group(1)
    return sc

def main():
    # 每次运行强制重取：清空缓存从头取，保证分位为最新（被 SIGKILL 则下次重跑）
    cache = {}
    if os.path.exists(CACHE):
        try: os.remove(CACHE)
        except: pass

    # 收集目标：数字代码页 + slug 页映射
    files = [f for f in os.listdir(DS) if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
    digit = re.compile(r"-chain-(\d{6})\.html$")
    slug_re = re.compile(r"-chain-([\w]+)\.html$")
    sc = slug_code_map()
    targets = []  # (filename, code)
    for f in files:
        m = digit.search(f)
        if m:
            targets.append((f, m.group(1)))
        else:
            sm = slug_re.search(f)
            if sm and sm.group(1) in sc:
                targets.append((f, sc[sm.group(1)]))

    codes = sorted(set(c for _, c in targets))
    print(f"目标页 {len(targets)} / 唯一代码 {len(codes)}")

    # 强制重取
    for code in codes:
        res = fetch_code(code)
        cache[code] = res
        if res:
            pe, pb = res.get("市盈率(TTM)", {}), res.get("市净率", {})
            print(f"fetch {code}: PE={pe.get('v')}(P{pe.get('p')}%) PB={pb.get('v')}(P{pb.get('p')}%)")
        else:
            print(f"fetch {code}: FAILED")
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    # 幂等重写
    filled = 0
    skip = []
    file_by_code = {}
    for f, code in targets:
        file_by_code.setdefault(code, []).append(f)
    for code, flist in file_by_code.items():
        res = cache.get(code)
        if not res or "v" not in res.get("市盈率(TTM)", {}) or "v" not in res.get("市净率", {}):
            for f in flist:
                skip.append((f, "no-data"))
            continue
        pe, pb = res["市盈率(TTM)"], res["市净率"]
        date = pe.get("d") or pb.get("d") or "—"
        tag = f"百度分位 · {date}"
        for fn in flist:
            p = os.path.join(DS, fn)
            t = open(p, encoding="utf-8").read()
            if "估值快照" not in t:
                continue
            # 保留原块已有的 总市值 / 股息率，不被本次刷新强制覆盖（避免抹掉已回填的股息率）
            old_total, old_div = "— 待采集", "— 待采集"
            m_old = VAL_BLOCK_RE.search(t)
            if m_old:
                block = m_old.group(3)
                tm = re.search(r'<td>总市值</td><td class="val">([^<]*)</td>', block)
                dm = re.search(r'<td>股息率</td><td class="val">([^<]*)</td>', block)
                if tm: old_total = tm.group(1)
                if dm: old_div = dm.group(1)
            rows = (
                f'    <tr><td>总市值</td><td class="val">{old_total}</td></tr>\n'
                f'    <tr><td>PE（TTM）</td><td class="val">{pe["v"]:.2f} · 近十年 {pe["p"]}%</td></tr>\n'
                f'    <tr><td>PB</td><td class="val">{pb["v"]:.2f} · 近十年 {pb["p"]}%</td></tr>\n'
                f'    <tr><td>股息率</td><td class="val">{old_div}</td></tr>\n'
            )
            def sub(m, rows=rows):
                return m.group(1) + f'<span class="fin-tag">{tag}</span>' + m.group(2) + rows + m.group(4)
            nt, n = VAL_BLOCK_RE.subn(sub, t)
            if n == 0:
                skip.append((fn, "regex-miss"))
                continue
            open(p, "w", encoding="utf-8").write(nt)
            filled += 1
    print(f"幂等重写完成 filled={filled} skip={len(skip)}")
    if skip:
        print("skip 样例:", skip[:5])

if __name__ == "__main__":
    main()
