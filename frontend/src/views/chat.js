// Chat view: streaming via /api/chat?stream=true OR WebSocket /ws/{project_id}
import { api, stream } from '../lib/api.js'

const ICON_SEND = '<svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="18" x2="15" y2="18"/></svg>'
const ICON_MIC = '<svg class="icon icon--sm" viewBox="0 0 24 24"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 18v3"/></svg>'
const ICON_PAPER = '<svg class="icon icon--sm" viewBox="0 0 24 24"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>'

export function renderChat(main) {
  main.innerHTML = `
    <div class="chat">
      <div class="chat__messages" id="chatMessages">
        <div class="message message--system">Sesion iniciada · Claude Sonnet 5 · WS o SSE streaming</div>
      </div>
      <div class="composer">
        <form class="composer__form" id="chatForm">
          <textarea class="composer__input" id="chatInput" rows="1" placeholder="Preguntale a Claude..." aria-label="Mensaje"></textarea>
          <button type="button" class="icon-btn" aria-label="Adjuntar" id="attachBtn">${ICON_PAPER}</button>
          <button type="button" class="icon-btn" aria-label="Microfono">${ICON_MIC}</button>
          <button type="submit" class="composer__send" aria-label="Enviar" id="sendBtn">${ICON_SEND}</button>
        </form>
      </div>
    </div>
  `
}

export function mountChat(main) {
  const form = main.querySelector('#chatForm')
  const input = main.querySelector('#chatInput')
  const msgs = main.querySelector('#chatMessages')
  const sendBtn = main.querySelector('#sendBtn')
  const PROJECT = 'osquestador-auditor'
  const WS_URL = (location.protocol === 'https:' ? 'wss' : 'ws') + '://' + location.host + '/ws/' + PROJECT

  let ws = null
  let wsReady = false
  try {
    ws = new WebSocket(WS_URL)
    ws.onopen = () => { wsReady = true; console.log('WS connected') }
    ws.onmessage = (ev) => {
      const d = JSON.parse(ev.data)
      if (d.type === 'message') {
        const sel = '[data-ts="' + d.ts + '"]'
        let el = msgs.querySelector(sel)
        if (!el) {
          el = document.createElement('div')
          el.className = 'message message--' + d.role
          el.dataset.ts = d.ts
          el.textContent = d.content
          msgs.appendChild(el)
        } else {
          el.textContent = d.content
        }
        msgs.scrollTop = msgs.scrollHeight
      }
    }
    ws.onclose = () => { wsReady = false; console.log('WS closed') }
    ws.onerror = () => { wsReady = false; console.warn('WS error') }
  } catch (e) {
    console.warn('WS init failed:', e)
  }

  input.addEventListener('input', () => {
    input.style.height = 'auto'
    input.style.height = Math.min(input.scrollHeight, 120) + 'px'
  })

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      form.dispatchEvent(new Event('submit'))
    }
  })

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const text = input.value.trim()
    if (!text) return
    input.value = ''
    input.style.height = 'auto'
    sendBtn.disabled = true

    // Show user message immediately
    const userMsg = document.createElement('div')
    userMsg.className = 'message message--user'
    userMsg.dataset.ts = Date.now() / 1000
    userMsg.textContent = text
    msgs.appendChild(userMsg)
    msgs.scrollTop = msgs.scrollHeight

    if (wsReady) {
      // WS path: response comes via ws.onmessage
      ws.send(JSON.stringify({ content: text, project_id: PROJECT }))
      setTimeout(() => { sendBtn.disabled = false }, 400)
      return
    }

    // SSE fallback
    const assistantMsg = document.createElement('div')
    assistantMsg.className = 'message message--assistant'
    assistantMsg.textContent = ''
    msgs.appendChild(assistantMsg)

    try {
      await stream('/api/chat?stream=true', {
        messages: [{ role: 'user', content: text }],
        model: 'claude-sonnet-4.5',
        project_id: PROJECT,
        stream: true
      }, (chunk) => {
        if (chunk.type === 'content_block_delta' && chunk.delta && chunk.delta.type === 'text_delta' && chunk.delta.text) {
          assistantMsg.textContent += chunk.delta.text
          msgs.scrollTop = msgs.scrollHeight
        }
      })
    } catch (err) {
      try {
        const r = await api('/api/chat', 'POST', {
          messages: [{ role: 'user', content: text }],
          model: 'claude-sonnet-4.5',
          project_id: PROJECT
        })
        assistantMsg.textContent = (r.content && r.content[0] && r.content[0].text) || 'Error'
      } catch (e2) {
        assistantMsg.textContent = 'Error: ' + e2.message
      }
    } finally {
      sendBtn.disabled = false
      msgs.scrollTop = msgs.scrollHeight
    }
  })
}
