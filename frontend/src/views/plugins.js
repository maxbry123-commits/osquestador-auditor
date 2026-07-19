// Plugins view: 13 tiles grid con invoke API
import { api } from '../lib/api.js'

export function renderPlugins(main) {
  main.innerHTML = `
    <h2 class="section-title">13 programas · Click para invocar</h2>
    <div class="plugins-grid" id="pluginsGrid"></div>
  `
}

export async function mountPlugins(main) {
  try {
    const plugins = await api('/api/plugins')
    const grid = main.querySelector('#pluginsGrid')
    grid.innerHTML = Object.entries(plugins).map(([name, p]) => `
      <button class="plugin-tile" data-plugin="${name}">
        <div class="plugin-tile__icon">${name.charAt(0).toUpperCase()}</div>
        <div class="plugin-tile__name">${name}</div>
        <div class="plugin-tile__desc">${p.description}</div>
      </button>
    `).join('')
    grid.querySelectorAll('.plugin-tile').forEach(tile => {
      tile.onclick = async () => {
        const name = tile.dataset.plugin
        // Map plugin to a default safe method
        const defaults = {
          'graphiti': { method: 'search', params: { query: 'osquestador', top_k: 3 } },
          'kanboard': { method: 'list_tasks', params: {} },
          'paddleocr': { method: 'ocr', params: { file_path: '/tmp/sample.png' } },
          'serper': { method: 'search', params: { query: 'osquestador', num: 3 } },
          'claude': { method: '_demo', params: {} },
          'observer': { method: 'get_status', params: {} },
          'watchdog': { method: 'check_openclaw', params: {} },
          'memory': { method: 'get_stats', params: {} },
          'research': { method: 'loop', params: { query: 'osquestador' } },
          'design': { method: 'get_tokens', params: {} },
          'build': { method: 'build', params: {} },
          'audit': { method: 'run', params: {} },
          'dispatch': { method: 'send', params: { channel: 'telegram', message: 'osquestador ok', target: '@maxbry' } }
        }
        const d = defaults[name]
        if (!d) {
          window.osquestador.showToast(`${name}: no default method`)
          return
        }
        try {
          let result
          if (d.method === '_demo') {
            // Direct chat call
            result = await api('/api/chat', 'POST', {
              messages: [{ role: 'user', content: `Describe el plugin ${name}` }],
              model: 'claude-sonnet-4.5',
              project_id: 'osquestador-auditor'
            })
            window.osquestador.showToast(`${name}: ${result.content?.[0]?.text?.slice(0, 50)}...`)
          } else {
            result = await api(`/api/plugins/${name}/${d.method}`, 'POST', d.params)
            window.osquestador.showToast(`${name}.${d.method} OK`)
            console.log(name, result)
          }
        } catch (e) {
          window.osquestador.showToast(`Error ${name}: ${e.message}`)
        }
      }
    })
  } catch (e) {
    main.querySelector('#pluginsGrid').innerHTML = `<p style="color:var(--fg-muted);padding:20px">Backend offline</p>`
  }
}
