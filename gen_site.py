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
/* Language bar */
.lang-bar{background:#f5f5f5;border-bottom:1px solid #ddd;padding:8px 0;text-align:center}
.lang-bar .inner{max-width:720px;margin:0 auto;padding:0 20px}
.lang-bar strong{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:.78rem;color:#555;margin-right:6px}
.lang-btn{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:.76rem;border:1px solid #ccc;background:#fff;color:#555;padding:2px 8px;border-radius:3px;cursor:pointer;margin:2px;transition:all .15s}
.lang-btn:hover{border-color:#b00;color:#b00}
.lang-active{background:#b00;color:#fff;border-color:#b00;font-weight:600}
.trans-banner{background:#fff3cd;border-bottom:1px solid #ffc107;text-align:center;font-size:.77rem;padding:5px 16px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#856404}

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
<div class="lang-bar"><div class="inner"><strong>Language:</strong> <button class="lang-btn lang-active" id="lang-en" onclick="setLang('en')">English</button> <button class="lang-btn" id="lang-hi" onclick="setLang('hi')">हिन्दी</button> <button class="lang-btn" id="lang-bn" onclick="setLang('bn')">বাংলা</button> <button class="lang-btn" id="lang-mr" onclick="setLang('mr')">मराठी</button> <button class="lang-btn" id="lang-te" onclick="setLang('te')">తెలుగు</button> <button class="lang-btn" id="lang-ta" onclick="setLang('ta')">தமிழ்</button> <button class="lang-btn" id="lang-gu" onclick="setLang('gu')">ગુજરાતી</button> <button class="lang-btn" id="lang-ur" onclick="setLang('ur')">اردو</button> <button class="lang-btn" id="lang-kn" onclick="setLang('kn')">ಕನ್ನಡ</button> </div></div>
<div class="trans-banner" id="trans-banner" style="display:none">⚠️ AI-generated translation. English original is authoritative.</div>


<!-- Header -->
<div class="container article-header">
<div class="tag" data-i18n="tag">
<h1 data-i18n="h1">
<div class="byline" data-i18n="byline">
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


<script>
const TR = {
  "en": {"label":"English","trans_d":""},
  "hi": {"tag": "सुरक्षा जांच", "h1": "Trust Mandate से Security Debacle तक", "byline": "<strong>CashlessConsumer</strong> · <span class=\"date\">28 जून 2026</span>", "h2_main": "33+ असुरक्षित API ने 5,576 बैंक कर्मचारियों के क्रेडेंशियल्स को एक साल से अधिक समय तक उजागर किया", "h2_sub": "IDRBT का डोमेन रजिस्ट्रेशन पोर्टल — भारत के .bank.in बैंकिंग नेमस्पेस का एकमात्र गेटकीपर — bcrypt पासवर्ड हैश, मोबाइल नंबर और लॉगिन डेटा को curl चलाने वाले किसी भी व्यक्ति के लिए लीक कर रहा था। CERT-In ने 25 जून को फिक्स की पुष्टि की।", "p1": "7 फरवरी 2025 को, भारतीय रिजर्व बैंक ने .bank.in की घोषणा की — भारतीय बैंकिंग के लिए एक समर्पित इंटरनेट डोमेन नेमस्पेस, जो भारतीय बैंकिंग के लिए एक विश्वास एंकर के रूप में काम करने वाला था। .bank.in URL टाइप करने वाले नागरिकों को पता होना चाहिए था कि वे एक वैध बैंक वेबसाइट पर हैं, जो नियामक द्वारा सत्यापित है।", "p2": "विश्वास एंकर ही पूरी तरह से खुला था।", "p3": "IDRBT डोमेन रजिस्ट्रेशन पोर्टल — जिसके माध्यम से प्रत्येक भारतीय बैंक को अपना .bank.in डोमेन पंजीकृत करना होगा — ने 33+ अनऑथेंटिकेटेड एंडपॉइंट्स के माध्यम से अपनी पूरी REST API को उजागर कर दिया। कोई पासवर्ड नहीं। कोई टोकन नहीं। कोई लॉगिन आवश्यक नहीं। बस एक curl कमांड, और कोई भी इंटरनेट उपयोगकर्ता 5,576 बैंक कर्मचारियों के bcrypt हैश, मोबाइल नंबर, ईमेल पते, लॉगिन IP और डिवाइस फिंगरप्रिंट प्राप्त कर सकता था।", "p4": "पोर्टल का निर्माण IKCON Technologies (हैदराबाद) द्वारा बिना किसी सार्वजनिक निविदा, RFP या प्रतिस्पर्धी प्रक्रिया के किया गया — जो IDRBT के स्वयं के प्रकाशित क्रय पुस्तिका (2015) का सीधा उल्लंघन है। IKCON के 22 कर्मचारी खाते थे, जिनमें 3 ग्लोबल सुपर एडमिन एक्सेस वाले थे। 1,497 पंजीकृत डोमेन में से केवल 6.9% RBI के IFSC डेटाबेस और DICGC बीमा रिकॉर्ड से मेल खाते थे।", "p5": "वैश्विक .bank TLD के विपरीत — जो DNSSEC, DMARC p=reject, HSTS और EV/OV प्रमाणपत्र अनिवार्य करता है — भारत का .bank.in इनमें से किसी को भी लागू नहीं करता है। 80% सहकारी बैंकों में DNSSEC नहीं है, 40% में DMARC नहीं है, और कई बैंक RBI डेटा स्थानीयकरण नियमों के उल्लंघन में विदेशी सर्वर पर ग्राहक-सामना वाली साइटें होस्ट करते हैं।", "p6": "कमजोरी की सूचना 8 जून 2026 को 05:30 UTC पर CERT-In को दी गई — खोज के 25 मिनट के भीतर। CERT-In ने 25 जून 2026 को समाधान की पुष्टि की। उजागर एंडपॉइंट अब सुलभ नहीं हैं।", "h2_attacks": "एक दुर्जन क्या कर सकता था", "attacks_sub": "डेटा 13 महीनों तक सार्वजनिक था। इन हमलों के लिए केवल अनऑथेंटिकेटेड एंडपॉइंट्स से प्राप्त डेटा की आवश्यकता थी।", "scenario_1_title": "1. बड़े पैमाने पर फिशिंग", "scenario_1_time": "< 1 घंटा", "scenario_1_text": "5,461 रिकॉर्ड नाम, ईमेल पते, मोबाइल नंबर और संगठन के नामों के साथ। प्रत्येक रिकॉर्ड बताता है कि कौन सा बैंक कर्मचारी किस बैंक के डोमेन का प्रबंधन करता है। सही आंतरिक विवरणों का उपयोग करके वैयक्तिकृत स्पीयर-फिशिंग ईमेल — केवल वास्तविक पोर्टल को ही पता होने चाहिए। एक समझौता किया गया क्रेडेंशियल प्रमाणित पोर्टल एक्सेस देता है।", "scenario_2_title": "2. क्रेडेंशियल चोरी से डोमेन अपहरण", "scenario_2_time": "दिनों से हफ्तों तक", "scenario_2_text": "1,072 अनाथ सुपर एडमिन खाते — जिनका किसी संगठन से कोई संबंध नहीं है — जिनके bcrypt हैश उजागर हो गए। कमजोर पासवर्ड (जैसे password123, bank@2025) घंटों में क्रैक किए जा सकते हैं। सुपर एडमिन एक्सेस से: किसी भी .bank.in डोमेन को स्थानांतरित करना, DNS रिकॉर्ड बदलना, वैध प्रशासकों को बाहर करना।", "scenario_3_title": "3. अदृश्य रिडायरेक्ट", "scenario_3_time": "पोर्टल एक्सेस से मिनट", "scenario_3_text": "एक सहकारी बैंक के A रिकॉर्ड को वैध सर्वर से विदेश में होस्टेड फिशिंग साइट पर बदलना। चूंकि .bank.in EV/OV प्रमाणपत्र अनिवार्य नहीं करता है, फिशिंग साइट एक मुफ्त Let's Encrypt प्रमाणपत्र प्राप्त करती है। ब्राउज़र हरा पैडलॉक दिखाता है। डोमेन sirsadccb.bank.in पढ़ता है। ग्राहक को पता नहीं चलता।", "scenario_4_title": "4. आंतरिक खतरे का विस्तार", "scenario_4_time": "तुरंत", "scenario_4_text": "डिवाइस फिंगरप्रिंट और लॉगिन IP मैप करते हैं कि किन कर्मचारियों के पास सुपर एडमिन एक्सेस है, किन संगठनों की सुरक्षा सबसे कमजोर है, और कौन से खाते बासी हैं। राष्ट्र-राज्य अभिनेता या संगठित साइबर अपराध समूह सबसे कमजोर कड़ी को सर्जिकल सटीकता के साथ लक्षित कर सकते हैं।", "callout_title": "मुख्य निष्कर्ष", "callout_text": "इनमें से किसी भी परिदृश्य के लिए जीरो-डे का शोषण, फायरवॉल को दरकिनार करना, या एक्सप्लॉइट कोड लिखना आवश्यक नहीं था। हमलावर को केवल curl की आवश्यकता थी। डेटा पहले से ही सार्वजनिक था। इन परिदृश्यों के साकार न होने का एकमात्र कारण यह है कि CashlessConsumer ने पहले कमजोरी पाई और जिम्मेदारी से रिपोर्ट की।", "h2_timeline": "खुलासा समयरेखा", "timeline_sub": "खोज से समाधान तक 17 दिन।", "tl_1": "RBI ने द्विमासिक मौद्रिक नीति वक्तव्य में .bank.in नेमस्पेस की घोषणा की", "tl_2": "RBI ने .bank.in को सभी अनुसूचित वाणिज्यिक बैंकों, सहकारी बैंकों और RRB के लिए अनिवार्य किया", "tl_3": "IDRBT डोमेन रजिस्ट्रेशन पोर्टल लॉन्च। IKCON द्वारा बिना सार्वजनिक निविदा के विकसित।", "tl_4": "CashlessConsumer ने नियमित OSINT स्कैन के दौरान पहला अनऑथेंटिकेटेड यूजर डेटाबेस एंडपॉइंट खोजा", "tl_5": "CERT-In को प्रारंभिक जिम्मेदार खुलासा रिपोर्ट प्रस्तुत", "tl_6": "अनऑथेंटिकेटेड इनवॉइस और बिलिंग एंडपॉइंट की खोज (1,535 रिकॉर्ड)", "tl_7": "विस्तारित रिपोर्ट: अनाथ उपयोगकर्ता (1,072), प्रेत डोमेन, DSC प्रॉक्सी एक्सपोज़र", "tl_8": "CERT-In ने स्वीकार किया (संदर्भ: CERTIn-62780526) और प्राप्ति की पुष्टि की", "tl_9": "CERT-In ने IDRBT द्वारा कमजोरी के समाधान की पुष्टि की", "h2_systemic": "प्रणालीगत मुद्दे बने हुए हैं", "systemic_sub": "तत्काल कमजोरी ठीक हो गई है। ये गहरे शासन और सुरक्षा अंतराल बने हुए हैं।", "sys_1": "कोई सार्वजनिक निविदा नहीं। IKCON Technologies को बिना किसी RFP के नियुक्त किया गया, जो IDRBT की अपनी 2015 क्रय पुस्तिका का उल्लंघन है। IKCON के पास 22 खाते थे जिनमें 3 सुपर एडमिन एक्सेस वाले थे।", "sys_2": "टेस्ट/प्रोडक्शन ओवरलैप। प्रेत डोमेन (VKTEST, IKCONTESTBANK, IDTMAY) और बकवास खाते वास्तविक बैंकों के साथ प्रोडक्शन डेटाबेस में हैं। कई के पास सर्टिफिकेट ट्रांसपेरेंसी लॉग में सक्रिय SSL प्रमाणपत्र हैं।", "sys_3": "कोई अनिवार्य सुरक्षा आधार रेखा नहीं। वैश्विक .bank TLD के विपरीत, भारत का .bank.in कोई DNSSEC, DMARC, HSTS या CAA आवश्यकताओं को लागू नहीं करता है। 80% सहकारी बैंकों में DNSSEC नहीं है, 40% में DMARC नहीं है, 47% में HSTS नहीं है।", "sys_4": "डेटा रेजीडेंसी उल्लंघन। सहकारी बैंक विदेशी सर्वर (अमेरिका, सिंगापुर, लिथुआनिया) पर ग्राहक-सामना वाली वेबसाइटें होस्ट करते हैं, जो RBI डेटा स्थानीयकरण आवश्यकताओं को कमजोर करता है।", "sys_5": "IDRBT के अपने सुरक्षा दावों का खंडन। पोर्टल की गोपनीयता नीति ने दावा किया कि इसे 'फायरवॉल और IPS सुरक्षा के साथ संरक्षित क्षेत्रों में रखा गया है' और 'लॉन्च से पहले ज्ञात एप्लिकेशन-स्तरीय कमजोरियों के लिए ऑडिट किया गया।' अनऑथेंटिकेटेड API पहले दिन से मौजूद था।", "sys_6": "शैक्षणिक शोध अनदेखा। IDRBT के शोधकर्ताओं ने डोमेन सुरक्षा, DNSSEC और बैंकिंग के लिए साइबर सुरक्षा बेंचमार्क पर पेपर प्रकाशित किए — जिनमें से किसी ने भी .bank.in कार्यान्वयन को सूचित नहीं किया।", "h2_data": "खुला डेटा", "data_sub": "सभी गैर-संवेदनशील डेटासेट स्वतंत्र सत्यापन के लिए प्रकाशित। कोई PII या bcrypt हैश शामिल नहीं।", "data_note": "डेटा bank-in-domains दैनिक सुरक्षा ऑडिट में फीड करता है, जो प्रतिदिन 02:30 UTC पर CT लॉग, Wayback Machine और urlscan.io से नए .bank.in सबडोमेन खोजता है।", "links_report": "📄 पूर्ण रिपोर्ट (PDF)", "links_code": "💻 स्रोत कोड", "links_audit": "🔍 दैनिक ऑडिट फीड", "links_archive": "📦 साक्ष्य संग्रह", "links_uptime": "⏱️ अपटाइम मॉनिटर", "about_title": "CashlessConsumer", "about_text": "एक उपभोक्ता सामूहिक जो भारत में डिजिटल भुगतान उद्योग को ट्रैक करता है, एक नकद रहित समाज की दिशा में जागरूकता संसाधन, तकनीकी विश्लेषण, खुला डेटा और नीति इनपुट तैयार करता है। यह जांच एक सुसंगत पद्धति का पालन करती है: सार्वजनिक रिकॉर्ड, OSINT, RTI और जिम्मेदार खुलासा — कोई हैकिंग नहीं, कोई चुराया डेटा नहीं, कोई प्रतिकूल तकनीक नहीं।", "about_prior": "पूर्व कार्य: KillerLoanApps · BFIL Consent Scam · Fintech Governance RTI Program", "about_links": "cashlessconsumer.in · Newsletter · GitHub", "footer": "जिम्मेदार खुलासा सिद्धांतों के तहत प्रकाशित। © जून 2026। रिपोर्ट Srikanth L, CashlessConsumer द्वारा।"},
  "bn": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "বাংলা"},
  "mr": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "मराठी"},
  "te": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "తెలుగు"},
  "ta": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "தமிழ்"},
  "gu": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "ગુજરાતી"},
  "ur": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "اردو"},
  "kn": {"tag": "…", "h1": "…", "byline": "…", "h2_main": "…", "h2_sub": "…", "p1": "…", "p2": "…", "p3": "…", "p4": "…", "p5": "…", "p6": "…", "h2_attacks": "…", "attacks_sub": "…", "scenario_1_title": "…", "scenario_1_time": "…", "scenario_1_text": "…", "scenario_2_title": "…", "scenario_2_time": "…", "scenario_2_text": "…", "scenario_3_title": "…", "scenario_3_time": "…", "scenario_3_text": "…", "scenario_4_title": "…", "scenario_4_time": "…", "scenario_4_text": "…", "callout_title": "…", "callout_text": "…", "h2_timeline": "…", "timeline_sub": "…", "tl_1": "…", "tl_2": "…", "tl_3": "…", "tl_4": "…", "tl_5": "…", "tl_6": "…", "tl_7": "…", "tl_8": "…", "tl_9": "…", "h2_systemic": "…", "systemic_sub": "…", "sys_1": "…", "sys_2": "…", "sys_3": "…", "sys_4": "…", "sys_5": "…", "sys_6": "…", "h2_data": "…", "data_sub": "…", "data_note": "…", "links_report": "…", "links_code": "…", "links_audit": "…", "links_archive": "…", "links_uptime": "…", "about_title": "…", "about_text": "…", "about_prior": "…", "about_links": "…", "footer": "…", "trans_d": "⚠️ AI-generated translation. English original is authoritative.", "label": "ಕನ್ನಡ"}
};
let currentLang = 'en';
function setLang(code) {
  currentLang = code;
  const t = TR[code];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key] && t[key] !== '…') el.innerHTML = t[key];
  });
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('lang-active'));
  document.getElementById('lang-' + code).classList.add('lang-active');
  document.documentElement.lang = code;
  const banner = document.getElementById('trans-banner');
  if (code !== 'en' && t.trans_d) {
    banner.style.display = 'block';
    banner.textContent = t.trans_d;
  } else {
    banner.style.display = 'none';
  }
}
</script>
</body>
</html>"""

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(HTML)

print(f"Site generated: {os.path.join(OUT, 'index.html')} ({len(HTML)} bytes)")
