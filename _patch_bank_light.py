# -*- coding: utf-8 -*-
# 把 _build_bank_chain_pages.py 的 BANK_CSS 从深色玻璃风改为浅色风（改 :root 变量 + 几处硬编码深色）。

LIGHT_BANK_CSS = """
:root{--bg:#f0f2f5;--soft:#f8fafc;--card:#ffffff;--ink:#1e293b;--mut:#64748b;--line:rgba(0,0,0,.09);--red:#dc2626;--green:#16a34a;--accent:#3b82f6;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;font-size:15px;-webkit-font-smoothing:antialiased}
.nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{max-width:1080px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.nav .brand{color:var(--ink);font-weight:600;font-size:15px;letter-spacing:.3px}
.nav .crumb{color:var(--mut);font-size:12.5px}
.nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:4px 9px;border-radius:6px;transition:.15s}
.nav a:hover{color:var(--accent);background:var(--soft)}
.hero{background:linear-gradient(135deg,#ffffff 0%,#f1f5f9 100%);border-bottom:1px solid var(--line);padding:46px 20px 38px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.hero-in{max-width:1080px;margin:0 auto}
.hero h1{margin:0 0 10px;font-size:29px;font-weight:700;letter-spacing:-.5px;color:#0f172a}
.hero p{margin:5px 0;color:var(--mut);max-width:760px;font-size:14.5px}
.hero .stat{display:flex;gap:40px;margin-top:26px;flex-wrap:wrap}
.hero .stat b{color:var(--accent);font-size:26px;display:block;font-weight:700}
.hero .stat span{font-size:12px;color:var(--mut)}
.wrap{max-width:1080px;margin:0 auto;padding:30px 20px 70px}
.section-title{font-size:18px;font-weight:700;margin:34px 0 16px;padding-left:12px;border-left:3px solid var(--accent);letter-spacing:-.2px;color:var(--ink)}
.filter{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 22px}
.filter button{border:1px solid var(--line);background:var(--card);color:var(--mut);padding:7px 16px;border-radius:8px;cursor:pointer;font-size:13px;transition:.15s}
.filter button:hover{border-color:var(--accent);color:var(--accent)}
.filter button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;transition:.18s;position:relative;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.card:hover{border-color:var(--accent);box-shadow:0 6px 20px rgba(59,130,246,.14)}
.card .top{display:flex;justify-content:space-between;align-items:baseline}
.card h3{margin:0;font-size:16.5px;font-weight:600;color:var(--ink)}
.card .code{font-size:12px;color:var(--mut)}
.card .cat{display:inline-block;font-size:11px;padding:2px 9px;border-radius:6px;background:var(--soft);color:var(--mut);margin:7px 0}
.card .pos{font-size:12.5px;color:var(--mut);min-height:34px;line-height:1.55}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 8px;margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
.kpis div{font-size:11px;color:var(--mut)}
.kpis b{display:block;color:var(--ink);font-size:14px;font-weight:600}
.detail{max-width:920px;margin:0 auto;padding:28px 20px 70px}
.detail .back{color:var(--accent);text-decoration:none;font-size:13px}
.detail>h1{font-weight:700;letter-spacing:-.5px;color:var(--ink)}
.layer{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:10px 0}
.layer h4{margin:0 0 4px;font-size:14px;color:var(--accent);font-weight:600}
.layer p{margin:0;font-size:13.5px;color:var(--mut);line-height:1.65}
.snap{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:16px 0}
.snap div{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:12px 10px;text-align:center}
.snap b{display:block;font-size:19px;color:var(--accent);font-weight:700}
.snap span{font-size:11px;color:var(--mut)}
.deep{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 18px 14px;margin:14px 0}
.deep h4{margin:0 0 6px;font-size:14px;color:var(--accent);font-weight:600}
.deep-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.deep-item{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:var(--soft)}
.deep-item h4{margin:0 0 6px;font-size:14px;color:var(--accent);font-weight:600}
.deep-item p{margin:0;font-size:13px;color:var(--ink);line-height:1.65}
.deep ul{margin:6px 0;padding-left:18px;font-size:13px;color:var(--ink);line-height:1.6}
.timeline{border-left:2px solid var(--line);padding-left:16px;margin:8px 0 8px 6px}
.timeline div{position:relative;font-size:13px;color:var(--ink);margin:8px 0;padding-left:2px}
.timeline div::before{content:'';position:absolute;left:-21px;top:7px;width:8px;height:8px;border-radius:50%;background:var(--accent)}
.note{background:var(--soft);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:12px 16px;margin:14px 0;font-size:13px;color:var(--mut);line-height:1.65}
.note a{color:var(--accent)}
.extend{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:14px}
.extend a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;text-decoration:none;color:var(--ink);transition:.18s;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.extend a:hover{border-color:var(--accent);box-shadow:0 6px 18px rgba(59,130,246,.14)}
.extend b{color:var(--accent);display:block;margin-bottom:5px;font-weight:600}
.extend span{font-size:12.5px;color:var(--mut);line-height:1.55}
.tbl{width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.tbl th,.tbl td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:center}
.tbl th{background:var(--soft);color:var(--ink);font-weight:600;border-bottom:2px solid var(--line)}
.tbl tr:hover td{background:var(--soft)}
.tag{display:inline-block;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600}
.tag.low{background:rgba(220,38,38,.12);color:var(--red)}
.tag.mid{background:rgba(59,130,246,.14);color:#2563eb}
.tag.high{background:rgba(22,163,74,.14);color:var(--green)}
.thermo{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}
.thermo .nm{width:130px;font-weight:600;font-size:14px;color:var(--ink)}
.thermo .bar{flex:1;height:10px;background:linear-gradient(90deg,#f87171,#e8b84b,#34d399);border-radius:6px;position:relative;min-width:160px;opacity:.85}
.thermo .dot{position:absolute;top:-4px;width:18px;height:18px;border-radius:50%;background:var(--card);border:3px solid var(--accent);transform:translateX(-50%);box-shadow:0 1px 3px rgba(0,0,0,.3)}
.thermo .v{font-size:12.5px;color:var(--mut);width:160px}
footer{background:var(--soft);color:var(--mut);text-align:center;padding:26px 20px;font-size:12.5px;border-top:1px solid var(--line)}
.svgbox{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:16px 0;overflow-x:auto}
.guide{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:14px 0}
.guide h4{margin:0 0 8px;color:var(--accent);font-weight:600}
.guide p,.guide li{font-size:13.5px;color:var(--ink);line-height:1.7}
@media(max-width:600px){.grid{grid-template-columns:1fr}.hero h1{font-size:23px}.hero .stat{gap:24px}.thermo .nm{width:100px}}
/* ---- 产业链三层流 ---- */
.flow3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:18px 0}
.flow3 .stage{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 16px 10px;position:relative;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.flow3 .stage .sno{position:absolute;top:-12px;left:16px;background:var(--accent);color:#fff;font-size:12px;font-weight:600;padding:3px 11px;border-radius:20px}
.flow3 .stage h4{margin:6px 0 2px;font-size:15px;color:var(--accent);font-weight:600}
.flow3 .stage .tagline{font-size:12px;color:var(--mut);margin-bottom:10px;line-height:1.5}
.node{background:var(--soft);border:1px solid var(--line);border-radius:9px;padding:10px 12px;margin:8px 0}
.node b{display:block;font-size:13.5px;color:var(--ink)}
.node span{font-size:12px;color:var(--mut);line-height:1.5}
.flow-cap{text-align:center;font-size:12.5px;color:var(--mut);margin:2px 0 18px}
.flow-cap b{color:var(--accent)}
@media(max-width:768px){.flow3{grid-template-columns:1fr}}
/* ---- 对比工具 ---- */
.cmp-ctrl{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:14px 0;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.cmp-ctrl .bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.cmp-ctrl input[type=text]{flex:1;min-width:180px;border:1px solid var(--line);border-radius:8px;padding:9px 12px;font-size:13px;outline:none;background:var(--bg);color:var(--ink)}
.cmp-ctrl input[type=text]:focus{border-color:var(--accent)}
.cmp-ctrl .fbtn{border:1px solid var(--line);background:var(--soft);color:var(--mut);padding:7px 14px;border-radius:8px;cursor:pointer;font-size:13px}
.cmp-ctrl .fbtn.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.cmp-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;max-height:230px;overflow:auto;padding:4px}
.cmp-item{display:flex;align-items:center;gap:8px;font-size:13px;padding:6px 9px;border:1px solid var(--line);border-radius:8px;cursor:pointer;transition:.15s}
.cmp-item:hover{border-color:var(--accent)}
.cmp-item input{accent-color:var(--accent);width:15px;height:15px}
.cmp-item .cc{font-size:11px;color:var(--mut)}
.cmp-sel{font-size:12.5px;color:var(--mut);margin:6px 0}
.cmp-good{color:var(--green);font-weight:600}
.cmp-bad{color:var(--red);font-weight:600}
"""

fn = r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\deploy_site\_build_bank_chain_pages.py"
s = open(fn, encoding="utf-8").read()
marker = 'BANK_CSS = """'
start = s.index(marker) + len(marker)
end = s.index('"""', start)
s2 = s[:start] + LIGHT_BANK_CSS + s[end:]
assert "#0a0e1a" not in s2, "深色背景残留(bank)"
assert "#f0f2f5" in s2, "浅色背景未写入(bank)"
# 同步更新顶部注释
s2 = s2.replace("（深色玻璃 · 霓虹金融蓝，与 AI/机器人/白酒 三链统一）", "（浅色风，与主页及 11 条产业链统一）")
open(fn, "w", encoding="utf-8").write(s2)
print("OK 改写浅色(bank)")
