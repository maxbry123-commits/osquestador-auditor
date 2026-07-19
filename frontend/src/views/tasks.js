// Kanban view: 4 cols, drag-drop entre columnas
import { api } from '../lib/api.js'

export function renderTasks(main) {
  main.innerHTML = `
    <h2 class="section-title">Pipeline · <span id="taskTotal">—</span> tareas</h2>
    <div class="kanban" id="kanban"></div>
  `
}

export async function mountTasks(main) {
  const cols = [
    { key: 'backlog', label: 'Backlog' },
    { key: 'doing', label: 'Doing' },
    { key: 'review', label: 'Review' },
    { key: 'done', label: 'Done' }
  ]
  try {
    const tasks = await api('/api/tasks')
    main.querySelector('#taskTotal').textContent = tasks.length
    const board = main.querySelector('#kanban')
    board.innerHTML = cols.map(col => {
      const colTasks = tasks.filter(t => t.column === col.key)
      return `
        <div class="kanban-col" data-col="${col.key}">
          <div class="kanban-col__title">${col.label}<span class="kanban-col__count">${colTasks.length}</span></div>
          ${colTasks.map(t => `
            <article class="kanban-card" draggable="true" data-id="${t.id}">
              <div class="kanban-card__title">${t.title}</div>
              <div class="kanban-card__meta"><span>${t.agent || '—'}</span> · <span>${t.priority || 'med'}</span></div>
            </article>
          `).join('')}
        </div>
      `
    }).join('')

    // Drag-drop
    let draggedId = null
    board.querySelectorAll('.kanban-card').forEach(card => {
      card.addEventListener('dragstart', (e) => {
        draggedId = card.dataset.id
        e.dataTransfer.effectAllowed = 'move'
      })
    })
    board.querySelectorAll('.kanban-col').forEach(col => {
      col.addEventListener('dragover', (e) => { e.preventDefault(); e.dataTransfer.dropEffect = 'move' })
      col.addEventListener('drop', async (e) => {
        e.preventDefault()
        if (!draggedId) return
        const targetCol = col.dataset.col
        try {
          await api(`/api/tasks/${draggedId}`, 'PATCH', { column: targetCol })
          window.osquestador.showToast('Tarea movida a ' + targetCol)
          mountTasks(main)  // re-render
        } catch (err) {
          window.osquestador.showToast('Error: ' + err.message)
        }
        draggedId = null
      })
    })
  } catch (e) {
    main.querySelector('#kanban').innerHTML = `<p style="color:var(--fg-muted);padding:20px">Backend offline.</p>`
  }
}
