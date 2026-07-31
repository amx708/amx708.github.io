# -*- coding: utf-8 -*-
"""同步半导体设备链的三处导航入口：index 卡片 / chains-hub hcard + 计数 / (chain-map 由 _build_chain_map.py 重生)。"""
import os

DEPLOY = "deploy_site"

CARD = '''    <a class="card" href="./berkshire-semiconductor-equip-chains.html">
      <span class="card-icon">🔬</span>
      <div class="card-title">半导体设备产业链</div>
      <div class="card-desc">12 家半导体设备上市公司（刻蚀 / 薄膜 / 清洗 / CMP / 量测）跨 5 层全栈梳理（零部件—设备—fab—国产替代），框架级原创整理，含产业周期判断标准。</div>
      <div class="card-meta">
        <span class="card-tag tag-blue">12 家设备</span>
        <span class="card-tag tag-amber">5 层跨链</span>
      </div>
    </a>
'''

HCARD = '''<div class="hcard" style="border-top:3px solid #6366f1"><div class="hname" style="color:#6366f1">半导体设备<span class="htag">国产替代</span></div><div class="hstat">半导体设备（新链）｜刻蚀/薄膜/清洗/CMP/量测全品类国产突破，受益晶圆厂扩产与自主可控（框架级整理·数据2026-07）</div><div class="hlinks"><a href="berkshire-semiconductor-equip-chains.html">图谱</a><span style="opacity:.55;font-size:12px;margin-left:6px">对比/温度计等建设中</span></div></div>'''

# 1) index.html
p = os.path.join(DEPLOY, "index.html")
t = open(p, encoding="utf-8").read()
anchor_card = '    <a class="card" href="./berkshire-chem-chains.html">'
assert anchor_card in t, "index chem card anchor not found"
if "berkshire-semiconductor-equip-chains.html" not in t:
    t = t.replace(anchor_card, CARD + anchor_card, 1)
    print("index.html: card inserted")
else:
    print("index.html: card already present, skip")
open(p, "w", encoding="utf-8", newline="").write(t)

# 2) chains-hub.html
p = os.path.join(DEPLOY, "berkshire-chains-hub.html")
t = open(p, encoding="utf-8").read()
anchor_hcard = 'border-top:3px solid #84cc16"><div class="hname" style="color:#84cc16">化工'
assert anchor_hcard in t, "hub chem hcard anchor not found"
if "berkshire-semiconductor-equip-chains.html" not in t:
    t = t.replace(anchor_hcard, HCARD + anchor_hcard, 1)
    print("chains-hub.html: hcard inserted")
else:
    print("chains-hub.html: hcard already present, skip")
# 计数 13 -> 14
n1 = t.count("13 条产业链")
n2 = t.count("13 链")
t = t.replace("13 条产业链", "14 条产业链")
t = t.replace("13 链", "14 链")
print(f"chains-hub.html: counts replaced (13 条产业链 x{n1}, 13 链 x{n2})")
open(p, "w", encoding="utf-8", newline="").write(t)

print("NAV SYNC DONE")
