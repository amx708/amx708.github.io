# -*- coding: utf-8 -*-
"""股息率刷新：THS 最新分红方案(每股现金股利) ÷ 腾讯实时股价 → 静态股息率。
幂等重写所有 A股深链页「估值快照」块的 股息率 行（总市值/PE/PB/标签保持不变）。

- 数字代码页 + slug 命名旧模板页（4 个 data 文件映射）全部覆盖。
- 每股股利：ak.stock_fhps_detail_ths(sandbox 通) 取最新 实施方案/预案 含「派」的方案，
  解析「每10股派X元(含税)」→ 每股=X/10。纯送转(无现金)→「—」。
- 股价：腾讯行情 qt.gtimg.cn（HTTP200 稳定, idx3=最新价）。
- 股息率 = 每股现金股利 / 股价 × 100%，保留2位 + '%'。
- 持久缓存 _dividend_cache.json，重跑可续；后台跑防 SIGKILL。
"""
import os, re, json, time, subprocess

DS = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"
CACHE = os.path.join(DS, "_dividend_cache.json")
DATA_FILES = ["_mil_electronics_data.py", "_consumer_electronics_data.py",
              "_rare_earth_data.py", "_semiconductor_equip_data.py"]
CHANGED = os.path.join(DS, "_dividend_changed.txt")

# 只替换 估值快照 块内的 股息率 行（其余行/标签不动）
DIV_ROW_RE = re.compile(r'(<tr><td>股息率</td><td class="val">)[^<]*(</td></tr>)')


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


def fetch_dps(code):
    """THS 分红方案 → 最新每股现金股利（元）。无现金分红返回 None。"""
    # 写到临时 .py 跑，避免 python -c 在 Windows 下中文/正则转义问题
    tmpl = (
        "import sys, json, re, akshare as ak\n"
        "code = %r\n"
        "df = ak.stock_fhps_detail_ths(symbol=code)\n"
        "rows = df.to_dict('records')\n"
        "cand = None\n"
        "for d in reversed(rows):\n"
        "    s = str(d.get('\\u5206\\u7ea2\\u65b9\\u6848\\u8bf4\\u660e', ''))\n"
        "    if '\\u6d3e' in s and d.get('\\u65b9\\u6848\\u8fdb\\u5ea6') in ('\\u5b9e\\u65bd\\u65b9\\u6848', '\\u80a1\\u4e1c\\u5927\\u4f1a\\u9884\\u6848'):\n"
        "        cand = s; break\n"
        "m = re.search(r'[\\u6d3e\\u53d1]\\s*([0-9]+(?:\\.[0-9]+)?)\\s*\\u5143', cand) if cand else None\n"
        "print(json.dumps({'desc': cand, 'dps': float(m.group(1))/10.0 if m else None}, ensure_ascii=False))\n"
    ) % code
    tmp = os.path.join(DS, "_dps_tmp.py")
    open(tmp, "w", encoding="utf-8").write(tmpl)
    try:
        for _ in range(3):
            try:
                p = subprocess.run([PY, tmp], capture_output=True, text=True, timeout=80)
                if p.returncode == 0 and p.stdout.strip():
                    return json.loads(p.stdout.strip())
            except Exception:
                pass
            time.sleep(1.5)
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass
    return None


def fetch_price(code):
    """腾讯行情最新价。6/9 开头→sh，其余→sz。"""
    m = "sh" if code[0] in "69" else "sz"
    for _ in range(3):
        try:
            raw = subprocess.run(["curl", "-s", "-m", "10", f"https://qt.gtimg.cn/q={m}{code}"],
                                 capture_output=True).stdout
            try:
                s = raw.decode("gbk")
            except Exception:
                s = raw.decode("utf-8", "ignore")
            s = s.split('="', 1)[1].rstrip(';\n"')
            return float(s.split("~")[3])
        except Exception:
            pass
        time.sleep(1.0)
    return None


def main():
    cache = {}
    if os.path.exists(CACHE):
        try:
            cache = json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            cache = {}

    files = [f for f in os.listdir(DS)
             if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
    digit = re.compile(r"-chain-(\d{6})\.html$")
    slug_re = re.compile(r"-chain-([\w]+)\.html$")
    sc = slug_code_map()
    targets = []
    for f in files:
        m = digit.search(f)
        if m:
            targets.append((f, m.group(1)))
        else:
            sm = slug_re.search(f)
            if sm and sm.group(1) in sc:
                targets.append((f, sc[sm.group(1)]))

    code_files = {}
    for f, code in targets:
        code_files.setdefault(code, []).append(f)
    codes = sorted(code_files)
    print(f"目标页 {len(targets)} / 唯一代码 {len(codes)} / 已缓存 {len(cache)}")

    # 抓取（持久缓存，可续跑）
    for i, code in enumerate(codes, 1):
        if code in cache and cache[code] and "yield" in cache[code]:
            continue
        dps_info = fetch_dps(code)
        dps = dps_info.get("dps") if dps_info else None
        desc = (dps_info or {}).get("desc")
        price = fetch_price(code)
        if dps and price and price > 0:
            yld = round(dps / price * 100, 2)
        else:
            yld = None  # 无现金分红或取数失败
        cache[code] = {"dps": dps, "price": price, "yield": yld, "desc": desc}
        tag = f"{yld}%" if yld is not None else "—"
        print(f"[{i}/{len(codes)}] {code}: dps={dps} price={price} 股息率={tag}  ({desc})")
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    # 幂等重写 股息率 行
    filled = 0
    skip = []
    changed = []
    for code, flist in code_files.items():
        yld = cache.get(code, {}).get("yield")
        val = f"{yld}%" if yld is not None else "—"
        for fn in flist:
            p = os.path.join(DS, fn)
            t = open(p, encoding="utf-8").read()
            if "估值快照" not in t or "<td>股息率</td>" not in t:
                skip.append((fn, "no-block"))
                continue
            nt, n = DIV_ROW_RE.subn(lambda m: m.group(1) + val + m.group(2), t)
            if n == 0:
                skip.append((fn, "regex-miss"))
                continue
            if nt != t:
                open(p, "w", encoding="utf-8").write(nt)
                filled += 1
                changed.append(fn)
    print(f"重写完成 filled={filled} skip={len(skip)}")
    if skip:
        print("skip 样例:", skip[:5])
    with open(CHANGED, "w", encoding="utf-8") as fh:
        fh.write("\n".join(changed) + ("\n" if changed else ""))
    print(f"改动清单 {len(changed)} 行 → {CHANGED}")


if __name__ == "__main__":
    main()
