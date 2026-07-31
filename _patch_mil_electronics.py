import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_mil_electronics_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 mil-electronics 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
mil_cycle = (
    "    },\n"
    "    'mil-electronics': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：军费增速与新质作战力量建设、装备换代与信息化 / 智能化升级、国产化率提升（自主可控）、军品审价机制、海外禁运倒逼国产、军民融合。</p><ul><li><b>装备建设</b>：军费稳健增长与新质作战力量（导弹 / 卫星 / 电子对抗）建设，是军工电子订单根本来源。</li><li><b>信息化升级</b>：雷达 / 制导 / 通信 / 红外 / FPGA 等电子系统单装价值量随装备信息化提升。</li><li><b>自主可控</b>：特种 IC 与高可靠器件国产化率提升，打开份额空间。</li><li><b>审价机制</b>：军品审价压价是盈利主要变量，规模与成本管控是对冲。</li><li><b>海外禁运</b>：高端芯片与器件限制倒逼本土供应链，也压制部分需求。</li></ul>''',\n"
    "        'current': '军工电子呈「装备放量 + 信息化升级 + 自主可控」三轮驱动：军费稳健增长与新质作战力量建设拉动雷达 / 制导 / 连接器 / 元器件需求，国产化率提升打开份额空间；最大变量是军品审价、订单确认节奏与装备列装周期，大额订单落地与业绩确认是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, mil_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入军工电子链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _mil_electronics_data import mil_electronics\n\nCHAINS = [mil_electronics]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
