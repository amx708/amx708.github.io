import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_pcb_chain.py'

t = open(SRC, encoding='utf-8').read()

anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
pcb_cycle = (
    "    },\n"
    "    'pcb': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：AI 算力与数据中心资本开支、汽车电动化/智能化、覆铜板材料升级（高频高速/载板）、铜价与稼动率、行业价格周期。</p><ul><li><b>算力需求</b>：AI 服务器拉动高阶数通板与封装基板用量，是近年最强增量。</li><li><b>汽车电子</b>：电动化与智能化提升车用板层数与时价，需求稳健。</li><li><b>材料升级</b>：覆铜板与载板高端化打开单价与国产替代空间。</li><li><b>周期属性</b>：PCB 行业稼动率与价格呈周期波动，铜价与产能投放是变量。</li><li><b>格局</b>：高阶板与载板认证壁垒高，头部集中。</li></ul>''',\n"
    "        'current': 'PCB 呈「AI 算力数通板 + 汽车电子 + 高端载板国产替代」三轮驱动：AI 服务器资本开支拉动高阶多层/高频板与 IC 载板需求，汽车电动化提升车用板价值量；最大变量是行业稼动率与价格周期、铜价，以及载板良率爬坡，龙头凭借工艺与客户认证穿越周期。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, pcb_cycle, 1)

idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _pcb_data import pcb\n\nCHAINS = [pcb]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
