"""Convert Markdown files to PDF locally.

Usage:
    python md2pdf.py <file-or-directory> [more files...] [-o OUTPUT_DIR]

Examples:
    python md2pdf.py ../pre-work/04-session-4-reference.md
    python md2pdf.py ../pre-work -o ../pdf

Requires: pip install markdown pygments
Rendering: Microsoft Edge or Chrome in headless mode (already on Windows).
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Run: pip install markdown pygments")

CSS = """
@page { margin: 18mm 15mm; }
* { box-sizing: border-box; }
body {
    font-family: "Segoe UI", -apple-system, Arial, sans-serif;
    font-size: 11pt; line-height: 1.55; color: #1f2328;
    max-width: 100%; margin: 0;
}
h1 { font-size: 20pt; border-bottom: 2px solid #d1d9e0; padding-bottom: 6px; }
h2 { font-size: 15pt; border-bottom: 1px solid #d1d9e0; padding-bottom: 4px; margin-top: 28px; }
h3 { font-size: 12.5pt; margin-top: 22px; }
h2, h3, h4 { page-break-after: avoid; }
a { color: #0969da; text-decoration: none; }
blockquote {
    margin: 12px 0; padding: 8px 14px; color: #59636e;
    border-left: 4px solid #d1d9e0; background: #f6f8fa;
}
code {
    font-family: "Cascadia Mono", Consolas, monospace; font-size: 9.5pt;
    background: #f0f2f4; padding: 1px 4px; border-radius: 4px;
}
pre {
    background: #f6f8fa; border: 1px solid #d1d9e0; border-radius: 6px;
    padding: 12px; overflow-x: auto; page-break-inside: avoid;
    white-space: pre-wrap; word-wrap: break-word;
}
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; page-break-inside: avoid; }
th, td { border: 1px solid #d1d9e0; padding: 6px 10px; text-align: left; font-size: 10pt; }
th { background: #f6f8fa; }
tr:nth-child(even) { background: #fafbfc; }
hr { border: none; border-top: 1px solid #d1d9e0; margin: 24px 0; }
img { max-width: 100%; }
.codehilite .k, .codehilite .kd { color: #cf222e; }
.codehilite .s, .codehilite .s2 { color: #0a3069; }
.codehilite .c, .codehilite .c1, .codehilite .cm { color: #59636e; font-style: italic; }
.codehilite .nc, .codehilite .nf { color: #6639ba; }
.codehilite .mi, .codehilite .mf { color: #0550ae; }
"""

BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "msedge", "chrome", "chromium", "google-chrome",
]


def find_browser() -> str:
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    sys.exit("No Edge or Chrome found. Install one or add it to PATH.")


def md_to_html(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "codehilite", "toc", "sane_lists"],
        extension_configs={"codehilite": {"guess_lang": False, "noclasses": False}},
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{md_path.stem}</title><style>{CSS}</style></head>"
        f"<body>{body}</body></html>"
    )


def convert(md_path: Path, out_dir: Path, browser: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / (md_path.stem + ".pdf")
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / (md_path.stem + ".html")
        html_path.write_text(md_to_html(md_path), encoding="utf-8")
        result = subprocess.run(
            [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
    if not pdf_path.is_file():
        sys.exit(f"PDF generation failed for {md_path.name}:\n{result.stderr}")
    return pdf_path


def collect_inputs(raw_paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in raw_paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(p.glob("*.md")))
        elif p.is_file() and p.suffix.lower() == ".md":
            files.append(p)
        else:
            sys.exit(f"Not a Markdown file or directory: {raw}")
    if not files:
        sys.exit("No .md files found.")
    return files






def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF locally.")
    parser.add_argument("inputs", nargs="+", help=".md files and/or directories")
    parser.add_argument("-o", "--output", default="pdf", help="output directory (default: ./pdf)")
    args = parser.parse_args()

    browser = find_browser()
    out_dir = Path(args.output)
    for md_file in collect_inputs(args.inputs):
        pdf = convert(md_file, out_dir, browser)
        print(f"OK  {md_file.name} -> {pdf}")


if __name__ == "__main__":
    main()


