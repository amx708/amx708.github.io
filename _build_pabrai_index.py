"""
从索引JSON中提取真实演讲日期（而非采集日期），
重新按演讲时间分组，生成帕伯莱专题索引页HTML。
"""

import json, os, re

DEPLOY_DIR = os.path.join(os.path.dirname(__file__), 'deploy_site')
INDEX_FILE = os.path.join(DEPLOY_DIR, '_pabrai_index.json')

# ============ 从标题提取真实演讲日期 ============
def extract_real_date(title):
    """从标题提取真实的演讲/访谈日期"""
    # 匹配各种日期格式
    patterns = [
        # "2024年3月访谈" → 2024-03
        r'(\d{4})年(\d{1,2})月',
        # "2013年7月13日" → 2013-07-13
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        # "2024年5月演讲问答" → 2024-05
        r'于(\d{4})年(\d{1,2})月(\d{1,2})日',
        # "2025年1月" → 2025-01
        r'(\d{4})年(\d{1,2})月',
        # "于2021年3月18日" → 2021-03-18
        r'于\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
    ]
    
    for p in patterns:
        m = re.search(p, title)
        if m:
            year = m.group(1)
            month = m.group(2).zfill(2)
            if len(m.groups()) >= 3 and m.group(3):
                day = m.group(3).zfill(2)
                return f"{year}-{month}-{day}"
            return f"{year}-{month}"
    
    # "2024年3月" without day
    m = re.search(r'(\d{4})年(\d{1,2})月', title)
    if m:
        return f"{m.group(1)}-{m.group(2).zfill(2)}"
    
    return None

# ============ 从标题提取地点/场合 ============
def extract_venue(title):
    """从标题提取演讲地点或场合"""
    venues = []
    # 大学
    uni_patterns = [
        ('北京大学', '北京大学'),
        ('北大', '北京大学'),
        ('波士顿学院', '波士顿学院'),
        ('波士顿大学', '波士顿大学'),
        ('剑桥大学', '剑桥大学'),
        ('哥伦比亚商学院', '哥伦比亚商学院'),
        ('哥伦比亚大学', '哥伦比亚大学'),
        ('加州大学尔湾分校', '加州大学尔湾分校'),
        ('加州大学（尔湾分校）', '加州大学尔湾分校'),
        ('加州大学洛杉矶分校', '加州大学洛杉矶分校'),
        ('乔治城大学', '乔治城大学'),
        ('克莱姆森大学', '克莱姆森大学'),
        ('巴布森学院', '巴布森学院'),
        ('印第安纳大学', '印第安纳大学'),
        ('伦敦商学院', '伦敦商学院'),
        ('南加州创业者协会', '南加州创业者协会'),
        ('MDI古尔冈', 'MDI古尔冈'),
        ('印度古尔冈管理发展研究所', '印度古尔冈'),
        ('印度商学院', '印度商学院'),
        ('波多黎各大学', '波多黎各大学'),
        ('内布拉斯加大学', '内布拉斯加大学奥马哈'),
        ('哈佛大学', '哈佛大学'),
        ('西班牙马德里', '马德里Value School'),
        ('都柏林圣三一学院', '都柏林圣三一学院'),
        ('Morningstar印度', 'Morningstar印度'),
        ('Pan IIT', 'Pan IIT加拿大'),
        ('SXSW', 'SXSW'),
        ('诺亚财富', '诺亚财富学院'),
        ('SumZero', 'SumZero'),
        ('CEO日记', 'CEO日记'),
        ('投资者播客', '投资者播客'),
        ('欧洲价值投资大会', '欧洲价值投资大会'),
        ('伦敦商学院', '伦敦商学院'),
        ('加尔各答价值投资者俱乐部', '加尔各答价值投资者'),
    ]
    for pattern, label in uni_patterns:
        if pattern in title:
            venues.append(label)
    
    if venues:
        return venues[0]
    
    # 特殊场合
    if '炉边' in title or '炉边对话' in title:
        return '炉边对话'
    if '访谈' in title:
        return '媒体访谈'
    if '专访' in title:
        return '专访'
    if '最新演讲' in title:
        return '公开演讲'
    
    return '公开演讲'

# ============ 主流程 ============
def main():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    
    # 为每条记录提取真实日期和场合
    for e in entries:
        real_date = extract_real_date(e['title'])
        venue = extract_venue(e['title'])
        e['real_date'] = real_date or e['date'][:7]
        e['venue'] = venue
        e['star'] = e.get('star', False)
        # No public account source
        e['pub_source'] = ''
    
    # 按真实日期排序
    entries.sort(key=lambda e: e['real_date'], reverse=True)
    
    # 按年份分组
    groups = {}
    for e in entries:
        yr = e['real_date'][:4]
        if yr not in groups:
            groups[yr] = []
        groups[yr].append(e)
    
    # 统计
    total = len(entries)
    speeches = sum(1 for e in entries if e['cat_type'] == '演讲')
    interviews = sum(1 for e in entries if e['cat_type'] == '访谈')
    qas = sum(1 for e in entries if e['cat_type'] == '问答')
    articles = sum(1 for e in entries if e['cat_type'] == '文章')
    
    # 生成索引页HTML
    html = generate_index_html(entries, groups, total, speeches, interviews, qas, articles)
    
    output_path = os.path.join(DEPLOY_DIR, 'berkshire-pabrai-index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"索引页已生成: {output_path}")
    print(f"共 {total} 篇: {speeches}演讲 + {interviews}访谈 + {qas}问答 + {articles}文章")
    print(f"年份跨度: {min(groups.keys())} - {max(groups.keys())}")
    
    # 保存更新后的索引
    updated_path = os.path.join(DEPLOY_DIR, '_pabrai_index_updated.json')
    with open(updated_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def generate_index_html(entries, groups, total, speeches, interviews, qas, articles):
    # 按年份升序排列（从早到晚）
    year_order = sorted(groups.keys(), reverse=True)
    
    # 年份分组HTML
    year_sections = ''
    for yr in year_order:
        items = groups[yr]
        items_html = ''
        for e in items:
            cat_color = {
                '演讲': '#f97316',
                '访谈': '#3b82f6',
                '问答': '#8b5cf6',
                '文章': '#22c55e',
            }.get(e['cat_type'], '#64748b')
            
            real_date_display = e['real_date']
            if len(real_date_display) == 10:
                real_date_display = real_date_display
            elif len(real_date_display) == 7:
                real_date_display = real_date_display
            
            star_badge = '<span class="meta-star">⭐ 必读</span>' if e.get('star') else ''
            
            items_html += f'''
            <a href="{e['url']}" class="speech-item">
              <div class="speech-badge" style="background:{cat_color}20;color:{cat_color};border-color:{cat_color}40">{e['cat_icon']} {e['cat_type']}</div>
              <div class="speech-body">
                <div class="speech-title">{e['title']}</div>
                <div class="speech-meta">
                  <span class="meta-date">{real_date_display}</span>
                  <span class="meta-venue">{e['venue']}</span>
                  {star_badge}
                </div>
              </div>
              <div class="speech-arrow">→</div>
            </a>'''
        
        year_sections += f'''
        <div class="year-section">
          <div class="year-header">{yr}年<span class="year-count">{len(items)}篇</span></div>
          <div class="speech-list">{items_html}</div>
        </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>莫尼什·帕伯莱演讲与访谈全集 — 伯克希尔投资数据中心</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f8f9fa;color:#1a1a2e;line-height:1.75}}
.top-bar{{position:sticky;top:0;z-index:100;background:rgba(15,23,42,0.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.08);padding:12px 20px;display:flex;align-items:center;gap:12px}}
.home-btn{{display:inline-flex;align-items:center;gap:6px;background:rgba(249,115,22,0.15);color:#f97316;border:1px solid rgba(249,115,22,0.3);border-radius:20px;padding:6px 14px;font-size:13px;cursor:pointer;text-decoration:none;transition:all .2s}}
.home-btn:hover{{background:#f97316;color:#fff}}
.breadcrumb{{font-size:13px;color:#94a3b8;display:flex;gap:4px;align-items:center}}
.breadcrumb a{{color:#94a3b8;text-decoration:none}}
.breadcrumb a:hover{{color:#f97316}}
.crumb-sep{{color:#64748b}}
.container{{max-width:860px;margin:0 auto;padding:20px 16px 40px}}
.hero{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border-radius:12px;padding:32px 28px;margin-bottom:24px;color:#fff;display:flex;gap:24px;align-items:center}}
.hero-left{{flex:1}}
.hero-avatar{{width:80px;height:80px;border-radius:50%;background:rgba(249,115,22,0.15);display:flex;align-items:center;justify-content:center;font-size:36px;border:2px solid rgba(249,115,22,0.3);flex-shrink:0}}
.hero-name{{font-size:24px;font-weight:700;margin-bottom:6px}}
.hero-sub{{font-size:14px;color:#94a3b8;margin-bottom:16px}}
.hero-stats{{display:flex;gap:12px}}
.stat-item{{background:rgba(255,255,255,0.08);border-radius:8px;padding:8px 14px;text-align:center}}
.stat-num{{font-size:20px;font-weight:700;color:#f97316}}
.stat-label{{font-size:11px;color:#64748b;margin-top:2px}}
.filter-bar{{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}}
.filter-btn{{display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border-radius:20px;font-size:13px;border:1px solid #e2e8f0;background:#fff;cursor:pointer;transition:all .2s;text-decoration:none;color:#475569}}
.filter-btn:hover,.filter-btn.active{{background:#f97316;color:#fff;border-color:#f97316}}
.year-section{{margin-bottom:20px}}
.year-header{{font-size:18px;font-weight:700;color:#0f172a;padding:10px 0 8px;border-bottom:2px solid #f97316;display:flex;align-items:center;gap:8px}}
.year-count{{font-size:12px;color:#94a3b8;background:rgba(249,115,22,0.1);padding:2px 10px;border-radius:12px}}
.speech-list{{display:flex;flex-direction:column;gap:8px;margin-top:8px}}
.speech-item{{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#fff;border-radius:8px;border:1px solid #e2e8f0;text-decoration:none;color:#1a1a2e;transition:all .2s}}
.speech-item:hover{{background:#f8fafc;border-color:#f97316;transform:translateX(4px}}
.speech-badge{{display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border-radius:16px;font-size:12px;border:1px solid}}
.speech-body{{flex:1;min-width:0}}
.speech-title{{font-size:15px;font-weight:600;line-height:1.4;overflow:hidden;text-overflow:ellipsis}}
.speech-meta{{font-size:12px;color:#94a3b8;display:flex;gap:8px;margin-top:4px}}
.meta-venue{{background:rgba(148,163,184,0.1);padding:1px 8px;border-radius:10px}}
.meta-star{{background:rgba(250,204,21,0.15);color:#ca8a04;padding:1px 8px;border-radius:10px;font-size:11px}}
.speech-arrow{{color:#94a3b8;font-size:14px;flex-shrink:0}}
.source-note{{background:rgba(249,115,22,0.08);border:1px solid rgba(249,115,22,0.2);border-radius:8px;padding:14px 16px;margin-top:20px;font-size:13px;color:#64748b;line-height:1.6}}
@media(max-width:640px){{.hero{{padding:20px 16px;gap:16px}}.hero-name{{font-size:20px}}.hero-stats{{gap:8px}}.stat-item{{padding:6px 10px}}.speech-item{{padding:10px 12px}}.speech-title{{font-size:13px}}}}
</style>
</head>
<body>
<div class="top-bar">
<a href="berkshire-value-investors.html" class="home-btn">← 人物</a>
<div class="breadcrumb">
<a href="berkshire-standalone.html">数据中心</a><span class="crumb-sep">/</span>
<a href="berkshire-value-investors.html">价值投资人物</a><span class="crumb-sep">/</span>
<span>帕伯莱全集</span>
</div>
</div>
<div class="container">
<div class="hero">
<div class="hero-avatar">🧑‍💼</div>
<div class="hero-left">
<div class="hero-name">莫尼什·帕伯莱 演讲与访谈全集</div>
<div class="hero-sub">Mohnish Pabrai · Pabrai Investment Funds · 2007年巴菲特午餐得主 · 《Dhandho Investor》作者</div>
<div class="hero-stats">
<div class="stat-item"><div class="stat-num">{total}</div><div class="stat-label">全部收录</div></div>
<div class="stat-item"><div class="stat-num">{speeches}</div><div class="stat-label">🏛️ 演讲</div></div>
<div class="stat-item"><div class="stat-num">{interviews}</div><div class="stat-label">🎙️ 访谈</div></div>
<div class="stat-item"><div class="stat-num">{qas}</div><div class="stat-label">💬 问答</div></div>
<div class="stat-item"><div class="stat-num">{articles}</div><div class="stat-label">📝 文章</div></div>
</div>
</div>
</div>
<div class="filter-bar">
<a class="filter-btn active" href="berkshire-pabrai-index.html">全部</a>
<a class="filter-btn" href="berkshire-pabrai-index.html?f=speech">🏛️ 演讲</a>
<a class="filter-btn" href="berkshire-pabrai-index.html?f=interview">🎙️ 访谈</a>
<a class="filter-btn" href="berkshire-pabrai-index.html?f=qa">💬 问答</a>
<a class="filter-btn" href="berkshire-pabrai-index.html?f=article">📝 文章</a>
</div>
{year_sections}
<div class="source-note">
📖 收录整理：伯克希尔投资数据中心｜⚠️ 部分历史演讲的日期从标题推断，仅供参考。
</div>
</div>
</body>
</html>'''

if __name__ == '__main__':
    main()
