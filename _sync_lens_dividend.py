# -*- coding: utf-8 -*-
"""七大师透镜股息率同步：把 lens 区静态占位 `股息率 <b>—</b>` 同步成真实值。

- 数据源：_dividend_cache.json 的 yield（与估值快照股息率同源，保证一致）。
- 仅当该页对应代码的 yield 非 None 时才改写；无分红的页保持 <b>—</b> 不动。
- 总市值透镜(<b>—亿</b>)按决策维持待采集，本脚本不改动。
- 幂等；输出改动清单 _lens_dividend_changed.txt 供部署。
"""
import os, re, json

DS = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DS, "_dividend_cache.json")
CHANGED = os.path.join(DS, "_lens_dividend_changed.txt")
DATA_FILES = ["_mil_electronics_data.py", "_consumer_electronics_data.py",
              "_rare_earth_data.py", "_semiconductor_equip_data.py"]

DASH = "—"  # em-dash
LENS_RE = re.compile(r"股息率 <b>" + re.escape(DASH) + r"</b>")


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
    cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
    sc = slug_code_map()
    digit = re.compile(r"-chain-(\d{6})\.html$")
    slug_re = re.compile(r"-chain-([\w]+)\.html$")

    files = [f for f in os.listdir(DS)
             if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
    changed = []
    n_sync = 0
    for f in files:
        m = digit.search(f)
        code = m.group(1) if m else sc.get(slug_re.search(f).group(1)) if slug_re.search(f) else None
        if not code:
            continue
        yld = cache.get(code, {}).get("yield")
        if yld is None:
            continue  # 无分红：透镜保持 <b>—</b>
        p = os.path.join(DS, f)
        t = open(p, encoding="utf-8").read()
        if "股息率 <b>" + DASH + "</b>" not in t:
            continue
        nt = LENS_RE.sub(f"股息率 <b>{yld}%</b>", t)
        if nt != t:
            open(p, "w", encoding="utf-8").write(nt)
            changed.append(f)
            n_sync += 1
    with open(CHANGED, "w", encoding="utf-8") as fh:
        fh.write("\n".join(changed) + ("\n" if changed else ""))
    print(f"透镜股息率同步完成：{n_sync} 页写入 / 改动清单 {len(changed)} 行 → {CHANGED}")


if __name__ == "__main__":
    main()
