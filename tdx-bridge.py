#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伯克希尔数据中心 — 通达信联动桥梁
运行方式：双击此文件（或用 python tdx-bridge.py），保持窗口后台运行
作用：接收网页 http://127.0.0.1:8765/jump?code=601288 请求，
      向已运行的通达信/券商定制版发送 Stock 广播消息，自动跳到该股 K 线。
"""
import sys
import re
import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

# 尝试导入 pywin32；若失败则给出友好提示
try:
    import win32api
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

HOST = "127.0.0.1"
PORT = 8765


def tdx_jump(code: str) -> dict:
    """向通达信发送 Stock 广播消息"""
    if not HAS_WIN32:
        return {"ok": False, "error": "缺少 pywin32 依赖，请执行：pip install pywin32"}

    # 只取 6 位数字
    m = re.search(r"\d{6}", code)
    if not m:
        return {"ok": False, "error": "股票代码必须是 6 位数字"}
    code6 = m.group(0)

    # wParam 编码：沪市 6/9/5 开头 -> 7+code；其它 -> 6+code
    first = code6[0]
    prefix = "7" if first in "695" else "6"
    wparam = int(prefix + code6)

    # 同时尝试 "Stock" / "stock" 两种注册名（不同券商版可能大小写不同）
    for name in ("Stock", "stock"):
        try:
            msg_id = win32api.RegisterWindowMessage(name)
            if msg_id:
                win32gui.PostMessage(win32con.HWND_BROADCAST, msg_id, wparam, 0)
        except Exception as e:
            return {"ok": False, "error": f"发送失败: {e}"}

    return {"ok": True, "code": code6, "wparam": wparam}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 简化日志，避免刷屏
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        # 跨域允许本地网页调用
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

        if parsed.path == "/jump":
            code = params.get("code", [""])[0]
            result = tdx_jump(code)
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            if result.get("ok"):
                print(f"[OK] 已联动 {result['code']} (wParam={result['wparam']})")
            else:
                print(f"[ERR] {result.get('error')}")
        else:
            self.wfile.write(json.dumps({"ok": False, "error": "未知路径，请使用 /jump?code=xxxxxx"}, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()


def main():
    if not HAS_WIN32:
        print("ERROR: 当前 Python 环境没有 pywin32。")
        print("请在同一 Python 下执行：pip install pywin32")
        input("按回车退出...")
        sys.exit(1)

    print(f"通达信联动桥梁已启动：http://{HOST}:{PORT}")
    print("使用方式：")
    print("  1) 保持本窗口运行（最小化即可）")
    print("  2) 在伯克希尔数据中心网页点击股票代码")
    print("  3) 确保通达信/券商定制版已经运行")
    print("")

    server = HTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已退出")


if __name__ == "__main__":
    main()
