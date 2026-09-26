#!/usr/bin/env python3
"""Check an Arabic AIGP module against its English source. usage: check_ar.py EN.md AR.md"""
import re,sys,collections
en,ar=open(sys.argv[1]).read(),open(sys.argv[2]).read()
def nof(s): return re.sub(r'```.*?```','',s,flags=re.S)
def heads(s): return [(len(h),(re.match(r'(\S+)',t).group(1) if h in('##','###') else re.sub(r'—.*','',t).strip())) for h,t in re.findall(r'^(#{1,3}) (.*)$',nof(s),flags=re.M)]
def lessons(s): return re.findall(r'^# (\d+\.\d+) — ',s,flags=re.M)
def lvl(s): return [(m[0],m[1]) for m in re.findall(r'^\*(?:Level|المستوى):\s*(🟢|🟡|🔴)[^*]*\*.*?(?:BoK|مجال المعرفة)[^:]*:\s*([^*]+)\*',s,flags=re.M)]
def inst(s):
    out=[]
    for sec in re.split(r'\n(?=## )',s):
        if sec.startswith('## ⚖'): out+= re.findall(r'^\|\s*\*\*([^*]+)\*\*',sec,flags=re.M)
    return out
def quiz(s): return re.findall(r'<details><summary>[^<]+</summary>\s*\n\s*\*\*([A-D])\.',s)
def opts(s): return len(re.findall(r'^- [A-D]\. ',s,flags=re.M))
def fences(s): return re.findall(r'```(\w*)\n(.*?)```',s,flags=re.S)
def icode(s): return collections.Counter(re.findall(r'`([^`\n]+)`',nof(s)))
def urls(s): return collections.Counter(re.findall(r'\]\((https?://[^)\s]+)\)',s))
err=[]
if lessons(en)!=lessons(ar): err.append(f'lessons {lessons(ar)} ≠ {lessons(en)}')
he,ha=heads(en),heads(ar)
if [h[0] for h in he]!=[h[0] for h in ha]: err.append(f'heading levels differ ({len(ha)} vs {len(he)})')
else:
    for (d,a),(d2,b) in zip(he,ha):
        if d in (2,3) and a[:1]!=b[:1]: err.append(f'section emoji differs: {a} vs {b}'); break
if lvl(en)!=lvl(ar): err.append(f'level/BoK lines differ: {lvl(ar)[:4]} vs {lvl(en)[:4]}')
if inst(en)!=inst(ar): err.append(f'⚖️ bold names differ: missing {[x for x in inst(en) if x not in inst(ar)][:5]}')
if quiz(en)!=quiz(ar): err.append(f'quiz answer letters differ ({len(quiz(ar))} vs {len(quiz(en))})')
if ar.count('<details>')!=en.count('<details>'): err.append('details block count differs')
if opts(en)!=opts(ar): err.append(f'option lines {opts(ar)} vs {opts(en)}')
fe,fa=fences(en),fences(ar)
if [f[0] for f in fe]!=[f[0] for f in fa]: err.append('fenced block count/languages differ')
else:
    for (l,a),(_,b) in zip(fe,fa):
        if l!='mermaid' and a!=b: err.append('a code block changed'); break
        if l=='mermaid' and len(a.splitlines())!=len(b.splitlines()): err.append('mermaid line count changed'); break
if icode(en)!=icode(ar): err.append(f'inline code differs: {list((icode(en)-icode(ar)))[:6]} / {list((icode(ar)-icode(en)))[:6]}')
if urls(en)!=urls(ar): err.append(f'links differ: {list((urls(en)-urls(ar)))[:4]}')
body=re.sub(r'[`|*#\-\[\]()]','',nof(ar)); a=len(re.findall(r'[؀-ۿ]',body)); t=len(re.sub(r'\s','',body))
if a/max(t,1)<0.45: err.append(f'only {a/max(t,1):.0%} Arabic script')
if err: print('✗',sys.argv[2]); [print('  -',e) for e in err]; sys.exit(1)
print(f'✓ {sys.argv[2]}: {len(lessons(ar))} lessons, {len(ha)} headings, {len(quiz(ar))} quiz answers, {len(inst(ar))} instrument rows, {a/max(t,1):.0%} Arabic')
