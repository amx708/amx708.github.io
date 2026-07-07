const fs = require('fs');

// Shared template styles
const sharedStyles = `<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei','Helvetica Neue',sans-serif;background:#f1f5f9;color:#1e293b;line-height:1.6;min-height:100vh}

.breadcrumb{max-width:1100px;margin:0 auto;padding:20px 24px 0;font-size:13px;color:#64748b}
.breadcrumb a{color:#64748b;text-decoration:none;transition:color .15s}
.breadcrumb a:hover{color:#2563eb}
.breadcrumb span{color:#94a3b8;margin:0 6px}
.breadcrumb .current{color:#334155;font-weight:500}

.hero{position:relative;background:linear-gradient(135deg,#0f172a 0%,#1e293b 40%,#1e3a5f 100%);padding:48px 24px 64px;text-align:center;overflow:hidden}
.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at 30% 20%, rgba(245,158,11,.08) 0%, transparent 50%),radial-gradient(ellipse at 70% 80%, rgba(37,99,235,.06) 0%, transparent 50%);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:100px;background:linear-gradient(to top, #f1f5f9 0%, transparent 100%);pointer-events:none}
.hero-content{position:relative;z-index:2;max-width:700px;margin:0 auto}
.hero-badge{display:inline-block;padding:4px 14px;background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.3);border-radius:20px;color:#fbbf24;font-size:12px;font-weight:500;letter-spacing:.5px;margin-bottom:20px}
.hero h1{font-size:clamp(26px,4vw,40px);font-weight:800;color:#fff;line-height:1.25;letter-spacing:-.5px;margin-bottom:12px}
.hero h1 span{color:#f59e0b}
.hero p{font-size:15px;color:#94a3b8;max-width:560px;margin:0 auto;line-height:1.7}

.main{max-width:1100px;margin:0 auto;padding:32px 24px 80px}

.year-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:10px}
.year-pill{display:flex;align-items:center;justify-content:center;padding:10px 14px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;color:#334155;font-size:14px;font-weight:500;text-decoration:none;transition:all .2s ease;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.year-pill:hover{background:#eff6ff;border-color:#bfdbfe;color:#2563eb;transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.year-pill.accent{background:linear-gradient(135deg,#fef3c7,#fffbeb);border-color:#fde68a;color:#92400e}
.year-pill.accent:hover{background:linear-gradient(135deg,#fde68a,#fef3c7)}

.content-card{background:#fff;border-radius:14px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.04);padding:32px 28px}
.content-card h2{font-size:18px;font-weight:700;color:#0f172a;margin-bottom:16px}
.content-card p{color:#475569;font-size:14.5px;line-height:1.8}
.content-card .meta{margin-top:20px;padding-top:20px;border-top:1px solid #f1f5f0;font-size:13px;color:#94a3b8}

.empty-state{text-align:center;padding:60px 20px}
.empty-state .icon{font-size:48px;margin-bottom:16px;display:block}
.empty-state h3{font-size:18px;color:#334155;margin-bottom:8px}
.empty-state p{font-size:14px;color:#94a3b8}

.back-link{margin-top:40px;text-align:center}
.back-link a{display:inline-flex;align-items:center;gap:8px;padding:10px 24px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;color:#334155;font-size:14px;font-weight:500;text-decoration:none;transition:all .2s ease;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.back-link a:hover{background:#f8fafc;border-color:#cbd5e1;color:#2563eb;box-shadow:0 4px 12px rgba(0,0,0,.06)}

.footer{text-align:center;padding:32px 24px;color:#94a3b8;font-size:12px;border-top:1px solid #e2e8f0}
.footer a{color:#64748b;text-decoration:none;transition:color .15s}
.footer a:hover{color:#2563eb}

@media(max-width:600px){
  .hero{padding:36px 20px 48px}
  .hero h1{font-size:24px}
  .year-grid{grid-template-columns:repeat(auto-fill,minmax(80px,1fr))}
  .main{padding:24px 16px 60px}
  .breadcrumb{padding:16px 16px 0}
}
</style>`;

function generatePage(options) {
  const { title, subtitle, badge, breadcrumb, yearList, empty, content } = options;
  let yearSection = '';
  if (yearList) {
    yearSection = `
  <div class="content-card" style="margin-bottom:24px">
    <h2>📅 年份列表</h2>
    <div class="year-grid" style="margin-top:16px">
${yearList.map(y => `      <span class="year-pill${y.highlight ? ' accent' : ''}">${y.year}${y.label ? ' <small style="font-size:11px;color:#94a3b8">'+y.label+'</small>' : ''}</span>`).join('\n')}
    </div>
  </div>`;
  }
  
  let contentSection = '';
  if (content) {
    contentSection = `
  <div class="content-card" style="margin-bottom:24px">
    <h2>${content.title}</h2>
    <p>${content.text}</p>
    ${content.meta ? `<div class="meta">${content.meta}</div>` : ''}
  </div>`;
  }
  
  let emptySection = '';
  if (empty) {
    contentSection = `
  <div class="content-card">
    <div class="empty-state">
      <span class="icon">🚧</span>
      <h3>${empty.title}</h3>
      <p>${empty.desc}</p>
    </div>
  </div>`;
  }

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title}</title>
${sharedStyles}
</head>
<body>

<nav class="breadcrumb">
  <a href="berkshire-standalone.html">投资数据中心</a>
  <span>/</span>
  <span class="current">${breadcrumb}</span>
</nav>

<header class="hero">
  <div class="hero-content">
    <div class="hero-badge">${badge}</div>
    <h1>伯克希尔·哈撒韦<br><span>${subtitle}</span></h1>
    <p>${options.desc}</p>
  </div>
</header>

<main class="main">
${yearSection}${contentSection}

  <div class="back-link">
    <a href="berkshire-standalone.html">← 返回投资数据中心</a>
  </div>
</main>

<footer class="footer">
  <p>数据来源：伯克希尔·哈撒韦官方年报 & 公开财经数据 | <a href="https://amx708.github.io/">漫漫扬</a></p>
</footer>

</body>
</html>`;
}

// 1. Abel Letters - only 2025
const abelYears = [{year:'2025', highlight:true, label:'最新'}];
fs.writeFileSync('berkshire-abel-letters.html', generatePage({
  title: '阿贝尔致股东的信 — 伯克希尔·哈撒韦 | 漫漫扬',
  subtitle: '阿贝尔致股东的信',
  badge: 'Abel Letters',
  breadcrumb: '阿贝尔致股东的信',
  desc: '格雷格·阿贝尔接任副董事长后致股东的信件合集',
  yearList: abelYears,
  content: {
    title: 'ℹ️ 说明',
    text: '格雷格·阿贝尔于 2024 年起在巴菲特致股东的信中以副董事长身份署名。2025 年起独立发布致股东的信。',
    meta: '由于信件内容涉及版权，本站仅提供索引导航，原文请前往伯克希尔·哈撒韦官方网站查阅。'
  }
}), 'utf8');

// 2. Partnership Letters - 1957-1970
const partnerYears = [];
for (let y = 1957; y <= 1970; y++) {
  partnerYears.push({year: y.toString(), highlight: false});
}
fs.writeFileSync('berkshire-partnership-letters.html', generatePage({
  title: '巴菲特合伙信 — 伯克希尔·哈撒韦 | 漫漫扬',
  subtitle: '巴菲特合伙信',
  badge: 'Partnership Letters',
  breadcrumb: '巴菲特合伙信',
  desc: '1957-1970 年巴菲特合伙公司时期致合伙人的信件',
  yearList: partnerYears,
  content: {
    title: 'ℹ️ 说明',
    text: '巴菲特合伙公司（Buffett Partnership Ltd.）存续于 1957-1970 年。这 14 年间巴菲特写给合伙人的信件，详细记录了他的投资理念与策略演进。',
    meta: '信件原文请前往 yeeyoung.com 或其他授权来源查阅。'
  }
}), 'utf8');

// 3. Shareholder Letters - 1977-2024
const letterYears = [];
for (let y = 1977; y <= 2024; y++) {
  letterYears.push({year: y.toString(), highlight: y >= 2020});
}
// Also add 1965-1976
for (let y = 1965; y <= 1976; y++) {
  letterYears.unshift({year: y.toString(), highlight: false});
}
fs.writeFileSync('berkshire-letters.html', generatePage({
  title: '巴菲特致股东的信 — 伯克希尔·哈撒韦 | 漫漫扬',
  subtitle: '巴菲特致股东的信',
  badge: 'Shareholder Letters',
  breadcrumb: '巴菲特致股东的信',
  desc: '1965-2024 年巴菲特致伯克希尔·哈撒韦股东的信件全集',
  yearList: letterYears,
  content: {
    title: 'ℹ️ 说明',
    text: '从 1965 年接管伯克希尔至今，巴菲特每年致股东的信累计 60 封。这些信件被誉为价值投资的"圣经"，记录了从纺织厂到万亿市值帝国的传奇历程。',
    meta: '中文版请前往 buffett-partnership-showcase.html 阅读。'
  }
}), 'utf8');

// 4. Meetings - empty
fs.writeFileSync('berkshire-meetings.html', generatePage({
  title: '股东大会 — 伯克希尔·哈撒韦 | 漫漫扬',
  subtitle: '股东大会',
  badge: 'Annual Meetings',
  breadcrumb: '股东大会',
  desc: '伯克希尔历年股东大会问答实录',
  empty: {
    title: '内容正在建设中',
    desc: '股东大会问答实录正在整理中，敬请期待。'
  }
}), 'utf8');

// 5. Speeches - empty
fs.writeFileSync('berkshire-speeches.html', generatePage({
  title: '巴菲特演讲 — 伯克希尔·哈撒韦 | 漫漫扬',
  subtitle: '巴菲特演讲',
  badge: 'Speeches',
  breadcrumb: '巴菲特演讲',
  desc: '巴菲特历年在各大学、会议上的经典演讲',
  empty: {
    title: '内容正在建设中',
    desc: '演讲合集正在整理中，敬请期待。'
  }
}), 'utf8');

// 6. Munger Speeches - empty
fs.writeFileSync('berkshire-munger-speeches.html', generatePage({
  title: '芒格演讲 — 伯克希尔·哈撒韦 | 漫漫扬',
  subtitle: '芒格演讲',
  badge: 'Munger Speeches',
  breadcrumb: '芒格演讲',
  desc: '查理·芒格历年在各大学、会议上的经典演讲',
  empty: {
    title: '内容正在建设中',
    desc: '芒格演讲合集正在整理中，敬请期待。'
  }
}), 'utf8');

console.log('All 6 pages rewritten successfully');
