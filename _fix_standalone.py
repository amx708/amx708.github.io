import re, sys
from pathlib import Path

f = Path("C:/Users/Administrator/WorkBuddy/2026-07-08-13-16-44/deploy_site/berkshire-standalone.html")
text = f.read_text(encoding="utf-8")

# 1. 去掉两个股东信卡片的 grid-row span
for n in (2, 5):
    text = text.replace(f'<div class="card accent-gold" style="grid-row:span {n}">',
                        '<div class="card accent-gold">')

# 2. 替换右侧股东信卡片描述
old_desc = '1957 — 2024 年中文翻译，含 1957-1970 合伙基金时期信件（芒格书院共读群友整理）'
new_desc = '1971 — 2024 年中文翻译（芒格书院共读群友整理）'
if old_desc in text:
    text = text.replace(old_desc, new_desc, 1)

# 3. 删除右侧股东信卡片中 1957-1970 的 14 个年份链接，保留 1971-2024
# 找到第二个年份网格（即「巴菲特历年致股东的信」内部的 year-grid）
blocks = text.split('<!-- 4. 股东信 -->')
if len(blocks) == 2:
    header, rest = blocks
    # 把 rest 再按「<!-- 5. Greg Abel 信 -->」分割，只处理股东信部分
    shareholder_part, footer = rest.split('<!-- 5. Greg Abel 信 -->', 1)
    # 在 shareholder_part 里定位 year-grid
    start_idx = shareholder_part.find('<div class="year-grid">')
    end_idx = shareholder_part.find('</div>\n      </div>\n    </div>\n\n    <!-- 5. Greg Abel 信 -->')
    # 更稳：找到从 start_idx 开始第一个 </div> 闭合标签
    grid_open = '<div class="year-grid">'
    start = shareholder_part.find(grid_open)
    # 手动找结束位置：从 start 后找 "</div>" 作为 year-grid 的闭合
    end_tag = '</div>'
    end = shareholder_part.find(end_tag, start + len(grid_open))
    # 提取 grid 内容
    grid_content = shareholder_part[start + len(grid_open):end]
    # 删除 1957-1970 的链接行
    lines = grid_content.split('\n')
    filtered = []
    for line in lines:
        if 'href="letters_content/cn/19' in line:
            m = re.search(r'cn/(\d{4})\.html"', line)
            if m and int(m.group(1)) <= 1970:
                continue
        filtered.append(line)
    new_grid = grid_open + '\n'.join(filtered) + end_tag
    shareholder_part = shareholder_part[:start] + new_grid + shareholder_part[end+len(end_tag):]
    rest = shareholder_part + '<!-- 5. Greg Abel 信 -->' + footer
    text = header + '<!-- 4. 股东信 -->' + rest

# 4. 调整年份网格：给不同卡片用更合适的列数，避免宽屏下太挤
# 在 year-grid 规则后增加针对两个特殊网格的覆盖
extra_css = '''
/* 年份网格：自动适应容器宽度，避免右侧被截断 */
.year-grid{grid-template-columns:repeat(auto-fit, minmax(40px, 1fr))}
.partner-year-grid,
.shareholder-year-grid{grid-template-columns:repeat(auto-fit, minmax(40px, 1fr))}
@media(max-width:900px){
  .year-grid,
  .partner-year-grid,
  .shareholder-year-grid{grid-template-columns:repeat(auto-fit, minmax(40px, 1fr))}
}
@media(max-width:768px){
  .year-grid,
  .partner-year-grid,
  .shareholder-year-grid{grid-template-columns:repeat(auto-fit, minmax(36px, 1fr))}
}
@media(max-width:480px){
  .year-grid,
  .partner-year-grid,
  .shareholder-year-grid{grid-template-columns:repeat(auto-fit, minmax(32px, 1fr))}
}
'''
# 插入到 .year-grid 规则块之后、Coming soon 规则之前
insert_marker = '/* Coming soon cards */'
if insert_marker in text and extra_css not in text:
    text = text.replace(insert_marker, extra_css + insert_marker)

f.write_text(text, encoding="utf-8")
print("done")
