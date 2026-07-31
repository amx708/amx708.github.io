"""slug 命名深页的关键财务回填（公司名桥接）。

问题：consumer-electronics / mil-electronics / semiconductor-equip 这 3 条原始链的
深页用「公司 slug 后缀」(如 cykg)，而 co 页用「股票代码后缀」(如 688036)，
命名不一致导致 _backfill_fin 按代码关联失败、财务一直空着。

桥接：深页 <title> 含公司名（"传音控股 链 · 消费电子产业链"），同链 co 页 <title>
也含公司名（"传音控股 · 消费电子产业链"）。按公司名在同链 co 页中匹配，拿代码，
再调 get_fin_from_co + inject_financials（填值 + 全填则翻「已采集」标签）。

rare-earth / semiconductor-chemical 这 2 条链根本没有 co 页（co=0），无数据源，跳过。
"""
import os, re, glob, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _upgrade_frames as uf

ROOT = os.path.dirname(os.path.abspath(__file__))
BRIDGE = {'consumer-electronics', 'mil-electronics', 'semiconductor-equip'}


def title_of(p):
    t = open(p, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    return (m.group(1).strip() if m else ''), t


def chain_name(title):
    # "传音控股 链 · 消费电子产业链" -> 传音控股
    for sep in (' 链', '链 ·', '·'):
        if sep in title:
            return title.split(sep)[0].strip()
    return title.strip()


def co_map(slug):
    d = {}
    for p in glob.glob(os.path.join(ROOT, f'berkshire-{slug}-co-*.html')):
        title, _ = title_of(p)
        code = re.search(r'-co-([0-9]+)\.html', os.path.basename(p))
        if not code:
            continue
        code = code.group(1)
        name = title.split('·')[0].strip()
        if name:
            d[name] = code
    return d


def main():
    changed = []
    bridged = nomatch = nosnap = 0
    for slug in sorted(BRIDGE):
        comap = co_map(slug)
        print(f'[{slug}] co 公司名: {list(comap.keys())}')
        for p in sorted(glob.glob(os.path.join(ROOT, f'berkshire-{slug}-chain-*.html'))):
            fn = os.path.basename(p)
            title, t0 = title_of(p)
            if '财务数据（待采集）' not in t0:
                continue
            name = chain_name(title)
            code = comap.get(name)
            if not code:
                for k, v in comap.items():
                    if name and (name in k or k in name):
                        code = v
                        break
            if not code:
                print(f'  NO MATCH {fn} name={name!r}')
                nomatch += 1
                continue
            fin = uf.get_fin_from_co(slug, code)
            if not fin:
                print(f'  NO SNAP {fn} code={code}')
                nosnap += 1
                continue
            if uf.inject_financials(p, fin):
                changed.append(fn)
                bridged += 1
    out = os.path.join(ROOT, '_backfill_slug_changed.txt')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(changed) + ('\n' if changed else ''))
    print(f'bridged={bridged} nomatch={nomatch} nosnap={nosnap} changed={len(changed)} -> {out}')


if __name__ == '__main__':
    main()
