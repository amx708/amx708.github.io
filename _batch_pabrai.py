"""
批量提取帕伯莱演讲/访谈 docx 文件，生成 HTML 页面和索引页。
排除：持仓周报、ETF电话会议、付费内容等非演讲类文件。
"""

import os, re, sys, json
from docx import Document

# ============ 配置 ============
DEPLOY_DIR = os.path.join(os.path.dirname(__file__), 'deploy_site')
CONTENT_DIR = os.path.join(DEPLOY_DIR, 'value-investors-content')
SRC_DIRS = [
    r'E:/公众号采集/投资漫想/word',
    r'E:/公众号采集/欣原驿马/word',
]

# 排除关键词（持仓周报、ETF电话会议、付费、截断文件名等）
EXCLUDE_KEYWORDS = ['持仓周报', 'Shareholder Call', '股东电话会议', '付费', 'Wagons ETF']

# 帕伯莱相关关键词
PABRAI_KEYWORDS = ['帕伯莱', '帕布拉', '帕布莱', '莫尼什', 'Pabrai', 'Mohnish']

# ============ 篮选文件 ============
def is_pabrai_file(filename):
    return any(kw in filename for kw in PABRAI_KEYWORDS)

def is_excluded(filename):
    return any(kw in filename for kw in EXCLUDE_KEYWORDS)

def find_files():
    results = []
    for src_dir in SRC_DIRS:
        if not os.path.exists(src_dir):
            print(f"  [WARN] 目录不存在: {src_dir}")
            continue
        for fn in os.listdir(src_dir):
            if not fn.endswith('.docx'):
                continue
            if not is_pabrai_file(fn):
                continue
            if is_excluded(fn):
                print(f"  [SKIP] 排除: {fn}")
                continue
            results.append(os.path.join(src_dir, fn))
    return results

# ============ 提取 docx 文本 ============
def extract_docx_text(filepath):
    """提取docx全部段落文本，保留换行"""
    doc = Document(filepath)
    paragraphs = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            paragraphs.append(text)
    return '\n'.join(paragraphs)

# ============ 从文件名解析信息 ============
def parse_filename(fn):
    """从公众号采集文件名解析日期、标题、来源"""
    # 格式: 来源_YYYY-MM-DD_标题.docx
    base = fn.replace('.docx', '')
    parts = base.split('_', 2)
    if len(parts) >= 3:
        source = parts[0]
        date = parts[1]
        title = parts[2]
    else:
        source = ''
        date = ''
        title = base
    
    # 清理标题
    title = title.strip()
    
    # 判断上下/中下
    part_label = ''
    if '（上）' in title or '(上)' in title:
        part_label = '（上）'
    elif '（下）' in title or '(下)' in title:
        part_label = '（下）'
    elif '（中）' in title or '(中)' in title:
        part_label = '（中）'
    
    return {'source': source, 'date': date, 'title': title, 'part': part_label}

# ============ 确定分类和标签 ============
def classify_entry(info):
    """判断演讲类型：演讲、访谈、问答、文章"""
    title = info['title']
    if '演讲' in title or '讲座' in title:
        return '演讲', '🏛️'
    elif '访谈' in title or '专访' in title or '播客' in title or '日记' in title:
        return '访谈', '🎙️'
    elif '问答' in title or 'Q&A' in title or 'Q&amp;A' in title or '互动' in title or '炉边' in title:
        return '问答', '💬'
    elif '交流实录' in title:
        return '问答', '💬'
    elif '十诫' in title or '六味药' in title or '投资术' in title or '持股哲学' in title or '清单' in title:
        return '文章', '📝'
    else:
        return '演讲', '🏛️'

# ============ 生成 HTML slug ============
def make_slug(info):
    """从日期+标题生成简短slug"""
    date = info['date'].replace('-', '')
    # 取标题前20字符做slug
    title_clean = re.sub(r'[^\w\u4e00-\u9fff]', '', info['title'][:30])
    slug = f"pabrai-{date}-{title_clean}"
    # 确保slug不会太长
    slug = slug[:60]
    return slug

# ============ HTML 模板 ============
def make_html(info, text, source_name):
    """生成演讲全文HTML页面"""
    title = info['title']
    date = info['date']
    cat_type, cat_icon = classify_entry(info)
    
    # 转义HTML
    text_html = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # 段落化
    paragraphs_html = '\n'.join(f'<p>{line}</p>' for line in text_html.split('\n') if line.strip())
    
    # 来源标注
    source_label = '投资漫想' if '投资漫想' in source_name else '欣原驿马'
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — 莫尼什·帕伯莱</title>
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
.container{{max-width:780px;margin:0 auto;padding:20px 16px 40px}}
.hero{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border-radius:12px;padding:32px 28px;margin-bottom:24px;color:#fff}}
.hero-cat{{display:inline-flex;align-items:center;gap:6px;background:rgba(249,115,22,0.2);color:#f97316;padding:4px 12px;border-radius:16px;font-size:13px;margin-bottom:12px}}
.hero-title{{font-size:22px;font-weight:700;line-height:1.4;margin-bottom:12px}}
.hero-meta{{font-size:14px;color:#94a3b8;display:flex;gap:8px;align-items:center}}
.hero-source{{background:rgba(148,163,184,0.15);padding:2px 10px;border-radius:12px;font-size:12px}}
.content-box{{background:#fff;border-radius:12px;padding:28px 24px;border:1px solid #e2e8f0}}
.content-box p{{margin-bottom:12px;text-align:justify}}
.content-box p:last-child{{margin-bottom:0}}
.source-note{{background:rgba(249,115,22,0.08);border:1px solid rgba(249,115,22,0.2);border-radius:8px;padding:12px 16px;margin-top:24px;font-size:13px;color:#64748b;display:flex;align-items:center;gap:8px}}
.source-note::before{{content:"📖"}}
@media(max-width:640px){{.hero{{padding:20px 16px}}.hero-title{{font-size:18px}}.content-box{{padding:16px 14px}}}}
</style>
</head>
<body>
<div class="top-bar">
<a href="../berkshire-value-investors.html" class="home-btn">← 人物</a>
<div class="breadcrumb">
<a href="../berkshire-standalone.html">数据中心</a><span class="crumb-sep">/</span>
<a href="../berkshire-value-investors.html">价值投资人物</a><span class="crumb-sep">/</span>
<span>帕伯莱</span>
</div>
</div>
<div class="container">
<div class="hero">
<div class="hero-cat">{cat_icon} {cat_type}</div>
<div class="hero-title">{title}</div>
<div class="hero-meta">
<span>{date}</span>
<span class="hero-source">{source_label}</span>
</div>
</div>
<div class="content-box">
{paragraphs_html}
</div>
<div class="source-note">
来源：{source_label}（公众号）｜ 整理收录：伯克希尔投资数据中心
</div>
</div>
</body>
</html>'''

# ============ 主流程 ============
def main():
    os.makedirs(CONTENT_DIR, exist_ok=True)
    
    files = find_files()
    print(f"找到 {len(files)} 个帕伯莱相关文件")
    
    entries = []
    
    for filepath in files:
        fn = os.path.basename(filepath)
        info = parse_filename(fn)
        slug = make_slug(info)
        cat_type, cat_icon = classify_entry(info)
        source_name = os.path.basename(os.path.dirname(filepath))
        
        # 提取文本
        try:
            text = extract_docx_text(filepath)
            if not text:
                print(f"  [WARN] 空内容: {fn}")
                continue
        except Exception as e:
            print(f"  [ERROR] 提取失败: {fn} - {e}")
            continue
        
        # 生成HTML
        html = make_html(info, text, source_name)
        html_path = os.path.join(CONTENT_DIR, f"{slug}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        entry = {
            'slug': slug,
            'title': info['title'],
            'date': info['date'],
            'source': source_name,
            'cat_type': cat_type,
            'cat_icon': cat_icon,
            'part': info['part'],
            'url': f"value-investors-content/{slug}.html",
        }
        entries.append(entry)
        print(f"  [OK] {fn} → {slug}.html ({len(text)} chars, {cat_type})")
    
    # 按日期降序排列
    entries.sort(key=lambda e: e['date'], reverse=True)
    
    # 输出JSON索引供后续使用
    index_path = os.path.join(DEPLOY_DIR, '_pabrai_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    
    print(f"\n共生成 {len(entries)} 个HTML页面")
    print(f"索引已保存到 {index_path}")
    
    # 按年份统计
    years = {}
    for e in entries:
        yr = e['date'][:4] if e['date'] else '未知'
        if yr not in years:
            years[yr] = 0
        years[yr] += 1
    print("\n年份分布:")
    for yr in sorted(years.keys()):
        print(f"  {yr}: {years[yr]}篇")

if __name__ == '__main__':
    main()
