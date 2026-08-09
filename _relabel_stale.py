# -*- coding: utf-8 -*-
"""#561 修正陈旧「待采集」标签：仅对含「总市值」(即有真实估值数据) 的页面，
把 section-title 的 估值指标（待采集）/财务数据（待采集） 改为（已采集）。
不含总市值的 12 个真空页自动排除。幂等：只替换存在的子串。
产出 _relabel_changed.txt 供部署 cp。
"""
import os, glob

DS = os.path.dirname(os.path.abspath(__file__))
changed = []
n_valu = 0
n_fin = 0
for f in sorted(glob.glob(os.path.join(DS, "*.html"))):
    t = open(f, encoding="utf-8", errors="ignore").read()
    if "待采集" not in t:
        continue
    if "总市值" not in t:
        continue  # 真空页，跳过（单独用真实数据补）
    nt = t
    if "估值指标（待采集）" in nt:
        nt = nt.replace("估值指标（待采集）", "估值指标（已采集）")
        n_valu += 1
    if "财务数据（待采集）" in nt:
        nt = nt.replace("财务数据（待采集）", "财务数据（已采集）")
        n_fin += 1
    if nt != t:
        open(f, "w", encoding="utf-8").write(nt)
        changed.append(os.path.basename(f))

with open(os.path.join(DS, "_relabel_changed.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(changed))

print(f"relabeled files: {len(changed)}")
print(f"  估值指标（待采集）→（已采集）: {n_valu} 处")
print(f"  财务数据（待采集）→（已采集）: {n_fin} 处")
print(f"manifest -> _relabel_changed.txt ({len(changed)} entries)")
