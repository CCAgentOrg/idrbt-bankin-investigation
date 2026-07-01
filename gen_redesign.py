#!/usr/bin/env python3
"""Redesign site in Research Report style.
Reads content from existing files; wraps in new template.
Output: site/redesign/index.html + site/redesign/cookie-tracking.html + site/redesign/shutdown-critique.html
"""

import re, json, os, html

SITE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/site"
OUT_DIR = SITE_DIR + "/redesign"

def read_file(path):
    with open(path) as f:
        return f.read()

def extract_body_content(html_str):
    """Extract everything between <body> and </body>, stripping the body tags."""
    m = re.search(r'<body>(.*?)</body>', html_str, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_title(html_str):
    m = re.search(r'<title>(.*?)</title>', html_str)
    return m.group(1) if m else ""

def extract_meta_description(html_str):
    m = re.search(r'name="description"\s*content="([^"]*)"', html_str)
    return m.group(1) if m else ""

def extract_tag_from_hero(body):
    """Extract the tag text from hero div"""
    m = re.search(r'<div class="tag"[^>]*>([^<]+)</div>', body)
    return m.group(1) if m else "Investigation"

def extract_h1(body):
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', body)
    return m.group(1) if m else ""

def extract_sections(body):
    """Extract all <section> blocks with their content."""
    sections = re.findall(r'<section>(.*?)</section>', body, re.DOTALL)
    return sections

def extract_toc_items(sections, html_str):
    """Generate TOC items from h2 headings in sections + page title"""
    items = []
    for i, sec in enumerate(sections):
        # Get h2 text
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', sec)
        if hm:
            txt = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
            num = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
            # Check for section-number pattern
            n = re.match(r'(?:<span[^>]*>)?([\d]+[\.\d]*)(?:\s|</span>\s*)?(.*)', txt)
            items.append((num, f"section-{i}"))
    return items

def make_index_sections(body, translations):
    """Rebuild index sections preserving data-i18n attributes."""
    sections_html = ""
    current_tag = re.search(r'<div class="tag" data-i18n="([^"]+)">', body)
    tag_key = current_tag.group(1) if current_tag else "tag"
    
    # Extract all sections
    sections = extract_sections(body)
    
    # Build TOC
    toc = [
        ("Executive Summary", "section-0"),
    ]
    
    for i, sec in enumerate(sections):
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', sec)
        if hm:
            label = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
            toc.append((label, f"section-{i}"))
    
    # Build section content preserving data-i18n
    for i, sec in enumerate(sections):
        # Clean up section padding classes
        sec = re.sub(r'padding:\d+px 0', '', sec)
        sections_html += f'<section id="section-{i}">\n{sec.strip()}\n</section>\n\n'
    
    return sections_html, toc

# ── Template ──

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{TITLE}}</title>
<meta name="description" content="{{DESCRIPTION}}" />
<style>
/* ── Reset ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}

/* ── Language bar ── */
.lang-bar{background:#fff;border-bottom:1px solid #e0ddd8;padding:8px 0;text-align:center;position:sticky;top:0;z-index:100}
.lang-bar .inner{max-width:1020px;margin:0 auto;padding:0 16px}
.lang-bar strong{font-size:.72rem;color:#999;margin-right:8px}
.lang-btn{font-size:.7rem;border:1px solid #ddd;background:#fff;color:#888;padding:2px 9px;border-radius:3px;cursor:pointer;margin:2px}
.lang-btn:hover{border-color:#c00;color:#c00}
.lang-active{background:#c00;color:#fff;border-color:#c00;font-weight:600}
.trans-banner{background:#fff3cd;border-bottom:1px solid #ffc107;text-align:center;font-size:.72rem;padding:4px 16px;color:#856404;display:none}

/* ── Base ── */
body{background:#faf8f6;color:#222;font:14.5px/1.7 -apple-system,"Helvetica Neue",Arial,sans-serif;display:flex;min-height:100vh}
a{color:#c00;text-decoration:none}
a:hover{text-decoration:underline}
tt,code,pre{font-family:Menlo,Consolas,monospace;font-size:.82em}

/* ── Sidebar TOC ── */
.toc{position:fixed;top:44px;left:0;width:220px;height:calc(100vh - 44px);overflow-y:auto;background:#fff;border-right:1px solid #e8e4e0;padding:24px 16px;flex-shrink:0;z-index:50}
.toc .label{font:.62rem/1;text-transform:uppercase;letter-spacing:.1em;color:#b0a8a0;margin-bottom:18px;font-weight:600}
.toc a{display:block;font:.76rem/1.5;color:#666;padding:5px 0;text-decoration:none;border-bottom:1px solid transparent;transition:.1s}
.toc a:hover{color:#c00;text-decoration:none}
.toc a.active{color:#222;font-weight:600}
.toc .sub{padding-left:14px;font-size:.72rem;color:#999}
.toc .spacer{height:12px}
.toc .nav-back{display:block;font:.7rem;margin-top:8px;padding:6px 0;color:#999;border-top:1px solid #eee}
.toc .nav-back:hover{color:#c00}

/* ── Main ── */
.main{flex:1;margin-left:220px;max-width:740px;padding:28px 44px 60px}

/* ── Report Header ── */
.report-header{margin-bottom:32px;padding-bottom:24px;border-bottom:2px solid #222}
.report-header .ref{font:.68rem/1;color:#b0a8a0;text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px}
.report-header .ref em{font-style:normal;background:#222;color:#fff;padding:2px 8px;border-radius:2px;font-size:.62rem;letter-spacing:.05em;margin-right:5px}
.report-header h1{font:1.5rem/1.3 -apple-system,sans-serif;font-weight:700;letter-spacing:-.01em;margin-bottom:10px}
.report-header .meta{font:.78rem/1.5;color:#999;display:flex;gap:18px;flex-wrap:wrap}
.report-header .meta dt{font-weight:600;color:#666;display:inline}
.report-header .meta dd{display:inline;margin-right:14px}

/* ── Sections ── */
section{margin-bottom:28px}
section p{margin-bottom:12px;color:#333;font-size:.9rem;line-height:1.75}
section p strong{color:#c00}
h2{font:1.1rem/1.3;font-weight:700;margin:28px 0 10px;padding-bottom:5px;border-bottom:1px solid #e0ddd8;color:#222}
h2 .section-num{color:#c00;margin-right:5px}
h3{font:.92rem/1.3;font-weight:600;margin:18px 0 7px;color:#333}

/* ── Evidence callout ── */
.evidence{background:#f8f6f4;border:1px solid #e0ddd8;border-left:3px solid #c00;padding:12px 16px;margin:14px 0;border-radius:0 4px 4px 0;font-size:.86rem;color:#555}

/* ── Callout (aliased to evidence style for backward compat) ── */
.callout{background:#f8f6f4;border:1px solid #e0ddd8;border-left:3px solid #c00;padding:12px 16px;margin:14px 0;border-radius:0 4px 4px 0;font-size:.86rem;color:#555}
.callout-green{border-left-color:#080}
.callout-grey{border-left-color:#888}
.callout-amber{background:#fff8e1;border-left-color:#f0c000;color:#6d5200}

/* ── Finding cards ── */
.finding{background:#fff;border:1px solid #e0ddd8;border-radius:4px;padding:14px 16px;margin:12px 0}
.finding .finding-title{font:.78rem/1.3;font-weight:600;color:#c00;margin-bottom:4px;font-size:.68rem;text-transform:uppercase;letter-spacing:.04em}
.finding .finding-text{font:.86rem/1.5;color:#444}
.finding .finding-ref{font:.7rem/1;color:#bbb;margin-top:6px}

/* ── Kingsly block ── */
.kingsly-block{background:#fff;border:1px solid #e0ddd8;border-radius:6px;padding:18px;margin:16px 0;font-size:.86rem}
.kingsly-block .tweet{color:#333;font-size:.9rem;margin-bottom:8px}
.kingsly-block .attribution{color:#999;font-size:.78rem}
.kingsly-block .cookies{margin:10px 0;padding:10px 14px;background:#f5f4f2;border-radius:3px;font-family:Menlo,Consolas,monospace;font-size:.78rem;color:#555}

/* ── Diagram box ── */
.diagram-box{background:#fff;border:1px solid #e0ddd8;border-radius:6px;padding:18px;margin:14px 0;font-size:.82rem;overflow-x:auto}
.diagram-box pre{font-family:Menlo,Consolas,monospace;font-size:.76rem;line-height:1.6;color:#555}

/* ── Tables ── */
.data-table{width:100%;border-collapse:collapse;font:.8rem/1.4;margin:14px 0}
.data-table th{text-align:left;padding:6px 10px;border-bottom:1px solid #222;color:#222;font-weight:600;font-size:.68rem;text-transform:uppercase;letter-spacing:.04em}
.data-table td{padding:6px 10px;border-bottom:1px solid #eee;color:#444}
.data-table .num{text-align:right;font-variant-numeric:tabular-nums}
.data-table tr.yes td{color:#080}
.data-table tr.no td{color:#c00}

/* ── Download strip ── */
.dl-strip{display:flex;flex-wrap:wrap;gap:10px;padding:12px 0}
.dl-strip a{font:.82rem;background:#fff;border:1px solid #ddd;border-radius:4px;padding:8px 16px;color:#444;display:inline-flex;align-items:center;gap:5px;transition:.15s}
.dl-strip a:hover{border-color:#c00;text-decoration:none}
.dl-primary{background:#c00!important;color:#fff!important;border-color:#c00!important;font-weight:600}

/* ── Nav links ── */
.nav-links{display:flex;flex-wrap:wrap;gap:16px;margin:24px 0;padding:16px 0;border-top:1px solid #e0ddd8;border-bottom:1px solid #e0ddd8}
.nav-links a{font:.82rem;color:#666}
.nav-links a:hover{color:#c00;text-decoration:none}

/* ── About / Footer ── */
.about-box{background:#fff;border:1px solid #e0ddd8;border-radius:5px;padding:18px;margin:20px 0;font-size:.84rem}
.about-box h3{font:.9rem;font-weight:600;margin-bottom:4px;color:#222}
.about-box p{color:#666;margin-bottom:5px;font-size:.84rem}
.about-box .ref{color:#aaa;font-size:.78rem}
.report-footer{margin-top:32px;padding-top:16px;border-top:1px solid #e0ddd8;font:.75rem/1.4;color:#bbb;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
.report-footer a{color:#888}

/* ── Images ── */
.compare-img{width:100%;max-width:680px;height:auto;border-radius:4px;border:1px solid #e0ddd8;margin:12px 0}
.compare-caption{font:.75rem;color:#999;text-align:center;margin-top:4px;margin-bottom:14px}

/* ── Responsive ── */
@media(max-width:900px){
  .toc{display:none}
  .main{margin-left:0;max-width:100%;padding:20px 16px}
}
</style>
</head>
<body>

<!-- Language bar -->
<div class="lang-bar"><div class="inner">
<strong>Language:</strong>
<button class="lang-btn lang-active" id="lang-en" onclick="setLang('en')">English</button>
<button class="lang-btn" id="lang-hi" onclick="setLang('hi')">हिन्दी</button>
<button class="lang-btn" id="lang-ta" onclick="setLang('ta')">தமிழ்</button>
<button class="lang-btn" id="lang-bn" onclick="setLang('bn')">বাংলা</button>
<button class="lang-btn" id="lang-mr" onclick="setLang('mr')">मराठी</button>
<button class="lang-btn" id="lang-te" onclick="setLang('te')">తెలుగు</button>
<button class="lang-btn" id="lang-gu" onclick="setLang('gu')">ગુજરાતી</button>
<button class="lang-btn" id="lang-ur" onclick="setLang('ur')">اردو</button>
<button class="lang-btn" id="lang-kn" onclick="setLang('kn')">ಕನ್ನಡ</button>
<button class="lang-btn" id="lang-ml" onclick="setLang('ml')">മലയാളം</button>
</div></div>
<div class="trans-banner" id="trans-banner">⚠️ AI-generated translation. English original is authoritative.</div>

<!-- Sidebar TOC -->
<nav class="toc">
<div class="label">Contents</div>
{{TOC_LINKS}}
<div class="spacer"></div>
{{NAV_LINKS}}
</nav>

<!-- Main -->
<div class="main">

<div class="report-header">
<div class="ref"><em>{{TAG}}</em> · IDRBT .bank.in Portal</div>
<h1>{{H1}}</h1>
<div class="meta">
<dl><dt>Researcher: </dt><dd>CashlessConsumer</dd></dl>
<dl><dt>Published: </dt><dd>{{DATE}}</dd></dl>
</div>
</div>

{{SECTIONS}}

<!-- Nav links -->
<div class="nav-links">
{{PAGE_LINKS}}
</div>

<!-- About -->
<div class="about-box">
<h3>CashlessConsumer</h3>
<p>A consumer collective that tracks the digital payments industry in India, producing awareness resources, technical analysis, open data, and policy inputs toward a fair cashless society.</p>
<div class="ref"><a href="https://cashlessconsumer.in">cashlessconsumer.in · GitHub</a></div>
</div>

</div>

<footer class="report-footer">
<span>© July 2026 · CashlessConsumer</span>
<a href="https://github.com/CCAgentOrg/idrbt-bankin-investigation">Source on GitHub</a>
</footer>

{{TRANSLATION_SCRIPT}}

</body>
</html>
"""

def make_toc_links(toc_items):
    links = ""
    for label, anchor in toc_items:
        links += f'<a href="#{anchor}">{label}</a>\n'
    return links

def make_page_links(current):
    """Links to other pages in the site."""
    all_pages = {
        "index": {"label": "🔐 Main Investigation", "path": "./"},
        "cookie-tracking": {"label": "🍪 Cookie Tracking", "path": "./cookie-tracking.html"},
        "shutdown-critique": {"label": "🔴 Shutdown Critique", "path": "./shutdown-critique.html"},
    }
    links = ""
    for key, info in all_pages.items():
        if key != current:
            links += f'<a href="{info["path"]}">{info["label"]}</a>\n'
    return links

def make_nav_sidebar_links(current):
    """Sidebar nav links between pages."""
    all_pages = {
        "index": {"label": "← Back to main investigation", "path": "./", "cls": "nav-back"},
        "cookie-tracking": {"label": "🍪 Cookie Analysis", "path": "./cookie-tracking.html", "cls": "nav-back"},
        "shutdown-critique": {"label": "🔴 Shutdown Critique", "path": "./shutdown-critique.html", "cls": "nav-back"},
    }
    links = ""
    for key, info in all_pages.items():
        if key != current:
            links += f'<a href="{info["path"]}" class="{info["cls"]}">{info["label"]}</a>\n'
    return links

def process_index():
    html = read_file(f"{SITE_DIR}/index.html")
    body = extract_body_content(html)
    title = extract_title(html)
    desc = extract_meta_description(html)
    tag = extract_tag_from_hero(body)
    h1 = extract_h1(body)
    
    # Extract the TR object as-is
    tr_m = re.search(r'const TR = (\{.*?\});', html, re.DOTALL)
    tr_script = tr_m.group(0) if tr_m else "const TR = {};"
    
    # Get the setLang JS
    lang_js_m = re.search(r'(let currentLang.*?)(?:</script>)', html, re.DOTALL)
    lang_js = lang_js_m.group(1) if lang_js_m else ""
    
    # Extract sections preserving data-i18n
    sections_raw = extract_sections(body)
    
    sections_html = ""
    toc = [("Executive Summary", "section-0")]
    
    for i, sec in enumerate(sections_raw):
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', sec)
        if hm:
            label = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
            toc.append((label, f"section-{i}"))
        sec = re.sub(r'padding:\d+px\s*0', '', sec)
        sections_html += f'<section id="section-{i}">\n{sec.strip()}\n</section>\n\n'
    
    # Also include download strip and other content outside sections
    dl_strip_m = re.search(r'(<div class="dl-strip">.*?</div>)', body, re.DOTALL)
    dl_strip = dl_strip_m.group(0) if dl_strip_m else ""
    
    # Insert download strip before first callout
    sections_html = sections_html.replace('<div class="callout"', dl_strip + '\n<div class="callout"', 1)
    
    full_script = f"<script>\n{tr_script}\n{lang_js}\n</script>"
    
    result = TEMPLATE
    result = result.replace("{{TITLE}}", title)
    result = result.replace("{{DESCRIPTION}}", desc)
    result = result.replace("{{TAG}}", tag)
    result = result.replace("{{H1}}", h1)
    result = result.replace("{{DATE}}", "June 28, 2026")
    result = result.replace("{{SECTIONS}}", sections_html.strip())
    result = result.replace("{{TOC_LINKS}}", make_toc_links(toc))
    result = result.replace("{{NAV_LINKS}}", make_nav_sidebar_links("index"))
    result = result.replace("{{PAGE_LINKS}}", make_page_links("index"))
    result = result.replace("{{TRANSLATION_SCRIPT}}", full_script)
    
    # Fix image paths - redesign is in a subfolder
    result = result.replace('src="idrbt-lied', 'src="../idrbt-lied')
    result = result.replace("src='idrbt-lied", "src='../idrbt-lied")
    
    return result

def process_cookie_tracking():
    html = read_file(f"{SITE_DIR}/cookie-tracking.html")
    body = extract_body_content(html)
    title = extract_title(html)
    desc = extract_meta_description(html)
    tag = extract_tag_from_hero(body)
    h1 = extract_h1(body)
    
    sections_raw = extract_sections(body)
    sections_html = ""
    toc = [("Overview", "section-0")]
    
    for i, sec in enumerate(sections_raw):
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', sec)
        if hm:
            label = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
            toc.append((label, f"section-{i}"))
        sections_html += f'<section id="section-{i}">\n{sec.strip()}\n</section>\n\n'
    
    # Extract ul/ol styles and callout blocks
    sections_html = re.sub(r'(<ul[^>]*style="[^"]*")(>)', r'\1 style="color:#444;font-size:.9rem;margin:12px 0 12px 24px;line-height:1.8"\2', sections_html)
    sections_html = re.sub(r'(<ol[^>]*style="[^"]*")(>)', r'\1 style="color:#444;font-size:.9rem;margin:12px 0 12px 24px;line-height:1.8"\2', sections_html)
    
    result = TEMPLATE
    result = result.replace("{{TITLE}}", title)
    result = result.replace("{{DESCRIPTION}}", desc)
    result = result.replace("{{TAG}}", tag if tag else "Privacy & Tracking")
    result = result.replace("{{H1}}", h1)
    result = result.replace("{{DATE}}", "June 30, 2026")
    result = result.replace("{{SECTIONS}}", sections_html.strip())
    result = result.replace("{{TOC_LINKS}}", make_toc_links(toc))
    result = result.replace("{{NAV_LINKS}}", make_nav_sidebar_links("cookie-tracking"))
    result = result.replace("{{PAGE_LINKS}}", make_page_links("cookie-tracking"))
    result = result.replace("{{TRANSLATION_SCRIPT}}", "")
    
    # Fix inline SVG img data URIs - remove entire img tag properly
    # The SVG data URI uses single quotes for src attr, double quotes inside SVG
    result = re.sub(r"<img[^>]*src='data:image/svg[^']*'[^>]*/?>", '<div style="background:#f8f6f4;border:1px solid #e0ddd8;border-radius:6px;padding:14px;margin:14px 0;font-size:.82rem;color:#999;text-align:center">📊 Diagram (see source for details)</div>', result)
    
    return result

def process_shutdown_critique():
    html = read_file(f"{SITE_DIR}/shutdown-critique.html")
    body = extract_body_content(html)
    title = extract_title(html)
    desc = extract_meta_description(html)
    tag = extract_tag_from_hero(body)
    h1 = extract_h1(body)
    
    sections_raw = extract_sections(body)
    sections_html = ""
    toc = [("Introduction", "section-0")]
    
    for i, sec in enumerate(sections_raw):
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', sec)
        if hm:
            label = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
            toc.append((label, f"section-{i}"))
        sections_html += f'<section id="section-{i}">\n{sec.strip()}\n</section>\n\n'
    
    sections_html = re.sub(r'(<ul[^>]*style="[^"]*")(>)', r'\1 style="color:#444;font-size:.9rem;margin:12px 0 12px 24px;line-height:1.8"\2', sections_html)
    
    result = TEMPLATE
    result = result.replace("{{TITLE}}", title)
    result = result.replace("{{DESCRIPTION}}", desc)
    result = result.replace("{{TAG}}", tag if tag else "Critique & Governance")
    result = result.replace("{{H1}}", h1)
    result = result.replace("{{DATE}}", "July 1, 2026")
    result = result.replace("{{SECTIONS}}", sections_html.strip())
    result = result.replace("{{TOC_LINKS}}", make_toc_links(toc))
    result = result.replace("{{NAV_LINKS}}", make_nav_sidebar_links("shutdown-critique"))
    result = result.replace("{{PAGE_LINKS}}", make_page_links("shutdown-critique"))
    result = result.replace("{{TRANSLATION_SCRIPT}}", "")
    
    return result

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    files = {
        "index.html": process_index,
        "cookie-tracking.html": process_cookie_tracking,
        "shutdown-critique.html": process_shutdown_critique,
    }
    
    total_in = 0
    total_out = 0
    
    for filename, processor in files.items():
        out_path = f"{OUT_DIR}/{filename}"
        result = processor()
        with open(out_path, "w") as f:
            f.write(result)
        
        in_size = os.path.getsize(f"{SITE_DIR}/{filename}")
        out_size = len(result)
        total_in += in_size
        total_out += out_size
        diff = "+" if in_size < out_size else "-"
        print(f"{filename}: {in_size/1000:.0f}K → {out_size/1000:.0f}K ({diff}{abs(out_size-in_size)/1000:.0f}K)")
    
    print(f"\nTotal: {total_in/1000:.0f}K → {total_out/1000:.0f}K")
    print(f"Output: {OUT_DIR}/")

if __name__ == "__main__":
    main()
