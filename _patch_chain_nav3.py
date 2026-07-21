# -*- coding: utf-8 -*-
"""给已有 4 条产业链（bank/baijiu/ai/robot）的导航补上 中药/创新药/家电 三个新链，
实现 7 链互通。bank 用 .nav 结构，其余用 .top-bar 内联 span 结构。"""
import os, re, glob

REPO = r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\repo\amx708.github.io"

NEW_LINKS = [
    ('中药', 'berkshire-tcm-chains.html'),
    ('创新药', 'berkshire-innov-chains.html'),
    ('家电', 'berkshire-appliance-chains.html'),
]

# 家族：前缀 -> (accent 颜色, 当前链标签)
FAMILIES = {
    'bank':    ('#3b82f6', '银行'),
    'baijiu':  ('#e8b84b', '白酒'),
    'ai':      ('#22d3ee', 'AI'),
    'robot':   ('#34d399', '机器人'),
}


def patch_topbar(path, accent, current):
    s = open(path, encoding='utf-8').read()
    if 'berkshire-tcm-chains.html' in s and 'berkshire-innov-chains.html' in s and 'berkshire-appliance-chains.html' in s:
        return False  # 已含新链，跳过
    # 找到 .top-bar 内的 nav span：<span style="display:inline-flex;gap:14px;...>...</span>
    # 该 span 内是 4 个 <a> 链接（银行/白酒/AI/机器人），在其后追加 3 个新链
    pat = re.compile(r'(<span style="display:inline-flex;gap:14px;align-items:center;margin-left:10px">)(.*?)(</span>)', re.S)
    m = pat.search(s)
    if not m:
        return False
    inner = m.group(2)
    # 检查当前页对应链接加粗
    for label, href in NEW_LINKS:
        bold = ';font-weight:700' if label == current else ''
        inner += '<a href="%s" style="color:%s;text-decoration:none;font-size:13px%s">%s</a>' % (href, accent, bold, label)
    new_span = m.group(1) + inner + m.group(3)
    s = s[:m.start()] + new_span + s[m.end():]
    open(path, 'w', encoding='utf-8').write(s)
    return True


def patch_nav(path, accent, current):
    s = open(path, encoding='utf-8').read()
    if 'berkshire-tcm-chains.html' in s and 'berkshire-innov-chains.html' in s and 'berkshire-appliance-chains.html' in s:
        return False
    # bank 的 .nav-in 内，在 <a href="berkshire-robot-chains.html">机器人</a> 之后追加
    anchor = '<a href="berkshire-robot-chains.html">机器人</a>'
    if anchor not in s:
        return False
    add = ''
    for label, href in NEW_LINKS:
        bold = ';font-weight:700' if label == current else ''
        add += '<a href="%s" style="color:%s;text-decoration:none;font-size:13px%s">%s</a>' % (href, accent, bold, label)
    s = s.replace(anchor, anchor + add, 1)
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
