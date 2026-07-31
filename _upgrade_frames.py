# -*- coding: utf-8 -*-
"""把「建设状态」(框架版 / 仅有 -co- 页) 的产业链升级为带真实企业深页的链。

做法：
1. 扫描 berkshire-<slug>-co-*.html 存在、但无 -chain- 深页的 slug（=建设状态）。
2. 对每个 slug 解析其索引页 berkshire-<slug>-chains.html：
   - 五层框架（LAYER1-5 的 lt/ld）
   - 代表公司（名称 / 代码 / 备注 nt / 真实财务 cf-fin）
3. 生成 _<slug>_data.py（源文件，便于以后编辑），并直接调用 _build_five_chains.render_detail
   写出 berkshire-<slug>-chain-<code>.html 深页（不重生成索引页，保留已有财务/效能/信号）。
4. 把索引页里的 -co- 链接换成 -chain-。
5. 「关键财务」块（营收/净利/毛利率/ROE/负债率/经营现金流）从各 co 页 <div class="snap"> 提取真实值注入，不编数字；总市值/PE/PB/股息率属「估值快照」块，由 _refresh_valuation 统一回填。

定性字段（overview/moat/risks/layers）由「框架 + 备注」诚实生成，留作用户后续记录理解的底稿。
估值块(PE/PB分位) 由后续的 _refresh_valuation.py 统一回填。

用法：
  python _upgrade_frames.py            # 全部建设状态链
  python _upgrade_frames.py steel      # 仅单链（验证用）
"""
import os, re, sys, pprint, importlib.util

DS = os.path.dirname(os.path.abspath(__file__))
ROOT = DS

# 加载渲染模块
spec = importlib.util.spec_from_file_location(
    "fcb", os.path.join(ROOT, "_build_five_chains.py"))
fcb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fcb)

PALETTE = ['0ea5e9', 'f59e0b', '10b981', 'ef4444', '8b5cf6', 'ec4899',
           '14b8a6', 'f97316', '6366f1', '84cc16', '06b6d4', 'eab308',
           'a855f7', 'f43f5e', '22c55e', '0d9488']
ICON_MAP = {
    '钢铁': '🏗️', '钢': '🏗️', '煤炭': '🪨', '煤': '🪨', '有色': '⛏️', '金属': '⛏️',
    '银行': '🏦', '证券': '📈', '保险': '🛡️', '信托': '💼', '租赁': '💼', '期货': '📊',
    '白酒': '🍶', '啤酒': '🍺', '食品': '🍎', '乳': '🥛', '休闲': '🍿', '饮料': '🥤',
    '医药': '💊', '中药': '🌿', '器械': '🔬', '生物': '🧬', '医院': '🏥', '药房': '💊',
    '家电': '🔌', '家居': '🛋️', '照明': '💡', '厨电': '🍳', '家居用品': '🧺',
    '汽车': '🚗', '零部件': '⚙️', '锂电': '🔋', '电子': '🔌', '智驾': '🤖', '轮胎': '🛞',
    '半导': '🔬', '面板': '🖥️', 'PCB': '🔲', '光学': '🔭', '传感': '📡', '被动': '🔧',
    '计算机': '💻', '软件': '🧩', '云': '☁️', '安全': '🔐', '安防': '📹', '工业': '🏭',
    '机器': '🤖', '工控': '🎛️', '机床': '🔧', '激光': '🔦', '电力': '⚡', '设备': '🔧',
    '光伏': '☀️', '风电': '🌬️', '储能': '🔋', '电网': '🔌', '核电': '⚛️', '化工': '⚗️',
    '化纤': '🧵', '氟': '⚗️', '硅': '💎', '涂料': '🎨', '水泥': '🏗️', '玻璃': '🪟',
    '玻纤': '🧱', '黄金': '🥇', '铜': '🟤', '地产': '🏢', '建筑': '🏗️', '装饰': '🎨',
    '园林': '🌳', '航运': '🚢', '港口': '⚓', '快递': '📦', '铁路': '🚆', '公路': '🛣️',
    '机场': '✈️', '机械': '⚙️', '轨交': '🚇', '油服': '🛢️', '通用': '🔧', '农机': '🚜',
    '电梯': '🛗', '通信': '📡', '运营': '📡', '设备': '📡', '光模': '🔦', '物联': '📶',
    '传媒': '🎬', '游戏': '🎮', '影视': '🎥', '出版': '📚', '广告': '📣', '体育': '⚽',
    '军工': '🛩️', '航空': '✈️', '船舶': '🚢', '卫星': '🛰️', '纺织': '👕', '造纸': '📄',
    '包装': '📦', '珠宝': '💍', '农业': '🌾', '养殖': '🐷', '饲料': '🌾', '种业': '🌱',
    '农药': '🧪', '动保': '💉', '商贸': '🛒', '零售': '🛒', '社服': '🍽️', '公用': '💧',
    '燃气': '🔥', '水务': '💧', '环保': '♻️',
}


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def darken(h, f=0.45):
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex((int(r * f), int(g * f), int(b * f)))


def pick_icon(name):
    for k, v in ICON_MAP.items():
        if k in name:
            return v
    return '🏭'


def discover_frame_slugs():
    deep = set()
    frame = set()
    for f in os.listdir(ROOT):
        m = re.search(r'berkshire-([a-z0-9-]+)-chain-', f)
        if m:
            deep.add(m.group(1))
    for f in os.listdir(ROOT):
        m = re.search(r'berkshire-([a-z0-9-]+)-co-', f)
        if m:
            s = m.group(1)
            if s not in deep:
                frame.add(s)
    return sorted(frame)


def parse_index(slug):
    path = os.path.join(ROOT, 'berkshire-%s-chains.html' % slug)
    if not os.path.exists(path):
        return None
    t = open(path, encoding='utf-8').read()
    # 链名
    m = re.search(r'<title>(.*?)产业链', t)
    name = m.group(1) + '产业链' if m else slug
    # 五层框架
    layers = []
    for lm in re.finditer(
            r'<div class="layer"><div class="ln">LAYER \d+</div>'
            r'<div class="lt">(.*?)</div><div class="ld">(.*?)</div></div>', t, re.S):
        layers.append({'name': lm.group(1), 'desc': lm.group(2)})
    # 公司（财务从各 co 页单独提取，避免可选组被最短匹配吞掉）
    # 索引页可能已被换链（co->chain），故这里 co/chain 链接都认，便于 repair 重跑
    companies = []
    for cm in re.finditer(
            r'<div class="co">.*?class="nm">(.*?)</div>.*?'
            r'berkshire-[a-z0-9-]+-(?:co|chain)-(\d{6})\.html".*?'
            r'<div class="nt">(.*?)</div>', t, re.S):
        nm = cm.group(1)
        code = cm.group(2)
        note = cm.group(3)
        companies.append({'name': nm, 'code': code, 'note': note})
    # 兜底：部分索引（如 securities）用表格行列出公司：<a href="...-co-CODE.html">名称</a>
    if not companies:
        seen = set()
        for am in re.finditer(
                r'<a href="berkshire-[a-z0-9-]+-(?:co|chain)-(\d{6})\.html">(.*?)</a>', t, re.S):
            code = am.group(1)
            nm = re.sub(r'<.*?>', '', am.group(2)).strip()
            if code in seen:
                continue
            seen.add(code)
            companies.append({'name': nm, 'code': code, 'note': ''})
    return {'name': name, 'layers': layers, 'companies': companies}


def fmt_num(v):
    """给整数位加千分位，保留小数与负号。如 3175.1 -> 3,175.1；-300.69 -> -300.69。"""
    v = (v or '').strip()
    if not v:
        return v
    try:
        neg = v.startswith('-')
        body = v[1:] if neg else v
        if '.' in body:
            ip, dp = body.split('.', 1)
        else:
            ip, dp = body, ''
        ip = ip or '0'
        ip = '{:,}'.format(int(ip))
        s = ip + ('.' + dp if dp else '')
        return ('-' + s) if neg else s
    except Exception:
        return v


# co 页 <div class="snap"> 中的标签 -> (深页「关键财务」行名, 单位)
SNAP_MAP = {
    '营收(亿)': ('营业总收入', '亿'),
    '归母净利(亿)': ('归母净利润', '亿'),
    '毛利率(%)': ('毛利率', '%'),
    'ROE(%)': ('ROE（加权）', '%'),
    '负债率(%)': ('资产负债率', '%'),
    '经营现金流(亿)': ('经营现金流净额', '亿'),
}


def get_fin_from_co(slug, code):
    """从各 co 页的 <div class="snap"> 块提取真实财务，回填到深页「关键财务」块。

    仅取 6 个纯财务行；总市值/PE/PB/股息率属于「估值快照」块，由 _refresh_valuation 统一回填。
    co 页可能挂在其他链 slug 下（跨链同公司），按代码全局查找。
    """
    import glob
    cands = glob.glob(os.path.join(ROOT, 'berkshire-*-co-%s.html' % code))
    if not cands:
        return None
    p = cands[0]
    t = open(p, encoding='utf-8').read()
    out = {}
    for bm in re.finditer(r'<div><b>(.*?)</b><span>(.*?)</span></div>', t):
        val = bm.group(1).strip()
        lab = bm.group(2).strip()
        if lab in SNAP_MAP:
            row, unit = SNAP_MAP[lab]
            out[row] = fmt_num(val) + ((' ' + unit) if unit else '')
    return out or None


def build_data(slug, info):
    name = info['name']
    nav = name.replace('产业链', '')
    short = nav
    icon = pick_icon(name)
    accent = PALETTE[abs(hash(slug)) % len(PALETTE)]
    accent_rgb = '%d,%d,%d' % hex_to_rgb(accent)
    accent_dark = darken(accent)
    layers5 = info['layers']
    # 投资逻辑层 = 第5层
    l5 = layers5[4] if len(layers5) >= 5 else (layers5[-1] if layers5 else {'name': '投资逻辑', 'desc': ''})
    chain_layers = [{'n': '%02d' % (i + 1), 'name': l['name'], 'desc': l['desc']}
                    for i, l in enumerate(layers5)] if layers5 else [
        {'n': '0%d' % (i + 1), 'name': '环节%d' % (i + 1), 'desc': ''} for i in range(5)]
    comps = []
    for c in info['companies']:
        note = c['note'] or ('%s代表公司' % nav)
        note_short = (note[:8] + '…') if len(note) > 9 else note
        comp_layers = []
        for i, l in enumerate(chain_layers):
            comp_layers.append('%s；在「%s」环节：%s' % (note, l['name'], l['desc']))
        overview = ('%s（%s）是%s产业链中的代表公司，%s。本页为框架级原创梳理，'
                    '业务结构、市场份额与最新财务以各公司公开年报为准，不构成投资建议。'
                    % (c['name'], c['code'], name, note))
        moat = ('护城河取决于本链「%s」所述逻辑（%s）；需结合%s判断其份额、牌照或工艺壁垒的高低。'
                % (l5['name'], l5['desc'], note))
        risks = ('主要风险来自行业周期与本链「%s」变量（%s），以及价格、竞争与需求波动；'
                 '具体以年报披露为准。' % (l5['name'], l5['desc']))
        comps.append({
            'slug': c['code'], 'name': c['name'], 'code': c['code'],
            'region': '中国', 'region_cls': 'region-cn',
            'desc': note,
            'stats': [('定位', note_short), ('产业链', nav), ('属性', 'A股样本')],
            'overview': overview,
            'layers': comp_layers,
            'info': [('主业', note_short), ('地位', '代表公司'), ('关注', l5['name'])],
            'moat': moat,
            'risks': risks,
        })
    data = {
        'key': slug, 'name': name, 'short': short, 'icon': icon,
        'accent': accent, 'accent_rgb': accent_rgb, 'accent_dark': accent_dark,
        'nav_label': nav, 'n_companies': len(comps),
        'hero_sub': '价值投资视角下的「%s」梳理 · 用公开年报/官网/新闻原创整理，不复制任何付费内容' % name,
        'layers': chain_layers,
        'companies': comps,
    }
    return data


KEY_FIN_ROWS = ['营业总收入', '归母净利润', '毛利率', 'ROE（加权）', '资产负债率', '经营现金流净额']


def inject_financials(path, fin):
    """把 fin（行名->值）回填到深页「关键财务」块；仅替换仍为「— 待采集」的行，幂等。

    增强：若 6 个关键财务行全部已填（t 中无对应「— 待采集」行），则把
    「财务数据（待采集）」section 标题与关键财务的 fin-tag 翻成「已采集」。
    估值快照块的 4 个「待采集」保持原样（由每日估值刷新 _refresh_valuation 回填）。
    即便 fin 为空（数据早已填），只要 6 行全填也会翻标签，从而修复历史印错标签。
    """
    t = open(path, encoding='utf-8').read()
    did = False
    if fin:
        for row, val in fin.items():
            a = '<tr><td>%s</td><td class="val">— 待采集</td></tr>' % row
            b = '<tr><td>%s</td><td class="val">%s</td></tr>' % (row, val)
            if a in t:
                t = t.replace(a, b, 1)
                did = True
    # 6 个关键财务行全填 -> 翻标签
    all_filled = all(
        ('<tr><td>%s</td><td class="val">— 待采集</td></tr>' % r) not in t
        for r in KEY_FIN_ROWS)
    if all_filled:
        s1 = '<div class="section-title">财务数据（待采集）</div>'
        s2 = '关键财务（最新可得年报）</div><span class="fin-tag">待采集</span>'
        if s1 in t:
            t = t.replace(s1, '<div class="section-title">财务数据（已采集）</div>', 1)
            did = True
        if s2 in t:
            t = t.replace(s2, '关键财务（最新可得年报）</div><span class="fin-tag">已采集</span>', 1)
            did = True
    if did:
        open(path, 'w', encoding='utf-8').write(t)
    return did


def swap_links(slug, codes):
    """把索引页里指向各代表公司 co 页的链接，改为指向本链深页。

    跨链同公司的 co 页可能挂在其他 slug 下，这里按代码全局匹配原 -co- 链接再改写，
    确保无论原链接前缀是哪个链，都指向本链 berkshire-<slug>-chain-<code>.html。
    """
    path = os.path.join(ROOT, 'berkshire-%s-chains.html' % slug)
    if not os.path.exists(path):
        return 0
    t = open(path, encoding='utf-8').read()
    n = 0
    for code in codes:
        new, k = re.subn(r'berkshire-[a-z0-9-]+-co-%s\.html' % code,
                         r'berkshire-%s-chain-%s.html' % (slug, code), t)
        if k:
            t = new
            n += k
    if n:
        open(path, 'w', encoding='utf-8').write(t)
    return n


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if only:
        # 强制处理指定 slug（即便已转深页，用于 repair）
        frame = [only]
    else:
        frame = discover_frame_slugs()
    print('slugs to process:', len(frame))
    done = 0
    skipped = []
    errors = []
    for slug in frame:
        try:
            info = parse_index(slug)
            if not info or not info['companies']:
                skipped.append((slug, 'parse-empty'))
                print('SKIP', slug, 'parse-empty')
                continue
            if len(info['layers']) < 5:
                # 补足到 5 层，避免渲染错位
                while len(info['layers']) < 5:
                    info['layers'].append({'name': '补充环节', 'desc': ''})
            data = build_data(slug, info)
            # 写源文件（便于以后编辑）
            var = slug.replace('-', '_')
            with open(os.path.join(ROOT, '_%s_data.py' % slug), 'w', encoding='utf-8') as fh:
                fh.write('# %s 产业链（由索引页自动提取；定性不杜撰，财务/估值见回填）\n' % slug)
                fh.write('%s = ' % var)
                pprint.pprint(data, fh, width=120, sort_dicts=False)
            # 渲染深页
            fcb.CHAINS = [data]
            fcb.CYCLE[slug] = {
                'criteria': '<p><b>驱动变量</b>：' + '；'.join(
                    l['desc'] for l in data['layers']) + '。</p>',
                'current': '%s周期看「%s」：%s（框架研判，需结合实盘校验）。' % (
                    data['name'], data['layers'][-1]['name'], data['layers'][-1]['desc']),
            }
            ngen = 0
            for co in data['companies']:
                det = fcb.render_detail(data, co)
                fn = os.path.join(ROOT, 'berkshire-%s-chain-%s.html' % (slug, co['slug']))
                open(fn, 'w', encoding='utf-8').write(det)
                fin = get_fin_from_co(slug, co['code'])
                inject_financials(fn, fin)
                ngen += 1
            nswap = swap_links(slug, [co['code'] for co in data['companies']])
            done += 1
            print('OK', slug, 'pages=%d linkswap=%d' % (ngen, nswap))
        except Exception as e:
            import traceback
            errors.append((slug, repr(e)))
            traceback.print_exc()
            print('ERROR', slug, repr(e))
    print('\nDONE: upgraded=%d skipped=%d errors=%d' % (done, len(skipped), len(errors)))
    if skipped:
        print('skipped:', skipped)
    if errors:
        print('errors:', errors)


if __name__ == '__main__':
    main()
