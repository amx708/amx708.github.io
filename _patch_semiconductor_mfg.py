import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_semiconductor_mfg_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 mfg 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
mfg_cycle = (
    "    },\n"
    "    'semiconductor-mfg': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：下游需求（AI / 手机 / 汽车 / 工控）、产能利用率、工艺节点（成熟 vs 先进）、国产客户绑定、资本开支周期、出口管制（设备）、封测价格。</p><ul><li><b>产能利用率</b>：晶圆厂 / 封测产能利用率回升到改善，是制造景气核心。</li><li><b>国产替代</b>：国产设计公司转单与成熟制程需求，支撑国内 Foundry 产能消化。</li><li><b>先进封装</b>：Chiplet / 2.5D 是后摩尔时代价值增量，拉动封测升级。</li><li><b>资本开支</b>：逆周期扩产对比折旧压力，是盈利主要变量。</li><li><b>出口管制</b>：设备获取限制先进制程推进，倒逼成熟制程深耕。</li></ul>''',\n"
    "        'current': '半导体制造呈「国产产能消化 + 先进封装 + 成熟制程深耕」：AI 与汽车拉动晶圆需求、Chiplet 推升封测价值，但产能利用率、资本开支折旧与设备管制是核心变量，稼动率与价格（代工 / 封测）是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, mfg_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入半导体制造链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _semiconductor_mfg_data import semiconductor_mfg\n\nCHAINS = [semiconductor_mfg]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
