// Config view: 5 grupos, toggle iOS, Cerrar sesión coral
const ICON_SLIDER = '<svg class="icon" viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1" fill="currentColor"/><circle cx="4" cy="12" r="1" fill="currentColor"/><circle cx="4" cy="18" r="1" fill="currentColor"/></svg>'
const ICON_GRID = '<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>'
const ICON_FACE = '<svg class="icon" viewBox="0 0 24 24"><path d="M5 8a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8z"/><circle cx="9" cy="10" r="1" fill="currentColor"/><circle cx="15" cy="10" r="1" fill="currentColor"/><line x1="9" y1="15" x2="15" y2="15"/></svg>'
const ICON_MOON = '<svg class="icon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
const ICON_FONT = '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><text x="6" y="18" font-family="serif" font-size="16" fill="currentColor" stroke="none">Aa</text></svg>'
const ICON_VOICE = '<svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/><circle cx="9" cy="6" r="1.5" fill="currentColor"/><circle cx="15" cy="12" r="1.5" fill="currentColor"/></svg>'
const ICON_PHONE = '<svg class="icon" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="2"/><line x1="9" y1="6" x2="9" y2="6.01"/><line x1="15" y1="6" x2="15" y2="6.01"/><line x1="9" y1="10" x2="9" y2="10.01"/><line x1="15" y1="10" x2="15" y2="10.01"/><line x1="9" y1="14" x2="9" y2="14.01"/><line x1="15" y1="14" x2="15" y2="14.01"/><path d="M5 18l-2 3M19 18l2 3"/></svg>'
const ICON_BELL = '<svg class="icon" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>'
const ICON_SHIELD = '<svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>'
const ICON_LINK = '<svg class="icon" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
const ICON_LOGOUT = '<svg class="icon" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'

export function renderConfig(main) {
  main.innerHTML = `
    <div style="margin-top:16px">
      <div class="config-group">
        <div class="config-row">${ICON_SLIDER}<div class="config-row__info"><div class="config-row__label">Capacidades</div><div class="config-row__sub">2 habilitadas</div></div></div>
        <div class="config-row">${ICON_GRID}<div class="config-row__info"><div class="config-row__label">Conectores</div></div></div>
        <div class="config-row">${ICON_FACE}<div class="config-row__info"><div class="config-row__label">Permisos</div></div></div>
      </div>
      <div class="config-group">
        <div class="config-row">${ICON_MOON}<div class="config-row__info"><div class="config-row__label">Modo de color</div><div class="config-row__sub">Sistema</div></div></div>
        <div class="config-row">${ICON_FONT}<div class="config-row__info"><div class="config-row__label">Estilo de fuente</div><div class="config-row__sub">Predeterminado</div></div></div>
        <div class="config-row">${ICON_VOICE}<div class="config-row__info"><div class="config-row__label">Voz</div></div></div>
      </div>
      <div class="config-group">
        <div class="config-row">${ICON_PHONE}<div class="config-row__info"><div class="config-row__label">Retroalimentación háptica</div></div><button class="toggle" id="toggle1" role="switch" aria-checked="true"></button></div>
        <div class="config-row">${ICON_BELL}<div class="config-row__info"><div class="config-row__label">Notificaciones</div></div></div>
        <div class="config-row">${ICON_SHIELD}<div class="config-row__info"><div class="config-row__label">Privacidad</div></div></div>
        <div class="config-row">${ICON_LINK}<div class="config-row__info"><div class="config-row__label">Enlaces compartidos</div></div></div>
      </div>
      <div class="config-group">
        <div class="config-row config-row--danger" id="logoutRow">${ICON_LOGOUT}<div class="config-row__info"><div class="config-row__label">Cerrar sesión</div></div></div>
      </div>
    </div>
  `
}

export function mountConfig(main) {
  const t1 = main.querySelector('#toggle1')
  t1.onclick = () => {
    const off = t1.classList.toggle('toggle--off')
    t1.setAttribute('aria-checked', off ? 'false' : 'true')
  }
  main.querySelector('#logoutRow').onclick = () => {
    if (confirm('¿Cerrar sesión?')) window.osquestador.showToast('Sesión cerrada')
  }
}
