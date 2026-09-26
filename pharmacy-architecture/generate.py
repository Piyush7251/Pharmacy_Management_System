import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Read original_script.js
script_path = r'C:\Users\piyush\.gemini\antigravity-ide\scratch\pharmacy-architecture\original_script.js'
with open(script_path, 'r', encoding='utf-8') as f:
    js_raw = f.read()

# Update Group Coordinates
js_raw = re.sub(
    r"\{id:'g-clinical'[^\}]+\}",
    "{id:'g-clinical',title:'CLINICAL SERVICES',note:'Prescription • safety • patient medication • refills • controlled drugs',x:55,y:765,w:575,h:285,color:'--clinical'}",
    js_raw
)
js_raw = re.sub(
    r"\{id:'g-inventory'[^\}]+\}",
    "{id:'g-inventory',title:'INVENTORY & PROCUREMENT',note:'Catalog • stock • FEFO • procurement • quality • branches',x:640,y:765,w:575,h:285,color:'--inventory'}",
    js_raw
)
js_raw = re.sub(
    r"\{id:'g-commerce'[^\}]+\}",
    "{id:'g-commerce',title:'COMMERCE & CUSTOMER TRANSACTIONS',note:'POS • billing • payments • orders • loyalty',x:1225,y:765,w:575,h:285,color:'--commerce'}",
    js_raw
)
js_raw = re.sub(
    r"\{id:'g-operations'[^\}]+\}",
    "{id:'g-operations',title:'FULFILMENT & OPERATIONS',note:'Delivery • notifications • finance • analytics • compliance • workforce',x:1810,y:765,w:575,h:285,color:'--operations'}",
    js_raw
)

# Update Domain API entry nodes coordinates
js_raw = re.sub(r"\{id:'clinical-api',([^\}]+)y:668,w:500,h:70", r"{id:'clinical-api',\1y:690,w:575,h:60", js_raw)
js_raw = re.sub(r"\{id:'inventory-api',([^\}]+)y:668,w:500,h:70", r"{id:'inventory-api',\1y:690,w:575,h:60", js_raw)
js_raw = re.sub(r"\{id:'commerce-api',([^\}]+)y:668,w:500,h:70", r"{id:'commerce-api',\1y:690,w:575,h:60", js_raw)
js_raw = re.sub(r"\{id:'ops-api',([^\}]+)y:668,w:500,h:70", r"{id:'ops-api',\1y:690,w:575,h:60", js_raw)

# Update Service Nodes coordinates in Layer 4
updates_nodes = {
    # Clinical Group (x: 55, w: 575)
    'rx': ("x:70,y:825,w:175,h:80", "x:80,y:760,w:160,h:78"),
    'safety': ("x:255,y:825,w:175,h:80", "x:255,y:760,w:160,h:78"),
    'patientSvc': ("x:440,y:825,w:175,h:80", "x:430,y:760,w:160,h:78"),
    'refill': ("x:70,y:940,w:260,h:80", "x:80,y:855,w:160,h:78"),
    'controlled': ("x:340,y:940,w:275,h:80", "x:255,y:855,w:160,h:78"),

    # Inventory Group (x: 640, w: 575)
    'catalog': ("x:655,y:825,w:175,h:80", "x:660,y:760,w:160,h:78"),
    'inventory': ("x:840,y:825,w:175,h:80", "x:835,y:760,w:160,h:78"),
    'procure': ("x:1025,y:825,w:175,h:80", "x:1010,y:760,w:160,h:78"),
    'quality': ("x:655,y:940,w:260,h:80", "x:660,y:855,w:160,h:78"),
    'branch': ("x:925,y:940,w:275,h:80", "x:835,y:855,w:160,h:78"),

    # Commerce Group (x: 1225, w: 575)
    'pos': ("x:1240,y:825,w:175,h:80", "x:1240,y:760,w:160,h:78"),
    'billing': ("x:1425,y:825,w:175,h:80", "x:1415,y:760,w:160,h:78"),
    'payments': ("x:1610,y:825,w:175,h:80", "x:1590,y:760,w:160,h:78"),
    'orders': ("x:1240,y:940,w:260,h:80", "x:1240,y:855,w:160,h:78"),
    'loyalty': ("x:1510,y:940,w:275,h:80", "x:1415,y:855,w:160,h:78"),

    # Operations Group (x: 1810, w: 575)
    'deliverySvc': ("x:1825,y:825,w:175,h:80", "x:1820,y:760,w:160,h:78"),
    'notifications': ("x:2010,y:825,w:175,h:80", "x:1995,y:760,w:160,h:78"),
    'finance': ("x:2195,y:825,w:175,h:80", "x:2170,y:760,w:160,h:78"),
    'analytics': ("x:1825,y:940,w:175,h:80", "x:1820,y:855,w:160,h:78"),
    'compliance': ("x:2010,y:940,w:175,h:80", "x:1995,y:855,w:160,h:78"),
    'workforce': ("x:2195,y:940,w:175,h:80", "x:2170,y:855,w:160,h:78"),
}

for nid, (new_pos, old_pos) in updates_nodes.items():
    js_raw = re.sub(
        r"(\{id:'" + re.escape(nid) + r"',[^\}]+)" + re.escape(old_pos),
        r"\1" + new_pos,
        js_raw
    )

# Update Layer 5 Data Nodes Y position (y: 1150)
js_raw = re.sub(r"(\{id:'(coredb|cache|searchidx|queue|storage|auditlog|reportdb)',[^\}]+)y:1120,", r"\1y:1150,", js_raw)

# Update Layer 6 External Nodes Y position
js_raw = re.sub(r"(\{id:'(payment|gst|erx|drugdb)',[^\}]+)y:1295,", r"\1y:1330,", js_raw)
js_raw = re.sub(r"(\{id:'(messaging|accounting|deliveryext|infra)',[^\}]+)y:1385,", r"\1y:1445,", js_raw)

# Prepend icons to node titles
icon_map = {
    'admin': '👑 ', 'pharmacist': '🩺 ', 'cashier': '💳 ', 'patient': '📱 ', 'supplier': '🚛 ', 'delivery': '🛵 ',
    'gateway': '🛡️ ',
    'role-admin': '🔑 ', 'role-pharmacist': '💊 ', 'role-cashier': '🏷️ ', 'role-patient': '📲 ', 'role-supplier': '📦 ', 'role-delivery': '🗺️ ',
    'clinical-api': '🩺 ', 'inventory-api': '📦 ', 'commerce-api': '🛍️ ', 'ops-api': '⚡ ',
    'rx': '📄 ', 'safety': '🧠 ', 'patientSvc': '📋 ', 'refill': '🔄 ', 'controlled': '🚨 ',
    'catalog': '🏷️ ', 'inventory': '📊 ', 'procure': '📦 ', 'quality': '❄️ ', 'branch': '🏬 ',
    'pos': '💻 ', 'billing': '🧾 ', 'payments': '💳 ', 'orders': '🚚 ', 'loyalty': '🎁 ',
    'deliverySvc': '🛵 ', 'notifications': '🔔 ', 'finance': '📈 ', 'analytics': '📊 ', 'compliance': '⚖️ ', 'workforce': '👥 ',
    'coredb': '🗄️ ', 'cache': '⚡ ', 'searchidx': '🔍 ', 'queue': '📨 ', 'storage': '📁 ', 'auditlog': '🔒 ', 'reportdb': '📈 ',
    'payment': '💳 ', 'gst': '🏛️ ', 'erx': '🏥 ', 'drugdb': '🌐 ', 'messaging': '💬 ', 'accounting': '📑 ', 'deliveryext': '🗺️ ', 'infra': '☁️ '
}

for node_id, icon in icon_map.items():
    js_raw = re.sub(
        r"(\{id:'" + re.escape(node_id) + r"',title:')([^']+)(')",
        lambda m: m.group(1) + (icon if not m.group(2).startswith(icon.strip()) else '') + m.group(2) + m.group(3),
        js_raw
    )

# Dynamic text scaling in draw() function to prevent ANY title or sub text overflow outside the node card box
js_node_drawing_fix = """
 nodes.forEach(n=>{const g=el('g',{class:`node ${n.c||''} ${n.role?'user-'+n.role:''} ${n.domain?'domain-'+n.domain:''}`,transform:`translate(${n.x},${n.y})`,'data-id':n.id});if(selected&&n.id!==selected&&!related(selected).includes(n.id))g.classList.add('dim');if(n.id===selected)g.classList.add('selected');
 const r=el('rect',{width:n.w,height:n.h});
 
 const maxW = n.w - 24;
 const title=el('text',{class:'title',x:12,y:22});
 const tLen = n.title.length;
 let tFont = 13.5;
 if (tLen * 7.5 > maxW) {
   tFont = Math.max(9.5, Math.min(12.5, (maxW / tLen) * 1.55));
 }
 title.setAttribute('font-size', tFont.toFixed(1) + 'px');
 title.textContent=n.title;
 
 const sub=el('text',{class:'sub',x:12,y:42});
 const sLen = (n.sub||'').length;
 let sFont = 10.8;
 if (sLen * 6.2 > maxW) {
   sFont = Math.max(8.5, Math.min(10.5, (maxW / sLen) * 1.45));
 }
 sub.setAttribute('font-size', sFont.toFixed(1) + 'px');
 sub.textContent=n.sub||'';
 
 g.append(r,title,sub);
 if(n.c?.includes('role')){
   const access=el('text',{class:'badge',x:12,y:65});
   const roleEdges=edges.filter(e=>e.a===n.id&&e.kind==='role').map(e=>byId[e.b]?.title.replace(' DOMAIN API','')).filter(Boolean);
   access.textContent='→ Allowed: '+(roleEdges.length?roleEdges.join(' • '):'No direct domain APIs mapped.');
   const aLen = access.textContent.length;
   let aFont = 10;
   if (aLen * 5.8 > maxW) {
     aFont = Math.max(8.5, Math.min(10, (maxW / aLen) * 1.4));
   }
   access.setAttribute('font-size', aFont.toFixed(1) + 'px');
   g.appendChild(access);
 }
 nodesG.appendChild(g);
 });
"""

# Replace original nodes.forEach in js_raw
js_raw = re.sub(
    r"nodes\.forEach\(n=>\{const g=el\('g',\{class:`node \$\{n\.c\|\|''\}.*?nodesG\.appendChild\(g\);\s*\}\);",
    js_node_drawing_fix.strip(),
    js_raw,
    flags=re.DOTALL
)

# Inject particle animation code into draw()
draw_particle_code = """
  // Animated data flow particles for active edges
  const particlesG = document.getElementById('particles');
  if (particlesG) {
    particlesG.innerHTML = '';
    if (selected) {
      edges.forEach(e => {
        if (e.a === selected || e.b === selected) {
          const na = byId[e.a], nb = byId[e.b];
          if (!na || !nb) return;
          const pa = anchor(na, nb), pb = anchor(nb, na);
          const pathD = bendPath(pa, pb);
          const p = document.createElementNS(NS, 'circle');
          p.setAttribute('r', '4');
          p.setAttribute('fill', '#38bdf8');
          p.setAttribute('filter', 'url(#glow)');
          const anim = document.createElementNS(NS, 'animateMotion');
          anim.setAttribute('path', pathD);
          anim.setAttribute('dur', '1.8s');
          anim.setAttribute('repeatCount', 'indefinite');
          p.appendChild(anim);
          particlesG.appendChild(p);
        }
      });
    }
  }
"""

if 'connectBtn.textContent=' in js_raw:
    js_raw = js_raw.replace("connectBtn.textContent='Show connections';", "connectBtn.textContent='Show connections';\n" + draw_particle_code)

# High-contrast CSS styling for all dark theme text
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pharmacy Management System — Detailed Interactive Architecture</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg-base: #06090e;
  --bg-surface: #0b111a;
  --bg-card: #101924;
  --bg-card-hover: #162232;
  --glass-bg: rgba(13, 20, 31, 0.88);
  --glass-border: rgba(255, 255, 255, 0.12);
  --glass-border-hover: rgba(56, 189, 248, 0.45);
  
  --text-main: #ffffff;
  --text-muted: #cbd5e1;
  --text-dim: #94a3b8;
  
  --accent-cyan: #38bdf8;
  --accent-emerald: #34d399;
  --accent-amber: #fbbf24;
  --accent-purple: #c084fc;
  --accent-rose: #f472b6;
  --accent-indigo: #818cf8;
  
  --admin: #fbbf24;
  --pharmacist: #34d399;
  --cashier: #38bdf8;
  --patient: #c084fc;
  --supplier: #f472b6;
  --delivery: #818cf8;
  
  --clinical: #10b981;
  --inventory: #f59e0b;
  --commerce: #06b6d4;
  --operations: #8b5cf6;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  height: 100%;
  background: var(--bg-base);
  color: var(--text-main);
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}

button, input { font: inherit; }

.app {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* Glass Header */
.topbar {
  height: 72px;
  background: var(--glass-bg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 24px;
  flex: 0 0 auto;
  z-index: 20;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 18px;
  letter-spacing: -0.3px;
  white-space: nowrap;
}

.brand-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(52, 211, 153, 0.2));
  border: 1px solid rgba(56, 189, 248, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
}

.brand-title span {
  background: linear-gradient(135deg, #38bdf8, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.version-badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 99px;
  background: rgba(56, 189, 248, 0.15);
  border: 1px solid rgba(56, 189, 248, 0.4);
  color: var(--accent-cyan);
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  align-self: flex-start;
  margin-top: 2px;
}

/* Filter Pills */
.filter-pills {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(15, 23, 42, 0.8);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  margin-left: 12px;
}

.filter-btn {
  border: 0;
  background: transparent;
  color: var(--text-muted);
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.08);
}

.filter-btn.active {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.3), rgba(52, 211, 153, 0.3));
  border: 1px solid rgba(56, 189, 248, 0.5);
  color: #ffffff;
  box-shadow: 0 2px 12px rgba(56, 189, 248, 0.3);
}

.filter-btn .dot-count {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 99px;
  background: rgba(255, 255, 255, 0.15);
  font-family: 'JetBrains Mono', monospace;
}

/* Toolbar Controls */
.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-left: auto;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box input {
  height: 38px;
  width: 230px;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid var(--glass-border);
  color: var(--text-main);
  border-radius: 10px;
  padding: 0 36px 0 36px;
  font-size: 13px;
  outline: none;
  transition: all 0.2s ease;
}

.search-box input:focus {
  border-color: var(--accent-cyan);
  box-shadow: 0 0 16px rgba(56, 189, 248, 0.3);
  background: rgba(15, 23, 42, 0.95);
  width: 270px;
}

.search-icon {
  position: absolute;
  left: 12px;
  font-size: 14px;
  color: var(--text-muted);
  pointer-events: none;
}

.search-shortcut {
  position: absolute;
  right: 10px;
  font-size: 10px;
  padding: 2px 5px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
  pointer-events: none;
}

.btn-action {
  height: 38px;
  padding: 0 14px;
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid var(--glass-border);
  color: var(--text-main);
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.btn-action:hover {
  border-color: var(--accent-cyan);
  background: rgba(30, 41, 59, 0.95);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}

.btn-primary {
  background: linear-gradient(135deg, #0284c7, #0d9488);
  border: 1px solid rgba(56, 189, 248, 0.6);
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0369a1, #0f766e);
  box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6);
}

/* Viewport Canvas */
.main {
  position: relative;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.viewport {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background-color: var(--bg-base);
  background-image: 
    radial-gradient(circle at 50% 10%, rgba(56, 189, 248, 0.1) 0%, transparent 65%),
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 100% 100%, 48px 48px, 48px 48px;
}

#svgWrap {
  position: absolute;
  left: 0;
  top: 0;
  transform-origin: 0 0;
  cursor: grab;
  user-select: none;
}

#svgWrap.dragging { cursor: grabbing; }
svg { display: block; }

/* HIGH CONTRAST SVG Visual Styles */
.layer rect {
  fill: rgba(11, 17, 26, 0.88);
  stroke: rgba(255, 255, 255, 0.12);
  stroke-width: 1.5;
  rx: 16;
}

.layer-title {
  fill: #ffffff;
  font-family: 'Outfit', sans-serif;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0.8px;
}

.layer-badge-bg {
  fill: rgba(56, 189, 248, 0.2);
  stroke: rgba(56, 189, 248, 0.5);
  stroke-width: 1;
  rx: 6;
}

.layer-badge-text {
  fill: #38bdf8;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 800;
}

.layer-note {
  fill: #cbd5e1;
  font-size: 12.5px;
  font-weight: 500;
}

.group rect {
  fill: rgba(15, 23, 42, 0.55);
  stroke: rgba(255, 255, 255, 0.18);
  stroke-width: 1.5;
  stroke-dasharray: 6 5;
  rx: 14;
}

.group-title {
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.group-note {
  font-size: 11.5px;
  fill: #cbd5e1;
  font-weight: 500;
}

/* Node Card Styling */
.node {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
}

.node rect {
  fill: #0f172a;
  stroke: #475569;
  stroke-width: 1.5;
  rx: 10;
  transition: all 0.2s ease;
  filter: drop-shadow(0 4px 14px rgba(0, 0, 0, 0.4));
}

.node .title {
  fill: #ffffff;
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
}

.node .sub {
  fill: #cbd5e1;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 500;
}

.badge {
  fill: #38bdf8;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
}

.node:hover rect {
  stroke: var(--accent-cyan);
  fill: #1e293b;
  filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.5));
  cursor: pointer;
}

.node.selected rect {
  stroke: var(--accent-cyan);
  stroke-width: 2.5;
  fill: #1e293b;
  filter: drop-shadow(0 0 24px rgba(56, 189, 248, 0.7));
}

.node.dim { opacity: 0.15; }

/* Custom Node Themes */
.node.user rect { stroke-width: 2; }
.node.role-admin rect { stroke: var(--admin); }
.node.role-pharmacist rect { stroke: var(--pharmacist); }
.node.role-cashier rect { stroke: var(--cashier); }
.node.role-patient rect { stroke: var(--patient); }
.node.role-supplier rect { stroke: var(--supplier); }
.node.role-delivery rect { stroke: var(--delivery); }

.node.domain-clinical rect { stroke: var(--clinical); }
.node.domain-inventory rect { stroke: var(--inventory); }
.node.domain-commerce rect { stroke: var(--commerce); }
.node.domain-operations rect { stroke: var(--operations); }

.node.data rect { fill: #0d1520; stroke: #64748b; }
.node.ext rect { fill: #0b111a; stroke: #475569; }

/* Edge Connections */
.edge {
  fill: none;
  stroke: #64748b;
  stroke-width: 1.8;
  marker-end: url(#arrow);
  opacity: 0.65;
  transition: all 0.3s ease;
  pointer-events: stroke;
}

.edge:hover {
  stroke: var(--accent-cyan);
  stroke-width: 2.8;
  opacity: 0.95;
  cursor: pointer;
}

.edge.user { stroke-width: 2.5; opacity: 0.8; }
.edge.role { stroke-width: 2.5; stroke-dasharray: 8 5; opacity: 0.9; }
.edge.domain { stroke-width: 2.2; opacity: 0.8; }

.edge.active {
  stroke: var(--accent-cyan);
  stroke-width: 3.2;
  opacity: 1;
  filter: url(#glow);
}

.edge.dim { opacity: 0.05; }

.edge-label {
  fill: #e2e8f0;
  font-size: 10.5px;
  font-weight: 700;
  pointer-events: none;
  font-family: 'JetBrains Mono', monospace;
}

.edge-label.active {
  fill: #ffffff;
  font-weight: 800;
}

/* Floating Diagram Help Banner */
.diagram-help {
  position: absolute;
  left: 24px;
  top: 24px;
  z-index: 10;
  background: var(--glass-bg);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 10px 16px;
  font-size: 11.5px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.diagram-help .pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-cyan);
  box-shadow: 0 0 10px var(--accent-cyan);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.8; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.8; }
}

/* Floating Legend Panel */
.legend {
  position: absolute;
  left: 24px;
  bottom: 24px;
  z-index: 10;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: 14px;
  padding: 12px 18px;
  font-size: 11.5px;
  color: var(--text-muted);
  display: flex;
  gap: 16px;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  flex-wrap: wrap;
  max-width: calc(100% - 240px);
}

.legend span {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: color 0.2s ease;
}

.legend span:hover { color: #ffffff; }

.legend i {
  display: inline-block;
  width: 22px;
  height: 3px;
  border-radius: 2px;
  background: #64748b;
}

.legend i.role {
  border-top: 2px dashed #94a3b8;
  height: 0;
  background: none;
}

.legend i.active { background: var(--accent-cyan); box-shadow: 0 0 8px var(--accent-cyan); }

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.admin { background: var(--admin); box-shadow: 0 0 8px var(--admin); }
.pharmacist { background: var(--pharmacist); box-shadow: 0 0 8px var(--pharmacist); }
.cashier { background: var(--cashier); box-shadow: 0 0 8px var(--cashier); }
.patient { background: var(--patient); box-shadow: 0 0 8px var(--patient); }
.supplier { background: var(--supplier); box-shadow: 0 0 8px var(--supplier); }
.delivery { background: var(--delivery); box-shadow: 0 0 8px var(--delivery); }

.domain-key {
  padding-left: 12px;
  margin-left: 4px;
  border-left: 1px solid var(--glass-border);
  display: flex;
  gap: 12px;
}

.domain-key b { font-size: 11px; font-weight: 700; }

/* Floating Zoom Controls */
.zoom {
  position: absolute;
  right: 24px;
  bottom: 24px;
  z-index: 10;
  display: flex;
  gap: 6px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 6px;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.zoom button {
  min-width: 38px;
  height: 38px;
  padding: 0 10px;
  border-radius: 8px;
  border: 1px solid transparent;
  background: rgba(15, 23, 42, 0.8);
  color: var(--text-main);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.zoom button:hover {
  border-color: var(--glass-border-hover);
  background: rgba(30, 41, 59, 0.9);
  color: var(--accent-cyan);
}

/* Sliding Drawer Details Panel */
.drawer {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: min(720px, 95vw);
  background: rgba(11, 17, 26, 0.96);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-left: 1px solid var(--glass-border);
  box-shadow: -24px 0 60px rgba(0, 0, 0, 0.7);
  transform: translateX(102%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 30;
  display: flex;
  flex-direction: column;
}

.drawer.open { transform: translateX(0); }

.drawer-head {
  padding: 22px 24px;
  border-bottom: 1px solid var(--glass-border);
  display: flex;
  gap: 16px;
  align-items: flex-start;
  background: rgba(15, 23, 42, 0.4);
}

.drawer-icon-box {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(52, 211, 153, 0.2));
  border: 1px solid rgba(56, 189, 248, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.drawer-head .grow { flex: 1; }

.drawer-title {
  font-family: 'Outfit', sans-serif;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.3px;
  color: #ffffff;
}

.drawer-desc {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 13px;
  line-height: 1.55;
}

.close {
  border: 1px solid var(--glass-border);
  background: rgba(15, 23, 42, 0.8);
  color: var(--text-main);
  width: 38px;
  height: 38px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.2s ease;
}

.close:hover {
  border-color: #f43f5e;
  background: rgba(244, 63, 94, 0.2);
  color: #f43f5e;
}

.tabs {
  display: flex;
  gap: 6px;
  padding: 12px 24px;
  border-bottom: 1px solid var(--glass-border);
  background: rgba(11, 17, 26, 0.6);
}

.tab {
  border: 0;
  background: transparent;
  color: var(--text-muted);
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab:hover { color: #ffffff; background: rgba(255, 255, 255, 0.08); }

.tab.active {
  background: rgba(56, 189, 248, 0.2);
  border: 1px solid rgba(56, 189, 248, 0.4);
  color: #ffffff;
}

.drawer-body {
  overflow-y: auto;
  padding: 20px 24px 32px;
  flex: 1;
}

.tabpane { display: none; }
.tabpane.active { display: block; }

/* Stat Cards in Drawer */
.statgrid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

.stat {
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.7);
  padding: 12px 14px;
}

.stat b {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-dim);
  margin-bottom: 6px;
}

.stat span {
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-main);
}

.section-title {
  font-family: 'Outfit', sans-serif;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1px;
  color: var(--accent-cyan);
  text-transform: uppercase;
  margin: 22px 0 12px;
}

.feature-list, .parts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.feature, .part {
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.6);
  font-size: 12px;
  line-height: 1.5;
  color: #cbd5e1;
}

.part strong {
  display: block;
  color: #ffffff;
  font-size: 13px;
  margin-bottom: 4px;
  font-weight: 700;
}

.part span {
  font-size: 11.5px;
  color: var(--text-muted);
}

/* Flow Step Boxes inside Drawer */
.flow {
  border: 1px solid var(--glass-border);
  border-radius: 14px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
}

.flowrow {
  display: grid;
  grid-template-columns: 1fr 32px 1fr;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.flowbox {
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  padding: 10px 12px;
  background: rgba(15, 23, 42, 0.85);
  font-size: 11.5px;
  line-height: 1.5;
  color: #cbd5e1;
}

.flowarrow {
  text-align: center;
  color: var(--accent-cyan);
  font-weight: 800;
  font-size: 16px;
}

.tech {
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 14px;
  background: rgba(15, 23, 42, 0.75);
  font-size: 12.5px;
  line-height: 1.6;
  color: #e2e8f0;
  font-family: 'JetBrains Mono', monospace;
}

.conn {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.chip {
  border: 1px solid var(--glass-border);
  background: rgba(15, 23, 42, 0.85);
  border-radius: 99px;
  padding: 6px 12px;
  font-size: 11.5px;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.chip:hover {
  border-color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.2);
  transform: translateY(-1px);
}

.access-map { display: grid; gap: 10px; }

.access-row {
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.6);
  color: #cbd5e1;
}

.access-row strong {
  display: block;
  font-size: 13px;
  margin-bottom: 6px;
  color: #ffffff;
}

.access-row .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 10.5px;
  border: 1px solid var(--glass-border);
  border-radius: 99px;
  padding: 3px 9px;
  color: var(--text-muted);
  background: rgba(15, 23, 42, 0.85);
}

.flow-badge {
  display: inline-block;
  border: 1px solid var(--glass-border);
  border-radius: 99px;
  padding: 4px 9px;
  font-size: 10.5px;
  color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.15);
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
}

/* Access Matrix Overlay */
.matrix-overlay {
  position: fixed;
  inset: 0;
  background: rgba(3, 7, 12, 0.88);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 100;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.matrix-overlay.open { display: flex; }

.matrix {
  width: min(1180px, 96vw);
  max-height: 88vh;
  overflow: auto;
  background: rgba(11, 17, 26, 0.96);
  border: 1px solid var(--glass-border);
  border-radius: 18px;
  box-shadow: 0 30px 100px rgba(0, 0, 0, 0.7);
  padding: 28px;
}

.matrix-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.matrix h2 {
  font-family: 'Outfit', sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: #ffffff;
}

.matrix p {
  color: var(--text-muted);
  font-size: 12px;
  margin-top: 4px;
}

.matrix table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11.5px;
  margin-top: 16px;
}

.matrix th, .matrix td {
  border: 1px solid var(--glass-border);
  padding: 12px;
  text-align: center;
}

.matrix th {
  background: rgba(15, 23, 42, 0.95);
  color: #ffffff;
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
}

.matrix td:first-child, .matrix th:first-child {
  text-align: left;
  position: sticky;
  left: 0;
  background: rgba(15, 23, 42, 0.98);
  font-weight: 700;
  color: #ffffff;
}

.yes { font-weight: 800; color: #34d399; }
.partial { font-weight: 800; color: #fbbf24; }
.no { color: #94a3b8; }

.matrix-close {
  border: 1px solid var(--glass-border);
  background: rgba(15, 23, 42, 0.85);
  color: var(--text-main);
  border-radius: 10px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.matrix-close:hover {
  border-color: #f43f5e;
  color: #f43f5e;
}

/* Toast Notifications */
.toast {
  position: fixed;
  left: 50%;
  bottom: 30px;
  transform: translateX(-50%) translateY(80px);
  padding: 12px 20px;
  border: 1px solid rgba(56, 189, 248, 0.5);
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(16px);
  color: #ffffff;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 120;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  gap: 10px;
}

.toast.show {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

@media (max-width: 1200px) {
  .filter-pills { display: none; }
  .search-box input { width: 180px; }
  .legend { max-width: 60%; }
}
</style>
</head>
<body>
<div class="app">
<header class="topbar">
  <div class="brand">
    <div class="brand-icon">💊</div>
    <div class="brand-text">
      <div class="brand-title">PHARMACY <span style="color: var(--accent-cyan)">ARCHITECTURE</span></div>
    </div>
    <span class="version-badge">v2.0 LIVE</span>
  </div>
  
  <div class="filter-pills">
    <button class="filter-btn active" data-filter="all">All <span class="dot-count">53</span></button>
    <button class="filter-btn" data-filter="role">👥 Roles</button>
    <button class="filter-btn" data-filter="clinical">🩺 Clinical</button>
    <button class="filter-btn" data-filter="inventory">📦 Inventory</button>
    <button class="filter-btn" data-filter="commerce">🛍️ Commerce</button>
    <button class="filter-btn" data-filter="operations">⚡ Operations</button>
    <button class="filter-btn" data-filter="infra">💾 Data &amp; Infra</button>
  </div>

  <div class="toolbar">
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input id="search" placeholder="Search module, role, feature…" aria-label="Search architecture">
      <span class="search-shortcut">/</span>
    </div>
    <button id="matrixBtn" class="btn-action btn-primary"><span>⚡</span> Access Matrix</button>
    <button id="connectBtn" class="btn-action"><span>🔗</span> Connections</button>
    <button id="fitBtn" class="btn-action"><span>🎯</span> Fit</button>
    <button id="resetBtn" class="btn-action"><span>🔄</span> Reset</button>
  </div>
</header>

<main class="main">
<div id="viewport" class="viewport">
<div id="svgWrap">
<svg id="arch" width="2400" height="1750" viewBox="0 0 2400 1750" role="img" aria-label="Pharmacy Architecture Diagram">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L0,6 L9,3 z" fill="#94a3b8"></path>
  </marker>
  <marker id="arrowActive" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L0,6 L9,3 z" fill="#38bdf8"></path>
  </marker>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>

<!-- Layer frames with high contrast text -->
<g class="layer"><rect x="20" y="18" width="2360" height="150"></rect>
  <rect x="38" y="32" width="75" height="22" class="layer-badge-bg"></rect>
  <text class="layer-badge-text" x="48" y="47">LAYER 1</text>
  <text class="layer-title" x="125" y="49">USERS &amp; CLIENT CHANNELS</text>
  <text class="layer-note" x="38" y="72">People and store devices enter through web dashboards, mobile apps, POS terminals, and partner API channels.</text>
</g>

<g class="layer"><rect x="20" y="186" width="2360" height="122"></rect>
  <rect x="38" y="200" width="75" height="22" class="layer-badge-bg"></rect>
  <text class="layer-badge-text" x="48" y="215">LAYER 2</text>
  <text class="layer-title" x="125" y="217">API GATEWAY + IDENTITY CONTROL</text>
  <text class="layer-note" x="38" y="240">One secure front door: authentication, MFA verification, RBAC policy checks, token validation, rate limiting, and correlation tracking.</text>
</g>

<g class="layer"><rect x="20" y="326" width="2360" height="284"></rect>
  <rect x="38" y="340" width="75" height="22" class="layer-badge-bg"></rect>
  <text class="layer-badge-text" x="48" y="355">LAYER 3</text>
  <text class="layer-title" x="125" y="357">ROLE WORKSPACES — CLEAR USER-TO-SYSTEM ISOLATION</text>
  <text class="layer-note" x="38" y="380">Each role workspace isolates features and maps exclusively to allowed domain APIs. Click any role to trace its authorization tree.</text>
</g>

<g class="layer"><rect x="20" y="628" width="2360" height="440"></rect>
  <rect x="38" y="642" width="75" height="22" class="layer-badge-bg"></rect>
  <text class="layer-badge-text" x="48" y="657">LAYER 4</text>
  <text class="layer-title" x="125" y="659">DOMAIN APIs &amp; PHARMACY BUSINESS SERVICES</text>
  <text class="layer-note" x="38" y="677">Four encapsulated business domains: Clinical, Inventory, Commerce, and Operations. Follow columns vertically to trace domain flows.</text>
</g>

<g class="layer"><rect x="20" y="1080" width="2360" height="150"></rect>
  <rect x="38" y="1094" width="75" height="22" class="layer-badge-bg"></rect>
  <text class="layer-badge-text" x="48" y="1109">LAYER 5</text>
  <text class="layer-title" x="125" y="1111">DATA, CACHE, SEARCH &amp; ASYNC INFRASTRUCTURE</text>
  <text class="layer-note" x="38" y="1131">Shared persistence, distributed caching, full-text search, event streaming, private object storage, and immutable audit logs.</text>
</g>

<g class="layer"><rect x="20" y="1250" width="2360" height="440"></rect>
  <rect x="38" y="1264" width="75" height="22" class="layer-badge-bg"></rect>
  <text class="layer-badge-text" x="48" y="1279">LAYER 6</text>
  <text class="layer-title" x="125" y="1281">EXTERNAL INTEGRATIONS &amp; CLOUD PLATFORM</text>
  <text class="layer-note" x="38" y="1301">Third-party PSPs, GST tax portals, national eRx networks, messaging providers, logistics partners, and cloud infrastructure.</text>
</g>

<g id="groups"></g>
<g id="edges"></g>
<g id="particles"></g>
<g id="nodes"></g>
</svg>
</div>

<div class="diagram-help">
  <span class="pulse-dot"></span>
  <b>INTERACTIVE SYSTEM TRACER</b> • Click any node to trace connection pathways &amp; view detailed component specs
</div>

<div class="legend">
  <span><i></i> Service Flow</span>
  <span><i class="role"></i> Role Scope</span>
  <span><i class="active"></i> Active Path</span>
  <span><b class="dot admin"></b> Admin</span>
  <span><b class="dot pharmacist"></b> Pharmacist</span>
  <span><b class="dot cashier"></b> Cashier</span>
  <span><b class="dot patient"></b> Patient</span>
  <span><b class="dot supplier"></b> Supplier</span>
  <span><b class="dot delivery"></b> Delivery</span>
  <span class="domain-key">
    <b style="color:var(--clinical)">Clinical</b>
    <b style="color:var(--inventory)">Inventory</b>
    <b style="color:var(--commerce)">Commerce</b>
    <b style="color:var(--operations)">Operations</b>
  </span>
</div>

<div class="zoom">
  <button id="zoomOut" title="Zoom Out ( - )">−</button>
  <button id="zoomReset" title="Reset Zoom">100%</button>
  <button id="zoomIn" title="Zoom In ( + )">+</button>
</div>

<div id="toast" class="toast"><span>✨</span> <span id="toastText">Ready</span></div>
</div>

<aside id="drawer" class="drawer" aria-hidden="true">
  <div class="drawer-head">
    <div id="drawerIcon" class="drawer-icon-box">💊</div>
    <div class="grow">
      <div id="drawerTitle" class="drawer-title">Component</div>
      <div id="drawerDesc" class="drawer-desc"></div>
    </div>
    <button id="closeBtn" class="close" aria-label="Close drawer">✕</button>
  </div>
  <div class="tabs">
    <button class="tab active" data-tab="overview">Overview</button>
    <button class="tab" data-tab="architecture">Inside Logic</button>
    <button class="tab" data-tab="access">Access Map</button>
    <button class="tab" data-tab="data">Data &amp; Security</button>
  </div>
  <div class="drawer-body">
    <section id="tab-overview" class="tabpane active"></section>
    <section id="tab-architecture" class="tabpane"></section>
    <section id="tab-access" class="tabpane"></section>
    <section id="tab-data" class="tabpane"></section>
  </div>
</aside>

<div id="matrixOverlay" class="matrix-overlay" aria-hidden="true">
  <div class="matrix">
    <div class="matrix-head">
      <div>
        <h2>Role Access Matrix</h2>
        <p>✓ = Authorized · ~ = Approval / Scoped · — = Restricted. Click any module to open specs.</p>
      </div>
      <button id="matrixClose" class="matrix-close">✕ Close</button>
    </div>
    <div id="matrixContent"></div>
  </div>
</div>
</main>
</div>
"""

# Append upgraded Javascript
html += js_raw

# Add enhanced interactive filter handling and keyboard shortcuts script before </body>
enhanced_js = """
// Additional UI Enhancements (Category Filter Pills & Keyboard Shortcuts)
document.querySelector('.filter-pills')?.addEventListener('click', (e) => {
  const btn = e.target.closest('.filter-btn');
  if (!btn) return;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  
  const filter = btn.dataset.filter;
  const nodes = document.querySelectorAll('#nodes .node');
  let count = 0;
  
  nodes.forEach(g => {
    const id = g.dataset.id;
    if (filter === 'all') {
      g.style.display = '';
      count++;
    } else if (filter === 'role') {
      const isRole = id.startsWith('role-') || ['admin','pharmacist','cashier','patient','supplier','delivery'].includes(id);
      g.style.display = isRole ? '' : 'none';
      if (isRole) count++;
    } else if (filter === 'clinical') {
      const isClin = id.includes('clinical') || ['rx','safety','patientSvc','refill','controlled','erx','drugdb'].includes(id);
      g.style.display = isClin ? '' : 'none';
      if (isClin) count++;
    } else if (filter === 'inventory') {
      const isInv = id.includes('inventory') || ['catalog','procure','quality','branch','supplier'].includes(id);
      g.style.display = isInv ? '' : 'none';
      if (isInv) count++;
    } else if (filter === 'commerce') {
      const isCom = id.includes('commerce') || ['pos','billing','payments','orders','loyalty','payment','gst'].includes(id);
      g.style.display = isCom ? '' : 'none';
      if (isCom) count++;
    } else if (filter === 'operations') {
      const isOps = id.includes('ops') || ['deliverySvc','notifications','finance','analytics','compliance','workforce','accounting','deliveryext','messaging'].includes(id);
      g.style.display = isOps ? '' : 'none';
      if (isOps) count++;
    } else if (filter === 'infra') {
      const isInfra = ['coredb','cache','searchidx','queue','storage','auditlog','reportdb','infra'].includes(id);
      g.style.display = isInfra ? '' : 'none';
      if (isInfra) count++;
    }
  });
  
  toastMsg(`Showing ${count} modules for filter: ${btn.textContent.trim()}`);
});

// Keyboard shortcut '/' for search
document.addEventListener('keydown', (e) => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    search.focus();
    search.select();
  }
});
</script>
</body>
</html>
"""

if '</script>' in html:
    html = html.replace('</script>\n</body>\n</html>', enhanced_js)
    html = html.replace('</script></body></html>', enhanced_js)
else:
    html += enhanced_js

# Write output file
out_path = r'C:\Users\piyush\.gemini\antigravity-ide\scratch\pharmacy-architecture\index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved upgraded HTML to scratch/pharmacy-architecture/index.html. File size:", os.path.getsize(out_path))

# Also copy to Downloads folder to upgrade original file
downloads_path = r'c:\Users\piyush\Downloads\pharmacy_management_architecture2.html'
with open(downloads_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved upgraded HTML to Downloads/pharmacy_management_architecture2.html. File size:", os.path.getsize(downloads_path))
