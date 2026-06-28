#!/usr/bin/env python3
"""Generate a compact landing page for IDRBT .bank.in investigation.

Short teaser → big Download Report button. Multi-lingual via TR dict.
"""
import os, shutil, json, re

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

shutil.copytree(os.path.join(REPO, "open-data"), os.path.join(OUT, "open-data"), dirs_exist_ok=True)

# ── Translations ────────────────────────────────────────────────

# English
TR_EN = {
    "label": "English",
    "trans_d": "",
    "tag": "Security Investigation",
    "h1": "IDRBT .bank.in: From Trust Anchor to Data Leak",
    "byline": '<strong>CashlessConsumer</strong> &nbsp;·&nbsp; <span class="date">June 28, 2026</span>',
    "subtitle": "33+ unauthenticated API endpoints exposed 5,576 bank employees' credentials <span class='nowrap'>for over a year.</span>",
    "lead": "India's <tt>.bank.in</tt> was RBI's flagship anti-phishing initiative — a domain suffix meant to be a trust anchor citizens could rely on. Instead, the very portal that issues these banking domains leaked every credential it held.",
    "p1": "The IDRBT Domain Registration Portal (<tt>registrar.idrbt.ac.in</tt>) — the exclusive registrar for India's <tt>.bank.in</tt> banking namespace — exposed its entire REST API via <strong>33+ unauthenticated endpoints</strong>. Anyone with <tt>curl</tt> could retrieve the bcrypt password hashes, mobile numbers, email addresses, login IPs, and device fingerprints of all <strong>5,576 bank employees</strong> trusted with managing India's banking domains.",
    "p2": "The portal was built by <strong>IKCON Technologies</strong> without any public tender, in violation of IDRBT's own procurement handbook. IKCON employees held 22 accounts including 3 with global Super Admin access.",
    "callout_text": "The vulnerability was reported to CERT-In (Jun 8, 05:30 UTC) and confirmed fixed by IDRBT on <strong>June 25, 2026</strong>. The exposed endpoints are no longer accessible.",
    "eli5": "Think of <tt>.bank.in</tt> as a special padlock RBI put on every bank website so you know it's real. This investigation found that the padlock maker's own system was leaking all the keys — and the report explains how, why it matters, and what's still broken.",
    "h2_data": "Open Data",
    "h2_links": "Links",
    "dl_report": "📄 Download Full Report (PDF)",
    "dl_open": "📦 Open Data & Datasets",
    "ln_code": "💻 Source Code",
    "ln_audit": "🔍 Daily Audit Feed",
    "ln_archive": "📋 Evidence Archive",
    "about_title": "CashlessConsumer",
    "about_text": "A consumer collective that tracks the digital payments industry in India, producing awareness resources, technical analysis, open data, and policy inputs toward a fair cashless society. This investigation follows a consistent methodology: public records, OSINT, RTI, and responsible disclosure — no hacking, no stolen data, no adversarial techniques.",
    "about_ref": "Prior work: KillerLoanApps · BFIL Consent Scam · Fintech Governance RTI Program",
    "about_links": "cashlessconsumer.in · Newsletter · GitHub",
    "footer": "Published under responsible disclosure principles. © June 2026. Report by Srikanth L, CashlessConsumer.",
}

# Hindi
TR_HI = {
    "label": "हिन्दी",
    "trans_d": "⚠️ AI-generated translation. English original is authoritative.",
    "tag": "सुरक्षा जांच",
    "h1": "IDRBT .bank.in: Trust Anchor से Data Leak तक",
    "byline": '<strong>CashlessConsumer</strong> · <span class="date">28 जून 2026</span>',
    "subtitle": "33+ असुरक्षित API ने 5,576 बैंक कर्मचारियों के क्रेडेंशियल्स को एक वर्ष से अधिक समय तक उजागर किया",
    "lead": "भारत का <tt>.bank.in</tt> RBI का प्रमुख एंटी-फिशिंग प्रयास था — एक डोमेन सफिक्स जो नागरिकों के लिए विश्वास एंकर बनना था। इसके बजाय, इन बैंकिंग डोमेन को जारी करने वाला पोर्टल ही अपने सभी क्रेडेंशियल्स लीक कर रहा था।",
    "p1": "IDRBT डोमेन रजिस्ट्रेशन पोर्टल (<tt>registrar.idrbt.ac.in</tt>) — भारत के <tt>.bank.in</tt> बैंकिंग नेमस्पेस का एकमात्र रजिस्ट्रार — ने <strong>33+ अनऑथेंटिकेटेड एंडपॉइंट्स</strong> के माध्यम से अपनी पूरी REST API उजागर कर दी। <tt>curl</tt> वाला कोई भी व्यक्ति भारत के बैंकिंग डोमेन के प्रबंधन के लिए जिम्मेदार <strong>5,576 बैंक कर्मचारियों</strong> के bcrypt पासवर्ड हैश, मोबाइल नंबर, ईमेल पते और लॉगिन IP प्राप्त कर सकता था।",
    "p2": "पोर्टल <strong>IKCON Technologies</strong> द्वारा बिना किसी सार्वजनिक निविदा के बनाया गया, जो IDRBT की अपनी क्रय पुस्तिका का उल्लंघन है। IKCON के 22 कर्मचारी खाते थे जिनमें 3 ग्लोबल सुपर एडमिन एक्सेस वाले थे।",
    "callout_text": "कमजोरी की सूचना CERT-In को (8 जून, 05:30 UTC) दी गई और IDRBT द्वारा <strong>25 जून 2026</strong> को ठीक होने की पुष्टि की गई। उजागर एंडपॉइंट अब सुलभ नहीं हैं।",
    "eli5": "<tt>.bank.in</tt> को एक विशेष ताले की तरह समझें जो RBI ने हर बैंक वेबसाइट पर लगाया है ताकि आप जान सकें कि यह असली है। इस जांच में पाया गया कि ताले बनाने वाले की अपनी प्रणाली सभी चाबियाँ लीक कर रही थी — और रिपोर्ट बताती है कि कैसे, क्यों यह मायने रखता है, और अभी भी क्या टूटा हुआ है।",
    "h2_data": "खुला डेटा",
    "h2_links": "लिंक",
    "dl_report": "📄 पूरी रिपोर्ट डाउनलोड करें (PDF)",
    "dl_open": "📦 खुला डेटा और डेटासेट",
    "ln_code": "💻 स्रोत कोड",
    "ln_audit": "🔍 दैनिक ऑडिट फीड",
    "ln_archive": "📋 साक्ष्य संग्रह",
    "about_title": "CashlessConsumer",
    "about_text": "एक उपभोक्ता सामूहिक जो भारत में डिजिटल भुगतान उद्योग को ट्रैक करता है, जागरूकता संसाधन, तकनीकी विश्लेषण, खुला डेटा और नीति इनपुट तैयार करता है। यह जांच एक सुसंगत पद्धति का पालन करती है: सार्वजनिक रिकॉर्ड, OSINT, RTI और जिम्मेदार खुलासा — कोई हैकिंग नहीं, कोई चुराया डेटा नहीं।",
    "about_ref": "पूर्व कार्य: KillerLoanApps · BFIL Consent Scam · Fintech Governance RTI Program",
    "about_links": "cashlessconsumer.in · Newsletter · GitHub",
    "footer": "जिम्मेदार खुलासा सिद्धांतों के तहत प्रकाशित। © जून 2026। Srikanth L, CashlessConsumer द्वारा।",
}

# Tamil
TR_TA = {
    "label": "தமிழ்",
    "trans_d": "⚠️ AI உருவாக்கிய மொழிபெயர்ப்பு. ஆங்கில அசலே அதிகாரப்பூர்வமானது.",
    "tag": "பாதுகாப்பு ஆய்வு",
    "h1": "IDRBT .bank.in: Trust Anchor இருந்து Data Leak வரை",
    "byline": '<strong>CashlessConsumer</strong> · <span class="date">28 ஜூன் 2026</span>',
    "subtitle": "33+ அங்கீகாரமற்ற API எண்ட்பாயின்ட்கள் 5,576 வங்கி ஊழியர்களின் கிரெடென்ஷியல்களை ஒரு வருடத்திற்கும் மேலாக வெளிப்படுத்தின",
    "lead": "இந்தியாவின் <tt>.bank.in</tt> என்பது RBIயின் முதன்மையான எதிர்ப்பு ஃபிஷிங் முயற்சியாகும் — குடிமக்கள் நம்பக்கூடிய ஒரு நம்பிக்கை நங்கூரமாக இருக்க வேண்டிய டொமைன் பின்னொட்டு. அதற்கு பதிலாக, இந்த வங்கி டொமைன்களை வழங்கும் போர்டலே தான் வைத்திருந்த ஒவ்வொரு கிரெடென்ஷியலையும் கசியவிட்டது.",
    "p1": "IDRBT டொமைன் பதிவு போர்டல் (<tt>registrar.idrbt.ac.in</tt>) — இந்தியாவின் <tt>.bank.in</tt> வங்கி நேம்ஸ்பேஸின் பிரத்யேக பதிவாளர் — <strong>33+ அங்கீகாரமற்ற எண்ட்பாயின்ட்கள்</strong> மூலம் அதன் முழு REST API ஐ வெளிப்படுத்தியது. <tt>curl</tt> உள்ள எவரும் இந்தியாவின் வங்கி டொமைன்களை நிர்வகிக்கும் <strong>5,576 வங்கி ஊழியர்களின்</strong> bcrypt கடவுச்சொல் ஹாஷ்கள், மொபைல் எண்கள், மின்னஞ்சல் முகவரிகள் மற்றும் உள்நுழைவு IPகளைப் பெற முடிந்தது.",
    "p2": "இந்த போர்ட்டல் <strong>IKCON டெக்னாலஜிஸ்</strong> நிறுவனத்தால் எந்த பொது டெண்டரும் இன்றி உருவாக்கப்பட்டது, IDRBT இன் சொந்த கொள்முதல் கையேட்டை மீறி. IKCON ஊழியர்களுக்கு 22 கணக்குகள் இருந்தன, அவற்றில் 3 உலகளாவிய சூப்பர் அட்மின் அணுகலுடன்.",
    "callout_text": "இந்த பாதிப்பு CERT-In க்கு (ஜூன் 8, 05:30 UTC) தெரிவிக்கப்பட்டது, மேலும் IDRBT ஆல் <strong>ஜூன் 25, 2026</strong> அன்று சரி செய்யப்பட்டது. வெளிப்பட்ட எண்ட்பாயின்ட்கள் இனி அணுக முடியாது.",
    "eli5": "<tt>.bank.in</tt> என்பது RBI ஒவ்வொரு வங்கி இணையதளத்திலும் பொருத்திய ஒரு சிறப்பு பூட்டு போன்றது — நீங்கள் உண்மையான தளத்தில்தான் இருக்கிறீர்கள் என்பதை உறுதிப்படுத்த. இந்த விசாரணை கண்டுபிடித்தது: அந்த பூட்டை தயாரிக்கும் நிறுவனத்தின் சொந்த அமைப்பே அனைத்து சாவிகளையும் கசியவிட்டுக்கொண்டிருந்தது — எப்படி, ஏன் இது முக்கியமானது, இன்னும் என்ன உடைந்துள்ளது என்பதை அறிக்கை விளக்குகிறது.",
    "h2_data": "திறந்த தரவு",
    "h2_links": "இணைப்புகள்",
    "dl_report": "📄 முழு அறிக்கையைப் பதிவிறக்கவும் (PDF)",
    "dl_open": "📦 திறந்த தரவு மற்றும் தரவுத்தொகுப்புகள்",
    "ln_code": "💻 மூலக் குறியீடு",
    "ln_audit": "🔍 தினசரி தணிக்கை ஊட்டம்",
    "ln_archive": "📋 ஆதார சேகரிப்பு",
    "about_title": "CashlessConsumer",
    "about_text": "இந்தியாவில் டிஜிட்டல் கட்டணத் துறையைக் கண்காணிக்கும் ஒரு நுகர்வோர் குழுமம், விழிப்புணர்வு ஆதாரங்கள், தொழில்நுட்ப பகுப்பாய்வு, திறந்த தரவு மற்றும் கொள்கை உள்ளீடுகளை உருவாக்குகிறது. இந்த விசாரணை ஒரு நிலையான வழிமுறையைப் பின்பற்றுகிறது: பொது பதிவுகள், OSINT, RTI மற்றும் பொறுப்பான வெளிப்படுத்தல் — ஹேக்கிங் இல்லை, திருடப்பட்ட தரவு இல்லை.",
    "about_ref": "முந்தைய பணி: KillerLoanApps · BFIL Consent Scam · Fintech Governance RTI Program",
    "about_links": "cashlessconsumer.in · Newsletter · GitHub",
    "footer": "பொறுப்பான வெளிப்படுத்தல் கொள்கைகளின் கீழ் வெளியிடப்பட்டது. © ஜூன் 2026. Srikanth L, CashlessConsumer ஆல் அறிக்கை.",
}

ALL_LANGS = {
    "en": TR_EN,
    "hi": TR_HI,
    "ta": TR_TA,
    "bn": {"label": "বাংলা", **{k: "…" for k in TR_EN}},
    "mr": {"label": "मराठी", **{k: "…" for k in TR_EN}},
    "te": {"label": "తెలుగు", **{k: "…" for k in TR_EN}},
    "gu": {"label": "ગુજરાતી", **{k: "…" for k in TR_EN}},
    "ur": {"label": "اردو", **{k: "…" for k in TR_EN}},
    "kn": {"label": "ಕನ್ನಡ", **{k: "…" for k in TR_EN}},
}

for code in ["bn", "mr", "te", "gu", "ur", "kn"]:
    ALL_LANGS[code]["trans_d"] = "⚠️ AI-generated translation. English original is authoritative."

LANG_BUTTONS = "".join(
    f'<button class="lang-btn{" lang-active" if c=="en" else ""}" id="lang-{c}" onclick="setLang(\'{c}\')">{ALL_LANGS[c]["label"]}</button>'
    for c in ["en", "hi", "ta", "bn", "mr", "te", "gu", "ur", "kn"]
)

TR_JS = "const TR = " + json.dumps(ALL_LANGS, ensure_ascii=False) + ";"

DATA_TABLE = """\
<table class="data-table">
<tr><th>Dataset</th><th>Records</th><th>Published</th></tr>
<tr><td>Registered .bank.in domains</td><td>1,497</td><td class="yes">Yes</td></tr>
<tr><td>Domains with active NS</td><td>1,402</td><td class="yes">Yes</td></tr>
<tr><td>Domains without NS (unpublished to NIXI)</td><td>95</td><td class="yes">Yes</td></tr>
<tr><td>Billing records (anonymized)</td><td>1,535</td><td class="yes">Yes</td></tr>
<tr><td>Certificate Transparency log entries</td><td>3,797</td><td class="yes">Yes</td></tr>
<tr><td>User records (original leak)</td><td>5,461</td><td class="no">No — contains PII/hashes</td></tr>
<tr><td>Orphan user records</td><td>1,072</td><td class="no">No — contains PII/hashes</td></tr>
</table>"""

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>IDRBT .bank.in Security Investigation — CashlessConsumer</title>
<meta name="description" content="33+ unauthenticated API endpoints on the IDRBT Domain Registration Portal exposed bcrypt password hashes for 5,576 bank employees." />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔐</text></svg>" />
<style>
/* ── Reset & Base ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#fafafa;color:#222;line-height:1.6;font-size:16px}
a{color:#b00;text-decoration:none}
a:hover{text-decoration:underline}
tt,code,pre{font-family:Menlo,Consolas,monospace;font-size:.85em}

/* ── Language bar ── */
.lang-bar{background:#fff;border-bottom:1px solid #e0e0e0;padding:8px 0;text-align:center;position:sticky;top:0;z-index:10}
.lang-bar .inner{max-width:720px;margin:0 auto;padding:0 16px}
.lang-bar strong{font-size:.75rem;color:#888;margin-right:6px}
.lang-btn{font-size:.74rem;border:1px solid #ddd;background:#fff;color:#666;padding:2px 8px;border-radius:3px;cursor:pointer;margin:2px}
.lang-btn:hover{border-color:#b00;color:#b00}
.lang-active{background:#b00;color:#fff;border-color:#b00;font-weight:600}
.trans-banner{background:#fff3cd;border-bottom:1px solid #ffc107;text-align:center;font-size:.75rem;padding:4px 16px;color:#856404;display:none}

/* ── Layout ── */
.container{max-width:680px;margin:0 auto;padding:0 20px}

/* ── Hero ── */
.hero{padding:48px 0 24px;text-align:center}
.hero .tag{display:inline-block;background:#b00;color:#fff;font-size:.7rem;font-weight:600;padding:3px 10px;border-radius:3px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:16px}
.hero h1{font-size:1.5rem;font-weight:700;line-height:1.3;margin-bottom:10px;letter-spacing:-.01em}
.hero .byline{color:#888;font-size:.82rem}

/* ── Body ── */
section{padding:24px 0}
section p{color:#444;margin-bottom:16px;font-size:.95rem}
section p strong{color:#b00}

/* ── Callout ── */
.callout{background:#fafafa;border-left:3px solid #b00;padding:16px 20px;margin:20px 0;border-radius:0 6px 6px 0;font-size:.92rem;color:#444}

/* ── Data table ── */
.data-table{width:100%;border-collapse:collapse;font-size:.84rem;margin:12px 0}
.data-table th,.data-table td{text-align:left;padding:6px 8px;border-bottom:1px solid #eee}
.data-table th{color:#888;font-weight:500;font-size:.74rem;text-transform:uppercase;letter-spacing:.03em}
.data-table td{color:#444}
.data-table .yes{color:#080}
.data-table .no{color:#b00}

/* ── Download / Links ── */
.dl-strip{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;padding:16px 0}
.dl-strip a{font-size:.9rem;background:#fff;border:1px solid #ddd;border-radius:5px;padding:10px 18px;color:#333;display:inline-flex;align-items:center;gap:6px;transition:all .15s}
.dl-strip a:hover{border-color:#b00;text-decoration:none}
.dl-primary{background:#b00!important;color:#fff!important;border-color:#b00!important;font-weight:600}

/* ── Small links row ── */
.links-row{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;padding:8px 0 20px;font-size:.85rem}
.links-row a{color:#666}
.links-row a:hover{color:#b00;text-decoration:none}

/* ── About ── */
.about-box{background:#fff;border:1px solid #eee;border-radius:6px;padding:20px;margin:20px 0;font-size:.88rem}
.about-box h3{font-size:.95rem;font-weight:600;margin-bottom:4px}
.about-box p{color:#666;margin-bottom:6px;font-size:.88rem}
.about-box .ref{color:#999;font-size:.8rem}

/* ── Footer ── */
footer{padding:32px 0;text-align:center;color:#bbb;font-size:.75rem}

@media(max-width:520px){
  .hero h1{font-size:1.25rem}
  .dl-strip a{width:100%;justify-content:center}
}
</style>
</head>
<body>

<!-- Language bar -->
<div class="lang-bar"><div class="inner"><strong>Language:</strong> """ + LANG_BUTTONS + r"""</div></div>
<div class="trans-banner" id="trans-banner">⚠️ AI-generated translation. English original is authoritative.</div>

<!-- Hero -->
<div class="container hero">
<div class="tag" data-i18n="tag">Security Investigation</div>
<h1 data-i18n="h1">IDRBT .bank.in: From Trust Anchor to Data Leak</h1>
<div class="byline" data-i18n="byline"><strong>CashlessConsumer</strong> &nbsp;·&nbsp; <span class="date">June 28, 2026</span></div>
</div>

<div class="container">

<!-- Summary -->
<section>
<p data-i18n="lead">India's <tt>.bank.in</tt> was RBI's flagship anti-phishing initiative — a domain suffix meant to be a trust anchor citizens could rely on. Instead, the very portal that issues these banking domains leaked every credential it held.</p>
<p data-i18n="p1">The IDRBT Domain Registration Portal (<tt>registrar.idrbt.ac.in</tt>) — the exclusive registrar for India&rsquo;s <tt>.bank.in</tt> banking namespace — exposed its entire REST API via <strong>33+ unauthenticated endpoints</strong>. Anyone with <tt>curl</tt> could retrieve the bcrypt password hashes, mobile numbers, email addresses, login IPs, and device fingerprints of all <strong>5,576 bank employees</strong> trusted with managing India&rsquo;s banking domains.</p>
<p data-i18n="p2">The portal was built by <strong>IKCON Technologies</strong> without any public tender, in violation of IDRBT&rsquo;s own procurement handbook. IKCON employees held 22 accounts including 3 with global Super Admin access.</p>

<p data-i18n="eli5">Think of <tt>.bank.in</tt> as a special padlock RBI put on every bank website so you know it's real. This investigation found that the padlock maker's own system was leaking all the keys — and the report explains how, why it matters, and what's still broken.</p>

<div class="callout" data-i18n="callout_text">The vulnerability was reported to CERT-In (Jun 8, 05:30 UTC) and confirmed fixed by IDRBT on <strong>June 25, 2026</strong>. The exposed endpoints are no longer accessible.</div>
</section>

<!-- Download -->
<div class="dl-strip">
<a href="report.pdf" class="dl-primary" data-i18n="dl_report">📄 Download Full Report (PDF)</a>
<a href="open-data/" data-i18n="dl_open">📦 Open Data &amp; Datasets</a>
</div>

<!-- Data table -->
<section>
<h2 data-i18n="h2_data">Open Data</h2>
""" + DATA_TABLE + r"""
<p style="font-size:.82rem;color:#888;margin-top:4px">Data feeds into the <a href="https://github.com/CCAgentOrg/bank-in-domains">bank-in-domains</a> daily audit (CT logs, Wayback Machine, urlscan.io at 02:30 UTC).</p>
</section>

<!-- Links -->
<div class="links-row" data-i18n="h2_links">
<a href="https://github.com/CCAgentOrg/idrbt-bankin-investigation" data-i18n="ln_code">💻 Source Code</a>
<a href="https://github.com/CCAgentOrg/bank-in-domains" data-i18n="ln_audit">🔍 Daily Audit Feed</a>
<a href="https://zo.pub/cashlessconsumer/idrbt-bankin-security" data-i18n="ln_archive">📋 Evidence Archive</a>
</div>

<!-- About -->
<div class="about-box">
<h3 data-i18n="about_title">CashlessConsumer</h3>
<p data-i18n="about_text">A consumer collective that tracks the digital payments industry in India, producing awareness resources, technical analysis, open data, and policy inputs toward a fair cashless society.</p>
<div class="ref">
<span data-i18n="about_ref">Prior work: KillerLoanApps · BFIL Consent Scam · Fintech Governance RTI Program</span><br/>
<a href="https://cashlessconsumer.in" data-i18n="about_links">cashlessconsumer.in · Newsletter · GitHub</a>
</div>
</div>

</div>

<footer class="container">
<p data-i18n="footer">Published under responsible disclosure principles. © June 2026. Report by Srikanth L, CashlessConsumer.</p>
</footer>

<script>
""" + TR_JS + r"""
let currentLang = 'en';
const banner = document.getElementById('trans-banner');
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
  if (code === 'en') {
    banner.style.display = 'none';
  } else {
    banner.style.display = 'block';
  }
}
</script>
</body>
</html>"""

# ── Write ──────────────────────────────────────────────────────
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Site generated: {os.path.join(OUT, 'index.html')} ({os.path.getsize(os.path.join(OUT, 'index.html'))} bytes)")
