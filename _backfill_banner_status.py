#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐 26 个老模板产业链索引页的「建设状态」banner 区块。
文案通用(本链...), 不依赖员工效率/三件套等其他模块, 直接追加到页尾 content 容器内。
幂等: 已含 <h2>建设状态</h2> 的页跳过。"""
import os, glob, io

REPO = os.path.dirname(os.path.abspath(__file__))

BANNER = (
    '<div class="block"><h2>建设状态</h2>\n'
    '    <div class="desc">本链为阶段 A「铺满地图」框架版：五层框架与代表公司索引已建；'
    '估值历史分位(PE/PB)与泊松跳变信号已基于 akshare 公开行情回填（详情页可见），'
    '2025 年报财报基本面与组织效能(员工效率)模块待采集，后续按同规格回填。'
    '公司列表为公开资料整理的代表性样本，非穷举。</div></div>\n'
)

# 26 个缺 banner 的老模板页(经普查确认无 <h2>建设状态</h2>)
TARGETS = [
    "berkshire-aero-chains.html","berkshire-ai-chains.html","berkshire-appliance-chains.html",
    "berkshire-baijiu-chains.html","berkshire-bank-chains.html","berkshire-chem-chains.html",
    "berkshire-coal-chains.html","berkshire-consumer-electronics-chains.html","berkshire-equip-chains.html",
    "berkshire-innov-chains.html","berkshire-metal-chains.html","berkshire-mil-electronics-chains.html",
    "berkshire-panel-chains.html","berkshire-pcb-chains.html","berkshire-power-chains.html",
    "berkshire-rare-earth-chains.html","berkshire-robot-chains.html","berkshire-satnav-chains.html",
    "berkshire-securities-chains.html","berkshire-semiconductor-chemical-chains.html",
    "berkshire-semiconductor-design-chains.html","berkshire-semiconductor-equip-chains.html",
    "berkshire-semiconductor-material-chains.html","berkshire-semiconductor-mfg-chains.html",
    "berkshire-shipbuilding-chains.html","berkshire-tcm-chains.html",
]

def anchor(html):
    # 优先 </body>; 否则 </html>; 否则最后一个 </div>
    for tag in ("</body>", "</html>"):
        i = html.rfind(tag)
        if i != -1:
            return i, tag
    i = html.rfind("</div>")
    return (i, "</div>") if i != -1 else (-1, "")

done, skipped, failed = [], [], []
for name in TARGETS:
    path = os.path.join(REPO, name)
    if not os.path.exists(path):
        failed.append((name, "文件不存在")); continue
    with io.open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if "<h2>建设状态</h2>" in html or "建设状态" in html:
        skipped.append(name); continue
    idx, tag = anchor(html)
    if idx == -1:
        failed.append((name, "无插入锚点")); continue
    new = html[:idx] + BANNER + html[idx:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(new)
    done.append(name)

print("已补齐:", len(done))
for d in done: print("  +", d)
print("跳过(已有):", len(skipped), skipped)
print("失败:", len(failed), failed)
