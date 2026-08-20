// app.js · wire everything
document.addEventListener('DOMContentLoaded', () => {
  // Init subsystems
  Files.init();
  AgentManager.init();
  Chat.init();
  bindTabs();
  bindModals();
  loadSettings();
  updateMemStats();
});

function bindTabs() {
  document.querySelectorAll('.ios-tab').forEach(t => {
    t.onclick = () => {
      document.querySelectorAll('.ios-tab').forEach(x => x.classList.remove('active'));
      document.querySelectorAll('.view').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
      const view = document.getElementById('view-' + t.dataset.tab);
      if (view) view.classList.add('active');
      const titles = { files: 'Archivos', chat: 'Chat', agents: 'Agentes', memory: 'Memoria' };
      document.getElementById('iosTitle').textContent = titles[t.dataset.tab] || '';
    };
  });
  // Action button (+)
  document.getElementById('iosAction').onclick = () => {
    const active = document.querySelector('.ios-tab.active').dataset.tab;
    if (active === 'files') addFile();
    else if (active === 'chat') document.getElementById('chatNew').click();
    else if (active === 'agents') NctLib.toast('🤖 Agentes preconfigurados');
    else if (active === 'memory') NctLib.toast('🧠 Memoria activa');
  };
  document.getElementById('chatNew').onclick = () => {
    Chat.messages = []; Chat.save(); Chat.render();
    NctLib.toast('💬 Nueva conversación');
  };
}

function bindModals() {
  document.getElementById('fileClose').onclick = () => document.getElementById('fileDetail').classList.remove('open');
  document.getElementById('cancelSend').onclick = () => document.getElementById('sendToAgent').classList.remove('open');
  document.getElementById('cancelPicker').onclick = () => document.getElementById('filePicker').classList.remove('open');
  document.querySelectorAll('.ios-modal').forEach(m => {
    m.onclick = e => { if (e.target === m) m.classList.remove('open'); };
  });
}

function addFile() {
  // Demo: agregar archivo de texto
  const nombre = prompt('Nombre del archivo (ejemplo.md):');
  if (!nombre) return;
  const content = prompt('Contenido (opcional):') || `# ${nombre}\n\nCreado en NCT Hub`;
  Files.add({
    id: NctLib.uuid(),
    name: nombre, type: nombre.split('.').pop(),
    size: content.length, content, folder: '/', starred: false,
    agents: [], createdAt: Date.now(),
  });
  NctLib.toast(`📄 ${nombre} creado`);
}

function loadSettings() {
  // Cargar API keys si están en .env inyectadas via localStorage
  // (esto se haría normalmente via backend, no en cliente por seguridad)
  // Para la demo, las keys se configuran via prompt si no están
  if (!localStorage.getItem('NVIDIA_API_KEY_1')) {
    // Demo mode: usar keys de la env del sistema
    // No las pongo en cliente por seguridad — el backend las inyecta
  }
}

function updateMemStats() {
  const stats = document.getElementById('memStats');
  if (!stats) return;
  const memWorking = NctLib.load(STORAGE.memWorking, '');
  const memLong = NctLib.load(STORAGE.memLong, []);
  const memObsidian = NctLib.load(STORAGE.memObsidian, []);
  const memGraphiti = NctLib.load(STORAGE.memGraphiti, []);
  const memAudit = NctLib.load(STORAGE.memAudit, []);
  const allMsgs = Chat.messages;
  const totalChars = memWorking.length + memLong.reduce((s, m) => s + (m.content || '').length, 0)
    + memObsidian.reduce((s, m) => s + (m.content || '').length, 0)
    + allMsgs.reduce((s, m) => s + (m.text || '').length, 0);
  const tokens = Math.floor(totalChars / 4);
  stats.innerHTML = `
    <div class="stat"><b>Tokens</b><span>${(tokens/1000).toFixed(1)}K</span></div>
    <div class="stat"><b>Mensajes</b><span>${allMsgs.length}</span></div>
    <div class="stat"><b>Archivos</b><span>${Files.list.length}</span></div>
    <div class="stat"><b>Agentes</b><span>${AGENTS.length}</span></div>
  `;
  // Update long-term
  const longList = document.getElementById('memLongList');
  if (longList) longList.innerHTML = memLong.slice(0, 50).map(m => `
    <div class="mem-list-item">📄 ${NctLib.escape(m.name)} · ${NctLib.fmtSize((m.content || '').length)} · ${NctLib.fmtTime(m.ts)}</div>
  `).join('') || '<p class="hint">Memoria long-term vacía</p>';
  // Obsidian
  const obsList = document.getElementById('memObsidianList');
  if (obsList) obsList.innerHTML = memObsidian.slice(0, 50).map(m => `
    <div class="mem-list-item">🗒 ${NctLib.escape(m.name)} · ${NctLib.fmtSize((m.content || '').length)}</div>
  `).join('') || '<p class="hint">Vault Obsidian vacío</p>';
  // Graphiti (graph simple)
  const gv = document.getElementById('graphView');
  if (gv) {
    const nodes = memGraphiti.slice(0, 10);
    gv.innerHTML = nodes.length === 0 ? '<p class="hint" style="text-align:center;padding:30px">Knowledge graph vacío</p>' : renderGraph(nodes);
  }
  // Audit
  const auditList = document.getElementById('memAuditList');
  if (auditList) auditList.innerHTML = memAudit.slice(0, 50).map(m => `
    <div class="mem-list-item">🔍 ${NctLib.escape(m.name || m.text || JSON.stringify(m))} · ${NctLib.fmtTime(m.ts)}</div>
  `).join('') || '<p class="hint">Sin entradas de auditoría</p>';
  // Working memory
  const mw = document.getElementById('memWorking');
  if (mw && !mw.value) mw.value = memWorking;
  if (mw) mw.oninput = () => NctLib.save(STORAGE.memWorking, mw.value);
}

function renderGraph(nodes) {
  const W = 300, H = 280;
  const cx = W/2, cy = H/2;
  let html = `<svg width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">`;
  html += `<line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="rgba(0,184,255,0.3)"/>`;
  nodes.forEach((n, i) => {
    const angle = (i / nodes.length) * Math.PI * 2;
    const x = cx + Math.cos(angle) * 90;
    const y = cy + Math.sin(angle) * 90;
    html += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="rgba(0,184,255,0.3)"/>`;
    html += `<circle cx="${x}" cy="${y}" r="14" fill="#00b8ff"/>`;
    html += `<text x="${x}" y="${y+4}" text-anchor="middle" fill="#000" font-size="9" font-weight="bold">${(n.name || '?').slice(0,6)}</text>`;
  });
  html += `<circle cx="${cx}" cy="${cy}" r="20" fill="#00d4aa"/>`;
  html += `<text x="${cx}" y="${cy+4}" text-anchor="middle" fill="#000" font-size="10" font-weight="bold">NCT</text>`;
  html += `</svg>`;
  return html;
}

// Memory tabs
document.querySelectorAll('.mem-tab').forEach(t => {
  t.onclick = () => {
    document.querySelectorAll('.mem-tab').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.mem-content-tab').forEach(x => x.hidden = true);
    document.getElementById('memWorking').hidden = t.dataset.mem !== 'working';
    document.getElementById('memLong').hidden = t.dataset.mem !== 'long';
    document.getElementById('memObsidian').hidden = t.dataset.mem !== 'obsidian';
    document.getElementById('memGraphiti').hidden = t.dataset.mem !== 'graphiti';
    document.getElementById('memAudit').hidden = t.dataset.mem !== 'audit';
    t.classList.add('active');
  };
});

// Init WebSocket relay to VPS (Modo 1 escalable)
Relay.init();
Relay.startHeartbeat();
Relay.checkHealth();
console.log('[NCT Hub] ready · 4 views · 16 modelos · 8 agentes · 5 APIs NVIDIA');
// === SANDBOXES (5 separados) ===
document.getElementById('sbRun')?.addEventListener('click', runSandboxCode);
document.getElementById('sbInput')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') { e.preventDefault(); runSandboxCode(); }
});
document.getElementById('debateRun')?.addEventListener('click', runDebate);

async function runSandboxCode() {
  const code = document.getElementById('sbInput').value.trim();
  if (!code) return;
  const lang = document.getElementById('sbLang').value;
  NctLib.toast(`▶ ${Sandboxes.current}: ejecutando ${lang}...`);
  await Sandboxes.runCode(code, lang);
  NctLib.toast(`✓ ${Sandboxes.current} listo`);
}

async function runDebate() {
  const q = document.getElementById('debateQuestion').value.trim();
  const opts = document.getElementById('debateOptions').value.trim();
  if (!q) return NctLib.toast('⚠️ Escribí una pregunta');
  const options = opts ? opts.split('\n').filter(Boolean) : null;
  const result = document.getElementById('debateResult');
  result.innerHTML = '<p class="hint" style="text-align:center;padding:20px">⏳ 5 sandboxes debatiendo...</p>';
  NctLib.toast('🗣 Debate iniciado entre 5 sandboxes');
  const debate = await Sandboxes.debate(q, options);
  // Render
  let html = `<div class="v" style="background:var(--bg2);padding:12px;border-radius:8px;margin-bottom:8px;border-left:3px solid var(--teal)">
    <h4 style="color:var(--title-color);margin:0 0 6px">📋 Pregunta</h4>
    <p style="margin:0">${debate.question}</p>
  </div>`;
  if (debate.options) {
    html += `<div class="v" style="background:var(--bg2);padding:12px;border-radius:8px;margin-bottom:8px">
      <h4 style="color:var(--title-color);margin:0 0 6px">🎯 Opciones</h4>
      <ol style="margin:0;padding-left:20px">${debate.options.map(o => `<li>${o}</li>`).join('')}</ol>
    </div>`;
  }
  for (const p of debate.positions) {
    html += `<div class="v" style="background:var(--bg2);padding:12px;border-radius:8px;margin-bottom:6px;border-left:3px solid var(--azure)">
      <h4 style="margin:0 0 4px">${p.emoji} ${p.name}</h4>
      <p style="margin:0;font-size:13px">${p.answer}</p>
      ${p.vote !== null && p.vote !== undefined ? `<small style="color:var(--teal)">→ Voto: opción ${p.vote + 1}</small>` : ''}
    </div>`;
  }
  if (debate.consensus.type === 'vote') {
    const total = Object.values(debate.consensus.votes).reduce((a,b)=>a+b, 0);
    html += `<div class="v" style="background:rgba(0,212,170,0.1);padding:14px;border-radius:8px;border:1px solid var(--teal);margin-top:12px">
      <h3 style="color:var(--teal);margin:0 0 6px">✅ CONSENSO: ${debate.consensus.winner}</h3>
      <p style="margin:0;font-size:13px">${debate.consensus.unanimity ? '🎉 Unanimidad' : 'Mayoría'} · ${debate.consensus.votes[debate.consensus.winner_idx]}/${total} votos</p>
    </div>`;
  } else if (debate.consensus.type === 'open_ended') {
    html += `<div class="v" style="background:rgba(255,217,61,0.1);padding:14px;border-radius:8px;border:1px solid var(--warn);margin-top:12px">
      <h3 style="color:var(--warn);margin:0 0 6px">💬 RESPUESTAS ABIERTAS</h3>
      <pre style="margin:0;font-size:12px;white-space:pre-wrap;font-family:inherit">${debate.consensus.summary}</pre>
    </div>`;
  }
  result.innerHTML = html;
  NctLib.toast(debate.consensus.type === 'vote' ? `🎯 Consenso: ${debate.consensus.winner}` : '💬 Debate abierto completo');
}

// Init sandboxes
Sandboxes.init();

// Update sandbox count
const _origRun = Sandboxes.runCode;
Sandboxes.runCode = async function(code, lang) {
  const result = await _origRun.call(this, code, lang);
  const sb = this.get(this.current);
  document.getElementById('currentSandboxCount').textContent = `${sb.history.length} ejecuciones`;
  return result;
};

// === WORKBENCH · sandbox prioritario del orquestador ===
const WB = {
  log: [],
  init() {
    this.logTo('Workbench listo · Mavis-417847400026327');
    this.logTo('5 sandboxes subordinados');
    this.logTo('8 agentes reales persistentes');
    this.logTo('WS relay: ' + (Relay.connected ? 'conectado' : 'desconectado'));
    this.logTo('Bitácora: MEMORIA/logs/CHAT-V22-AUTOLOG.md');
    this.logTo('---');
    this.logTo('Comandos:');
this.logTo('  list - listar tareas');
this.logTo('  dag goal="<texto>" nodes=n1:A1:ocr,n2:A2:audit - crear DAG y escribir a state.json');
this.logTo('  validate <id> - validar tarea');
this.logTo('  status - estado del sistema');
this.logTo('  bitacora - abrir bitácora');
    this.refreshStatus();
    this.interval = setInterval(() => this.refreshStatus(), 5000);
  },
  logTo(text) {
    const t = new Date().toLocaleTimeString();
    this.log.push(`[${t}] ${text}`);
    if (this.log.length > 50) this.log.shift();
    this.renderLog();
  },
  renderLog() {
    const el = document.getElementById('wbConsole');
    if (el) el.textContent = this.log.join('\n');
  },
  async refreshStatus() {
    // Peers del relay
    const peersEl = document.getElementById('wbPeers');
    if (peersEl) peersEl.textContent = Relay.peers.length || 0;
    const relayEl = document.getElementById('wbRelay');
    if (relayEl) relayEl.textContent = Relay.connected ? '🟢 conectado' : '🔴 offline';
    // Tareas via GitHub raw
    try {
      const r = await fetch('https://raw.githubusercontent.com/maxbry123-commits/TAREAS-PENDIENTES/main/state.json?_=' + Date.now());
      if (r.ok) {
        const state = await r.json();
        const pending = state.tasks.filter(t => t.status === 'pending').length;
        const done = state.tasks.filter(t => t.status === 'done').length;
        const pendingEl = document.getElementById('wbPending');
        const doneEl = document.getElementById('wbDone');
        if (pendingEl) pendingEl.textContent = pending;
        if (doneEl) doneEl.textContent = done;
      }
    } catch (e) { /* silencioso */ }
    // Bitácora sync
    try {
      const r = await fetch('https://api.github.com/repos/maxbry123-commits/MEMORIA/commits?per_page=1');
      if (r.ok) {
        const d = await r.json();
        const last = d[0]?.commit?.author?.date;
        const el = document.getElementById('wbBitacora');
        if (el && last) el.textContent = NctLib.fmtTime(new Date(last).getTime());
      }
    } catch (e) {}
  },
  async run(cmd) {
    this.logTo(`> ${cmd}`);
    const parts = cmd.trim().split(/\s+/);
    if (parts[0] === 'list') {
      try {
        const r = await fetch('https://raw.githubusercontent.com/maxbry123-commits/TAREAS-PENDIENTES/main/state.json?_=' + Date.now());
        if (r.ok) {
          const state = await r.json();
          for (const t of state.tasks) {
            this.logTo(`  [${t.assigned_to}] ${t.id} ${t.status.padEnd(20)} ${(t.instruction || '').slice(0, 50)}`);
          }
        } else this.logTo('⚠️ No pude leer state.json');
      } catch (e) { this.logTo('❌ ' + e.message); }
    } else if (parts[0] === 'add' && (parts[1] === 'A1' || parts[1] === 'A2')) {
      const instr = parts.slice(2).join(' ').replace(/^["']|["']$/g, '');
      this.logTo(`📋 Asignando a ${parts[1]}: ${instr.slice(0, 60)}`);
      this.logTo('💡 Usá: export GITHUB_PAT_MAXBRY=... y python3 add_task.py en el repo TAREAS-PENDIENTES');
      this.logTo('   o pedímelo y lo hago yo vía API');
    } else if (parts[0] === 'validate' && parts.length >= 2) {
      this.logTo(`✅ Para validar: python3 validate.py ${parts[1]} --accept (o --reject "feedback")`);
    } else if (parts[0] === 'help' || parts[0] === '?') {
      this.logTo('Comandos:');
      this.logTo('  list - listar tareas de state.json');
      this.logTo('  add A1|A2 <instr> - guía para asignar');
      this.logTo('  validate <task_id> - guía para validar');
      this.logTo('  status - ver estado del sistema');
      this.logTo('  bitacora - abrir bitácora');
    } else if (parts[0] === 'status') {
      this.refreshStatus();
      this.logTo('✓ status refrescado');
    } else if (parts[0] === 'bitacora') {
      window.open('https://github.com/maxbry123-commits/MEMORIA/blob/main/logs/CHAT-V22-AUTOLOG.md', '_blank');
      this.logTo('📒 Bitácora abierta en nueva tab');
    } else {
      this.logTo('❓ comando no reconocido. probá: help, list, status, bitacora');
    }
  },
};
window.WB = WB;

// Bind handlers del workbench
document.getElementById('wbRun')?.addEventListener('click', () => {
  const v = document.getElementById('wbInput').value;
  if (v) WB.run(v);
});
document.getElementById('wbInput')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') { e.preventDefault(); document.getElementById('wbRun').click(); }
});
document.querySelectorAll('.dsl-card').forEach(c => {
  c.onclick = () => {
    const d = c.dataset.dsl;
    const url = d === 'orquestador'
      ? 'https://raw.githubusercontent.com/maxbry123-commits/MEMORIA/main/logs/MD-1-DSL-MAVIS-ORQUESTADOR.md'
      : d === 'a1'
      ? 'https://raw.githubusercontent.com/maxbry123-commits/MEMORIA/main/logs/MD-2-DSL-MAVIS-WORKER-A1.md'
      : 'https://raw.githubusercontent.com/maxbry123-commits/MEMORIA/main/logs/MD-3-DSL-MAVIS-WORKER-A2.md';
    navigator.clipboard.writeText('Ver DSL en: ' + url);
    NctLib.toast('📋 URL copiada al clipboard');
    window.open(url, '_blank');
  };
});
document.getElementById('qaAssign')?.addEventListener('click', () => {
  document.getElementById('wbInput').value = 'add A1 ';
  document.getElementById('wbInput').focus();
});
document.getElementById('qaAssign2')?.addEventListener('click', () => {
  document.getElementById('wbInput').value = 'add A2 ';
  document.getElementById('wbInput').focus();
});
document.getElementById('qaValidate')?.addEventListener('click', async () => {
  try {
    const r = await fetch('https://raw.githubusercontent.com/maxbry123-commits/TAREAS-PENDIENTES/main/state.json?_=' + Date.now());
    if (r.ok) {
      const state = await r.json();
      const pending = state.tasks.filter(t => t.status === 'pending' || t.status === 'needs_correction');
      if (pending.length) {
        document.getElementById('wbInput').value = `validate ${pending[0].id}`;
        NctLib.toast(`📋 ${pending.length} tareas por validar`);
      } else {
        NctLib.toast('✅ Sin tareas pendientes');
      }
    }
  } catch (e) { NctLib.toast('⚠️ No pude leer pizarra'); }
});
document.getElementById('qaBitacora')?.addEventListener('click', () => WB.run('bitacora'));

// Init cuando se carga la tab
const _origSetTab = document.querySelectorAll('.ios-tab')[0]?.onclick;
document.querySelectorAll('.ios-tab').forEach(t => {
  t.addEventListener('click', () => {
    if (t.dataset.tab === 'workbench') {
      setTimeout(() => WB.init(), 100);
    }
  });
});

// Inicializar al cargar
WB.init();

// === DAG MANAGER · cómo YO (M3 manager) doy las órdenes ===
const DAGManager = {
  // Schema validator
  validateDag(dag) {
    const errors = [];
    if (!dag.id) errors.push('falta id');
    if (!dag.goal) errors.push('falta goal');
    if (!Array.isArray(dag.nodes) || !dag.nodes.length) errors.push('falta nodes[]');
    // Verificar que no haya ciclos (topological sort)
    const ids = new Set(dag.nodes.map(n => n.id));
    for (const n of dag.nodes) {
      if (!n.id) errors.push(`nodo sin id`);
      if (!n.assigned_to) errors.push(`${n.id}: falta assigned_to`);
      if (!['A1', 'A2', 'A3'].includes(n.assigned_to)) errors.push(`${n.id}: assigned_to debe ser A1/A2/A3`);
      if (n.deps) for (const d of n.deps) {
        if (!ids.has(d)) errors.push(`${n.id}: dep ${d} no existe`);
      }
    }
    // Cycle check simple
    const visiting = new Set();
    const visited = new Set();
    const hasCycle = (id) => {
      if (visited.has(id)) return false;
      if (visiting.has(id)) return true;
      visiting.add(id);
      const node = dag.nodes.find(n => n.id === id);
      if (node?.deps) for (const d of node.deps) if (hasCycle(d)) return true;
      visiting.delete(id);
      visited.add(id);
      return false;
    };
    for (const n of dag.nodes) if (hasCycle(n.id)) errors.push(`ciclo detectado desde ${n.id}`);
    return errors;
  },

  // Topological sort
  topoSort(dag) {
    const sorted = [];
    const visited = new Set();
    const visit = (id) => {
      if (visited.has(id)) return;
      const node = dag.nodes.find(n => n.id === id);
      if (!node) return;
      if (node.deps) for (const d of node.deps) visit(d);
      visited.add(id);
      sorted.push(node);
    };
    for (const n of dag.nodes) visit(n.id);
    return sorted;
  },

  // Construir task desde nodo DAG
  nodeToTask(node, dagId) {
    return {
      id: 'task_' + Date.now().toString(16) + Math.random().toString(16).slice(2, 6),
      dag_node: node.id,
      dag_id: dagId,
      assigned_to: node.assigned_to,
      status: 'pending',
      deps: (node.deps || []).map(d => `task_dep_${d}`),
      capability: node.capability,
      connector: node.connector,
      accion: node.accion,
      params: node.params || {},
      instruction: node.instruction || this.autoDescribe(node),
      context: {
        sandbox: this.sandboxOf(node.assigned_to),
        dag_id: dagId,
        dag_node: node.id,
        repo: this.repoOf(node.assigned_to),
        ...(node.context || {}),
      },
      tools_allowed: node.tools_allowed || ['shell', 'file_read', 'file_write', 'fetch', 'git', 'python3'],
      timeout_ms: node.timeout_ms || 1800000,
      on_error: node.on_error || 'continue',
      result: null,
      created_at: new Date().toISOString(),
    };
  },

  // Auto-describir nodo para el worker
  autoDescribe(node) {
    if (node.instruction) return node.instruction;
    if (node.capability) return `Ejecutar capability '${node.capability}' con params: ${JSON.stringify(node.params || {})}`;
    if (node.connector) return `Llamar connector '${node.connector}' acción '${node.accion}' con params: ${JSON.stringify(node.params || {})}`;
    return `Nodo ${node.id} del DAG ${node.dag_id}`;
  },

  // Sandbox de cada worker
  sandboxOf(assignedTo) {
    return { 'A1': '/tmp/sandbox-tarea-1', 'A2': '/tmp/sandbox-tarea-2', 'A3': '/tmp/sandbox-tarea-3' }[assignedTo];
  },
  repoOf(assignedTo) {
    return { 'A1': 'maxbry123-commits/nct-hub', 'A2': 'maxbry123-commits/orchestrator-auditor', 'A3': 'maxbry123-commits/ws-relay' }[assignedTo];
  },

  // Persistir DAG a state.json
  async writeDag(dag) {
    const errors = this.validateDag(dag);
    if (errors.length) return { ok: false, errors };

    const tasks = this.topoSort(dag).map(n => this.nodeToTask(n, dag.id));

    // Escribir al state.json via GitHub API
    try {
      const currentSha = await this.getFileSha('maxbry123-commits/TAREAS-PENDIENTES', 'state.json');
      const current = await this.getFile('maxbry123-commits/TAREAS-PENDIENTES', 'state.json');
      current.tasks = [...(current.tasks || []), ...tasks];
      current.dags = current.dags || [];
      current.dags.push({ id: dag.id, goal: dag.goal, created_at: dag.created_at, status: 'running' });
      current.updated_at = new Date().toISOString();
      const content = btoa(unescape(encodeURIComponent(JSON.stringify(current, null, 2))));
      const r = await fetch(`https://api.github.com/repos/maxbry123-commits/TAREAS-PENDIENTES/contents/state.json`, {
        method: 'PUT',
        headers: { 'Authorization': 'token ' + (window.GITHUB_PAT || ''), 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `DAG ${dag.id}: ${dag.goal}`,
          content, sha: currentSha,
        }),
      });
      if (!r.ok) {
        // Si falla la API directa (no hay token en el browser), fallback a mostrar el YAML
        return { ok: false, error: 'No se pudo escribir via API. Token no configurado.', dag, tasks };
      }
      // Bitácora
      await this.logBitacora(`DAG ${dag.id} creado: ${dag.goal} (${tasks.length} tasks)`);
      return { ok: true, dag, tasks };
    } catch (e) {
      return { ok: false, error: e.message, dag, tasks };
    }
  },

  async getFile(repo, path) {
    const r = await fetch(`https://api.github.com/repos/${repo}/contents/${path}`);
    const d = await r.json();
    return JSON.parse(atob(d.content.replace(/\n/g, '')));
  },
  async getFileSha(repo, path) {
    const r = await fetch(`https://api.github.com/repos/${repo}/contents/${path}`);
    const d = await r.json();
    return d.sha;
  },
  async logBitacora(entry) {
    try {
      const r = await fetch('https://api.github.com/repos/maxbry123-commits/MEMORIA/contents/logs/CHAT-V22-AUTOLOG.md');
      const d = await r.json();
      const current = atob(d.content.replace(/\n/g, ''));
      const newContent = current + `\n## ${new Date().toISOString()} · M3-Manager\n- ${entry}\n`;
      const content = btoa(unescape(encodeURIComponent(newContent)));
      await fetch(`https://api.github.com/repos/maxbry123-commits/MEMORIA/contents/logs/CHAT-V22-AUTOLOG.md`, {
        method: 'PUT',
        headers: { 'Authorization': 'token ' + (window.GITHUB_PAT || ''), 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: entry, content, sha: d.sha, branch: 'main' }),
      });
    } catch (e) { console.warn('Bitacora write failed', e); }
  },
};

window.DAGManager = DAGManager;

// === WORKBENCH CONSOLE · versión DAG-aware ===
// Override el WB.run para que use el DSL DAG schema
const _origWBRun = WB.run;
WB.run = async function(cmd) {
  const parts = cmd.trim().split(/\s+/);
  if (parts[0] === 'dag' || parts[0] === 'order') {
    // Crear un DAG desde el comando
    // Sintaxis: dag goal=<texto> nodes=N1:A1:ocr,N2:A2:audit
    const goalMatch = cmd.match(/goal=([^\s]+(?:\s+[^\s]+)*?)\s+nodes=/);
    const nodesMatch = cmd.match(/nodes=([^\n]+)/);
    if (!goalMatch || !nodesMatch) {
      this.logTo('❌ Sintaxis: dag goal="<texto>" nodes=N1:A1:ocr,N2:A2:audit');
      return;
    }
    const goal = goalMatch[1].replace(/^"|"$/g, '');
    const nodes = nodesMatch[1].split(',').map(s => {
      const [id, who, what, ...rest] = s.split(':');
      return { id, assigned_to: who, capability: what, params: rest.length ? JSON.parse(rest.join(':')) : {} };
    });
    const dag = {
      id: 'ord_' + Date.now().toString(16),
      created_at: new Date().toISOString(),
      created_by: 'Mavis-417847400026327',
      goal, nodes,
    };
    this.logTo(`📐 Construyendo DAG ${dag.id}...`);
    const errors = DAGManager.validateDag(dag);
    if (errors.length) { this.logTo('❌ Errores:'); errors.forEach(e => this.logTo('  - ' + e)); return; }
    this.logTo(`✓ DAG válido · ${dag.nodes.length} nodos`);
    const r = await DAGManager.writeDag(dag);
    if (r.ok) {
      this.logTo(`✓ DAG ${dag.id} escrito a state.json`);
      this.logTo(`  ${r.tasks.length} tasks creadas, asignadas a:`);
      r.tasks.forEach(t => this.logTo(`    - ${t.dag_node} → ${t.assigned_to} (${t.capability || t.connector})`));
      this.logTo(`📒 Bitácora: 1 entrada`);
    } else {
      this.logTo(`⚠️ ${r.error || 'fallback mode'}`);
      this.logTo('DAG generado (para commit manual):');
      this.logTo(JSON.stringify(dag, null, 2));
    }
    return;
  }
  // Si no es dag, fallback al run original
  return _origWBRun.call(this, cmd);
};

// Quick action: "Generar DAG desde template"
document.getElementById('qaAssign')?.addEventListener('click', () => {
  document.getElementById('wbInput').value = 'dag goal="Tarea A1" nodes=n1:A1:code';
  document.getElementById('wbInput').focus();
  WB.logTo('💡 Editá el goal y nodos, después Enter para enviar');
});
document.getElementById('qaAssign2')?.addEventListener('click', () => {
  document.getElementById('wbInput').value = 'dag goal="Tarea A2" nodes=n1:A2:research';
  document.getElementById('wbInput').focus();
});
