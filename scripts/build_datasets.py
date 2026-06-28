#!/usr/bin/env python3
# Build open datasets from IDRBT triangulation report
import re, json, csv, shutil, os

REPORT = "/home/workspace/IDRBT/triangulation/triangulation_report.md"
OUT = "/home/workspace/IDRBT/report/website/open-data"
os.makedirs(OUT, exist_ok=True)

with open(REPORT) as f:
    text = f.read()

for fn in ["domains.txt", "domains-with-ns.txt", "domains-without-ns.txt"]:
    src = f"/home/workspace/IDRBT/{fn}"
    dst = os.path.join(OUT, fn)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {fn}")

ct_src = "/home/workspace/IDRBT/2026-06-08_bankin.csv"
ct_dst = os.path.join(OUT, "certificate-transparency.csv")
if os.path.exists(ct_src):
    shutil.copy2(ct_src, ct_dst)
    print(f"Copied CT log ({os.path.getsize(ct_dst)} bytes)")

readme_lines = [
    "# IDRBT .bank.in Security Investigation - Open Data",
    "",
    "## Datasets",
    "",
    "| File | Description | Records | PII? |",
    "|------|-------------|---------|------|",
    "| `domains.txt` | All registered .bank.in domain names | 1,497 | No |",
    "| `domains-with-ns.txt` | Domains with name servers configured | 1,402 | No |",
    "| `domains-without-ns.txt` | Domains without name servers | 95 | No |",
    "| `certificate-transparency.csv` | CT log data from crt.sh | 6,543 | No |",
    "",
    "## Ethics",
    "",
    "- User PII (names, emails, phones, passwords, IPs) **not published**",
    "- Bcrypt hashes, OTP hashes **not published**",
    "- Only domain names and public CT log data",
    "- Every record was accessible via unauthenticated API on registrar.idrbt.ac.in",
    "",
    "## License",
    "",
    "Published for independent verification and security research under responsible disclosure principles.",
]
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write("\n".join(readme_lines) + "\n")

print("\nOpen data package complete!")
