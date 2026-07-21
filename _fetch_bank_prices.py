#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量抓取42家银行的后复权(hfq)年线收盘价，输出 HIST_PRICE 字典片段。"""
import subprocess, re, json, sys

NODE = r"C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2/node.exe"
CLI = r"E:/Program Files/WorkBuddy/resources/app.asar.unpacked/resources/builtin-skills/westock-data/scripts/index.js"

# slug -> (name, code)
BANKS = [
    ("icbc","工商银行","601398"),("ccb","建设银行","601939"),("abc","农业银行","601288"),
    ("boc","中国银行","601988"),("bocom","交通银行","601328"),("psbc","邮储银行","601658"),
    ("cmb","招商银行","600036"),("citic","中信银行","601998"),("spdb","浦发银行","600000"),
    ("indy","兴业银行","601166"),("cmbc","民生银行","600016"),("ceb","光大银行","601818"),
    ("hxb","华夏银行","600015"),("pab","平安银行","000001"),("czb","浙商银行","601916"),
    ("bobj","北京银行","601169"),("njcb","南京银行","601009"),("nib","宁波银行","002142"),
    ("shb","上海银行","601229"),("jsb","江苏银行","600919"),("hzb","杭州银行","600926"),
    ("cdb","成都银行","601838"),("csb","长沙银行","601577"),("cqb","重庆银行","601963"),
    ("qdb","青岛银行","002948"),("zzb","郑州银行","002936"),("szb","苏州银行","002966"),
    ("xab","西安银行","600928"),("xmb","厦门银行","601187"),("qlb","齐鲁银行","601665"),
    ("gyb","贵阳银行","601997"),("lzb","兰州银行","001227"),
    ("cqrc","渝农商行","601077"),("qrc","青农商行","002958"),("changshu","常熟银行","601128"),
    ("zijin","紫金银行","601860"),("wuxi","无锡银行","600908"),("zjg","张家港行","002839"),
    ("sunong","苏农银行","603323"),("jiangyin","江阴银行","002807"),("ruifeng","瑞丰银行","601528"),
    ("shnc","沪农商行","601825"),
]

# 目标年份：2014底,2018底,2020底,2022底,2024底,2025底,2026H1(最新)
TARGET_YEARS = ["2014","2018","2020","2022","2024","2025"]

def ts(code):
    return ("sh" if code[0]=="6" else "sz") + code

def fetch(code):
    out = subprocess.run([NODE, CLI, "kline", ts(code), "--period","year","--fq","hfq","--limit","30"],
                         capture_output=True, text=True, encoding="utf-8")
    txt = out.stdout
    rows = {}
    latest = None  # 2026 进行中
    for line in txt.splitlines():
        m = re.match(r"\|\s*(\d{4})-\d{2}-\d{2}\s*\|\s*[\d.]+\s*\|\s*([\d.]+)\s*\|", line)
        if m:
            year, last = m.group(1), float(m.group(2))
            if year == "2026" and latest is None:
                latest = last
            rows[year] = last
    prices = []
    for y in TARGET_YEARS:
        prices.append(rows.get(y))
    prices.append(latest)  # 2026H1
    return prices

result = {}
for slug, name, code in BANKS:
    p = fetch(code)
    result[slug] = p
    print(f"{slug:10s} {name:6s} {code}: {p}", file=sys.stderr)

# 输出可直接粘贴的字典
print("HIST_PRICE_DATA = {")
for slug, name, code in BANKS:
    p = result[slug]
    pv = ", ".join("None" if v is None else f"{v}" for v in p)
    print(f'    "{slug}": [{pv}],  # {name}')
print("}")
