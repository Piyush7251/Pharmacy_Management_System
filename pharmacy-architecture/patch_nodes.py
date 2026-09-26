import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\piyush\.gemini\antigravity-ide\scratch\pharmacy-architecture\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── The replacement nodes.forEach block ──────────────────────────────────────
# Key fix: each node gets a <clipPath> so text is HARD-clipped to the rect.
# Text is also truncated with ellipsis in JS so it never exceeds its maxWidth.

OLD = """nodes.forEach(n=>{const g=el('g',{class:`node ${n.c||''} ${n.role?'user-'+n.role:''} ${n.domain?'domain-'+n.domain:''}`,transform:`translate(${n.x},${n.y})`,'data-id':n.id});if(selected&&n.id!==selected&&!related(selected).includes(n.id))g.classList.add('dim');if(n.id===selected)g.classList.add('selected');const r=el('rect',{width:n.w,height:n.h});const title=el('text',{class:'title',x:13,y:24});title.textContent=n.title;const sub=el('text',{class:'sub',x:13,y:45});sub.textContent=n.sub;g.append(r,title,sub);if(n.c?.includes('role')){const access=el('text',{class:'badge',x:13,y:66});const roleEdges=edges.filter(e=>e.a===n.id&&e.kind==='role').map(e=>byId[e.b]?.title.replace(' DOMAIN API','')).filter(Boolean);access.textContent='→ Allowed: '+(roleEdges.length?roleEdges.join(' • '):'No direct domain API');g.append(access)}g.addEventListener('click',ev=>{ev.stopPropagation();openNode(n.id)});nodesG.appendChild(g)});"""

NEW = """nodes.forEach(n=>{
  const g=el('g',{class:`node ${n.c||''} ${n.role?'user-'+n.role:''} ${n.domain?'domain-'+n.domain:''}`,transform:`translate(${n.x},${n.y})`,'data-id':n.id});
  if(selected&&n.id!==selected&&!related(selected).includes(n.id))g.classList.add('dim');
  if(n.id===selected)g.classList.add('selected');
  const r=el('rect',{width:n.w,height:n.h});

  // ClipPath to hard-clip ALL text inside the rect
  const clipId='cp-'+n.id;
  const cp=document.createElementNS(NS,'clipPath');
  cp.setAttribute('id',clipId);
  const cr=el('rect',{x:4,y:2,width:Math.max(0,n.w-8),height:Math.max(0,n.h-4)});
  cp.appendChild(cr);
  g.appendChild(cp);

  // Helper: truncate text to fit maxWidth pixels (approx 6.5px/char for 13px font)
  function trunc(str,maxPx,pxPerChar){const max=Math.floor(maxPx/pxPerChar);return str.length<=max?str:str.slice(0,max-1)+'…';}

  const maxW=n.w-26;
  const title=el('text',{class:'title',x:13,y:23,'clip-path':`url(#${clipId})`});
  title.textContent=trunc(n.title||'',maxW,6.2);

  const sub=el('text',{class:'sub',x:13,y:40,'clip-path':`url(#${clipId})`});
  sub.textContent=trunc(n.sub||'',maxW,5.4);

  g.append(r,title,sub);

  if(n.c?.includes('role')){
    const roleEdges=edges.filter(e=>e.a===n.id&&e.kind==='role').map(e=>byId[e.b]?.title.replace(' DOMAIN API','').replace(' Domain API','')).filter(Boolean);
    const allowedStr='→ '+(roleEdges.length?roleEdges.join(' • '):'No domains');
    const access=el('text',{class:'badge',x:13,y:58,'clip-path':`url(#${clipId})`});
    access.textContent=trunc(allowedStr,maxW,5.4);
    g.appendChild(access);
  }

  g.addEventListener('click',ev=>{ev.stopPropagation();openNode(n.id)});
  nodesG.appendChild(g);
});"""

if OLD in html:
    html = html.replace(OLD, NEW)
    print("Replacement succeeded!")
else:
    print("ERROR: OLD block not found! Trying unicode escape version...")
    OLD2 = OLD.replace('&&', '\\u0026\\u0026')
    if OLD2 in html:
        html = html.replace(OLD2, NEW)
        print("Replacement with unicode escape succeeded!")
    else:
        print("Both replacements failed. Need manual check.")

with open(r'C:\Users\piyush\.gemini\antigravity-ide\scratch\pharmacy-architecture\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
print("File size:", os.path.getsize(r'C:\Users\piyush\.gemini\antigravity-ide\scratch\pharmacy-architecture\index.html'))

import shutil
shutil.copy(
    r'C:\Users\piyush\.gemini\antigravity-ide\scratch\pharmacy-architecture\index.html',
    r'C:\Users\piyush\Downloads\pharmacy_management_architecture2.html'
)
print("Copied to Downloads.")
