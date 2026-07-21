# -*- coding: utf-8 -*-
# 把 _build_five_chains.py / _build_three_chains.py 的 CSS 从深色玻璃风改为浅色风。
# 仅替换 CSS 三引号整块，保留 __ACC__/__ACC_RGB__/__ACC_DARK__ 占位符。
import io

LIGHT_CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f0f2f5;color:#1e293b;line-height:1.75}
.top-bar{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(__ACC_RGB__,0.18);padding:12px 20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.home-btn{display:inline-flex;align-items:center;gap:6px;background:rgba(__ACC_RGB__,0.10);color:#__ACC__;border:1px solid rgba(__ACC_RGB__,0.3);border-radius:20px;padding:6px 14px;font-size:13px;cursor:pointer;text-decoration:none;transition:all .2s}
.home-btn:hover{background:#__ACC__;color:#fff}
.breadcrumb{font-size:13px;color:#64748b;display:flex;gap:4px;align-items:center}
.breadcrumb a{color:#64748b;text-decoration:none}
.breadcrumb a:hover{color:#__ACC__}
.crumb-sep{color:#cbd5e1}
.container{max-width:980px;margin:0 auto;padding:24px 16px 48px}
.hero{background:linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);border-radius:14px;padding:32px 28px;margin-bottom:20px;border:1px solid rgba(__ACC_RGB__,0.25);box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.hero-title{font-size:26px;font-weight:800;color:#0f172a;margin-bottom:6px;letter-spacing:.5px}
.hero-sub{font-size:14px;color:#64748b;margin-bottom:18px}
.hero-stats{display:flex;gap:12px;flex-wrap:wrap}
.stat-item{background:rgba(__ACC_RGB__,0.08);border:1px solid rgba(__ACC_RGB__,0.15);border-radius:10px;padding:10px 18px;text-align:center}
.stat-num{font-size:20px;font-weight:800;color:#__ACC__}
.stat-label{font-size:11px;color:#64748b;margin-top:2px;white-space:nowrap}
.explain-banner{display:flex;gap:16px;align-items:flex-start;background:linear-gradient(135deg,#ffffff,#f8fafc);border:1px solid rgba(__ACC_RGB__,0.25);border-radius:12px;padding:18px 20px;margin-bottom:22px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}
.explain-banner .eb-icon{font-size:24px;flex-shrink:0}
.explain-banner .eb-body{flex:1;min-width:0}
.explain-banner .eb-title{font-size:15px;font-weight:700;color:#0f172a;margin-bottom:8px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.explain-banner .eb-tag{font-size:11px;color:#__ACC__;background:rgba(__ACC_RGB__,0.12);padding:2px 9px;border-radius:10px}
.explain-banner .eb-text{font-size:13px;color:#475569;line-height:1.8}
.explain-banner .eb-text b{color:#0f172a;font-weight:600}
.section-title{font-size:18px;font-weight:700;color:#0f172a;margin:28px 0 14px;padding-left:12px;border-left:3px solid #__ACC__}
.layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:8px}
.layer-card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px 14px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.layer-num{font-size:12px;color:#__ACC__;font-weight:700}
.layer-name{font-size:14px;color:#0f172a;font-weight:600;margin:4px 0 4px}
.layer-desc{font-size:12px;color:#64748b;line-height:1.6}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.giant-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;transition:all .2s;text-decoration:none;display:block;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.giant-card:hover{border-color:#__ACC__;background:rgba(__ACC_RGB__,0.05);transform:translateY(-2px);box-shadow:0 4px 14px rgba(__ACC_RGB__,0.12)}
.giant-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.giant-name{font-size:16px;font-weight:700;color:#0f172a}
.region-tag{font-size:11px;padding:2px 9px;border-radius:10px;font-weight:600}
.region-cn{background:rgba(220,38,38,0.12);color:#dc2626;border:1px solid rgba(220,38,38,0.25)}
.region-hk{background:rgba(234,179,8,0.14);color:#b45309;border:1px solid rgba(234,179,8,0.3)}
.giant-desc{font-size:12.5px;color:#64748b;line-height:1.65;margin-bottom:10px}
.giant-foot{font-size:12px;display:flex;align-items:center;justify-content:space-between}
.giant-link{color:#__ACC__;font-weight:600}
.source-note{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px 16px;margin-top:24px;font-size:12.5px;color:#64748b;line-height:1.7;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.source-note b{color:#475569}
@media(max-width:640px){.hero{padding:22px 16px}.hero-title{font-size:21px}.grid{grid-template-columns:1fr}.explain-banner{flex-direction:column;padding:16px}}
.region-tag-mini{font-size:11px;padding:2px 10px;border-radius:10px;font-weight:600;display:inline-block;margin-top:8px}
.overview{background:rgba(__ACC_RGB__,0.05);border:1px solid rgba(__ACC_RGB__,0.14);border-radius:12px;padding:18px 20px;margin-bottom:8px;font-size:14px;color:#334155;line-height:1.85}
.overview b{color:#0f172a;font-weight:600}
.layer-detail{background:#fff;border:1px solid #e2e8f0;border-left:3px solid #__ACC__;border-radius:12px;padding:16px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.layer-detail-title{font-size:15px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:10px;margin-bottom:8px}
.layer-detail-body{font-size:13.5px;color:#475569;line-height:1.8}
.layer-detail-body b{color:#334155}
.info-table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-top:8px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.info-table tr{border-bottom:1px solid #eef2f7}
.info-table tr:last-child{border-bottom:none}
.info-table td{padding:12px 16px;font-size:13.5px;color:#334155}
.info-table td:first-child{width:160px;color:#64748b;background:#f8fafc}
.insight-box{background:linear-gradient(135deg,#f8fafc,#ffffff);border:1px solid rgba(__ACC_RGB__,0.2);border-radius:12px;padding:18px 20px;margin-top:16px}
.insight-title{font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.insight-title .icon{color:#__ACC__}
.insight-body{font-size:13.5px;color:#475569;line-height:1.8}
.back-bar{margin-top:20px}
.back-btn{display:inline-flex;align-items:center;gap:6px;background:rgba(__ACC_RGB__,0.08);color:#__ACC__;border:1px solid rgba(__ACC_RGB__,0.25);border-radius:20px;padding:8px 16px;font-size:13px;text-decoration:none;transition:all .2s}
.back-btn:hover{background:rgba(__ACC_RGB__,0.16)}
.data-banner{background:rgba(__ACC_RGB__,0.07);border:1px solid rgba(__ACC_RGB__,0.22);border-left:4px solid #__ACC__;border-radius:10px;padding:12px 16px;margin-bottom:20px;font-size:12.5px;color:#334155;line-height:1.7}
.data-banner b{color:#0f172a;font-weight:600}
.data-banner .upd{color:#__ACC__;font-weight:600}
.cycle-block{background:linear-gradient(135deg,#f8fafc,#ffffff);border:1px solid rgba(__ACC_RGB__,0.22);border-radius:12px;padding:18px 20px;margin-bottom:8px}
.cycle-title{font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.cycle-title .icon{color:#__ACC__}
.cycle-body{font-size:13.5px;color:#475569;line-height:1.85}
.cycle-body b{color:#0f172a;font-weight:600}
.cycle-body p{margin-bottom:8px}
.cycle-body ul{margin:8px 0 0 18px;padding:0}
.cycle-body li{margin-bottom:6px}
.cycle-current{margin-top:12px;font-size:12.5px;color:#64748b;border-left:3px solid #__ACC__;padding:8px 12px;background:rgba(__ACC_RGB__,0.06);line-height:1.7}
.cycle-current b{color:#334155}
.cycle-current a{text-decoration:none}
.fin-block{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,0.04)}
.fin-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.fin-title{font-size:15px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:8px}
.fin-title .icon{color:#__ACC__}
.fin-tag{font-size:11px;color:#b45309;background:rgba(251,191,36,0.14);border:1px solid rgba(251,191,36,0.35);padding:2px 9px;border-radius:10px}
.fin-table{width:100%;border-collapse:collapse;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden}
.fin-table tr{border-bottom:1px solid #eef2f7}
.fin-table tr:last-child{border-bottom:none}
.fin-table td{padding:10px 14px;font-size:13px;color:#334155}
.fin-table td:first-child{width:130px;color:#64748b}
.fin-table .val{color:#b45309;font-weight:600}
.fin-note{font-size:12px;color:#64748b;margin-top:8px;line-height:1.6}
'''

FILES = [
    r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\deploy_site\_build_five_chains.py",
    r"C:\Users\Administrator\WorkBuddy\2026-07-08-13-16-44\deploy_site\_build_three_chains.py",
]

for fn in FILES:
    s = open(fn, encoding="utf-8").read()
    marker = 'CSS = """'
    start = s.index(marker) + len(marker)
    end = s.index('"""', start)
    s2 = s[:start] + LIGHT_CSS + s[end:]
    # 校验：确认旧深色特征已消失、浅色特征已出现
    assert "#0a0e1a" not in s2, "深色背景残留: " + fn
    assert "#f0f2f5" in s2, "浅色背景未写入: " + fn
    open(fn, "w", encoding="utf-8").write(s2)
    print("OK 改写浅色:", fn)
print("DONE")
