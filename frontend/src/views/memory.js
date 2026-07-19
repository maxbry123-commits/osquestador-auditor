// Memory view: HOT/WARM/COLD stats + search
import { api } from '../lib/api.js'

export function renderMemory(main) {
  main.innerHTML = `
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
  `
}

export async function mountMemory(main) {
  const stats = main.querySelector('#memStats')
  const results = main.querySelector('#memResults')
  const form = main.querySelector('#memSearch')

  try {
    const s = await api('/api/memory')
    stats.innerHTML = `
      <div class="mem-card">
        <div class="mem-card__temp mem-card__temp--hot">H</div>
        <div class="card__info" style="flex:1">
          <div class="mem-card__label">HOT · Decisiones en RAM</div>
          <div class="mem-card__sub">D1-D64 + decisiones activas</div>
        </div>
        <div class="card__sub">${s.hot}</div>
      </div>
      <div class="mem-card">
        <div class="mem-card__temp mem-card__temp--warm">W</div>
        <div class="card__info" style="flex:1">
          <div class="mem-card__label">WARM · Episodios Graphiti</div>
          <div class="mem-card__sub">SQLite + FAISS</div>
        </div>
        <div class="card__sub">${s.warm}</div>
      </div>
      <div class="mem-card">
        <div class="mem-card__temp mem-card__temp--cold">C</div>
        <div class="card__info" style="flex:1">
          <div class="mem-card__label">COLD · Repo + Chat history</div>
          <div class="mem-card__sub">Git commits + embeddings</div>
        </div>
        <div class="card__sub">${s.cold}</div>
      </div>
    `
  } catch (e) {
    stats.innerHTML = `<p style="color:var(--fg-muted)">Backend offline</p>`
  }

  form.onsubmit = async (e) => {
    e.preventDefault()
    const q = main.querySelector('#memQuery').value.trim()
    if (!q) return
    results.innerHTML = '<p style="color:var(--fg-muted)">Buscando...</p>'
    try {
      const r = await api('/api/memory/search', 'POST', { query: q, top_k: 5 })
      if (!r.results || r.results.length === 0) {
        results.innerHTML = '<p style="color:var(--fg-muted)">Sin resultados</p>'
        return
      }
      results.innerHTML = '<div class="card" style="display:block">' + r.results.map(item => {
        const text = (item.text || item.value || '').slice(0, 200)
        const score = item.score ? ` <span style="color:var(--fg-muted);font-size:11px">${(item.score * 100).toFixed(1)}%</span>` : ''
        return `<div style="padding:8px 0;border-bottom:0.5px solid var(--border)"><div style="font-size:13px">${text}${item.text && item.text.length > 200 ? '...' : ''}</div>${score}</div>`
      }).join('') + '</div>'
    } catch (e) {
      results.innerHTML = `<p style="color:var(--accent)">Error: ${e.message}</p>`
    }
  }
}
