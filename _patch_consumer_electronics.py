import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_consumer_electronics_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 consumer-electronics 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
ce_cycle = (
    "    },\n"
    "    'consumer-electronics': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：智能手机 / PC 换机周期、AI 终端（AI Phone / PC / 可穿戴）创新、折叠屏 / MR 等新形态、果链 / 安卓链创新节奏、出海与份额变化、汇兑与地缘、半导体国产替代（CIS / 射频 / 存储）。</p><ul><li><b>换机周期</b>：手机 / PC 历经下行后迎换代，是需求回暖的根本来源。</li><li><b>AI 终端</b>：AI Phone / PC 与端侧算力开启创新周期，推高单机价值量。</li><li><b>新形态</b>：折叠屏 / MR / 可穿戴等新品拓宽创新与销量空间。</li><li><b>龙头集中</b>：精密制造与垂直整合推动份额向头部代工厂集中。</li><li><b>出海</b>：新兴市场品牌与制造出海打开第二增长曲线。</li></ul>''',\n"
    "        'current': '消费电子处「换机周期回暖 + AI 终端创新 + 龙头集中」窗口：手机 / PC 历经下行后迎换代，AI Phone / PC 与折叠屏等新形态开启创新周期，果链与安卓链龙头凭精密制造与垂直整合提升份额；变量在终端销量、创新节奏、汇率与地缘，新品发布与出货指引是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, ce_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入消费电子链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _consumer_electronics_data import consumer_electronics\n\nCHAINS = [consumer_electronics]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
