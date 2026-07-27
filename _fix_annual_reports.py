# -*- coding: utf-8 -*-
"""
_fix_annual_reports.py  ——  修正 chain_annual_reports.json 数据质量

处理三类问题：
1. year 字段不是 4 位数字（旧脚本把公司名塞进 year）。
2. A+H 公司混进 H 股年报 / 摘要，导致同年重复。
3. 年份序列断层（缺某年年报）。

流程：
- 对现有 A 股记录：从 title 提取 4 位年份 → 过滤 H 股/摘要 → 按年去重（优先保留 A 股年报全文、非修订版）。
- 仍缺年份或仍有断层的 A 股公司，用 akshare 重新拉取全量年报并归一化。
- 保存 JSON，并重写 Markdown 总表。
"""
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "chain_annual_reports.json")
MD_OUT = os.path.join(ROOT, "产业链公司_年报链接总表.md")

YEAR_RE = re.compile(r"(\d{4})年(?:度)?(?:报告|年报)")
DIGIT4_RE = re.compile(r"\d{4}")


def extract_year(title, date=None):
    """从标题中提取最可能的年报年份；标题缺年份时按披露日期推断（上年报）。"""
    title = str(title or "")
    # 优先匹配 "2025年年度报告" / "2025年度报告" / "2025年报"
    m = YEAR_RE.search(title)
    if m:
        y = int(m.group(1))
        if 1990 <= y <= 2030:
            return str(y)
    # 兜底：取所有 4 位数字中在合理范围的
    candidates = [int(y) for y in DIGIT4_RE.findall(title)]
    candidates = [y for y in candidates if 1990 <= y <= 2030]
    if candidates:
        # 对 "中国神华2025年度报告" 这类，max 就是年份
        return str(max(candidates))
    # 标题只有 "年报全文" 等：按披露日期减 1 年（A 股年报通常次年 4 月披露）
    if date and len(str(date)) >= 4:
        try:
            y = int(str(date)[:4]) - 1
            if 1990 <= y <= 2030:
                return str(y)
        except ValueError:
            pass
    return ""


def is_h_share(title):
    t = str(title or "")
    return "H股" in t or t.startswith("H股公告") or "港股公告" in t


def is_summary(title):
    t = str(title or "")
    return "摘要" in t and "全文" not in t


def score_report(r):
    """同年多条时，分高者保留。"""
    title = r.get("title", "")
    score = 0
    if "年度报告全文" in title:
        score += 10
    elif "年度报告" in title or "年报" in title:
        score += 5
    # 优先非修订/更正/补充
    if any(w in title for w in ("修订", "更正", "补充")):
        score -= 3
    return score


def normalize_reports(reports):
    """修正年份、过滤 H 股/摘要、按年去重。返回排序后的列表（年份倒序）。"""
    cleaned = []
    for r in reports:
        title = r.get("title", "")
        # 去掉 H 股年报和摘要
        if is_h_share(title) or is_summary(title):
            continue
        yr = extract_year(title, r.get("date"))
        if yr:
            r = dict(r)
            r["year"] = yr
        cleaned.append(r)

    # 按年分组，取评分最高、同分取日期最早
    by_year = {}
    for r in cleaned:
        yr = str(r.get("year", "")).strip()
        if not re.fullmatch(r"\d{4}", yr):
            continue
        if yr not in by_year:
            by_year[yr] = r
        else:
            old = by_year[yr]
            if score_report(r) > score_report(old):
                by_year[yr] = r
            elif score_report(r) == score_report(old) and r.get("date", "") < old.get("date", ""):
                by_year[yr] = r

    return sorted(by_year.values(), key=lambda x: x.get("year", ""), reverse=True)


def get_reports(code):
    """用 akshare 从巨潮拉取某 A 股公司的全部年报。"""
    import akshare as ak
    df = ak.stock_zh_a_disclosure_report_cninfo(
        symbol=code, market="沪深京", keyword="", category="年报",
        start_date="20080101", end_date="20261231")
    out = []
    for _, r in df.iterrows():
        title = r["公告标题"]
        if "年度报告" not in title and "年报" not in title:
            continue
        if is_h_share(title) or is_summary(title):
            continue
        aid = re.search(r"announcementId=(\d+)", r["公告链接"])
        dt = str(r["公告时间"])[:10]
        aid = aid.group(1) if aid else ""
        pdf = ("https://static.cninfo.com.cn/finalpage/%s/%s.PDF" % (dt, aid)) if aid else ""
        yr = extract_year(title, dt)
        out.append({"year": yr, "title": title, "date": dt, "pdf": pdf, "detail": r["公告链接"]})
    return out


def missing_years(reports):
    """返回 min~max 之间缺失的年份列表。"""
    years = [int(r["year"]) for r in reports if re.fullmatch(r"\d{4}", str(r.get("year", "")))]
    if not years:
        return []
    mn, mx = min(years), max(years)
    return sorted(set(range(mn, mx + 1)) - set(years))


def regen_md(data, path):
    lines = ["# 产业链公司 年报链接总表", "",
             "> 数据来源：巨潮资讯网(cninfo) 官方披露，经 AkShare 拉取并构造直达 PDF。",
             "> 港股给港交所披露易检索入口。本表仅作链接聚合，不托管文件。", ""]
    lines.append("| 公司 | 代码 | 年报份数 | 跳转 |")
    lines.append("|------|------|---------|------|")
    for c in data:
        n = len(c.get("reports", []))
        slug = c.get("slug", c.get("name", ""))
        lines.append("| %s | %s | %d | [#%s](#%s) |" % (c["name"], c["code"], n, c["name"], slug))
    lines.append("")
    for c in data:
        lines.append("")
        lines.append("## %s  (%s)" % (c["name"], c["code"]))
        lines.append("")
        if c.get("hk"):
            lines.append("- [%s](%s)" % (c["reports"][0]["title"], c["reports"][0]["pdf"]))
            continue
        for r in sorted(c.get("reports", []), key=lambda x: x.get("year", ""), reverse=True):
            lines.append("- %s ：[%s](%s)" % (r.get("year", ""), r.get("title", ""), r.get("pdf") or r.get("detail")))
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def main():
    # 备份
    backup = DATA + ".bak"
    with open(DATA, "rb") as f:
        open(backup, "wb").write(f.read())
    print("已备份原 JSON ->", backup)

    data = json.load(open(DATA, encoding="utf-8"))
    by_code = {c["code"]: c for c in data}

    # 第一步：归一化所有现有 A 股记录
    for c in data:
        if c.get("hk"):
            continue
        c["reports"] = normalize_reports(c.get("reports", []))

    # 第二步：找出仍需重新抓取的公司（仍有坏年份 或 有断层）
    to_refetch = []
    for c in data:
        if c.get("hk"):
            continue
        code = c["code"]
        if not re.fullmatch(r"\d{6}", code):
            continue
        bad = any(not re.fullmatch(r"\d{4}", str(r.get("year", ""))) for r in c.get("reports", []))
        miss = missing_years(c.get("reports", []))
        if bad or miss:
            to_refetch.append((code, c.get("name", ""), miss))

    print("需重新抓取的公司数:", len(to_refetch))
    for code, name, miss in to_refetch:
        print("  %s %s 缺 %s" % (code, name, miss))

    # 第三步：重新抓取并归一化
    for code, name, miss in to_refetch:
        try:
            reps = get_reports(code)
            by_code[code]["reports"] = normalize_reports(reps)
            print("[OK] %s %s -> %d 份" % (code, name, len(by_code[code]["reports"])))
        except Exception as e:
            print("[FAIL] %s %s : %s" % (code, name, e), file=sys.stderr)
        time.sleep(0.35)

    # 第四步：最终归一化并保存
    for c in data:
        if c.get("hk"):
            continue
        c["reports"] = normalize_reports(c.get("reports", []))

    json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("已保存 ->", DATA)

    regen_md(data, MD_OUT)
    print("Markdown 总表已更新 ->", MD_OUT)


if __name__ == "__main__":
    main()
