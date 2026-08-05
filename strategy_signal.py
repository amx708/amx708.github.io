# -*- coding: utf-8 -*-
"""
strategy_signal.py  —— 用 akshare(免费) 复刻 v7 小市值选股信号
================================================================
每周由 GitHub Action 调用一次：
  1. 取中证1000成分股
  2. 财务过滤：营收>1亿 & 净利润>0 & 净资产>0
  3. 排除：ST / 科创(688) / 北交(8,4) / 高价(>100) / 停牌
  4. 按总市值升序取最小的 8 只
  5. 计算当前 8 只近一年等权组合表现
  6. 写入 data.json（供 generate_site.py 生成网页）
akshare 无 token，全程无需密钥。
"""
import os, json, time, datetime as dt
import pandas as pd

try:
    import akshare as ak
except Exception as e:
    print("[错误] 未安装 akshare: %s" % e)
    raise

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(OUT_DIR, "data.json")

HOLD_NUM = 8
MCAP_CEILING = 200
PRICE_CAP = 100.0
REVENUE_MIN = 1e8
REPORT_DATES = ["20260331", "20251231", "20250930", "20250630"]


def norm_code(c):
    """统一成 6 位代码：去空格、去后缀、零填充"""
    s = str(c).strip().split(".")[0]
    return s.zfill(6)


def col(df, *kw):
    """按关键字匹配列名（兼容 akshare 不同版本）"""
    for c in df.columns:
        if all(k in c for k in kw):
            return c
    return None


def get_index_codes():
    try:
        df = ak.index_stock_cons_csindex(symbol="000852")
        if df is not None and not df.empty and "成分券代码" in df.columns:
            return [norm_code(c) for c in df["成分券代码"].tolist()]
    except Exception as e:
        print("[warn] index_stock_cons_csindex 失败: %s" % e)
    return []


def get_spot(max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            df = ak.stock_zh_a_spot_em()
            df["code"] = df["代码"].map(norm_code)
            return df
        except Exception as e:
            print("[warn] 行情(spot)获取失败（%d/%d）: %s" % (attempt, max_attempts, e))
            if attempt < max_attempts:
                time.sleep(5)
    raise RuntimeError("行情(spot)连续 %d 次获取失败" % max_attempts)


def get_fundamentals(report_date, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            yj = ak.stock_yjbb_em(date=report_date)
            zc = ak.stock_zcfz_em(date=report_date)
            yj["code"] = yj["股票代码"].map(norm_code)
            zc["code"] = zc["股票代码"].map(norm_code)
            return yj, zc
        except Exception as e:
            print("[warn] 财务(%s)获取失败（%d/%d）: %s" % (report_date, attempt, max_attempts, e))
            if attempt < max_attempts:
                time.sleep(5)
    raise RuntimeError("财务(%s)连续 %d 次获取失败" % (report_date, max_attempts))


def get_st_set():
    try:
        df = ak.stock_zh_a_st_em()
        return set(norm_code(c) for c in df["代码"].tolist())
    except Exception as e:
        print("[warn] ST列表获取失败: %s" % e)
        return set()


def select():
    today = dt.date.today()
    codes = get_index_codes()
    print("[选股] 中证1000成分数: %d" % len(codes))
    if not codes:
        return None
    code_set = set(codes)

    spot = get_spot()
    spot = spot[spot["code"].isin(code_set)].copy()
    print("[选股] 成分股行情数: %d" % len(spot))
    if spot.empty:
        return None

    yj = zc = None
    used_rd = None
    for rd in REPORT_DATES:
        try:
            yj, zc = get_fundamentals(rd)
            if yj is not None and not yj.empty:
                used_rd = rd
                break
        except Exception as e:
            print("[warn] 报告期 %s 获取失败: %s" % (rd, e))
    if yj is None:
        print("[错误] 财务数据全部获取失败")
        return None
    print("[选股] 使用报告期: %s" % used_rd)

    rev_c = col(yj, "营业总收入")
    np_c = col(yj, "净利润")
    eq_c = col(zc, "股东权益合计")
    print("[选股] 财务列: 营收=%s 净利=%s 权益=%s" % (rev_c, np_c, eq_c))
    if not rev_c or not np_c:
        print("[错误] 财务关键列缺失")
        return None

    fin = yj[["code", rev_c, np_c]].copy()
    fin.columns = ["code", "rev", "np"]
    if eq_c:
        fin = fin.merge(zc[["code", eq_c]], on="code", how="left")
        fin = fin.rename(columns={eq_c: "eq"})

    st_set = get_st_set()
    merged = spot.merge(fin, on="code", how="left")
    print("[选股] 合并后: %d" % len(merged))

    keep = []
    for _, r in merged.iterrows():
        code = str(r["code"])
        code6 = code
        if code6.startswith("688"):
            continue
        if code6.startswith("8") or code6.startswith("4"):
            continue
        if code in st_set:
            continue
        try:
            rev = float(r["rev"]); np_ = float(r["np"])
        except Exception:
            continue
        if pd.isna(rev) or pd.isna(np_) or rev <= REVENUE_MIN or np_ <= 0:
            continue
        if "eq" in merged.columns:
            eq = r.get("eq", None)
            if eq is not None and not pd.isna(eq) and float(eq) <= 0:
                continue
        try:
            price = float(r["最新价"])
        except Exception:
            continue
        if pd.isna(price) or price <= 0 or price > PRICE_CAP:
            continue
        try:
            mcap = float(r["总市值"])
        except Exception:
            continue
        if pd.isna(mcap):
            continue
        keep.append({"code": code, "name": r.get("名称", ""),
                     "price": price, "mcap_yi": mcap / 1e8,
                     "rev_yi": rev / 1e8, "np_yi": np_ / 1e8})
    print("[选股] 财务/板块过滤后: %d" % len(keep))

    keep.sort(key=lambda x: x["mcap_yi"])
    pool = keep[:MCAP_CEILING]
    selected = pool[:HOLD_NUM]
    print("[选股] 最终入选: %s" % ",".join(s["code"] for s in selected))
    return selected


def _hist_one(symbol, start, end, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                                    start_date=start, end_date=end, adjust="qfq")
            return df
        except Exception as e:
            print("[warn] %s 历史行情获取失败（%d/%d）: %s" % (symbol, attempt, max_attempts, e))
            if attempt < max_attempts:
                time.sleep(3)
    return None


def portfolio_curve(selected, today):
    """当前 8 只近一年等权组合指数（基期=100）"""
    start = (today - dt.timedelta(days=365)).strftime("%Y%m%d")
    end = today.strftime("%Y%m%d")
    frames = []
    for s in selected:
        df = _hist_one(s["code"], start, end)
        if df is None or df.empty:
            continue
        idx = (1 + df["收盘"].pct_change().fillna(0)).cumprod() * 100
        sub = pd.Series(idx.values, index=df["日期"].tolist(), name=s["code"])
        frames.append(sub)
    if not frames:
        return [], []
    mat = pd.concat(frames, axis=1).ffill().bfill()
    eq = mat.mean(axis=1)
    return eq.index.tolist(), [round(float(v), 2) for v in eq.tolist()]


def load_history():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history": []}


def main():
    today = dt.date.today()
    selected = select()
    if not selected:
        print("[结果] 未选出股票，保留历史")
        return
    curve_dates, curve_vals = portfolio_curve(selected, today)

    hist = load_history()
    snap = {
        "date": today.strftime("%Y-%m-%d"),
        "holdings": [{"code": s["code"], "name": s["name"],
                     "price": s["price"], "mcap_yi": round(s["mcap_yi"], 2),
                     "rev_yi": round(s["rev_yi"], 2), "np_yi": round(s["np_yi"], 2)}
                    for s in selected],
        "trailing_1y_return": round((curve_vals[-1] / curve_vals[0] - 1) * 100, 2) if curve_vals else None,
    }
    hist["history"].append(snap)
    hist["history"] = hist["history"][-52:]
    hist["updated"] = today.strftime("%Y-%m-%d")
    hist["current"] = snap
    hist["curve"] = {"dates": [str(d) for d in curve_dates], "values": curve_vals}

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)
    print("[完成] data.json 已更新，更新日期 %s" % hist["updated"])


if __name__ == "__main__":
    main()
