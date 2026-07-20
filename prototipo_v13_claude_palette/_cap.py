from playwright.sync_api import sync_playwright
import os
abs_path = '/workspace/osquestador-auditor/prototipo_v13_claude_palette/index.html'
out = '/workspace/osquestador-auditor/prototipo_v13_claude_palette/screenshots'
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/root/.cache/ms-playwright/chromium-1223/chrome-linux/chrome')
    ctx = b.new_context(viewport={'width': 1100, 'height': 900})
    page = ctx.new_page()
    page.goto('file://' + abs_path)
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_timeout(500)
    page.screenshot(path=f'{out}/V13_full.png', full_page=True)
    # Capture each section
    sections = page.locator('.section').all()
    for i, sec in enumerate(sections):
        try:
            sec.screenshot(path=f'{out}/V13_modelo_{i}.png')
            print(f'OK modelo {i}', flush=True)
        except Exception as e:
            print(f'fail {i}: {e}', flush=True)
    ctx.close()
    # Mobile
    ctx2 = b.new_context(viewport={'width': 390, 'height': 844})
    page2 = ctx2.new_page()
    page2.goto('file://' + abs_path)
    page2.wait_for_load_state('domcontentloaded')
    page2.wait_for_timeout(500)
    page2.screenshot(path=f'{out}/V13_mobile.png', full_page=True)
    ctx2.close()
    b.close()
print('DONE')
