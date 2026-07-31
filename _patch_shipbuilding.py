import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_shipbuilding_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 shipbuilding 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
ship_cycle = (
    "    },\n"
    "    'shipbuilding': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：全球贸易与运价（新船订单）、环保法规（脱硫/双燃料/甲醇替代）、钢价与汇率、海军建设（军船）、海工与浮式风电（系泊链/水下装备）、造船产能（中国集中度）。</p><ul><li><b>新船订单</b>：运价高企+船队老化+环保替代拉动集装箱/LNG/散货新单。</li><li><b>环保替代</b>：IMO 法规推动双燃料/甲醇船与旧船淘汰。</li><li><b>海军建设</b>：远洋海军拉动护卫舰/驱逐舰/补给舰。</li><li><b>钢价汇率</b>：钢价下行+本币弱势利好盈利。</li><li><b>海工复苏</b>：油价回升+浮式风电拉动系泊链与水下装备。</li></ul>''',\n"
    "        'current': '船舶制造呈「新船订单 + 环保替代 + 海军建设」三轮驱动：运价高企与船队老化拉动民船高价订单，IMO 环保法规加速双燃料船替代，海军远洋化拉动军船；最大变量是造船周期、钢价、汇率与运力周期，高价船交付与业绩确认是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, ship_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入船舶制造链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _shipbuilding_data import shipbuilding\n\nCHAINS = [shipbuilding]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
