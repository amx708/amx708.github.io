# -*- coding: utf-8 -*-
"""生成伯克希尔数据中心 · 银行业投资图谱（42家A股上市银行）。
复用白酒产业链脚本结构：索引页 + 42家详情页 + 方法论文 + 周期 + 回测 + 温度计 + 逐轮买点回报图。
数据口径：财务=2025年年报；估值=2026-07-12行情。42家均已接入行情接口后复权年线绘制回报曲线。
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- 通用 CSS（浅色风，与主页及 11 条产业链统一）----------------
BANK_CSS = """
:root{--bg:#f0f2f5;--soft:#f8fafc;--card:#ffffff;--ink:#1e293b;--mut:#64748b;--line:rgba(0,0,0,.09);--red:#dc2626;--green:#16a34a;--accent:#3b82f6;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;font-size:15px;-webkit-font-smoothing:antialiased}
.nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{max-width:1080px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.nav .brand{color:var(--ink);font-weight:600;font-size:15px;letter-spacing:.3px}
.nav .crumb{color:var(--mut);font-size:12.5px}
.nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:4px 9px;border-radius:6px;transition:.15s}
.nav a:hover{color:var(--accent);background:var(--soft)}
.hero{background:linear-gradient(135deg,#ffffff 0%,#f1f5f9 100%);border-bottom:1px solid var(--line);padding:46px 20px 38px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.hero-in{max-width:1080px;margin:0 auto}
.hero h1{margin:0 0 10px;font-size:29px;font-weight:700;letter-spacing:-.5px;color:#0f172a}
.hero p{margin:5px 0;color:var(--mut);max-width:760px;font-size:14.5px}
.hero .stat{display:flex;gap:40px;margin-top:26px;flex-wrap:wrap}
.hero .stat b{color:var(--accent);font-size:26px;display:block;font-weight:700}
.hero .stat span{font-size:12px;color:var(--mut)}
.wrap{max-width:1080px;margin:0 auto;padding:30px 20px 70px}
.section-title{font-size:18px;font-weight:700;margin:34px 0 16px;padding-left:12px;border-left:3px solid var(--accent);letter-spacing:-.2px;color:var(--ink)}
.filter{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 22px}
.filter button{border:1px solid var(--line);background:var(--card);color:var(--mut);padding:7px 16px;border-radius:8px;cursor:pointer;font-size:13px;transition:.15s}
.filter button:hover{border-color:var(--accent);color:var(--accent)}
.filter button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;transition:.18s;position:relative;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.card:hover{border-color:var(--accent);box-shadow:0 6px 20px rgba(59,130,246,.14)}
.card .top{display:flex;justify-content:space-between;align-items:baseline}
.card h3{margin:0;font-size:16.5px;font-weight:600;color:var(--ink)}
.card .code{font-size:12px;color:var(--mut)}
.card .cat{display:inline-block;font-size:11px;padding:2px 9px;border-radius:6px;background:var(--soft);color:var(--mut);margin:7px 0}
.card .pos{font-size:12.5px;color:var(--mut);min-height:34px;line-height:1.55}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 8px;margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
.kpis div{font-size:11px;color:var(--mut)}
.kpis b{display:block;color:var(--ink);font-size:14px;font-weight:600}
.detail{max-width:920px;margin:0 auto;padding:28px 20px 70px}
.detail .back{color:var(--accent);text-decoration:none;font-size:13px}
.detail>h1{font-weight:700;letter-spacing:-.5px;color:var(--ink)}
.layer{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:10px 0}
.layer h4{margin:0 0 4px;font-size:14px;color:var(--accent);font-weight:600}
.layer p{margin:0;font-size:13.5px;color:var(--mut);line-height:1.65}
.snap{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:16px 0}
.snap div{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:12px 10px;text-align:center}
.snap b{display:block;font-size:19px;color:var(--accent);font-weight:700}
.snap span{font-size:11px;color:var(--mut)}
.deep{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 18px 14px;margin:14px 0}
.deep h4{margin:0 0 6px;font-size:14px;color:var(--accent);font-weight:600}
.deep-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.deep-item{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:var(--soft)}
.deep-item h4{margin:0 0 6px;font-size:14px;color:var(--accent);font-weight:600}
.deep-item p{margin:0;font-size:13px;color:var(--ink);line-height:1.65}
.deep ul{margin:6px 0;padding-left:18px;font-size:13px;color:var(--ink);line-height:1.6}
.timeline{border-left:2px solid var(--line);padding-left:16px;margin:8px 0 8px 6px}
.timeline div{position:relative;font-size:13px;color:var(--ink);margin:8px 0;padding-left:2px}
.timeline div::before{content:'';position:absolute;left:-21px;top:7px;width:8px;height:8px;border-radius:50%;background:var(--accent)}
.note{background:var(--soft);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:12px 16px;margin:14px 0;font-size:13px;color:var(--mut);line-height:1.65}
.note a{color:var(--accent)}
.extend{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:14px}
.extend a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;text-decoration:none;color:var(--ink);transition:.18s;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.extend a:hover{border-color:var(--accent);box-shadow:0 6px 18px rgba(59,130,246,.14)}
.extend b{color:var(--accent);display:block;margin-bottom:5px;font-weight:600}
.extend span{font-size:12.5px;color:var(--mut);line-height:1.55}
.tbl{width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.tbl th,.tbl td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:center}
.tbl th{background:var(--soft);color:var(--ink);font-weight:600;border-bottom:2px solid var(--line)}
.tbl tr:hover td{background:var(--soft)}
.tag{display:inline-block;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600}
.tag.low{background:rgba(220,38,38,.12);color:var(--red)}
.tag.mid{background:rgba(59,130,246,.14);color:#2563eb}
.tag.high{background:rgba(22,163,74,.14);color:var(--green)}
.thermo{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}
.thermo .nm{width:130px;font-weight:600;font-size:14px;color:var(--ink)}
.thermo .bar{flex:1;height:10px;background:linear-gradient(90deg,#f87171,#e8b84b,#34d399);border-radius:6px;position:relative;min-width:160px;opacity:.85}
.thermo .dot{position:absolute;top:-4px;width:18px;height:18px;border-radius:50%;background:var(--card);border:3px solid var(--accent);transform:translateX(-50%);box-shadow:0 1px 3px rgba(0,0,0,.3)}
.thermo .v{font-size:12.5px;color:var(--mut);width:160px}
footer{background:var(--soft);color:var(--mut);text-align:center;padding:26px 20px;font-size:12.5px;border-top:1px solid var(--line)}
.svgbox{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:16px 0;overflow-x:auto}
.guide{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:14px 0}
.guide h4{margin:0 0 8px;color:var(--accent);font-weight:600}
.guide p,.guide li{font-size:13.5px;color:var(--ink);line-height:1.7}
@media(max-width:600px){.grid{grid-template-columns:1fr}.hero h1{font-size:23px}.hero .stat{gap:24px}.thermo .nm{width:100px}}
/* ---- 产业链三层流 ---- */
.flow3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:18px 0}
.flow3 .stage{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 16px 10px;position:relative;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.flow3 .stage .sno{position:absolute;top:-12px;left:16px;background:var(--accent);color:#fff;font-size:12px;font-weight:600;padding:3px 11px;border-radius:20px}
.flow3 .stage h4{margin:6px 0 2px;font-size:15px;color:var(--accent);font-weight:600}
.flow3 .stage .tagline{font-size:12px;color:var(--mut);margin-bottom:10px;line-height:1.5}
.node{background:var(--soft);border:1px solid var(--line);border-radius:9px;padding:10px 12px;margin:8px 0}
.node b{display:block;font-size:13.5px;color:var(--ink)}
.node span{font-size:12px;color:var(--mut);line-height:1.5}
.flow-cap{text-align:center;font-size:12.5px;color:var(--mut);margin:2px 0 18px}
.flow-cap b{color:var(--accent)}
@media(max-width:768px){.flow3{grid-template-columns:1fr}}
/* ---- 对比工具 ---- */
.cmp-ctrl{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:14px 0;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.cmp-ctrl .bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.cmp-ctrl input[type=text]{flex:1;min-width:180px;border:1px solid var(--line);border-radius:8px;padding:9px 12px;font-size:13px;outline:none;background:var(--bg);color:var(--ink)}
.cmp-ctrl input[type=text]:focus{border-color:var(--accent)}
.cmp-ctrl .fbtn{border:1px solid var(--line);background:var(--soft);color:var(--mut);padding:7px 14px;border-radius:8px;cursor:pointer;font-size:13px}
.cmp-ctrl .fbtn.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.cmp-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;max-height:230px;overflow:auto;padding:4px}
.cmp-item{display:flex;align-items:center;gap:8px;font-size:13px;padding:6px 9px;border:1px solid var(--line);border-radius:8px;cursor:pointer;transition:.15s}
.cmp-item:hover{border-color:var(--accent)}
.cmp-item input{accent-color:var(--accent);width:15px;height:15px}
.cmp-item .cc{font-size:11px;color:var(--mut)}
.cmp-sel{font-size:12.5px;color:var(--mut);margin:6px 0}
.cmp-good{color:var(--green);font-weight:600}
.cmp-bad{color:var(--red);font-weight:600}
"""


def header(title, crumb):
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{BANK_CSS}</style></head><body>
<div class="nav"><div class="nav-in">
<div class="brand">伯克希尔数据中心</div><div class="crumb">{crumb}</div>
<a href="berkshire-standalone.html">数据中心</a>
<a href="berkshire-bank-chains.html">银行</a>
<a href="berkshire-baijiu-chains.html">白酒</a>
<a href="berkshire-ai-chains.html">AI</a>
<a href="berkshire-robot-chains.html">机器人</a>
</div></div>"""


def footer():
    return """<footer>伯克希尔数据中心 · 银行业投资图谱 ｜ 数据口径：财务=2025年年报（最新可得年报，2026年中报预计8月后披露），估值=2026-07-12行情 ｜ 内容仅供研究参考，不构成投资建议</footer></body></html>"""


# ---------------- 业务条线框架（5层）模板 ----------------
def biz(cat, special=None):
    base = {
        "零售": "个人存贷款、信用卡、住房按揭与消费信贷，依托网点与App触达海量零售客户。",
        "对公": "企业贷款、机构金融、普惠金融与供应链金融，服务实体经济融资需求。",
        "同业": "同业拆借、票据贴现、金融市场投资与债券交易，管理流动性与利率风险。",
        "财富": "理财子公司产品、私人银行、代理代销与托管，沉淀中收与AUM。",
        "投行": "债券承销、并购顾问、交易银行与资本市场服务，对接直接融资。",
    }
    if cat == "国有大行":
        base.update({"零售": "全国网点+手机银行覆盖最广的零售客群，住房按揭与借记卡基础雄厚。",
                     "对公": "央企、地方国企与重大项目主力融资行，对公存款成本低。"})
    elif cat == "股份行":
        base.update({"零售": "差异化零售策略（如招行零售之王、平安银行零售转型），信用卡与财富管理见长。",
                     "对公": "股份制灵活机制，深耕民企、投行与同业链条。"})
    elif cat == "城商行":
        base.update({"零售": "立足本地市民与公积金、市民卡场景，区域零售客群稳定。",
                     "对公": "地方平台、城投与本土企业主力行，区域深耕能力强。"})
    elif cat == "农商行":
        base.update({"零售": "县域农户、小微与乡镇居民，存款扎根本地、成本极低。",
                     "对公": "县域中小微、三农与个体工商户，接地气的普惠金融服务。"})
    if special:
        base.update(special)
    return base


# ---------------- 42家数据 ----------------
company_data = [
    # ===== 国有大行 6 =====
    dict(slug="icbc", name="工商银行", code="601398", cat="国有大行",
         pos="宇宙行，资产规模全球第一，综合化经营标杆。",
         business=biz("国有大行", {"对公": "服务央企与重大项目的主力行，对公存款成本全行业最低。",
                                "财富": "工银理财+私行AUM领先，中收贡献稳定。"}),
         snapshot=dict(rev=8013.95, profit=3685.62, npl=1.31, cpr=213.60, nim=1.28, roe=9.45, pb=0.67, div=4.23, mcap=26124.58)),
    dict(slug="ccb", name="建设银行", code="601939", cat="国有大行",
         pos="住房金融领先，零售与大财富转型扎实。",
         business=biz("国有大行", {"零售": "住房按揭传统强项，建信理财与私行稳步扩张。"}),
         snapshot=dict(rev=7408.71, profit=3389.06, npl=1.31, cpr=233.15, nim=1.34, roe=10.04, pb=0.74, div=3.90, mcap=26238.52)),
    dict(slug="abc", name="农业银行", code="601288", cat="国有大行",
         pos="县域金融护城河，存款成本优势突出。",
         business=biz("国有大行", {"零售": "县域网点数量第一，农户与县域存款成本低廉。",
                                "对公": "服务三农与乡村振兴的政策性定位叠加市场化经营。"}),
         snapshot=dict(rev=7253.06, profit=2910.41, npl=1.27, cpr=292.55, nim=1.28, roe=10.16, pb=0.78, div=4.00, mcap=21803.94)),
    dict(slug="boc", name="中国银行", code="601988", cat="国有大行",
         pos="国际化程度最高，外汇与跨境业务龙头。",
         business=biz("国有大行", {"同业": "海外网点最广，外币资金与外汇交易优势明显。",
                                "投行": "跨境结算、外币债券承销与离岸金融领先。"}),
         snapshot=dict(rev=6599.00, profit=2430.21, npl=1.23, cpr=200.37, nim=1.26, roe=8.94, pb=0.69, div=3.91, mcap=18656.10)),
    dict(slug="bocom", name="交通银行", code="601328", cat="国有大行",
         pos="总行在沪的综合性大行，长三角区位优势。",
         business=biz("国有大行"),
         snapshot=dict(rev=2650.71, profit=956.22, npl=1.28, cpr=208.38, nim=1.20, roe=8.38, pb=0.51, div=4.91, mcap=5840.85)),
    dict(slug="psbc", name="邮储银行", code="601658", cat="国有大行",
         pos="网点下沉至县域乡镇，存款成本全行业最低。",
         business=biz("国有大行", {"零售": "近4万个网点覆盖城乡，个人存款占比极高、成本最低。",
                                "对公": "依托邮政网络做小微与三农，对公业务仍在补强。"}),
         snapshot=dict(rev=3557.28, profit=874.04, npl=0.95, cpr=227.94, nim=1.66, roe=8.67, pb=0.59, div=4.30, mcap=6052.79)),
    # ===== 股份行 9 =====
    dict(slug="cmb", name="招商银行", code="600036", cat="股份行",
         pos="零售之王，财富管理与高拨备的标杆股份行。",
         business=biz("股份行", {"零售": "零售AUM与私行规模股份行第一，'牛奶咖啡'式服务口碑。",
                              "财富": "招银理财+代销能力行业领先，中收占比最高。"}),
         snapshot=dict(rev=3375.32, profit=1501.81, npl=0.94, cpr=391.79, nim=1.87, roe=13.44, pb=0.84, div=5.50, mcap=9301.08)),
    dict(slug="citic", name="中信银行", code="601998", cat="股份行",
         pos="对公与投行见长，集团协同（中信集团）优势。",
         business=biz("股份行", {"投行": "债券承销与交易银行领先，集团内产融协同。"}),
         snapshot=dict(rev=2124.75, profit=706.18, npl=1.15, cpr=203.61, nim=1.63, roe=9.39, pb=0.54, div=5.33, mcap=3978.63)),
    dict(slug="spdb", name="浦发银行", code="600000", cat="股份行",
         pos="上海起家的老牌股份行，对公底蕴深。",
         business=biz("股份行"),
         snapshot=dict(rev=1739.64, profit=500.17, npl=1.26, cpr=200.72, nim=1.42, roe=6.76, pb=0.40, div=4.11, mcap=3017.51)),
    dict(slug="indy", name="兴业银行", code="601166", cat="股份行",
         pos="同业之王，绿色金融与商行+投行战略。",
         business=biz("股份行", {"同业": "同业业务与金融市场投资传统强项，银银平台领先。",
                              "投行": "绿色金融表内外规模行业前列。"}),
         snapshot=dict(rev=2127.41, profit=774.69, npl=1.08, cpr=228.41, nim=1.71, roe=9.15, pb=0.45, div=6.15, mcap=3667.52)),
    dict(slug="cmbc", name="民生银行", code="600016", cat="股份行",
         pos="民营银行代表，小微金融开创者。",
         business=biz("股份行", {"零售": "小微金融'商贷通'开创者，客群以民企为主。"}),
         snapshot=dict(rev=1428.65, profit=305.63, npl=1.49, cpr=142.04, nim=1.40, roe=4.93, pb=0.26, div=5.66, mcap=1462.33)),
    dict(slug="ceb", name="光大银行", code="601818", cat="股份行",
         pos="集团协同（光大集团）的综合股份行。",
         business=biz("股份行"),
         snapshot=dict(rev=1263.11, profit=388.26, npl=1.27, cpr=174.14, nim=1.40, roe=7.00, pb=0.36, div=6.21, mcap=1808.02)),
    dict(slug="hxb", name="华夏银行", code="600015", cat="股份行",
         pos="首都老牌股份行，对公与基建见长。",
         business=biz("股份行"),
         snapshot=dict(rev=919.14, profit=272.00, npl=1.55, cpr=143.30, nim=1.56, roe=8.32, pb=0.34, div=6.30, mcap=1079.03)),
    dict(slug="pab", name="平安银行", code="000001", cat="股份行",
         pos="平安集团赋能，零售转型深化。",
         business=biz("股份行", {"零售": "依托平安集团客群做零售转型，信用卡与汽融见长。",
                              "财富": "代理代销与私行借助集团综合金融。"}),
         snapshot=dict(rev=1314.42, profit=426.33, npl=1.05, cpr=220.88, nim=1.78, roe=9.15, pb=0.44, div=5.70, mcap=2027.92)),
    dict(slug="czb", name="浙商银行", code="601916", cat="股份行",
         pos="最年轻的股份行，平台化服务战略。",
         business=biz("股份行", {"对公": "聚焦浙江与长三角，平台化场景撮合融资。"}),
         snapshot=dict(rev=625.14, profit=129.31, npl=1.36, cpr=155.37, nim=1.60, roe=6.80, pb=0.42, div=4.76, mcap=755.28)),
    # ===== 城商行 17 =====
    dict(slug="bobj", name="北京银行", code="601169", cat="城商行",
         pos="资产规模第一的城商行，扎根首都。",
         business=biz("城商行", {"对公": "北京地区财政、国企与机构客户深厚。"}),
         snapshot=dict(rev=680.36, profit=200.86, npl=1.29, cpr=200.21, nim=1.27, roe=6.11, pb=0.38, div=3.93, mcap=1076.18)),
    dict(slug="njcb", name="南京银行", code="601009", cat="城商行",
         pos="债券特色与高拨备的优质城商行。",
         business=biz("城商行", {"同业": "债券投资与交易能力突出，金融市场业务强。"}),
         snapshot=dict(rev=555.42, profit=218.07, npl=0.83, cpr=313.62, nim=1.82, roe=12.05, pb=0.71, div=4.60, mcap=1332.79)),
    dict(slug="nib", name="宁波银行", code="002142", cat="城商行",
         pos="高ROE标杆，小微+零售+财资强。",
         business=biz("城商行", {"零售": "消费贷与信用卡深耕浙江，客户分层精细。",
                              "对公": "中小微'+进出口企业服务，不良控制优异。"}),
         snapshot=dict(rev=719.69, profit=293.33, npl=0.76, cpr=373.16, nim=1.74, roe=13.11, pb=0.88, div=3.87, mcap=2049.09)),
    dict(slug="shb", name="上海银行", code="601229", cat="城商行",
         pos="立足上海的综合性城商行。",
         business=biz("城商行"),
         snapshot=dict(rev=547.61, profit=241.93, npl=1.18, cpr=244.94, nim=1.16, roe=9.44, pb=0.51, div=5.76, mcap=1283.07)),
    dict(slug="jsb", name="江苏银行", code="600919", cat="城商行",
         pos="资产规模领先的优质城商行，区域红利。",
         business=biz("城商行", {"对公": "江苏制造业与外贸企业客群扎实，信贷增速快。"}),
         snapshot=dict(rev=879.42, profit=345.01, npl=0.84, cpr=322.98, nim=1.54, roe=10.21, pb=0.78, div=4.83, mcap=2071.86)),
    dict(slug="hzb", name="杭州银行", code="600926", cat="城商行",
         pos="高拨备、高ROE的精品城商行。",
         business=biz("城商行", {"财富": "理财与代销能力在城商行中领先，中收占比高。"}),
         snapshot=dict(rev=387.99, profit=190.29, npl=0.76, cpr=502.24, nim=1.36, roe=14.65, pb=0.83, div=4.12, mcap=1160.57)),
    dict(slug="cdb", name="成都银行", code="601838", cat="城商行",
         pos="成渝经济圈红利，高ROE低不良。",
         business=biz("城商行", {"对公": "成渝地区基建与产业客群，资产质量优异。"}),
         snapshot=dict(rev=236.03, profit=132.83, npl=0.68, cpr=426.17, nim=1.53, roe=15.39, pb=0.86, div=4.90, mcap=788.35)),
    dict(slug="csb", name="长沙银行", code="601577", cat="城商行",
         pos="湖南区域龙头城商行。", business=biz("城商行"),
         snapshot=dict(rev=254.71, profit=81.08, npl=1.15, cpr=280.86, nim=1.62, roe=11.24, pb=0.52, div=4.53, mcap=382.05)),
    dict(slug="cqb", name="重庆银行", code="601963", cat="城商行",
         pos="成渝双城区域的老牌城商行。", business=biz("城商行"),
         snapshot=dict(rev=151.13, profit=56.54, npl=1.14, cpr=245.58, nim=1.39, roe=9.50, pb=0.63, div=4.20, mcap=400.65)),
    dict(slug="qdb", name="青岛银行", code="002948", cat="城商行",
         pos="山东半岛区域城商行。", business=biz("城商行"),
         snapshot=dict(rev=145.73, profit=51.88, npl=0.97, cpr=292.30, nim=1.66, roe=12.68, pb=0.81, div=3.20, mcap=330.60)),
    dict(slug="zzb", name="郑州银行", code="002936", cat="城商行",
         pos="中原地区城商行，资产质量承压。",
         business=biz("城商行", {"对公": "河南区域对公与城投敞口较高，不良率偏高。"}),
         snapshot=dict(rev=129.21, profit=18.95, npl=1.71, cpr=185.81, nim=1.61, roe=3.44, pb=0.35, div=1.13, mcap=160.93)),
    dict(slug="szb", name="苏州银行", code="002966", cat="城商行",
         pos="制造业强市苏州的优质城商行。", business=biz("城商行", {"对公": "苏州制造业与外贸企业客群优质。"}),
         snapshot=dict(rev=123.56, profit=53.48, npl=0.82, cpr=418.60, nim=1.33, roe=10.66, pb=0.70, div=5.03, mcap=364.36)),
    dict(slug="xab", name="西安银行", code="600928", cat="城商行",
         pos="西北区域城商行。", business=biz("城商行"),
         snapshot=dict(rev=99.66, profit=26.50, npl=1.65, cpr=214.62, nim=1.85, roe=7.74, pb=0.43, div=2.85, mcap=156.00)),
    dict(slug="xmb", name="厦门银行", code="601187", cat="城商行",
         pos="海峡西岸区域城商行。", business=biz("城商行"),
         snapshot=dict(rev=58.60, profit=26.35, npl=0.77, cpr=312.71, nim=1.09, roe=9.05, pb=0.69, div=4.21, mcap=187.91)),
    dict(slug="qlb", name="齐鲁银行", code="601665", cat="城商行",
         pos="山东省级城商行。", business=biz("城商行"),
         snapshot=dict(rev=131.35, profit=57.13, npl=1.05, cpr=355.91, nim=1.53, roe=12.17, pb=0.74, div=3.79, mcap=374.15)),
    dict(slug="gyb", name="贵阳银行", code="601997", cat="城商行",
         pos="贵州区域城商行，资产质量承压。", business=biz("城商行"),
         snapshot=dict(rev=129.99, profit=52.49, npl=1.59, cpr=235.62, nim=1.58, roe=7.97, pb=0.33, div=4.89, mcap=216.81)),
    dict(slug="lzb", name="兰州银行", code="001227", cat="城商行",
         pos="甘肃区域城商行。", business=biz("城商行"),
         snapshot=dict(rev=77.95, profit=18.65, npl=1.82, cpr=198.38, nim=1.37, roe=5.36, pb=0.39, div=4.76, mcap=120.00)),
    # ===== 农商行 10 =====
    dict(slug="cqrc", name="渝农商行", code="601077", cat="农商行",
         pos="资产规模第一的农商行（重庆）。", business=biz("农商行"),
         snapshot=dict(rev=286.48, profit=121.28, npl=1.08, cpr=367.26, nim=1.60, roe=9.18, pb=0.53, div=5.09, mcap=715.49)),
    dict(slug="qrc", name="青农商行", code="002958", cat="农商行",
         pos="山东青岛的农商行。", business=biz("农商行"),
         snapshot=dict(rev=100.27, profit=31.28, npl=1.75, cpr=261.01, nim=1.60, roe=7.94, pb=0.42, div=4.30, mcap=155.00)),
    dict(slug="changshu", name="常熟银行", code="601128", cat="农商行",
         pos="小微金融标杆，净息差最高的上市银行之一。",
         business=biz("农商行", {"零售": "小微+村镇银行模式，'常银微贷'风控成熟。"}),
         snapshot=dict(rev=116.19, profit=42.19, npl=0.76, cpr=451.25, nim=2.53, roe=14.05, pb=0.70, div=4.06, mcap=220.71)),
    dict(slug="zijin", name="紫金银行", code="601860", cat="农商行",
         pos="南京地区的农商行。", business=biz("农商行"),
         snapshot=dict(rev=41.18, profit=12.44, npl=1.35, cpr=180.09, nim=1.13, roe=6.17, pb=0.45, div=4.02, mcap=91.16)),
    dict(slug="wuxi", name="无锡银行", code="600908", cat="农商行",
         pos="无锡地区的农商行。", business=biz("农商行"),
         snapshot=dict(rev=48.19, profit=23.09, npl=0.77, cpr=414.91, nim=1.35, roe=10.05, pb=0.50, div=4.63, mcap=113.68)),
    dict(slug="zjg", name="张家港行", code="002839", cat="农商行",
         pos="张家港地区的农商行。", business=biz("农商行"),
         snapshot=dict(rev=47.47, profit=19.79, npl=0.94, cpr=328.87, nim=1.39, roe=10.36, pb=0.53, div=5.38, mcap=99.97)),
    dict(slug="sunong", name="苏农银行", code="603323", cat="农商行",
         pos="苏州吴江地区的农商行。", business=biz("农商行"),
         snapshot=dict(rev=42.13, profit=20.43, npl=0.88, cpr=370.17, nim=1.41, roe=10.84, pb=0.47, div=4.73, mcap=89.70)),
    dict(slug="jiangyin", name="江阴银行", code="002807", cat="农商行",
         pos="江阴地区的农商行。", business=biz("农商行"),
         snapshot=dict(rev=41.25, profit=20.49, npl=0.82, cpr=329.98, nim=1.60, roe=10.71, pb=0.53, div=5.18, mcap=104.51)),
    dict(slug="ruifeng", name="瑞丰银行", code="601528", cat="农商行",
         pos="绍兴地区的农商行。", business=biz("农商行"),
         snapshot=dict(rev=44.08, profit=19.66, npl=0.99, cpr=326.51, nim=1.50, roe=10.20, pb=0.45, div=4.61, mcap=89.47)),
    dict(slug="shnc", name="沪农商行", code="601825", cat="农商行",
         pos="上海地区的农商行，规模居前。", business=biz("农商行"),
         snapshot=dict(rev=258.70, profit=123.13, npl=0.96, cpr=328.87, nim=1.37, roe=9.74, pb=0.57, div=5.68, mcap=738.76)),
]

# ---------------- 重点解析（国有大行6 + 招行 + 特色农商行3）----------------
DEEP_DATA = {
    "icbc": dict(
        asset_quality="不良率1.31%保持行业低位，拨备覆盖率213.6%安全垫充足；关注类贷款占比约1.8%，逾期贷款与不良偏离度控制在100%以内。",
        spread="净息差1.28%，在让利实体与LPR下行周期中稳中有压，得益于低存款成本（活期占比高）部分对冲。",
        capital="核心一级资本充足率约13.5%（资本厚度居全球大行前列），支撑信贷稳健扩张与分红。",
        valuation="PB约0.67x（破净），股息率约4.2%；2024-2025高股息行情中估值从0.5x修复至0.7x附近。",
        latest="2025年营收超8000亿、净利3686亿，拟中期+末期双分红；数字化转型（手机银行月活行业第一）持续推进。",
        news=["2023 高股息策略升温，国有大行率先破净修复", "2024 监管引导中期分红，工行首次实施中期派息",
              "2024 险资与ETF增持国有大行", "2025 财政部注资国有大行补充核心一级资本",
              "2026 中特估+红利行情延续，PB回到0.7x附近"]),
    "ccb": dict(
        asset_quality="不良率1.31%，拨备覆盖率233%优于行业；住房按揭不良率虽略升仍可控。",
        spread="净息差1.34%，存款成本管控较好，零售AUM沉淀降低负债成本。",
        capital="核心一级资本充足率约13.8%，资本实力雄厚。",
        valuation="PB约0.74x，股息率约3.9%；估值在国有大行中相对较高（零售属性溢价）。",
        latest="2025年净利3389亿，住房金融与理财稳健；参与房企纾困与保交楼配套融资。",
        news=["2023 房地产风险暴露，建行加大保交楼支持", "2024 中期分红落地",
              "2025 财政部注资补充资本", "2026 红利行情中PB修复至0.74x"]),
    "abc": dict(
        asset_quality="不良率1.27%，拨备覆盖率292.6%领先大行；县域金融不良率低于全行平均。",
        spread="净息差1.28%，县域存款成本极低（个人存款占比高）形成护城河。",
        capital="核心一级资本充足率约12.0%（注资后提升）。",
        valuation="PB约0.78x，股息率约4.0%；县域护城河获估值认可。",
        latest="2025年净利2910亿，县域存款优势延续；'三农'与乡村振兴贷款增速高于平均。",
        news=["2023 县域金融护城河受关注", "2024 中期分红", "2025 财政部注资", "2026 PB居大行之首约0.78x"]),
    "boc": dict(
        asset_quality="不良率1.23%为大行最低，拨备覆盖率200%。",
        spread="净息差1.26%，外币资产受美联储高利率带动，部分对冲人民币息差压力。",
        capital="核心一级资本充足率约12.5%。",
        valuation="PB约0.69x，股息率约3.9%；国际化属性在人民币贬值周期有对冲价值。",
        latest="2025年净利2430亿，海外业务与外汇交易贡献提升；一带一路沿线布局深化。",
        news=["2023 美联储加息带动外币息差", "2024 中期分红", "2025 注资", "2026 跨境金融回暖"]),
    "bocom": dict(
        asset_quality="不良率1.28%，拨备覆盖率208%。",
        spread="净息差1.20%为大行偏低，负债成本有待优化。",
        capital="核心一级资本充足率约10.5%（注资后提升）。",
        valuation="PB约0.51x为大行最低，股息率约4.9%；估值修复空间大但弹性弱。",
        latest="2025年净利956亿，长三角一体化与金融科技投入加大。",
        news=["2023 估值跌至0.4x历史极低", "2024 中期分红", "2025 注资", "2026 PB修复至0.51x"]),
    "psbc": dict(
        asset_quality="不良率0.95%为大行最优，拨备覆盖率228%。",
        spread="净息差1.66%为大行最高，县域存款成本极低是核心优势。",
        capital="核心一级资本充足率约10.0%（注资后提升）。",
        valuation="PB约0.59x，股息率约4.3%；高息差+低不良但资本与零售变现仍在补强。",
        latest="2025年净利874亿，代理保险与财富管理借助邮政网络下沉。",
        news=["2023 存款成本优势凸显", "2024 中期分红", "2025 注资", "2026 县域零售转型加速"]),
    "cmb": dict(
        asset_quality="不良率0.94%股份行最优，拨备覆盖率391.8%极厚；关注类1.2%左右，逾期偏离度<90%。",
        spread="净息差1.87%股份行最高，零售负债成本优势+财富中收平滑息差压力。",
        capital="核心一级资本充足率约14.5%，资本充裕支撑回购与分红。",
        valuation="PB约0.84x（股份行最高），股息率约5.5%；零售溢价显著但亦受地产敞口担忧压制。",
        latest="2025年营收3375亿、净利1502亿；财富管理AUM领先，地产风险持续出清。",
        news=["2023 地产风险拖累估值至0.7x", "2024 中期分红+提升分红比例",
              "2025 行长变更、基本面企稳", "2026 估值修复至0.84x，股息率重回5.5%"]),
    "changshu": dict(
        asset_quality="不良率0.76%为农商行最优，拨备覆盖率451%极厚；小微贷款单户金额小、分散度高，风险高度分散，抗单点违约能力强。",
        spread="净息差2.53%为全部A股上市银行最高，源于'常银微贷'小微高定价、村镇银行下沉与低成本活期存款，是最纯粹的高息差成长样本。",
        capital="核心一级资本充足率约10%，可转债转股与内生利润补充资本，支撑异地村镇银行并表扩张。",
        valuation="PB约0.70x，股息率约4.1%；因高成长+全行业最高息差，长期在农商行中享受估值溢价。",
        latest="2025年营收116亿、净利42亿；异地村镇银行并表与小微投放延续双位数增长，是价值投资者眼中'小而美'的样本。",
        news=["2019 村镇银行'投管行'模式跑通", "2022 息差逆势走阔受关注",
              "2024 高股息+高成长双属性被资金重估", "2026 PB回到0.7x、仍是农商行成长标杆"]),
    "sunong": dict(
        asset_quality="不良率0.88%，拨备覆盖率370%充足；深耕苏州吴江制造业与小微客群，资产质量长期稳健。",
        spread="净息差1.41%，区域同业竞争激烈致息差承压，靠规模扩张与中收增长部分对冲。",
        capital="核心一级资本充足率稳健，可转债补充资本；异地分支与投行业务贡献增量。",
        valuation="PB约0.47x破净较深，股息率约4.7%；估值处农商行偏低区，具红利+修复双重弹性。",
        latest="2025年营收42亿、净利20亿；吴江制造业景气与异地扩张是主要增长看点。",
        news=["2018 更名'苏农银行'突出区域属性", "2021 异地分行布局提速",
              "2024 破净+高股息进入红利视野", "2026 PB约0.47x处低估区"]),
    "zjg": dict(
        asset_quality="不良率0.94%，拨备覆盖率329%较为充足；以张家港本地小微与个体工商户为主，风险分散、区域经济外向型活跃。",
        spread="净息差1.39%，处农商行中游；小微定价能力与存款成本控制决定息差韧性。",
        capital="核心一级资本充足率满足监管要求，转债与利润留存补充资本。",
        valuation="PB约0.53x，股息率约5.4%在农商行中偏高；低估值+高分红是主要吸引力。",
        latest="2025年营收47亿、净利20亿；港口外贸经济与小微投放支撑基本面。",
        news=["2017 上市成为'农商第一股'之一", "2021 转债发行补充资本",
              "2024 高股息属性受红利资金关注", "2026 PB约0.53x、股息率5.4%"]),
}

# ---------------- 后复权价（回报图用）：全42家，行情接口 hfq 年线收盘价 ----------------
# 数据源：腾讯自选股行情接口（westock-data，kline --period year --fq hfq），采集于 2026-07-12。
# 后复权价含历次分红再投资累积，绝对值可能远高于现价（如招行/平安），回报图按基准年=100 归一化不受影响。
HIST_PRICE = {
    # 国有大行
    "icbc": dict(prices=[6.37, 7.81, 8.03, 7.94, 11.27, 12.8, 12.35], note="2006-10上市 · 后复权"),
    "ccb": dict(prices=[8.47, 9.31, 9.88, 9.92, 14.13, 15.28, 16.08], note="2007-09上市 · 后复权"),
    "abc": dict(prices=[4.23, 4.82, 4.71, 4.87, 7.76, 10.46, 9.14], note="2010-07上市 · 后复权"),
    "boc": dict(prices=[5.48, 5.66, 5.6, 6.04, 9.14, 9.77, 9.96], note="2006-07上市 · 后复权"),
    "bocom": dict(prices=[9.36, 9.47, 8.6, 9.77, 14.54, 14.56, 13.96], note="2007-05上市 · 后复权"),
    "psbc": dict(prices=[None, None, 4.99, 5.29, 6.87, 6.9, 6.61], note="2019-12上市 · 后复权"),
    # 股份行
    "cmb": dict(prices=[65.52, 110.37, 191.49, 176.29, 198.62, 217.26, 204.81], note="2002-04上市 · 后复权"),
    "citic": dict(prices=[10.04, 7.64, 7.8, 8.31, 11.71, 13.0, 12.57], note="2007-04上市 · 后复权"),
    "spdb": dict(prices=[106.72, 106.47, 113.59, 100.64, 131.95, 153.91, 124.92], note="1999-11上市 · 后复权"),
    "indy": dict(prices=[55.42, 58.27, 82.15, 77.48, 89.77, 99.35, 90.73], note="2007-02上市 · 后复权"),
    "cmbc": dict(prices=[175.05, 129.4, 132.68, 109.24, 131.19, 129.38, 121.65], note="2000-12上市 · 后复权"),
    "ceb": dict(prices=[5.34, 4.81, 5.48, 4.97, 6.13, 5.94, 5.62], note="2010-08上市 · 后复权"),
    "hxb": dict(prices=[30.98, 27.91, 25.82, 24.59, 35.06, 32.91, 32.94], note="2003-09上市 · 后复权"),
    "pab": dict(prices=[1653.73, 1491.5, 3045.48, 2176.59, 2144.98, 2191.34, 2101.02], note="1991-04上市（深发展）· 后复权"),
    "czb": dict(prices=[None, None, 4.32, 3.34, 3.99, 4.36, 4.15], note="2019-11上市 · 后复权"),
    # 城商行
    "bobj": dict(prices=[17.33, 17.53, 17.08, 17.27, 23.41, 22.54, 21.79], note="2007-09上市 · 后复权"),
    "njcb": dict(prices=[23.94, 30.19, 39.98, 53.0, 59.7, 64.94, 62.63], note="2007-07上市 · 后复权"),
    "nib": dict(prices=[17.38, 28.99, 60.22, 59.28, 47.21, 55.75, 60.22], note="2007-07上市 · 后复权"),
    "shb": dict(prices=[None, 21.52, 21.46, 18.79, 29.15, 32.63, 30.34], note="2016-11上市 · 后复权"),
    "jsb": dict(prices=[None, 6.33, 6.68, 9.94, 14.4, 15.81, 17.4], note="2016-08上市 · 后复权"),
    "hzb": dict(prices=[None, 15.22, 31.14, 28.9, 34.43, 37.04, 37.31], note="2016-10上市 · 后复权"),
    "cdb": dict(prices=[None, 8.33, 11.72, 17.44, 20.91, 20.82, 23.7], note="2018-01上市 · 后复权"),
    "csb": dict(prices=[None, 8.52, 10.12, 8.03, 10.89, 12.32, 11.57], note="2018-09上市 · 后复权"),
    "cqb": dict(prices=[None, None, None, 7.54, 10.85, 12.81, 12.22], note="2021-02上市 · 后复权"),
    "qdb": dict(prices=[None, None, 6.33, 4.19, 5.27, 6.25, 7.6], note="2019-01上市 · 后复权"),
    "zzb": dict(prices=[None, 5.07, 5.16, 3.09, 3.05, 2.85, 2.53], note="2018-09上市 · 后复权"),
    "szb": dict(prices=[None, None, 7.88, 9.28, 10.65, 11.3, 10.4], note="2019-08上市 · 后复权"),
    "xab": dict(prices=[None, None, 5.91, 4.25, 4.56, 4.75, 4.58], note="2019-03上市 · 后复权"),
    "xmb": dict(prices=[None, None, 13.2, 6.16, 6.82, 8.82, 8.67], note="2020-10上市 · 后复权"),
    "qlb": dict(prices=[None, None, None, 4.53, 6.36, 6.78, 7.22], note="2021-06上市 · 后复权"),
    "gyb": dict(prices=[None, 11.27, 12.55, 9.95, 11.49, 11.71, 11.29], note="2016-08上市 · 后复权"),
    "lzb": dict(prices=[None, None, None, 3.87, 2.78, 2.74, 2.53], note="2021-01上市 · 后复权"),
    # 农商行
    "cqrc": dict(prices=[None, None, 4.73, 4.23, 7.31, 8.03, 8.19], note="2019-10上市 · 后复权"),
    "qrc": dict(prices=[None, None, 5.39, 3.44, 3.69, 3.87, 3.68], note="2019-03上市 · 后复权"),
    "changshu": dict(prices=[None, 6.5, 8.12, 8.69, 9.97, 10.61, 10.29], note="2016-09上市 · 后复权"),
    "zijin": dict(prices=[None, None, 4.41, 2.99, 3.45, 3.46, 3.29], note="2019-01上市 · 后复权"),
    "wuxi": dict(prices=[None, 5.54, 6.74, 6.29, 7.33, 7.68, 7.06], note="2016-09上市 · 后复权"),
    "zjg": dict(prices=[None, 5.55, 6.6, 6.35, 6.54, 7.14, 6.71], note="2017-01上市 · 后复权"),
    "sunong": dict(prices=[None, 8.2, 7.69, 7.75, 9.11, 9.89, 9.12], note="2016-11上市 · 后复权"),
    "jiangyin": dict(prices=[None, 5.33, 5.65, 5.71, 6.61, 7.24, 6.99], note="2016-09上市 · 后复权"),
    "ruifeng": dict(prices=[None, None, None, 6.49, 7.88, 8.23, 7.03], note="2021-06上市 · 后复权"),
    "shnc": dict(prices=[None, None, None, 6.44, 10.03, 11.24, 9.81], note="2021-08上市 · 后复权"),
}
# 价格序列年份对齐：2014底, 2018底, 2020底, 2022底, 2024底, 2025底, 2026H1
PRICE_YEARS = ["2014底", "2018底", "2020底", "2022底", "2024底", "2025底", "2026H1"]


# ================= render 函数 =================
def render_index():
    cats = ["国有大行", "股份行", "城商行", "农商行"]
    cards = ""
    for c in company_data:
        s = c["snapshot"]
        cards += f"""<a class="card" href="berkshire-bank-chain-{c['slug']}.html" style="text-decoration:none;color:inherit;display:block">
<div class="top"><h3>{c['name']}</h3><span class="code">{c['code']}</span></div>
<span class="cat">{c['cat']}</span>
<div class="pos">{c['pos']}</div>
<div class="kpis">
<div><b>{s['pb']}x</b>PB</div><div><b>{s['div']}%</b>股息率</div>
<div><b>{s['npl']}%</b>不良率</div><div><b>{s['cpr']}%</b>拨备</div>
<div><b>{s['nim']}%</b>NIM</div><div><b>{s['roe']}%</b>ROE</div></div></a>"""
    extend = """<div class="extend">
<a href="berkshire-bank-industrial-chain.html"><b>银行业产业链</b><span>资金流向地图：上游负债来源→中游运作→下游资产去向，读懂银行生意模式</span></a>
<a href="berkshire-bank-compare.html"><b>横向对比工具</b><span>勾选多家银行并排比 PB/股息率/不良率/拨备/NIM/ROE 等</span></a>
<a href="berkshire-bank-methodology.html"><b>银行方法论文</b><span>不良率/关注类/逾期、净息差、拨备、ROE与PB、资本约束怎么读</span></a>
<a href="berkshire-bank-cycle.html"><b>信用周期 2016→2025</b><span>去杠杆、资管新规、让利、地产风险、息差探底串起来看</span></a>
<a href="berkshire-bank-backtest.html"><b>三轮大底回测</b><span>2014 / 2018 / 2022-24 的 PB 与股息率买点复盘</span></a>
<a href="berkshire-bank-thermometer.html"><b>估值温度计</b><span>42家 PB分位+股息率 冷热排序（分组筛选）</span></a>
<a href="berkshire-bank-backtest-detail.html"><b>逐轮买点回报图</b><span>42家后复权累计回报曲线，基准年=100 横向可比</span></a>
</div>"""
    html = header("银行业投资图谱 · 42家A股上市银行", "首页 / 投资数据中心 / 银行图谱")
    html += f"""<div class="hero"><div class="hero-in">
<h1>银行业投资图谱</h1>
<p>42家A股上市银行，按属性分4类，逐家业务条线框架 + 财务快照 + 六维要点解读（资产质量/盈利/估值/规模/投资逻辑/核心风险）；国有大行6家、招商与3家特色农商行附资产质量、息差、资本、估值的重点解析与事件时间线。</p>
<p style="font-size:12.5px">数据口径：财务=2025年年报（最新可得年报，2026年中报预计8月后披露）；估值=2026-07-12行情。42家均已绘制后复权累计回报曲线。</p>
<div class="stat">
<b>42家</b><span>上市银行覆盖</span>
<b>4类</b><span>国有大行/股份行/城商行/农商行</span>
<b>7页</b><span>图谱+方法论+周期+回测+温度计+回报图</span>
</div></div></div>
<div class="wrap">
<div class="section-title">银行图谱（点击进入逐家详情）</div>
<div class="filter">
<button class="on" data-f="all">全部</button>
<button data-f="国有大行">国有大行</button><button data-f="股份行">股份行</button>
<button data-f="城商行">城商行</button><button data-f="农商行">农商行</button></div>
<div class="grid" id="grid">{cards}</div>
<div class="section-title">延伸阅读</div>{extend}
</div>"""
    html += """<script>
var btns=document.querySelectorAll('.filter button');
var grid=document.getElementById('grid');
var cards=Array.from(grid.children);
btns.forEach(function(b){b.onclick=function(){btns.forEach(x=>x.classList.remove('on'));b.classList.add('on');
var f=b.dataset.f;cards.forEach(function(c){var cat=c.querySelector('.cat').textContent;c.style.display=(f==='all'||cat===f)?'':'none';});};});
</script>""" + footer()
    return html


def gen_thesis(c):
    """基于真实财务快照，为每家银行生成「投资逻辑（看多理由）」——价值投资视角。"""
    s = c["snapshot"]
    npl, cpr, nim, roe, pb, div = s["npl"], s["cpr"], s["nim"], s["roe"], s["pb"], s["div"]
    cat = c["cat"]
    pts = []
    # 安全边际：低PB + 高股息
    if pb < 0.7 and div >= 4.5:
        pts.append(f"低PB（{pb}x）+ 高股息率（{div}%）构成高安全边际，是红利/价值策略的核心标的")
    elif pb < 0.7:
        pts.append(f"深度破净（PB {pb}x）提供折价买入1元净资产的机会，下行空间相对有限")
    elif div >= 5:
        pts.append(f"股息率高达 {div}%，收息回报丰厚，适合长期持有收股息")
    # 资产质量护城河
    if npl <= 0.85 and cpr >= 350:
        pts.append(f"不良率 {npl}% 低、拨备覆盖率 {cpr}% 极厚，资产质量扎实、隐藏利润空间大")
    # 息差/盈利护城河
    if nim >= 2.0:
        pts.append(f"净息差 {nim}% 为全行业最高档，负债成本优势构成宽护城河")
    elif roe >= 12:
        pts.append(f"ROE {roe}% 居行业前列，股东回报能力强、内生资本补充足")
    # 定位
    if cat == "国有大行":
        pts.append("系统重要性银行，经营稳健、分红连续，是防御性底仓与「中特估」主线")
    elif cat == "农商行" and nim >= 1.5:
        pts.append("深耕本地小微/县域，存款成本低、区域壁垒强，'小而美'成长样本")
    elif cat == "城商行" and roe >= 12:
        pts.append("区域龙头，受益于本地经济红利，成长性与资产质量兼顾")
    elif cat == "股份行":
        pts.append("机制灵活、综合化经营，零售/投行/同业各有特色，弹性大于大行")
    if not pts:
        pts.append(f"PB {pb}x、股息率 {div}%，估值处于行业中枢，需结合资产质量趋势判断")
    return "；".join(pts) + "。"


def gen_risk(c):
    """基于真实财务快照，为每家银行生成「核心风险（看空理由）」。"""
    s = c["snapshot"]
    npl, cpr, nim, roe, pb, div = s["npl"], s["cpr"], s["nim"], s["roe"], s["pb"], s["div"]
    pts = []
    if npl >= 1.5:
        pts.append(f"不良率 {npl}% 偏高，资产质量存隐忧（关注地产/城投/区域信用风险）")
    elif npl >= 1.3:
        pts.append(f"不良率 {npl}% 高于行业均值，需持续跟踪资产质量走向")
    if cpr < 180:
        pts.append(f"拨备覆盖率 {cpr}% 偏薄，抵御坏账余量有限")
    if nim < 1.4:
        pts.append(f"净息差 {nim}% 偏低，受让利与负债成本挤压，盈利弹性弱")
    if roe < 7:
        pts.append(f"ROE {roe}% 偏低，资本内生能力弱、估值修复动力不足")
    if pb < 0.45:
        pts.append(f"PB 深度破净（{pb}x）反映市场对资产质量的深度担忧，警惕价值陷阱")
    if not pts:
        pts.append(f"主要风险为行业共性：经济下行期资产质量扰动、净息差持续收窄与政策让利")
    return "；".join(pts) + "。"


def key_points(c):
    """基于真实财务快照，为每家银行生成六维要点解读（资产质量/盈利能力/估值分红/规模定位/投资逻辑/核心风险）。"""
    s = c["snapshot"]
    npl, cpr, nim, roe, pb, div = s["npl"], s["cpr"], s["nim"], s["roe"], s["pb"], s["div"]
    rev, profit, mcap, cat = s["rev"], s["profit"], s["mcap"], c["cat"]

    # —— 资产质量 ——
    if npl <= 0.85:
        q1 = f"不良率 {npl}% 处于行业优秀水平，资产质量扎实"
    elif npl <= 1.15:
        q1 = f"不良率 {npl}% 优于行业均值，资产质量良好"
    elif npl <= 1.4:
        q1 = f"不良率 {npl}% 与行业均值相当，总体可控"
    elif npl <= 1.6:
        q1 = f"不良率 {npl}% 略高于行业均值，需关注资产质量走向"
    else:
        q1 = f"不良率 {npl}% 偏高，资产质量存在一定压力"
    if cpr >= 380:
        q1 += f"；拨备覆盖率 {cpr}% 极为充足，安全垫厚、隐藏利润与抗风险空间大。"
    elif cpr >= 280:
        q1 += f"；拨备覆盖率 {cpr}% 较为充足，坏账缓冲能力强。"
    elif cpr >= 200:
        q1 += f"；拨备覆盖率 {cpr}% 高于监管红线、处于中等水平。"
    else:
        q1 += f"；拨备覆盖率 {cpr}% 相对偏薄，抵御坏账的余地有限。"

    # —— 盈利能力 ——
    if nim >= 2.0:
        q2 = f"净息差 {nim}% 显著高于行业（行业约1.5%），盈利发动机强劲"
    elif nim >= 1.7:
        q2 = f"净息差 {nim}% 高于行业均值，息差优势明显"
    elif nim >= 1.4:
        q2 = f"净息差 {nim}% 与行业相当，处于合理区间"
    else:
        q2 = f"净息差 {nim}% 偏低，受让利与负债成本挤压"
    if roe >= 13:
        q2 += f"；ROE {roe}% 位居行业前列，股东回报能力突出。"
    elif roe >= 10:
        q2 += f"；ROE {roe}% 高于行业均值，盈利能力较强。"
    elif roe >= 8:
        q2 += f"；ROE {roe}% 处于行业中游。"
    else:
        q2 += f"；ROE {roe}% 偏低，盈利能力有待修复。"

    # —— 估值与分红 ——
    if pb < 0.45:
        q3 = f"PB {pb}x 破净幅度深，市场对其资产质量或成长性定价偏谨慎"
    elif pb < 0.7:
        q3 = f"PB {pb}x 明显破净，估值处于折价区间"
    elif pb < 1.0:
        q3 = f"PB {pb}x 合理偏低，破净但已获一定认可"
    else:
        q3 = f"PB {pb}x 高于1倍净资产，享有零售/成长溢价"
    if div >= 5.5:
        q3 += f"；股息率 {div}% 极具吸引力，是红利策略的核心标的。"
    elif div >= 4.5:
        q3 += f"；股息率 {div}% 较高，具备稳定收息价值。"
    elif div >= 3.5:
        q3 += f"；股息率 {div}% 处于合理水平。"
    else:
        q3 += f"；股息率 {div}% 偏低，分红吸引力一般。"

    # —— 规模与定位 ——
    scale = {"国有大行": "国有大行", "股份行": "全国性股份行", "城商行": "区域城商行", "农商行": "区域农商行"}[cat]
    if mcap >= 5000:
        sz = "总市值居行业前列"
    elif mcap >= 1000:
        sz = "属中大型体量"
    elif mcap >= 300:
        sz = "属中型体量"
    else:
        sz = "属中小型体量"
    q4 = f"2025年营收 {rev} 亿、归母净利 {profit} 亿，总市值 {mcap} 亿，{sz}；作为{scale}，{c['pos']}"

    items = [
        ("资产质量", q1),
        ("盈利能力", q2),
        ("估值与分红", q3),
        ("规模与定位", q4),
        ("投资逻辑", gen_thesis(c)),
        ("核心风险", gen_risk(c)),
    ]
    grid = "".join(f'<div class="deep-item"><h4>{t}</h4><p>{v}</p></div>' for t, v in items)
    return f'<div class="deep-grid">{grid}</div>'


def render_detail(c):
    s = c["snapshot"]
    b = c["business"]
    layers = "".join(
        f'<div class="layer"><h4>{k}</h4><p>{v}</p></div>' for k, v in b.items())
    snap = f"""<div class="snap">
<div><b>{s['rev']}</b><span>营收(亿)</span></div>
<div><b>{s['profit']}</b><span>归母净利(亿)</span></div>
<div><b>{s['npl']}%</b><span>不良率</span></div>
<div><b>{s['cpr']}%</b><span>拨备覆盖率</span></div>
<div><b>{s['nim']}%</b><span>净息差NIM</span></div>
<div><b>{s['roe']}%</b><span>ROE</span></div>
<div><b>{s['pb']}x</b><span>PB</span></div>
<div><b>{s['div']}%</b><span>股息率</span></div>
<div><b>{s['mcap']}</b><span>总市值(亿)</span></div></div>"""
    d = DEEP_DATA.get(c["slug"])
    if d:
        detail_items = [
            ("资产质量", d['asset_quality']),
            ("净息差", d['spread']),
            ("资本充足", d['capital']),
            ("估值与分红", d['valuation']),
            ("最新经营信号", d['latest']),
            ("投资逻辑", gen_thesis(c)),
            ("核心风险", gen_risk(c)),
        ]
        cards_h = "".join(f'<div class="deep-item"><h4>{t}</h4><p>{v}</p></div>' for t, v in detail_items)
        tl = "".join(f'<div>{n}</div>' for n in d['news'])
        deep = f"""<h3 class="section-title">重点解析（资产质量 / 息差 / 资本 / 估值）</h3>
<div class="deep-grid">{cards_h}</div>
<h3 class="section-title">关键事件时间线</h3>
<div class="timeline">{tl}</div>"""
    else:
        deep = '<h3 class="section-title">要点解读（基于2025年报 / 2026-07-12估值）</h3>' + key_points(c)
    note = """<div class="note">框架知识：银行看三张表——资产质量（不良率/拨备/逾期偏离度）、盈利能力（NIM/ROE/中收）、资本与估值（核心一级资本充足率/PB/股息率）。详见<a href="berkshire-bank-methodology.html" style="color:var(--accent)">银行方法论文</a>。</div>"""
    html = header(f"{c['name']} · 银行图谱", f"首页 / 投资数据中心 / 银行图谱 / {c['name']}")
    html += f"""<div class="detail">
<a class="back" href="berkshire-bank-chains.html">← 返回银行图谱</a>
<h1 style="margin:10px 0 2px">{c['name']} <span style="font-size:14px;color:var(--mut)">{c['code']} · {c['cat']}</span></h1>
<p style="color:var(--mut);margin:0 0 14px">{c['pos']}</p>
<h3 class="section-title" style="margin-top:18px">财务快照（2025年报 / 2026-07-12估值）</h3>{snap}
<h3 class="section-title">业务条线框架（5层）</h3>{layers}
{deep}{note}
</div>"""
    html += footer()
    return html


def render_methodology():
    html = header("银行方法论文", "首页 / 投资数据中心 / 银行图谱 / 方法论文")
    html += """<div class="detail">
<a class="back" href="berkshire-bank-chains.html">← 返回银行图谱</a>
<h1 style="margin:10px 0">银行怎么读：核心指标框架</h1>
<div class="guide"><h4>为什么银行不能用普通工商企业的估值框架？</h4>
<p>银行是经营「风险」的企业：用存款人的钱去放贷，赚利差。它的「存货」是贷款（会违约），所以估值核心是<b>资产质量</b>与<b>拨备厚度</b>，而非单纯的营收增速。市场长期给银行PB&lt;1（破净），本质是在给「看不见的坏账」打折。</p></div>

<h3 class="section-title">1. 资产质量三件套：不良率 / 关注类 / 逾期</h3>
<div class="layer"><h4>不良贷款率（NPL ratio）</h4><p>不良余额 / 贷款总额。公认「已出问题」的贷款。但要警惕：不良是「分类结果」，银行有调节空间（借新还旧、展期可暂不计入不良）。</p></div>
<div class="layer"><h4>关注类贷款</h4><p>虽未违约但存在隐患的贷款。关注类占比上升往往预示未来不良压力。看「（不良+关注）/ 贷款总额」比单看不良率更前瞻。</p></div>
<div class="layer"><h4>逾期贷款与「逾期偏离度」</h4><p>逾期90天以上贷款原则上应计入不良。偏离度 = 逾期90天以上贷款 / 不良贷款，&lt;100%说明分类严格（藏雷少），&gt;100%说明有「逾期但没认定为不良」的粉饰嫌疑。</p></div>

<h3 class="section-title">2. 拨备覆盖率：安全垫厚不厚</h3>
<div class="layer"><h4>拨备覆盖率 = 贷款减值准备金 / 不良余额</h4><p>越高越能吸收未来坏账。但过高的拨备也可能在「隐藏利润」（监管曾要求不低于150%，后改为120%-150%弹性区间）。拨备覆盖率高的银行（如招行390%+、杭州500%+）抗风险与利润释放空间都大。</p></div>
<div class="layer"><h4>拨贷比 = 贷款减值准备金 / 贷款总额</h4><p>拨备覆盖率的补充，反映每100元贷款提了多少「保险」。与拨备覆盖率配合看，避免被低不良率+低拨备的「虚假安全」误导。</p></div>

<h3 class="section-title">3. 净息差 NIM：银行盈利的发动机</h3>
<div class="layer"><h4>净息差 = （利息收入-利息支出）/ 生息资产均值</h4><p>银行最核心的盈利驱动。2022-2024年行业NIM从2.1%降至1.5%附近（LPR下调+存款定期化），是银行利润增速放缓的主因。常熟银行NIM 2.5%、邮储1.66%显著高于大行，源于存款成本优势。</p></div>

<h3 class="section-title">4. 资本充足率：扩张的天花板</h3>
<div class="layer"><h4>核心一级资本充足率 / 一级 / 资本充足率</h4><p>监管红线（核心一级≥7.5%、资本充足率≥10.5%，系统重要性银行更高）。资本不足则无法放贷、无法分红。2025年财政部注资国有大行即补充核心一级资本。高ROE+高资本充足率=可持续扩张能力。</p></div>

<h3 class="section-title">5. ROE 与 PB：破净之谜</h3>
<div class="layer"><h4>为什么高ROE的银行PB却低于1？</h4><p>招行ROE 13%、宁波13%，但PB仅0.8-0.9x；民生ROE 5%、PB 0.26x。市场给PB=1以下的折扣，是在为「潜在不良+让利政策+经济下行」定价。反过来，<b>高ROE + 低PB + 高股息</b>常被价值投资者视为「烟蒂变金条」——但前提是资产质量真实稳健，否则是价值陷阱。</p></div>
<div class="note">实用口诀：看银行先看「不良偏离度+拨备覆盖率」定安全边际，再看「NIM+中收」定盈利趋势，最后用「PB分位+股息率」定买点。具体买点方法见<a href="berkshire-bank-thermometer.html" style="color:var(--accent)">估值温度计</a>与<a href="berkshire-bank-backtest.html" style="color:var(--accent)">三轮大底回测</a>。</div>
</div>"""
    html += footer()
    return html


def render_cycle():
    rows = [
        ("2016", "债转股试点、去产能", "银行不良贷款见顶回落，资产质量边际改善"),
        ("2017", "金融去杠杆开启", "同业、理财扩张受限，MPA考核收紧"),
        ("2018", "资管新规落地(4月)、紧信用", "民企违约潮，股份行/城商行不良承压，PB探底"),
        ("2019", "包商银行接管(5月)", "中小银行风险首次公开暴露，同业信仰打破"),
        ("2020", "疫情、让利实体1.5万亿、LPR下行", "净息差快速收窄，拨备计提加大，利润零增/负增"),
        ("2021", "房地产三道红线传导、恒大违约", "地产风险暴露，对公地产贷款不良抬头"),
        ("2022", "断供潮、理财破净、河南村镇银行", "地产+城投担忧加剧，银行股破净比例创新高"),
        ("2023", "城投风险、中特估行情、存款降息开启", "高股息策略升温，国有大行率先修复；手工补息前存款成本仍高"),
        ("2024", "手工补息治理、息差探底、高股息行情", "行业NIM约1.5%历史低位；大行PB跌至0.4-0.6x，股息率6-9%"),
        ("2025", "化债推进、险资举牌银行、PB修复", "财政部注资大行；大行PB回到0.7-0.8x，股息率仍高"),
    ]
    tr = "".join(f"<tr><td>{r[0]}</td><td style='text-align:left'>{r[1]}</td><td style='text-align:left'>{r[2]}</td></tr>" for r in rows)
    html = header("信用周期 2016→2025", "首页 / 投资数据中心 / 银行图谱 / 信用周期")
    html += f"""<div class="detail">
<a class="back" href="berkshire-bank-chains.html">← 返回银行图谱</a>
<h1 style="margin:10px 0">银行业信用周期 · 2016→2025</h1>
<p style="color:var(--mut)">把42家银行的调整数据串成一条宏观视图：监管周期、货币政策与风险暴露交替主导银行股十年估值。</p>
<div class="guide"><h4>十年主线</h4>
<p>2016-2017 去产能后资产质量改善 → 2018 去杠杆+资管新规刺破同业与民企风险 → 2020 疫情让利压息差 → 2021-2022 地产与城投风险 sequential 暴露 → 2023-2025 高股息行情+化债+注资推动估值修复。银行股本质是对「经济信用风险」的定价。</p></div>
<table class="tbl"><tr><th>年份</th><th>监管/政策主线</th><th>对银行的影响</th></tr>{tr}</table>
<h3 class="section-title">关键指标十年变化</h3>
<div class="layer"><h4>行业净息差 NIM</h4><p>约 2.2%(2016) → 2.1%(2019) → 1.7%(2022) → 1.5%(2024) → 1.5%(2025)。单边下行是利润增速放缓的核心，也是高股息行情的背景（估值已充分反映悲观预期）。</p></div>
<div class="layer"><h4>上市银行平均 PB</h4><p>约 0.9x(2016) → 0.8x(2018) → 0.7x(2020) → 0.5x(2022-2024谷底) → 0.7x(2025修复)。破净成为常态，股息率从3%升至6-9%吸引配置型资金。</p></div>
<div class="layer"><h4>不良率</h4><p>行业商业银行不良率约 1.74%(2016) → 1.96%(2018峰) → 1.84%(2020) → 1.62%(2025)，总体平稳但结构分化（地产/城投相关敞口隐性压力用拨备与注资对冲）。</p></div>
<div class="note">周期启示：银行股的最佳买点往往出现在「坏消息最密集、PB最低、股息率最高」之时（如2014、2018、2022-2024），而非财报最好看时。详见<a href="berkshire-bank-backtest.html" style="color:var(--accent)">三轮大底回测</a>。</div>
</div>"""
    html += footer()
    return html


def render_backtest():
    html = header("三轮大底回测", "首页 / 投资数据中心 / 银行图谱 / 回测")
    html += """<div class="detail">
<a class="back" href="berkshire-bank-chains.html">← 返回银行图谱</a>
<h1 style="margin:10px 0">银行股三轮大底买点回测</h1>
<p style="color:var(--mut)">银行估值锚是 PB（市净率）而非 PE。三轮历史大底的 PB 与股息率水平，是判断「便宜与否」的标尺。</p>
<table class="tbl">
<tr><th>买点</th><th>宏观背景</th><th>大行 PB</th><th>大行股息率</th><th>逻辑</th></tr>
<tr><td>2014底</td><td>牛市前夜、经济低迷</td><td>0.7-0.9x</td><td>4-5%</td><td>破净初期，无人问津</td></tr>
<tr><td>2018底</td><td>去杠杆+贸易战+民企违约</td><td>0.6-0.8x</td><td>4-5%</td><td>悲观定价极致</td></tr>
<tr><td>2022-2024</td><td>地产+城投风险、息差探底</td><td>0.4-0.6x</td><td>6-9%</td><td>破净比例历史新高，红利资产重估起点</td></tr>
</table>
<div class="guide"><h4>回测结论（以国有大行+招行为样本）</h4>
<p>在三轮大底买入并持有至今（2025底），年化回报主要来自<b>股息再投资</b>与<b>PB修复</b>两部分。2014、2018买点持有至今累计回报以倍数计；2022-2024买点虽时间短，但股息率6-9%已提供高安全垫，PB从0.4-0.6x修复至0.7x附近贡献资本利得。</p></div>
<div class="layer"><h4>为什么银行适合「买点+收息」策略？</h4><p>银行盈利波动小于周期股，分红连续且比例高（30%左右，大行更高）。低PB买入=用折价拿到1元净资产+高股息，时间站在收息者一边。但前提：资产质量真实（偏离度低、拨备厚），否则「便宜」是陷阱。</p></div>
<div class="note">回测≠预测。历史低PB买点提供的是「安全边际参考」，不是买入保证。逐家买点回报曲线见<a href="berkshire-bank-backtest-detail.html" style="color:var(--accent)">逐轮买点回报图</a>（42家均已绘制后复权累计回报曲线，基准年=100 可横向比较）。</div>
</div>"""
    html += footer()
    return html


def _thermo_sort_key(c):
    # 越破净、股息越高 => 越偏"价值/冷"左侧；PB越近1越"热"
    return c["snapshot"]["pb"]


def render_thermometer():
    groups = ["国有大行", "股份行", "城商行", "农商行"]
    out = ""
    for g in groups:
        items = [c for c in company_data if c["cat"] == g]
        items.sort(key=lambda x: x["snapshot"]["pb"])
        rows = ""
        for c in items:
            s = c["snapshot"]
            # 位置：PB 0.25 -> 左(红/冷低估)，1.0 -> 中，>1 -> 右(绿/热)
            pos = max(2, min(98, s["pb"] / 1.2 * 100))
            if s["pb"] < 0.7:
                zone = "破净区(低估)"
            elif s["pb"] < 1.0:
                zone = "中性区"
            else:
                zone = "溢价区"
            rows += f"""<div class="thermo"><div class="nm">{c['name']}</div>
<div class="bar"><div class="dot" style="left:{pos}%"></div></div>
<div class="v">PB <b>{s['pb']}x</b> · 股息率 {s['div']}% · {zone}</div></div>"""
        out += f'<h3 class="section-title">{g}（{len(items)}家，按PB升序）</h3>' + rows
    html = header("估值温度计", "首页 / 投资数据中心 / 银行图谱 / 温度计")
    html += f"""<div class="detail">
<a class="back" href="berkshire-bank-chains.html">← 返回银行图谱</a>
<h1 style="margin:10px 0">银行估值温度计 · 42家</h1>
<p style="color:var(--mut)">按 PB（市净率）升序排列，越靠左越破净（越「冷」/低估），越靠右越接近或高于1倍净资产（越「热」）。条形颜色：红=破净低估，黄=中性，绿=溢价。</p>
<div class="guide"><h4>怎么读温度计</h4>
<p>银行破净是常态。PB&lt;0.7x 多为市场担忧资产质量（地产/城投敞口）；PB 0.7-1.0x 为合理偏低；&gt;1x 多为零售/财富溢价（招行、宁波、成都、杭州等）。<b>低PB+高股息</b>组合（如交行、兴业、华夏、光大）是红利策略核心标的。</p></div>
{out}
<div class="note">温度计为静态快照（估值基准2026-07-12），会随行情变动。PB分位需近10年区间判断，本页用绝对PB水平近似。买点逻辑见<a href="berkshire-bank-backtest.html" style="color:var(--accent)">回测</a>。</div>
</div>"""
    html += footer()
    return html


def _backtest_svg(hist):
    prices = hist["prices"]
    # 找第一个非None
    start = next((i for i, v in enumerate(prices) if v is not None), None)
    if start is None:
        return None
    pts = [(PRICE_YEARS[i], prices[i]) for i in range(start, len(prices)) if prices[i] is not None]
    if len(pts) < 2:
        return None
    base = pts[0][1]
    vals = [v / base * 100 for _, v in pts]
    import math
    y_lo = min(min(vals), 80)
    y_hi = max(max(vals), 120)
    pad = (y_hi - y_lo) * 0.15
    y_lo, y_hi = y_lo - pad, y_hi + pad
    W, H = 560, 240
    m_l, m_r, m_t, m_b = 44, 16, 16, 28
    pw = W - m_l - m_r
    ph = H - m_t - m_b
    n = len(vals)
    def X(i): return m_l + (pw * i / (n - 1)) if n > 1 else m_l + pw / 2
    def Y(v): return m_t + ph * (1 - (v - y_lo) / (y_hi - y_lo))
    # 网格
    grid = ""
    for t in range(int(y_lo // 20 * 20), int(y_hi), 20):
        yy = Y(t)
        grid += f'<line x1="{m_l}" y1="{yy:.1f}" x2="{W-m_r}" y2="{yy:.1f}" stroke="#eef2f7"/><text x="{m_l-6}" y="{yy+3:.1f}" font-size="10" fill="#5d6b7a" text-anchor="end">{t}</text>'
    line = " ".join(f"{X(i):.1f},{Y(vals[i]):.1f}" for i in range(n))
    dots = "".join(f'<circle cx="{X(i):.1f}" cy="{Y(vals[i]):.1f}" r="3" fill="#0f2c4c"/>' for i in range(n))
    xl = "".join(f'<text x="{X(i):.1f}" y="{H-10}" font-size="10" fill="#5d6b7a" text-anchor="middle">{pts[i][0]}</text>' for i in range(n))
    lab = "".join(f'<text x="{X(i):.1f}" y="{Y(vals[i])-7:.1f}" font-size="9.5" fill="#c8a04a" text-anchor="middle">{vals[i]:.0f}</text>' for i in range(n))
    return f'''<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:560px">
<rect x="{m_l}" y="{m_t}" width="{pw}" height="{ph}" fill="#fafcff" stroke="#e2e8f0"/>
{grid}
<polyline points="{line}" fill="none" stroke="#c8a04a" stroke-width="2.5"/>
{dots}{xl}{lab}
<text x="{m_l}" y="12" font-size="11" fill="#0f2c4c">后复权累计回报指数（{pts[0][0]}=100）</text>
</svg>'''


def render_backtest_detail():
    html = header("逐轮买点回报图", "首页 / 投资数据中心 / 银行图谱 / 回报图")
    html += """<div class="detail">
<a class="back" href="berkshire-bank-chains.html">← 返回银行图谱</a>
<h1 style="margin:10px 0">逐轮买点回报图（后复权）</h1>
<div class="note">数据说明：银行几乎只分红不送股，后复权价能真实反映「分红再投资」的总回报。全 42 家均已接入<b>行情接口后复权（hfq）年线收盘价</b>（数据源：腾讯自选股行情接口，采集于 2026-07-12），从各自上市年起绘制曲线，基准年=100。后复权价含历次分红再投资累积，绝对值可能远高于现价（如招行、平安），归一化为指数后可横向比较。数据仅供研究参考，最终以交易所与行情终端为准，<b>不构成投资建议</b>。</div>
"""
    for c in company_data:
        s = c["snapshot"]
        hist = HIST_PRICE.get(c["slug"])
        if hist:
            svg = _backtest_svg(hist)
            body = svg if svg else '<p style="color:var(--mut)">数据不足，无法绘图。</p>'
            body += f'<p style="font-size:12px;color:var(--mut)">口径：{hist["note"]}；后复权价基准={PRICE_YEARS[[i for i,v in enumerate(hist["prices"]) if v is not None][0]]}=100。</p>'
        else:
            body = '<p style="color:var(--mut);font-size:13px">暂无后复权历史价数据。</p>'
        html += f'<div class="svgbox"><h3 style="margin:0 0 8px;color:var(--navy)">{c["name"]} <span style="font-size:13px;color:var(--mut)">{c["code"]} · {c["cat"]}</span></h3>{body}</div>'
    html += """<div class="guide"><h4>怎么用这张图</h4>
<p>曲线从买入年起算=100，上行代表持有至今的后复权总回报。银行回报主要由「股息再投资」累积，长期持有+低PB买入，曲线斜率往往比直觉更陡。42 家横向比较可看出：宁波、成都、江苏、南京等成长型城商行后复权回报斜率最陡，国有大行则以稳健分红复利见长，郑州、兰州等则长期跑输。<b>注意：过去回报≠未来收益，后复权曲线不含买卖摩擦成本。</b></p></div>
</div>"""
    html += footer()
    return html


def render_industrial_chain():
    def node(b, desc):
        return f'<div class="node"><b>{b}</b><span>{desc}</span></div>'
    up = (
        node("中央银行", "基础货币投放——降准、MLF、再贷款再贴现、SLF，是银行负债的源头活水，也是货币政策调节器。")
        + node("居民存款", "成本最低、最稳定的负债来源；邮储、农行、农商行凭借网点下沉优势存款成本全行业最低。")
        + node("企业存款", "对公活期+定期、结算沉淀；国有大行与招行凭借客群基础占据低成本对公存款优势。")
        + node("同业负债", "同业存单、同业拆借、央行借款等主动负债，受市场利率与流动性环境波动影响。")
    )
    mid = (
        node("牌照与资本监管", "银行牌照稀缺；资本充足率（核心一级≥7.5%）是扩张的天花板；MPA 考核与系统重要性银行附加监管约束经营。")
        + node("负债端管理", "存款成本管控（活期占比）、主动负债节奏调节，决定净息差（NIM）的下限与稳定性。")
        + node("资产配置", "信贷（对公/零售）、金融投资（债券/基金）、同业资产之间的风险—收益权衡，决定资产端收益。")
        + node("风控与拨备", "不良分类、拨备计提、逾期偏离度检验，直接决定资产质量的真实度与利润含金量。")
    )
    down = (
        node("对公贷款", "基建/央企、地产、制造业、小微、城投平台——构成银行资产端的主体，也是信用风险的集中区。")
        + node("零售贷款", "住房按揭、消费贷、信用卡——招行、平安等零售型银行的主要高收益资产。")
        + node("政府债券", "国债、地方政府债——低风险资产配置，兼顾流动性与监管指标。")
        + node("同业与金融市场", "债券投资、非标、ABS 等——平衡流动性与收益，受市场利率与监管影响较大。")
    )
    stages = [
        ("01 上游 · 资金端 / 负债来源", "钱从哪来", up),
        ("02 中游 · 银行运作中枢", "信用中介如何加工", mid),
        ("03 下游 · 资产端 / 资金去向", "钱到哪去", down),
    ]
    flow = ""
    for sno, tag, body in stages:
        flow += f'<div class="stage"><div class="sno">{sno.split(" ")[0]}</div><h4>{sno.split(" ",1)[1]}</h4><div class="tagline">{tag}</div>{body}</div>'
    html = header("银行业产业链 · 资金流向地图", "首页 / 投资数据中心 / 银行图谱 / 产业链")
    html += f"""<div class="detail">
<button class="back" style="border:none;background:none;cursor:pointer" onclick="location.href='berkshire-bank-chains.html'">← 返回银行图谱</button>
<h1 style="margin:10px 0 2px">银行业「产业链」：资金的流向地图</h1>
<p style="color:var(--mut);margin:0 0 8px">银行不是制造企业，它的「产业链」是<b>资金的流向</b>——从央行与储户出发，经银行这一信用中介加工，再流向实体部门与金融市场。看懂这条链，就读懂了银行的生意模式。</p>
<div class="guide"><h4>银行的利润公式</h4>
<p><b>利润 ≈ 资产端收益 − 负债端成本 − 信用成本（坏账损失）</b>。上游决定「资金多贵」，中游决定「怎么加工、风险多高」，下游决定「钱生多少钱、会不会坏账」。估值长期破净，本质是在给「看不见的坏账」打折。</p></div>
<div class="flow3">{flow}</div>
<div class="flow-cap">↑ 资金流向：<b>央行 / 储户 / 同业</b> →（银行信用中介：负债管理 + 资产配置 + 风控拨备）→ <b>实体部门 / 金融市场</b> ↑</div>
<h3 class="section-title">怎么用这张产业链图</h3>
<div class="layer"><h4>上游看「负债成本」</h4><p>存款成本低的银行（邮储/农行/农商行）天然息差占优；依赖同业负债的银行则受市场利率摆布。</p></div>
<div class="layer"><h4>中游看「资本与风控」</h4><p>资本充足率决定能放多少贷；拨备覆盖率与逾期偏离度决定利润有没有「水分」。这是银行区别于普通企业的最关键之处。</p></div>
<div class="layer"><h4>下游看「资产结构」</h4><p>对公地产/城投敞口高的银行，资产质量随宏观信用风险波动；零售+财富占比高的银行（招行/平安）周期性更弱、估值溢价更稳。</p></div>
<div class="note">这张图是理解单家银行的「地图」。回到<a href="berkshire-bank-chains.html" style="color:var(--accent)">银行图谱</a>逐家看业务条线与财务快照，或用<a href="berkshire-bank-compare.html" style="color:var(--accent)">横向对比工具</a>并排比较指标。</div>
</div>"""
    html += footer()
    return html


def render_compare():
    import json
    data = [{"name": c["name"], "code": c["code"], "cat": c["cat"],
             "pb": c["snapshot"]["pb"], "div": c["snapshot"]["div"], "npl": c["snapshot"]["npl"],
             "cpr": c["snapshot"]["cpr"], "nim": c["snapshot"]["nim"], "roe": c["snapshot"]["roe"],
             "rev": c["snapshot"]["rev"], "profit": c["snapshot"]["profit"], "mcap": c["snapshot"]["mcap"]}
            for c in company_data]
    js = json.dumps(data, ensure_ascii=False)
    cols = [("pb", "PB", "low"), ("div", "股息率%", "high"), ("npl", "不良率%", "low"),
            ("cpr", "拨备%", "high"), ("nim", "NIM%", "high"), ("roe", "ROE%", "high"),
            ("rev", "营收亿", "high"), ("profit", "净利亿", "high"), ("mcap", "市值亿", "high")]
    colheads = "".join(f"<th>{t}</th>" for _, t, _ in cols)
    html = header("银行横向对比工具", "首页 / 投资数据中心 / 银行图谱 / 对比")
    html += f"""<div class="detail">
<button class="back" style="border:none;background:none;cursor:pointer" onclick="location.href='berkshire-bank-chains.html'">← 返回银行图谱</button>
<h1 style="margin:10px 0 2px">银行横向对比工具</h1>
<p style="color:var(--mut);margin:0 0 10px">勾选多家银行并排比较核心指标（数据：财务=2025年报，估值=2026-07-12行情）。绿色=该行该项指标在所选样本中占优，红色=偏弱。</p>
<div class="cmp-ctrl">
<div class="bar">
<input type="text" id="q" placeholder="搜索银行名称或代码…">
<button class="fbtn on" data-f="all">全部</button>
<button class="fbtn" data-f="国有大行">国有大行</button>
<button class="fbtn" data-f="股份行">股份行</button>
<button class="fbtn" data-f="城商行">城商行</button>
<button class="fbtn" data-f="农商行">农商行</button>
</div>
<div class="cmp-list" id="list"></div>
<div class="cmp-sel" id="selinfo">已选 0 家</div>
</div>
<div class="svgbox" style="overflow-x:auto">
<table class="tbl" id="tbl"><thead><tr><th>银行</th><th>类别</th>{colheads}</tr></thead><tbody id="tbody"></tbody></table>
</div>
<div class="note">提示：先按类别或搜索筛出候选，再勾选对比。指标口径见<a href="berkshire-bank-methodology.html" style="color:var(--accent)">方法论文</a>。估值会随行情变动，以交易所与行情终端为准，<b>不构成投资建议</b>。</div>
</div>
<script>
var DATA={js};
var COLS={json.dumps(cols, ensure_ascii=False)};
var sel=new Set();
var filt="all", q="";
var listEl=document.getElementById('list');
var tbody=document.getElementById('tbody');
var selinfo=document.getElementById('selinfo');
function renderList(){{
  listEl.innerHTML='';
  DATA.filter(function(d){{(filt==='all'||d.cat===filt)&&(q===''||d.name.indexOf(q)>=0||d.code.indexOf(q)>=0)}}).forEach(function(d){{
    var lab=document.createElement('label');lab.className='cmp-item';
    lab.innerHTML='<input type="checkbox" '+(sel.has(d.code)?'checked':'')+'><b>'+d.name+'</b><span class="cc">'+d.code+' · '+d.cat+'</span>';
    lab.querySelector('input').onchange=function(e){{if(e.target.checked)sel.add(d.code);else sel.delete(d.code);renderList();renderTbl();}};
    listEl.appendChild(lab);
  }});
}}
function color(v,dir,best,worst){{
  if(v===best)return '<span class="cmp-good">'+v+'</span>';
  if(v===worst)return '<span class="cmp-bad">'+v+'</span>';
  return ''+v;
}}
function renderTbl(){{
  var rows=DATA.filter(function(d){{return sel.has(d.code);}});
  selinfo.textContent='已选 '+rows.length+' 家';
  if(!rows.length){{tbody.innerHTML='<tr><td colspan="11" style="color:var(--mut)">请在上方勾选银行</td></tr>';return;}}
  var stats={{}};
  COLS.forEach(function(c){{var vs=rows.map(function(r){{return r[c[0]];}});stats[c[0]]={{best:Math[c[2]==='high'?'max':'min'].apply(null,vs),worst:Math[c[2]==='high'?'min':'max'].apply(null,vs)}};}});
  tbody.innerHTML=rows.map(function(d){{
    var tds=COLS.map(function(c){{return '<td>'+color(d[c[0]],c[2],stats[c[0]].best,stats[c[0]].worst)+'</td>';}}).join('');
    return '<tr><td style="text-align:left"><b>'+d.name+'</b></td><td>'+d.cat+'</td>'+tds+'</tr>';
  }}).join('');
}}
document.getElementById('q').oninput=function(e){{q=e.target.value.trim();renderList();}};
document.querySelectorAll('.cmp-ctrl .fbtn').forEach(function(b){{b.onclick=function(){{document.querySelectorAll('.cmp-ctrl .fbtn').forEach(function(x){{x.classList.remove('on');}});b.classList.add('on');filt=b.dataset.f;renderList();}};}});
renderList();renderTbl();
</script>"""
    html += footer()
    return html


# ================= main =================
if __name__ == "__main__":
    files = {}
    files["berkshire-bank-chains.html"] = render_index()
    for c in company_data:
        files[f"berkshire-bank-chain-{c['slug']}.html"] = render_detail(c)
    files["berkshire-bank-industrial-chain.html"] = render_industrial_chain()
    files["berkshire-bank-compare.html"] = render_compare()
    files["berkshire-bank-methodology.html"] = render_methodology()
    files["berkshire-bank-cycle.html"] = render_cycle()
    files["berkshire-bank-backtest.html"] = render_backtest()
    files["berkshire-bank-thermometer.html"] = render_thermometer()
    files["berkshire-bank-backtest-detail.html"] = render_backtest_detail()
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"generated {len(files)} files")
