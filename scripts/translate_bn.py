#!/usr/bin/env python3
"""Translate Bengali (bn) stub in gen_site.py via Zo API."""
import asyncio, aiohttp, json, os, re

GEN = "/home/workspace/idrbt-bankin-investigation/gen_site.py"
MODEL = "byok:b5700bd6-fca9-4aa2-9d31-bc9f5bb33bbc"
CODE = "bn"
LANG = "বাংলা"
LOCALE_DATE = "২৮ জুন ২০২৬"

EN_KEYS = {
    "tag": "Security Investigation",
    "h1": "IDRBT .bank.in: From Trust Anchor to Data Leak",
    "subtitle": "33+ unauthenticated API endpoints exposed 5,576 bank employees' credentials for over a year.",
    "lead": "India's .bank.in was RBI's flagship anti-phishing initiative — a domain suffix meant to be a trust anchor citizens could rely on. Instead, the very portal that issues these banking domains leaked every credential it held.",
    "p1": "The IDRBT Domain Registration Portal (registrar.idrbt.ac.in) — the exclusive registrar for India's .bank.in banking namespace — exposed its entire REST API via 33+ unauthenticated endpoints. Anyone with curl could retrieve the bcrypt password hashes, mobile numbers, email addresses, login IPs, and device fingerprints of all 5,576 bank employees trusted with managing India's banking domains.",
    "p2": "The portal was built by IKCON Technologies without any public tender, in violation of IDRBT's own procurement handbook. IKCON employees held 22 accounts including 3 with global Super Admin access.",
    "callout_text": "The vulnerability was reported to CERT-In (Jun 8, 05:30 UTC) and confirmed fixed by IDRBT on June 25, 2026. The exposed endpoints are no longer accessible.",
    "eli5": "Think of .bank.in as a special padlock RBI put on every bank website so you know it's real. This investigation found that the padlock maker's own system was leaking all the keys — and the report explains how, why it matters, and what's still broken.",
    "h2_data": "Open Data",
    "h2_links": "Links",
    "dl_report": "Download Full Report (PDF)",
    "dl_open": "Open Data & Datasets",
    "ln_code": "Source Code",
    "ln_audit": "Daily Audit Feed",
    "ln_archive": "Evidence Archive",
    "about_title": "CashlessConsumer",
    "about_text": "A consumer collective that tracks the digital payments industry in India, producing awareness resources, technical analysis, open data, and policy inputs toward a fair cashless society. This investigation follows a consistent methodology: public records, OSINT, RTI, and responsible disclosure — no hacking, no stolen data, no adversarial techniques.",
    "about_ref": "Prior work: KillerLoanApps · BFIL Consent Scam · Fintech Governance RTI Program",
    "about_links": "cashlessconsumer.in · Newsletter · GitHub",
    "footer": "Published under responsible disclosure principles. © June 2026. Report by Srikanth L, CashlessConsumer.",
}

def extract_json(text):
    """Extract JSON from model response that may include markdown fences."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r'```(?:json)?\s*\n(.+?)\n```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    m = re.search(r'(\{.*\})', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not extract JSON from response")

async def main():
    print(f"Translating {LANG}...")
    prompt = f"""Translate these i18n keys to {LANG} (language code: {CODE}).
- Keep {CODE} script (Bengali script) for all translated text.
- Translate all text including the padlock metaphor ("special padlock", "leaking all the keys")
- Preserve proper nouns like "RBI", "IDRBT", "IKCON Technologies", "CERT-In", "CashlessConsumer", "KillerLoanApps", "BFIL Consent Scam"
- Keep the future date and copyright as: "{LOCALE_DATE}" and in Bengali format
- Return ONLY a valid JSON object with these exact keys and their Bengali translations

{json.dumps(EN_KEYS, ensure_ascii=False, indent=2)}"""

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.zo.computer/zo/ask",
            headers={
                "authorization": os.environ["ZO_CLIENT_IDENTITY_TOKEN"],
                "content-type": "application/json"
            },
            json={"input": prompt, "model_name": MODEL},
            timeout=aiohttp.ClientTimeout(total=120)
        ) as resp:
            result = await resp.json()
            output = result.get("output", "")

    translated = extract_json(output)
    translated["label"] = LANG
    translated["byline"] = f'<strong>CashlessConsumer</strong> · <span class="date">{LOCALE_DATE}</span>'
    translated["trans_d"] = "⚠️ AI-উৎপাদিত অনুবাদ। ইংরেজি মূল সংস্করণই প্রামাণিক।"

    # Patch into gen_site.py
    content = open(GEN).read()
    start = content.index(f'"{CODE}": {{')
    # Find where this language block ends (next "" or end of ALL_LANGS)
    end = content.index("}", start)
    # Scan forward to find the proper end - the closing } followed by ,\n    " or }\n}
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1

    trans_json = json.dumps(translated, ensure_ascii=False, indent=4)
    indented = "\n".join("    " + line for line in trans_json.split("\n"))
    replacement = indented
    # Check if there should be a trailing comma
    after = content[end:].strip()
    if after.startswith(","):
        replacement += ","
        end += after.index(",") + 1

    new_content = content[:start] + replacement + "\n" + content[end:]
    open(GEN, "w").write(new_content)
    print(f"✅ {LANG} — {len(translated)} keys patched")

asyncio.run(main())
