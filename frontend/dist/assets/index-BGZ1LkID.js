(function(){const o=document.createElement("link").relList;if(o&&o.supports&&o.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))t(e);new MutationObserver(e=>{for(const i of e)if(i.type==="childList")for(const c of i.addedNodes)c.tagName==="LINK"&&c.rel==="modulepreload"&&t(c)}).observe(document,{childList:!0,subtree:!0});function a(e){const i={};return e.integrity&&(i.integrity=e.integrity),e.referrerPolicy&&(i.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?i.credentials="include":e.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function t(e){if(e.ep)return;e.ep=!0;const i=a(e);fetch(e.href,i)}})();const l={menu:'<svg class="icon" viewBox="0 0 24 24"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>',info:'<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',more:'<svg class="icon" viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.5" fill="currentColor"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><circle cx="19" cy="12" r="1.5" fill="currentColor"/></svg>',close:'<svg class="icon" viewBox="0 0 24 24"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>',plus:'<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>',search:'<svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',skills:'<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>',clock:'<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/></svg>',folder:'<svg class="icon" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7l-2-2H5a2 2 0 0 0-2 2z"/></svg>',mobile:'<svg class="icon" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18.01"/></svg>',leaf:'<svg class="icon" viewBox="0 0 24 24"><path d="M12 2C8 6 6 9 6 13a6 6 0 0 0 12 0c0-4-2-7-6-11z"/></svg>',arrowUp:'<svg class="icon" viewBox="0 0 24 24"><path d="M12 4v12m0 0l-4-4m4 4l4-4M5 20h14"/></svg>'};function C(s,{title:o,onMenu:a,onMore:t}){s.innerHTML=`
    <button class="topbar__btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="sidebar" id="btnMenu">${l.menu}</button>
    <h1 class="topbar__title">${o}</h1>
    <div class="topbar__actions">
      <button class="topbar__btn" aria-label="Información" id="btnInfo">${l.info}</button>
      <button class="topbar__btn" aria-label="Más opciones" id="btnMoreTop">${l.more}</button>
    </div>
  `,s.querySelector("#btnMenu").onclick=a,s.querySelector("#btnMoreTop").onclick=t}function k(s,{onClose:o,onItem:a}){s.innerHTML=`
    <div class="sidebar__header">
      <div class="sidebar__brand">Claude</div>
      <button class="sidebar__close" aria-label="Cerrar" id="btnCloseSidebar">${l.close}</button>
    </div>
    <button class="sidebar__item sidebar__item--highlight" data-label="New task">${l.plus}<span class="sidebar__item-label">New task</span></button>
    <button class="sidebar__item" data-label="Search">${l.search}<span class="sidebar__item-label">Search</span></button>
    <button class="sidebar__item" data-label="Skills">${l.skills}<span class="sidebar__item-label">Skills</span></button>
    <button class="sidebar__item" data-label="Scheduled">${l.clock}<span class="sidebar__item-label">Scheduled</span></button>
    <button class="sidebar__item" data-label="Assets">${l.folder}<span class="sidebar__item-label">Assets</span></button>
    <button class="sidebar__item" data-label="Connect Mobile">${l.mobile}<span class="sidebar__item-label">Connect Mobile</span></button>
    <div class="sidebar__heading">Show more</div>
    <button class="sidebar__item" data-label="MaxHermes">${l.leaf}<span class="sidebar__item-label">MaxHermes</span></button>
    <button class="sidebar__item" data-label="MaxClaw">${l.leaf}<span class="sidebar__item-label">MaxClaw</span></button>
    <div class="sidebar__heading">Projects</div>
    <button class="sidebar__item" data-label="Add new project">${l.folder}<span class="sidebar__item-label">Add new project</span></button>
    <div class="sidebar__footer">
      <div class="sidebar__avatar">M</div>
      <div class="sidebar__user">
        <div class="sidebar__name">Maxbry Odreman</div>
        <div class="sidebar__plan">Plus Plan</div>
      </div>
      <button class="sidebar__user-action" aria-label="Cerrar sesión" id="btnLogout">${l.arrowUp}</button>
    </div>
  `,s.querySelector("#btnCloseSidebar").onclick=o,s.querySelector("#btnLogout").onclick=()=>{confirm("¿Cerrar sesión?")&&window.osquestador.showToast("Sesión cerrada")},s.querySelectorAll(".sidebar__item").forEach(t=>{t.onclick=()=>a(t.dataset.label)})}const h="";async function d(s,o="GET",a=null){const t={method:o,headers:{"Content-Type":"application/json"}};a&&(t.body=JSON.stringify(a));try{const e=await fetch(h+s,t);if(!e.ok){const i=await e.json().catch(()=>({detail:e.statusText}));throw new Error(i.detail||`HTTP ${e.status}`)}return await e.json()}catch(e){throw console.warn("API error:",s,e.message),e}}async function M(s,o,a){const t=await fetch(h+s,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(o)});if(!t.ok||!t.body)throw new Error("stream failed");const e=t.body.getReader(),i=new TextDecoder;let c="";for(;;){const{done:r,value:n}=await e.read();if(r)break;c+=i.decode(n,{stream:!0});const v=c.split(`
`);c=v.pop();for(const u of v)if(u.startsWith("data: ")){const b=u.slice(6).trim();if(b==="[DONE]")return;try{const w=JSON.parse(b);a(w)}catch{}}}}const f='<svg class="icon" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7l-2-2H5a2 2 0 0 0-2 2z"/></svg>',_='<svg class="icon" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>';function $(s,{onNavigate:o,status:a}){const t=a||{projects:4,tasks:13,artifacts:5};s.innerHTML=`
    <h2 class="greeting">Hola, <em>Max</em></h2>
    <p class="subtitle">${t.projects} proyectos · 9 agentes · 3 modos de memoria</p>

    <article class="card" data-go="artifacts">
      <div class="card__icon">${f}</div>
      <div class="card__info">
        <div class="card__name">osquestador-auditor</div>
        <div class="card__sub">${t.artifacts} artefactos · 23 decisiones</div>
      </div>
    </article>

    <article class="card" data-go="plugins">
      <div class="card__icon">${_}</div>
      <div class="card__info">
        <div class="card__name">Plugins & Skills</div>
        <div class="card__sub">13 plugins · 8 skills</div>
      </div>
    </article>

    <article class="card" data-go="tasks">
      <div class="card__icon">${_}</div>
      <div class="card__info">
        <div class="card__name">Tareas activas</div>
        <div class="card__sub">${t.tasks} tareas en pipeline</div>
      </div>
    </article>

    <article class="card" data-go="chat">
      <div class="card__icon">${f}</div>
      <div class="card__info">
        <div class="card__name">Chat con Claude</div>
        <div class="card__sub">Streaming · Sonnet 5 Bajo</div>
      </div>
    </article>
  `,s.querySelectorAll("[data-go]").forEach(e=>{e.onclick=()=>o(e.dataset.go,e.querySelector(".card__name").textContent)})}const S='<svg class="icon icon--lg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="13" y2="17"/></svg>',T='<svg class="icon icon--lg" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="14" y1="4" x2="10" y2="20"/></svg>',B='<svg class="icon" viewBox="0 0 24 24"><path d="M12 4v12m0 0l-4-4m4 4l4-4M5 20h14"/></svg>',E='<svg class="icon" viewBox="0 0 24 24"><polyline points="18 15 12 9 6 15"/></svg>',L='<svg class="icon icon--sm" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7l-2-2H5a2 2 0 0 0-2 2z"/></svg>';function O(s){s.innerHTML=`
    <div class="artifact-count">${L} <span id="countNum">—</span> artefactos</div>
    <div id="artifactsList"></div>
    <button class="fab" id="scrollTop" aria-label="Ir arriba">${E}</button>
  `,document.getElementById("scrollTop").onclick=()=>s.scrollTo({top:0,behavior:"smooth"})}async function q(s){const o=s.querySelector("#artifactsList"),a=s.querySelector("#countNum");try{const t=await d("/api/artifacts");a.textContent=t.length,o.innerHTML=t.map(e=>{const c=e.type==="py"||e.type==="json"||e.type==="html"||e.type==="css"||e.type==="jsx"?T:S,n=(e.meta?typeof e.meta=="string"?JSON.parse(e.meta):e.meta:{}).desc||(e.type==="md"?"Documento":"Código");return`
        <article class="artifact-card">
          <div class="artifact-card__chip">${c}</div>
          <div class="artifact-card__info">
            <div class="artifact-card__name">${e.name}</div>
            <div class="artifact-card__meta">${n} · ${(e.type||"").toUpperCase()}</div>
          </div>
          <button class="artifact-card__download" data-id="${e.id}" aria-label="Descargar ${e.name}">${B}</button>
        </article>
      `}).join(""),o.querySelectorAll(".artifact-card__download").forEach(e=>{e.onclick=async()=>{try{const i=await d("/api/artifacts/"+e.dataset.id),c=new Blob([i.content],{type:"text/plain"}),r=URL.createObjectURL(c),n=document.createElement("a");n.href=r,n.download=i.name,n.click(),URL.revokeObjectURL(r),window.osquestador.showToast("Descargado: "+i.name)}catch(i){window.osquestador.showToast("Error: "+i.message)}}})}catch{o.innerHTML='<p style="color:var(--fg-muted);padding:20px">Backend offline. <button onclick="location.reload()" style="color:var(--blue)">Reintentar</button></p>'}}const I='<svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="18" x2="15" y2="18"/></svg>',N='<svg class="icon icon--sm" viewBox="0 0 24 24"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 18v3"/></svg>',H='<svg class="icon icon--sm" viewBox="0 0 24 24"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>';function A(s){s.innerHTML=`
    <div class="chat">
      <div class="chat__messages" id="chatMessages">
        <div class="message message--system">Sesión iniciada · Claude Sonnet 5 · osquestador-auditor</div>
      </div>
      <div class="composer">
        <form class="composer__form" id="chatForm">
          <textarea class="composer__input" id="chatInput" rows="1" placeholder="Pregúntale a Claude..." aria-label="Mensaje"></textarea>
          <button type="button" class="icon-btn" aria-label="Adjuntar" id="attachBtn">${H}</button>
          <button type="button" class="icon-btn" aria-label="Micrófono">${N}</button>
          <button type="submit" class="composer__send" aria-label="Enviar" id="sendBtn">${I}</button>
        </form>
      </div>
    </div>
  `}function P(s){const o=s.querySelector("#chatForm"),a=s.querySelector("#chatInput"),t=s.querySelector("#chatMessages"),e=s.querySelector("#sendBtn");a.addEventListener("input",()=>{a.style.height="auto",a.style.height=Math.min(a.scrollHeight,120)+"px"}),a.addEventListener("keydown",i=>{i.key==="Enter"&&!i.shiftKey&&(i.preventDefault(),o.dispatchEvent(new Event("submit")))}),o.addEventListener("submit",async i=>{i.preventDefault();const c=a.value.trim();if(!c)return;const r=document.createElement("div");r.className="message message--user",r.textContent=c,t.appendChild(r),a.value="",a.style.height="auto",t.scrollTop=t.scrollHeight,e.disabled=!0;const n=document.createElement("div");n.className="message message--assistant",n.textContent="",t.appendChild(n);try{await M("/api/chat?stream=true",{messages:[{role:"user",content:c}],model:"claude-sonnet-4.5",project_id:"osquestador-auditor",stream:!0},v=>{v.delta?.text&&(n.textContent+=v.delta.text,t.scrollTop=t.scrollHeight)})}catch{try{const u=await d("/api/chat","POST",{messages:[{role:"user",content:c}],model:"claude-sonnet-4.5",project_id:"osquestador-auditor"});n.textContent=u.content?.[0]?.text||"Error"}catch(u){n.textContent="Error: "+u.message}}finally{e.disabled=!1,t.scrollTop=t.scrollHeight}})}function D(s){s.innerHTML=`
    <h2 class="section-title">Pipeline · <span id="taskTotal">—</span> tareas</h2>
    <div class="kanban" id="kanban"></div>
  `}async function x(s){const o=[{key:"backlog",label:"Backlog"},{key:"doing",label:"Doing"},{key:"review",label:"Review"},{key:"done",label:"Done"}];try{const a=await d("/api/tasks");s.querySelector("#taskTotal").textContent=a.length;const t=s.querySelector("#kanban");t.innerHTML=o.map(i=>{const c=a.filter(r=>r.column===i.key);return`
        <div class="kanban-col" data-col="${i.key}">
          <div class="kanban-col__title">${i.label}<span class="kanban-col__count">${c.length}</span></div>
          ${c.map(r=>`
            <article class="kanban-card" draggable="true" data-id="${r.id}">
              <div class="kanban-card__title">${r.title}</div>
              <div class="kanban-card__meta"><span>${r.agent||"—"}</span> · <span>${r.priority||"med"}</span></div>
            </article>
          `).join("")}
        </div>
      `}).join("");let e=null;t.querySelectorAll(".kanban-card").forEach(i=>{i.addEventListener("dragstart",c=>{e=i.dataset.id,c.dataTransfer.effectAllowed="move"})}),t.querySelectorAll(".kanban-col").forEach(i=>{i.addEventListener("dragover",c=>{c.preventDefault(),c.dataTransfer.dropEffect="move"}),i.addEventListener("drop",async c=>{if(c.preventDefault(),!e)return;const r=i.dataset.col;try{await d(`/api/tasks/${e}`,"PATCH",{column:r}),window.osquestador.showToast("Tarea movida a "+r),x(s)}catch(n){window.osquestador.showToast("Error: "+n.message)}e=null})})}catch{s.querySelector("#kanban").innerHTML='<p style="color:var(--fg-muted);padding:20px">Backend offline.</p>'}}const j='<svg class="icon" viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1" fill="currentColor"/><circle cx="4" cy="12" r="1" fill="currentColor"/><circle cx="4" cy="18" r="1" fill="currentColor"/></svg>',R='<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',z='<svg class="icon" viewBox="0 0 24 24"><path d="M5 8a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8z"/><circle cx="9" cy="10" r="1" fill="currentColor"/><circle cx="15" cy="10" r="1" fill="currentColor"/><line x1="9" y1="15" x2="15" y2="15"/></svg>',F='<svg class="icon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',U='<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><text x="6" y="18" font-family="serif" font-size="16" fill="currentColor" stroke="none">Aa</text></svg>',V='<svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/><circle cx="9" cy="6" r="1.5" fill="currentColor"/><circle cx="15" cy="12" r="1.5" fill="currentColor"/></svg>',G='<svg class="icon" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="2"/><line x1="9" y1="6" x2="9" y2="6.01"/><line x1="15" y1="6" x2="15" y2="6.01"/><line x1="9" y1="10" x2="9" y2="10.01"/><line x1="15" y1="10" x2="15" y2="10.01"/><line x1="9" y1="14" x2="9" y2="14.01"/><line x1="15" y1="14" x2="15" y2="14.01"/><path d="M5 18l-2 3M19 18l2 3"/></svg>',J='<svg class="icon" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',K='<svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',W='<svg class="icon" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',Q='<svg class="icon" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>';function X(s){s.innerHTML=`
    <div style="margin-top:16px">
      <div class="config-group">
        <div class="config-row">${j}<div class="config-row__info"><div class="config-row__label">Capacidades</div><div class="config-row__sub">2 habilitadas</div></div></div>
        <div class="config-row">${R}<div class="config-row__info"><div class="config-row__label">Conectores</div></div></div>
        <div class="config-row">${z}<div class="config-row__info"><div class="config-row__label">Permisos</div></div></div>
      </div>
      <div class="config-group">
        <div class="config-row">${F}<div class="config-row__info"><div class="config-row__label">Modo de color</div><div class="config-row__sub">Sistema</div></div></div>
        <div class="config-row">${U}<div class="config-row__info"><div class="config-row__label">Estilo de fuente</div><div class="config-row__sub">Predeterminado</div></div></div>
        <div class="config-row">${V}<div class="config-row__info"><div class="config-row__label">Voz</div></div></div>
      </div>
      <div class="config-group">
        <div class="config-row">${G}<div class="config-row__info"><div class="config-row__label">Retroalimentación háptica</div></div><button class="toggle" id="toggle1" role="switch" aria-checked="true"></button></div>
        <div class="config-row">${J}<div class="config-row__info"><div class="config-row__label">Notificaciones</div></div></div>
        <div class="config-row">${K}<div class="config-row__info"><div class="config-row__label">Privacidad</div></div></div>
        <div class="config-row">${W}<div class="config-row__info"><div class="config-row__label">Enlaces compartidos</div></div></div>
      </div>
      <div class="config-group">
        <div class="config-row config-row--danger" id="logoutRow">${Q}<div class="config-row__info"><div class="config-row__label">Cerrar sesión</div></div></div>
      </div>
    </div>
  `}function Y(s){const o=s.querySelector("#toggle1");o.onclick=()=>{const a=o.classList.toggle("toggle--off");o.setAttribute("aria-checked",a?"false":"true")},s.querySelector("#logoutRow").onclick=()=>{confirm("¿Cerrar sesión?")&&window.osquestador.showToast("Sesión cerrada")}}function Z(s){s.innerHTML=`
    <h2 class="section-title">13 programas · Click para invocar</h2>
    <div class="plugins-grid" id="pluginsGrid"></div>
  `}async function ee(s){try{const o=await d("/api/plugins"),a=s.querySelector("#pluginsGrid");a.innerHTML=Object.entries(o).map(([t,e])=>`
      <button class="plugin-tile" data-plugin="${t}">
        <div class="plugin-tile__icon">${t.charAt(0).toUpperCase()}</div>
        <div class="plugin-tile__name">${t}</div>
        <div class="plugin-tile__desc">${e.description}</div>
      </button>
    `).join(""),a.querySelectorAll(".plugin-tile").forEach(t=>{t.onclick=async()=>{const e=t.dataset.plugin,c={graphiti:{method:"search",params:{query:"osquestador",top_k:3}},kanboard:{method:"list_tasks",params:{}},paddleocr:{method:"ocr",params:{file_path:"/tmp/sample.png"}},serper:{method:"search",params:{query:"osquestador",num:3}},claude:{method:"_demo",params:{}},observer:{method:"get_status",params:{}},watchdog:{method:"check_openclaw",params:{}},memory:{method:"get_stats",params:{}},research:{method:"loop",params:{query:"osquestador"}},design:{method:"get_tokens",params:{}},build:{method:"build",params:{}},audit:{method:"run",params:{}},dispatch:{method:"send",params:{channel:"telegram",message:"osquestador ok",target:"@maxbry"}}}[e];if(!c){window.osquestador.showToast(`${e}: no default method`);return}try{let r;c.method==="_demo"?(r=await d("/api/chat","POST",{messages:[{role:"user",content:`Describe el plugin ${e}`}],model:"claude-sonnet-4.5",project_id:"osquestador-auditor"}),window.osquestador.showToast(`${e}: ${r.content?.[0]?.text?.slice(0,50)}...`)):(r=await d(`/api/plugins/${e}/${c.method}`,"POST",c.params),window.osquestador.showToast(`${e}.${c.method} OK`),console.log(e,r))}catch(r){window.osquestador.showToast(`Error ${e}: ${r.message}`)}}})}catch{s.querySelector("#pluginsGrid").innerHTML='<p style="color:var(--fg-muted);padding:20px">Backend offline</p>'}}function se(s){s.innerHTML=`
    <h2 class="section-title">Memoria triple</h2>
    <div id="memStats"></div>
    <h2 class="section-title">Búsqueda semántica</h2>
    <form id="memSearch" style="display:flex;gap:8px;margin-bottom:16px">
      <input id="memQuery" placeholder="Buscar..." style="flex:1;background:var(--surface);border:0.5px solid var(--border);color:var(--fg);padding:12px;border-radius:var(--r-md);outline:none" />
      <button class="icon-btn" style="background:var(--accent-coral);color:white" aria-label="Buscar">
        <svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </button>
    </form>
    <div id="memResults"></div>
  `}async function ae(s){const o=s.querySelector("#memStats"),a=s.querySelector("#memResults"),t=s.querySelector("#memSearch");try{const e=await d("/api/memory");o.innerHTML=`
      <div class="mem-card">
        <div class="mem-card__temp mem-card__temp--hot">H</div>
        <div class="card__info" style="flex:1">
          <div class="mem-card__label">HOT · Decisiones en RAM</div>
          <div class="mem-card__sub">D1-D64 + decisiones activas</div>
        </div>
        <div class="card__sub">${e.hot}</div>
      </div>
      <div class="mem-card">
        <div class="mem-card__temp mem-card__temp--warm">W</div>
        <div class="card__info" style="flex:1">
          <div class="mem-card__label">WARM · Episodios Graphiti</div>
          <div class="mem-card__sub">SQLite + FAISS</div>
        </div>
        <div class="card__sub">${e.warm}</div>
      </div>
      <div class="mem-card">
        <div class="mem-card__temp mem-card__temp--cold">C</div>
        <div class="card__info" style="flex:1">
          <div class="mem-card__label">COLD · Repo + Chat history</div>
          <div class="mem-card__sub">Git commits + embeddings</div>
        </div>
        <div class="card__sub">${e.cold}</div>
      </div>
    `}catch{o.innerHTML='<p style="color:var(--fg-muted)">Backend offline</p>'}t.onsubmit=async e=>{e.preventDefault();const i=s.querySelector("#memQuery").value.trim();if(i){a.innerHTML='<p style="color:var(--fg-muted)">Buscando...</p>';try{const c=await d("/api/memory/search","POST",{query:i,top_k:5});if(!c.results||c.results.length===0){a.innerHTML='<p style="color:var(--fg-muted)">Sin resultados</p>';return}a.innerHTML='<div class="card" style="display:block">'+c.results.map(r=>{const n=(r.text||r.value||"").slice(0,200),v=r.score?` <span style="color:var(--fg-muted);font-size:11px">${(r.score*100).toFixed(1)}%</span>`:"";return`<div style="padding:8px 0;border-bottom:0.5px solid var(--border)"><div style="font-size:13px">${n}${r.text&&r.text.length>200?"...":""}</div>${v}</div>`}).join("")+"</div>"}catch(c){a.innerHTML=`<p style="color:var(--accent)">Error: ${c.message}</p>`}}}}const te=document.getElementById("app"),g={view:"dashboard",user:{name:"Maxbry Odreman",plan:"Plus Plan"},status:null};async function ie(){te.innerHTML=`
    <header class="topbar" id="topbar"></header>
    <main class="main" id="main"></main>
    <div id="bottombar"></div>
    <aside class="sidebar" id="sidebar"></aside>
    <div class="scrim" id="scrim"></div>
    <div class="toast" id="toast"></div>
  `,C(document.getElementById("topbar"),{title:"Navidad",onMenu:y,onMore:()=>p("config","Configuración")}),k(document.getElementById("sidebar"),{onClose:m,onItem:s=>{const a={"New task":["dashboard","Navidad"],Search:["memory","Memoria"],Skills:["plugins","Plugins"],Scheduled:["tasks","Tareas"],Assets:["artifacts","Artefactos"],"Connect Mobile":["config","Configuración"],MaxHermes:["plugins","MaxHermes"],MaxClaw:["plugins","MaxClaw"],"Add new project":["config","Configuración"]}[s]||["dashboard","Navidad"];p(a[0],a[1]),m()}}),document.getElementById("scrim").addEventListener("click",m),document.addEventListener("keydown",s=>{s.key==="Escape"&&m()});try{g.status=await d("/api/observer/status")}catch(s){console.warn("backend offline, using cached state",s)}p("dashboard","Navidad"),window.osquestador={switchView:p,openSidebar:y,closeSidebar:m,showToast:s=>oe(s),invoke:(s,o,a)=>d(`/api/plugins/${s}/${o}`,"POST",a),getState:()=>g,version:"1.0.0",plugins:13},console.log("%cOsquestador-Auditor v1.0 · 13 plugins","color:#FF6B6B;font-weight:bold;font-size:14px")}function y(){document.getElementById("sidebar").classList.add("open"),document.getElementById("scrim").classList.add("open"),document.getElementById("topbar").querySelector('[aria-label="Abrir menú"]')?.setAttribute("aria-expanded","true")}function m(){document.getElementById("sidebar").classList.remove("open"),document.getElementById("scrim").classList.remove("open"),document.getElementById("topbar").querySelector('[aria-label="Abrir menú"]')?.setAttribute("aria-expanded","false")}function p(s,o){g.view=s,document.querySelector(".topbar__title").textContent=o;const a=document.getElementById("main");switch(a.innerHTML="",a.scrollTop=0,s){case"dashboard":$(a,{onNavigate:p,status:g.status});break;case"artifacts":O(a),q(a);break;case"chat":A(a),P(a);break;case"tasks":D(a),x(a);break;case"config":X(a),Y(a);break;case"plugins":Z(a),ee(a);break;case"memory":se(a),ae(a);break}}function oe(s,o=2400){const a=document.getElementById("toast");a.textContent=s,a.classList.add("show"),clearTimeout(a._timer),a._timer=setTimeout(()=>a.classList.remove("show"),o)}ie();
