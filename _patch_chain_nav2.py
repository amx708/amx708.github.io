import io, re, glob, os

# 1) 回滚之前注入的错误 nav span；2) 健壮重注入（两种 home-btn 变体 + 正确主色）
LINKS = [
    ("银行", "berkshire-bank-chains.html"),
    ("白酒", "berkshire-baijiu-chains.html"),
    ("AI",   "berkshire-ai-chains.html"),
    ("机器人", "berkshire-robot-chains.html"),
]
FAM = {"ai": "AI", "baijiu": "白酒", "robot": "机器人"}

def cur_label(name):
    for k, v in FAM.items():
        if k in name:
            return v
    return ""

def accent_of(s):
    m = re.search(r'\.home-btn\s*\{[^}]*?color:(#[0-9a-fA-F]{6})', s)
    return m.group(1) if m else "#22d3ee"

def revert(s):
    return re.sub(r'<span style="display:inline-flex;gap:14px;align-items:center;margin-left:10px">.*?</span>', '', s, flags=re.S)

def inject(s, label, accent):
    if "berkshire-bank-chains.html" in s:
        return s  # 已注入
    anc = re.search(r'<a href="berkshire-standalone\.html" class="home-btn[^"]*">← 数据中心</a>', s) \
       or re.search(r'<a href="berkshire-(?:ai|robot|baijiu)-chains\.html" class="home-btn[^"]*">← 产业链地图</a>', s)
    if not anc:
        return None  # 无导航（如 coming 占位页）
    spans = []
    for t, href in LINKS:
        st = f"color:{accent};text-decoration:none;font-size:13px"
        if t == label:
            st += ";font-weight:700"
        spans.append(f'<a href="{href}" style="{st}">{t}</a>')
    block = anc.group(0) + '\n<span style="display:inline-flex;gap:14px;align-items:center;margin-left:10px">' + "".join(spans) + "</span>"
    return s[:anc.start()] + block + s[anc.end():]

roots = [
    "C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site",
    "C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/repo/amx708.github.io",
]
for root in roots:
    print("==", root.split("/")[-1], "==")
    for fam in FAM:
        pat = os.path.join(root, f"berkshire-{fam}-*.html")
        n_ok = n_skip = n_none = 0
        for f in sorted(glob.glob(pat)):
            s = io.open(f, encoding="utf-8").read()
            s2 = revert(s)
            if s2 != s:
                io.open(f, "w", encoding="utf-8").write(s2)
            s3 = io.open(f, encoding="utf-8").read()
            r = inject(s3, cur_label(os.path.basename(f)), accent_of(s3))
            if r is None:
                n_none += 1
            elif r == s3:
                n_skip += 1
            else:
                io.open(f, "w", encoding="utf-8").write(r)
                n_ok += 1
        print(f"  {fam}: 注入 {n_ok} / 跳过(已注入) {n_skip} / 无导航 {n_none}")
print("DONE")
