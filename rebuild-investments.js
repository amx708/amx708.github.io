const fs = require('fs');
const html = fs.readFileSync('berkshire-investments.html', 'utf8');
const rowMatches = html.match(/<tr[^>]*>.*?<\/tr>/gs);
const data = [];
for (let i = 1; i < rowMatches.length; i++) {
  const cells = rowMatches[i].match(/<td[^>]*>(.*?)<\/td>/gs);
  if (!cells) continue;
  const clean = cells.map(c => c.replace(/<.*?>/g, '').replace(/\s+/g, ' ').replace(/&amp;/g, '&').trim());
  data.push({
    cusip: clean[1],
    name: clean[2],
    cnName: clean[3],
    type: clean[4],
    industry: clean[5],
    buy: clean[6],
    sell: clean[7],
    hold: clean[8],
    acquired: clean[9],
    current: clean[10],
    subsidiary: clean[11]
  });
}

const pageHtml = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>历年投资数据 — 伯克希尔·哈撒韦 | 漫漫扬</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei","Helvetica Neue",sans-serif;
  background:#f1f5f9;color:#1e293b;line-height:1.6;min-height:100vh;
}

/* Breadcrumb */
.breadcrumb{
  max-width:1100px;margin:0 auto;padding:20px 24px 0;font-size:13px;color:#64748b;
}
.breadcrumb a{color:#64748b;text-decoration:none;transition:color 0.15s}
.breadcrumb a:hover{color:#2563eb}
.breadcrumb span{color:#94a3b8;margin:0 6px}
.breadcrumb .current{color:#334155;font-weight:500}

/* Hero */
.hero{
  position:relative;background:linear-gradient(135deg,#0f172a 0%,#1e293b 40%,#1e3a5f 100%);
  padding:48px 24px 64px;text-align:center;overflow:hidden;
}
.hero::before{
  content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
  background:radial-gradient(ellipse at 30% 20%, rgba(245,158,11,0.08) 0%, transparent 50%),
              radial-gradient(ellipse at 70% 80%, rgba(37,99,235,0.06) 0%, transparent 50%);
  pointer-events:none;
}
.hero::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:100px;
  background:linear-gradient(to top, #f1f5f9 0%, transparent 100%);pointer-events:none;
}
.hero-content{position:relative;z-index:2;max-width:700px;margin:0 auto}
.hero-badge{
  display:inline-block;padding:4px 14px;background:rgba(245,158,11,0.15);
  border:1px solid rgba(245,158,11,0.3);border-radius:20px;color:#fbbf24;
  font-size:12px;font-weight:500;letter-spacing:0.5px;margin-bottom:20px;
}
.hero h1{font-size:clamp(26px,4vw,40px);font-weight:800;color:#fff;line-height:1.25;letter-spacing:-0.5px;margin-bottom:12px}
.hero h1 span{color:#f59e0b}
.hero p{font-size:15px;color:#94a3b8;max-width:560px;margin:0 auto;line-height:1.7}

/* Main */
.main{max-width:1100px;margin:0 auto;padding:32px 24px 80px}

/* Stats */
.stats-bar{
  display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px;
}
.stat-card{
  background:#fff;border-radius:12px;padding:20px 16px;text-align:center;
  box-shadow:0 1px 3px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04);border:1px solid #e2e8f0;
  transition:transform 0.2s ease,box-shadow 0.2s ease;
}
.stat-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.08)}
.stat-number{font-size:28px;font-weight:800;background:linear-gradient(135deg,#f59e0b,#d97706);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1}
.stat-label{font-size:13px;color:#64748b;margin-top:6px;font-weight:500}

/* Table */
.table-wrap{
  background:#fff;border-radius:14px;border:1px solid #e2e8f0;
  box-shadow:0 1px 3px rgba(0,0,0,0.04);overflow:hidden;
}
.table-header{
  padding:20px 24px;border-bottom:1px solid #e2e8f0;
  display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;
}
.table-header h2{font-size:18px;font-weight:700;color:#0f172a}
.table-header .count{font-size:13px;color:#64748b;background:#f1f5f9;padding:4px 12px;border-radius:20px}
.table-scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:13px}
thead th{
  background:#f8fafc;padding:14px 16px;text-align:left;font-weight:600;color:#475569;
  border-bottom:1px solid #e2e8f0;white-space:nowrap;font-size:12px;text-transform:uppercase;letter-spacing:0.3px;
}
tbody td{padding:14px 16px;border-bottom:1px solid #f1f5f0;color:#334155;vertical-align:top}
tbody tr:hover{background:#f8fafc}
tbody tr:last-child td{border-bottom:none}

.company-name{font-weight:600;color:#0f172a;font-size:13.5px}
.company-cn{font-size:12px;color:#64748b;margin-top:2px}

/* Tags */
.tag{
  display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:500;
}
.tag-industry{background:#eff6ff;color:#2563eb}
.tag-type{background:#f0fdfa;color:#0d9488}
.tag-acquired{background:#fffbeb;color:#b45309}
.tag-current{background:#ecfdf5;color:#059669}
.tag-sold{background:#f1f5f9;color:#64748b}
.tag-subsidiary{background:#fef2f2;color:#dc2626}

.year{font-family:ui-monospace,monospace;font-size:12.5px;color:#475569;font-weight:500}

/* Back link */
.back-link{margin-top:40px;text-align:center}
.back-link a{
  display:inline-flex;align-items:center;gap:8px;padding:10px 24px;
  background:#fff;border:1px solid #e2e8f0;border-radius:8px;color:#334155;
  font-size:14px;font-weight:500;text-decoration:none;transition:all 0.2s ease;
  box-shadow:0 1px 2px rgba(0,0,0,0.04);
}
.back-link a:hover{background:#f8fafc;border-color:#cbd5e1;color:#2563eb;box-shadow:0 4px 12px rgba(0,0,0,0.06)}

/* Footer */
.footer{text-align:center;padding:32px 24px;color:#94a3b8;font-size:12px;border-top:1px solid #e2e8f0}
.footer a{color:#64748b;text-decoration:none;transition:color 0.15s}
.footer a:hover{color:#2563eb}

/* Responsive */
@media(max-width:900px){.stats-bar{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){
  .hero{padding:36px 20px 48px}
  .hero h1{font-size:24px}
  .stats-bar{grid-template-columns:1fr 1fr}
  .table-header{padding:16px}
  thead th{padding:10px 12px;font-size:11px}
  tbody td{padding:10px 12px}
  .main{padding:24px 16px 60px}
  .breadcrumb{padding:16px 16px 0}
}
</style>
</head>
<body>

<nav class="breadcrumb">
  <a href="berkshire-standalone.html">投资数据中心</a>
  <span>/</span>
  <span class="current">历年投资数据</span>
</nav>

<header class="hero">
  <div class="hero-content">
    <div class="hero-badge">Portfolio Holdings</div>
    <h1>伯克希尔·哈撒韦<br><span>历年投资数据</span></h1>
    <p>持仓明细、行业分布、买卖记录 —— 1966 年至今 BRK 投资组合全景</p>
  </div>
</header>

<main class="main">
  <div class="stats-bar">
    <div class="stat-card"><div class="stat-number">${data.length}</div><div class="stat-label">投资记录</div></div>
    <div class="stat-card"><div class="stat-number">${data.filter(d=>d.current==='是').length}</div><div class="stat-label">当前持有</div></div>
    <div class="stat-card"><div class="stat-number">${data.filter(d=>d.acquired==='是').length}</div><div class="stat-label">被收购</div></div>
    <div class="stat-card"><div class="stat-number">${new Set(data.map(d=>d.industry)).size}</div><div class="stat-label">行业分布</div></div>
  </div>

  <div class="table-wrap">
    <div class="table-header">
      <h2>投资明细</h2>
      <span class="count">共 ${data.length} 条记录</span>
    </div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>公司名称</th>
            <th>类型</th>
            <th>行业</th>
            <th>首次买入</th>
            <th>最后卖出</th>
            <th>持有年数</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
${data.map(d=>{
  const statusTags = [];
  if (d.current === '是') statusTags.push('<span class="tag tag-current">持有中</span>');
  if (d.acquired === '是') statusTags.push('<span class="tag tag-acquired">被收购</span>');
  if (d.subsidiary === '是') statusTags.push('<span class="tag tag-subsidiary">全资子公司</span>');
  if (statusTags.length === 0) statusTags.push('<span class="tag tag-sold">已卖出</span>');
  const name = d.name.replace(/&amp;/g, '&');
  return `          <tr>
            <td>
              <div class="company-name">${name}</div>
              ${d.cnName ? '<div class="company-cn">' + d.cnName + '</div>' : ''}
            </td>
            <td><span class="tag tag-type">${d.type}</span></td>
            <td><span class="tag tag-industry">${d.industry}</span></td>
            <td><span class="year">${d.buy}</span></td>
            <td><span class="year">${d.sell}</span></td>
            <td><span class="year">${d.hold}</span></td>
            <td>${statusTags.join(' ')}</td>
          </tr>`;
}).join('\n')}
        </tbody>
      </table>
    </div>
  </div>

  <div class="back-link">
    <a href="berkshire-standalone.html">← 返回投资数据中心</a>
  </div>
</main>

<footer class="footer">
  <p>数据来源：伯克希尔·哈撒韦官方年报 & 公开财经数据 | <a href="https://amx708.github.io/">漫漫扬</a></p>
</footer>

</body>
</html>`;

fs.writeFileSync('berkshire-investments.html', pageHtml, 'utf8');
console.log('Done. Written', pageHtml.length, 'bytes');
