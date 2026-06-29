#!/usr/bin/env python3
"""Add missing keys to ALL_LANGS non-English entries in gen_site.py"""
import re

FILE = "/home/workspace/idrbt-bankin-investigation/gen_site.py"

with open(FILE) as f:
    content = f.read()

MISSING = ["h2_timeline", "timeline_intro", "ln_llms"]
ADD_AFTER = 'ALL_LANGS[code]["trans_d"] = "⚠️ AI-generated translation. English original is authoritative."'

insertion = """
# Fill missing keys in non-English languages
MISSING = ["h2_timeline", "timeline_intro", "ln_llms"]
for code in ["hi", "ta", "bn", "mr", "te", "gu", "ur", "kn", "ml"]:
    for key in MISSING:
        if key not in ALL_LANGS[code]:
            ALL_LANGS[code][key] = "\\u2026"
"""

new_content = content.replace(ADD_AFTER, ADD_AFTER + insertion)

if new_content == content:
    print("ERROR: Pattern not found")
else:
    with open(FILE, "w") as f:
        f.write(new_content)
    print("OK: Added missing key filler to gen_site.py")
