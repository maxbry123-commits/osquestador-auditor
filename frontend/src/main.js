// Osquestador-Auditor Frontend
// 13 programas integrados. SPA vanilla con Vite.
// API: window.osquestador.*

import { renderSidebar, renderTopbar, renderComposer } from './components/layout.js'
import { renderDashboard } from './views/dashboard.js'
import { renderArtifacts, mountArtifacts } from './views/artifacts.js'
import { renderChat, mountChat } from './views/chat.js'
import { renderTasks, mountTasks } from './views/tasks.js'
import { renderConfig, mountConfig } from './views/config.js'
import { renderPlugins, mountPlugins } from './views/plugins.js'
import { renderMemory, mountMemory } from './views/memory.js'
import { renderLogin, mountLogin } from './views/auth.js'
import { api } from './lib/api.js'

const app = document.getElementById('app')

const state = {
  view: 'dashboard',
  user: { name: 'Maxbry Odreman', plan: 'Plus Plan' },
  status: null
}

async function init() {
  // Check auth first
  let auth = null
  try {
    auth = await api('/api/auth/me')
  } catch (e) { auth = { authenticated: false } }

  if (!auth.authenticated) {
    // Show login screen
    app.innerHTML = `<main class="main" id="main"></main><div class="toast" id="toast"></div>`
    const main = document.getElementById('main')
    renderLogin(main)
    mountLogin(main)
    window.osquestador = {
      showToast: (msg) => showToast(msg),
      onLoginSuccess: () => init()  // re-init after login
    }
    return
  }

  // Topbar + sidebar shell
  app.innerHTML = `
    <header class="topbar" id="topbar"></header>
    <main class="main" id="main"></main>
    <div id="bottombar"></div>
    <aside class="sidebar" id="sidebar"></aside>
    <div class="scrim" id="scrim"></div>
    <div class="toast" id="toast"></div>
  `

  renderTopbar(document.getElementById('topbar'), {
    title: 'Navidad',
    onMenu: openSidebar,
    onMore: () => switchView('config', 'Configuración')
  })
  renderSidebar(document.getElementById('sidebar'), {
    onClose: closeSidebar,
    onItem: (label) => {
      const routes = {
        'New task': ['dashboard', 'Navidad'],
        'Search': ['memory', 'Memoria'],
        'Skills': ['plugins', 'Plugins'],
        'Scheduled': ['tasks', 'Tareas'],
        'Assets': ['artifacts', 'Artefactos'],
        'Connect Mobile': ['config', 'Configuración'],
        'MaxHermes': ['plugins', 'MaxHermes'],
        'MaxClaw': ['plugins', 'MaxClaw'],
        'Add new project': ['config', 'Configuración']
      }
      const r = routes[label] || ['dashboard', 'Navidad']
      switchView(r[0], r[1])
      closeSidebar()
    }
  })

  document.getElementById('scrim').addEventListener('click', closeSidebar)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar()
  })

  // Fetch initial state
  try {
    state.status = await api('/api/observer/status')
  } catch (e) {
    console.warn('backend offline, using cached state', e)
  }

  // Default view
  switchView('dashboard', 'Navidad')

  // Expose global API
  window.osquestador = {
    switchView,
    openSidebar, closeSidebar,
    showToast: (msg) => showToast(msg),
    invoke: (plugin, method, params) => api(`/api/plugins/${plugin}/${method}`, 'POST', params),
    getState: () => state,
    version: '1.1.0',
    plugins: 13,
    user: auth.user
  }
  console.log('%cOsquestador-Auditor v1.1 · 13 plugins · auth OK', 'color:#FF6B6B;font-weight:bold;font-size:14px')
}

function openSidebar() {
  document.getElementById('sidebar').classList.add('open')
  document.getElementById('scrim').classList.add('open')
  document.getElementById('topbar').querySelector('[aria-label="Abrir menú"]')?.setAttribute('aria-expanded', 'true')
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open')
  document.getElementById('scrim').classList.remove('open')
  document.getElementById('topbar').querySelector('[aria-label="Abrir menú"]')?.setAttribute('aria-expanded', 'false')
}

function switchView(viewId, title) {
  state.view = viewId
  document.querySelector('.topbar__title').textContent = title
  const main = document.getElementById('main')
  main.innerHTML = ''
  main.scrollTop = 0
  switch (viewId) {
    case 'dashboard':
      renderDashboard(main, { onNavigate: switchView, status: state.status })
      break
    case 'artifacts':
      renderArtifacts(main)
      mountArtifacts(main)
      break
    case 'chat':
      renderChat(main)
      mountChat(main)
      break
    case 'tasks':
      renderTasks(main)
      mountTasks(main)
      break
    case 'config':
      renderConfig(main)
      mountConfig(main)
      break
    case 'plugins':
      renderPlugins(main)
      mountPlugins(main)
      break
    case 'memory':
      renderMemory(main)
      mountMemory(main)
      break
  }
}

function showToast(msg, duration = 2400) {
  const t = document.getElementById('toast')
  t.textContent = msg
  t.classList.add('show')
  clearTimeout(t._timer)
  t._timer = setTimeout(() => t.classList.remove('show'), duration)
}

init()
