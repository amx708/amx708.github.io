# -*- coding: utf-8 -*-
"""给已有 7 条产业链（bank/baijiu/ai/robot/tcm/innov/appliance）的导航补上
电力/煤炭/有色/化工/电力设备 五个新链，实现 12 链互通。
bank 用 .nav 结构，其余用 .top-bar 内联 span 结构。"""
import os, re, glob

REPO = r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\repo\amx708.github.io"

NEW_LINKS = [
    ('电力', 'berkshire-power-chains.html'),
    ('煤炭', 'berkshire-coal-chains.html'),
    ('有色', 'berkshire-metal-chains.html'),
    ('化工', 'berkshire-chem-chains.html'),
    ('电力设备', 'berkshire-equip-chains.html'),
]

# 家族：前缀 -> (accent 颜色, 当前链标签)
FAMILIES = {
    'bank':    ('#3b82f6', '银行'),
    'baijiu':  ('#e8b84b', '白酒'),
    'ai':      ('#22d3ee', 'AI'),
    'robot':   ('#34d399', '机器人'),
    'tcm':     ('#e0533d', '中药'),
    'innov':   ('#ec4899', '创新药'),
    'appliance': ('#f59e0b', '家电'),
}

NEW_SET = set(h for _, h in NEW_LINKS)


def has_all_new(s):
    return all(h in s for h in NEW_SET)


def patch_topbar(path, accent, current):
    s = open(path, encoding='utf-8').read()
    if has_all_new(s):
        return False  # 已含新链，跳过
    pat = re.compile(r'(<span style="display:inline-flex;gap:14px;align-items:center;margin-left:10px">)(.*?)(</span>)', re.S)
    m = pat.search(s)
    if not m:
        return False
    inner = m.group(2)
    add = ''
    for label, href in NEW_LINKS:
        add += '<a href="%s" style="color:%s;text-decoration:none;font-size:13px">%s</a>' % (href, accent, label)
    new_open = '<span style="display:inline-flex;gap:12px;align-items:center;margin-left:10px;flex-wrap:wrap">'
    new_span = new_open + inner + add + m.group(3)
    s = s[:m.start()] + new_span + s[m.end():]
    open(path, 'w', encoding='utf-8').write(s)
    return True


def patch_nav(path, accent, current):
    s = open(path, encoding='utf-8').read()
    if has_all_new(s):
        return False
    # bank 的 .nav-in 内，在最后一个已有链（家电）之后追加 5 个新链
    anchor_pat = re.compile(r'<a href="berkshire-appliance-chains\.html"[^>]*>家电</a>')
    m = anchor_pat.search(s)
    if not m:
        return False
    add = ''
    for label, href in NEW_LINKS:
        add += '<a href="%s" style="color:%s;text-decoration:none;font-size:13px">%s</a>' % (href, accent, label)
    s = s[:m.end()] + add + s[m.end():]
    open(path, 'w', encoding='utf-8').write(s)
    return True


def main():
    for fam, (accent, current) in FAMILIES.items():
        files = glob.glob(os.path.join(REPO, 'berkshire-%s-*.html' % fam))
        cnt = 0
        for f in files:
            if fam == 'bank':
                if patch_nav(f, accent, current):
                    cnt += 1
            else:
                if patch_topbar(f, accent, current):
                    cnt += 1
        print('%s: patched %d files' % (fam, cnt))


if __name__ == '__main__':
    main()
