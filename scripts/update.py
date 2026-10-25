import json, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEARCHES={
 '商业犯罪': 'corporate fraud OR corruption OR money laundering Malaysia',
 '政商关系': 'government procurement OR political donation OR conflict of interest Malaysia',
 '金融暗线': 'CBDC OR financial surveillance OR banking regulation',
 'AI情报': 'deepfake scam OR AI disinformation OR data poisoning',
 '灰产风险': 'scam compound OR cybercrime Southeast Asia',
 '神秘事件': 'UAP disclosure OR unidentified anomalous phenomena'
}
rows=[]; seen=set(); errors=[]
for category,q in SEARCHES.items():
    params=urllib.parse.urlencode({'q':q+' when:7d','hl':'en-MY','gl':'MY','ceid':'MY:en'})
    url='https://news.google.com/rss/search?'+params
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 BeeRadar/2.0'})
        with urllib.request.urlopen(request,timeout=18) as rsp:
            xml=rsp.read()
        tree=ET.fromstring(xml)
        for item in tree.findall('./channel/item')[:12]:
            title=(item.findtext('title') or '').strip(); link=(item.findtext('link') or '').strip()
            if not title or not link:continue
            key=re.sub(r'\W+','',title.lower())[:115]
            if key in seen:continue
            seen.add(key)
            source_node=item.find('source'); source=source_node.text.strip() if source_node is not None and source_node.text else '来源待确认'
            rows.append({'id':__import__('hashlib').sha256((title+link).encode()).hexdigest()[:16], 'title':title,'link':link,'category':category,'source':source,'published':item.findtext('pubDate') or '', 'status':'待核实','note':'自动收录的报道线索，不代表指控属实。须查原始证据与独立来源。'})
    except Exception as e: errors.append(f'{category}: {str(e)[:100]}')
    time.sleep(.25)
rows=rows[:65]
out={'updated_at':datetime.now(timezone.utc).isoformat(),'timezone':'Asia/Kuala_Lumpur','count':len(rows),'items':rows,'errors':errors}
path=ROOT/'data'/'feed.json'
if rows or not path.exists():path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Collected {len(rows)} items, {len(errors)} errors')
