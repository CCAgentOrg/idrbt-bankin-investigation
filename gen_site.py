#!/usr/bin/env python3
"""Generate crisp static landing page for IDRBT .bank.in investigation.

A scannable, Sam Curry-style disclosure page. Full details remain in report.pdf.
"""
import os, shutil

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(REPO, "site")

os.makedirs(OUT, exist_ok=True)

# ── Copy assets ─────────────────────────────────────────────────
shutil.copy2(os.path.join(REPO, "report.pdf"), os.path.join(OUT, "report.pdf"))
try:
    for fn in os.listdir(os.path.join(REPO, "assets")):
        shutil.copy2(os.path.join(REPO, "assets", fn), os.path.join(OUT, fn))
except FileNotFoundError:
    pass

# Copy open-data
shutil.copytree(os.path.join(REPO, "open-data"), os.path.join(OUT, "open-data"), dirs_exist_ok=True)

# ── Page content from report.md ────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>IDRBT .bank.in Security Investigation — CashlessConsumer</title>
<meta name="description" content="33+ unauthenticated API endpoints on the IDRBT Domain Registration Portal exposed bcrypt password hashes for 5,576 bank employees." />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔐</text></svg>" />
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Georgia, "Times New Roman", Times, serif;background:#fff;color:#222;line-height:1.8;font-size:18px}
a{color:#b00;text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:720px;margin:0 auto;padding:0 20px}
tt, code, pre{font-family:Menlo, Consolas, monospace;font-size:.85em}

/* Article header */
.article-header{padding:56px 0 24px;border-bottom:1px solid #ddd;margin-bottom:32px}
.article-header h1{font-size:2rem;font-weight:700;line-height:1.25;margin-bottom:12px;letter-spacing:-.01em}
.article-header .byline{color:#555;font-size:.9rem;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.article-header .byline .date{color:#888}
.article-header .tag{display:inline-block;background:#b00;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:.72rem;font-weight:600;padding:3px 10px;border-radius:3px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:16px}

/* Article body */
article p{margin-bottom:18px;color:#333}
article p strong{color:#b00}
article h2{font-size:1.4rem;font-weight:700;margin:40px 0 8px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
article h3{font-size:1.1rem;font-weight:600;margin:24px 0 4px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
article .subhead{color:#666;font-size:.92rem;margin-bottom:20px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}

/* Scenario cards - simplified */
.scenario{margin-bottom:16px;padding:0 0 16px 0;border-bottom:1px solid #eee}
.scenario:last-child{border-bottom:none}
.scenario h3{font-size:1.05rem;margin-bottom:2px}
.scenario .sc-time{color:#b00;font-family:Menlo, Consolas, monospace;font-size:.8rem;margin-bottom:4px}
.scenario p{color:#444;font-size:.92rem}

/* Timeline */
.timeline{list-style:none;padding:0}
.timeline li{display:flex;gap:16px;padding:8px 0;border-bottom:1px solid #eee;font-size:.92rem}
.timeline li:last-child{border-bottom:none}
.timeline .date{color:#b00;font-family:Menlo, Consolas, monospace;font-size:.82rem;white-space:nowrap;min-width:115px;padding-top:1px}
.timeline .event{color:#444}

/* Callout */
.callout{background:#fafafa;border-left:3px solid #b00;padding:18px 22px;margin:24px 0;border-radius:0 6px 6px 0}
.callout h3{color:#b00;margin-bottom:4px;font-size:1rem}
.callout p{color:#444;font-size:.9rem;margin-bottom:0}

/* Data table */
.data-table{width:100%;border-collapse:collapse;font-size:.88rem;margin:16px 0}
.data-table th,.data-table td{text-align:left;padding:7px 10px;border-bottom:1px solid #eee}
.data-table th{color:#666;font-weight:500;font-size:.78rem;text-transform:uppercase;letter-spacing:.03em;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.data-table td{color:#333}
.data-table .yes{color:#080}
.data-table .no{color:#b00}

/* Issues list */
.issue{margin-bottom:10px;font-size:.92rem;color:#444}
.issue strong{color:#222}

/* Links */
.links{padding:24px 0;display:flex;flex-wrap:wrap;gap:10px}
.links a{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:.88rem;background:#fafafa;border:1px solid #ddd;border-radius:5px;padding:8px 14px;color:#333}
.links a:hover{border-color:#b00;text-decoration:none}

/* About box */
.about-box{background:#fafafa;border:1px solid #eee;border-radius:6px;padding:20px;margin:28px 0;font-size:.9rem}
.about-box h3{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:1rem;font-weight:600;margin-bottom:4px}
.about-box p{color:#444;margin-bottom:6px}
.about-box .ref{color:#777;font-size:.82rem}

footer{padding:32px 0;text-align:center;color:#aaa;font-size:.78rem;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}

@media(max-width:600px){
  body{font-size:16px}
  .article-header h1{font-size:1.5rem}
  .timeline li{flex-direction:column;gap:2px}
  .timeline .date{min-width:auto}
}
</style>
</head>
<body>

<!-- Header -->
<div class="container article-header">
<div class="tag">Security Investigation</div>
<h1>From Trust Mandate to Security Debacle</h1>
<div class="byline">
  <strong>CashlessConsumer</strong> &nbsp;·&nbsp; <span class="date">June 28, 2026</span>
</div>
</div>

<!-- Article body -->
<article class="container">

<section>
<h2>33+ unauthenticated APIs exposed 5,576 bank employees' credentials for over a year</h2>
<div class="subhead">IDRBT&rsquo;s domain registration portal — the exclusive gatekeeper for India&rsquo;s <tt>.bank.in</tt> banking namespace — was leaking bcrypt password hashes, mobile numbers, and login data to anyone with <tt>curl</tt>. CERT-In confirmed the fix on June 25.</div>

<p>
On February 7, 2025, the Reserve Bank of India announced the creation of <tt>.bank.in</tt> — a dedicated Internet domain namespace meant to serve as a <strong>trust anchor</strong> for Indian banking. Citizens typing a <tt>.bank.in</tt> URL were supposed to know they were on a legitimate bank website, verified by the regulator.
</p>

<p>
The trust anchor itself was wide open.
</p>

<p>
The IDRBT Domain Registration Portal at <tt>registrar.idrbt.ac.in</tt> — the exclusive registry through which every Indian bank must register its <tt>.bank.in</tt> domain — exposed its entire REST API via <strong>33+ unauthenticated endpoints</strong>. No password. No token. No login required. Just a <tt>curl</tt> command, and anyone on the internet could retrieve the bcrypt password hashes, mobile numbers, email addresses, login IPs, and device fingerprints of all <strong>5,576 bank employees</strong> entrusted with managing India&rsquo;s banking domains.
</p>

<p>
The portal was built by <strong>IKCON Technologies</strong> (Hyderabad) without any public tender, RFP, or competitive process — in direct violation of IDRBT&rsquo;s own published procurement handbook (2015). IKCON employees held 22 accounts in the system, including 3 with global Super Admin access. Of the <strong>1,497 registered domains</strong>, only <strong>6.9%</strong> matched across RBI&rsquo;s IFSC database and DICGC insurance records. The rest include phantom test domains, gibberish registrations, and non-bank entities, several with live SSL certificates.
</p>

<p>
Beyond credentials, the investigation found that unlike the global <tt>.bank</tt> TLD — which mandates DNSSEC, DMARC <tt>p=reject</tt>, HSTS, and EV/OV certificates — India&rsquo;s <tt>.bank.in</tt> enforces none of these. 80% of cooperative banks lack DNSSEC, 40% have no DMARC, and multiple banks host customer-facing sites on foreign servers in violation of RBI data localization rules.
</p>

<p>
The vulnerability was reported to CERT-In at <strong>05:30 UTC on June 8, 2026</strong> — within 25 minutes of discovery. CERT-In acknowledged with reference <tt>CERTIn-62780526</tt> and confirmed the fix on <strong>June 25, 2026</strong>. The exposed endpoints are no longer accessible.
</p>

</section>

<section>
<h2>What a bad actor could have done</h2>
<div class="subhead">The data was public for 13 months. These attack chains required only the data already accessible through unauthenticated endpoints.</div>

<div class="scenario">
<h3>1. Phishing at Scale</h3>
<div class="sc-time">&lt; 1 hour</div>
<p>5,461 records with names, email addresses, mobile numbers, and organization names. Each record identifies exactly which bank employee manages which bank's domain registration. Personalised spear-phishing emails referencing correct internal details — only the real portal should know them. A single compromised credential gives authenticated portal access.</p>
</div>

<div class="scenario">
<h3>2. Domain Hijacking via Credential Theft</h3>
<div class="sc-time">Days to weeks</div>
<p><strong>1,072 orphan Super Admin accounts</strong> — accounts with no organization association, meaning they can access any bank&rsquo;s domain settings — had their bcrypt hashes exposed. Weak passwords (e.g. <tt>password123</tt>, <tt>bank@2025</tt>) crackable in hours. With Super Admin access: transfer any <tt>.bank.in</tt> domain, change DNS records, lock legitimate administrators out.</p>
</div>

<div class="scenario">
<h3>3. The Invisible Redirect</h3>
<div class="sc-time">Minutes with portal access</div>
<p>Change a cooperative bank&rsquo;s A record from a legitimate server to a phishing site hosted overseas. Since <tt>.bank.in</tt> does not mandate EV/OV certificates, the phishing site obtains a free Let&rsquo;s Encrypt certificate. The browser shows a green padlock. The domain reads <tt>sirsadccb.bank.in</tt>. The customer has no way to know.</p>
</div>

<div class="scenario">
<h3>4. Insider Threat Amplification</h3>
<div class="sc-time">Instant</div>
<p>Device fingerprints and login IPs map exactly which employees have Super Admin access, which organizations have the weakest security postures, and which accounts are stale. Nation-state actors or organized cybercrime groups can target the weakest link with surgical precision.</p>
</div>

<div class="callout">
<h3>Key takeaway</h3>
<p>None of these scenarios required exploiting a zero-day, bypassing a firewall, or writing exploit code. The attacker only needed <tt>curl</tt>. The data was already public. The only reason these scenarios did not materialise is that CashlessConsumer found the vulnerability first and reported it responsibly.</p>
</div>
</section>

<section>
<h2>Disclosure timeline</h2>
<div class="subhead">From discovery to fix in 17 days.</div>
<ul class="timeline">
<li><span class="date">Feb 7, 2025</span><span class="event">RBI announces <tt>.bank.in</tt> namespace in bi-monthly monetary policy statement</span></li>
<li><span class="date">Apr 22, 2025</span><span class="event">RBI circular mandates <tt>.bank.in</tt> for all scheduled commercial banks, cooperative banks, and RRBs</span></li>
<li><span class="date">May 2025</span><span class="event">IDRBT Domain Registration Portal launched. Developed by IKCON Technologies without visible public tender.</span></li>
<li><span class="date">Jun 8, 05:07 UTC</span><span class="event">CashlessConsumer discovers first unauthenticated user database endpoint during routine OSINT scan</span></li>
<li><span class="date">Jun 8, 05:30 UTC</span><span class="event">Initial responsible disclosure report filed with CERT-In</span></li>
<li><span class="date">Jun 8, 06:30 UTC</span><span class="event">Discovery of unauthenticated invoice and billing endpoints (1,535 records)</span></li>
<li><span class="date">Jun 8, 07:30 UTC</span><span class="event">Extended report: orphan users (1,072), phantom domains, DSC proxy exposure</span></li>
<li><span class="date">Jun 9, 2026</span><span class="event">CERT-In acknowledges (ref: CERTIn-62780526) and confirms receipt</span></li>
<li><span class="date">Jun 25, 2026</span><span class="event">CERT-In confirms vulnerability has been fixed by IDRBT</span></li>
</ul>
</section>

<section>
<h2>Systemic issues remain</h2>
<div class="subhead">The immediate vulnerability is fixed. These deeper governance and security gaps are not.</div>

<div class="issue"><strong>No public tender.</strong> IKCON Technologies appointed without any RFP, violating IDRBT&rsquo;s own 2015 procurement handbook. IKCON held 22 accounts including 3 with Super Admin access. No public tender, RFP, or contract award was found across IDRBT&rsquo;s tenders page, MSTC eProcure, or GeM.</div>

<div class="issue"><strong>Test/production overlap.</strong> Phantom domains (VKTEST, IKCONTESTBANK, IDTMAY) and gibberish accounts sit alongside real banks in the production database. Several have active SSL certificates in Certificate Transparency logs.</div>

<div class="issue"><strong>No mandatory security baseline.</strong> Unlike the global <tt>.bank</tt> TLD, India&rsquo;s <tt>.bank.in</tt> enforces no DNSSEC, DMARC, HSTS, or CAA requirements. 80% of cooperative banks lack DNSSEC, 40% have no DMARC, 47% have no HSTS.</div>

<div class="issue"><strong>Data residency violations.</strong> Cooperative banks host customer-facing websites on foreign servers (US, Singapore, Lithuania), undermining RBI data localization requirements and exposing customers to foreign jurisdiction risks.</div>

<div class="issue"><strong>IDRBT&rsquo;s own security claims contradicted.</strong> The portal&rsquo;s Privacy Policy claimed it was "placed in protected zones along with firewall and IPS protection" and "audited for known application-level vulnerabilities before launch." The unauthenticated API was present from day one.</div>

<div class="issue"><strong>Academic research ignored.</strong> IDRBT&rsquo;s researchers published papers on domain security, DNSSEC, and cybersecurity benchmarks for banking — none of which informed the <tt>.bank.in</tt> implementation.</div>
</section>

<section>
<h2>Open data</h2>
<div class="subhead">All non-sensitive datasets published for independent verification. No PII or bcrypt hashes included.</div>
<table class="data-table">
<tr><th>Dataset</th><th>Records</th><th>Published</th></tr>
<tr><td>Registered .bank.in domains</td><td>1,497</td><td class="yes">Yes</td></tr>
<tr><td>Domains with active NS</td><td>1,402</td><td class="yes">Yes</td></tr>
<tr><td>Domains without NS (unpublished to NIXI)</td><td>95</td><td class="yes">Yes</td></tr>
<tr><td>Billing records (anonymized)</td><td>1,535</td><td class="yes">Yes</td></tr>
<tr><td>Certificate Transparency log entries</td><td>3,797</td><td class="yes">Yes</td></tr>
<tr><td>User records (original leak)</td><td>5,461</td><td class="no">No — contains PII/hashes</td></tr>
<tr><td>Orphan user records</td><td>1,072</td><td class="no">No — contains PII/hashes</td></tr>
</table>
<p style="font-size:.88rem;color:#666;margin-top:2px">Data feeds into the <a href="https://github.com/CCAgentOrg/bank-in-domains">bank-in-domains</a> daily security audit, which discovers new <tt>.bank.in</tt> subdomains from CT logs, Wayback Machine, and urlscan.io every day at 02:30 UTC.</p>
</section>

<div class="links">
<a href="report.pdf">📄 Full Report (PDF)</a>
<a href="https://github.com/CCAgentOrg/idrbt-bankin-investigation">💻 Source Code</a>
<a href="https://github.com/CCAgentOrg/bank-in-domains">🔍 Daily Audit Feed</a>
<a href="https://zo.pub/cashlessconsumer/idrbt-bankin-security">📦 Evidence Archive</a>
<a href="https://uptime.cashlessconsumer.in">⏱️ Uptime Monitor</a>
</div>

<div class="about-box">
<h3>CashlessConsumer</h3>
<p>A consumer collective that tracks the digital payments industry in India, producing awareness resources, technical analysis, open data, and policy inputs toward a fair cashless society. This investigation follows a consistent methodology: <strong>public records, OSINT, RTI, and responsible disclosure</strong> — no hacking, no stolen data, no adversarial techniques.</p>
<div class="ref">
Prior work: <a href="https://www.cashlessconsumer.in/post/killerloanapps">KillerLoanApps</a> · <a href="https://internetfreedom.in/bfil-consent-scam">BFIL Consent Scam</a> · <a href="https://www.cashlessconsumer.in/post/rtilist">Fintech Governance RTI Program</a><br/>
<a href="https://cashlessconsumer.in">cashlessconsumer.in</a> · <a href="https://newsletter.cashlessconsumer.in">Newsletter</a> · <a href="https://github.com/CCAgentOrg">GitHub</a>
</div>
</div>

</article>

<footer class="container">
<p>Published under responsible disclosure principles. © June 2026. Report by Srikanth L, CashlessConsumer.</p>
</footer>

</body>
</html>"""

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(HTML)

print(f"Site generated: {os.path.join(OUT, 'index.html')} ({len(HTML)} bytes)")
