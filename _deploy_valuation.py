#!/usr/bin/env python
# 部署：仅推送估值回填改动的深链页（含「百度分位」的 berkshire-*-chain-*.html）
#
# 抗并发改进（2026-08-02）：blob 仅创建一次；commit/ref 阶段在紧凑重试循环里
# 反复重取 main 并重建 tree+commit，从而能在「抢 main 锁」的并发推送间隙落地，
# 不再每次重试都重做 ~1000 个 blob POST（旧逻辑每次尝试 ~22min，遇持续 409 必被 SIGKILL）。
import subprocess, json, base64, os, sys, tempfile, time, re

REPO = "amx708/amx708.github.io"
WD = r"C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site"
COMMIT_MSG = "feat: 深链详情页估值刷新 — akshare 百度 PE(TTM)/PB 近十年分位 (2026-08-02)"

RETRY_KEYS = ("409","422","conflict","rate limit","TLS","timeout","handshake",
              "connection reset","EOF","i/o timeout","network is unreachable")

def gh(method, path, data=None, jq=None, tries=4):
    cmd = ["gh", "api", path, "-X", method]
    tf = None
    if data is not None:
        tf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, tf, ensure_ascii=False); tf.flush(); tf.close()
        cmd += ["--input", tf.name]
    if jq:
        cmd += ["--jq", jq]
    last = None
    for _ in range(tries):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if tf:
            try: os.unlink(tf.name)
            except: pass
        if r.returncode == 0:
            return r.stdout
        last = r.stderr.strip()[:300]
        if not any(k in last for k in RETRY_KEYS):
            raise RuntimeError(f"gh {method} {path} 失败: {last}")
        time.sleep(3)
    raise RuntimeError(f"gh {method} {path} 失败(重试耗尽): {last}")

os.chdir(WD)
# 收集含「百度分位」的链页
files = [f for f in os.listdir('.') if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
filled = [f for f in files if "百度分位" in open(f, encoding="utf-8").read()]
print("待部署估值回填页:", len(filled))
filled.sort()

# ---- 阶段1：创建 blob（仅一次，内容寻址，并发无关）----
print("创建 blob ...")
tree_items = []
for f in filled:
    with open(f, "rb") as fh:
        b = base64.b64encode(fh.read()).decode()
    sha = json.loads(gh("POST", f"repos/{REPO}/git/blobs",
                        data={"content": b, "encoding": "base64"}, tries=5))["sha"]
    tree_items.append({"path": f, "mode": "100644", "type": "blob", "sha": sha})
print(f"blob 创建完成: {len(tree_items)}")

# ---- 阶段2：紧凑重试 commit/ref（反复重取 main，抢到稳定间隙即落地）----
MAX_ROUNDS = 400
for rnd in range(1, MAX_ROUNDS + 1):
    try:
        main_sha = gh("GET", f"repos/{REPO}/git/refs/heads/main", jq=".object.sha").strip()
        tree_sha = gh("GET", f"repos/{REPO}/git/commits/{main_sha}", jq=".tree.sha").strip()
        new_tree_sha = tree_sha
        for i in range(0, len(tree_items), 100):
            chunk = tree_items[i:i+100]
            new_tree_sha = json.loads(gh("POST", f"repos/{REPO}/git/trees",
                            data={"base_tree": new_tree_sha, "tree": chunk}))["sha"]
        new_commit = json.loads(gh("POST", f"repos/{REPO}/git/commits",
                        data={"message": COMMIT_MSG, "tree": new_tree_sha, "parents": [main_sha]}))["sha"]
        gh("PATCH", f"repos/{REPO}/git/refs/heads/main", data={"sha": new_commit, "force": False})
        gh("POST", f"repos/{REPO}/pages/builds")
        print(f"__DONE__{new_commit} files={len(filled)} round={rnd}")
        break
    except RuntimeError as e:
        err = str(e)
        if any(k in err for k in RETRY_KEYS):
            if rnd % 10 == 0 or rnd == 1:
                print(f"  [round {rnd}] 冲突/限流/网络抖动，重取 main 重试... {err[:100]}")
            time.sleep(3)
            continue
        raise
else:
    print("重试超限"); sys.exit(1)
