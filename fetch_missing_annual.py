# -*- coding: utf-8 -*-
"""
fetch_missing_annual.py —— 补齐 chain 管线里「缺年报链接」的 A 股公司

自动从仓库结构发现缺失公司：
1. 用 AST 解析 5 个 build 脚本，拿到 (chain, slug) -> {code, name} 映射；
2. 遍历所有 berkshire-*-chain-*.html，凡 code 是 6 位 A 股、且不在现有
   data/chain_annual_reports.json 里的，用 AkShare cninfo 拉「年度报告」直链；
3. 合并进 JSON（并重生成 Markdown 总表），供 inject_annual_reports.py 重跑注入。

注意：外资巨头(ali/amazon/apple/...)在映射里 code=None，自动跳过；
      港股已在 JSON 里，自动跳过。
"""
import ast
import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "chain_annual_reports.json")
BUILD_SCRIPTS = [
    "_build_five_chains.py", "_build_three_chains.py",
    "_build_robot_chain_pages.py", "_build_bank_chain_pages.py", "_build_chip_game.py",
]
MD_OUT = os.path.join(ROOT, "产业链公司_年报链接总表.md")


def const(v):
    return v.value if isinstance(v, ast.Constant) else None


def fields(node):
    if isinstance(node, ast.Dict):
        return {const(k): v.value for k, v in zip(node.keys, node.values) if isinstance(v, ast.Constant)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
        return {k.arg: (k.value.value if isinstance(k.value, ast.Constant) else None) for k in node.keywords}
    return {}


def extract_meta():
    """(chain, slug) -> {code, name}"""
    out = {}
    BAIJIU = {
        "maotai": ("600519", "贵州茅台"), "wuliangye": ("000858", "五粮液"),
        "fenjiu": ("600809", "山西汾酒"), "luzhou": ("000568", "泸州老窖"),
        "yanghe": ("002304", "洋河股份"), "gujing": ("000596", "古井贡酒"),
        "shunxin": ("000860", "顺鑫农业"), "jinshiyuan": ("603369", "今世缘"),
        "kouzijiao": ("603589", "口子窖"), "shede": ("600702", "舍得酒业"),
        "jiugui": ("000799", "酒鬼酒"), "yingjia": ("603198", "迎驾贡酒"),
        "shuijingfang": ("600779", "水井坊"),
    }
    for sl, (co, nm) in BAIJIU.items():
        out[("baijiu", sl)] = {"code": co, "name": nm}

    for s in BUILD_SCRIPTS:
        path = os.path.join(ROOT, s)
        if not os.path.exists(path):
            continue
        tree = ast.parse(open(path, encoding="utf-8").read())
        vardict = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                vardict[node.targets[0].id] = node.value
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "append" and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "CHAINS" and node.args):
                arg = node.args[0]
                if isinstance(arg, ast.Name) and arg.id in vardict:
                    arg = vardict[arg.id]
                if not isinstance(arg, ast.Dict):
                    continue
                f = fields(arg)
                ckey = f.get("key")
                comps = None
                for k, v in zip(arg.keys, arg.values):
                    if const(k) == "companies" and isinstance(v, ast.List):
                        comps = v
                        break
                if not ckey or not comps:
                    continue
                for cd in comps.elts:
                    cf = fields(cd)
                    sl, co, nm = cf.get("slug"), cf.get("code"), cf.get("name")
                    if isinstance(sl, str) and isinstance(co, str):
                        out[(ckey, sl)] = {"code": co, "name": nm}
        if "company_data" in vardict and isinstance(vardict["company_data"], ast.List):
            for cd in vardict["company_data"].elts:
                cf = fields(cd)
                sl, co, nm = cf.get("slug"), cf.get("code"), cf.get("name")
                if isinstance(sl, str) and isinstance(co, str):
                    out[("bank", sl)] = {"code": co, "name": nm}
    return out


def get_reports(code):
    import akshare as ak
    df = ak.stock_zh_a_disclosure_report_cninfo(
        symbol=code, market="沪深京", keyword="", category="年报",
        start_date="20080101", end_date="20261231")
    out = []
    for _, r in df.iterrows():
        title = r["公告标题"]
        if "年度报告" in title and "摘要" not in title:
            aid = re.search(r"announcementId=(\d+)", r["公告链接"])
            dt = str(r["公告时间"])[:10]
            aid = aid.group(1) if aid else ""
            pdf = ("https://static.cninfo.com.cn/finalpage/%s/%s.PDF" % (dt, aid)) if aid else ""
            ym = re.search(r"(\d{4})年年度报告", title)
            yr = ym.group(1) if ym else (title[:4] if title[:4].isdigit() else "")
            out.append({"year": yr, "title": title, "date": dt, "pdf": pdf, "detail": r["公告链接"]})
    return out


def main():
    meta = extract_meta()
    data = json.load(open(DATA, encoding="utf-8"))
    have = set(c["code"] for c in data)
    pages = sorted(glob.glob(os.path.join(ROOT, "berkshire-*-chain-*.html")))

    to_fetch = []
    for p in pages:
        m = re.search(r"berkshire-([a-z]+)-chain-([A-Za-z0-9_\-]+)\.html$", p)
        if not m:
            continue
        info = meta.get((m.group(1), m.group(2)))
        if not info:
            continue
        code = info["code"]
        if not code or ".hk" in code.lower() or not re.fullmatch(r"\d{6}", code):
            continue
        if code in have:
            continue
        to_fetch.append((m.group(2), code, info["name"]))

    print("待补齐 A 股公司数 :", len(to_fetch))
    for sl, co, nm in to_fetch:
        print("   %-12s %-8s %s" % (sl, co, nm))

    new_entries = []
    for slug, code, name in to_fetch:
        try:
            reps = get_reports(code)
        except Exception as e:
            print("  [FAIL] %s %s : %s" % (code, name, e), file=sys.stderr)
            reps = []
        new_entries.append({"slug": slug, "name": name, "code": code, "reports": reps})
        print("  [OK] %s %s -> %d 份" % (code, name, len(reps)))
        time.sleep(0.35)

    by_code = {c["code"]: c for c in data}
    added = 0
    for e in new_entries:
        if e["code"] in by_code:
            by_code[e["code"]]["reports"] = e["reports"]
        else:
            data.append(e)
            added += 1
    json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("已合并 %d 条新公司 -> %s（JSON 现有 %d 家）" % (added, DATA, len(data)))

    # 重生成 Markdown 总表
    regen_md(data, MD_OUT)
    print("Markdown 总表已更新 ->", MD_OUT)


def regen_md(data, path):
    lines = ["# 产业链公司 年报链接总表", "",
             "> 数据来源：巨潮资讯网(cninfo) 官方披露，经 AkShare 拉取并构造直达 PDF。",
             "> 港股给港交所披露易检索入口。本表仅作链接聚合，不托管文件。", ""]
    lines.append("| 公司 | 代码 | 年报份数 | 跳转 |")
    lines.append("|------|------|---------|------|")
    for c in data:
        n = len(c.get("reports", []))
        lines.append("| %s | %s | %d | [#%s](#%s) |" % (c["name"], c["code"], n, c["name"], c["slug"]))
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


if __name__ == "__main__":
    main()
