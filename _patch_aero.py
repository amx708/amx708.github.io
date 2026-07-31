import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_aero_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 aero 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
aero_cycle = (
    "    },\n"
    "    'aero': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：军费增速与战略空军建设、装备换代与大型化/隐身化升级、国产航发替代、民机配套（C919/AG600）、军品审价机制、海外限制。</p><ul><li><b>装备建设</b>：战略空军与远程打击拉动运/轰与特种机需求，是整机订单根本来源。</li><li><b>国产航发</b>：太行与新机型替代进口动力，打开发动机与部件份额空间。</li><li><b>民机配套</b>：C919 机体与复材部件配套，打开第二曲线。</li><li><b>审价机制</b>：军品审价压价是盈利主要变量，规模与成本管控是对冲。</li><li><b>材料自主</b>：高温合金/复材/锻件国产化支撑装备放量。</li></ul>''',\n"
    "        'current': '航空装备呈「战略空军建设 + 装备换代 + 国产航发/材料替代」三轮驱动：军费稳健增长与大型化/隐身化升级拉动整机与发动机需求，民机配套打开第二曲线；最大变量是军品审价、大额订单确认节奏与装备列装周期，整机交付与业绩确认是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, aero_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入航空装备链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _aero_data import aero\n\nCHAINS = [aero]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
