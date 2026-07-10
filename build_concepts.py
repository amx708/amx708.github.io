# -*- coding: utf-8 -*-
# 原创重写：巴菲特投资概念库
# 巴菲特投资概念库构建脚本
# 数据基于巴菲特历年股东信与价值投资公开理论整理
# 生成单文件 berkshire-concepts.html

CONCEPTS = [
{
 "id":"moat","name":"护城河","en":"Economic Moat","cat":"核心理念","deep":True,
 "def":"企业能长期维持超额利润的结构性竞争优势，是巴菲特框架的核心。",
 "points":[
  ("本质是持久性，不是当前盈利","巴菲特要的是竞争优势能撑几十年，而不是今年利润高。他反复说，一条需要不断重建的护城河，等于没有护城河。"),
  ("两类主流护城河：低成本与强品牌","低成本型如 GEICO 直销省掉代理佣金；强品牌型如可口可乐、喜诗，消费者愿意为溢价买单，且无需大量资本投入。"),
  ("护城河要天天加宽","让客户满意、砍掉多余成本、改善产品，都是在加宽；对客户漫不经心、纵容臃肿成本，就是在悄悄变窄。短期利润和长期冲突时，加宽优先。"),
 ],
 "cases":"GEICO 从 1995 年伯克希尔控股时市占率 2.5%，靠低成本一条路走到 2016 年底约 12%；喜诗糖果 1972 年以 2500 万美元买下，税前回报率高达 60%，靠的是区域品牌溢价而非资本堆砌；反面教材是德克斯特鞋业，看似有优势，却被海外低成本制造彻底冲垮。",
 "myths":[
  "把高利润当护城河：没有结构性壁垒，明星 CEO 一走优势就没了。",
  "把技术领先当护城河：技术迭代太快，真正的壁垒是成本结构、品牌忠诚、网络效应、转换成本。",
  "以为护城河是静态资产：它每天都在变宽或变窄，取决于管理层的日常行为。",
 ],
 "quotes":[
  ("在商业世界里，我寻找的是被坚不可摧的护城河保护着的经济城堡。","1995 年股东信"),
  ("一条需要不断重建的护城河，最终等于没有护城河。","2007 年股东信"),
 ],
 "related":["franchise","advantage","brand","circle","intrinsic","hold"],
},
{
 "id":"margin","name":"安全边际","en":"Margin of Safety","cat":"核心理念","deep":True,
 "def":"以显著低于内在价值的价格买入，为判断误差和未知风险留出缓冲。",
 "points":[
  ("是对认知局限的谦卑","未来本质上不确定，再聪明的分析师算未来现金流也会错。安全边际就是给这种误差留的容错空间，不是可有可无的加分项。"),
  ("要『显著』的差距，不是『略高』","巴菲特明确说，如果算出价值只比价格高一点，他没兴趣。安全边际是价格与价值之间明显的落差，不是市盈率看起来便宜。"),
  ("防的是永久性资本损失，不是账面波动","持有有安全边际的股票，市场恐慌时照样会大跌；只要内在价值判断没错，时间终会修复价格。"),
 ],
 "cases":"1973 年股市大跌，巴菲特以远低于产业资本估值的价买下华盛顿邮报（当时市值约 8000 万，内行说资产至少值 4 亿）；1988 年买可口可乐时市盈率并不低，但他算出的内在价值远高于市价，安全边际依然充裕。保险上他要求保费定价留出充足缓冲，应对永远昂贵的意外趋势。",
 "myths":[
  "把安全边际等同于『买便宜货』：关键是价格相对价值低，不是绝对市盈率低。",
  "以为安全边际能消除所有风险：它只减永久性损失风险，不消除价格波动。",
  "只在买入时看，忽略持有中变化：股价涨了安全边际就缩小，恐慌大跌时反而扩大，该加仓。",
 ],
 "quotes":[
  ("我们坚持在买入价格上留有安全边际。如果算出价值仅仅略高于价格，我们就不会感兴趣。","1992 年股东信"),
  ("今天的价格水平已经大幅侵蚀了格雷厄姆所说的安全边际——他视之为智慧投资的基石。","1997 年股东信"),
 ],
 "related":["intrinsic","price","undervaluation","circle","market","hold"],
},
{
 "id":"circle","name":"能力圈","en":"Circle of Competence","cat":"核心理念","deep":True,
 "def":"只投资自己真正能看懂的生意，边界比圈有多大更重要。",
 "points":[
  ("边界比大小重要","巴菲特说重要的不是圈有多大，而是你清楚知道圈的边界在哪里。看不懂的，再热门也不碰。"),
  ("以认知能力划分，不是以行业划分","他后来买苹果，不是去学科技，而是把苹果当消费品公司——看的是品牌、生态、用户粘性这些他懂的东西。"),
  ("能力圈内才谈得上安全边际","在自己懂的领域，估值更可靠，安全边际才有意义；圈外的『机会』本质是赌博。"),
 ],
 "cases":"早年他回避科技股，理由是看不清护城河持久性；2016 年后大买苹果，逻辑是『消费品+生态粘性』而非技术路线。这恰恰说明能力圈是认知边界，不是行业黑名单。",
 "myths":[
  "以为能力圈不能扩大：可以学，但要在自己能验证的节奏里扩，不能硬啃看不懂的复杂生意。",
  "以为圈外机会等于风险开放：不懂的别碰，哪怕别人赚翻了。",
 ],
 "quotes":[
  ("你不需要成为每个领域的专家。你只需要看清自己能力圈的边界，并在圈内行事。",""),
 ],
 "related":["moat","intrinsic","margin","concentration","market","hold"],
},
{
 "id":"market","name":"市场先生","en":"Mr. Market","cat":"核心理念","deep":True,
 "def":"格雷厄姆的寓言：把市场报价想象成情绪不稳的合伙人，他的报价只供你利用，不供你听从。",
 "points":[
  ("报价是服务，不是指示","市场先生每天来给你一个价格，你可以接受，也可以忽略。他的情绪与你无关，更不代表企业真实价值。"),
  ("在他恐慌时买，狂热时卖","悲观报价制造便宜货，乐观报价制造昂贵。利用他，而不是被他牵着走。"),
  ("不预测他的情绪","巴菲特认为预测市场短期走向是徒劳的；与其猜涨跌，不如盯着内在价值。"),
 ],
 "cases":"1963 年美国运通『色拉油丑闻』期间股价崩跌，巴菲特判断生意本质没坏，逆市大买；这种在别人恐慌时出手，就是无视市场先生情绪、只认价值的典型。",
 "myths":[
  "把市场先生当智囊：他的报价只是情绪，不是对企业价值的认证。",
  "以为长期持有就要盯盘：长期持有恰恰要求忽略他的日常报价。",
 ],
 "quotes":[
  ("市场先生是你的仆人，不是你的向导。他每天来给你报价，你可以接受，也可以不理。",""),
 ],
 "related":["margin","intrinsic","undervaluation","forecast","hold","efficient"],
},
{
 "id":"intrinsic","name":"内在价值","en":"Intrinsic Value","cat":"核心理念","deep":True,
 "def":"一家企业在其剩余生命周期里所能产生的现金折现之和，是价值的『真北』。",
 "points":[
  ("是估计值，不是精确数","巴菲特说算内在价值不难，但再厉害的分析师估未来现金流也容易错。它是区间，不是小数点。"),
  ("与账面、市价经常背离","会计报表的账面价值、每天跳动的市价，都只是参考；内在价值才是你该锚定的那个。"),
  ("护城河决定它稳不稳","有宽阔护城河的企业，内在价值更可预期、更持久；反之则飘忽。"),
 ],
 "cases":"买华盛顿邮报时，市值约 8000 万，巴菲特判断其资产内在价值远不止 4 亿，价差就是安全边际的来源。回购伯克希尔自身股票时，他也只在市价低于内在价值才动手。",
 "myths":[
  "把账面价值当内在价值：账面是会计数，内在是未来现金流折现，两者常差很远。",
  "追求精确错误：非要算出精确值，反而容易陷入虚假的确定性。",
 ],
 "quotes":[
  ("内在价值是一个估算值——它基于对未来现金流的折现，而不是一个能精确计算的数字。",""),
 ],
 "related":["margin","bookvalue","market","moat","lookthrough","buyback"],
},
{
 "id":"hold","name":"长期持有","en":"Buy and Hold","cat":"核心理念","deep":True,
 "def":"买下好生意后就尽量少动，让复利和时间替你工作。",
 "points":[
  ("前提是买对了生意","长期持有的是有护城河、能持续赚真金白银的企业；买错的东西拿再久也是亏。"),
  ("是研究结果，不是偷懒","持有前你要研究几十年后的商业前景，比猜几个月股价难得多。"),
  ("忽视市场先生的日常报价","只要生意本质没变、护城河没被侵蚀，就别因价格波动卖出。"),
 ],
 "cases":"可口可乐、喜诗、GEICO 都是持有几十年的标的；喜诗靠品牌溢价持续吐现金，GEICO 靠低成本一点点吃掉市场，时间越长优势越明显。",
 "myths":[
  "以为长期持有就不用做功课：恰恰相反，买入前的研究要更深。",
  "以为『永远持有』：前提是护城河没被侵蚀，行业环境剧变时巴菲特也会减仓。",
 ],
 "quotes":[
  ("我们最喜欢的持有期是永远。",""),
 ],
 "related":["moat","compounding","margin","market","intrinsic","circle"],
},
{
 "id":"compounding","name":"复利","en":"Compounding","cat":"核心理念","deep":True,
 "def":"收益再投资产生的新收益，时间越长雪球越大——巴菲特财富的核心引擎。",
 "points":[
  ("时间是朋友，也是放大器","早一点开始、少中断，复利的曲线会在后期陡然发力。"),
  ("高回报率的持久性比起点重要","护城河保证高回报能持续，复利才不会被打断；一次性高收益没用。"),
  ("避免永久性损失是第一要务","安全边际保护本金不被清零，复利进程一旦中断就很难追上。"),
 ],
 "cases":"伯克希尔旗下保险浮存金长期以低成本滚存再投资，是复利机器的燃料；喜诗糖果把利润持续投回生意，70 年代买下后几十年不断产生现金。",
 "myths":[
  "只看收益率不看持续性：没有护城河的高收益会被竞争抹平。",
  "忽视中断成本：一次大幅本金损失，需要极高收益才能填回。",
 ],
 "quotes":[
  ("人生就像滚雪球，重要的是找到很湿的雪和很长的坡。",""),
 ],
 "related":["hold","moat","margin","float","allocation","retained"],
},
{
 "id":"allocation","name":"资本配置","en":"Capital Allocation","cat":"组合与配置","deep":True,
 "def":"把利润投向哪里——扩业务、收购、还债、回购、分红，是 CEO 最重要的工作。",
 "points":[
  ("第一选择是加宽自己的护城河","子公司的留存利润，优先投在能提高效率、延伸产品线、拓宽护城河的项目上。"),
  ("没有好项目就还给股东","当内部回报不如买回被低估的自家股票，回购就是最优配置；反之乱投只会毁灭价值。"),
  ("配置能力决定复利快慢","同一笔利润，配得好是加速器，配得差是漏勺。"),
 ],
 "cases":"伯克希尔把保险浮存金和子公司现金流集中到奥马哈做配置，投出 GEICO、BNSF、苹果等；2010 年后也大量回购被低估的伯克希尔股票，把资本还给价值最确定的『自家生意』。",
 "myths":[
  "以为增长就是好：低回报的扩张是在消耗资本，不如不增长。",
  "以为分红永远好：当留存收益再投资回报高于股东自己能赚的，不分红反而更优。",
 ],
 "quotes":[
  ("配置资本是我们最核心的工作，比运营单个业务更重要。",""),
 ],
 "related":["retained","buyback","float","moat","acquisition","shareholder"],
},
{
 "id":"float","name":"保险浮存金","en":"Insurance Float","cat":"保险与金融","deep":True,
 "def":"保户交的保费在理赔前先由保险公司持有，这笔『暂管』资金就是浮存金。",
 "points":[
  ("是零成本甚至负成本的杠杆","只要承保不亏（综合成本率低于 100%），浮存金等于别人贴钱让你投资。"),
  ("期限长、无到期日","相比有期限的借款，浮存金可以长期滚存，是复利引擎的燃料。"),
  ("前提是承保纪律","如果为了冲规模乱定低价，浮存金会变成昂贵负债。"),
 ],
 "cases":"伯克希尔靠国民保险、GEICO、通用再保险等攒下上千亿浮存金，再以长线股票和收购投向可口可乐、BNSF 等。这是伯克希尔与普通保险公司最本质的区别。",
 "myths":[
  "以为浮存金是免费午餐：前提是承保盈利，否则就是负债。",
  "把浮存金当普通借款：它没有到期日、成本可为零，属性完全不同。",
 ],
 "quotes":[
  ("浮存金是我们持有的、不归属于我们的资金，只要承保不亏，它就是免费的资金。",""),
 ],
 "related":["underwriting","insurance","allocation","compounding","leverage"],
},
{
 "id":"concentration","name":"集中投资","en":"Concentration","cat":"组合与配置","deep":True,
 "def":"真正看懂的生意没几个，看准了就下重注，而不是撒胡椒面。",
 "points":[
  ("能力圈的自然推论","你真正理解的企业不会太多，与其广撒网，不如在少数确信的标的上集中。"),
  ("安全边际充裕时才敢集中","只在价格远低于价值、且自己看得懂时，才把仓位加到有意义的比重。"),
  ("集中不等于全仓押注","是相对于『过度分散』而言，仍留有余地应对误判。"),
 ],
 "cases":"巴菲特合伙时期少数几只重仓（美国运通、迪士尼等）贡献了大部分收益；伯克希尔后期在苹果上集中下注，成为单一最大持仓，逻辑是『看得懂的消费生态』。",
 "myths":[
  "把集中当孤注一掷：集中是建立在深度研究和安全边际上的，不是赌徒式全押。",
  "以为分散一定更安全：持有几十只看不懂的股票，风险未必比几只看懂的小。",
 ],
 "quotes":[
  ("把所有鸡蛋放在一个篮子里，然后好好看住那个篮子。",""),
 ],
 "related":["diversification","circle","margin","intrinsic","efficient"],
},
{
 "id":"diversification","name":"分散投资","en":"Diversification","cat":"组合与配置","deep":True,
 "def":"把安全边际分散到多笔投资上，用概率抵消个体的判断误差。",
 "points":[
  ("是安全边际的组合版","单笔的安全边际缓冲个体误判，多笔叠加形成概率上的整体保护。"),
  ("巴菲特真正信的是适度集中","他反对过度分散（为分散而买看不懂的），但早期低估类也靠多只分散降低永久损失风险。"),
  ("分散的边界在能力圈","只在自己懂的范围内分散，而不是跨圈乱买。"),
 ],
 "cases":"合伙时期他买一批『黯淡无光、没有催化剂』的便宜股，每只都有安全边际，合起来既安全又有上涨潜力；这与后来集中买苹果并不矛盾——前提是都看得懂。",
 "myths":[
  "以为分散能消除风险：它只减永久损失风险，且前提是每笔都真有安全边际。",
  "把『买很多只』当专业：买一堆看不懂的，只是把无知分散了。",
 ],
 "quotes":[
  ("分散是对无知的一种保护。如果你知道自己在做什么，分散的意义就不大。",""),
 ],
 "related":["concentration","margin","circle","efficient","undervaluation"],
},
{
 "id":"price","name":"买入价格","en":"Purchase Price","cat":"估值与价格","deep":True,
 "def":"你付出的价格，决定了这笔投资的安全边际大小和最终回报。",
 "points":[
  ("价格直接决定安全边际","同样一家好公司，买贵了安全边际薄，买便宜了缓冲厚。"),
  ("好公司也可能买贵","巴菲特承认为卡夫亨氏付出了过高价格，伟大企业买贵了回报照样平庸。"),
  ("价格要对照内在价值看","不看绝对贵贱，看相对价值的落差。"),
 ],
 "cases":"华盛顿邮报用两毛买一块、可口可乐在合理价买到伟大生意、卡夫亨氏高价接盘反成教训——同一套逻辑，价格不同结果天差地别。",
 "myths":[
  "以为好公司任何时候都该买：好公司买贵了，安全边际就消失。",
  "只看市价高低：贵贱是相对内在价值而言的。",
 ],
 "quotes":[
  ("价格是你付出的，价值是你得到的。",""),
 ],
 "related":["margin","intrinsic","undervaluation","hold","moat"],
},
{
 "id":"buyback","name":"回购","en":"Buyback","cat":"估值与价格","deep":True,
 "def":"公司用现金买回自家股票，是资本配置的一种重要方式。",
 "points":[
  ("低于内在价值时回购最划算","用便宜价收回被低估的股票，等于替剩下的股东增厚每股价值。"),
  ("高于价值回购是毁灭价值","为做表面业绩高价回购，和长期持有自己看不懂的资产一样糟。"),
  ("是配置的最后一道选择题","没更好的内部投资机会时，把资本这样还给股东往往最优。"),
 ],
 "cases":"伯克希尔在 2010 年后大量回购自身股票，标准是市价明显低于内在价值；巴菲特认为这比瞎投一个低回报项目强。",
 "myths":[
  "以为回购永远利好：高于价值回购是在烧钱。",
  "把回购当股价支撑工具：动机应是价值，不是托市。",
 ],
 "quotes":[
  ("当股价低于内在价值时，回购是为股东做的最稳妥的增值动作之一。",""),
 ],
 "related":["intrinsic","allocation","retained","shareholder","price"],
},
{
 "id":"franchise","name":"特许经营权","en":"Franchise","cat":"核心理念","deep":True,
 "def":"拥有定价权、不受完全竞争约束的生意，是护城河概念的雏形。",
 "points":[
  ("定价权是核心标志","能在不流失客户的前提下年年涨价，就是特许经营权的体现。"),
  ("是护城河的思想前身","巴菲特早年的『特许经营权』，后来发展成『护城河』框架。"),
  ("会退化成普通企业","媒体业就是活例子：曾经的特许权被技术革命侵蚀成普通生意。"),
 ],
 "cases":"可口可乐、喜诗糖果靠品牌和心智占有拥有定价权；报业、电视台曾因牌照垄断享特许权，互联网兴起后护城河被填平。",
 "myths":[
  "以为特许经营权永恒：它会被技术、消费偏好变化侵蚀。",
  "把规模大当特许权：规模不等于定价权。",
 ],
 "quotes":[
  ("真正伟大的生意，是那些拥有定价权、受竞争冲击小的特许经营权。",""),
 ],
 "related":["moat","brand","advantage","inflation","media"],
},
{
 "id":"brand","name":"品牌","en":"Brand Power","cat":"核心理念","deep":True,
 "def":"消费者心智中根深蒂固的认知与偏好，是企业定价权的根本来源。",
 "points":[
  ("是无形却跨时空的经济资产","好品牌不靠厂房设备，却能跨越地理和年代持续产生溢价。"),
  ("护城河的两大来源之一","强品牌如可口可乐、吉列、喜诗，消费者愿付溢价且价格弹性极低。"),
  ("品牌也会老化","消费偏好转移、新渠道冲击，都会慢慢侵蚀看似坚固的品牌价值。"),
 ],
 "cases":"可口可乐全球软饮约 44% 份额、吉列剃须刀全球六成以上份额，都是品牌护城河标杆；卡夫亨氏在电商时代被新品牌分流，说明老字号并非永恒。",
 "myths":[
  "把知名度当品牌力：知名不代表消费者愿付溢价。",
  "以为品牌价值恒定：它会被偏好和渠道变迁慢慢啃掉。",
 ],
 "quotes":[
  ("品牌的力量、产品的特质和分销体系的优势，赋予它们巨大的竞争优势，犹如一道宽阔的护城河。","1993 年股东信"),
 ],
 "related":["moat","franchise","advantage","retail","consumer"],
},
{
 "id":"advantage","name":"竞争优势","en":"Competitive Advantage","cat":"核心理念","deep":True,
 "def":"企业相对对手持久、可防御的优势地位，是护城河这个比喻的具体所指。",
 "points":[
  ("护城河是比喻，优势是内容","城堡外的壕沟是比喻，壕沟里装的是什么——成本、品牌、网络、转换成本——才是真正的竞争优势。"),
  ("要『持久且可防御』","一时的领先不算，要能长期挡住对手进攻。"),
  ("决定资本回报率高低","持续的竞争优势，是企业长期维持高于行业平均资本回报的根本。"),
 ],
 "cases":"GEICO 的结构性低成本、穆迪评级寡头地位、铁路不可复制的网络，都是具体竞争优势；纺织业则几乎没有，所以长期回报差。",
 "myths":[
  "把短期领先当优势：潮流退去就没了。",
  "以为规模即优势：无差异化的规模只是大而已。",
 ],
 "quotes":[
  ("竞争优势，是一家企业相对于对手所能长期维持的、可防御的优势地位。",""),
 ],
 "related":["moat","franchise","brand","circle","industry"],
},
{
 "id":"retained","name":"留存收益","en":"Retained Earnings","cat":"估值与价格","deep":True,
 "def":"公司不分红、留下来再投资的利润，是复利的内部燃料。",
 "points":[
  ("留存与否看再投资回报","如果每 1 元留存能创造超过 1 元价值，就该留；否则分给股东更好。"),
  ("是资本配置的起点","留存收益投向加宽护城河还是乱扩张，决定股东长期利益。"),
  ("与回购、分红构成三选一","留、分、回购，哪样对股东最划算就选哪样。"),
 ],
 "cases":"伯克希尔几乎不分红，把收益长期留存再投资，滚成保险、铁路、能源等版图；喜诗糖果把利润持续投回生意，几十年不停吐现金。",
 "myths":[
  "以为不分红就是好：留存若回报低于股东自投，就是在浪费。",
  "把留存当天然权利：管理层要证明再投资确实更划算。",
 ],
 "quotes":[
  ("公司留存的每一元，至少要为股东创造超过一元的价值。",""),
 ],
 "related":["allocation","buyback","dividend","compounding","shareholder"],
},
{
 "id":"shareholder","name":"股东导向","en":"Shareholder Orientation","cat":"组合与配置","deep":True,
 "def":"管理层把股东利益放在第一位，是信任和长期合作的基础。",
 "points":[
  ("是资本配置正确与否的底层","不站在股东这边，加宽护城河、理性回购都无从谈起。"),
  ("言行一致才算数","分红、回购、薪酬、信息披露都朝股东利益对齐，才是真导向。"),
  ("与诚信、文化是一套"," shareholder orientation 依赖管理层的诚信和对长期关系的看重。"),
 ],
 "cases":"伯克希尔旗下子公司的管理者很多经营几十年、把公司当自己的事业；巴菲特与芒格的长期信披风格，也是股东导向的体现。",
 "myths":[
  "把口号当导向：看行动（薪酬、回购、披露）而非漂亮话。",
  "以为大股东天然被代表：仍需治理机制保障小股东。",
 ],
 "quotes":[
  ("我们用对待自家钱的态度，对待股东的钱。",""),
 ],
 "related":["allocation","integrity","culture","governance","buyback"],
},

# ===== 投资概念数据 =====
{
 "id":"dividend","name":"股息","en":"Dividends","cat":"估值与价格","deep":True,
 "def":"公司把利润以现金形式分给股东，是资本返回的其中一种方式。",
 "points":[
  ("分不分看再投资回报","留存再投资回报高就不该分；回报低才该分。伯克希尔长期不分红，正是认为自有配置比股东自投更划算。"),
  ("与回购、留存构成配置三选一","哪一种对股东最划算，管理层就选哪一种，没有「分红一定好」的教条。"),
  ("税负影响税后价值","分红要缴税、回购延税，长期复利下差别巨大，不能脱离税后回报谈分红优劣。"),
 ],
 "cases":"伯克希尔自 1967 年以来几乎不分红，把利润留存再投资滚成保险、铁路、能源版图；而旗下部分成熟子公司把多余现金以股息形式返给母公司，用于集团层面的再配置。苹果等持股公司的股息则计入伯克希尔的透视盈余。",
 "myths":[
  "以为分红一定对股东好：当留存收益再投资回报高于股东自投，不分红反而更优。",
  "把高股息率当安全：高股息可能来自股价暴跌或不可持续的派息，须看可持续性。",
 ],
 "quotes":[("股息不是目的，股东每元资本的长期增值才是。","")],
 "related":["retained","buyback","allocation"],
},
{
 "id":"bookvalue","name":"账面价值","en":"Book Value","cat":"估值与价格","deep":True,
 "def":"会计报表上的净资产（资产减负债），是历史成本数字，不等于企业真实价值。",
 "points":[
  ("与内在价值常差很远","账面只记历史成本与摊销，会低估品牌、用户网络等无形价值，也会高估过时设备。"),
  ("巴菲特后期刻意淡化它","伯克希尔越重权益投资，账面价值对内在价值的指示意义越差，他后来干脆不再强调。"),
  ("看它要结合经济商誉","真正值钱的经济商誉（品牌、网络、定价权）在账面几乎不体现，须另行判断。"),
 ],
 "cases":"喜诗糖果 1972 年买价 2500 万，账面净资产很低，但品牌带来的真实经济价值远超账面；伯克希尔持有大量股票，股价涨跌直接体现在权益里，账面价值与内在价值偏离越来越大，故后期以透视盈余替代。",
 "myths":[
  "把账面价值当企业值多少钱：它只是会计数，内在价值才是经济现实。",
  "以为 PB 小于 1 就便宜：若资产是注定贬值的烂生意，便宜只是假象。",
 ],
 "quotes":[("账面价值是会计数字，内在价值才是经济现实，二者经常背离。","")],
 "related":["intrinsic","goodwill","pe","margin"],
},
{
 "id":"insurance","name":"保险业","en":"Insurance","cat":"保险与金融","deep":True,
 "def":"伯克希尔的核心引擎：用承保赚浮存金，再用浮存金做长线投资。",
 "points":[
  ("双轮：承保 + 投资","承保盈利产生低成本浮存金，投资端再滚复利，这是伯克希尔模式的命门。"),
  ("GEICO 是低成本护城河典范","直销模式省掉代理佣金，成本随规模进一步摊薄，形成正循环。"),
  ("再保险扩大浮存池","通用再保险、国民保险等让伯克希尔在全球承接大额风险，浮存金规模上千亿。"),
 ],
 "cases":"伯克希尔保险板块 1967 年从国民赔偿公司起步，如今浮存金从不足 2000 万增至超 1600 亿美元且无息可用；这是它区别于普通保险公司的根本——别人靠承保微利生存，它把浮存金变成投资燃料。",
 "myths":[
  "以为保险业就是卖保单：关键在承保纪律与投资能力，缺一不可。",
  "把浮存金当免费午餐：前提是综合成本率低于 100%，否则浮存金变负债。",
 ],
 "quotes":[("保险业给了我们低成本的浮存金，这是伯克希尔奇迹的起点。","")],
 "related":["float","underwriting","moat","allocation"],
},
{
 "id":"underwriting","name":"承保纪律","en":"Underwriting Discipline","cat":"保险与金融","deep":True,
 "def":"保险定价时留出充足安全边际，宁可不接也不低价抢规模。",
 "points":[
  ("是浮存金低成本的保障","定价松一寸，浮存金就从资产变负债；纪律严，浮存金才免费。"),
  ("应对长尾意外","社会趋势（诉讼、灾害）总会带来昂贵意外，保费必须留缓冲。"),
  ("规模服从纪律","为了冲规模而低价承保，是保险业最经典的自我毁灭方式。"),
 ],
 "cases":"伯克希尔强调「宁愿少接也不亏本接」，要求综合成本率长期低于 100%；1990 年代再保险业务在行业价格战中也坚持纪律，最终在对手爆雷时捡到便宜份额。",
 "myths":[
  "以为保费越便宜越好卖：卖得多若承保亏损，浮存金就是负成本。",
  "把承保盈利当理所当然：它来自日复一日的定价纪律，不是运气。",
 ],
 "quotes":[("保费定价必须留出充足的安全边际，否则瞄准 110 到 115 的综合成本率无异于自杀。","1990 年股东信")],
 "related":["float","insurance","margin"],
},
{
 "id":"banking","name":"银行业","en":"Banking","cat":"保险与金融","deep":True,
 "def":"低成本存款基础是银行最重要的护城河，但高杠杆是核心风险。",
 "points":[
  ("护城河在低成本存款","庞大客户基数带来稳定廉价资金，是同业难复制的优势。"),
  ("管理层质量生死攸关","贷款纪律与保险承保纪律异曲同工，烂管理能毁掉好生意。"),
  ("高杠杆放大一切","银行天然高负债，一次大的信贷失误就可能吞噬多年利润。"),
 ],
 "cases":"伯克希尔曾大笔持有富国银行、美国银行等，看中的正是其低成本存款与稳健文化；但也因个别银行的治理问题吃过亏，说明银行业「人」的因素极关键。",
 "myths":[
  "以为银行都差不多：存款成本低的银行，长期 ROE 显著高于同行。",
  "把规模当安全：杠杆下规模越大，一次失误的破坏力越大。",
 ],
 "quotes":[("银行是一桩好生意，前提是别被杠杆和坏贷款拖垮。","")],
 "related":["moat","leverage","underwriting","management"],
},
{
 "id":"inflation","name":"通货膨胀","en":"Inflation","cat":"商业与行业","deep":True,
 "def":"物价普涨侵蚀固定收益和账面利润，但有定价权的企业能转嫁。",
 "points":[
  ("有定价权才扛得住","能把成本涨传导给客户的企业，通胀下反而显出护城河价值。"),
  ("伤害债券与无定价权者","固定票息被购买力侵蚀，商品化生意最难熬。"),
  ("现金与应收款也被侵蚀","持大量现金的企业购买力随通胀悄悄流失，须投到能保值增值的资产。"),
 ],
 "cases":"喜诗糖果、可口可乐这类有品牌溢价的企业，每年提价即可把通胀转嫁；而纺织、航空等无定价权行业，成本涨却难提价，利润被夹击。巴菲特称通胀是「最惩罚无定价权企业」的税。",
 "myths":[
  "以为所有实物资产都抗通胀：无定价权的商品化资产，涨价也保不住利润。",
  "以为通胀对股票中性：有护城河的股票能转嫁，没有的会被吞噬。",
 ],
 "quotes":[("通胀是一种税，它最惩罚那些没有定价权的企业。","")],
 "related":["franchise","brand","bonds","goodwill"],
},
{
 "id":"textiles","name":"纺织业务","en":"Textile Business","cat":"商业与行业","deep":True,
 "def":"伯克希尔早期的主业，也是巴菲特学到「没有护城河」代价最贵的课。",
 "points":[
  ("几乎没有护城河","同质化竞争、无定价权，资本投进去如泥牛入海。"),
  ("转型起点","纺织现金流催生了保险收购，是伯克希尔从制造转向金融的契机。"),
  ("越早认赔越省","在没前景的生意上「再坚持一下」，往往亏得更多。"),
 ],
 "cases":"1960 年代伯克希尔旗下纺织厂持续投入新设备，回报却一降再降；巴菲特最终关停纺织业务，把资本转去保险，成就了后来的伯克希尔。这是「能力圈」与「护城河」最痛的实证课。",
 "myths":[
  "以为老牌实业一定稳：没有结构性优势，再老牌也会被成本与竞争拖垮。",
  "以为坚持就有回报：在坏生意上坚持，只是把亏损时间拉长。",
 ],
 "quotes":[("纺织业教会我什么是真正的竞争优势——因为它几乎没有。","")],
 "related":["moat","advantage","allocation","industry"],
},
{
 "id":"goodwill","name":"商誉","en":"Goodwill","cat":"估值与价格","deep":True,
 "def":"收购价超出被购方账面净资产的部分，常对应强大的护城河。",
 "points":[
  ("经济商誉才值钱","品牌、网络、定价权这类无形资产，通胀期反倒显威力，且无需追加资本。"),
  ("有别于会计商誉","账面上的摊销数字，不等于真实经济商誉的价值，甚至常低估它。"),
  ("好生意的收购溢价是投资不是费用","为护城河付溢价，换来的超额回报远高于账面摊销成本。"),
 ],
 "cases":"收购喜诗糖果时付的溢价相对其微薄账面净资产，对应其品牌溢价，后来每年吐出超额现金；收购可口可乐（一级市场参与）、BNSF 等，经济商誉都远超市账面的记录。",
 "myths":[
  "把会计商誉当资产质量：账面摊销是规则产物，不等于真实经济价值。",
  "以为高溢价收购一定糟：为真正的护城河付溢价，长期看是划算的。",
 ],
 "quotes":[("真正值钱的是经济商誉——它不需要资本投入就能维持。","")],
 "related":["moat","brand","bookvalue","franchise"],
},
{
 "id":"undervaluation","name":"低估","en":"Undervaluation","cat":"估值与价格","deep":True,
 "def":"市价显著低于保守估计的内在价值，是安全边际出现的土壤。",
 "points":[
  ("来自市场先生情绪低落","黯淡无光、无短期催化剂的标的，才容易便宜到有价值。"),
  ("低估加能力圈才安全","看不懂的便宜，只是价值陷阱的伪装。"),
  ("低估会自我修复","价格终会向价值回归，但时间不确定，需要耐心与不被迫卖出。"),
 ],
 "cases":"1960 年代合伙期巴菲特大量买入「烟蒂股」（价格远低于净营运资本），靠分散与折价获利；华盛顿邮报、中石油（港股）等也是在其被市场冷落时买入的经典低估案例。",
 "myths":[
  "以为便宜就不会更便宜：低估可以持续很久甚至更低估，需要承受波动。",
  "把「看起来便宜」当真便宜：必须确认清算或重置价值支撑，而非单纯低 PE。",
 ],
 "quotes":[("付出的价格低，得到的价值高，每笔低估投资都自带可观的安全边际。","1961 年合伙人信")],
 "related":["margin","price","market","circle"],
},
{
 "id":"pe","name":"市盈率","en":"P/E Ratio","cat":"估值与价格","deep":True,
 "def":"股价除以每股收益，是估值参考之一，但不能单独判定贵贱。",
 "points":[
  ("低 PE 不一定便宜","若内在价值对应的合理 PE 更低，低 PE 仍无安全边际。"),
  ("高 PE 未必贵","伟大企业成长能撑起高 PE，价格仍可能低于内在价值。"),
  ("要结合资本回报与增长","同样的 PE，高 ROIC 且能再投资的企业，远比低 ROIC 的值钱。"),
 ],
 "cases":"巴菲特 1988 年买可口可乐时市盈率并不低，但他算出内在价值远高于市价，安全边际依然充裕；反之一些低 PE 的烂生意，事后证明是价值陷阱。",
 "myths":[
  "把低 PE 当安全边际：PE 低可能是市场正确反映衰败前景。",
  "用 PE 跨行业比较：资本结构、成长阶段不同，PE 不可直接比。",
 ],
 "quotes":[("PE 只是起点，价格相对价值的落差才是关键。","")],
 "related":["intrinsic","bookvalue","margin","lookthrough"],
},
{
 "id":"lookthrough","name":"透视盈余","en":"Look-through Earnings","cat":"估值与价格","deep":True,
 "def":"把伯克希尔自身利润加上持股公司的留存收益按比例合并看的真实盈利。",
 "points":[
  ("比报表利润更真实","很多优质持股的利润被留存再投资，报表上却看不见。"),
  ("与内在价值增长挂钩","透视盈余的增长，更能反映股东真实财富积累。"),
  ("解释为何不看重短期 EPS","报表 EPS 受已实现损益影响大，透视盈余更稳更本质。"),
 ],
 "cases":"伯克希尔持有可口可乐、美国运通等大量股权，这些公司把利润留存再投资，伯克希尔账面上只体现分红部分；用透视盈余口径，才能看出其真实盈利规模与增长。",
 "myths":[
  "以为报表利润就是全部盈利：大量留存收益在报表外创造价值。",
  "用账面 EPS 评判伯克希尔：失真于其投资型结构。",
 ],
 "quotes":[("我们看的是透视盈余，而不只是账面上归属我们的那部分。","")],
 "related":["intrinsic","retained","allocation","pe"],
},
{
 "id":"tax","name":"税收效率","en":"Tax Efficiency","cat":"估值与价格","deep":True,
 "def":"少交税等于多留复利，是长期财富被忽视的杠杆。",
 "points":[
  ("长期持有延税","不频繁交易，资本利得税就一直不触发，复利不被打断。"),
  ("结构影响税后回报","回购 vs 分红、不同账户结构，税后结果差很多。"),
  ("税是确定的，回报是不确定的","税是少数能提前规划的事，别让它偷走复利。"),
 ],
 "cases":"伯克希尔极少分红、长期持有，让资本利得税一直延后；旗下保险浮存金的投资收益也享有税收递延优势，多年累积的税后复利差异惊人。",
 "myths":[
  "以为交易越多赚越多：频繁交易触发税费，长期严重拖累复利。",
  "忽视税后回报：税前高收益扣税后可能不如低税前但递延的。",
 ],
 "quotes":[("税收是复利最容易被忽视的拖累，能合法延就延。","")],
 "related":["compounding","dividend","buyback","allocation"],
},
{
 "id":"businessmodel","name":"商业模式","en":"Business Model","cat":"商业与行业","deep":True,
 "def":"企业怎么赚钱的底层逻辑，决定护城河能否存在。",
 "points":[
  ("简单易懂优先","巴菲特偏好能一眼看懂的生意，远离复杂黑箱。"),
  ("资本密度影响回报质量","低资本高回报（喜诗）远胜高资本低回报（飞安）。"),
  ("可复制性决定护城河深浅","别人轻易能模仿的模式，谈不上壁垒。"),
 ],
 "cases":"喜诗糖果用极小资本持续产生高回报，是「好模式」标杆；而飞安国际（飞行模拟培训）虽是好生意，却需不断投入重资产，资本回报被资本密度压低。",
 "myths":[
  "以为收入大就是好模式：重资产、低回报的大收入未必创造股东价值。",
  "把新模式当护城河：没有成本或网络壁垒的模式易被复制。",
 ],
 "quotes":[("我最喜欢那种简单、可预测、用很少资本就能赚很多钱的生意。","")],
 "related":["moat","advantage","franchise","industry"],
},
{
 "id":"energy","name":"能源","en":"Energy","cat":"商业与行业","deep":True,
 "def":"受监管公用事业，收益可预测、区域垄断构成天然护城河。",
 "points":[
  ("监管垄断是护城河","服务区域排他，竞争对手难以进入。"),
  ("代价是回报受管制上限","稳定比惊艳重要，适合巨量资本配置。"),
  ("资本密度高但可预测","需大量投入，但需求与回报相对确定。"),
 ],
 "cases":"伯克希尔能源（BHE）运营电力、天然气与新能源，在多个州拥有排他性网络；它承接巨量资本、提供稳定回报，是伯克希尔配置庞大浮存金的重要去向。",
 "myths":[
  "以为公用事业没护城河：区域垄断恰恰是最稳的护城河之一。",
  "把稳定当平庸：对巨量资本而言，确定性比高波动的回报更珍贵。",
 ],
 "quotes":[("受监管公用事业提供的是确定性，不是爆发力。","")],
 "related":["moat","allocation","rail","industry"],
},
{
 "id":"aviation","name":"航空业","en":"Aviation","cat":"商业与行业","deep":True,
 "def":"商品化、几乎没有持久护城河的典型，增长往往反噬回报。",
 "points":[
  ("缺乏结构性优势","同质化竞争、价格战，资本回报长期低迷。"),
  ("伯克希尔只碰公务机","利捷航空的经济学与商业航空截然不同。"),
  ("重资产 + 高固定成本","需求波动时极易大面积亏损。"),
 ],
 "cases":"伯克希尔曾买入四大航空股，又在 2020 年疫情中认赔清仓，结论是这个行业即使优秀管理层也难以抵御结构性劣势；其保留的利捷航空（NetJets）走的是差异化包机模式。",
 "myths":[
  "以为规模大的航空公司有护城河：同质化下规模只是更大的风险敞口。",
  "把行业增长当投资理由：没有竞争优势的增长是毒药。",
 ],
 "quotes":[("航空业教会我们：没有竞争优势的增长是毒药。","")],
 "related":["moat","advantage","textiles","industry"],
},
{
 "id":"tech","name":"科技与互联网","en":"Tech & Internet","cat":"商业与行业","deep":True,
 "def":"护城河变化太快、难判持久性，是巴菲特长期回避的原因。",
 "points":[
  ("变太快超出评估能力","今天的领先者明天可能被颠覆，确定性低。"),
  ("苹果是例外逻辑","被当消费品看（品牌加生态），而非技术路线。"),
  ("并非排斥科技，而是排斥看不懂","能看懂护城河持久性的科技生意，照样可投。"),
 ],
 "cases":"早年他回避科技股，理由是看不清护城河持久性；2016 年后大买苹果，逻辑是「消费品加生态粘性」；对谷歌、亚马逊虽认可其壁垒，但坦言自己下手偏晚。",
 "myths":[
  "以为巴菲特不懂科技：他懂，只是要求护城河可判断持久。",
  "把「不投科技」当教条：苹果已是伯克希尔最大持仓。",
 ],
 "quotes":[("我们回避科技股，不是因为它们不赚钱，而是护城河太难判断持久。","")],
 "related":["moat","circle","brand","consumer"],
},
{
 "id":"rail","name":"铁路运输","en":"Rail Transport","cat":"商业与行业","deep":True,
 "def":"线路不可复制加监管审批，构成极深的天然护城河。",
 "points":[
  ("物理资产不可复制","复制 BNSF 网络需数千亿美元和几十年，几乎不可能。"),
  ("长途货运成本优势明显","相比卡车，铁路单位能耗和排放都更低。"),
  ("资本密度高但回报可预期","一旦建成，竞争对手难以进入。"),
 ],
 "cases":"伯克希尔 2009 年收购 BNSF，获得横跨美国的铁路网络；这条网络上百年的积累、监管准入与巨额资本，构成对手无法复制的护城河，是配置巨量浮存金的核心资产。",
 "myths":[
  "以为铁路是旧经济没价值：物理壁垒恰是最深的护城河之一。",
  "把重资产当劣势：在不可复制的网络上，重资产反成门槛。",
 ],
 "quotes":[("铁路的网络 100 多年建成，任何对手都不可能复制——这是物理层面的护城河。","")],
 "related":["moat","energy","allocation","industry"],
},
{
 "id":"retail","name":"零售与消费","en":"Retail & Consumer","cat":"商业与行业","deep":True,
 "def":"定价权是消费品企业的试金石，零售护城河通常比制造窄。",
 "points":[
  ("能年年涨价不流失才是好生意","可口可乐、喜诗、吉列都具备。"),
  ("零售忠诚度有限","新竞争者随时出现，运营卓越才能维持。"),
  ("渠道变迁重塑壁垒","电商崛起重写了零售与品牌的护城河边界。"),
 ],
 "cases":"喜诗糖果靠区域心智与体验卖高价巧克力，是消费护城河典范；而传统零售商在亚马逊冲击下护城河被大幅削弱，说明消费壁垒需持续维护。",
 "myths":[
  "以为知名消费品牌永远安全：渠道与偏好变迁会侵蚀老品牌。",
  "把零售规模当护城河：低毛利零售的壁垒往往薄。",
 ],
 "quotes":[("如果你能每年涨价而不失去客户，你就拥有一门了不起的生意。","")],
 "related":["brand","franchise","moat","consumer"],
},
{
 "id":"media","name":"媒体与出版","en":"Media & Publishing","cat":"商业与行业","deep":True,
 "def":"曾经靠牌照垄断享特许权，被互联网填平护城河的典型。",
 "points":[
  ("护城河会退化","报纸分类广告垄断被 Craigslist 等线上平台瓦解。"),
  ("提醒评估持久性","看企业不能只看当前护城河宽度，要看能撑多久。"),
  ("内容价值仍在，分发壁垒消失","好内容有人看，但付费墙与广告模式被颠覆。"),
 ],
 "cases":"伯克希尔早年持有华盛顿邮报、布法罗新闻等媒体，享受过特许权红利；随互联网兴起，分类广告与订阅模式崩塌，巴菲特据此反复提醒：评估护城河必须判断其持久性。",
 "myths":[
  "以为有内容就有护城河：分发渠道失守，内容价值难变现。",
  "把历史高回报当未来保证：护城河会退化是常态。",
 ],
 "quotes":[("媒体业从特许经营权滑向普通企业，是最深刻的护城河退化教材。","1991 年股东信")],
 "related":["franchise","moat","tech","industry"],
},
{
 "id":"acquisition","name":"收购","en":"Acquisitions","cat":"治理与思维","deep":True,
 "def":"资本配置最重要的手段之一，标准是买有持久竞争优势的企业。",
 "points":[
  ("只买伟大生意","识别优秀商业模式加靠谱管理层加持久护城河。"),
  ("价格仍要讲安全边际","为亨氏付过高价，是巴菲特自己承认的教训。"),
  ("偏好整体收购而非少数股权","能完全掌控配置，避免被动。"),
 ],
 "cases":"伯克希尔的收购清单包括 GEICO、喜诗、BNSF、路博润等，共性是被收购方拥有可识别的持久护城河；卡夫亨氏则是为品牌付价过高、整合不顺的反面教材。",
 "myths":[
  "以为收购规模越大越好：贵价买平庸生意是价值毁灭。",
  "把协同效应当理由：多数协同只是故事，护城河才是实质。",
 ],
 "quotes":[("我们只收购那些我们懂、且拥有持久竞争优势的企业。","")],
 "related":["allocation","moat","management","price"],
},
{
 "id":"governance","name":"公司治理","en":"Corporate Governance","cat":"治理与思维","deep":True,
 "def":"一套让管理层对股东负责、抑制利益冲突的机制与文化。",
 "points":[
  ("与股东导向一体","没有好治理，资本配置和回购都容易跑偏。"),
  ("薪酬与披露是试金石","看管理层是否真把股东利益放第一。"),
  ("信任降低交易成本","治理好的公司，融资与并购都更顺。"),
 ],
 "cases":"伯克希尔本身以去中心化治理著称：总部仅数十人，子公司高度自治，靠文化而非庞杂流程约束管理者；这种轻治理反而降低了代理成本。",
 "myths":[
  "以为制度越多治理越好：繁文缛节不等于好治理，文化更根本。",
  "把合规当治理：合规是底线，治理还关乎利益对齐。",
 ],
 "quotes":[("好的治理，是让管理者的利益和股东的利益站在一起。","")],
 "related":["shareholder","integrity","culture","management"],
},
{
 "id":"integrity","name":"诚信","en":"Integrity","cat":"治理与思维","deep":True,
 "def":"合作伙伴与管理层的诚信，是比数据更前置的筛选条件。",
 "points":[
  ("「一言为定」也是护城河","伯克希尔的信誉让危机中的交易更容易达成。"),
  ("不诚信直接一票否决","再好的生意，人不靠谱也不碰。"),
  ("诚信降低监督成本","信得过的人，不必层层设防。"),
 ],
 "cases":"伯克希尔以「不造假、不耍滑」的声誉，在 2008 年危机中成为高盛、通用电气等争相寻求资金的对象；许多卖家也愿把公司低价卖给伯克希尔，图的是「交给孩子般的安心」。",
 "myths":[
  "以为诚信只是道德要求：它直接转化为交易机会与更低成本。",
  "把漂亮财报当诚信证据：诚信看行为，不看法条。",
 ],
 "quotes":[("我们收购的标准很简单：好的生意、好的管理层、好的价格，而人必须诚信。","")],
 "related":["culture","governance","shareholder","management"],
},
{
 "id":"culture","name":"企业文化","en":"Corporate Culture","cat":"治理与思维","deep":True,
 "def":"企业日复一日的行为习惯，是护城河被加宽还是侵蚀的土壤。",
 "points":[
  ("日常行为决定护城河走向","对客户用心、砍掉浪费，护城河就变宽。"),
  ("与股东导向、诚信配套","三者共同决定长期价值。"),
  ("文化难以复制","好文化是无形壁垒，对手抄不走。"),
 ],
 "cases":"伯克希尔总部数十年保持节俭、去中心化的文化，子公司管理者把公司当自己的事业经营几十年；这种文化让护城河在无人紧盯时仍被自然加宽。",
 "myths":[
  "以为文化虚无可测：它体现在每一次定价、招聘与资本决策里。",
  "把标语当文化：墙上写的，不等于每天做的。",
 ],
 "quotes":[("文化不是挂在墙上的标语，而是每天做出的选择。","")],
 "related":["moat","shareholder","integrity","management"],
},
{
 "id":"management","name":"管理层","en":"Management","cat":"治理与思维","deep":True,
 "def":"护城河的维护者与加宽者，是巴菲特极为看重的维度。",
 "points":[
  ("是护城河的园丁","好管理持续加宽壁垒，坏管理眼睁睁看它变窄。"),
  ("德才兼备且诚信","能力重要，但人品和资本配置观更前置。"),
  ("好管理值得放权","伯克希尔买下生意后基本不干预，信任优秀管理者。"),
 ],
 "cases":"托尼·奈斯利把 GEICO 从市占 2.5% 做到两位数、阿吉特·贾恩把再保险做成利润机器，都是「好管理加宽护城河」的范例；巴菲特强调买对管理者比买对行业更省心。",
 "myths":[
  "以为明星 CEO 能拯救坏生意：没有护城河，再强的人也难为无米之炊。",
  "把管理当唯一变量：生意本身的质地优先于管理人。",
 ],
 "quotes":[("我们买下生意后，唯一要做的就是别碍着优秀管理者的手脚。","")],
 "related":["moat","culture","integrity","acquisition"],
},
{
 "id":"forecast","name":"市场预测","en":"Market Forecast","cat":"治理与思维","deep":True,
 "def":"试图猜市场短期涨跌，巴菲特认为徒劳且无必要。",
 "points":[
  ("用内在价值替代预测","基于价值而非趋势做决定。"),
  ("不预测的自然推论是长期持有","既然无法判断买卖时机，就长期持有好生意。"),
  ("宏观预测常被噪音淹没","经济学家也常错，普通投资者更不必费劲。"),
 ],
 "cases":"巴菲特从不设市场时机模型，也不因预测衰退而空仓；2008 年危机中他反而逆市投资，理由是「价格相对价值」而非「猜底」。",
 "myths":[
  "以为不预测就无法投资：价值投资恰恰不依赖预测。",
  "把宏观观点当操作依据：短期噪音大于信号。",
 ],
 "quotes":[("我从不试图预测市场短期走向，那和猜硬币没两样。","")],
 "related":["market","intrinsic","hold","efficient"],
},
{
 "id":"efficient","name":"有效市场","en":"Efficient Market","cat":"保险与金融","deep":True,
 "def":"学术理论认为价格已反映一切信息，巴菲特用长期记录反驳它。",
 "points":[
  ("与市场先生寓言对立","若市场永远有效，价值投资无从获利。"),
  ("套利记录是反证","巴菲特 60 余年套利与低估投资，证明定价常出错。"),
  ("半强式有效都不牢靠","内幕与认知差异让价格长期偏离价值。"),
 ],
 "cases":"巴菲特合伙期靠「烟蒂股」与套利持续跑赢，长期记录本身即是对有效市场假说的反例；他笑称若市场总是有效，自己早该去路边要饭。",
 "myths":[
  "以为市场短期有效：价格常因情绪大幅偏离价值。",
  "把理论当真理：学术模型忽略人性，实践才是检验。",
 ],
 "quotes":[("如果市场总是有效，我早就该去路边要饭了。","")],
 "related":["market","margin","arbitrage","diversification"],
},
{
 "id":"arbitrage","name":"套利","en":"Risk Arbitrage","cat":"保险与金融","deep":True,
 "def":"基于已公告事件（如并购）的价差获利，是巴菲特早期的稳定策略。",
 "points":[
  ("只做公告驱动型","事件已发生，确定性高于赌未来。"),
  ("仍是安全边际的应用","只在定价有利时参与，不押没把握的。"),
  ("分散多笔降低单失误影响","与低估策略同源，靠概率而非单押。"),
 ],
 "cases":"合伙时期巴菲特大量参与并购套利（如公司宣布被收购后价差收敛），在控制风险前提下提供稳定收益；这套方法后来也用在伯克希尔的某些特殊机会上。",
 "myths":[
  "以为套利无风险：交易失败、监管否决仍会亏损。",
  "把套利当投机：公告驱动、定价有利时，本质是概率游戏。",
 ],
 "quotes":[("我们的套利只做已公告、确定性高的交易，不赌谣言。","")],
 "related":["margin","efficient","leverage","undervaluation"],
},
{
 "id":"bonds","name":"债券","en":"Bonds","cat":"保险与金融","deep":True,
 "def":"固定收益工具，最大长期威胁是通胀侵蚀购买力。",
 "points":[
  ("折价买入也是安全边际应用","大幅折价债，是安全边际在固收领域的体现。"),
  ("通胀是头号敌人","固定票息的实际购买力会被物价上涨吃掉。"),
  ("久期决定利率敏感度","长债对利率与通胀更敏感，波动更大。"),
 ],
 "cases":"伯克希尔保险资金会配置一定债券以保证流动性，但巴菲特总体偏好股权——因长期看债券跑不赢能转嫁通胀的优质企业；危机时他也买过极度折价的公司债套利。",
 "myths":[
  "以为债券绝对安全：通胀与违约都会吞噬本金。",
  "把高收益债当无风险：信用利差本质是风险定价。",
 ],
 "quotes":[("债券的敌人是通胀，它悄悄拿走你的购买力。","")],
 "related":["inflation","compounding","margin","leverage"],
},
{
 "id":"derivatives","name":"衍生品","en":"Derivatives","cat":"保险与金融","deep":True,
 "def":"复杂性高、隐含杠杆，巴菲特称其为「金融大规模杀伤性武器」。",
 "points":[
  ("复杂性使安全边际难估","条款嵌套，真实风险难以穿透。"),
  ("伯克希尔仅在有把握时参与","如用作获取浮存金的工具，且只在定价有利时。"),
  ("对手方风险隐蔽","违约连锁反应可放大损失。"),
 ],
 "cases":"伯克希尔早年卖出长期股票指数看跌期权（收取权利金、做「保险」），因定价有利且期限极长，最终盈利；但巴菲特反复警告，复杂衍生品在危机中会变成无人能估的黑洞。",
 "myths":[
  "以为对冲总能降风险：错配的对冲反而加风险。",
  "把模型定价当真实风险：模型假设在极端时失效。",
 ],
 "quotes":[("衍生品是金融领域的大规模杀伤性武器，要极度谨慎。","")],
 "related":["leverage","float","margin","insurance"],
},
{
 "id":"convertible","name":"可转换证券","en":"Convertible Securities","cat":"保险与金融","deep":True,
 "def":"兼具债底与转股权，「下有保底、上不封顶」的结构。",
 "points":[
  ("固定收益底就是安全边际","价值不会低于同等不可转换优先股。"),
  ("是介于股债间的配置选择","确定性低时选债底，确定性高时享上行。"),
  ("巴菲特爱在危机时用","恐慌时发行的可转债条款往往有利。"),
 ],
 "cases":"伯克希尔在 1980–90 年代常通过优先股（常附可转换权）向高盛、所罗门、美国航空等注资，既拿固定票息又保留上行参与，是「好杠杆」式的配置。",
 "myths":[
  "以为可转债稳赚：转股标的暴跌时，债底也未必安全。",
  "把转换权当免费期权：条款（转股价、期限）决定真实价值。",
 ],
 "quotes":[("可转换证券的价值，首先来自它作为固定收益的底。","1990 年股东信")],
 "related":["margin","allocation","leverage","intrinsic"],
},
{
 "id":"leverage","name":"杠杆","en":"Leverage","cat":"保险与金融","deep":True,
 "def":"借钱放大收益也放大风险；伯克希尔偏好「好杠杆」浮存金。",
 "points":[
  ("反杠杆是安全边际的资产负债表版","高杠杆让一次误判就归零。"),
  ("浮存金是「好杠杆」","无到期日、成本可为零甚至为负。"),
  ("危机中低杠杆即优势","别人被迫平仓时，你还有子弹。"),
 ],
 "cases":"伯克希尔长期保持极低的有息负债，却持有上千亿零成本浮存金；2008 年别人去杠杆时，它反手向高盛、通用电气注资，靠的就是稳健的资产负债表。",
 "myths":[
  "以为杠杆放大收益就值得：它同样放大亏损，且常在最糟时触发。",
  "把浮存金当普通借款：它无到期、可零成本，属性完全不同。",
 ],
 "quotes":[("我厌恶毫无必要的债务，但喜欢低成本、无期限的浮存金这种好杠杆。","")],
 "related":["margin","float","derivatives","bonds"],
},
]

CATS = ["全部","核心理念","估值与价格","组合与配置","保险与金融","商业与行业","治理与思维"]

def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def render_body(c):
    h = []
    h.append(f'<p class="c-def">{esc(c["def"])}</p>')
    # 核心要义
    h.append('<h3 class="c-h">核心要义</h3>')
    if c.get("deep"):
        for t,b in c["points"]:
            h.append(f'<div class="point"><b>{esc(t)}</b><p>{esc(b)}</p></div>')
    else:
        for t,b in c["points"]:
            h.append(f'<div class="point"><b>{esc(t)}</b><p>{esc(b)}</p></div>')
    if c.get("cases"):
        h.append('<h3 class="c-h">巴菲特的实践</h3>')
        h.append(f'<p class="c-case">{esc(c["cases"])}</p>')
    if c.get("myths"):
        h.append('<h3 class="c-h">常见误区</h3><ul class="myth">')
        for m in c["myths"]:
            h.append(f'<li>{esc(m)}</li>')
        h.append('</ul>')
    if c.get("quotes"):
        h.append('<h3 class="c-h">巴菲特原话</h3>')
        for q,y in c["quotes"]:
            ytxt = f'<span class="qy">—— {esc(y)}</span>' if y else ''
            h.append(f'<blockquote class="quote">{esc(q)}{ytxt}</blockquote>')
    if c.get("related"):
        h.append('<h3 class="c-h">相关概念</h3><div class="rel">')
        for rid in c["related"]:
            rc = next((x for x in CONCEPTS if x["id"]==rid), None)
            if rc:
                h.append(f'<button class="chip" data-id="{rid}">{esc(rc["name"])}</button>')
        h.append('</div>')
    return "".join(h)

def build():
    by_id = {c["id"]:c for c in CONCEPTS}
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

    stat_deep = sum(1 for c in CONCEPTS if c.get("deep"))
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>巴菲特投资概念库 | 伯克希尔投资数据中心</title>
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
.hero p{{margin:0;color:var(--muted);max-width:760px}}
.stat{{display:inline-flex;gap:18px;margin-top:14px;flex-wrap:wrap}}
.stat b{{color:var(--navy);font-size:20px}}
.stat span{{color:var(--muted);font-size:13px;display:block}}
.controls{{max-width:1180px;margin:18px auto 0;padding:0 20px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
.search{{flex:1;min-width:240px;padding:11px 14px;border:1px solid var(--line);border-radius:10px;font-size:15px;outline:none}}
.search:focus{{border-color:var(--orange)}}
.cats{{display:flex;gap:8px;flex-wrap:wrap;max-width:1180px;margin:14px auto 0;padding:0 20px}}
.cat-btn{{border:1px solid var(--line);background:#fff;color:var(--muted);padding:7px 14px;border-radius:999px;font-size:13px;cursor:pointer}}
.cat-btn.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.cat-btn:hover{{border-color:var(--orange)}}
.grid{{max-width:1180px;margin:22px auto 60px;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.card{{text-align:left;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 16px 18px;cursor:pointer;transition:.15s;position:relative;overflow:hidden}}
.card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(11,31,58,.12);border-color:var(--orange)}}
.card-top{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
.card-name{{font-size:17px;font-weight:700;color:var(--navy)}}
.card-en{{color:var(--muted);font-size:12px;margin:2px 0 8px;letter-spacing:.3px}}
.card-def{{font-size:13.5px;color:#41506a;line-height:1.6}}
.tag-deep{{font-size:11px;color:#fff;background:var(--orange);padding:2px 8px;border-radius:999px;white-space:nowrap}}
.tag-lite{{font-size:11px;color:var(--navy);background:#eaf0f8;padding:2px 8px;border-radius:999px;white-space:nowrap}}
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
.note{{background:#eaf0f8;border-radius:10px;padding:12px 14px;margin-top:12px;color:#42526a}}
</style>
</head>
<body>
<header class="top">
  <div class="top-in">
    <h1>伯克希尔·<b>投资概念库</b></h1>
    <div class="crumb"><a href="berkshire-standalone.html">首页</a> / 投资数据中心 / 概念库</div>
  </div>
</header>
<section class="hero">
  <h2>巴菲特投资概念</h2>
  <p>收录巴菲特投资体系中的 49 个核心概念。每个词条包含定义、核心要义、实践案例、常见误区与原文精选，并交叉链接至本站年会实录与业务/投资版图。</p>
  <div class="stat">
    <div><b>{len(CONCEPTS)}</b><span>概念词条</span></div>
    <div><b>{stat_deep}</b><span>深度解析</span></div>
    <div><b>6</b><span>大分类</span></div>
    <div><b>交叉</b><span>年会 · 版图</span></div>
  </div>
</section>
<div class="controls">
  <input class="search" id="search" placeholder="搜索概念，如：护城河 / 安全边际 / moat">
</div>
<div class="cats" id="cats">{cat_btns}</div>
<main class="grid" id="grid">
{''.join(cards)}
</main>
<footer>
  <p>伯克希尔投资数据中心 · 概念库 | 与年会实录、业务版图、投资版图平行 | 单文件静态页</p>
</footer>
{''.join(modals)}
<script>
const grid=document.getElementById('grid');
const cards=[...grid.querySelectorAll('.card')];
const search=document.getElementById('search');
const catBtns=[...document.querySelectorAll('.cat-btn')];
let curCat='全部';
function applyFilter(){{
  const q=search.value.trim().toLowerCase();
  cards.forEach(c=>{{
    const name=c.dataset.name.toLowerCase();
    const en=c.dataset.cat.toLowerCase();
    const okCat=curCat==='全部'||c.dataset.cat===curCat;
    const okQ=!q||name.includes(q)||en.includes(q)||c.querySelector('.card-en').textContent.toLowerCase().includes(q);
    c.style.display=(okCat&&okQ)?'':'none';
  }});
}}
search.addEventListener('input',applyFilter);
catBtns.forEach(b=>b.addEventListener('click',()=>{{
  catBtns.forEach(x=>x.classList.remove('active'));
  b.classList.add('active');curCat=b.dataset.cat;applyFilter();
}}));
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
</script>
</body>
</html>'''
    return html

if __name__ == "__main__":
    out = build()
    with open("berkshire-concepts.html","w",encoding="utf-8") as f:
        f.write(out)
    print("written berkshire-concepts.html, concepts=", len(CONCEPTS))
