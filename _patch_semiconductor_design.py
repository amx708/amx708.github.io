import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_semiconductor_design_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 design 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
design_cycle = (
    "    },\n"
    "    'semiconductor-design': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：下游需求（AI 算力 / 手机 / 汽车 / 物联网）、国产替代率、晶圆代工产能与价格、代工限制（先进制程）、库存周期、产品迭代（端侧 AI）。</p><ul><li><b>国产替代</b>：国产手机与 AI 算力链拉动设计公司转单，替代空间结构性增长。</li><li><b>代工产能</b>：台积电 / 中芯产能与代工价格是设计公司成本与供给核心变量。</li><li><b>库存周期</b>：芯片渠道库存去化到补库，是设计公司业绩弹性来源。</li><li><b>产品迭代</b>：端侧 AI（NPU/SoC）、汽车电子提升芯片价值量与用量。</li><li><b>代工限制</b>：先进制程受设备管制，倒逼成熟制程与架构创新。</li></ul>''',\n"
    "        'current': '半导体设计呈「国产替代 + 端侧 AI + 汽车电子」三轮驱动：国产手机与 AI 算力链拉动 Fabless 转单，端侧 AI 与智驾提升芯片价值量；最大变量是代工产能与价格、库存周期、先进制程限制与产品迭代节奏，订单与毛利率是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, design_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入半导体设计链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _semiconductor_design_data import semiconductor_design\n\nCHAINS = [semiconductor_design]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
