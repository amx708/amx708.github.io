import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_rare_earth_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 rare-earth 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
rare_cycle = (
    "    },\n"
    "    'rare-earth': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：稀土价格（轻稀土镨钕 / 中重稀土镝铽）、国家总量控制配额（开采 + 冶炼分离指标）、"
    "下游新能源 / 风电 / 机器人磁材需求、海外矿供应与政策、走私与替代材料。</p>\n<ul>\n"
    "<li><b>稀土价格</b>：轻稀土看镨钕（磁材需求），中重稀土看镝铽（战略属性）；价格受指标与囤货影响波动大。</li>\n"
    "<li><b>总量控制配额</b>：开采 + 冶炼分离指标由主管部门下达，是供给根本约束，决定量与价。</li>\n"
    "<li><b>下游需求</b>：新能源车 / 风电 / 机器人拉动高性能钕铁硼，是长期需求主线。</li>\n"
    "<li><b>海外与替代</b>：海外矿（澳美等）供应、稀土永磁替代（铁氧体 / 无稀土电机）是潜在压制。</li>\n"
    "<li><b>政策</b>：集团专业化整合（中国稀土集团）优化供给格局，战略地位提升。</li>\n</ul>''',\n"
    "        'current': '稀土呈\"资源战略化 + 配额约束 + 磁材驱动\"：轻稀土看镨钕（新能源磁材），中重稀土看镝铽（战略属性），"
    "总量控制配额是供给根本约束；当前磁材需求（风电 / 电车 / 机器人）提供长期拉动，价格周期与配额政策是核心变量。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, rare_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入稀土链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _rare_earth_data import rare_earth\n\nCHAINS = [rare_earth]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
