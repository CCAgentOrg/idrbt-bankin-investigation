#!/usr/bin/env python3
"""Translate all stub languages in gen_site.py using Zo's /zo/ask API.
Generates TR dicts for bn, mr, te, gu, ur, kn."""
import json, os, re, requests, sys, asyncio, aiohttp

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(REPO, "gen_site.py")

# ── English source keys ────────────────────────────────────────
EN_SRC = {
    "label": "",  # placeholder, set per language
    "trans_d": "⚠️ AI-generated translation. English original is authoritative.",
    "tag": "Security Investigation",
    "h1": "IDRBT .bank.in: From Trust Anchor to Data Leak",
    "byline": "<strong>CashlessConsumer</strong> · <span class=\"date\">28 ಜೂನ್ 2026</span>",  # per-language date fmt
    "subtitle": "33+ unauthenticated API endpoints exposed 5,576 bank employees' credentials for over a year.",
    "lead": "India's .bank.in was RBI's flagship anti-phishing initiative — a domain suffix meant to be a trust anchor citizens could rely on. Instead, the very portal that issues these banking domains leaked every credential it held.",
    "p1": "The IDRBT Domain Registration Portal (registrar.idrbt.ac.in) — the exclusive registrar for India's .bank.in banking namespace — exposed its entire REST API via 33+ unauthenticated endpoints. Anyone with curl could retrieve the bcrypt password hashes, mobile numbers, email addresses, login IPs, and device fingerprints of all 5,576 bank employees trusted with managing India's banking domains.",
    "p2": "The portal was built by IKCON Technologies without any public tender, in violation of IDRBT's own procurement handbook. IKCON employees held 22 accounts including 3 with global Super Admin access.",
    "callout_text": "The vulnerability was reported to CERT-In (Jun 8, 05:30 UTC) and confirmed fixed by IDRBT on June 25, 2026. The exposed endpoints are no longer accessible.",
    "eli5": "Think of .bank.in as a special padlock RBI put on every bank website so you know it's real. This investigation found that the padlock maker's own system was leaking all the keys — and the report explains how, why it matters, and what's still broken.",
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

LANGUAGES = {
    "bn": {"label": "বাংলা", "byline_date": "28 জুন 2026"},
    "mr": {"label": "मराठी", "byline_date": "२८ जून २०२६"},
    "te": {"label": "తెలుగు", "byline_date": "28 జూన్ 2026"},
    "gu": {"label": "ગુજરાતી", "byline_date": "28 જૂન 2026"},
    "ur": {"label": "اردو", "byline_date": "28 جون 2026"},
    "kn": {"label": "ಕನ್ನಡ", "byline_date": "28 ಜೂನ್ 2026"},
}

MODEL = "byok:b5700bd6-fca9-4aa2-9d31-bc9f5bb33bbc"
AUTH_TOKEN = os.environ.get("ZO_CLIENT_IDENTITY_TOKEN", "")

# Keys that need HTML/emoji preserved
KEYS_RAW_HTML = {"byline", "dl_report", "dl_open", "ln_code", "ln_audit", "ln_archive"}

def make_prompt(code, meta, src):
    name = meta["label"]
    return f"""Translate the following English text into {name} ({code}). Return ONLY a raw JSON object with these exact keys, no markdown, no backticks.

Rules:
- Keep all HTML tags like <strong>, <tt>, <span> exactly as-is, only translate the surrounding text
- Keep all emojis (📄, 📦, 💻, 🔍, 📋) exactly as-is  
- For "byline": keep the HTML structure, replace "June 28, 2026" with "{meta['byline_date']}" and "CashlessConsumer" with the transliterated form
- For "h1": keep "IDRBT .bank.in:" untranslated, translate only the rest
- For "tag": translate "Security Investigation" naturally
- For "subtitle": keep numbers and <span class='nowrap'> tags intact
- For "lead", "p1", "p2", "callout_text", "eli5": translate naturally, keep .bank.in and technical terms like bcrypt, API, REST, curl, CERT-In, IDRBT, IKCON, RBI, DNSSEC, DMARC, HSTS untranslated
- Keep <tt>.bank.in</tt> in lead, eli5, p1 where they appear (use backtick-escaped HTML)
- For "about_text": translate naturally, keep methodology terms like OSINT, RTI
- For "about_ref": keep product names untranslated  
- For "about_links": keep URLs untranslated
- For "footer": translate naturally, keep name "Srikanth L" and "CashlessConsumer"

Source JSON:
{json.dumps(src, ensure_ascii=False, indent=2)}"""

async def translate_lang(session, code, meta):
    prompt = make_prompt(code, meta, EN_SRC)
    async with session.post(
        "https://api.zo.computer/zo/ask",
        headers={
            "authorization": AUTH_TOKEN,
            "content-type": "application/json"
        },
        json={"input": prompt, "model_name": MODEL}
    ) as resp:
        result = await resp.json()
        output = result.get("output", "")
        # Try to find JSON in the response
        try:
            # First try direct parse
            data = json.loads(output.strip())
        except json.JSONDecodeError:
            # Try to extract JSON from markdown
            m = re.search(r'\{[^{]*"tag"[^}]+"footer"[^}]*\}', output, re.DOTALL)
            if m:
                data = json.loads(m.group())
            else:
                print(f"  ⚠️  Failed to parse response for {code}, using stub")
                return code, None
        
        # Ensure all required keys
        for k in EN_SRC:
            if k not in data or not data[k]:
                print(f"  ⚠️  Missing key '{k}' in {code}, filling with stub")
                data[k] = "…"
        
        data["trans_d"] = "⚠️ AI-generated translation. English original is authoritative."
        data["label"] = meta["label"]
        # Ensure byline has the right date format
        if "byline" in data:
            data["byline"] = data["byline"].replace("June 28, 2026", meta["byline_date"])
        return code, data

async def main():
    """Main async entrypoint."""
    print(f"Translating {len(LANGUAGES)} language(s) via Zo API...\n")
    async with aiohttp.ClientSession() as session:
        tasks = [translate_lang(session, code, meta) for code, meta in LANGUAGES.items()]
        results = await asyncio.gather(*tasks)
    
    translations = {}
    for code, data in results:
        if data:
            translations[code] = data
            print(f"  ✅ {code} ({LANGUAGES[code]['label']}) — {len(data)} keys")
        else:
            print(f"  ❌ {code} — failed")
    
    if len(translations) < len(LANGUAGES):
        print("\n⚠️  Some translations failed, will only patch successful ones")
    
    # ── Patch gen_site.py ────────────────────────────────────────
    with open(GEN) as f:
        code = f.read()
    
    # Build new ALL_LANGS
    tr_lines = []
    tr_lines.append('    "en": TR_EN,')
    tr_lines.append('    "hi": TR_HI,')
    tr_lines.append('    "ta": TR_TA,')
    for c, d in translations.items():
        tr_lines.append(f'    "{c}": {json.dumps(d, ensure_ascii=False)},')
    
    tr_js = "ALL_LANGS = {\n" + "\n".join(tr_lines) + "\n}"
    
    # Find and replace ALL_LANGS section
    pattern = r'ALL_LANGS = \{.*?\n\}'
    if re.search(pattern, code, re.DOTALL):
        code = re.sub(pattern, tr_js, code, flags=re.DOTALL)
        with open(GEN, 'w') as f:
            f.write(code)
        print(f"\n✅ Patched {len(translations)} language(s) into gen_site.py")
    else:
        print("\n⚠️  Could not find ALL_LANGS in gen_site.py — manual patch needed")
        print("Generated translations written below:")
        for c, d in translations.items():
            print(f"\n# {c}")
            print(json.dumps({c: d}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
