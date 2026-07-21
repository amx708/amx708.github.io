import io, re, glob, os

# 给 AI / 机器人 / 白酒 三链页面注入与银行页一致的 5 链跨链导航
# 顺序：数据中心(回首页按钮) / 银行 / 白酒 / AI / 机器人；当前页加粗，沿用各自主色
TARGETS = {
    "ai":     ("berkshire-ai-chains.html",     "AI"),
    "baijiu": ("berkshire-baijiu-chains.html", "白酒"),
    "robot":  ("berkshire-robot-chains.html",  "机器人"),
}
LINKS = [
    ("银行", "berkshire-bank-chains.html"),
    ("白酒", "berkshire-baijiu-chains.html"),
    ("AI",   "berkshire-ai-chains.html"),
    ("机器人", "berkshire-robot-chains.html"),
]

def patch(path, current_label, accent):
    s = io.open(path, encoding="utf-8").read()
    if "berkshire-bank-chains.html" in s:
        return False  # 已注入，跳过
    home = re.search(r'<a href="berkshire-standalone\.html" class="home-btn[^"]*">← 数据中心</a>', s)
    if not home:
        print("  !! 未找到 home-btn:", path)
        return False
    spans = []
    for label, href in LINKS:
        if label == current_label:
            style = f"color:{accent};text-decoration:none;font-size:13px;font-weight:700"
        else:
            style = f"color:{accent};text-decoration:none;font-size:13px"
        spans.append(f'<a href="{href}" style="{style}">{label}</a>')
    inject = home.group(0) + '\n<span style="display:inline-flex;gap:14px;align-items:center;margin-left:10px">' + "".join(spans) + "</span>"
    s = s[:home.start()] + inject + s[home.end():]
    io.open(path, "w", encoding="utf-8").write(s)
    return True

def accent_of(path):
    s = io.open(path, encoding="utf-8").read()
    m = re.search(r'\.home-btn\{[^}]*color:(#[0-9a-fA-F]+)', s)
    return m.group(1) if m else "#22d3ee"

roots = [
    "C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site",
    "C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/repo/amx708.github.io",
]
for root in roots:
    print("== root:", root)
    for key, (idx, label) in TARGETS.items():
        idxp = os.path.join(root, idx)
        if not os.path.exists(idxp):
            print("  跳过(无文件):", idx); continue
        acc = accent_of(idxp)
        done = patch(idxp, label, acc)
        # 同族详情页用同一主色
        pat = os.path.join(root, f"berkshire-{key}-*.html")
        n = 0
        for f in glob.glob(pat):
            if os.path.basename(f) == idx:
                continue
            if patch(f, label, acc):
                n += 1
        print(f"  {key}: index={'OK' if done else 'skip'} + 详情页注入 {n} 个 (accent={acc})")
print("DONE")
