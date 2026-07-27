# -*- coding: utf-8 -*-
"""
_fetch_peg_data.py —— 采集「净利润增速 g」用于 PEG = PE ÷ g（P2 项）

数据源：akshare stock_yjbb_em(年度业绩报表)，一次性取全市场最新年报的
「归母净利润增长率」(g)，按股票代码存 data/chain_peg_data.json。
后续 _inject_peg.py 读取该 JSON + 页面 PE，算 PEG 注入估值快照。

注意：仅作 g 的代理（单年同比）。亏损/无数据记为 null。
"""
import akshare as ak
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "data", "chain_peg_data.json")


def main():
    df = ak.stock_yjbb_em(date="20251231")  # 2025 年报业绩报表
    print("COLS:", list(df.columns))
    gcol = None
    for c in df.columns:
        s = str(c)
        if "净利润" in s and ("增长" in s or "增长率" in s):
            gcol = c
            break
    print("gcol:", gcol)
    out = {}
    for _, r in df.iterrows():
        code = str(r.get("股票代码", "") or "").strip()
        if not code:
            continue
        g = r.get(gcol) if gcol else None
        try:
            g = float(g)
        except Exception:
            g = None
        out[code] = round(g, 2) if g is not None else None
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", len(out), "codes ->", OUT)


if __name__ == "__main__":
    main()
