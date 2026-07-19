// Login view
import { api } from '../lib/api.js'

const ICON_USER = '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="10" r="3"/><path d="M6.5 18a7 7 0 0 1 11 0"/></svg>'
const ICON_LOCK = '<svg class="icon" viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'

export function renderLogin(main) {
  main.innerHTML = `
    <div style="max-width:360px;margin:60px auto;padding:0 16px;text-align:center">
      <h1 style="font-family:var(--font-serif);font-size:32px;margin-bottom:8px;font-weight:700">Osquestador</h1>
      <p style="color:var(--fg-muted);margin-bottom:32px">Inicia sesión para continuar</p>
      <form id="loginForm" style="display:flex;flex-direction:column;gap:12px;text-align:left">
        <label style="font-size:13px;color:var(--fg-muted)">Usuario</label>
        <div style="display:flex;align-items:center;gap:8px;background:var(--surface);border:0.5px solid var(--border);border-radius:var(--r-md);padding:12px">
          ${ICON_USER}
          <input id="username" value="max" style="flex:1;background:none;border:none;outline:none;color:var(--fg);font-size:15px" autocomplete="username" />
        </div>
        <label style="font-size:13px;color:var(--fg-muted);margin-top:8px">Contraseña</label>
        <div style="display:flex;align-items:center;gap:8px;background:var(--surface);border:0.5px solid var(--border);border-radius:var(--r-md);padding:12px">
          ${ICON_LOCK}
          <input id="password" type="password" value="max123" style="flex:1;background:none;border:none;outline:none;color:var(--fg);font-size:15px" autocomplete="current-password" />
        </div>
        <button type="submit" class="composer__send" style="width:100%;height:48px;border-radius:var(--r-md);background:var(--accent-coral);color:white;font-weight:600;font-size:15px;margin-top:16px;cursor:pointer;border:none">
          Iniciar sesión
        </button>
        <p id="loginError" style="color:var(--accent);font-size:13px;margin-top:8px;display:none"></p>
      </form>
      <p style="color:var(--fg-muted);font-size:12px;margin-top:32px">Demo: usuario <strong>max</strong> · contraseña <strong>max123</strong></p>
    </div>
  `
}

export async function mountLogin(main) {
  const form = main.querySelector('#loginForm')
  form.onsubmit = async (e) => {
    e.preventDefault()
    const username = main.querySelector('#username').value
    const password = main.querySelector('#password').value
    const errEl = main.querySelector('#loginError')
    errEl.style.display = 'none'
    try {
      const r = await api('/api/auth/login', 'POST', { username, password })
      window.osquestador.showToast('Sesión iniciada')
      window.osquestador.onLoginSuccess?.(r)
    } catch (err) {
      errEl.textContent = err.message || 'Error de autenticación'
      errEl.style.display = 'block'
    }
  }
}
