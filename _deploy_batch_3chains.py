#!/usr/bin/env python
# blob-first 部署：PCB + 面板 + 半导体化学 三链深页 + 导航三处 + 链地图
import subprocess, json, base64, os, sys, glob, tempfile, time

REPO = "amx708/amx708.github.io"
WD = r"C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site"
COMMIT_MSG = "feat: add PCB(9)+面板(10)+半导体化学(10) 产业链框架链 + 入口导航 (2026-07-30)"

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

# 收集文件：三链深页 + 导航 + 链地图
patterns = [
    "berkshire-pcb-chain-*.html",
    "berkshire-panel-chain-*.html",
    "berkshire-semiconductor-chemical-chain-*.html",
    "index.html",
    "berkshire-chains-hub.html",
    "berkshire-chain-map.html",
]
files = []
for p in patterns:
    files += glob.glob(p)
files = sorted(set(files))
print(f"待推送文件数={len(files)}")

for attempt in range(1, 7):
    try:
        main_sha = gh("GET", f"repos/{REPO}/git/refs/heads/main", jq=".object.sha").strip()
        tree_sha = gh("GET", f"repos/{REPO}/git/commits/{main_sha}", jq=".tree.sha").strip()
        print(f"[尝试{attempt}] 远端 main={main_sha}, base tree={tree_sha}")

        blobs = []
        n = len(files)
        for i, f in enumerate(files, 1):
            with open(f, "rb") as fh:
                b = base64.b64encode(fh.read()).decode()
            out = gh("POST", f"repos/{REPO}/git/blobs", data={"content": b, "encoding": "base64"})
            sha = json.loads(out)["sha"]
            blobs.append({"path": f, "mode": "100644", "type": "blob", "sha": sha})
        # 分块建 tree（≤100）
        new_tree = tree_sha
        for j in range(0, n, 100):
            chunk = blobs[j:j+100]
            td = {"base_tree": new_tree, "tree": chunk} if j == 0 else {"base_tree": new_tree, "tree": chunk}
            to = gh("POST", f"repos/{REPO}/git/trees", data=td)
            new_tree = json.loads(to)["sha"]
        print(f"  new tree={new_tree}")

        co = gh("POST", f"repos/{REPO}/git/commits",
                data={"message": COMMIT_MSG, "tree": new_tree, "parents": [main_sha]})
        new_commit = json.loads(co)["sha"]
        print(f"  new commit={new_commit}")

        gh("PATCH", f"repos/{REPO}/git/refs/heads/main", data={"sha": new_commit, "force": False})
        gh("POST", f"repos/{REPO}/pages/builds")
        print(f"__DONE__{new_commit}")
        break
    except RuntimeError as e:
        err = str(e)
        if ("409" in err or "422" in err or "conflict" in err.lower() or "fetch first" in err.lower()):
            print(f"  冲突/并发，重试... ({err[:120]})")
            time.sleep(3)
            continue
        else:
            raise
else:
    print("超过最大重试次数"); sys.exit(1)
