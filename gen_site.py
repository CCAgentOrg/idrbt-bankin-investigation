#!/usr/bin/env python3
"""Generate static site for IDRBT .bank.in investigation.

Reads report.md and produces a standalone HTML page.
"""
import os, re, json
from html import escape

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(REPO, "site")
# ASSETS_SRC removed
REPORT_MD = os.path.join(REPO, "report.md")

os.makedirs(OUT, exist_ok=True)

# ── Read report.md ──────────────────────────────────────────────
with open(REPORT_MD) as f:
    md = f.read()

# ── Copy assets ─────────────────────────────────────────────────
import shutil

# Copy report PDF
shutil.copy2(os.path.join(REPO, "report.pdf"), os.path.join(OUT, "report.pdf"))

# ── CSS ─────────────────────────────────────────────────────────
CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: #0a0a0b; color: #e4e0d8; line-height: 1.7; font-size: 17px;
}
a { color: #f59e0b; text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3, h4 { color: #f5f1e8; line-height: 1.3; }
h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
h2 { font-size: 1.6rem; margin: 2.5rem 0 1rem; border-bottom: 1px solid #222; padding-bottom: 0.4rem; }
h3 { font-size: 1.2rem; margin: 1.8rem 0 0.8rem; color: #d8a657; }
h4 { font-size: 1.05rem; margin: 1.2rem 0 0.5rem; color: #c9b99a; }
p { margin: 0.8rem 0; }
ul, ol { margin: 0.8rem 0; padding-left: 1.5rem; }
li { margin: 0.4rem 0; }
strong { color: #f5f1e8; }
code, pre {
  font-family: "SF Mono", "Cascadia Code", "JetBrains Mono", "Fira Code", Consolas, monospace;
  background: #1a1a1e; border-radius: 4px; font-size: 0.9em;
}
code { padding: 0.15em 0.35em; }
pre { padding: 1rem; overflow-x: auto; margin: 1rem 0; border: 1px solid #2a2a2e; }
table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; }
th, td { padding: 0.6rem 0.8rem; text-align: left; border-bottom: 1px solid #222; }
th { background: #151518; color: #c9b99a; font-weight: 600; }
tt { font-family: monospace; background: #1a1a1e; padding: 0.1em 0.3em; border-radius: 3px; }
blockquote { border-left: 3px solid #f59e0b; margin: 1rem 0; padding: 0.5rem 1rem; background: #111114; }

/* Hero */
.hero {
  background: linear-gradient(135deg, #0f0f11 0%, #1a1410 100%);
  padding: 4rem 2rem; text-align: center; border-bottom: 1px solid #222;
}
.hero h1 { font-size: 2.8rem; max-width: 800px; margin: 0 auto 0.5rem; }
.hero .subtitle { color: #aaa39a; font-size: 1.1rem; margin-bottom: 1.5rem; }
.hero .stats { display: flex; flex-wrap: wrap; justify-content: center; gap: 1.5rem; margin: 2rem 0; }
.hero .stat { background: rgba(28,26,22,0.7); border: 1px solid #333; border-radius: 8px; padding: 1rem 1.5rem; min-width: 120px; }
.hero .stat .num { font-size: 1.8rem; font-weight: 700; color: #f59e0b; display: block; }
.hero .stat .label { font-size: 0.8rem; color: #aaa39a; text-transform: uppercase; letter-spacing: 0.05em; }
.hero .actions { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem; }
.btn {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.7rem 1.5rem; border-radius: 6px; font-weight: 600; font-size: 0.95rem;
  transition: all 0.2s; cursor: pointer; border: none;
}
.btn-primary { background: #f59e0b; color: #0a0a0b; }
.btn-primary:hover { background: #d48a0a; text-decoration: none; }
.btn-outline { background: transparent; color: #e4e0d8; border: 1px solid #444; }
.btn-outline:hover { border-color: #f59e0b; color: #f59e0b; text-decoration: none; }

/* Nav */
nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(10,10,11,0.92); backdrop-filter: blur(8px);
  border-bottom: 1px solid #222; padding: 0.6rem 1rem;
  display: flex; gap: 0.4rem; flex-wrap: wrap;
}
nav a {
  color: #aaa39a; font-size: 0.82rem; padding: 0.3rem 0.6rem; border-radius: 4px;
  white-space: nowrap; transition: all 0.2s;
}
nav a:hover { color: #f59e0b; background: rgba(245,158,11,0.08); text-decoration: none; }

/* Content */
.container { max-width: 840px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
.tag {
  display: inline-block; padding: 0.2rem 0.6rem; border-radius: 4px;
  font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;
}
.tag-critical { background: #7f1d1d; color: #fca5a5; }
.tag-high { background: #78350f; color: #fcd34d; }
.tag-medium { background: #1e3a5f; color: #93c5fd; }
.tag-fixed { background: #14532d; color: #86efac; }
.tag-issue { background: #4c1d95; color: #c4b5fd; }

/* Grid cards */
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.card {
  background: #141416; border: 1px solid #222; border-radius: 8px; padding: 1.2rem;
}
.card h4 { margin-top: 0; color: #f5f1e8; }
.card p { font-size: 0.95rem; color: #c9c3b8; }

footer {
  border-top: 1px solid #222; padding: 2rem; text-align: center; color: #666;
  font-size: 0.9rem; margin-top: 3rem;
}
footer a { color: #aaa39a; }
@media (max-width: 640px) {
  h1 { font-size: 1.8rem; }
  .hero h1 { font-size: 1.8rem; }
  .hero .actions { flex-direction: column; align-items: center; }
  nav { overflow-x: auto; }
  .card-grid { grid-template-columns: 1fr; }
}
"""

# ── Parse sections from markdown ────────────────────────────────
# We extract headings to build sections

HEADING_RE = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
SECTION_ORDER = [
    ("eli5", "Explain It Like I'm Five"),
    ("introduction", "Introduction"),
    ("comparison", "Domain Trust: .bank vs .bank.in"),
    ("timeline", "Disclosure Timeline"),
    ("impact", "Impact Assessment"),
    ("scenarios", "Attack Scenarios"),
    ("triangulation", "Domain Triangulation"),
    ("systemic", "Systemic Issues"),
    ("methodology", "Methodology"),
    ("recommendations", "Recommendations"),
    ("opendata", "Open Data"),
    ("conclusion", "Conclusion"),
    ("disclosure", "Responsible Disclosure"),
    ("references", "References"),
    ("glossary", "Glossary"),
    ("about", "About the Author"),
]

# ── Helper: convert text with `code`, \texttt, \textbf, \url, --- etc ──
def fmt(text):
    """Convert markdown/LaTeX inline formatting to HTML."""
    text = text.replace("---", "&mdash;")
    text = text.replace("``", "&ldquo;").replace("''", "&rdquo;")
    text = text.replace("`", "").replace("\\texttt{", "<tt>").replace("}", "</tt>")
    text = text.replace("\\textbf{", "<strong>")
    text = text.replace("\\emph{", "<em>")
    text = text.replace("\\textquote{", "&ldquo;").replace("\\textquote", "&ldquo;")
    text = text.replace("\\textcolor{success}{", '<span style="color:#22c55e">')
    text = text.replace("\\textcolor{danger}{", '<span style="color:#ef4444">')
    text = text.replace("\\textcolor{accent}{", '<span style="color:#f59e0b">')
    text = text.replace("\\url{", '<a href="').replace("}", '</a>')
    text = text.replace("\\texttt{", "<code>").replace("\\textbf{", "<strong>")
    text = text.replace("\\textbf{", "<strong>").replace("\\emph{", "<em>")
    # Keep closing braces balanced — simple approach
    for _ in range(10):
        old = text
        text = re.sub(r'<tt>([^<]*?)</tt>\}', r'<tt>\1</tt>', text)
        if text == old: break
    return text

def chunk_to_html(chunk):
    """Convert a raw textual section into HTML paragraphs and lists."""
    lines = chunk.strip().split('\n')
    html = ""
    in_list = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html += {"ul": "</ul>\n", "ol": "</ol>\n"}.get(in_list, "")
                in_list = None
            continue
        if stripped.startswith("\\item["):
            # description list item
            m = re.match(r'\\item\[([^\]]+)\]\s*(.*)', stripped)
            if m:
                term = fmt(m.group(1))
                desc = fmt(m.group(2))
                html += f"<dt>{term}</dt><dd>{desc}</dd>\n"
        elif stripped.startswith("\\item") or stripped.startswith("- "):
            content = stripped.lstrip("\\item- ").strip()
            if in_list != "ul":
                if in_list: html += "</ul>\n"
                html += "<ul>\n"; in_list = "ul"
            html += f"<li>{fmt(content)}</li>\n"
        elif stripped.startswith("\\begin{itemize}"):
            if in_list: html += "</ul>\n"
            in_list = "ul"
        elif stripped.startswith("\\end{itemize}") or stripped.startswith("\\end{enumerate}"):
            if in_list: html += "</ul>\n"; in_list = None
        elif stripped.startswith("\\begin{enumerate}"):
            if in_list: html += "</ol>\n"
            in_list = "ol"
        elif stripped.startswith("\\subsection*"):
            h = re.sub(r'\\subsection\*?\{(.+)\}', r'<h3>\1</h3>', stripped)
            html += fmt(h) + "\n"
        elif stripped.startswith("\\section*"):
            h = re.sub(r'\\section\*?\{(.+)\}', r'<h2>\1</h2>', stripped)
            html += fmt(h) + "\n"
        elif stripped.startswith("\\textbf{"):
            html += f"<p>{fmt(stripped)}</p>\n"
        elif stripped.startswith("\\texttt{"):
            html += f"<p>{fmt(stripped)}</p>\n"
        elif stripped.startswith("\\begin{description}"):
            html += "<dl>\n"
        elif stripped.startswith("\\end{description}"):
            html += "</dl>\n"
        elif stripped.startswith("\\begin{verbatim}"):
            in_list = "pre"  # hack: reuse in_list
        elif stripped.startswith("\\end{verbatim}"):
            html += "</pre>\n"
            in_list = None
        elif in_list == "pre":
            html += escape(stripped) + "\n"
        elif stripped.startswith("\\begin{longtable}"):
            html += "<table>\n"
            in_list = "table"
        elif stripped.startswith("\\endlastfoot"):
            pass
        elif stripped.startswith("\\bottomrule"):
            pass
        elif stripped.startswith("\\end{longtable}"):
            html += "</table>\n"
            in_list = None
        elif stripped.startswith("\\endfirsthead"):
            pass
        elif stripped.startswith("\\endhead"):
            pass
        elif stripped.startswith("\\multicolumn"):
            pass
        elif stripped.startswith("\\toprule"):
            pass
        elif stripped.startswith("\\midrule"):
            pass
        elif in_list == "table":
            cells = [c.strip() for c in stripped.split("&")]
            cells_html = "".join(f"<td>{fmt(c)}</td>" for c in cells)
            if "\\textbf" in stripped:
                html += f"<tr>{cells_html}</tr>\n"
            else:
                html += f"<tr>{cells_html}</tr>\n"
        elif stripped.startswith("\\textbf{") and len(stripped) > 20:
            html += f"<p>{fmt(stripped)}</p>\n"
        elif stripped.startswith("\\includegraphics"):
            m = re.search(r'\{([^}]+)\}', stripped)
            if m:
                src = m.group(1).replace("./img/", "").replace("img/", "")
                html += f'<figure><img src="{src}" style="max-width:100%;border-radius:6px;margin:1rem 0" /></figure>\n'
        elif stripped.startswith("\\noindent\\textbf{"):
            html += f"<p>{fmt(stripped[12:])}</p>\n"
        elif stripped.startswith("\\vspace"):
            pass
        elif stripped.startswith("\\newpage"):
            pass
        elif stripped.startswith("\\clearpage"):
            pass
        elif stripped.startswith("\\hypertarget"):
            pass
        elif stripped.startswith("%"):
            pass
        elif stripped.startswith("\\["):
            pass
        elif stripped.startswith("\\]"):
            pass
        else:
            html += f"<p>{fmt(stripped)}</p>\n"
    if in_list in ("ul", "ol"):
        html += {"ul": "</ul>\n", "ol": "</ol>\n"}.get(in_list, "")
    return html

def read_section(start_marker, end_markers):
    """Read a section from md between start_marker and any end_marker."""
    start = md.find(start_marker)
    if start == -1:
        return ""
    start = start + len(start_marker)
    end = len(md)
    for m in end_markers:
        pos = md.find(m, start)
        if pos != -1 and pos < end:
            end = pos
    chunk = md[start:end].strip()
    # Remove heading if present
    chunk = re.sub(r'^#+\s+.+\n', '', chunk)
    return chunk_to_html(chunk)

# ── Build sections ──────────────────────────────────────────────
SECTIONS = {}

# ELI5
eli5_raw = read_section("# Appendix A: Explain It Like I'm Five",
    ["# Appendix B:"])
SECTIONS["eli5"] = eli5_raw

# Glossary
gloss_raw = read_section("# Appendix B: Glossary",
    ["# Appendix C:"])
SECTIONS["glossary"] = gloss_raw

# About
about_raw = read_section("# Appendix C: About the Author", [])
SECTIONS["about"] = about_raw

# Comparison table
comparison_raw = read_section("# Domain Trust: `", 
    ["## Disclosure Timeline", "# Disclosure Timeline"])
SECTIONS["comparison"] = comparison_raw

# Timeline
timeline_raw = read_section("# Disclosure Timeline",
    ["## Impact Assessment", "# Impact Assessment"])
SECTIONS["timeline"] = timeline_raw

# Introduction
intro_raw = read_section("# Introduction",
    ["## What the Comparison Reveals", "# Domain Trust"])
SECTIONS["introduction"] = intro_raw

# Impact
impact_raw = read_section("# Impact Assessment",
    ["## Attack Scenarios", "# Attack Scenarios"])
SECTIONS["impact"] = impact_raw

# Scenarios
scenarios_raw = read_section("# Attack Scenarios",
    ["## Domain Triangulation", "# Domain Triangulation"])
SECTIONS["scenarios"] = scenarios_raw

# Triangulation
triang_raw = read_section("# Domain Triangulation",
    ["## Systemic Issues", "# Systemic Issues"])
SECTIONS["triangulation"] = triang_raw

# Systemic
systemic_raw = read_section("# Systemic Issues",
    ["## Methodology", "# Methodology"])
SECTIONS["systemic"] = systemic_raw

# Methodology
method_raw = read_section("# Methodology",
    ["## Recommendations", "# Recommendations"])
SECTIONS["methodology"] = method_raw

# Recommendations
recs_raw = read_section("# Recommendations",
    ["## Open Data", "# Open Data"])
SECTIONS["recommendations"] = recs_raw

# Open Data
opendata_raw = read_section("# Open Data",
    ["## Conclusion", "# Conclusion"])
SECTIONS["opendata"] = opendata_raw

# Conclusion
conclusion_raw = read_section("# Conclusion",
    ["## Responsible Disclosure", "# Responsible Disclosure"])
SECTIONS["conclusion"] = conclusion_raw

# Responsible Disclosure
disc_raw = read_section("# Responsible Disclosure",
    ["## References", "# References", "# Appendix A:"])
SECTIONS["disclosure"] = disc_raw

# References
refs_raw = read_section("## Primary Sources \\& Official Documents",
    ["# Appendix A:"])
SECTIONS["references"] = refs_raw

# ── Nav bar ─────────────────────────────────────────────────────
NAV_ITEMS = [
    ("eli5", "TL;DR"),
    ("introduction", "Intro"),
    ("comparison", "Comparison"),
    ("timeline", "Timeline"),
    ("impact", "Impact"),
    ("scenarios", "Scenarios"),
    ("triangulation", "Triangulation"),
    ("systemic", "Issues"),
    ("methodology", "Methodology"),
    ("recommendations", "Recommendations"),
    ("opendata", "Open Data"),
    ("conclusion", "Conclusion"),
    ("disclosure", "Disclosure"),
    ("references", "Sources"),
    ("glossary", "Glossary"),
    ("about", "About"),
]
nav_html = "\n".join(f'<a href="#{sid}">{label}</a>' for sid, label in NAV_ITEMS)

# ── Assemble HTML ──────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>From Trust Mandate to Security Debacle — IDRBT .bank.in Investigation</title>
<meta name="description" content="A security investigation of the IDRBT .bank.in Domain Registration Portal: 33+ unauthenticated endpoints, 5,576 exposed bank employee credentials, systemic governance failures.">
<style>{CSS}</style>
</head>
<body>

<header class="hero">
  <h1>From Trust Mandate to Security&nbsp;Debacle</h1>
  <p class="subtitle">A Security Investigation of the IDRBT <tt>.bank.in</tt> Domain Registry Portal</p>
  <p style="color:#aaa39a;font-size:0.9rem">Srikanth L, CashlessConsumer &middot; June 2026 &middot; Responsible Disclosure</p>
  <div class="stats">
    <div class="stat"><span class="num">5,576</span><span class="label">Exposed Bank Employees</span></div>
    <div class="stat"><span class="num">33+</span><span class="label">Unauthenticated Endpoints</span></div>
    <div class="stat"><span class="num">1,072</span><span class="label">Orphan Super Admins</span></div>
    <div class="stat"><span class="num">6.9%</span><span class="label">Domains Verified</span></div>
  </div>
  <div class="actions">
    <a href="report.pdf" class="btn btn-primary">&#11015; Download Full PDF Report</a>
    <a href="#eli5" class="btn btn-outline">&#9660; Quick Summary</a>
  </div>
</header>

<nav>{nav_html}</nav>

<main class="container">

<section id="eli5">
<h2>Explain It Like I'm Five</h2>
{SECTIONS.get("eli5", "")}
</section>

<section id="introduction">
<h2>Introduction</h2>
{SECTIONS.get("introduction", "")}
</section>

<section id="comparison">
<h2>Domain Trust: <tt>.bank</tt> vs <tt>.bank.in</tt></h2>
{SECTIONS.get("comparison", "")}
</section>

<section id="timeline">
<h2>Disclosure Timeline</h2>
{SECTIONS.get("timeline", "")}
</section>

<section id="impact">
<h2>Impact Assessment</h2>
{SECTIONS.get("impact", "")}
</section>

<section id="scenarios">
<h2>Attack Scenarios</h2>
{SECTIONS.get("scenarios", "")}
</section>

<section id="triangulation">
<h2>Domain Triangulation</h2>
{SECTIONS.get("triangulation", "")}
</section>

<section id="systemic">
<h2>Systemic Issues</h2>
{SECTIONS.get("systemic", "")}
</section>

<section id="methodology">
<h2>Methodology</h2>
{SECTIONS.get("methodology", "")}
</section>

<section id="recommendations">
<h2>Recommendations</h2>
{SECTIONS.get("recommendations", "")}
</section>

<section id="opendata">
<h2>Open Data</h2>
{SECTIONS.get("opendata", "")}
</section>

<section id="conclusion">
<h2>Conclusion</h2>
{SECTIONS.get("conclusion", "")}
</section>

<section id="disclosure">
<h2>Responsible Disclosure</h2>
{SECTIONS.get("disclosure", "")}
</section>

<section id="references">
<h2>References</h2>
{SECTIONS.get("references", "")}
</section>

<section id="glossary">
<h2>Glossary</h2>
{SECTIONS.get("glossary", "")}
</section>

<section id="about">
<h2>About the Author</h2>
{SECTIONS.get("about", "")}
</section>

</main>

<footer>
<p><strong>From Trust Mandate to Security Debacle</strong> &mdash; A Security Investigation by CashlessConsumer</p>
<p>All non-sensitive data published as open data. No PII included.</p>
<p><a href="https://github.com/CCAgentOrg/idrbt-bankin-investigation">Source Code</a> &middot;
<a href="https://zo.pub/cashlessconsumer/idrbt-bankin-security">Evidence Archive</a> &middot;
<a href="report.pdf">Download PDF</a> &middot;
<a href="https://uptime.cashlessconsumer.in">Uptime Monitor</a> &middot;
<a href="https://github.com/CCAgentOrg/bank-in-domains">bank-in-domains</a></p>
</footer>

</body>
</html>"""

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(HTML)

print(f"Site generated: {os.path.join(OUT, 'index.html')} ({len(HTML)} bytes)")
