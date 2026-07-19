// Artefactos view: 5 cards con chip + download
import { api } from '../lib/api.js'

const ICON_DOC = '<svg class="icon icon--lg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="13" y2="17"/></svg>'
const ICON_CODE = '<svg class="icon icon--lg" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="14" y1="4" x2="10" y2="20"/></svg>'
const ICON_DOWN = '<svg class="icon" viewBox="0 0 24 24"><path d="M12 4v12m0 0l-4-4m4 4l4-4M5 20h14"/></svg>'
const ICON_UP = '<svg class="icon" viewBox="0 0 24 24"><polyline points="18 15 12 9 6 15"/></svg>'
const ICON_FOLDER = '<svg class="icon icon--sm" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7l-2-2H5a2 2 0 0 0-2 2z"/></svg>'

export function renderArtifacts(main) {
  main.innerHTML = `
    <div class="artifact-count">${ICON_FOLDER} <span id="countNum">—</span> artefactos</div>
    <div id="artifactsList"></div>
    <button class="fab" id="scrollTop" aria-label="Ir arriba">${ICON_UP}</button>
  `
  document.getElementById('scrollTop').onclick = () => main.scrollTo({ top: 0, behavior: 'smooth' })
}

export async function mountArtifacts(main) {
  const list = main.querySelector('#artifactsList')
  const count = main.querySelector('#countNum')
  try {
    const items = await api('/api/artifacts')
    count.textContent = items.length
    list.innerHTML = items.map(a => {
      const isCode = a.type === 'py' || a.type === 'json' || a.type === 'html' || a.type === 'css' || a.type === 'jsx'
      const icon = isCode ? ICON_CODE : ICON_DOC
      const meta = a.meta ? (typeof a.meta === 'string' ? JSON.parse(a.meta) : a.meta) : {}
      const desc = meta.desc || (a.type === 'md' ? 'Documento' : 'Código')
      return `
        <article class="artifact-card">
          <div class="artifact-card__chip">${icon}</div>
          <div class="artifact-card__info">
            <div class="artifact-card__name">${a.name}</div>
            <div class="artifact-card__meta">${desc} · ${(a.type || '').toUpperCase()}</div>
          </div>
          <button class="artifact-card__download" data-id="${a.id}" aria-label="Descargar ${a.name}">${ICON_DOWN}</button>
        </article>
      `
    }).join('')
    list.querySelectorAll('.artifact-card__download').forEach(btn => {
      btn.onclick = async () => {
        try {
          const a = await api('/api/artifacts/' + btn.dataset.id)
          const blob = new Blob([a.content], { type: 'text/plain' })
          const url = URL.createObjectURL(blob)
          const x = document.createElement('a')
          x.href = url
          x.download = a.name
          x.click()
          URL.revokeObjectURL(url)
          window.osquestador.showToast('Descargado: ' + a.name)
        } catch (e) {
          window.osquestador.showToast('Error: ' + e.message)
        }
      }
    })
  } catch (e) {
    list.innerHTML = `<p style="color:var(--fg-muted);padding:20px">Backend offline. <button onclick="location.reload()" style="color:var(--blue)">Reintentar</button></p>`
  }
}
