#!/usr/bin/env python
# 部署：仅推送估值回填改动的深链页（含「百度分位」的 berkshire-*-chain-*.html）
import subprocess, json, base64, os, sys, tempfile, time, re

REPO = "amx708/amx708.github.io"
WD = r"C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site"
COMMIT_MSG = "feat: 深链详情页估值刷新 — akshare 百度 PE(TTM)/PB 近十年分位 (2026-07-31)"

def gh(method, path, data=None, jq=None):
    cmd = ["gh", "api", path, "-X", method]
    tf = None
    if data is not None:
        tf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, tf, ensure_ascii=False); tf.flush(); tf.close()
        cmd += ["--input", tf.name]
    if jq:
        cmd += ["--jq", jq]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if tf:
        try: os.unlink(tf.name)
        except: pass
    if r.returncode != 0:
        raise RuntimeError(f"gh {method} {path} 失败: {r.stderr.strip()[:300]}")
    return r.stdout

os.chdir(WD)
# 收集含「百度分位」的链页
files = [f for f in os.listdir('.') if f.startswith("berkshire-") and "-chain-" in f and f.endswith(".html")]
filled = [f for f in files if "百度分位" in open(f, encoding="utf-8").read()]
print("待部署估值回填页:", len(filled))
filled.sort()

for attempt in range(1, 8):
    try:
        main_sha = gh("GET", f"repos/{REPO}/git/refs/heads/main", jq=".object.sha").strip()
        tree_sha = gh("GET", f"repos/{REPO}/git/commits/{main_sha}", jq=".tree.sha").strip()
        print(f"[尝试{attempt}] main={main_sha} base tree={tree_sha}")
        tree_items = []
        for f in filled:
            with open(f, "rb") as fh:
                b = base64.b64encode(fh.read()).decode()
            sha = json.loads(gh("POST", f"repos/{REPO}/git/blobs", data={"content": b, "encoding": "base64"}))["sha"]
            tree_items.append({"path": f, "mode": "100644", "type": "blob", "sha": sha})
        # 分块 <=100
        new_tree_sha = tree_sha
        for i in range(0, len(tree_items), 100):
            chunk = tree_items[i:i+100]
            new_tree_sha = json.loads(gh("POST", f"repos/{REPO}/git/trees",
                            data={"base_tree": new_tree_sha, "tree": chunk}))["sha"]
        new_commit = json.loads(gh("POST", f"repos/{REPO}/git/commits",
                        data={"message": COMMIT_MSG, "tree": new_tree_sha, "parents": [main_sha]}))["sha"]
        gh("PATCH", f"repos/{REPO}/git/refs/heads/main", data={"sha": new_commit, "force": False})
        gh("POST", f"repos/{REPO}/pages/builds")
        print(f"__DONE__{new_commit} files={len(filled)}")
        break
    except RuntimeError as e:
        err = str(e)
        if any(k in err for k in ("409","422","conflict","rate limit","TLS","timeout","handshake","connection reset","EOF","i/o timeout","network is unreachable")):
            print(f"  冲突/限流/网络抖动重试... {err[:120]}"); time.sleep(4); continue
        raise
else:
    print("重试超限"); sys.exit(1)
