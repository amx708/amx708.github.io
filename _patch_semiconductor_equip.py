import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_semiconductor_equip_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 semiconductor-equip 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
semi_cycle = (
    "    },\n"
    "    'semiconductor-equip': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：晶圆厂 capex 周期（扩产节奏）、国产替代政策与采购倾斜、先进制程推进（层数 / 结构复杂度提升设备用量）、"
    "设备验证与导入节奏、海外设备与零部件限制、下游需求（AI / 存储 / 汽车电子）。</p>\n<ul>\n"
    "<li><b>晶圆厂扩产</b>：本土逻辑 / 存储 fab 扩产是设备订单根本来源，capex 周期决定景气。</li>\n"
    "<li><b>国产替代</b>：自主可控政策与采购倾斜，加速刻蚀 / 薄膜 / 清洗 / CMP / 量测等环节导入。</li>\n"
    "<li><b>先进制程</b>：制程推进与 3D 结构增加刻蚀 / 薄膜 / 量测等用量，单价与价值量提升。</li>\n"
    "<li><b>海外限制</b>：设备与零部件出口管制是最大外部变量，倒逼本土供应链，也压制部分需求。</li>\n"
    "<li><b>验证节奏</b>：设备从样机到量产导入周期长，验证通过与重复订单是兑现信号。</li>\n</ul>''',\n"
    "        'current': '半导体设备呈\"国产替代 + 扩产周期 + 先进制程\"三轮驱动：本土 fab 扩产与采购倾斜加速刻蚀 / 薄膜 / 清洗 / CMP / 量测全品类突破，"
    "先进制程层数提升推高设备价值量；最大变量是海外限制与下游 capex 周期，验证通过与重复订单是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, semi_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入半导体设备链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _semiconductor_equip_data import semiconductor_equip\n\nCHAINS = [semiconductor_equip]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
