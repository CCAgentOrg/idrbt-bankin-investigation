#!/usr/bin/env python3
"""Translate missing sections for multiple languages in gen_site.py."""
import requests, json, os, re, sys

API = "https://api.zo.computer/zo/ask"
MODEL = "byok:b5700bd6-fca9-4aa2-9d31-bc9f5bb33bbc"
HEADERS = {"authorization": os.environ["ZO_CLIENT_IDENTITY_TOKEN"], "content-type": "application/json"}
FILE = "/home/workspace/idrbt-bankin-investigation/gen_site.py"

# ── English reference texts for the 17 missing keys ──
EN_TEXTS = {
    "p3": "The vulnerability was reported to CERT-In on June 8 and confirmed fixed by IDRBT on June 25. But the deeper accountability questions remain: Who at RBI and IDRBT is responsible for a national security infrastructure built without process, oversight, or a single external security review? Why did no one — not IDRBT's own VAPT contractor, not the internal team — notice that the entire user database was publicly readable for over a year?",
    "h2_scenarios": "What a Bad Actor Could Have Done",
    "scenario1": "Imagine you're a fraudster with <tt>curl</tt>. You download <strong>5,576 user records</strong> — names, email addresses, mobile numbers, the exact bank each person works for. You now have a precision-targeted list for spear-phishing: \"Dear SBI branch manager, your .bank.in domain registration is expiring. Click here to renew.\" These emails look legitimate because they contain internal details only the real IDRBT portal should know. <strong>One compromised credential</strong> — one employee who clicks — gives you authenticated portal access. You're inside India's banking domain registry.",
    "scenario2": "Inside, you find <strong>1,072 orphan Super Admin accounts</strong> — accounts with no organization attached, meaning they can modify any bank's domain settings. Their bcrypt password hashes are sitting in the data you already downloaded. Password <tt>password123</tt>? Cracked in seconds. You change the DNS A record for <tt>sirsadccb.bank.in</tt> — a real cooperative bank — from its legitimate server to a phishing site on a cheap overseas host. Let's Encrypt gives you a free SSL certificate. The customer's browser shows a green padlock next to the fake site. They enter their username, password, OTP. You drain their account. <strong>They have no way to know</strong> — every visible signal (the <tt>.bank.in</tt> domain, the padlock, the familiar layout) tells them this is legitimate.",
    "scenario3": "None of these scenarios required a zero-day, a firewall bypass, or exploit code. Only <tt>curl</tt> against 33 open endpoints. The sole reason they did not materialize is that CashlessConsumer found the vulnerability first and reported it responsibly — before any malicious actor did.",
    "data_footnote": "Data feeds into the <a href=\"https://github.com/CCAgentOrg/bank-in-domains\">bank-in-domains</a> daily audit (CT logs, Wayback Machine, urlscan.io at 02:30 UTC). PII and credential hashes are never published — only domain names and metadata that were already publicly accessible.",
    "h2_claims": "Security Claims vs Reality",
    "claims_intro": 'IDRBT\'s published <a href="https://registrar.idrbt.ac.in/assets/files/privacy%20policy.pdf">Privacy &amp; Security Policy</a> makes specific claims about security auditing, authentication, and data protection for the Domain Registration Portal. Our investigation found every one of these claims to be false.',
    "claims_caption": "Left: What IDRBT's Security Policy claimed. Right: What our investigation found.",
    "h3_claim1": '❌ Claim #1: "Audited for vulnerabilities before launch — all addressed"',
    "claims_text1": 'The Security Policy claims: <em>"The website was audited for known application-level vulnerabilities before the launch, and all the known vulnerability was addressed."</em> Our investigation found <strong>33+ unauthenticated API endpoints</strong> that exposed the entire user database, billing records, system configuration, and DSC proxy — a comprehensive failure that no competent security audit could have missed. The portal also had <strong>no vulnerability disclosure program (security.txt)</strong>, making it impossible for researchers to report issues through official channels.',
    "h3_claim2": '❌ Claim #2: "Content is authenticated"',
    "claims_text2": 'The policy states: <em>"Content is authenticated and is provided for general information."</em> Accessing every discovered endpoint required <strong>zero authentication</strong> — no login, no API key, no session cookie, no token. Anyone with <tt>curl</tt> could download the entire user database. The only thing protecting India\'s banking domain registry was security through obscurity.',
    "h3_claim3": '❌ Claim #3: "Procedural safeguards that comply with applicable laws"',
    "claims_text3": 'The policy pledges: <em>"We protect your personal information by maintaining physical, electronic, and procedural safeguards that comply with applicable laws."</em> Exposing bcrypt password hashes, phone numbers, and device fingerprints of 5,576 bank employees without authentication violates every principle of data protection under the Digital Personal Data Protection Act, 2023, and RBI\'s own cybersecurity framework (RBI/2023-24/90).',
    "claims_callout": '<strong>Bottom line:</strong> IDRBT\'s published security policy is a work of fiction. It claims the site was audited for vulnerabilities but 33+ endpoints were wide open. It claims content is authenticated but no endpoint required a login. It claims procedural safeguards but the portal violated India\'s data protection law and RBI\'s own cyber framework.',
    "ln_llms": "🤖 LLMs.txt",
}

def get_translations(lang_code, lang_name):
    """Translate a single language's missing keys."""
    prompt = f"""You are a professional Indian language translator. Translate the following English text into {lang_name} ({lang_code}).

Return ONLY valid JSON in this exact format:
{{"<key>": "<translated_text>", ...}}

CRITICAL: Preserve ALL HTML tags exactly as-is (<em>, <strong>, <tt>, <a href=...>, etc.). Translate only the visible text content.
CRITICAL: Do NOT change or re-write the key names. Use the exact English key names provided below.

English text to translate:
{json.dumps(EN_TEXTS, indent=2, ensure_ascii=False)}"""

    r = requests.post(API, headers=HEADERS, json={
        "input": prompt, "model_name": MODEL
    }, timeout=300)
    
    resp = r.json()
    output_str = resp.get("output", "")
    if not output_str:
        print(f"  ✗ Empty response. Full: {json.dumps(resp)[:300]}")
        return {}
    
    # The model may wrap in ```json ... ``` or just raw JSON
    output_str = output_str.strip()
    if output_str.startswith("```"):
        lines = output_str.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        output_str = "\n".join(lines).strip()
    
    try:
        result = json.loads(output_str)
        return result
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parse error: {e}")
        print(f"  Response preview: {output_str[:300]}")
        return {}

def update_file(lang_code, translations):
    """Update gen_site.py with translations. Must handle \\
-> just " in Regular Python strings too (not raw strings)."""
    with open(FILE, 'r') as f:
        content = f.read()
    
    changes = 0
    for key, value in translations.items():
        if not value or value == "…":
            continue
        # JSON-encode the value to properly escape it for Python source
        encoded = json.dumps(value, ensure_ascii=False)
        # The file stores keys as: "key": "…"
        # Replace with: "key": "translated"
        old = f'"{key}": "…"'
        new = f'"{key}": {encoded}'
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            changes += count
            print(f"  ✓ {key}: replaced ({count} occurrence{'s' if count > 1 else ''})")
    
    if changes == 0:
        print(f"  ⚠ No changes made for '{lang_code}'")
        return False
    
    with open(FILE, 'w') as f:
        f.write(content)
    print(f"  → {changes} total replacement{'s' if changes > 1 else ''}")
    return True

# ── Define the 17 keys to translate ──
MISSING_KEYS = ["p3", "h2_scenarios", "scenario1", "scenario2", "scenario3", "data_footnote",
                "h2_claims", "claims_intro", "claims_caption", "h3_claim1", "claims_text1",
                "h3_claim2", "claims_text2", "h3_claim3", "claims_text3", "claims_callout", "ln_llms"]

LANGS = [
    ("hi", "HINDI (हिन्दी)"),
    ("ta", "TAMIL (தமிழ்)"),
    ("mr", "MARATHI (मराठी)"),
    ("te", "TELUGU (తెలుగు)"),
    ("gu", "GUJARATI (ગુજરાતી)"),
    ("ur", "URDU (اردو)"),
    ("kn", "KANNADA (ಕನ್ನಡ)"),
    ("bn", "BENGALI (বাংলা)"),
]

# ── Execute ──
total = len(LANGS)
for i, (code, name) in enumerate(LANGS, 1):
    print(f"\n[{i}/{total}] {code} ({name})...")
    sys.stdout.flush()
    
    result = get_translations(code, name)
    
    if code in result:
        if update_file(code, result):
            print(f"  ✓ {code}: Applied {len(MISSING_KEYS)} translations")
        else:
            print(f"  ✗ {code}: Failed to apply translations")
    else:
        print(f"  ✗ {code}: Language '{code}' not found in response. Keys: {list(result.keys())}")
    
    sys.stdout.flush()
