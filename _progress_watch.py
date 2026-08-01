#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""实时监视深凿升级进度，写出 _progress.json 供进度条页面读取。"""
import os, time, json, glob, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
CHANGED = os.path.join(BASE, "._deep_changed.txt")
JSON_OUT = os.path.join(BASE, "_progress.json")
TOTAL = len(glob.glob(os.path.join(BASE, "berkshire-*-chain-*.html")))

def proc_alive():
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*_build_deep_all*'} | Measure-Object | Select-Object -ExpandProperty Count"],
            capture_output=True, text=True, timeout=10).stdout.strip()
        return int(out or 0) > 0
    except Exception:
        return True

start = time.time()
prev_done = None
prev_t = None
while True:
    try:
        with open(CHANGED, encoding="utf-8") as f:
            done = sum(1 for _ in f)
    except FileNotFoundError:
        done = 0
    now = time.time()
    elapsed = now - start
    remaining = max(0, TOTAL - done)
    # 滑动窗口瞬时速率（相邻两次真实增量）
    rate_per_sec = 0.0
    if prev_done is not None and (now - prev_t) > 0:
        rate_per_sec = (done - prev_done) / (now - prev_t)
    prev_done, prev_t = done, now
    eta = remaining / rate_per_sec if rate_per_sec > 0 else 0
    alive = proc_alive()
    if remaining == 0:
        status = "done"
    elif alive:
        status = "running"
    else:
        status = "stalled"
    data = {
        "total": TOTAL, "done": done, "remaining": remaining,
        "percent": round(done / TOTAL * 100, 1) if TOTAL else 0,
        "rate_per_min": round(rate_per_sec * 60, 1),
        "eta_sec": round(eta),
        "elapsed_sec": round(elapsed),
        "status": status,
        "updated": time.strftime("%H:%M:%S"),
    }
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    if status == "done":
        break
    time.sleep(2)
