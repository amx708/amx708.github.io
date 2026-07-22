# -*- coding: utf-8 -*-
"""
fetch_research_reports.py  ——  伯克希尔数据中心 · chain 管线步骤

采集各家产业链公司的「券商研报」链接，写入 data/chain_research_reports.json。

数据源：AkShare -> stock_research_report_em (东方财富 个股研报)
版权规避：研报为券商版权内容，本脚本只采集东方财富研报 PDF 直链（pdf.dfcfw.com，
          文件托管在东方财富服务器），本仓库零托管、零落地，符合站点「不落地文件」约定。

范围：沿用年报那批公司；仅采集 A 股（6 位代码）。港股(含 .HK)东方财富该接口取不到，
      跳过，由注入器按「无数据」处理（页面不挂研报区）。

输出结构（data/chain_research_reports.json）：
[
  {
    "code": "600519",
    "name": "贵州茅台",
    "reports": [
      {"date": "2026-07-20", "title": "...", "org": "群益证券",
       "rating": "持有", "url": "https://pdf.dfcfw.com/..."}
    ]
  }
]

用法：
    python fetch_research_reports.py
"""
import json
import os
import sys
import time
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
ANNUAL = os.path.join(ROOT, "data", "chain_annual_reports.json")
OUT = os.path.join(ROOT, "data", "chain_research_reports.json")
MAX_PER = 20  # 每家公司最多保留最新 N 条


def load_akshare():
    try:
        import akshare as ak
        return ak
    except Exception as e:  # noqa
        print("ERROR: 未安装 akshare，无法采集研报。请先 pip install akshare。")
        sys.exit(1)


def is_ashare(code):
    return bool(code) and not code.upper().endswith(".HK")


def fetch_with_retry(ak, code, tries=4, base=1.5):
    """东方财富接口在连续请求下偶发 SSL EOF（疑似限流/TLS 抖动），
    失败处做指数退避重试，避免整家公司研报丢失。"""
    last = None
    for t in range(tries):
        try:
            return ak.stock_research_report_em(symbol=code)
        except Exception as e:  # noqa
            last = e
            wait = base * (2 ** t) + random.uniform(0, 0.5)
            print("    [retry %d/%d] %s : %s (%.1fs)" % (t + 1, tries, code, e, wait))
            time.sleep(wait)
    raise last


def main():
    ak = load_akshare()
    annual = json.load(open(ANNUAL, encoding="utf-8"))
    companies = [c for c in annual if is_ashare(c.get("code"))]
    print("待采集 A 股公司数 :", len(companies))

    results = []
    ok = skip = fail = 0
    for c in companies:
        code = c["code"]
        name = c.get("name", code)
        try:
            df = fetch_with_retry(ak, code)
        except Exception as e:  # noqa
            print("  [FAIL] %s %s : %s" % (code, name, e))
            fail += 1
            results.append({"code": code, "name": name, "reports": [], "error": str(e)[:120]})
            time.sleep(0.6)
            continue

        if df is None or len(df) == 0:
            print("  [SKIP] %s %s : 东方财富无研报" % (code, name))
            skip += 1
            results.append({"code": code, "name": name, "reports": []})
            time.sleep(0.3)
            continue

        rows = []
        for _, r in df.iterrows():
            rows.append({
                "date": str(r.get("日期", "")).strip(),
                "title": str(r.get("报告名称", "")).strip(),
                "org": str(r.get("机构", "")).strip(),
                "rating": str(r.get("东财评级", "")).strip(),
                "url": str(r.get("报告PDF链接", "")).strip(),
            })
        # 按日期倒序，去空 url，截断
        rows = [x for x in rows if x["url"]]
        rows.sort(key=lambda x: x["date"], reverse=True)
        rows = rows[:MAX_PER]
        print("  [OK]   %s %s : %d 条 (取最新 %d)" % (code, name, len(df), len(rows)))
        results.append({"code": code, "name": name, "reports": rows})
        time.sleep(0.6 + random.uniform(0, 0.4))  # 轻量限速 + 抖动，避免被东方财富限流

    # 写 JSON
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    total_reports = sum(len(x["reports"]) for x in results)
    with_reports = sum(1 for x in results if x["reports"])
    print("\n=== 研报采集完成 ===")
    print("公司总数   :", len(results))
    print("有研报公司 :", with_reports)
    print("无研报公司 :", skip)
    print("失败公司   :", fail)
    print("研报总条数 :", total_reports)
    print("输出文件   :", OUT)


if __name__ == "__main__":
    main()
