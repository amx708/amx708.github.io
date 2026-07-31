import io, os

SRC = 'deploy_site/_build_five_chains.py'
DST = 'deploy_site/_build_satnav_chain.py'

t = open(SRC, encoding='utf-8').read()

# 1) 在 CYCLE 字典闭合前插入 satnav 周期判断
anchor = "    },\n}\n\n\n# 财务 / 估值占位框架"
assert anchor in t, "CYCLE anchor not found"
satnav_cycle = (
    "    },\n"
    "    'satnav': {\n"
    "        'criteria': '''<p><b>驱动变量</b>：北斗三号全球化与特色服务（短报文/星基增强）、高精度定位渗透（测绘/农机/无人机/自动驾驶）、卫星互联网与星座建设（星载配套）、国防信息化、民用出海。</p><ul><li><b>北斗全球化</b>：北斗三号全球组网后海外授权与特色服务打开空间。</li><li><b>高精度渗透</b>：RTK/板卡从测绘向农机/无人机/自动驾驶下沉。</li><li><b>卫星星座</b>：低轨星座建设拉动星载部件与星敏感器。</li><li><b>国防信息化</b>：北斗终端与抗干扰是装备标配。</li><li><b>民用出海</b>：高精度板卡与农机自动驾驶出海加速。</li></ul>''',\n"
    "        'current': '卫星导航呈「北斗全球化 + 高精度渗透 + 卫星星座建设」三轮驱动：北斗三号全球组网后特色服务与海外授权打开空间，高精度定位向农机/无人机/自动驾驶下沉，低轨星座建设拉动星载配套；最大变量是民品价格战、海外竞争与航天计划节奏，北斗授权与高精度放量、星座配套交付是兑现信号。'\n"
    "    },\n"
    "}\n\n\n# 财务 / 估值占位框架"
)
t = t.replace(anchor, satnav_cycle, 1)

# 2) 把 CHAINS 装配段替换为仅导入卫星导航链
idx_chains = t.index('CHAINS = []')
idx_render = t.index('def render_index')
replacement = "from _satnav_data import satnav\n\nCHAINS = [satnav]\n\n"
t = t[:idx_chains] + replacement + t[idx_render:]

open(DST, 'w', encoding='utf-8').write(t)
print('patched ->', DST, 'len', len(t))
