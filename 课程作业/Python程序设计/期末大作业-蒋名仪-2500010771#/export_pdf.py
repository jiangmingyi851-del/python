# -*- coding: utf-8 -*-
"""
用 Edge headless + 本地 HTTP 服务器 将 HTML 幻灯片导出为 16:9 PDF
"""
import subprocess, os, urllib.parse, threading, time
from http.server import HTTPServer, SimpleHTTPRequestHandler

html_file = 'presentation.html'
src_dir = r'C:\Users\32698\笔记与作业\code\python\考试\作业\python程设\期末大作业-蒋名仪'
pdf_path = os.path.join(src_dir, 'presentation.pdf')
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

os.chdir(src_dir)
server = HTTPServer(('127.0.0.1', 0), QuietHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

url = f'http://127.0.0.1:{port}/{html_file}'
print(f'Serving at {url}')
print('Generating PDF...')

time.sleep(1)

import json as _json
# Use CDP to print with custom paper size and background
cdp_script = f'''
const {{ chromium }} = require('playwright');
// fallback: use Edge DevTools Protocol directly
'''

# Edge headless --print-to-pdf doesn't support custom paper size directly
# Use --dump-dom to check if page is rendering, then print with background
cmd = [
    edge,
    '--headless=new',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--no-pdf-header-footer',
    '--virtual-time-budget=10000',
    f'--print-to-pdf={pdf_path}',
    url
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
server.shutdown()

print(f'Return code: {result.returncode}')
if os.path.exists(pdf_path):
    sz = os.path.getsize(pdf_path)
    print(f'PDF saved: {pdf_path}')
    print(f'Size: {sz/1024:.0f} KB ({sz/1024/1024:.1f} MB)')
else:
    print('PDF creation failed')
    if result.stderr:
        print(f'Error: {result.stderr[:500]}')
