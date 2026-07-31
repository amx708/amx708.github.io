"""全站关键财务回填 + 标签修正。

遍历 deploy_site 下所有 berkshire-*-chain-*.html 深页：
  - 按股票代码从全局 co 页 <div class="snap"> 取 6 项真实财务（营收/归母净利/毛利率/ROE/负债率/经营现金流）
  - 调用增强版 inject_financials：填空行 + 若 6 行全填则把「财务数据（待采集）」标题与关键财务 fin-tag 翻成「已采集」
幂等：已填的行与已翻的标签不会重复改动。

改动的页面路径写入 _backfill_changed.txt（相对 deploy_site），供部署脚本分批推送。
"""
import os, re, glob, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _upgrade_frames as uf

ROOT = os.path.dirname(os.path.abspath(__file__))
CODE_RE = re.compile(r'berkshire-[a-z0-9-]+-chain-(\d{6})\.html')


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, 'berkshire-*-chain-*.html')))
    changed = []
    filled = 0
    relabeled = 0
    no_co = 0
    for p in pages:
        fn = os.path.basename(p)
        m = CODE_RE.search(fn)
        if not m:
            continue
        code = m.group(1)
        slug = fn[len('berkshire-'):].split('-chain-')[0]
        fin = uf.get_fin_from_co(slug, code)
        if fin is None:
            no_co += 1
        did = uf.inject_financials(p, fin)
        if did:
            changed.append(fn)
            t2 = open(p, encoding='utf-8').read()
            if '财务数据（已采集）' in t2:
                relabeled += 1
            if fin:
                filled += 1
    out = os.path.join(ROOT, '_backfill_changed.txt')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(changed) + ('\n' if changed else ''))
    print('chain pages total=%d  changed=%d  (filled=%d relabeled=%d  no_co_source=%d)'
          % (len(pages), len(changed), filled, relabeled, no_co))
    print('changed list -> %s' % out)


if __name__ == '__main__':
    main()
