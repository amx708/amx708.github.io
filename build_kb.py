# -*- coding: utf-8 -*-
# 合并构建：巴菲特投资知识概念库
# 合并原「概念库」(49 深度词条) + 原「知识库」(公司/人物/股东信索引)
# 复用 build_concepts.py 的 CONCEPTS 数据与渲染函数，避免重复维护
import json
from build_concepts import CONCEPTS, CATS, esc, render_body
from kb_index import COMPANIES, PEOPLE, LETTERS


def build():
    cards = []
    modals = []
    for c in CONCEPTS:
        deep_tag = '<span class="tag-deep">深度</span>' if c.get("deep") else '<span class="tag-lite">精要</span>'
        cards.append(f'''<button class="card" data-id="{c['id']}" data-cat="{esc(c['cat'])}" data-name="{esc(c['name'])}">
  <div class="card-top"><span class="card-name">{esc(c['name'])}</span>{deep_tag}</div>
  <div class="card-en">{esc(c['en'])}</div>
  <div class="card-def">{esc(c['def'])}</div>
</button>''')
        modals.append(f'''<div class="modal" id="m-{c['id']}" aria-hidden="true">
  <div class="modal-mask" data-close></div>
  <div class="modal-box">
    <button class="modal-x" data-close aria-label="关闭">×</button>
    <div class="modal-cat">{esc(c['cat'])}</div>
    <h2 class="modal-title">{esc(c['name'])} <span class="modal-en">{esc(c['en'])}</span></h2>
    <div class="modal-body">{render_body(c)}</div>
  </div>
</div>''')

    cat_btns = "".join(
        f'<button class="cat-btn{" active" if cat=="全部" else ""}" data-cat="{esc(cat)}">{esc(cat)}</button>'
        for cat in CATS)
    idx_json = json.dumps({"companies": COMPANIES, "people": PEOPLE, "letters": LETTERS}, ensure_ascii=False)
    cards_joined = "".join(cards)
    modals_joined = "".join(modals)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>巴菲特投资知识概念库 | 伯克希尔投资数据中心</title>
<style>
:root{{--navy:#0b1f3a;--navy2:#102a4c;--orange:#f5a623;--orange2:#ffb84d;--ink:#1a2433;--muted:#6b7a90;--line:#e3e9f2;--bg:#f4f7fb;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7}}
header.top{{position:sticky;top:0;z-index:30;background:rgba(11,31,58,.82);backdrop-filter:blur(10px);border-bottom:1px solid rgba(245,166,35,.35)}}
.top-in{{max-width:1180px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}}
.crumb{{color:#9fb3cf;font-size:13px}}
.crumb a{{color:#9fb3cf;text-decoration:none}}
.crumb a:hover{{color:var(--orange2)}}
.top h1{{margin:0;font-size:19px;color:#fff;font-weight:700}}
.top h1 b{{color:var(--orange)}}
.hero{{max-width:1180px;margin:0 auto;padding:30px 20px 8px}}
.hero h2{{margin:0 0 6px;font-size:26px}}
.hero p{{margin:0;color:var(--muted);max-width:780px}}
.stat{{display:inline-flex;gap:18px;margin-top:14px;flex-wrap:wrap}}
.stat b{{color:var(--navy);font-size:20px}}
.stat span{{color:var(--muted);font-size:13px;display:block}}
.tabs{{max-width:1180px;margin:18px auto 0;padding:0 20px;display:flex;gap:8px;flex-wrap:wrap}}
.tab{{border:1px solid var(--line);background:#fff;color:var(--muted);padding:9px 16px;border-radius:10px;font-size:14px;cursor:pointer;font-weight:600;transition:.15s}}
.tab.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.tab:hover{{border-color:var(--orange)}}
.controls{{max-width:1180px;margin:16px auto 0;padding:0 20px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
.search{{flex:1;min-width:240px;padding:11px 14px;border:1px solid var(--line);border-radius:10px;font-size:15px;outline:none}}
.search:focus{{border-color:var(--orange)}}
.cats{{display:flex;gap:8px;flex-wrap:wrap;max-width:1180px;margin:14px auto 0;padding:0 20px}}
.cat-btn{{border:1px solid var(--line);background:#fff;color:var(--muted);padding:7px 14px;border-radius:999px;font-size:13px;cursor:pointer}}
.cat-btn.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.cat-btn:hover{{border-color:var(--orange)}}
.grid{{max-width:1180px;margin:22px auto 60px;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.grid.idx{{gap:12px}}
.card{{text-align:left;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 16px 18px;cursor:pointer;transition:.15s;position:relative;overflow:hidden}}
.card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(11,31,58,.12);border-color:var(--orange)}}
.card-top{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
.card-name{{font-size:17px;font-weight:700;color:var(--navy)}}
.card-en{{color:var(--muted);font-size:12px;margin:2px 0 8px;letter-spacing:.3px}}
.card-def{{font-size:13.5px;color:#41506a;line-height:1.6}}
.tag-deep{{font-size:11px;color:#fff;background:var(--orange);padding:2px 8px;border-radius:999px;white-space:nowrap}}
.tag-lite{{font-size:11px;color:var(--navy);background:#eaf0f8;padding:2px 8px;border-radius:999px;white-space:nowrap}}
.icard{{display:flex;flex-direction:column;gap:4px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:13px 15px;text-decoration:none;color:var(--ink);transition:.15s}}
.icard:hover{{transform:translateY(-2px);box-shadow:0 6px 18px rgba(11,31,58,.1);border-color:var(--orange)}}
.icard-name{{font-size:15px;font-weight:600;color:var(--navy)}}
.icard-meta{{font-size:12px;color:var(--muted)}}
.modal{{position:fixed;inset:0;z-index:50;display:none}}
.modal.open{{display:block}}
.modal-mask{{position:absolute;inset:0;background:rgba(8,18,34,.55)}}
.modal-box{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:min(720px,92vw);max-height:86vh;overflow:auto;background:#fff;border-radius:16px;padding:26px 28px 30px;box-shadow:0 20px 60px rgba(0,0,0,.3)}}
.modal-x{{position:absolute;top:12px;right:16px;border:none;background:none;font-size:26px;color:var(--muted);cursor:pointer;line-height:1}}
.modal-cat{{display:inline-block;font-size:12px;color:#fff;background:var(--navy);padding:3px 10px;border-radius:999px}}
.modal-title{{margin:10px 0 4px;font-size:23px;color:var(--navy)}}
.modal-en{{font-size:14px;color:var(--muted);font-weight:400}}
.modal-body{{margin-top:10px}}
.c-def{{background:#fbf6ec;border-left:4px solid var(--orange);padding:12px 14px;border-radius:0 8px 8px 0;color:#5a4a2e;font-size:15px}}
.c-h{{margin:22px 0 8px;font-size:15px;color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:6px}}
.point{{margin:10px 0}}
.point b{{color:var(--navy);font-size:14.5px}}
.point p{{margin:3px 0 0;font-size:14px;color:#3c4a60}}
.c-case{{font-size:14px;color:#3c4a60;background:#f3f7fc;padding:12px 14px;border-radius:8px}}
.myth{{margin:6px 0;padding-left:18px}}
.myth li{{font-size:14px;color:#3c4a60;margin:6px 0}}
.quote{{margin:10px 0;padding:10px 14px;background:#fff8ec;border-radius:8px;color:#4a3c22;font-size:14.5px;border-left:3px solid var(--orange)}}
.qy{{display:block;margin-top:6px;color:var(--muted);font-size:12.5px}}
.rel{{display:flex;gap:8px;flex-wrap:wrap}}
.chip{{border:1px solid var(--line);background:#f3f7fc;color:var(--navy);padding:6px 12px;border-radius:999px;font-size:13px;cursor:pointer}}
.chip:hover{{border-color:var(--orange);color:var(--orange)}}
footer{{max-width:1180px;margin:0 auto;padding:24px 20px 50px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line)}}
</style>
</head>
<body>
<header class="top">
  <div class="top-in">
    <h1>伯克希尔·<b>投资知识概念库</b></h1>
    <div class="crumb"><a href="berkshire-standalone.html">首页</a> / 投资数据中心 / 知识概念库</div>
  </div>
</header>
<section class="hero">
  <h2>巴菲特投资知识概念库</h2>
  <p>本站巴菲特投资知识的站内总览：{len(CONCEPTS)} 个核心投资概念（深度解析），并链往业务版图、投资版图、年会实录等。点击下方标签切换「概念 / 公司 / 人物 / 股东信」。</p>
  <div class="stat">
    <div><b>{len(CONCEPTS)}</b><span>核心概念</span></div>
    <div><b>{len(COMPANIES)}</b><span>重要公司</span></div>
    <div><b>{len(PEOPLE)}</b><span>关键人物</span></div>
    <div><b>{len(LETTERS)}</b><span>股东信年表</span></div>
  </div>
</section>
<div class="tabs" id="tabs">
  <button class="tab active" data-tab="concepts">核心概念</button>
  <button class="tab" data-tab="companies">重要公司</button>
  <button class="tab" data-tab="people">关键人物</button>
  <button class="tab" data-tab="letters">股东信</button>
</div>
<div class="controls">
  <input class="search" id="search" placeholder="搜索概念 / 公司 / 人物 / 股东信">
</div>
<div class="cats" id="cats">{cat_btns}</div>
<main class="grid" id="grid">
{cards_joined}
</main>
<main class="grid idx" id="grid-co" style="display:none"></main>
<main class="grid idx" id="grid-pe" style="display:none"></main>
<main class="grid idx" id="grid-le" style="display:none"></main>
<footer>
  <p>伯克希尔投资数据中心 · 知识概念库 | 由原「概念库」与「知识库」合并而成 | 单文件静态页</p>
</footer>
{modals_joined}
<script>
function esc(s){{return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}
const grid=document.getElementById('grid');
const cards=[...grid.querySelectorAll('.card')];
const search=document.getElementById('search');
const catsBar=document.getElementById('cats');
const catBtns=[...document.querySelectorAll('.cat-btn')];
const tabs=[...document.querySelectorAll('.tab')];
const panels={{concepts:grid,companies:document.getElementById('grid-co'),people:document.getElementById('grid-pe'),letters:document.getElementById('grid-le')}};
const IDX_DATA={idx_json};
let curTab='concepts';
let curCat='全部';
for(const key in IDX_DATA){{
  const wrap=panels[key];
  IDX_DATA[key].forEach(it=>{{
    const a=document.createElement('a');
    a.className='icard'; a.href=it.url;
    let meta = it.period ? '<span class="icard-meta">'+it.period+'</span>' : (it.hot!=null ? '<span class="icard-meta">热度 '+it.hot+'</span>' : '');
    a.innerHTML='<span class="icard-name">'+esc(it.name)+'</span>'+meta;
    wrap.appendChild(a);
  }});
}}
function applyFilter(){{
  const q=search.value.trim().toLowerCase();
  if(curTab==='concepts'){{
    cards.forEach(c=>{{
      const name=c.dataset.name.toLowerCase();
      const cat=c.dataset.cat.toLowerCase();
      const okCat=curCat==='全部'||c.dataset.cat===curCat;
      const okQ=!q||name.includes(q)||cat.includes(q)||c.querySelector('.card-en').textContent.toLowerCase().includes(q);
      c.style.display=(okCat&&okQ)?'':'none';
    }});
  }} else {{
    [...panels[curTab].querySelectorAll('.icard')].forEach(a=>{{
      const ok=!q||a.querySelector('.icard-name').textContent.toLowerCase().includes(q);
      a.style.display=ok?'':'none';
    }});
  }}
}}
function showTab(t){{
  curTab=t;
  tabs.forEach(x=>x.classList.toggle('active',x.dataset.tab===t));
  for(const k in panels){{ panels[k].style.display=(k===t)?'grid':'none'; }}
  catsBar.style.display=(t==='concepts')?'flex':'none';
  applyFilter();
}}
search.addEventListener('input',applyFilter);
catBtns.forEach(b=>b.addEventListener('click',()=>{{catBtns.forEach(x=>x.classList.remove('active'));b.classList.add('active');curCat=b.dataset.cat;applyFilter();}}));
tabs.forEach(b=>b.addEventListener('click',()=>showTab(b.dataset.tab)));
function openModal(id){{
  const m=document.getElementById('m-'+id);
  if(!m)return;
  m.classList.add('open');m.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
}}
function closeModal(m){{m.classList.remove('open');m.setAttribute('aria-hidden','true');document.body.style.overflow='';}}
cards.forEach(c=>c.addEventListener('click',()=>openModal(c.dataset.id)));
document.querySelectorAll('.modal').forEach(m=>{{
  m.querySelectorAll('[data-close]').forEach(x=>x.addEventListener('click',()=>closeModal(m)));
  m.querySelectorAll('.chip').forEach(ch=>ch.addEventListener('click',e=>{{e.stopPropagation();closeModal(m);openModal(ch.dataset.id);}}));
}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape'){{document.querySelectorAll('.modal.open').forEach(closeModal);}}}});
showTab('concepts');
</script>
</body>
</html>'''
    return html


if __name__ == "__main__":
    out = build()
    with open("berkshire-concepts.html", "w", encoding="utf-8") as f:
        f.write(out)
    print("written berkshire-concepts.html, concepts=", len(CONCEPTS),
          "companies=", len(COMPANIES), "people=", len(PEOPLE), "letters=", len(LETTERS))
