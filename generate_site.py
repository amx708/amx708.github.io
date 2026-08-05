# -*- coding: utf-8 -*-
"""
generate_site.py —— 读取 data.json，生成 smallcap/index.html（自包含交互看板）
依赖：data.json（由 strategy_signal.py 生成）
输出：<本目录>/smallcap/index.html
"""
import os, json

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(OUT_DIR, "data.json")
SITE_DIR = os.path.join(OUT_DIR, "smallcap")
INDEX_PATH = os.path.join(SITE_DIR, "index.html")

METRICS = {
    "策略收益": "511.28%", "年化收益": "32.83%", "超额收益": "329.68%",
    "基准收益": "42.26%", "夏普比率": "1.185", "最大回撤": "27.68%",
    "胜率": "62.6%", "盈亏比": "1.533",
}
PARAMS = [
    ("持仓数量", "8 只"), ("基础池", "中证1000 (000852)"),
    ("调仓频率", "每周二收盘后重算"), ("空仓月份", "1 月、4 月（回测逻辑）"),
    ("小市值候选池", "市值最小的 200 只里取 8"), ("股价上限", "¥100"),
    ("财务过滤", "营收>1亿 & 净利>0 & 净资产>0"), ("个股止损", "-9%（回测逻辑）"),
    ("大盘清仓", "沪深300 跌破 MA20（回测逻辑）"),
    ("拥挤度代理", "中证2000 近 20 日涨幅>25% 则半仓（回测逻辑）"),
]


def load():
    if not os.path.exists(DATA_PATH):
        raise SystemExit("找不到 data.json，请先跑 strategy_signal.py")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build(d):
    cur = d.get("current", {})
    curve = d.get("curve", {"dates": [], "values": []})
    hist = d.get("history", [])
    updated = d.get("updated", "—")
    holdings = cur.get("holdings", [])
    trail = cur.get("trailing_1y_return")

    avg_mcap = round(sum(h["mcap_yi"] for h in holdings) / len(holdings), 2) if holdings else None
    kpis = [
        ("更新日期", updated, "slate"),
        ("当前持仓", "%d 只" % len(holdings), "blue"),
        ("平均市值", ("%.1f 亿" % avg_mcap) if avg_mcap else "—", "blue"),
        ("信号近一年收益", ("+%.2f%%" % trail) if trail is not None else "—",
         "emerald" if (trail or 0) >= 0 else "red"),
    ]

    data_js = json.dumps({
        "curve": curve, "current": cur, "history": hist[-12:],
        "params": PARAMS, "metrics": METRICS,
    }, ensure_ascii=False)

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>国九小市值策略 · 信号看板</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{font-family:'Inter','PingFang SC','Microsoft YaHei',sans-serif;}</style>
</head>
<body class="bg-slate-50 text-slate-800">
<div class="max-w-6xl mx-auto px-4 py-10">
  <header class="mb-8">
    <h1 class="text-3xl font-bold text-slate-900">国九小市值 + 拥挤度减仓策略</h1>
    <p class="text-slate-500 mt-2">自动信号看板 · 数据源 akshare（免费）· GitHub Action 每周二收盘后自动更新</p>
  </header>

  <div id="kpi" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>

  <div class="grid md:grid-cols-3 gap-6 mb-8">
    <div class="md:col-span-2 bg-white rounded-xl shadow p-6">
      <h2 class="text-lg font-semibold mb-4">当前信号组合 · 近一年等权表现</h2>
      <canvas id="curveChart" height="300"></canvas>
      <p class="text-xs text-slate-400 mt-2">说明：按当周选出的 8 只等权持有、近一年回测式表现，仅用于观察信号质量，非实盘收益。</p>
    </div>
    <div class="bg-white rounded-xl shadow p-6">
      <h2 class="text-lg font-semibold mb-4">当前持仓</h2>
      <div class="overflow-auto max-h-96">
        <table class="w-full text-sm text-left">
          <thead class="text-slate-500 border-b"><tr>
            <th class="py-2 pr-3">代码</th><th class="py-2 pr-3">名称</th>
            <th class="py-2 pr-3">现价</th><th class="py-2 pr-3">市值(亿)</th>
            <th class="py-2 pr-3">营收(亿)</th><th class="py-2 pr-3">净利(亿)</th>
          </tr></thead>
          <tbody id="holdBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="bg-white rounded-xl shadow p-6 mb-8">
    <h2 class="text-lg font-semibold mb-4">近 12 周持仓轮换</h2>
    <div class="overflow-auto max-h-80">
      <table class="w-full text-sm text-left">
        <thead class="text-slate-500 border-b"><tr>
          <th class="py-2 pr-3">日期</th><th class="py-2 pr-3">持仓代码</th><th class="py-2 pr-3">近一年收益</th>
        </tr></thead>
        <tbody id="histBody"></tbody>
      </table>
    </div>
  </div>

  <div class="bg-white rounded-xl shadow p-6 mb-8">
    <h2 class="text-lg font-semibold mb-4">策略参数</h2>
    <div id="params" class="grid md:grid-cols-3 gap-y-2 gap-x-6 text-sm"></div>
  </div>

  <div class="bg-white rounded-xl shadow p-6 mb-8">
    <h2 class="text-lg font-semibold mb-4">回测参考指标（v7）</h2>
    <div id="metrics" class="grid md:grid-cols-4 gap-y-2 gap-x-6 text-sm"></div>
  </div>

  <div class="bg-amber-50 border border-amber-200 rounded-xl p-6 mb-8">
    <h2 class="text-lg font-semibold text-amber-800 mb-2">风险提示</h2>
    <ul class="list-disc list-inside text-sm text-amber-900 space-y-1">
      <li>本页为策略<b>信号跟踪</b>，由 akshare 公开数据每周重算，不等于实盘收益，亦不构成投资建议。</li>
      <li>小市值策略对流动性、滑点、市场风格切换高度敏感，实盘表现可能显著弱于回测/信号曲线。</li>
      <li>akshare 数据为第三方公开接口，存在延迟或口径差异，信号仅供参考。</li>
      <li>策略尚未经过模拟盘或实盘验证，仅作为研究记录使用。</li>
    </ul>
  </div>

  <footer class="text-center text-xs text-slate-400">
    <p>生成时间：__UPDATED__ · 数据源：<span id="srcTag">akshare（免费公开接口）</span></p>
    <p class="mt-1">以上为数据整理，不构成投资建议，决策请自行判断。</p>
  </footer>
</div>

<script>
const D = __DATA__;
const colorMap={red:'text-red-600 border-red-500',blue:'text-blue-600 border-blue-500',emerald:'text-emerald-600 border-emerald-500',slate:'text-slate-600 border-slate-400'};
document.getElementById('kpi').innerHTML = [
  ['更新日期',D.current?D.current.date:'—','slate'],
  ['当前持仓',(D.current?D.current.holdings.length:0)+' 只','blue'],
  ['平均市值',(D.current&&D.current.holdings.length)?(D.current.holdings.reduce((s,h)=>s+h.mcap_yi,0)/D.current.holdings.length).toFixed(1)+' 亿':'—','blue'],
  ['信号近一年收益',(D.current&&D.current.trailing_1y_return!=null)?((D.current.trailing_1y_return>=0?'+':'')+D.current.trailing_1y_return.toFixed(2)+'%'):'—',(D.current&&D.current.trailing_1y_return>=0)?'emerald':'red']
].map(([k,v,c])=>`<div class="bg-white rounded-xl shadow p-5 border-l-4 ${colorMap[c]}"><p class="text-xs text-slate-400 uppercase tracking-wide">${k}</p><p class="text-2xl font-bold ${colorMap[c].split(' ')[0]}">${v}</p></div>`).join('');
(function(){
  var s = D.current ? D.current.source : null, el = document.getElementById('srcTag');
  if(!el) return;
  if(s === 'sina_cached'){
    el.innerHTML = '新浪行情 + 股本缓存（<span class="text-amber-600 font-semibold">备用源，市值为近似值</span>）';
  } else if(s === 'eastmoney'){
    el.textContent = '东方财富实时快照（akshare）';
  }
})();
document.getElementById('holdBody').innerHTML = (D.current?D.current.holdings:[]).map(h=>
  `<tr class="border-b"><td class="py-2 pr-3">${h.code}</td><td class="py-2 pr-3">${h.name}</td><td class="py-2 pr-3">${h.price.toFixed(2)}</td><td class="py-2 pr-3">${h.mcap_yi.toFixed(1)}</td><td class="py-2 pr-3">${h.rev_yi.toFixed(1)}</td><td class="py-2 pr-3">${h.np_yi.toFixed(1)}</td></tr>`).join('');
document.getElementById('histBody').innerHTML = (D.history||[]).slice().reverse().map(s=>
  `<tr class="border-b"><td class="py-2 pr-3">${s.date}</td><td class="py-2 pr-3">${(s.holdings||[]).map(h=>h.code).join(', ')}</td><td class="py-2 pr-3 ${s.trailing_1y_return>=0?'text-emerald-600':'text-red-600'}">${s.trailing_1y_return!=null?(s.trailing_1y_return>=0?'+':'')+s.trailing_1y_return.toFixed(2)+'%':'—'}</td></tr>`).join('');
document.getElementById('params').innerHTML = D.params.map(([k,v])=>`<div class="flex justify-between border-b py-2"><span class="text-slate-500">${k}</span><span class="font-medium">${v}</span></div>`).join('');
document.getElementById('metrics').innerHTML = Object.entries(D.metrics).map(([k,v])=>`<div class="flex justify-between border-b py-2"><span class="text-slate-500">${k}</span><span class="font-medium">${v}</span></div>`).join('');
if(D.curve&&D.curve.dates&&D.curve.dates.length){
  new Chart(document.getElementById('curveChart'),{type:'line',data:{labels:D.curve.dates,datasets:[{label:'信号组合(基期100)',data:D.curve.values,borderColor:'#2563eb',backgroundColor:'rgba(37,99,235,0.08)',fill:true,pointRadius:0,borderWidth:2}]},options:{plugins:{legend:{display:false}},scales:{x:{ticks:{maxTicksLimit:12}},y:{ticks:{callback:v=>v.toFixed(0)}}}}});
}
</script>
</body>
</html>"""
    html = html.replace("__DATA__", data_js).replace("__UPDATED__", updated)
    os.makedirs(SITE_DIR, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK ->", INDEX_PATH)


if __name__ == "__main__":
    build(load())
