# -*- coding: utf-8 -*-
"""#562 填充 4 个 AI 链 A 股公司页（北方华创/寒武纪/浪潮信息/中际旭创）的 Format A 合成块。
读取 _valuation_cache.json（002371/300308 已有真实 PE%/PB%）；688256/000977 实时源当前
不可达 -> 诚实标注「实时行情接口当前环境不可用」，不编造。
幂等：仅当页面仍存在「数据不足」占位时才替换。
"""
import os, re, json

DS = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DS, "_valuation_cache.json")
cache = json.load(open(CACHE, encoding="utf-8"))

# slug -> (code, name)
PAGES = {
    "berkshire-ai-chain-beifanghuachuang.html": ("002371", "北方华创"),
    "berkshire-ai-chain-hanwujie.html": ("688256", "寒武纪"),
    "berkshire-ai-chain-langchao.html": ("000977", "浪潮信息"),
    "berkshire-ai-chain-zhongjixuchuang.html": ("300308", "中际旭创"),
}

def valid(pe, pb):
    return (isinstance(pe, dict) and "v" in pe and isinstance(pe.get("p"), (int, float))
            and isinstance(pb, dict) and "v" in pb and isinstance(pb.get("p"), (int, float)))

def fill_page(fname, code, name):
    path = os.path.join(DS, fname)
    if not os.path.exists(path):
        return f"{fname}: MISSING"
    t = open(path, encoding="utf-8").read()
    if "数据不足" not in t:
        return f"{fname}: already-filled (skip)"

    ent = cache.get(code, {})
    pe = ent.get("市盈率(TTM)", {})
    pb = ent.get("市净率", {})
    if not valid(pe, pb):
        # 实时源不可达：诚实标注，不编造
        t = t.replace(
            "synth-verdict\"><b>综合结论：</b>估值数据不足（待采集），无法做便宜/贵判定</div>",
            "synth-verdict\"><b>综合结论：</b>估值数据不足（实时行情接口当前环境不可用，待恢复后补），无法做便宜/贵判定</div>")
        open(path, "w", encoding="utf-8").write(t)
        return f"{fname} ({code} {name}): NET-BLOCKED -> 诚实标注"

    X = pe["p"]; Y = pb["p"]
    avg = (X + Y) / 2.0
    cheap_disp = "便宜" if avg < 40 else ("贵" if avg > 60 else "中性")
    pe_hit = "已触发" if X < 20 else "未触发（当前偏贵）"
    pb_hit = "已触发" if Y < 20 else "未触发（当前偏贵）"
    pe_cls = "db-on" if X < 20 else "db-off"
    pb_cls = "db-on" if Y < 20 else "db-off"
    pe_mg = "mg-on" if X < 20 else "mg-off"
    pb_mg = "mg-on" if Y < 20 else "mg-off"
    verdict = (f"{cheap_disp}（护城河数据不足，需自行核验基本面）" if cheap_disp != "贵"
               else "贵（护城河数据不足）")
    if cheap_disp == "贵":
        verdict = "贵的好生意（资产优质，但价格未给安全边际，等更好买点）" if False else "贵（护城河数据不足）"
    # SVG
    cx = round(70 + avg * 5.7, 1)
    cy = 105  # tech 链 permanent_risk=高
    fill = "#E24B4A" if cheap_disp == "贵" else ("#BA7517" if cheap_disp == "中性" else "#639922")
    zone = "甜区（便宜+低风险）" if cheap_disp == "便宜" else ("回避区（贵+高风险）" if cheap_disp == "贵" else "中区")
    rng = "<40%" if avg < 40 else (">60%" if avg > 60 else "中性")
    new_tip = (f"<b>{code} {name}</b><br>估值分位：PE {X}% / PB {Y}% → {cheap_disp}（{rng}）"
               f"<br>永久损失风险：高<br>护城河：数据不足（ROE 待采集）<br>信号：数据不足<br>落位：{zone}")

    # 1) 估值便宜度 card
    t = t.replace(
        'db-val">数据不足</div><div class="db-sub">PE —% · PB —%</div>',
        f'db-val">{cheap_disp}</div><div class="db-sub">PE {X}% · PB {Y}%</div>')
    # 2) chips
    t = t.replace('db-chip db-na">PB分位 数据不足</span>',
                  f'db-chip {pb_cls}">PB分位 {Y}% · {pb_hit}</span>')
    t = t.replace('db-chip db-na">PE分位 数据不足</span>',
                  f'db-chip {pe_cls}">PE分位 {X}% · {pe_hit}</span>')
    # 3) verdict
    t = t.replace(
        "synth-verdict\"><b>综合结论：</b>估值数据不足（待采集），无法做便宜/贵判定</div>",
        f"synth-verdict\"><b>综合结论：</b>{verdict}</div>")
    # 4) mg-rows
    t = t.replace(
        'mg-row mg-na"><div class="mg-label">PB分位</div><div class="mg-track"><div class="mg-bar" style="width:0%"></div></div><div class="mg-meta"><span class="mg-status">数据不足</span>',
        f'mg-row {pb_mg}"><div class="mg-label">PB分位</div><div class="mg-track"><div class="mg-bar" style="width:{Y}%</div></div></div><div class="mg-meta"><span class="mg-status {pb_mg}">{Y}% · {pb_hit}</span>')
    t = t.replace(
        'mg-row mg-na"><div class="mg-label">PE分位</div><div class="mg-track"><div class="mg-bar" style="width:0%"></div></div><div class="mg-meta"><span class="mg-status">数据不足</span>',
        f'mg-row {pe_mg}"><div class="mg-label">PE分位</div><div class="mg-track"><div class="mg-bar" style="width:{X}%</div></div></div><div class="mg-meta"><span class="mg-status {pe_mg}">{X}% · {pe_hit}</span>')
    # 5) SVG stock circle
    pat = re.compile(
        r'<circle cx="[\d.]+" cy="[\d.]+" r="12" fill="#639922" stroke="#ffffff" stroke-width="3" data-tip="<b>'
        + re.escape(f"{code} {name}") + r'</b><br>估值分位：PE —% / PB —% → 数据不足[^"]*"')
    new_circle = (f'<circle cx="{cx}" cy="{cy}" r="12" fill="{fill}" stroke="#ffffff" stroke-width="3" '
                  f'data-tip="{new_tip}"')
    t, n = pat.subn(new_circle, t)
    if n == 0:
        # fallback: any stock circle with 数据不足
        pat2 = re.compile(r'<circle cx="355.0" cy="220.0" r="12"[^>]*data-tip="[^"]*→ 数据不足[^"]*"')
        t, n = pat2.subn(new_circle, t)

    open(path, "w", encoding="utf-8").write(t)
    return f"{fname} ({code} {name}): FILLED PE={X}% PB={Y}% avg={avg:.1f}% -> {cheap_disp} (cx={cx},cy={cy},n={n})"

if __name__ == "__main__":
    for f, (c, n) in PAGES.items():
        print(fill_page(f, c, n))
