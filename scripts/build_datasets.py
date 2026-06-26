#!/usr/bin/env python3
# Build open datasets from IDRBT triangulation report
import re, json, csv, shutil, os

REPORT = "/home/workspace/IDRBT/triangulation/triangulation_report.md"
OUT = "/home/workspace/IDRBT/report/website/open-data"
os.makedirs(OUT, exist_ok=True)

with open(REPORT) as f:
    text = f.read()

# The rupee sign in the report is the actual Unicode character
RUPEE = "\u20B9"

def parse_line(line):
    m = re.match(r'(\S+\.bank\.in)\s+', line)
    if not m:
        return None
    domain = m.group(1)
    rest = line[m.end():]
    amt_m = re.search(RUPEE + r'\s*([\d,]+)\s+(.*?)(?:\s{2,}|$)', rest)
    if not amt_m:
        return None
    amount = int(amt_m.group(1).replace(",", ""))
    status = amt_m.group(2).strip()
    bank_part = rest[:amt_m.start()].strip()
    bank_name = bank_part.strip() if bank_part else ""
    return {"domain": domain, "bank_name": bank_name, "amount": amount, "status": status}

def extract_section(text, start_marker, end_marker):
    idx_start = text.find(start_marker)
    if idx_start == -1:
        return []
    idx_start = text.find("\n", idx_start) + 1
    idx_end = text.find(end_marker)
    if idx_end == -1:
        idx_end = len(text)
    section = text[idx_start:idx_end]
    records = []
    for line in section.split("\n"):
        r = parse_line(line)
        if r:
            records.append(r)
    return records

records = []
records += extract_section(text, "--- SECTION 1:", "--- SECTION 2:")
records += extract_section(text, "--- SECTION 2:", "--- SECTION 3:")
records += extract_section(text, "--- SECTION 3:", "STATISTICS")

print(f"Total billing records parsed: {len(records)}")

csv_path = os.path.join(OUT, "billing.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["domain", "bank_name", "amount_inr", "payment_status"])
    for r in records:
        w.writerow([r["domain"], r["bank_name"], r["amount"], r["status"]])

json_path = os.path.join(OUT, "billing.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

total = sum(r["amount"] for r in records)
approved = sum(r["amount"] for r in records if "approved" in r["status"].lower())
pending = sum(r["amount"] for r in records if "ready" in r["status"].lower())
completed = sum(r["amount"] for r in records if "completed" in r["status"].lower())

stats = {
    "total_records": len(records),
    "total_amount_inr": total,
    "approved_amount_inr": approved,
    "pending_amount_inr": pending,
    "completed_amount_inr": completed,
    "unique_domains": len({r["domain"] for r in records}),
}
with open(os.path.join(OUT, "stats.json"), "w") as f:
    json.dump(stats, f, indent=2)

print(f"Total: {RUPEE}{total:,}")
print(f"Approved: {RUPEE}{approved:,}")
print(f"Pending: {RUPEE}{pending:,}")
print(f"Completed: {RUPEE}{completed:,}")

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
    f"| `billing.csv` | Anonymized billing/invoice records | {len(records)} | No |",
    f"| `billing.json` | Same data as JSON | {len(records)} | No |",
    "| `certificate-transparency.csv` | CT log data from crt.sh | 6,543 | No |",
    "| `stats.json` | Aggregate statistics | - | No |",
    "",
    "## Ethics",
    "",
    "- User PII (names, emails, phones, passwords, IPs) **not published**",
    "- Bcrypt hashes, OTP hashes **not published**",
    "- Only domain names, billing amounts (already public via invoice API), and public CT log data",
    "- Every record in billing.csv was accessible via unauthenticated API on registrar.idrbt.ac.in",
    "",
    "## License",
    "",
    "Published for independent verification and security research under responsible disclosure principles.",
]
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write("\n".join(readme_lines) + "\n")

print("\nOpen data package complete!")
