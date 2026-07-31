# -*- coding: utf-8 -*-
"""强制重写 16 家企业的深页「关键财务」6 行，从（现已正确的）co 页取值，无条件覆盖。

背景：_collect_missing_co.py 首跑因 akshare 单位缩放把 中科三环/富创精密 的
净利/经营现金流写成荒谬值，且 inject_financials 只替换「— 待采集」行，导致深页
残留脏值（co 页已被二跑覆盖为正确值，深页没动）。本脚本用 co 页真值无条件重写。
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _upgrade_frames as uf

DS = os.path.dirname(os.path.abspath(__file__))

# (chain_slug, code, chain_page_code)
PAIRS = [
    ("rare-earth", "600111", "bfxt"),
    ("rare-earth", "600010", "bggf"),
    ("rare-earth", "600259", "gsys"),
    ("rare-earth", "002056", "hddc"),
    ("rare-earth", "300748", "jlcy"),
    ("rare-earth", "600366", "nbys"),
    ("rare-earth", "600392", "shhe"),
    ("rare-earth", "600549", "xmwy"),
    ("rare-earth", "000795", "ylh"),
    ("rare-earth", "000831", "zgxt"),
    ("rare-earth", "300224", "zhmc"),
    ("rare-earth", "000970", "zkth"),
    ("semiconductor-chemical", "688106", "688106"),
    ("semiconductor-chemical", "688138", "688138"),
    ("semiconductor-equip", "688409", "fcjm"),
    ("semiconductor-equip", "688596", "zfkj"),
]

KEY_FIN_ROWS = ['营业总收入', '归母净利润', '毛利率', 'ROE（加权）', '资产负债率', '经营现金流净额']


def main():
    changed = []
    for slug, code, cslug in PAIRS:
        fin = uf.get_fin_from_co(slug, code)
        if not fin:
            print("NO CO for", slug, code)
            continue
        path = os.path.join(DS, "berkshire-%s-chain-%s.html" % (slug, cslug))
        if not os.path.exists(path):
            print("NO chain page", path)
            continue
        t = open(path, encoding="utf-8").read()
        did = False
        for row in KEY_FIN_ROWS:
            val = fin.get(row)
            if not val:
                continue
            pat = re.compile(r'(<tr><td>%s</td><td class="val">)[^<]*(</td></tr>)' % re.escape(row))
            newt, k = pat.subn(lambda m, v=val: m.group(1) + v + m.group(2), t)
            if k:
                t = newt
                did = True
        # 标签翻已采集（保险）
        t = t.replace('财务数据（待采集）', '财务数据（已采集）')
        t = t.replace('关键财务（最新可得年报）</div><span class="fin-tag">待采集</span>',
                      '关键财务（最新可得年报）</div><span class="fin-tag">已采集</span>')
        if did:
            open(path, "w", encoding="utf-8").write(t)
            changed.append(os.path.basename(path))
            print("reinjected %s %s -> %s" % (slug, code, {r: fin.get(r) for r in KEY_FIN_ROWS}))
        else:
            print("NO CHANGE %s %s (rows already correct?)" % (slug, code))
    open(os.path.join(DS, "_reinject_changed.txt"), "w", encoding="utf-8").write("\n".join(changed))
    print("TOTAL changed=", len(changed))


if __name__ == "__main__":
    main()
