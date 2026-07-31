#!/usr/bin/env python
# 补推缺失的半导体化学索引页（上次批次漏入 commit）
import subprocess, json, base64, os, sys, tempfile, time

REPO = "amx708/amx708.github.io"
WD = r"C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site"
COMMIT_MSG = "fix: 补推半导体化学产业链索引页 (漏入上批次)"

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
f = "berkshire-semiconductor-chemical-chains.html"

for attempt in range(1, 7):
    try:
        main_sha = gh("GET", f"repos/{REPO}/git/refs/heads/main", jq=".object.sha").strip()
        tree_sha = gh("GET", f"repos/{REPO}/git/commits/{main_sha}", jq=".tree.sha").strip()
        print(f"[尝试{attempt}] main={main_sha} base tree={tree_sha}")
        with open(f, "rb") as fh:
            b = base64.b64encode(fh.read()).decode()
        sha = json.loads(gh("POST", f"repos/{REPO}/git/blobs", data={"content": b, "encoding": "base64"}))["sha"]
        new_tree = json.loads(gh("POST", f"repos/{REPO}/git/trees",
                        data={"base_tree": tree_sha, "tree": [{"path": f, "mode": "100644", "type": "blob", "sha": sha}]}))["sha"]
        new_commit = json.loads(gh("POST", f"repos/{REPO}/git/commits",
                        data={"message": COMMIT_MSG, "tree": new_tree, "parents": [main_sha]}))["sha"]
        gh("PATCH", f"repos/{REPO}/git/refs/heads/main", data={"sha": new_commit, "force": False})
        gh("POST", f"repos/{REPO}/pages/builds")
        print(f"__DONE__{new_commit}")
        break
    except RuntimeError as e:
        err = str(e)
        if ("409" in err or "422" in err or "conflict" in err.lower()):
            print(f"  冲突重试... {err[:100]}"); time.sleep(3); continue
        raise
else:
    print("重试超限"); sys.exit(1)
