# -*- coding: utf-8 -*-
"""
inject_annual_reports.py  ——  伯克希尔数据中心 · chain 管线步骤

把 data/chain_annual_reports.json（各公司历年年报链接总表）注入到每家公司的
chain 详情页（berkshire-{chain}-chain-{slug}.html）的「年报」区。

设计要点：
1. 关联键用「股票代码」而非 slug：
   - 年报总表(JSON) 的 slug 是自动生成的，与页面真实文件名 slug 不一致；
   - 页面真实 slug 来自 build 脚本，但 JSON 没有可靠 slug。
   - 因此用 build 脚本里的 slug->code 映射，再用 code 去 JSON 里取年报。
2. 兼容两套页面模板：
   - 标准页：结尾有 <div class="back-bar">，注入到它之前；
   - 银行业页：结尾是 <footer>，注入到最后一个 <footer> 之前；
   - 兜底：注入到 </body> 之前。
3. 幂等：页面已含 id="annual-reports" 则跳过（重跑不重复）。
4. A 股用巨潮 PDF 直链；港股(代码含 .HK)用港交所披露易检索入口。

用法：
    python inject_annual_reports.py
"""
import ast
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "chain_annual_reports.json")
BUILD_SCRIPTS = [
    "_build_five_chains.py",
    "_build_three_chains.py",
    "_build_robot_chain_pages.py",
    "_build_bank_chain_pages.py",
    "_build_chip_game.py",
]


def const(v):
    return v.value if isinstance(v, ast.Constant) else None


def fields(node):
    """从 dict 字面量 或 dict(...) 调用里取出 key->value(str) 映射。"""
    if isinstance(node, ast.Dict):
        out = {}
        for k, v in zip(node.keys, node.values):
            if isinstance(v, ast.Constant):
                out[const(k)] = v.value
        return out
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
        return {k.arg: (k.value.value if isinstance(k.value, ast.Constant) else None) for k in node.keywords}
    return {}


def extract_chain_slug_code():
    """AST 解析 build 脚本，建立 (chain, slug) -> code 映射。

    处理三种结构：
    1) CHAINS = [] ; ... ; CHAINS.append(power)  —— power 是含 'key' + 'companies' 的 dict 变量
    2) bank 脚本：顶层 company_data = [dict(slug=..., code=...)]，chain 固定 'bank'
    3) 白酒链代码不在脚本结构化字段里，用一份稳定的硬编码 slug->code 备查
    """
    out = {}

    # 3) 白酒硬编码（13 家 A 股，代码稳定；用于后续补齐白酒年报时按 (baijiu,slug) 命中）
    BAIJIU = {
        "maotai": "600519", "wuliangye": "000858", "fenjiu": "600809", "luzhou": "000568",
        "yanghe": "002304", "gujing": "000596", "shunxin": "000860", "jinshiyuan": "603369",
        "kouzijiao": "603589", "shede": "600702", "jiugui": "000799", "yingjia": "603198",
        "shuijingfang": "600779",
    }
    for sl, co in BAIJIU.items():
        out[("baijiu", sl)] = co

    for s in BUILD_SCRIPTS:
        path = os.path.join(ROOT, s)
        if not os.path.exists(path):
            continue
        src = open(path, encoding="utf-8").read()
        tree = ast.parse(src)

        # 收集模块级变量 -> dict 节点（用于解析 CHAINS.append(power)）
        vardict = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                vardict[node.targets[0].id] = node.value

        # 1) CHAINS.append(...) -> 解析变量 / 字面量
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
                # 找 companies 字段对应节点
                for k, v in zip(arg.keys, arg.values):
                    if const(k) == "companies" and isinstance(v, ast.List):
                        comps = v
                        break
                if not ckey or not comps:
                    continue
                for cd in comps.elts:
                    cf = fields(cd)
                    sl, co = cf.get("slug"), cf.get("code")
                    if isinstance(sl, str) and isinstance(co, str):
                        out[(ckey, sl)] = co

        # 2) bank 脚本 company_data 列表
        if "company_data" in vardict and isinstance(vardict["company_data"], ast.List):
            for cd in vardict["company_data"].elts:
                cf = fields(cd)
                sl, co = cf.get("slug"), cf.get("code")
                if isinstance(sl, str) and isinstance(co, str):
                    out[("bank", sl)] = co

    return out


def build_section(reports, is_hk):
    """生成「年报」区 HTML（内联样式，幂等靠外层 id 守卫）。"""
    if is_hk:
        r = reports[0]
        return (
            '<div id="annual-reports" style="margin-top:28px;padding-top:10px">'
            '<div style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:10px;'
            'display:flex;align-items:center;gap:8px"><span style="font-size:18px">📄</span> '
            '历年年报（港交所披露易）</div>'
            '<p style="font-size:12.5px;color:#64748b;margin:0 0 12px;line-height:1.6">'
            '港股公司年报通过港交所「披露易」检索，点击下方入口按年份查看 / 下载 PDF。'
            '本页仅作链接聚合，不托管文件，最新以公司公告为准。</p>'
            '<div style="display:flex;flex-wrap:wrap;gap:8px">'
            '<a href="%s" target="_blank" rel="noopener" '
            'style="display:inline-block;padding:7px 14px;background:#f8fafc;border:1px solid #e2e8f0;'
            'border-radius:8px;font-size:13px;color:#1d4ed8;text-decoration:none">'
            '📑 港交所披露易 · 年报检索入口</a></div></div>' % r["pdf"]
        )
    # A 股：按年份倒序
    items = sorted(reports, key=lambda x: x.get("year", ""), reverse=True)
    chips = []
    for r in items:
        yr = r.get("year", "")
        title = r.get("title") or ("%s 年年度报告" % yr)
        pdf = r.get("pdf") or r.get("detail") or ""
        if not pdf:
            continue
        label = ("%s 年报" % yr) if yr else title
        chips.append(
            '<a href="%s" target="_blank" rel="noopener" '
            'style="display:inline-block;padding:6px 12px;background:#f8fafc;border:1px solid #e2e8f0;'
            'border-radius:8px;font-size:13px;color:#1d4ed8;text-decoration:none">%s</a>' % (pdf, label)
        )
    if not chips:
        return ""
    return (
        '<div id="annual-reports" style="margin-top:28px;padding-top:10px">'
        '<div style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:10px;'
        'display:flex;align-items:center;gap:8px"><span style="font-size:18px">📄</span> '
        '历年年报（巨潮资讯网）</div>'
        '<p style="font-size:12.5px;color:#64748b;margin:0 0 12px;line-height:1.6">'
        '点击年份直达该公司年度报告原文 PDF（来源：巨潮资讯网）。本页仅作链接聚合，不托管文件，'
        '最新以公司公告为准。</p>'
        '<div style="display:flex;flex-wrap:wrap;gap:8px">%s</div></div>' % "".join(chips)
    )


def inject_into_page(path, html, section):
    """在合适的锚点前插入 section；幂等守卫。返回 (new_html, injected_bool)。"""
    if 'id="annual-reports"' in html:
        return html, False
    anchor = None
    if '<div class="back-bar">' in html:
        anchor = '<div class="back-bar">'
    elif '<footer>' in html:
        # 最后一个 footer
        idx = html.rfind('<footer>')
        anchor = html[idx:idx + len('<footer>')]
    if anchor:
        new_html = html.replace(anchor, section + "\n" + anchor, 1)
    else:
        new_html = html.replace('</body>', section + "\n</body>", 1)
    return new_html, True


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    code2rep = {c["code"]: c for c in data}
    chain_slug_code = extract_chain_slug_code()

    pages = sorted(glob.glob(os.path.join(ROOT, "berkshire-*-chain-*.html")))
    done, skipped_no_data, skipped_existing, failed = 0, 0, 0, 0
    injected_list, no_data_list = [], []

    for p in pages:
        m = re.search(r"berkshire-([a-z]+)-chain-([A-Za-z0-9_\-]+)\.html$", p)
        if not m:
            continue
        chain, slug = m.group(1), m.group(2)
        code = chain_slug_code.get((chain, slug))
        rep = code2rep.get(code) if code else None
        html = open(p, encoding="utf-8").read()

        if not rep or not rep.get("reports"):
            skipped_no_data += 1
            no_data_list.append((os.path.basename(p), chain, slug, code))
            continue

        is_hk = any(r.get("hk") for r in rep["reports"]) or ".hk" in code.lower()
        section = build_section(rep["reports"], is_hk)
        if not section:
            skipped_no_data += 1
            continue
        new_html, injected = inject_into_page(p, html, section)
        if injected:
            open(p, "w", encoding="utf-8").write(new_html)
            done += 1
            injected_list.append((os.path.basename(p), rep["name"], len(rep["reports"])))
        else:
            skipped_existing += 1

    print("=== 年报区注入完成 ===")
    print("成功注入页面数 :", done)
    print("已存在跳过     :", skipped_existing)
    print("无年报数据跳过 :", skipped_no_data)
    print()
    print("--- 已注入（示例前 20）---")
    for f, n, c in injected_list[:20]:
        print("  %-45s %s (%d份)" % (f, n, c))
    print()
    print("--- 无数据页面（%d 个，多为银行/白酒/外资巨头，待补齐）---" % len(no_data_list))
    for f, chain, slug, code in no_data_list:
        print("  %-45s chain=%s slug=%s code=%s" % (f, chain, slug, code))


if __name__ == "__main__":
    main()
