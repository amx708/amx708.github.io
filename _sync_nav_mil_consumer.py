# -*- coding: utf-8 -*-
"""同步军工电子 / 消费电子两条新链的三处导航入口：index 卡片 / chains-hub hcard + 计数 / (chain-map 由 _build_chain_map.py 重生)。"""
import os

DEPLOY = "deploy_site"

MIL_CARD = '''    <a class="card" href="./berkshire-mil-electronics-chains.html">
      <span class="card-icon">🛰️</span>
      <div class="card-title">军工电子产业链</div>
      <div class="card-desc">10 家军工电子上市公司（雷达 / 制导 / 元器件）跨 5 层全栈梳理（基础元件—核心部件—系统总成），框架级原创整理，含产业周期判断标准。</div>
      <div class="card-meta">
        <span class="card-tag tag-blue">10 家军工电子</span>
        <span class="card-tag tag-amber">5 层跨链</span>
      </div>
    </a>
'''

CONSUMER_CARD = '''    <a class="card" href="./berkshire-consumer-electronics-chains.html">
      <span class="card-icon">📱</span>
      <div class="card-title">消费电子产业链</div>
      <div class="card-desc">8 家消费电子上市公司（手机 / PC / 可穿戴 / 精密制造）跨 5 层全栈梳理（零部件—模组—终端），框架级原创整理，含产业周期判断标准。</div>
      <div class="card-meta">
        <span class="card-tag tag-blue">8 家消费电子</span>
        <span class="card-tag tag-amber">5 层跨链</span>
      </div>
    </a>
'''

MIL_HCARD = '<div class="hcard" style="border-top:3px solid #0ea5e9"><div class="hname" style="color:#0ea5e9">军工电子<span class="htag">装备信息化</span></div><div class="hstat">军工电子（新链）｜雷达/制导/核心元器件，受益装备放量、信息化升级与自主可控（框架级整理·数据2026-07）</div><div class="hlinks"><a href="berkshire-mil-electronics-chains.html">图谱</a><span style="opacity:.55;font-size:12px;margin-left:6px">对比/温度计等建设中</span></div></div>'

CONSUMER_HCARD = '<div class="hcard" style="border-top:3px solid #8b5cf6"><div class="hname" style="color:#8b5cf6">消费电子<span class="htag">精密制造</span></div><div class="hstat">消费电子（新链）｜手机/PC/可穿戴精密制造，受益换机周期回暖、AI 终端创新与龙头集中（框架级整理·数据2026-07）</div><div class="hlinks"><a href="berkshire-consumer-electronics-chains.html">图谱</a><span style="opacity:.55;font-size:12px;margin-left:6px">对比/温度计等建设中</span></div></div>'

# 1) index.html
p = os.path.join(DEPLOY, "index.html")
t = open(p, encoding="utf-8").read()
anchor_card = '    <a class="card" href="./berkshire-chem-chains.html">'
assert anchor_card in t, "index chem card anchor not found"
if "berkshire-mil-electronics-chains.html" not in t and "berkshire-consumer-electronics-chains.html" not in t:
    t = t.replace(anchor_card, MIL_CARD + CONSUMER_CARD + anchor_card, 1)
    print("index.html: 2 cards inserted")
else:
    print("index.html: cards already present, skip")
open(p, "w", encoding="utf-8", newline="").write(t)

# 2) chains-hub.html
p = os.path.join(DEPLOY, "berkshire-chains-hub.html")
t = open(p, encoding="utf-8").read()
anchor_hcard = 'border-top:3px solid #84cc16"><div class="hname" style="color:#84cc16">化工'
assert anchor_hcard in t, "hub chem hcard anchor not found"
if "berkshire-mil-electronics-chains.html" not in t and "berkshire-consumer-electronics-chains.html" not in t:
    t = t.replace(anchor_hcard, MIL_HCARD + CONSUMER_HCARD + anchor_hcard, 1)
    print("chains-hub.html: 2 hcards inserted")
else:
    print("chains-hub.html: hcards already present, skip")
# 计数 14 -> 16
n1 = t.count("14 条产业链")
n2 = t.count("14 链")
t = t.replace("14 条产业链", "16 条产业链")
t = t.replace("14 链", "16 链")
print(f"chains-hub.html: counts replaced (14 条产业链 x{n1}, 14 链 x{n2})")
open(p, "w", encoding="utf-8", newline="").write(t)

print("NAV SYNC DONE")
