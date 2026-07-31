import sys, json, re, akshare as ak
code = '000703'
df = ak.stock_fhps_detail_ths(symbol=code)
rows = df.to_dict('records')
cand = None
for d in reversed(rows):
    s = str(d.get('\u5206\u7ea2\u65b9\u6848\u8bf4\u660e', ''))
    if '\u6d3e' in s and d.get('\u65b9\u6848\u8fdb\u5ea6') in ('\u5b9e\u65bd\u65b9\u6848', '\u80a1\u4e1c\u5927\u4f1a\u9884\u6848'):
        cand = s; break
m = re.search(r'[\u6d3e\u53d1]\s*([0-9]+(?:\.[0-9]+)?)\s*\u5143', cand) if cand else None
print(json.dumps({'desc': cand, 'dps': float(m.group(1))/10.0 if m else None}, ensure_ascii=False))
