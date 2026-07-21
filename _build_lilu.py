# -*- coding: utf-8 -*-
"""Build Li Lu reading pages from public speech sources (verbatim transcript style)."""
import requests, bs4, re, os

OUT = os.path.join(os.path.dirname(__file__), "value-investors-content")
os.makedirs(OUT, exist_ok=True)

CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei","Helvetica Neue",sans-serif;background:#f1f5f9;color:#1e293b;line-height:1.7;min-height:100vh}
.top-home-bar{position:sticky;top:0;z-index:100;background:linear-gradient(135deg,#0f172a,#1e293b);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:10px 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08)}
.top-home-bar .left{display:flex;align-items:center;gap:12px}
.home-btn{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.18);border-radius:20px;color:rgba(255,255,255,0.85);font-size:13px;font-weight:500;text-decoration:none;transition:all 0.2s ease}
.home-btn:hover{background:rgba(255,255,255,0.18);color:#fff}
.breadcrumb-bar{font-size:13px;color:rgba(255,255,255,0.5);display:flex;align-items:center;gap:6px}
.breadcrumb-bar a{color:rgba(255,255,255,0.65);text-decoration:none;transition:color 0.15s}
.breadcrumb-bar a:hover{color:#fbbf24}
.breadcrumb-bar span{color:rgba(255,255,255,0.3)}
.breadcrumb-bar .current{color:rgba(255,255,255,0.85);font-weight:500}
.speech-hero{position:relative;background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 40%,#1e293b 100%);padding:48px 24px 60px;text-align:center;overflow:hidden}
.speech-hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at 30% 20%, rgba(37,99,235,0.12) 0%, transparent 50%),radial-gradient(ellipse at 70% 80%, rgba(245,158,11,0.06) 0%, transparent 50%);pointer-events:none}
.speech-hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:80px;background:linear-gradient(to top, #f1f5f9 0%, transparent 100%);pointer-events:none}
.hero-content{position:relative;z-index:2;max-width:820px;margin:0 auto}
.hero-badge{display:inline-block;padding:4px 14px;background:rgba(37,99,235,0.15);border:1px solid rgba(37,99,235,0.3);border-radius:20px;color:#60a5fa;font-size:12px;font-weight:500;letter-spacing:0.5px;margin-bottom:18px}
.hero h1{font-size:clamp(22px,3.5vw,34px);font-weight:800;color:#fff;line-height:1.3;margin-bottom:10px}
.hero .speech-sub{font-size:15px;color:#94a3b8;margin-bottom:16px;line-height:1.6}
.hero .speech-meta-row{display:flex;gap:16px;justify-content:center;font-size:13px;color:rgba(255,255,255,0.55);flex-wrap:wrap}
.hero .speech-meta-row span{display:flex;align-items:center;gap:4px}
.tag-bar{display:flex;gap:8px;justify-content:center;margin-top:20px;flex-wrap:wrap}
.tag-pill{padding:4px 12px;border-radius:8px;font-size:12px;font-weight:500}
.tag-pill.tag-global{background:rgba(37,99,235,0.15);border:1px solid rgba(37,99,235,0.3);color:#60a5fa}
.tag-pill.tag-value{background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);color:#fbbf24}
.tag-pill.tag-moat{background:rgba(5,150,105,0.15);border:1px solid rgba(5,150,105,0.3);color:#34d399}
.tag-pill.tag-life{background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);color:#c084fc}
.tag-pill.tag-china{background:rgba(220,38,38,0.15);border:1px solid rgba(220,38,38,0.3);color:#f87171}
.tag-pill.tag-era{background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.3);color:#a5b4fc}
.content-wrap{max-width:860px;margin:0 auto;padding:48px 24px 80px}
.section-h2{font-size:22px;font-weight:700;color:#0f172a;margin:40px 0 16px;padding-left:14px;border-left:4px solid #2563eb;line-height:1.3}
.section-h2:first-child{margin-top:0}
.section-h3{font-size:17px;font-weight:600;color:#1e293b;margin:24px 0 12px}
.speech-p{font-size:15.5px;color:#334155;line-height:1.85;margin-bottom:16px;text-indent:0}
.speaker-buf{color:#dc2626;font-weight:700}
.speaker-host{color:#0284c7;font-weight:700}
.speaker-li{color:#dc2626;font-weight:700}
.speaker-green{color:#0284c7;font-weight:700}
.speech-quote{margin:24px 0;padding:20px 24px;border-radius:12px;background:linear-gradient(135deg,#f8fafc,#fff);border:1px solid #e2e8f0;border-left:4px solid #f59e0b;font-size:15px;color:#475569;line-height:1.75}
.speech-quote .quote-mark{font-size:28px;color:#f59e0b;font-weight:700;line-height:1;float:left;margin-right:8px;margin-top:-4px}
.speech-quote .quote-source{font-size:12px;color:#94a3b8;margin-top:10px;font-style:normal;font-weight:500}
.key-point{margin:20px 0;padding:18px 22px;border-radius:10px;background:#fff;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.key-point .kp-icon{font-size:18px;margin-bottom:4px}
.key-point .kp-title{font-size:14px;font-weight:700;color:#0f172a;margin-bottom:6px}
.key-point .kp-text{font-size:13.5px;color:#64748b;line-height:1.6}
.section-nav{position:sticky;top:48px;z-index:50;background:#fff;border-bottom:1px solid #e2e8f0;padding:8px 24px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;box-shadow:0 1px 4px rgba(0,0,0,0.04)}
.nav-link{padding:4px 12px;border-radius:6px;font-size:12px;font-weight:500;color:#64748b;text-decoration:none;border:1px solid transparent;transition:all 0.15s ease}
.nav-link:hover{color:#2563eb;border-color:#bfdbfe;background:#eff6ff}
.page-footer{max-width:860px;margin:0 auto;padding:24px;text-align:center;font-size:12px;color:#94a3b8;border-top:1px solid #e2e8f0}
.qa{margin:22px 0;padding:18px 22px;border-radius:12px;background:#fff;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.qa-q{font-size:15.5px;font-weight:700;color:#1e293b;margin-bottom:10px;padding-left:12px;border-left:4px solid #2563eb;line-height:1.6}
.qa-a{font-size:15px;color:#334155;line-height:1.85}
.qa-a p{margin-bottom:12px}
.qa-a p:last-child{margin-bottom:0}
@media(max-width:768px){.speech-hero{padding:40px 20px 50px}.content-wrap{padding:32px 20px 60px}.section-h2{font-size:18px}.speech-p{font-size:14.5px}.section-nav{top:0;padding:6px 12px}.top-home-bar{padding:8px 16px}}"""

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 李录</title>
<style>{css}</style>
</head>
<body>

<div class="top-home-bar">
  <div class="left">
    <a href="index.html" class="home-btn">🏠 首页</a>
    <div class="breadcrumb-bar">
      <a href="index.html">首页</a><span>/</span>
      <a href="berkshire-standalone.html">数据中心</a><span>/</span>
      <a href="berkshire-value-investors.html">价值投资人物</a><span>/</span>
      <span class="current">李录·{short}</span>
    </div>
  </div>
</div>

<div class="section-nav">
{nav}
</div>

<div class="speech-hero">
  <div class="hero-content">
    <div class="hero-badge">{badge}</div>
    <h1>{title}</h1>
    <div class="speech-sub">{sub}</div>
    <div class="speech-meta-row">
      <span>📅 {date}</span>
      <span>📍 {venue}</span>
      <span>🎤 李录</span>
    </div>
    <div class="tag-bar">
{tags}
    </div>
  </div>
</div>

<div class="content-wrap">
{body}
</div>

<div class="page-footer">
  内容来源：{source} · 仅供学习参考 · 不构成投资建议<br>
  <a href="berkshire-value-investors.html" style="color:#2563eb;text-decoration:none;font-weight:500">← 返回价值投资人物</a>
</div>

</body>
</html>"""

DROP = ["责任编辑","返回搜狐","扫码","关注我们","24小时滚动播报","炒股就看","金麒麟","报名入口","粉丝福利",
        "原文链接","转载请","风险提示","声明：","本文来源","更多精彩","点击查看","打开APP","下载APP",
        "未经授权","版权所有","微信公众号","芒格书院","聪明投资者","巴伦周刊","证券市场周刊","新浪财经",
        "澎湃新闻","腾讯新闻","凤凰网","基金嘉年华","推荐阅读","往期回顾","分享到","点赞","在看",
        "点击上方","订阅","商务合作","联系我们","免责声明","本文版权","制图","编辑部"]

def clean_text(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def bold(s):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)

def inject_h2(body, items, anchors):
    """Insert synthetic <h2> section breaks before the first paragraph containing each trigger."""
    idx = 0
    for trig, head in items:
        aid = anchors[idx] if idx < len(anchors) else f"s{idx+1}"
        idx += 1
        pat = re.compile(r'<p class="speech-p">[^<]*' + re.escape(trig) + r'[^<]*</p>')
        m = pat.search(body)
        if m:
            body = body[:m.start()] + f'<h2 class="section-h2" id="{aid}">{head}</h2>' + body[m.end():]
        else:
            print("  WARN inject_h2 trigger not found:", trig)
    return body

def is_drop(p):
    if len(p) < 4: 
        return True
    for d in DROP:
        if d in p:
            return True
    return False

def extract_paras(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    for tag in soup(["script","style","noscript","iframe","svg","header","footer","nav","aside","form","button","meta","link"]):
        tag.decompose()
    # Uniform: take all <p> from the whole document, then filter.
    ps=[p.get_text(" ",strip=True) for p in soup.find_all("p")]
    ps=[clean_text(p) for p in ps]
    ps=[p for p in ps if len(p)>5 and not is_drop(p)]
    # dedupe consecutive duplicates
    out=[]
    for p in ps:
        if out and p==out[-1]: continue
        out.append(p)
    # fallback: if too few, pull block text from largest div
    if len(out)<5:
        divs=soup.find_all("div")
        best=max(divs,key=lambda c:len(c.get_text(strip=True))) if divs else soup
        lines=[clean_text(l) for l in best.get_text("\n",strip=True).split("\n")]
        out=[l for l in lines if len(l)>5 and not is_drop(l)]
    # trim trailing @handle / website promo
    while out and (out[-1].startswith("@") or len(out[-1])<8):
        out.pop()
    while out and (out[0].startswith("@") or len(out[0])<8):
        out.pop(0)
    return out

HEADING_RE = re.compile(r'^(一|二|三|四|五|六|七|八|九|十){1,3}[、．.．\s]')
HEADING_RE2 = re.compile(r'^（(一|二|三|四|五|六|七|八|九|十)）')
NUM_HEAD_RE = re.compile(r'^\d{1,2}[\.\、]\s*\S')

def render_sections(paras, anchors):
    out=[]
    idx=0
    for p in paras:
        if HEADING_RE.match(p) or HEADING_RE2.match(p):
            aid = anchors[idx] if idx < len(anchors) else f"s{idx+1}"
            idx+=1
            out.append(f'<h2 class="section-h2" id="{aid}">{p}</h2>')
        elif NUM_HEAD_RE.match(p) and len(p)<40:
            aid = anchors[idx] if idx < len(anchors) else f"s{idx+1}"
            idx+=1
            out.append(f'<h2 class="section-h2" id="{aid}">{p}</h2>')
        else:
            out.append(f'<p class="speech-p">{p}</p>')
    return "\n".join(out)

def render_qa(paras):
    """Render dialogue: split on 问： ; preserve speaker labels inline."""
    out=[]
    buf=[]
    cur_q=None
    def flush():
        nonlocal cur_q, buf
        if cur_q is None and not buf: return
        block=f'<div class="qa">'
        if cur_q:
            block+=f'<div class="qa-q">问：{cur_q}</div>'
        ans="".join(buf)
        # split speaker turns
        ans=re.sub(r'(李录[：:])\s*', r'<span class="speaker-li">李录：</span>', ans)
        ans=re.sub(r'(布鲁斯[·\s]?格林沃德[：:])\s*', r'<span class="speaker-green">布鲁斯·格林沃德：</span>', ans)
        ans=re.sub(r'(格林沃德[：:])\s*', r'<span class="speaker-green">格林沃德：</span>', ans)
        ans_paras=[a.strip() for a in re.split(r'(?<=。)\s*(?=<span)', ans) ] if False else [ans]
        block+=f'<div class="qa-a"><p>{ans}</p></div></div>'
        out.append(block)
        cur_q=None; buf=[]
    for p in paras:
        m=re.match(r'^\s*问[：:]\s*(.*)', p)
        if m:
            flush()
            cur_q=m.group(1).strip()
        else:
            buf.append(p)
    flush()
    return "\n".join(out)

def render_dialogue(paras):
    """Speaker-labeled dialogue: 布鲁斯·格林沃德 / 李录 turns."""
    out=[]
    for p in paras:
        m=re.match(r"^\s*(布鲁斯[·\s]*格林沃德|格林沃德)\s*[：:]\s*(.*)", p)
        if m:
            out.append(f'<p class="speech-p"><span class="speaker-green">布鲁斯·格林沃德：</span>{bold(esc(m.group(2)))}</p>')
            continue
        m=re.match(r"^\s*(李录)\s*[：:]\s*(.*)", p)
        if m:
            out.append(f'<p class="speech-p"><span class="speaker-li">李录：</span>{bold(esc(m.group(2)))}</p>')
            continue
        out.append(f'<p class="speech-p">{bold(esc(p))}</p>')
    return "\n".join(out)

ARTICLES = [
 {
  "file":"li-lu-2015.html",
  "url":"https://weibo.com/ttarticle/p/show?id=2309635125362693832798",
  "title":"价值投资在中国的展望",
  "short":"2015北大",
  "badge":"🎓 Li Lu · 北京大学光华管理学院",
  "sub":"李录2015年重返北大讲台的首场价值投资课——系统梳理价值投资四大核心理念，论证其在中国市场的适用性",
  "date":"2015年10月23日",
  "venue":"北京大学光华管理学院",
  "tags":['<span class="tag-pill tag-value">价值投资四大理念</span>','<span class="tag-pill tag-china">适用于中国</span>','<span class="tag-pill tag-life">资产管理伦理</span>'],
  "nav":'<a href="#s1" class="nav-link">① 行业伦理</a><a href="#s2" class="nav-link">② 财富增长</a><a href="#s3" class="nav-link">③ 投资大道</a><a href="#s4" class="nav-link">④ 中国适用</a>',
  "anchors":["s1","s2","s3","s4"],
  "mode":"sections",
  "source":"李录2015年10月北京大学光华管理学院演讲（微博长文整理）",
 },
 {
  "file":"li-lu-2024.html",
  "url":"https://business.sohu.com/a/843484608_121124365",
  "title":"全球价值投资与时代",
  "short":"2024北大",
  "badge":"🎓 Li Lu · 北大光华价值投资课程十周年",
  "sub":"第三次登上北大讲台，从宏观时代变量切入——中等收入陷阱、国际秩序重塑、消费占比提升，回归价值投资六原则",
  "date":"2024年12月7日",
  "venue":"北京大学光华管理学院 · 价值投资课程十周年",
  "tags":['<span class="tag-pill tag-era">时代变量</span>','<span class="tag-pill tag-value">价值投资六原则</span>','<span class="tag-pill tag-china">中国消费红利</span>'],
  "nav":'<a href="#s1" class="nav-link">① 时代困惑</a><a href="#s2" class="nav-link">② 中等收入陷阱</a><a href="#s3" class="nav-link">③ 应对之道</a>',
  "anchors":["s1","s2","s3"],
  "mode":"sections",
  "inject_h2":[("先谈第一个主题","一、我们时代的困惑"),("中等收入陷阱","二、中等收入陷阱与国家的跨越"),("全球价值投资人应该如何应对时代的挑战","三、回到主题：全球价值投资人如何应对时代")],
  "source":"李录2024年12月北京大学光华管理学院《价值投资》课程十周年沙龙演讲（搜狐财经整理）",
 },
 {
  "file":"lilu-2021-columbia.html",
  "url":"https://licai.cofool.com/user/guide_view_1922499.html",
  "title":"市场的疯狂和暴跌可以服务于你",
  "short":"2021哥大对话",
  "badge":"🎙️ Li Lu × Bruce Greenwald",
  "sub":"2021哥伦比亚大学中国商业论坛炉边对话——与价值投资大师格林沃德畅谈价值投资、中国市场与应对波动的性情",
  "date":"2021年4月10日",
  "venue":"哥伦比亚大学中国商业论坛",
  "tags":['<span class="tag-pill tag-value">价值投资本质</span>','<span class="tag-pill tag-china">布局中国</span>','<span class="tag-pill tag-life">市场波动</span>'],
  "nav":'<a href="#qa" class="nav-link">💬 对话实录</a>',
  "anchors":["qa"],
  "mode":"dialogue",
  "source":"李录与布鲁斯·格林沃德2021年哥伦比亚大学中国商业论坛炉边对话（公开整理）",
 },
 {
  "file":"lilu-2021-china-economy.html",
  "url":"https://www.thepaper.cn/newsdetail_forward_11449181",
  "title":"中国未来20年的经济大趋势",
  "short":"2021经济演讲",
  "badge":"📈 Li Lu · 中国经济展望",
  "sub":"李录破例谈宏观——从中西方文化差异到现代化历程，从刘易斯拐点到工程师红利，推演中国经济的增长潜力",
  "date":"2021年3月2日",
  "venue":"公开演讲（澎湃新闻整理）",
  "tags":['<span class="tag-pill tag-china">中国经济</span>','<span class="tag-pill tag-era">现代化历程</span>','<span class="tag-pill tag-value">投资逻辑</span>'],
  "nav":'<a href="#s1" class="nav-link">① 中西方差异</a><a href="#s2" class="nav-link">② 现代化历程</a><a href="#s3" class="nav-link">③ 悲观情绪</a><a href="#s4" class="nav-link">④ 三阶段</a><a href="#s5" class="nav-link">⑤ 增长潜力</a>',
  "anchors":["s1","s2","s3","s4","s5"],
  "mode":"sections",
  "source":"李录2021年关于中国未来20年经济大趋势的公开演讲（澎湃新闻整理）",
 },
 {
  "file":"lilu-2025-tariff.html",
  "url":"https://finance.sina.cn/fund/sm/2025-04-24/detail-ineuhiqt3436765.d.html?vt=4",
  "title":"关税战、世界秩序与中国",
  "short":"2025关税访谈",
  "badge":"🗞️ Li Lu · 芒格书院问答",
  "sub":"59岁生日之际在西雅图接受芒格书院会员提问——两个堵点、贸易战与世界秩序转移、中美关系与AI冲击",
  "date":"2025年4月6日",
  "venue":"西雅图 · 芒格书院会员问答",
  "tags":['<span class="tag-pill tag-era">世界秩序</span>','<span class="tag-pill tag-china">内需转型</span>','<span class="tag-pill tag-life">AI冲击</span>'],
  "nav":'<a href="#qa" class="nav-link">💬 问答实录</a>',
  "anchors":["qa"],
  "mode":"qa",
  "source":"李录2025年4月6日西雅图问答（芒格书院整理，新浪财经刊发）",
 },
]

import time

def fetch(url):
    last=None
    hdr={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for attempt in range(4):
        try:
            r=requests.get(url, headers=hdr, timeout=30)
            r.encoding=r.apparent_encoding
            if r.status_code==200:
                return r
            last=Exception("HTTP %d"%r.status_code)
        except Exception as e:
            last=e
            print("  retry", attempt+1, repr(e)[:80])
        time.sleep(1)
    try:
        r=requests.get(url, headers=hdr, timeout=30, verify=False)
        r.encoding=r.apparent_encoding
        return r
    except Exception as e:
        raise last or e

for a in ARTICLES:
    print("Fetching", a["file"], "...")
    try:
        r=fetch(a["url"])
    except Exception as e:
        import traceback; traceback.print_exc()
        print("  FAILED", a["file"], repr(e)[:120]); continue
    paras=extract_paras(r.text)
    print("  paras:", len(paras), "chars:", sum(len(p) for p in paras))
    if len(paras) < 20:
        print("  TOO FEW paras, skipping write to preserve existing file")
        continue
    if a["mode"]=="qa":
        body=render_qa(paras)
    elif a["mode"]=="dialogue":
        body=render_dialogue(paras)
    else:
        body=render_sections(paras, a["anchors"])
    if "inject_h2" in a:
        body=inject_h2(body, a["inject_h2"], a["anchors"])
    html=HEAD.format(css=CSS, title=a["title"], short=a["short"], badge=a["badge"],
                     sub=a["sub"], date=a["date"], venue=a["venue"], tags="\n".join(a["tags"]),
                     nav=a["nav"], body=body, source=a["source"])
    path=os.path.join(OUT, a["file"])
    with open(path,"w",encoding="utf-8") as f:
        f.write(html)
    print("  -> wrote", path, len(html), "bytes")
print("DONE")
