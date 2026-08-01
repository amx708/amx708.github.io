#!/usr/bin/env python3
# 监控「全站深凿升级」线上部署进度：数 main 上基准 commit 之后的深凿切片 commit 数 / 总切片数
import json, time, subprocess, os

BASE = "9530f976abb8"   # aa 切片推送前的 main 顶端（7-31 最后一次旧提交）
TOTAL_SLICES = 13       # 1244 页拆成 13 个切片
SLICE_SEC = 330         # 每切片约 5.5 分钟（实测 aa=5m30s）
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_progress.json")

def count_slices():
    """数 main 上 BASE 之后的 commit 数量（每个切片 = 1 次 push = 1 个 commit）"""
    try:
        out = subprocess.run(
            ["gh", "api", "repos/amx708/amx708.github.io/commits?per_page=30"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(out.stdout)
        cnt = 0
        for c in data:
            sha = c["sha"][:12]
            if sha == BASE:
                break
            cnt += 1
        return cnt
    except Exception as e:
        return -1

def main():
    last = None
    while True:
        done = count_slices()
        if done < 0:
            done = last if last is not None else 0
        last = done
        remaining = max(0, TOTAL_SLICES - done)
        status = "done" if remaining == 0 else "deploying"
        eta = remaining * SLICE_SEC
        data = {
            "total": TOTAL_SLICES,
            "done": done,
            "remaining": remaining,
            "percent": round(done / TOTAL_SLICES * 100, 1),
            "rate_per_min": round(60 / SLICE_SEC, 2),
            "eta_sec": eta,
            "elapsed_sec": 0,
            "status": status,
            "updated": time.strftime("%H:%M:%S"),
            "phase": "deploy",
        }
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        time.sleep(15)

if __name__ == "__main__":
    main()
