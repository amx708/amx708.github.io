# -*- coding: utf-8 -*-
"""回填深链详情页「估值指标」块：用 akshare 百度 PE(TTM)/PB 近十年日度序列，
计算最新值 + 近十年分位，注入 berkshire-*-chain-<code>.html。

规则：
- 仅处理文件名为 6 位纯数字代码的深页（英文 slug 链如 AI 巨头/aero 等无数字代码页跳过）。
- 总市值 / 股息率 因 EastMoney 接口在沙箱被墙不可用 → 保留「待采集」诚实占位。
- 财务块（营收/利润）不触碰，另需年报/巨潮，排后。
- 数据来源：akshare stock_zh_valuation_baidu（百度，覆盖 A 股）。
"""
import os, re, sys, json, time
import socket
socket.setdefaulttimeout(30)

DS = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"

CACHE = os.path.join(DS, "_valuation_cache.json")

# 估值快照块匹配：从 💰 估值快照 头 到 该 fin-block 的 </table></div>
VAL_BLOCK_RE = re.compile(
    r'(<div class="fin-head"><div class="fin-title"><span class="icon">💰</span> 估值快照</div>)'
    r'<span class="fin-tag">待采集</span>(</div>\s*<table class="fin-table">)(.*?)(</table>\s*</div>)',
    re.DOTALL,
)

def fetch_code(code):
    """返回 dict: {pe, pe_pct, pb, pb_pct, date} 或 None。"""
    import subprocess
    code = code.lstrip("0") if False else code  # 保持 6 位原样（百度需无前缀 6 位）
    src = (
        "import sys,json\n"
        "import akshare as ak\n"
        "def pct(series, cur):\n"
        "    import math\n"
        "    vs=[x for x in series if x==x and x is not None]\n"
        "    if not vs: return None\n"
        "    below=sum(1 for v in vs if v<=cur)\n"
        "    return round(below/len(vs)*100,1)\n"
        "out={}\n"
        "for ind in ['市盈率(TTM)','市净率']:\n"
        "    try:\n"
        "        df=ak.stock_zh_valuation_baidu(symbol=%r, indicator=ind, period='近十年')\n"
        "        df=df.dropna(subset=['value'])\n"
        "        if len(df)==0: continue\n"
        "        last=df.iloc[-1]\n"
        "        cur=float(last['value']); d=str(last['date'])\n"
        "        out[ind]={'v':cur,'p':pct(df['value'].tolist(),cur),'d':d}\n"
        "    except Exception as e:\n"
        "        out[ind]={'err':str(e)[:120]}\n"
        "print(json.dumps(out, ensure_ascii=False))\n" % code
    )
    for attempt in range(3):
        try:
            p = subprocess.run([PY, "-c", src], capture_output=True, text=True, timeout=90)
            if p.returncode == 0 and p.stdout.strip():
                return json.loads(p.stdout.strip())
        except Exception as e:
            err = str(e)[:120]
        time.sleep(1.5)
    return None

def main():
    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as f:
            cache = json.load(f)

    # 发现所有深页 + 提取数字代码
    files = [f for f in os.listdir(DS) if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
    code_map = {}  # code -> [files]
    for f in files:
        m = re.search(r"-chain-(\d{6})\.html$", f)
        if not m:
            continue
        code_map.setdefault(m.group(1), []).append(f)

    print("深页总数", len(files), "唯一数字代码", len(code_map))

    # 取数（带缓存）
    for code in sorted(code_map):
        if code in cache and cache[code]:
            continue
        res = fetch_code(code)
        cache[code] = res
        if res:
            pe = res.get("市盈率(TTM)", {})
            pb = res.get("市净率", {})
            print(f"{code}: PE={pe.get('v')}(P{pe.get('p')}%) PB={pb.get('v')}(P{pb.get('p')}%) d={pe.get('d')}")
        else:
            print(f"{code}: 取数失败")
        # 边取边存缓存，防中途崩
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=0)

    # 注入
    filled = 0
    skipped = []
    for code, flist in code_map.items():
        res = cache.get(code)
        if not res:
            skipped.append(code)
            continue
        pe = res.get("市盈率(TTM)", {})
        pb = res.get("市净率", {})
        if "v" not in pe or "v" not in pb:
            skipped.append(code)
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
        for fn in flist:
            path = os.path.join(DS, fn)
            with open(path, "rb") as f:
                raw = f.read()
            txt = raw.decode("utf-8")
            if "估值快照" not in txt:
                continue
            repl_count = [0]
            def sub(m):
                repl_count[0] += 1
                return m.group(1) + f'<span class="fin-tag">{new_tag}</span>' + m.group(2) + new_rows + m.group(4)
            new_txt, n = VAL_BLOCK_RE.subn(sub, txt)
            if n == 0:
                continue
            with open(path, "wb") as f:
                f.write(new_txt.encode("utf-8"))
            filled += 1
    print(f"\n注入完成：filled={filled} skipped(无数据)={len(skipped)} {skipped}")
    # 统计剩余估值块「待采集」占位（未被替换的）
    remain = 0
    for f in files:
        path = os.path.join(DS, f)
        with open(path, "rb") as fh:
            raw = fh.read()
        # 估值快照 块内仍含「待采集」= 未填
        txt = raw.decode("utf-8", "ignore")
        m = re.search(r"估值快照</div><span class=\"fin-tag\">待采集</span>", txt)
        if m:
            remain += 1
    print(f"估值块仍含待采集占位：{remain} / {len(files)}")
    print("DONE")

if __name__ == "__main__":
    main()
