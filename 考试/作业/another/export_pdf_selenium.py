# -*- coding: utf-8 -*-
"""
用 Selenium + Edge 逐页截图 HTML 幻灯片，合成 16:9 PDF
"""
import os, time, base64, json, threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from PIL import Image
from fpdf import FPDF
from io import BytesIO

src_dir = r'C:\Users\32698\笔记与作业\code\python\考试\作业\python程设\期末大作业-蒋名仪'
html_file = 'presentation.html'
pdf_path = os.path.join(src_dir, 'presentation.pdf')

# Start local HTTP server
os.chdir(src_dir)
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *a): pass
server = HTTPServer(('127.0.0.1', 0), QuietHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
url = f'http://127.0.0.1:{port}/{html_file}'
print(f'Server: {url}')

# Launch Edge headless
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--window-size=1920,1080')
opts.add_argument('--force-device-scale-factor=1')

print('Launching Edge...')
driver = webdriver.Edge(options=opts)
driver.set_window_size(1920, 1080)
driver.get(url)
time.sleep(3)

slide_count = driver.execute_script("return document.querySelectorAll('.slide').length")
print(f'Found {slide_count} slides')

screenshots = []
for i in range(slide_count):
    driver.execute_script(f"""
        if (window.deck) {{
            window.deck.showSlide({i});
        }} else {{
            document.querySelectorAll('.slide').forEach((s, j) => {{
                if (j === {i}) {{
                    s.classList.add('active', 'visible');
                    s.style.visibility = 'visible';
                    s.style.opacity = '1';
                }} else {{
                    s.classList.remove('active', 'visible');
                    s.style.visibility = 'hidden';
                    s.style.opacity = '0';
                }}
            }});
        }}
    """)
    time.sleep(0.5)
    png_data = driver.get_screenshot_as_png()
    screenshots.append(png_data)
    print(f'  Captured slide {i+1}/{slide_count}')

driver.quit()
server.shutdown()

# Combine into PDF (16:9 landscape)
print('Creating PDF...')
W_MM = 338.667  # 1920px at 144 dpi ≈ 338.67mm
H_MM = 190.5    # 1080px at 144 dpi ≈ 190.5mm

pdf = FPDF(orientation='L', unit='mm', format=(H_MM, W_MM))
pdf.set_auto_page_break(False)

for i, png in enumerate(screenshots):
    img = Image.open(BytesIO(png))
    # Save to temp file (fpdf2 needs file path or BytesIO)
    tmp = os.path.join(src_dir, f'_tmp_slide_{i}.png')
    img.save(tmp)
    pdf.add_page()
    pdf.image(tmp, x=0, y=0, w=W_MM, h=H_MM)
    os.remove(tmp)

pdf.output(pdf_path)
sz = os.path.getsize(pdf_path)
print(f'PDF saved: {pdf_path}')
print(f'Size: {sz/1024:.0f} KB ({sz/1024/1024:.1f} MB)')
print(f'Pages: {slide_count}')
