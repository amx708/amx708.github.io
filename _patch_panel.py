import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_panel_chain.py'

t = open(SRC, encoding='utf-8').read()

anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
panel_cycle = (
    "    },\n"
    "    'panel': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：TV/IT 大尺寸化、车载与商用显示渗透、供给格局（龙头控产保价）、稼动率、OLED 替代与折旧、面板价格周期。</p><ul><li><b>大尺寸化</b>：TV 平均尺寸提升带动面积需求，是 LCD 需求根本来源。</li><li><b>供给格局</b>：头部控产与退出改善供需，价格周期趋稳。</li><li><b>车载显示</b>：智能座舱提升单车面板数量与规格，需求稳健。</li><li><b>OLED 替代</b>：中小尺寸 OLED 渗透提升，折旧与良率是变量。</li><li><b>周期</b>：面板价格呈明显周期，稼动率调节是关键。</li></ul>''',\n"
    "        'current': '面板呈「大尺寸化 + 供给格局优化 + 车载显示」三轮驱动：TV/IT 平均尺寸提升与龙头控产改善供需，车载智能座舱提升面板用量；最大变量是面板价格周期与稼动率、OLED 折旧压力，以及需求端资本开支节奏，格局优化下龙头盈利弹性改善。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, panel_cycle, 1)

idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _panel_data import panel\n\nCHAINS = [panel]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
