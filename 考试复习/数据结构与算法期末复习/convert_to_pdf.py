"""
将 Markdown cheatsheet 转换为带样式的 HTML，再用 Chrome headless 打印为 PDF。

用法:
    python convert_to_pdf.py                  # 转主文件 数算期末cheetsheet.md
    python convert_to_pdf.py 数算期末cheetsheet补充   # 转指定文件(可带或不带.md)
"""
import markdown
import subprocess
import os
import sys
import tempfile

_DIR = os.path.dirname(__file__)
if len(sys.argv) > 1:
    _base = sys.argv[1][:-3] if sys.argv[1].endswith(".md") else sys.argv[1]
else:
    _base = "数算期末cheetsheet"
INPUT_MD = os.path.join(_DIR, _base + ".md")
OUTPUT_PDF = os.path.join(_DIR, _base + "_new.pdf")

CSS = r"""
@page {
    size: A4;
    margin: 12mm 10mm 12mm 10mm;
}
body {
    font-family: "Microsoft YaHei", "Noto Sans SC", "PingFang SC", sans-serif;
    font-size: 9pt;
    line-height: 1.35;
    color: #1a1a1a;
    max-width: 100%;
    margin: 0 auto;
}
h1 { font-size: 16pt; border-bottom: 2px solid #2563eb; padding-bottom: 4px; margin-top: 0; }
h2 { font-size: 12pt; color: #2563eb; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; margin-top: 14px; margin-bottom: 6px; page-break-after: avoid; }
h3 { font-size: 10pt; margin-top: 8px; margin-bottom: 4px; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 8px 0; }

/* 代码块 */
pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 5px 7px;
    font-size: 7.8pt;
    line-height: 1.3;
    overflow-x: auto;
    margin: 4px 0;
    page-break-inside: avoid;
}
code {
    font-family: "Cascadia Code", "Consolas", "Fira Code", monospace;
    font-size: 7.8pt;
}
p > code, li > code, td > code {
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8pt;
}

/* 表格（包括并列布局的 HTML table 和 Markdown table） */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 6px 0;
    page-break-inside: avoid;
}
/* Markdown 生成的表格 */
table:not([class]) th,
table:not([class]) td {
    border: 1px solid #cbd5e1;
    padding: 3px 6px;
    font-size: 8.5pt;
    vertical-align: top;
}
table:not([class]) th {
    background: #f1f5f9;
    font-weight: 600;
}
/* 并列布局表格（HTML <table> 无 border） */
table tr td {
    vertical-align: top;
    padding: 0 8px;
}
table tr td:first-child {
    padding-left: 0;
}
table tr td:last-child {
    padding-right: 0;
}

/* 并列布局中的代码块更紧凑 */
td pre {
    font-size: 7.5pt;
}

/* 目录表格特殊样式 */
table:first-of-type td {
    border: none;
    padding: 2px 8px;
    font-size: 8.5pt;
}
table:first-of-type a {
    color: #2563eb;
    text-decoration: none;
}

blockquote {
    border-left: 3px solid #2563eb;
    margin: 6px 0;
    padding: 4px 10px;
    background: #f8fafc;
    font-size: 8.5pt;
}
strong { color: #1e40af; }
a { color: #2563eb; text-decoration: none; }
ul, ol { margin: 4px 0; padding-left: 20px; }
li { margin: 1px 0; }
p { margin: 4px 0; }

/* Pygments 代码高亮 */
.codehilite .k, .codehilite .kn, .codehilite .kd { color: #8959a8; font-weight: bold; }
.codehilite .s, .codehilite .s1, .codehilite .s2 { color: #718c00; }
.codehilite .n { color: #4271ae; }
.codehilite .nf { color: #c82829; }
.codehilite .nb { color: #f5871f; }
.codehilite .c, .codehilite .c1, .codehilite .cm { color: #8e908c; font-style: italic; }
.codehilite .mi, .codehilite .mf { color: #f5871f; }
.codehilite .o, .codehilite .ow { color: #3e999f; }
.codehilite .bp { color: #f5871f; }
.codehilite .nn { color: #4271ae; }
"""

def md_to_html(text):
    """Convert markdown text to HTML with code highlighting."""
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "codehilite", "toc"],
        extension_configs={
            "codehilite": {"guess_lang": True, "css_class": "codehilite", "noclasses": False},
        },
    )


import re

def convert_with_tables(md_text):
    """
    Two-pass conversion:
    1. Extract <table>...</table> blocks, process markdown inside each <td> separately
    2. Convert the rest as normal markdown
    3. Reassemble
    """
    table_pattern = re.compile(r'(<table>.*?</table>)', re.DOTALL)
    parts = table_pattern.split(md_text)

    result = []
    for part in parts:
        if part.startswith('<table>'):
            result.append(process_html_table(part))
        else:
            result.append(md_to_html(part))
    return '\n'.join(result)


def process_html_table(table_html):
    """Process a <table> block: convert markdown inside each <td> to HTML."""
    td_pattern = re.compile(r'<td>(.*?)</td>', re.DOTALL)

    def replace_td(match):
        inner_md = match.group(1).strip()
        if not inner_md:
            return '<td></td>'
        inner_html = md_to_html(inner_md)
        return f'<td>\n{inner_html}\n</td>'

    return td_pattern.sub(replace_td, table_html)


def main():
    with open(INPUT_MD, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = convert_with_tables(md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
{CSS}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    html_path = os.path.join(_DIR, _base + ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"HTML written to: {html_path}")

    chrome = None
    for path in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]:
        if os.path.exists(path):
            chrome = path
            break

    if not chrome:
        print("No Chrome/Edge found. Please open the HTML file and print to PDF manually.")
        return

    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(OUTPUT_PDF)
    file_url = "file:///" + abs_html.replace("\\", "/")

    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={abs_pdf}",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        file_url,
    ]
    print(f"Running Chrome headless...")
    result = subprocess.run(cmd, capture_output=True, timeout=120)
    stderr_text = result.stderr.decode('utf-8', errors='replace')
    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 1000:
        size_kb = os.path.getsize(abs_pdf) / 1024
        print(f"PDF generated: {abs_pdf} ({size_kb:.0f} KB)")
    else:
        print(f"Chrome failed: {stderr_text}")
        print("Trying with Edge...")
        edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        if os.path.exists(edge):
            cmd[0] = edge
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 1000:
                size_kb = os.path.getsize(abs_pdf) / 1024
                print(f"PDF generated: {abs_pdf} ({size_kb:.0f} KB)")
            else:
                print(f"Edge also failed: {result.stderr.decode('utf-8', errors='replace')}")

if __name__ == "__main__":
    main()
