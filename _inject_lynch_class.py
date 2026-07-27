# -*- coding: utf-8 -*-
"""
_inject_lynch_class.py —— 伯克希尔数据中心 · P2 增强

给每家公司的 chain 详情页注入「彼得·林奇 6 分类」公司级标签（P2 项）。
- 锚点（优先级链，覆盖全站 174 详情页）：data-banner > <h1> > hero-title。
  已含 `lynch-tag` 标记则跳过（幂等）。
- 分类来源：逐链默认分类(CHAIN_LYNCH) + 重点公司 override(OVERRIDE)。
  属框架级启发式标签，非研究结论；已在标签里声明"非买卖建议"。
- 幂等：已含 `lynch-tag` 标记则跳过。

用法：python _inject_lynch_class.py
"""
import glob
import os
import re

import inject_annual_reports as ia

ROOT = os.path.dirname(os.path.abspath(__file__))

# 林奇 6 分类：缓慢增长 / 稳健 / 周期 / 成长 / 困境 / 资产
CHAIN_LYNCH = {
    "bank": "稳健型（大笨象 · 息差敏感）",
    "baijiu": "稳健型（消费防御 · 定价权分化）",
    "ai": "成长型（高资本开支 · 高不确定）",
    "robot": "成长型（主题高波动 · 量产鸿沟）",
    "tcm": "稳健型（消费防御 · 稀缺性）",
    "innov": "成长 / 困境并存（研发驱动 · BD 兑现）",
    "appliance": "稳健型（消费防御 · 出海）",
    "power": "周期 / 公用事业（煤价 · 电价敏感）",
    "coal": "周期型（现金牛 · 高分红）",
    "metal": "周期型（商品驱动 · 全球定价）",
    "chem": "周期型（价差驱动 · 产能周期）",
    "equip": "成长 / 周期（产能周期 · 技术迭代）",
}

# 重点公司 override（slug -> 林奇分类文案），其余走链默认
OVERRIDE = {
    # 煤炭：现金牛+高分红
    "shenhua": "周期型 · 现金牛 + 高分红", "shaanxi": "周期型 · 现金牛 + 高分红",
    "yanzhou": "周期型 · 现金牛 + 高分红", "zhongmei": "周期型 · 现金牛 + 高分红",
    "pingmei": "周期型 · 现金牛 + 高分红", "luan": "周期型 · 现金牛 + 高分红",
    "jizhong": "周期型 · 现金牛 + 高分红", "huaibei": "周期型 · 现金牛 + 高分红",
    "sxjh": "周期型 · 现金牛 + 高分红", "sxjk": "周期型 · 现金牛 + 高分红",
    "shanmei": "周期型 · 现金牛 + 高分红",
    # 白酒：定价权分化
    "maotai": "稳健型 · 强定价权（提价权）", "wuliangye": "稳健型 · 强定价权（提价权）",
    "luzhou": "稳健型 · 次高端弹性", "fenjiu": "稳健型 · 全国化扩张",
    "yanghe": "稳健型 · 调整期", "gujing": "稳健型 · 区域强势",
    "shede": "成长 / 困境 · 招商转民", "jiugui": "困境反转 · 改制预期",
    # 银行：系统重要/零售
    "icbc": "稳健型 · 系统重要行", "ccb": "稳健型 · 系统重要行",
    "boc": "稳健型 · 外汇优势", "abc": "稳健型 · 县域下沉",
    "psbc": "稳健型 · 普惠下沉", "cmb": "稳健型 · 零售标杆",
    "cmbc": "稳健型 · 股份行", "bobj": "稳健型 · 城商标杆",
    # 有色：商品驱动 + 个别成长矿企
    "zijin": "周期型 · 成长型矿企（铜金）", "ganfeng": "周期型 · 锂周期",
    "tianqi": "周期型 · 锂周期", "huayou": "周期型 · 镍钴产业链",
    "jiangxi": "周期型 · 稀土", "sdgold": "周期型 · 黄金",
    "chalco": "周期型 · 铝", "zhongjin": "周期型 · 黄金",
    "yunlu": "周期型 · 铝", "shenhuo": "周期型 · 铝电一体",
    "lomo": "周期型 · 铜钴钼多金属",
    # 创新药：研发驱动
    "hengrui": "成长型 · 创新药龙头", "beigene": "成长 / 困境 · 出海 BD",
    "innovent": "成长型 · 出海 BD", "kelun": "成长型 · ADC 平台",
    "akesobio": "成长 / 困境 · 临床兑现", "junshi": "成长 / 困境 · 单抗",
    # 电力设备 / 新能源装备
    "catl": "成长 / 周期 · 锂电龙头", "longi": "成长 / 周期 · 光伏",
    "tongwei": "成长 / 周期 · 硅料", "goldwind": "周期型 · 风电",
    "dongfang": "周期型 · 风光储", "sungrow": "成长型 · 逆变器",
    "trina": "成长 / 周期 · 组件", "jinko": "成长 / 周期 · 组件",
    "nari": "稳健型 · 电网设备",
    # 机器人 / 汽零
    "tuopu": "成长型 · 汽配", "huichuan": "成长型 · 工控",
    "estun": "成长型 · 工业机器人", "orbbec": "成长型 · 视觉",
    "sanhuayd": "成长型 · 热管理", "shuanghuan": "成长型 · 减速器",
    # 中药
    "yunnanbaiyao": "稳健型 · 消费中药", "tongrentang": "稳健型 · 老字号",
    "pianzaihuang": "稳健型 · 强品牌定价权", "dong ejiao": "稳健型 · 阿胶龙头",
}


def badge(cls):
    return ('<div class="lynch-tag" style="margin:14px 0;padding:10px 14px;background:#f8fafc;'
            'border:1px solid rgba(0,0,0,.09);border-left:3px solid #a8a29e;border-radius:8px;'
            'font-size:13px;color:#475569;line-height:1.6">🏷️ <b style="color:#0f172a">林奇分类</b>：'
            '<b style="color:#1d4ed8">%s</b>　'
            '<span style="color:#94a3b8">· 彼得·林奇公司分类透镜（缓慢增长/稳健/周期/成长/困境/资产），框架标签非买卖建议</span></div>'
            % cls)


def inject_after_anchor(html, b):
    """优先级锚点链：data-banner > </h1> > hero-title。命中第一个即注入。"""
    anchors = [
        r'(<div class="data-banner">.*?</div>)',                       # 105 页（five/three_chains 等）
        r'(<h1[^>]*>.*?</h1>)',                                        # 42 页银行链
        r'(<div class="hero-title">.*?</div>)',                        # 27 页白酒/AI外企/robot-coming
    ]
    for pat in anchors:
        new = re.sub(pat, r'\1\n' + b, html, count=1, flags=re.S)
        if new != html:
            return new
    return None


def main():
    csc = ia.extract_chain_slug_code()
    pages = sorted(glob.glob(os.path.join(ROOT, "berkshire-*-chain-*.html")))
    done, skipped, missing, nomap, noanchor = 0, 0, 0, 0, 0
    for p in pages:
        m = re.search(r"berkshire-([a-z]+)-chain-([A-Za-z0-9_\-]+)\.html$", p)
        if not m:
            continue
        chain, slug = m.group(1), m.group(2)
        if (chain, slug) not in csc:
            missing += 1
            continue
        html = open(p, encoding="utf-8").read()
        if "lynch-tag" in html:
            skipped += 1
            continue
        cls = OVERRIDE.get(slug) or CHAIN_LYNCH.get(chain)
        if not cls:
            nomap += 1
            continue
        b = badge(cls)
        new = inject_after_anchor(html, b)
        if new is None:
            noanchor += 1
            continue
        open(p, "w", encoding="utf-8").write(new)
        done += 1
    print("=== 林奇 6 分类注入完成 ===")
    print("注入:", done, " 跳过(已存在):", skipped, " 未映射:", missing,
          " 无分类:", nomap, " 无锚点:", noanchor)


if __name__ == "__main__":
    main()
