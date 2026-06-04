// export-slides-pdf.mjs
// 用 Playwright 将 HTML 幻灯片逐页截图并合成 PDF
// 用法: node export-slides-pdf.mjs <input.html> [output.pdf]
import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, existsSync } from 'fs';
import { resolve, dirname, extname, basename } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const inputFile = process.argv[2];
if (!inputFile) { console.error('Usage: node export-slides-pdf.mjs <input.html> [output.pdf]'); process.exit(1); }
const htmlPath = resolve(inputFile);
const outputPdf = process.argv[3] ? resolve(process.argv[3]) : htmlPath.replace(/\.html$/i, '.pdf');
const baseDir = dirname(htmlPath);

// Simple static file server
const mimeTypes = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

const server = createServer((req, res) => {
    let filePath = resolve(baseDir, '.' + decodeURIComponent(req.url.split('?')[0]));
    if (!existsSync(filePath)) { res.writeHead(404); res.end(); return; }
    const ext = extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
    res.end(readFileSync(filePath));
});

server.listen(0, '127.0.0.1', async () => {
    const port = server.address().port;
    const url = `http://127.0.0.1:${port}/${basename(htmlPath)}`;
    console.log(`Serving at ${url}`);

    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait for fonts & KaTeX to render
    await page.waitForTimeout(2000);

    // Get total slide count
    const slideCount = await page.evaluate(() => document.querySelectorAll('.slide').length);
    console.log(`Found ${slideCount} slides`);

    // Collect screenshots as buffers
    const screenshots = [];
    for (let i = 0; i < slideCount; i++) {
        // Navigate to slide
        await page.evaluate((idx) => {
            if (window.deck) {
                window.deck.showSlide(idx);
            } else {
                const slides = document.querySelectorAll('.slide');
                slides.forEach((s, j) => {
                    s.classList.toggle('active', j === idx);
                    s.classList.toggle('visible', j === idx);
                });
            }
        }, i);
        await page.waitForTimeout(600);

        const buf = await page.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
        screenshots.push(buf);
        console.log(`  Captured slide ${i + 1}/${slideCount}`);
    }

    // Create PDF using a new page with images
    const pdfPage = await browser.newPage();
    const imgTags = screenshots.map(buf => {
        const b64 = buf.toString('base64');
        return `<div style="page-break-after:always;margin:0;padding:0;"><img src="data:image/png;base64,${b64}" style="width:100%;height:auto;display:block;"></div>`;
    }).join('\n');

    await pdfPage.setContent(`
        <html><head><style>
            @page { size: 1920px 1080px; margin: 0; }
            body { margin: 0; padding: 0; }
            div:last-child { page-break-after: auto; }
        </style></head><body>${imgTags}</body></html>
    `, { waitUntil: 'load' });

    await pdfPage.pdf({
        path: outputPdf,
        width: '1920px',
        height: '1080px',
        margin: { top: 0, right: 0, bottom: 0, left: 0 },
        printBackground: true,
    });

    console.log(`PDF saved: ${outputPdf}`);
    await browser.close();
    server.close();
});
