# -*- coding: utf-8 -*-
"""Build li-lu-2019.html from the WebFetch-recovered full transcript of
Li Lu's 2019 PKU speech '价值投资如何做到知行合一'."""
import os, re

HERE=os.path.dirname(__file__)
OUT=os.path.join(HERE,"value-investors-content")

# reuse exact CSS from the already-built 2015 page
css_src=open(os.path.join(OUT,"li-lu-2015.html"),encoding="utf-8").read()
CSS=re.search(r"<style>(.*?)</style>", css_src, re.S).group(1)
CSS += """
.li-bullets{margin:8px 0 16px 4px;padding-left:22px}
.li-bullets li{font-size:15.5px;color:#334155;line-height:1.8;margin-bottom:6px}"""

TITLE="价值投资在实践中的知行合一"
SHORT="2019北大"
BADGE="🎓 Li Lu · 北京大学光华管理学院"
SUB="时隔四年再度登上北大讲台，从实践维度探讨知行合一——能力圈的真实边界、投资与投机的本质、价值投资人的品性，以及比亚迪22年8次暴跌50%的心路"
DATE="2019年11月29日"
VENUE="北京大学光华管理学院"
TAGS='<span class="tag-pill tag-value">知行合一</span><span class="tag-pill tag-moat">能力圈边界</span><span class="tag-pill tag-life">投资人品性</span>'
NAV='<a href="#s1" class="nav-link">① 四概念</a><a href="#s2" class="nav-link">② 投资vs投机</a><a href="#s3" class="nav-link">③ 能力圈</a><a href="#s4" class="nav-link">④ 品性</a><a href="#s5" class="nav-link">⑤ 普通人</a><a href="#s6" class="nav-link">⑥ 提醒</a><a href="#qa" class="nav-link">⑦ 问答</a>'
SOURCE="李录2019年11月29日北京大学光华管理学院演讲（公开整理）"

RAW = """很高兴五年后有机会重新来到北大光华管理学院的这门价值投资课上与大家分享。今天是美国的感恩节，借此机会我要感谢光华管理学院的姜国华教授和喜马拉雅资本的常劲先生，以及在座的各位同学和价值投资的追求者、支持者，感谢各位这些年来对价值投资在中国的实践的传播与支持。

另外，五年来，我一直对自己在此讲的第一课有点遗憾。那堂课中我们主要讨论了价值投资的基本理论，尤其是否适合中国，但是对价值投资的具体实践讲得不多。事实上，价值投资主要是一门实践的学问，所以今天我主要讲价值投资中的实践问题。我想先讲讲自己理解的价值投资实践的框架，然后留出时间给大家提问。

一、价值投资的四个基本概念

价值投资的基本概念只有四个：

第一，股票是对公司的部分所有权，而不仅仅是可以买卖的一张纸
你买的不是一个交易符号，而是公司生意的一部分。这是最根本的认知起点。

第二，安全边际
投资的本质是对未来进行预测，而我们对未来无法精确预测，只能得到一个概率，所以需要预留安全边际。用明显低于内在价值的价格买入，为不确定性留足缓冲。

第三，市场先生
市场的存在是为了服务你的，不是来指导你的。市场每天给你报价，时而疯狂乐观、时而极度悲观，你可以利用它，但绝不能被它左右情绪、被它指挥决策。

第四，能力圈
投资人需要通过长期的学习建立一个属于自己的能力圈，然后在能力圈范围之内去做投资。不懂不做，只在自己看得懂的地方下注。

这四个概念逻辑简单、清晰，理解起来并不困难。但真正在实践中坚持、做到知行合一的人极少。为什么？因为它违背人性。

二、投资 vs 投机：本质完全不同

股市里从一开始就两类人：投资者和投机者。

• 投资者：预测公司本身的长期表现，赚企业成长、盈利复利的钱。
• 投机者：预测其他投机者的行为、猜股价短期波动，赚博弈的钱。

投资是正和游戏：长期看，经济和优秀企业在增长，所有参与者整体是共赢的，对社会有正向贡献，推动资源有效配置。

投机是零和游戏：扣除交易成本后，长期总和为零。你赚的钱就是别人亏的钱，和赌场本质一样，对社会没有增量价值。

拉长到一生来看，只有像巴菲特这样的价值投资者，能取得持续、大规模、可复制的成功；所有投机者，无论短期多风光，长期记录一定归零。市场大部分时候在征收“无知税”，靠信息剥削、情绪收割、短期博弈生存，这些都不可持续。

三、能力圈：是什么、怎么建、怎么守

1. 能力圈的核心：真懂
真懂一家公司，意味着你能大致判断：
• 它 10 年以后最差会是什么样？
• 它的盈利逻辑、竞争优势（护城河）是否可持续？
• 它的内在价值大概在什么区间？
不是懂一点皮毛、看过财报、听过消息叫懂。懂，是能经得起相反观点最严厉的挑战，仍然确信自己的判断。

我常用一个方法：找身边最有见解、但和你观点相反的人辩论。只有当你发现你的逻辑、证据、理解深度，明显比他更站得住脚时，你才可以说“我大概懂了”。

2. 怎么建立能力圈
• 从兴趣出发：对商业、对生意本身有强烈好奇心，琢磨“它为什么能赚钱、为什么能一直赚钱”。
• 所有者心态：把自己当成公司的主人、长期股东，而不是炒股票的。买完后天天关心它怎么运营、怎么管理、客户怎么看，像对待自己的孩子一样。
• 深度研究、亲力亲为：不只看研报，要实地看、和员工聊、和客户聊、和竞争对手聊。
• 慢慢积累、做减法：能力圈不是越大越好，而是越准、越牢越好。大多数人总在做加法，什么热点都想抓；真正的投资者要不断做减法，只守着自己最确定的一小片天地。
• 对知识诚实：承认自己不懂，不懂的坚决不碰。人最难的是客观、理性，总愿意相信对自己有利的判断，要刻意克服这种天性。

3. 能力圈的边界
• 你不需要懂很多公司，赚钱靠的是懂的东西正确、确定，而不是多。
• 机会来的时候，要敢下重注；没机会时，耐心持有现金，什么都不做。
• 投资投的是确定性，不是可能性。

四、价值投资者必备的品性（比智商、学历更重要）

决定你能不能成为成功的价值投资者，主要不是智商、学历、经历，而是品性。

1. 独立思考（最重要）
• 不盲从共识、不跟风、不看别人怎么操作。
• 你的价值标尺是公司内在价值，不是股价、不是别人的评价。
• 市场共识经常是错的：人人都看好时，价格已透支；人人都悲观时，价值往往被埋没。

2. 客观理性
• 不带情绪分析，不因持仓而扭曲观点，不因涨跌而改变判断。
• 情绪是投资最大的敌人，要把情绪影响降到最低。

3. 极度耐心 + 非常果决
• 平时可以几年不出手，像芒格一样，读几十年《Barron's》，几年才等到一个大机会。
• 机会出现时，要极度果断、敢重仓，不犹豫、不拖延。

4. 对商业极度有兴趣，有金钱意识
• 没事就琢磨生意、商业模式、赚钱逻辑。
• 不是为钱而钱，但对价值、价格、复利、机会成本有本能的敏感。

同时具备这几点，再加上长期学习，才可能成为出色的价值投资者。

五、非专业投资人：如何保护与增加财富

如果你不是职业投资者，给你几个最实用的原则：

1. 没有好机会，持有现金优于盲目投资
现金至少不会亏，比乱投、跟风、投机强太多。

2. 长期投资低成本宽基指数
买能代表整体经济的指数基金（如标普500、沪深300等），长期持有、复利增长，能跑赢绝大多数专业投资者。

3. 如果选管理人：看品行 > 能力圈 > 业绩
• 品行端正、诚实、有价值投资信仰
• 有清晰、可解释的能力圈
• 长期业绩可验证、策略稳定不漂移
• 不和市场博弈、不赚快钱

4. 远离诱惑，远离噪音
• 别被各种短线、热点、杠杆、内幕消息诱惑
• 离金融圈、一线城市越远，有时反而心态越好、干扰越少
• 相信复利，不追求短期暴利

5. 投资自己：知识、健康、家庭
人生最确定、回报最高的复利，是知识、经验、健康、家庭关系。把自己活长、活好、活明白，比什么投资都重要。

六、投资实践的几个关键提醒

• 无压力状态：从一开始就不要把自己放在过大压力下。不要用短期钱、杠杆钱、急用的钱投资。压力会扭曲判断，让人做愚蠢决策。
• 知行合一：价值投资是一种生活方式、一种价值观。你相信什么，就必须怎么做；不能嘴上价值，行为投机。
• 慢即是快：投资不要急。年轻时总想快、总想赚大钱，反而容易摔跟头。慢慢来、守得住、活得久，最终结果反而最好。
• 多赢、双赢：做投资、做人，都按黄金法则来。不剥削、不对赌、不占别人便宜，长期走得最稳。

七、问答环节（精华）

问：卖方分析师转价值投资，怎么切入？
李录：主要是心理转变。卖方是服务、是推荐、是取悦市场；买方是所有者、是判断、是对自己负责。把心态从“服务别人”转到“这是我的公司”，一切就顺了。

问：年轻人做价值投资为什么容易失败？
李录：大多是因为没有真正兴趣，只是想赚快钱。价值投资很枯燥、很孤独、要长期等待，没有发自内心的兴趣，坚持不下来。成功一定是兴趣和能力的结合。

问：怎么判断自己真懂还是假懂？
李录：懂，就是你能清晰回答：这家公司 10 年后最坏情况是什么？它的护城河为什么能持续？相反观点最有力的地方在哪里，你为什么仍然正确？做不到这几点，就是不懂。

问：价值投资最好的学习方法？
李录：1. 自学为主：这门学问是孤独的，讨论多了容易失去客观性。2. 为你最尊敬的人工作：近距离看他怎么思考、怎么决策、怎么做人。3. 用科学方法积累：深度、系统、长期，不投机取巧。

问：企业护城河最重要的来源是什么？
李录：长期看，是行业特性+商业模式；短期看，是人（企业家与组织能力）。优秀行业本身资本回报就高于平均，再配上优秀的人，护城河最宽。

问：您看重的企业家有什么特点？
李录：能把生意本质想透、有长期眼光、对产品和客户极度专注、诚信、有定力，不被短期股价和诱惑带偏。

问：投资和人生、健康的关系？
李录：投资是一辈子的事。巴菲特、芒格成功，很大原因是活得长、心态好、做自己喜欢的事。
• 干热爱的事
• 保持平常心、无压力
• 好的生活习惯、好的家庭
• 待人友善，远离烂人烂事
复利不仅在钱，更在人生本身。

结语

价值投资不只是一套方法，更是一种思维方式、生活态度、道德选择。它要求你诚实、理性、独立、有耐心、有长期主义。这条路很难、很孤独，但走通了，不仅能获得财富，更能获得内心的平静与人生的自由。

希望大家真正做到知行合一，在投资和人生中，都能走得稳、走得远。"""

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

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def bold(s):
    s=re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

SECT_RE=re.compile(r"^(一|二|三|四|五|六|七)[、．.．\s]")
def render(text):
    lines=[l.rstrip() for l in text.split("\n")]
    out=[]
    i=0
    n=len(lines)
    in_qa=False
    sect_num=0
    while i<n:
        line=lines[i].strip()
        if not line:
            i+=1; continue
        if SECT_RE.match(line) or line=="结语":
            sect_num+=1
            if line.startswith("七"):
                aid="qa"
            else:
                aid=f"s{sect_num}"
            out.append(f'<h2 class="section-h2" id="{aid}">{esc(line)}</h2>')
            in_qa = line.startswith("七")
            i+=1; continue
        if in_qa and line.startswith("问") and "：" in line:
            q=line[line.index("：")+1:].strip()
            out.append(f'<div class="qa"><div class="qa-q">问：{bold(esc(q))}</div>')
            # gather answer lines until next 问 or heading
            ans=[]
            i+=1
            while i<n:
                nxt=lines[i].strip()
                if not nxt: i+=1; continue
                if SECT_RE.match(nxt) or nxt=="结语": break
                if nxt.startswith("问") and "：" in nxt: break
                # speaker label
                m=re.match(r"^(李录)[：:]\s*(.*)", nxt)
                if m:
                    ans.append(f'<p><span class="speaker-li">李录：</span>{bold(esc(m.group(1)))}</p>')
                elif nxt.startswith("•"):
                    ans.append(f'<p>· {bold(esc(nxt[1:].strip()))}</p>')
                else:
                    ans.append(f'<p>{bold(esc(nxt))}</p>')
                i+=1
            out.append(f'<div class="qa-a">{"".join(ans)}</div></div>')
            continue
        if line.startswith("•"):
            # group bullets
            grp=[line]
            i+=1
            while i<n and lines[i].strip().startswith("•"):
                grp.append(lines[i].strip()); i+=1
            lis="".join(f"<li>{bold(esc(g[1:].strip()))}</li>" for g in grp)
            out.append(f"<ul class='li-bullets'>{lis}</ul>")
            continue
        out.append(f"<p class='speech-p'>{bold(esc(line))}</p>")
        i+=1
    return "\n".join(out)

body=render(RAW)
html=HEAD.format(css=CSS,title=TITLE,short=SHORT,badge=BADGE,sub=SUB,date=DATE,
                 venue=VENUE,tags=TAGS,nav=NAV,body=body,source=SOURCE)
path=os.path.join(OUT,"li-lu-2019.html")
open(path,"w",encoding="utf-8").write(html)
print("wrote",path,len(html),"bytes; body chars:",len(body))
