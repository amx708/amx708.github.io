# -*- coding: utf-8 -*-
"""
_fetch_peg.py —— 伯克希尔数据中心 · P2-C 增强
给成长链(AI/创新药/机器人/有色)的 A 股公司补 PEG = PE(TTM) ÷ 净利增速(%).

数据源(akshare, 托管 venv, 需清代理):
- PE(TTM):  ak.stock_zh_valuation_baidu(symbol=code, indicator="市盈率(TTM)", period="近十年") -> 末值
- 净利增速: ak.stock_financial_analysis_indicator(symbol=code, start_year="2019")
           取年度(日期 endswith -12-31)的 扣除非经常性损益后的净利润(元)，
           算近 ~3-4 年 CAGR 作为 G。

优雅降级:
- 港股(code 含字母/.hk 或长度≠6 纯数字): 百度估值不覆盖 -> PE=N/A
- 亏损/扣非净利为负或不足 2 个年度点: G=N/A
- PEG = PE / (G*100)，仅当 PE>0 且 G>0 时有效；否则标 N/A 并附原因。

结果写 data/chain_peg.json: {code:{chain,slug,name,pe_ttm,g_cagr,peg,note}}
原始抓取缓存 data/_peg_cache.json(加速重跑)。
"""
import os, re, json, time
import inject_annual_reports as ia

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "chain_peg.json")
CACHE = os.path.join(DATA, "_peg_cache.json")
ANNUAL = os.path.join(DATA, "chain_annual_reports.json")
TARGET_CHAINS = ["ai", "innov", "robot", "metal"]

import akshare as ak

PROXY_ENV = dict(HTTP_PROXY="", HTTPS_PROXY="", http_proxy="", https_proxy="",
                 no_proxy="localhost,127.0.0.1")


def load_cache():
    if os.path.exists(CACHE):
        try:
            return json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_cache(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def is_ashare(code):
    return bool(re.fullmatch(r"\d{6}", str(code)))


def get_pe(code, cache):
    key = "pe_" + code
    if key in cache:
        return cache[key]
    val = None
    try:
        df = ak.stock_zh_valuation_baidu(symbol=code, indicator="市盈率(TTM)", period="近十年")
        if df is not None and len(df):
            v = df.iloc[-1].get("value")
            try:
                val = float(v)
            except Exception:
                val = None
    except Exception:
        val = None
    cache[key] = val
    return val


def get_npy_cagr(code, cache):
    """返回 (cagr_float_or_None, note)"""
    key = "np_" + code
    if key in cache:
        return cache[key]
    res = (None, "数据不足")
    try:
        df = ak.stock_financial_analysis_indicator(symbol=code, start_year="2019")
        if df is not None and len(df):
            ye_rows = df[df["日期"].astype(str).str.endswith("-12-31")].copy()
            if len(ye_rows) >= 2:
                ye_rows["_y"] = ye_rows["日期"].astype(str).str[:4].astype(int)
                ye_rows = ye_rows.sort_values("_y")
                col = "扣除非经常性损益后的净利润(元)"
                if col in ye_rows.columns:
                    vals = list(zip(ye_rows["_y"], ye_rows[col].astype(float)))
                    # 取最近 ~4 个年度点
                    vals = vals[-4:]
                    y0, v0 = vals[0]
                    y1, v1 = vals[-1]
                    if v0 > 0 and v1 > 0 and (y1 - y0) > 0:
                        cagr = (v1 / v0) ** (1.0 / (y1 - y0)) - 1
                        res = (cagr, "扣非净利CAGR %d-%d" % (y0, y1))
                    elif v1 <= 0:
                        res = (None, "近期扣非净利为负")
                    else:
                        res = (None, "净利基数非正")
                else:
                    res = (None, "无扣非净利列")
            else:
                res = (None, "年度点不足")
    except Exception as e:
        res = (None, "抓取失败:%s" % type(e).__name__)
    cache[key] = res
    return res


def main():
    csc = ia.extract_chain_slug_code()
    ann = {c["code"]: c["name"] for c in json.load(open(ANNUAL, encoding="utf-8"))}
    cache = load_cache()
    out = {}
    for (chain, slug), code in sorted(csc.items()):
        if chain not in TARGET_CHAINS:
            continue
        if not is_ashare(code):
            out[code] = dict(chain=chain, slug=slug, name=ann.get(code, slug),
                             pe_ttm=None, g_cagr=None, peg=None,
                             note="港股/非A股(百度估值不覆盖)")
            continue
        name = ann.get(code, slug)
        pe = get_pe(code, cache)
        g, gnote = get_npy_cagr(code, cache)
        peg = None
        note = gnote
        if pe is not None and pe > 0 and g is not None and g > 0:
            peg = pe / (g * 100.0)
            note = "PEG=PE(%.1f)÷增速(%.0f%%)" % (pe, g * 100)
        elif pe is None:
            note = "PE缺失;" + gnote
        elif pe <= 0:
            note = "PE≤0(亏损);" + gnote
        out[code] = dict(chain=chain, slug=slug, name=name, pe_ttm=pe,
                         g_cagr=(g * 100.0 if g is not None else None),
                         peg=(round(peg, 2) if peg is not None else None),
                         note=note)
        print("  %s %s: PE=%s G=%s PEG=%s | %s" % (
            code, name, pe, (round(g * 100, 1) if g else g), peg, note))
        time.sleep(0.15)
    save_cache(cache)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n=== PEG 采集完成 ===")
    print("目标公司数:", len(out))
    valid = sum(1 for v in out.values() if v.get("peg") is not None)
    print("有效 PEG:", valid, " N/A:", len(out) - valid)


if __name__ == "__main__":
    main()
