// Dashboard view: greeting + 3 proyectos + status
import { api } from '../lib/api.js'

const ICON_FOLDER = '<svg class="icon" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7l-2-2H5a2 2 0 0 0-2 2z"/></svg>'
const ICON_CODE = '<svg class="icon" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>'

export function renderDashboard(main, { onNavigate, status }) {
  const stats = status || { projects: 4, tasks: 13, artifacts: 5, memory_entries: 5 }
  main.innerHTML = `
    <h2 class="greeting">Hola, <em>Max</em></h2>
    <p class="subtitle">${stats.projects} proyectos · 9 agentes · 3 modos de memoria</p>

    <article class="card" data-go="artifacts">
      <div class="card__icon">${ICON_FOLDER}</div>
      <div class="card__info">
        <div class="card__name">osquestador-auditor</div>
        <div class="card__sub">${stats.artifacts} artefactos · 23 decisiones</div>
      </div>
    </article>

    <article class="card" data-go="plugins">
      <div class="card__icon">${ICON_CODE}</div>
      <div class="card__info">
        <div class="card__name">Plugins & Skills</div>
        <div class="card__sub">13 plugins · 8 skills</div>
      </div>
    </article>

    <article class="card" data-go="tasks">
      <div class="card__icon">${ICON_CODE}</div>
      <div class="card__info">
        <div class="card__name">Tareas activas</div>
        <div class="card__sub">${stats.tasks} tareas en pipeline</div>
      </div>
    </article>

    <article class="card" data-go="chat">
      <div class="card__icon">${ICON_FOLDER}</div>
      <div class="card__info">
        <div class="card__name">Chat con Claude</div>
        <div class="card__sub">Streaming · Sonnet 5 Bajo</div>
      </div>
    </article>
  `
  main.querySelectorAll('[data-go]').forEach(el => {
    el.onclick = () => onNavigate(el.dataset.go, el.querySelector('.card__name').textContent)
  })
}
