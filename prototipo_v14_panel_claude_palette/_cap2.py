from playwright.sync_api import sync_playwright
import os
abs_path = '/workspace/osquestador-auditor/prototipo_v14_panel_claude_palette/index.html'
out = '/workspace/osquestador-auditor/prototipo_v14_panel_claude_palette/screenshots'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/root/.cache/ms-playwright/chromium-1223/chrome-linux/chrome')
    ctx = b.new_context(viewport={'width': 1280, 'height': 800})
    page = ctx.new_page()
    page.goto('file://' + abs_path)
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_timeout(500)
    page.evaluate('showView("chat")')
    page.wait_for_timeout(200)
    page.fill('#chat-input', '/memory status del orquestador')
    page.wait_for_timeout(200)
    page.screenshot(path=f'{out}/V14_chat_real.png', full_page=False)
    page.evaluate('showView("api")')
    page.wait_for_timeout(200)
    page.screenshot(path=f'{out}/V14_api_real.png', full_page=False)
    page.evaluate('showView("artifacts")')
    page.wait_for_timeout(200)
    page.screenshot(path=f'{out}/V14_artifacts_real.png', full_page=False)
    b.close()
print('OK')
