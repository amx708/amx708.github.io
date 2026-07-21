# -*- coding: utf-8 -*-
"""给 白酒 / AI / 机器人 三条产业链页面（索引 + 详情）注入统一「数据口径」banner。
这些链的旧生成器未带 banner；本脚本直接改产物 HTML（deploy_site 与 repo 双份），
保持与 电力/煤炭/有色/化工/电力设备/中药/创新药/家电 八链一致的披露。
中性 slate 风格，适配各链深色页，不依赖具体主题色。
"""
import re, os
from pathlib import Path

DEPL = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\deploy_site")
REPO = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\repo\amx708.github.io")

BANNER = ('<div class="data-banner">📊 <b>数据口径</b>：财务数据以各公司<b>最新可得年报</b>为准；'
          '估值 / 行情为<b>采集日快照</b>（实时行情接口当前环境不可用）。本页为框架级原创整理，'
          '<b>不构成投资建议</b>。最后更新：<span class="upd">2026-07-12</span></div>\n\n')

CSSADD = ('.data-banner{background:rgba(100,116,139,0.12);border:1px solid rgba(100,116,139,0.35);'
          'border-left:4px solid #64748b;border-radius:10px;padding:12px 16px;margin-bottom:20px;'
          'font-size:12.5px;color:#cbd5e1;line-height:1.7}\n'
          '.data-banner b{color:#fff;font-weight:600}\n'
          '.data-banner .upd{color:#94a3b8;font-weight:600}\n')

PREFIXES = ['berkshire-baijiu-chain', 'berkshire-ai-chain', 'berkshire-robot-chain']


def patch_file(path: Path):
    if not path.exists():
        return False
    html = path.read_text(encoding='utf-8')
    if 'data-banner' in html:
        return False  # already patched
    # 1) inject CSS before </style>
    html = html.replace('</style>', CSSADD + '</style>', 1)
    # 2) inject banner after hero (before first explain-banner or section-title)
    m = re.search(r'(</div>\s*\n)(<div class="(explain-banner|section-title|layer-block|overview)")', html)
    if not m:
        return False
    html = html[:m.end(1)] + BANNER + html[m.end(1):]
    path.write_text(html, encoding='utf-8')
    return True


def main():
    total = 0
    for base in (DEPL, REPO):
        for pre in PREFIXES:
            for f in sorted(base.glob(pre + '*.html')):
                if patch_file(f):
                    total += 1
                    print('patched:', f.name)
    print('total patched:', total)


if __name__ == '__main__':
    main()
