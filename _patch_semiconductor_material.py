import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_semiconductor_material_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 material 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
material_cycle = (
    "    },\n"
    "    'semiconductor-material': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：晶圆厂扩产节奏、国产替代率、客户认证周期、材料品类（硅片 / 气体 / 光刻胶 / CMP / 靶材）、技术迭代（先进制程材料）、价格。</p><ul><li><b>晶圆厂扩产</b>：国内 Foundry 与存储厂扩产直接拉动材料消耗，是需求根本来源。</li><li><b>国产替代</b>：硅片 / 光刻胶 / 特气 / CMP 等材料国产化率低，替代空间大。</li><li><b>客户认证</b>：材料认证壁垒高、周期长，通过验证后黏性强、放量稳。</li><li><b>品类扩张</b>：平台型公司横向扩品类，是第二增长曲线。</li><li><b>技术迭代</b>：先进制程材料（ArF 光刻胶、大硅片）升级打开价值量。</li></ul>''',\n"
    "        'current': '半导体材料呈「晶圆厂扩产 + 国产替代 + 品类扩张」三轮驱动：国内产能建设与材料低国产化率打开替代空间，认证通过后黏性强；最大变量是客户认证周期、扩产节奏、材料价格与技术迭代，认证通过与放量是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, material_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入半导体材料链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _semiconductor_material_data import semiconductor_material\n\nCHAINS = [semiconductor_material]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
