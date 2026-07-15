#!/usr/bin/env python3
"""Generate index.html (fast-lookup app) from print.html (canonical deck).

Card content is extracted VERBATIM from the print deck — this script never
rewrites procedures. Edit print.html (via the normal deck pipeline), then run:
    python3 tools/build_app.py
"""
import re, html, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "print.html").read_text()

BRANDS = ["Sennheiser", "Shure", "Sony", "Wisycom", "Lectrosonics",
          "Comtek", "Sound Devices", "Zaxcom"]

def slugify(t):
    t = re.sub(r"&[a-z]+;", " ", t)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")

cards = []
for sheet in src.split('<section class="sheet">')[1:]:
    h1 = re.search(r"<h1>(.*?)</h1>", sheet, re.S).group(1)
    h1 = re.sub(r"\s+", " ", h1).strip()
    if h1.startswith("Wireless Quick-Dial"):
        continue  # index/legend page — the app home replaces it
    subm = re.search(r'<div class="sub">(.*?)</div>', sheet, re.S)
    sub = re.sub(r"\s+", " ", subm.group(1)).strip() if subm else ""
    body = re.search(r'(<div class="meta">.*?)\s*<footer class="foot">', sheet, re.S).group(1)
    brand = next(b for b in BRANDS if h1.startswith(b))
    model = h1[len(brand):].strip()
    badge = re.search(r'<span class="tag ([a-z-]+)">([^<]*)</span>', body)
    cards.append(dict(slug=slugify(h1), title=h1, brand=brand, model=model,
                      sub=sub, body=body,
                      badgecls=badge.group(1), badgetxt=badge.group(2)))

assert len(cards) == 22, f"expected 16 cards, got {len(cards)}"

ISSUE = "https://github.com/gothamsound/quick-dial-cards/issues/new"
sections = []
for c in cards:
    fix = f"{ISSUE}?template=suggest-change.yml&card={urllib.parse.quote(c['title'])}&title={urllib.parse.quote('[Card change]: ' + c['title'])}"
    mailbody = urllib.parse.quote(f"Card: {c['title']}\n\nWhat it says now:\n\nWhat it should say:\n\nSource:\n\nCredit me as (or say no thanks):\n")
    sections.append(f'''<section class="card" id="{c['slug']}" data-brand="{html.escape(c['brand'])}" data-model="{html.escape(c['model'])}" data-title="{html.escape(c['title'])}" data-badgecls="{c['badgecls']}" data-badgetxt="{html.escape(c['badgetxt'])}" hidden>
<div class="cardhead"><div class="ch-brand">{html.escape(c['brand'])}</div><h2>{html.escape(c['model'])}</h2><div class="ch-sub">{c['sub']}</div></div>
{c['body']}
<div class="cardfoot"><a href="{fix}" target="_blank" rel="noopener">Something wrong on this card? Suggest a fix →</a><br>No GitHub account (you really should)? <a href="mailto:peters@gothamsound.com?subject=quickdialchange&body={mailbody}">Email it here</a>.</div>
</section>''')

page = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wireless Quick-Dial Cards — Gotham Sound</title>
<style>
:root { --ink:#16181d; --mut:#4a4f57; --grn:#2f7d52; --grn-d:#256641; --oli:#6a6f33; --amb:#b7791b; --bg:#f4f4ee; --line:#e1e1d6; }
* { box-sizing:border-box; }
html { font-size:17px; }
body { margin:0; font-family:Arial,Helvetica,sans-serif; color:var(--ink); background:var(--bg); }
a { color:var(--grn); }
header { position:sticky; top:0; z-index:50; background:#fff; border-bottom:2px solid var(--ink); padding:10px 14px; display:flex; gap:12px; align-items:center; }
header img { width:118px; height:auto; flex:none; }
#q { flex:1; min-width:0; font-size:1rem; padding:11px 13px; border:1.6px solid var(--line); border-radius:8px; background:var(--bg); }
#q:focus { outline:2px solid var(--grn); background:#fff; }
main { max-width:780px; margin:0 auto; padding:16px 14px 90px; }

/* ---------- home ---------- */
.bigask { font-size:1.45rem; margin:14px 2px 6px; letter-spacing:-.01em; }
.reassure { color:var(--mut); margin:0 2px 16px; line-height:1.45; }
#lastused { margin:0 0 14px; }
#lastused button { width:100%; text-align:left; background:#fff; border:1.6px solid var(--grn); border-left:7px solid var(--grn); border-radius:10px; padding:13px 15px; font-size:1.05rem; font-weight:700; color:var(--ink); cursor:pointer; }
#lastused .lu-k { display:block; font-size:.72rem; font-weight:800; letter-spacing:.09em; color:var(--grn); text-transform:uppercase; margin-bottom:2px; }
#brands { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }
@media(min-width:560px){ #brands { grid-template-columns:repeat(3,1fr);} }
#brands button, .modelbtn { background:#fff; border:1.6px solid var(--line); border-radius:10px; padding:16px 14px; font-size:1.12rem; font-weight:700; color:var(--ink); cursor:pointer; text-align:left; min-height:72px; }
#brands button:active, .modelbtn:active { border-color:var(--grn); }
#brands .n { display:block; font-size:.8rem; font-weight:400; color:var(--mut); margin-top:3px; }
#models, #results { display:flex; flex-direction:column; gap:10px; }
.modelbtn { display:flex; justify-content:space-between; align-items:center; gap:10px; width:100%; min-height:64px; }
.modelbtn small { display:block; font-weight:400; color:var(--mut); font-size:.8rem; margin-top:2px; }
.backrow { background:none; border:none; color:var(--grn); font-size:1rem; font-weight:700; padding:6px 2px 12px; cursor:pointer; }
.nores { color:var(--mut); padding:8px 2px; }
.homefoot { color:var(--mut); font-size:.9rem; margin-top:26px; border-top:1px solid var(--line); padding-top:14px; }

/* badge chips */
.tag { font-size:.72rem; font-weight:800; letter-spacing:.04em; color:#fff; padding:5px 10px; border-radius:4px; white-space:nowrap; }
.t-tune{background:#2f7d52}.t-grp{background:#b7791b}.t-blk{background:#4a6b86}.t-chan{background:#8a4f1d}.tag.na{background:#7a7f88}
.modelbtn .tag { flex:none; font-size:.62rem; }

/* ---------- card chrome ---------- */
#cardwrap[hidden], #home[hidden], [hidden] { display:none !important; }
.cardbar { display:flex; align-items:center; gap:10px; margin:2px 0 12px; }
.cardbar .backrow { padding:6px 2px; flex:1; text-align:left; }
.freqbox { display:flex; align-items:center; gap:7px; background:#16181d; border-radius:10px; padding:7px 12px; }
.freqbox span { font-size:.62rem; font-weight:800; letter-spacing:.08em; color:#9fe0bd; text-transform:uppercase; line-height:1.15; }
.freqbox input { width:118px; border:none; background:none; color:#fff; font-family:'DejaVu Sans Mono',Menlo,monospace; font-size:1.35rem; font-weight:700; text-align:right; }
.freqbox input:focus { outline:none; }
.freqbox b { color:#9fe0bd; font-size:.8rem; }
.cardhead { margin:0 0 10px; }
.ch-brand { font-size:.75rem; letter-spacing:.12em; font-weight:800; color:var(--oli); text-transform:uppercase; }
.card h2 { font-size:1.6rem; margin:2px 0 4px; letter-spacing:-.01em; }
.ch-sub { color:var(--mut); font-size:.92rem; line-height:1.4; }
.seg { display:flex; gap:8px; position:sticky; top:64px; z-index:40; background:var(--bg); padding:8px 0 10px; }
.seg button { flex:1; min-height:54px; border-radius:10px; border:1.8px solid var(--line); background:#fff; font-size:1.02rem; font-weight:800; color:var(--mut); cursor:pointer; }
.seg button small { display:block; font-weight:400; font-size:.72rem; margin-top:1px; }
.seg button.on-tx { border-color:#2f7d52; background:#2f7d52; color:#fff; }
.seg button.on-rx { border-color:#1f6f9e; background:#1f6f9e; color:#fff; }

/* ---------- verbatim deck content, re-styled ---------- */
.meta { display:flex; flex-wrap:wrap; gap:7px; margin:6px 0 8px; align-items:center; }
.pill { font-size:.86rem; color:#2a2d33; background:#efefe8; border:1px solid var(--line); border-radius:4px; padding:5px 10px; }
.pill b { color:var(--ink); }
.labelrow { font-size:.88rem; margin:2px 0 12px; line-height:1.9; }
.ll { font-weight:700; color:var(--mut); margin-right:6px; }
.chip { display:inline-block; font-size:.8rem; background:var(--ink); color:#fff; border-radius:4px; padding:3px 9px; margin:0 5px 4px 0; font-weight:600; }
.groupbar { display:flex; align-items:stretch; border:1.8px solid var(--amb); border-radius:8px; overflow:hidden; margin:0 0 12px; background:#fdf3e4; }
.gb-tag { flex:none; background:#fdf3e4; padding:10px 11px; display:flex; align-items:center; }
.gb-txt { font-size:.95rem; line-height:1.45; padding:9px 12px 9px 0; color:#5b3d0e; }
.procs { display:flex; flex-direction:column; gap:14px; }
.proc { border:1.5px solid var(--line); border-radius:9px; padding:0 0 8px; overflow:hidden; background:#fff; }
.proc.tx { border-top:5px solid #2f7d52; }
.proc.rx { border-top:5px solid #1f6f9e; }
.proc-h { padding:10px 13px 8px; border-bottom:1px solid #ededdf; background:#fafaf6; }
.proc-k { display:block; font-size:.76rem; font-weight:800; letter-spacing:.08em; }
.proc.tx .proc-k { color:#2f7d52; } .proc.rx .proc-k { color:#1f6f9e; }
.proc-m { display:block; font-size:1.02rem; font-weight:700; margin-top:1px; }
ol.steps { list-style:none; margin:0; padding:13px 13px 0; }
ol.steps li { display:flex; gap:11px; align-items:flex-start; margin-bottom:14px; }
ol.steps .num { flex:none; width:27px; height:27px; border-radius:50%; background:var(--ink); color:#fff; font-weight:800; font-size:.95rem; display:flex; align-items:center; justify-content:center; margin-top:1px; }
ol.steps .txt { font-size:1.04rem; line-height:1.5; }
kbd { font-family:'DejaVu Sans Mono',Menlo,monospace; font-size:.86rem; font-weight:700; background:#fff; border:1.4px solid var(--ink); border-bottom-width:2.6px; border-radius:5px; padding:1px 6px; white-space:nowrap; }
.mode-tx .proc.rx, .mode-rx .proc.tx { display:none; }
@media(min-width:900px){ .procs{flex-direction:row} .procs .proc{flex:1} .mode-tx .proc.rx,.mode-rx .proc.tx{display:block} .seg{display:none} }
.linkbar { display:flex; align-items:stretch; border:1.4px solid #d8d8cf; border-left:5px solid #A6A82B; border-radius:6px; background:#fbfaf3; margin:12px 0; }
.lk-t { flex:none; font-size:.74rem; font-weight:800; letter-spacing:.05em; color:var(--oli); padding:9px 12px; display:flex; align-items:center; }
.linkbar span:last-child { font-size:.94rem; line-height:1.45; padding:9px 12px 9px 0; color:#33373e; }
.rfbar { border:1.4px solid #e3b9a0; border-left:5px solid #c0492b; border-radius:6px; background:#fcefe9; margin:12px 0 0; overflow:hidden; }
.rf-row { display:flex; align-items:stretch; border-top:1px solid #f2dccf; }
.rf-row:first-child { border-top:none; }
.rf-k { flex:none; width:96px; font-size:.72rem; font-weight:800; letter-spacing:.03em; color:#8a3a22; padding:8px 10px; display:flex; align-items:center; }
.rf-k.rf-warn { color:#fff; background:#c0492b; }
.rf-v { font-size:.92rem; line-height:1.42; padding:8px 11px; color:#3a2a22; }
.watch { border:1.4px solid #e6d4bf; background:#fcf4ec; border-radius:8px; padding:10px 14px; margin-top:12px; }
.w-t { font-size:.74rem; font-weight:800; letter-spacing:.08em; color:#9a6516; }
.watch ul { margin:6px 0 0; padding-left:18px; }
.watch li { font-size:.95rem; line-height:1.45; margin-bottom:5px; }
.sources { font-size:.84rem; color:var(--mut); margin-top:14px; line-height:1.6; border-top:1px dashed var(--line); padding-top:9px; }
.sources .s-t { font-weight:800; letter-spacing:.08em; font-size:.68rem; color:var(--oli); margin-right:6px; }
.cardfoot { margin-top:18px; border-top:1px solid var(--line); padding-top:12px; font-size:.9rem; }
.suggest-fab { position:fixed; right:16px; bottom:16px; background:var(--grn); color:#fff; font-weight:700; font-size:.92rem; padding:11px 17px; border-radius:26px; text-decoration:none; box-shadow:0 2px 8px rgba(0,0,0,.25); z-index:60; }
.suggest-fab:hover { background:var(--grn-d); }
body.in-card .suggest-fab { display:none; }
@media print { header,.seg,.cardbar,.suggest-fab,.cardfoot{display:none} }
</style>
</head>
<body>
<header>
<a href="#" aria-label="Home"><img src="assets/gotham-logo.png" alt="Gotham Sound"></a>
<input id="q" type="search" autocomplete="off" placeholder="Search model — ULX-D, 6000, A20…" aria-label="Search systems">
</header>
<main>
<div id="home">
  <div id="lastused"></div>
  <h1 class="bigask">Pick the brand written on your transmitter</h1>
  <p class="reassure">Have your assigned frequency ready (e.g. <b>541.200&nbsp;MHz</b>) — the card walks you through dialing it, step by step.</p>
  <p class="reassure" style="font-size:.88rem">This deck is a <b>community effort</b> — corrections come in from working coordinators and crews and are verified against the manufacturer manuals before publishing.</p>
  <div id="brands"></div>
  <div id="models" hidden></div>
  <div id="results" hidden></div>
  <p class="homefoot">Working from paper? <a href="print.html">Printable deck</a> · <a href="quick-dial-cards.pdf">PDF</a> · <a href="quick-dial-cards-editable.xlsx">Editable XLSX</a><br>
  Maintained by <a href="https://gothamsound.com">Gotham Sound</a>. Spot an error? <a href="https://github.com/gothamsound/quick-dial-cards/issues/new/choose">Suggest a change</a> — or if you don't have a GitHub account (you really should), <a href="mailto:peters@gothamsound.com?subject=quickdialchange">email it here</a>. Contributors are credited in the README — tell us if you&rsquo;d like that (or prefer not).</p>
</div>
<div id="cardwrap" hidden>
  <div class="cardbar">
    <button class="backrow" id="back" type="button">← All systems</button>
    <label class="freqbox"><span>Assigned<br>freq</span><input id="freq" inputmode="decimal" autocomplete="off" placeholder="—"><b>MHz</b></label>
  </div>
  <div class="seg">
    <button id="seg-tx" type="button">TX — Transmitter<small>beltpack / handheld</small></button>
    <button id="seg-rx" type="button">RX — Portable receiver<small>camera hop / bag rig</small></button>
  </div>
@@SECTIONS@@
</div>
</main>
<a class="suggest-fab" href="https://github.com/gothamsound/quick-dial-cards/issues/new/choose" target="_blank" rel="noopener">Suggest a change</a>
<script>
(function(){
var $=function(s){return document.querySelector(s)}, $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))};
var cards=$$('section.card');
var store={get:function(k){try{return localStorage.getItem(k)}catch(e){return null}},set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};

/* home: brand grid */
var brands={};
cards.forEach(function(c){var b=c.dataset.brand;(brands[b]=brands[b]||[]).push(c)});
var bx=$('#brands');
Object.keys(brands).forEach(function(b){
  var n=brands[b].length, btn=document.createElement('button');
  btn.innerHTML='<span>'+b+'</span><span class="n">'+n+' system'+(n>1?'s':'')+'</span>';
  btn.onclick=function(){ n===1 ? go(brands[b][0].id) : showModels(b); };
  bx.appendChild(btn);
});
function modelBtn(c){
  var btn=document.createElement('button'); btn.className='modelbtn';
  btn.innerHTML='<span><span class="mb-b">'+c.dataset.model+'</span><small>'+c.dataset.brand+'</small></span><span class="tag '+c.dataset.badgecls+'">'+c.dataset.badgetxt+'</span>';
  btn.onclick=function(){go(c.id)}; return btn;
}
function showModels(b){
  var m=$('#models'); m.innerHTML=''; 
  var back=document.createElement('button'); back.className='backrow'; back.textContent='← All brands';
  back.onclick=function(){m.hidden=true; bx.hidden=false; $('.bigask').hidden=false; $('.reassure').hidden=false;};
  m.appendChild(back);
  brands[b].forEach(function(c){m.appendChild(modelBtn(c))});
  bx.hidden=true; $('.bigask').hidden=true; $('.reassure').hidden=true; m.hidden=false;
}

/* search */
var idx=cards.map(function(c){return {c:c, t:(c.dataset.title||'').toLowerCase(), all:c.textContent.toLowerCase()}});
$('#q').addEventListener('input',function(){
  var q=this.value.trim().toLowerCase(), r=$('#results');
  if(!q){r.hidden=true; bx.hidden=false; $('.bigask').hidden=false; $('.reassure').hidden=false; $('#models').hidden=true; return;}
  var hits=idx.filter(function(e){return e.t.indexOf(q)>-1});
  if(hits.length<6) idx.forEach(function(e){ if(e.t.indexOf(q)===-1 && e.all.indexOf(q)>-1 && hits.indexOf(e)===-1) hits.push(e); });
  r.innerHTML=''; 
  if(!hits.length){ r.innerHTML='<p class="nores">No match — try part of the model name (e.g. “ULX”, “6000”), or <a href="https://github.com/gothamsound/quick-dial-cards/issues/new?template=new-system.yml" target="_blank" rel="noopener">request this system</a>.</p>'; }
  hits.slice(0,8).forEach(function(e){r.appendChild(modelBtn(e.c))});
  bx.hidden=true; $('.bigask').hidden=true; $('.reassure').hidden=true; $('#models').hidden=true; r.hidden=false;
});

/* routing */
var wrap=$('#cardwrap'), home=$('#home'), current=null;
function go(slug){ location.hash=slug; }
function setMode(m){
  wrap.classList.remove('mode-tx','mode-rx'); wrap.classList.add('mode-'+m);
  $('#seg-tx').className = m==='tx' ? 'on-tx' : ''; $('#seg-rx').className = m==='rx' ? 'on-rx' : '';
  store.set('qdc-mode',m);
}
$('#seg-tx').onclick=function(){setMode('tx')}; $('#seg-rx').onclick=function(){setMode('rx')};
$('#back').onclick=function(){ location.hash=''; };
function route(){
  var slug=location.hash.replace('#',''), c=slug && document.getElementById(slug);
  cards.forEach(function(x){x.hidden=true});
  if(c && c.classList.contains('card')){
    c.hidden=false; current=c; home.hidden=true; wrap.hidden=false; document.body.classList.add('in-card');
    var kt=c.querySelector('.proc.tx .proc-k'), kr=c.querySelector('.proc.rx .proc-k');
    var dt=kt&&kt.textContent!=='TRANSMITTER', dr=kr&&kr.textContent!=='PORTABLE RECEIVER'&&kr.textContent!=='RECEIVER (RACK)';
    document.getElementById('seg-tx').innerHTML = dt ? kt.textContent : 'TX — Transmitter<small>beltpack / handheld</small>';
    document.getElementById('seg-rx').innerHTML = dr ? kr.textContent : (kr&&kr.textContent==='RECEIVER (RACK)' ? 'RX — Rack receiver<small>no portable in-series</small>' : 'RX — Portable receiver<small>camera hop / bag rig</small>');
    setMode(store.get('qdc-mode')||'tx'); store.set('qdc-last',slug);
    window.scrollTo(0,0);
  } else {
    home.hidden=false; wrap.hidden=true; document.body.classList.remove('in-card'); renderLast();
  }
}
window.addEventListener('hashchange',route);

/* last used */
function renderLast(){
  var lu=$('#lastused'), slug=store.get('qdc-last'), c=slug&&document.getElementById(slug);
  lu.innerHTML='';
  if(!c) return;
  var b=document.createElement('button');
  b.innerHTML='<span class="lu-k">Jump back to</span>'+c.dataset.title;
  b.onclick=function(){go(slug)}; lu.appendChild(b);
}

/* assigned frequency (persona 2: keep it huge & visible) */
var f=$('#freq'); f.value=store.get('qdc-freq')||'';
f.addEventListener('input',function(){store.set('qdc-freq',this.value)});

route();
})();
</script>
</body>
</html>'''

out = page.replace("@@SECTIONS@@", "\n".join(sections))
(ROOT / "index.html").write_text(out)
print(f"wrote index.html ({len(out)//1024} KB, {len(cards)} cards)")
