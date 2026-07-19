// Layout components: topbar, sidebar, composer

const ICON = {
  menu: '<svg class="icon" viewBox="0 0 24 24"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>',
  info: '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  more: '<svg class="icon" viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.5" fill="currentColor"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><circle cx="19" cy="12" r="1.5" fill="currentColor"/></svg>',
  close: '<svg class="icon" viewBox="0 0 24 24"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>',
  plus: '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>',
  search: '<svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
  skills: '<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>',
  clock: '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/></svg>',
  folder: '<svg class="icon" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7l-2-2H5a2 2 0 0 0-2 2z"/></svg>',
  mobile: '<svg class="icon" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18.01"/></svg>',
  leaf: '<svg class="icon" viewBox="0 0 24 24"><path d="M12 2C8 6 6 9 6 13a6 6 0 0 0 12 0c0-4-2-7-6-11z"/></svg>',
  arrowUp: '<svg class="icon" viewBox="0 0 24 24"><path d="M12 4v12m0 0l-4-4m4 4l4-4M5 20h14"/></svg>',
  send: '<svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="18" x2="15" y2="18"/></svg>',
  mic: '<svg class="icon icon--sm" viewBox="0 0 24 24"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 18v3"/></svg>',
  chevDown: '<svg class="icon icon--sm" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>',
  chevUp: '<svg class="icon" viewBox="0 0 24 24"><polyline points="18 15 12 9 6 15"/></svg>'
}

export function renderTopbar(el, { title, onMenu, onMore }) {
  el.innerHTML = `
    <button class="topbar__btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="sidebar" id="btnMenu">${ICON.menu}</button>
    <h1 class="topbar__title">${title}</h1>
    <div class="topbar__actions">
      <button class="topbar__btn" aria-label="Información" id="btnInfo">${ICON.info}</button>
      <button class="topbar__btn" aria-label="Más opciones" id="btnMoreTop">${ICON.more}</button>
    </div>
  `
  el.querySelector('#btnMenu').onclick = onMenu
  el.querySelector('#btnMoreTop').onclick = onMore
}

export function renderSidebar(el, { onClose, onItem }) {
  el.innerHTML = `
    <div class="sidebar__header">
      <div class="sidebar__brand">Claude</div>
      <button class="sidebar__close" aria-label="Cerrar" id="btnCloseSidebar">${ICON.close}</button>
    </div>
    <button class="sidebar__item sidebar__item--highlight" data-label="New task">${ICON.plus}<span class="sidebar__item-label">New task</span></button>
    <button class="sidebar__item" data-label="Search">${ICON.search}<span class="sidebar__item-label">Search</span></button>
    <button class="sidebar__item" data-label="Skills">${ICON.skills}<span class="sidebar__item-label">Skills</span></button>
    <button class="sidebar__item" data-label="Scheduled">${ICON.clock}<span class="sidebar__item-label">Scheduled</span></button>
    <button class="sidebar__item" data-label="Assets">${ICON.folder}<span class="sidebar__item-label">Assets</span></button>
    <button class="sidebar__item" data-label="Connect Mobile">${ICON.mobile}<span class="sidebar__item-label">Connect Mobile</span></button>
    <div class="sidebar__heading">Show more</div>
    <button class="sidebar__item" data-label="MaxHermes">${ICON.leaf}<span class="sidebar__item-label">MaxHermes</span></button>
    <button class="sidebar__item" data-label="MaxClaw">${ICON.leaf}<span class="sidebar__item-label">MaxClaw</span></button>
    <div class="sidebar__heading">Projects</div>
    <button class="sidebar__item" data-label="Add new project">${ICON.folder}<span class="sidebar__item-label">Add new project</span></button>
    <div class="sidebar__footer">
      <div class="sidebar__avatar">M</div>
      <div class="sidebar__user">
        <div class="sidebar__name">Maxbry Odreman</div>
        <div class="sidebar__plan">Plus Plan</div>
      </div>
      <button class="sidebar__user-action" aria-label="Cerrar sesión" id="btnLogout">${ICON.arrowUp}</button>
    </div>
  `
  el.querySelector('#btnCloseSidebar').onclick = onClose
  el.querySelector('#btnLogout').onclick = () => {
    if (confirm('¿Cerrar sesión?')) window.osquestador.showToast('Sesión cerrada')
  }
  el.querySelectorAll('.sidebar__item').forEach(b => {
    b.onclick = () => onItem(b.dataset.label)
  })
}

export function renderComposer(el, { model = 'Sonnet 5 Bajo' }) {
  el.innerHTML = `
    <button class="model-pill">${model}${ICON.chevDown}</button>
    <button class="icon-btn" aria-label="Micrófono">${ICON.mic}</button>
    <button class="icon-btn" aria-label="Enviar" id="composerSend">${ICON.send}</button>
  `
}
