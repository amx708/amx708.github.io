import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_semiconductor_chemical_chain.py'

t = open(SRC, encoding='utf-8').read()

anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
sc_cycle = (
    "    },\n"
    "    'semiconductor-chemical': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：晶圆厂（逻辑/存储）扩产节奏、先进制程与国产替代、材料验证导入周期、客户集中度、价格与竞争。</p><ul><li><b>扩产驱动</b>：本土晶圆厂扩产与产能利用率提升直接拉动电子化学品耗材用量。</li><li><b>国产替代</b>：光刻胶/特气/CMP/靶材等卡脖子环节替代空间大，是核心逻辑。</li><li><b>制程升级</b>：先进制程与存储对材料纯度与品类要求提升，单价与用量双升。</li><li><b>验证周期</b>：半导体材料认证周期长（数年），导入节奏是主要变量。</li><li><b>客户集中</b>：下游集中度高，单一大客户波动影响大。</li></ul>''',\n"
    "        'current': '半导体化学呈「晶圆厂扩产 + 国产替代 + 制程升级」三轮驱动：本土逻辑/存储扩产与先进制程推进，拉动光刻胶、电子特气、CMP、靶材等卡脖子耗材用量与替代；最大变量是材料验证导入周期、客户集中度与价格竞争，认证通过后的放量弹性是核心看点。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, sc_cycle, 1)

idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _semiconductor_chemical_data import semiconductor_chemical\n\nCHAINS = [semiconductor_chemical]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
