from playwright.sync_api import sync_playwright
import os
abs_path = '/workspace/osquestador-auditor/prototipo_v14_panel_claude_palette/index.html'
out = '/workspace/osquestador-auditor/prototipo_v14_panel_claude_palette/screenshots'
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/root/.cache/ms-playwright/chromium-1223/chrome-linux/chrome')
    ctx = b.new_context(viewport={'width': 1280, 'height': 800})
    page = ctx.new_page()
    page.goto('file://' + abs_path)
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_timeout(500)
    page.screenshot(path=f'{out}/V14_dashboard.png', full_page=False)
    # Open bandeja
    page.locator('.sidebar__new').click()
    page.wait_for_timeout(300)
    page.screenshot(path=f'{out}/V14_bandeja.png', full_page=False)
    page.locator('#scrim-bandeja').click()
    page.wait_for_timeout(200)
    # Chat
    page.evaluate('showView("chat")')
    page.fill('#chat-input', '/memory status del orquestador')
    page.wait_for_timeout(200)
    page.screenshot(path=f'{out}/V14_chat.png', full_page=False)
    # API
    page.evaluate('showView("api")')
    page.wait_for_timeout(200)
    page.screenshot(path=f'{out}/V14_api.png', full_page=False)
    # Artefactos
    page.evaluate('showView("artifacts")')
    page.wait_for_timeout(200)
    page.screenshot(path=f'{out}/V14_artifacts.png', full_page=False)
    ctx.close()
    # Mobile
    ctx2 = b.new_context(viewport={'width': 390, 'height': 844})
    page2 = ctx2.new_page()
    page2.goto('file://' + abs_path)
    page2.wait_for_load_state('domcontentloaded')
    page2.wait_for_timeout(500)
    page2.screenshot(path=f'{out}/V14_mobile_dashboard.png', full_page=False)
    page2.locator('.header__menu').click()
    page2.wait_for_timeout(400)
    page2.screenshot(path=f'{out}/V14_mobile_drawer.png', full_page=False)
    ctx2.close()
    b.close()
print('DONE 7 screenshots')
