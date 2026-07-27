# -*- coding: utf-8 -*-
"""
_fetch_dividend_compound.py —— 伯克希尔数据中心 · P2-D 增强
给现金牛链(煤炭/银行/电力)的 A 股公司补「分红再投 10 年复利」情景。

方法(诚实、零编造):
- 后复权(hfq)月线 10 年：ak.stock_zh_a_hist(symbol, period="monthly", start_date="20160101", adjust="hfq")
  hfq 价已内含分红再投(及送转)，故 hfq 回报 = 买入持有+分红再投的总回报。
- 不复权("")月线：纯资本回报(价回报)。
- 分红再投贡献 = hfq 回报 − 价回报。
- 年化 = (1+回报)^(1/年数) − 1。

结果写 data/chain_dividend_compound.json:
  {code:{chain,slug,name,years,hfq_ret,price_ret,div_contrib,ann_hfq,ann_price,note}}
原始抓取缓存 data/_div_cache.json。
"""
import os, re, json, time
import inject_annual_reports as ia
import akshare as ak

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "chain_dividend_compound.json")
CACHE = os.path.join(DATA, "_div_cache.json")
ANNUAL = os.path.join(DATA, "chain_annual_reports.json")
TARGET_CHAINS = ["coal", "bank", "power"]
START = "20160101"


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


def _prefix(code):
    return ("sh" if code[0] == "6" else "sz") + code


def _try_source(fn, code, adj):
    for attempt in range(4):
        try:
            df = fn(code, adj)
            if df is not None and len(df) >= 30:
                first = float(df.iloc[0]["close"])
                last = float(df.iloc[-1]["close"])
                d0 = str(df.iloc[0]["date"]); d1 = str(df.iloc[-1]["date"])
                return dict(first=first, last=last, d0=d0, d1=d1, n=len(df))
        except Exception:
            pass
        time.sleep(1.2 + attempt * 1.2 + (hash(code) % 7) * 0.2)
    return None


def fetch_hist(code, adj, cache):
    key = "hist_%s_%s" % (adj, code)
    if key in cache:
        return cache[key]   # 仅成功结果入缓存
    res = None
    # 主源：新浪 stock_zh_a_daily（后复权口径稳定）；兜底：东财 stock_zh_a_hist
    sina_sym = _prefix(code)
    res = _try_source(
        lambda c, a: ak.stock_zh_a_daily(symbol=sina_sym, start_date=START,
                                        end_date="20260701", adjust=a),
        code, adj)
    if res is None:
        res = _try_source(
            lambda c, a: ak.stock_zh_a_hist(symbol=code, period="monthly",
                                           start_date=START, end_date="20260701", adjust=a),
            code, adj)
    if res is not None:
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
                             note="港股/非A股")
            continue
        name = ann.get(code, slug)
        hf = fetch_hist(code, "hfq", cache)
        pr = fetch_hist(code, "", cache)
        if not hf or not pr:
            out[code] = dict(chain=chain, slug=slug, name=name, note="数据不足(上市<10年或抓取失败)")
            print("  %s %s: 数据不足" % (code, name))
            continue
        hfq_ret = hf["last"] / hf["first"] - 1
        price_ret = pr["last"] / pr["first"] - 1
        years = max((int(hf["d1"][:4]) - int(hf["d0"][:4])), 1)
        ann_hfq = (1 + hfq_ret) ** (1.0 / years) - 1
        ann_price = (1 + price_ret) ** (1.0 / years) - 1
        div_contrib = hfq_ret - price_ret
        out[code] = dict(chain=chain, slug=slug, name=name, years=years,
                         hfq_ret=round(hfq_ret, 4), price_ret=round(price_ret, 4),
                         div_contrib=round(div_contrib, 4),
                         ann_hfq=round(ann_hfq, 4), ann_price=round(ann_price, 4),
                         note="")
        print("  %s %s: 分红再投年化%.1f%% / 价回报年化%.1f%% / 分红贡献%+.0f%%" % (
            code, name, ann_hfq * 100, ann_price * 100, div_contrib * 100))
        time.sleep(0.12)
    save_cache(cache)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n=== 分红再投复利采集完成 ===")
    print("目标公司:", len(out))
    ok = sum(1 for v in out.values() if v.get("ann_hfq") is not None and "note" not in v or (v.get("note") == ""))
    print("有效:", sum(1 for v in out.values() if v.get("note") == ""))


if __name__ == "__main__":
    main()
