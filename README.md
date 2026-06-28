# IDRBT .bank.in Security Investigation

## Overview
A responsible disclosure investigation into the IDRBT Domain Registration Portal (registrar.idrbt.ac.in) — the exclusive registry for .bank.in domains under RBI purview.

**Date:** June 8-26, 2026  
**Status:** CERT-In confirmed vulnerability is now fixed (June 26, 2026)  
**Researcher:** Cashless Consumer

## Key Findings

1. **33+ Unauthenticated API Endpoints** — User database (5,576 records with bcrypt hashes), system config all exposed without auth
2. **5,576 User Records Exposed** — Full PII, bcrypt password hashes, OTP hashes, device fingerprints
3. **Phantom Test Domains** — Test domains (VKTEST, IDTMAY, etc.) live on NIXI alongside real banks
4. **No DMARC Enforcement** — 40% of .bank.in domains have zero email spoofing protection
5. **Data Residency Violations** — Cooperative banks hosted on foreign servers (US, Singapore, Lithuania)
6. **Non-Bank Entities** — Housing finance companies and phantom organizations with Super Admin access
7. **No Public Tender** — IKCON Technologies appointed without visible procurement process

## Timeline

| Date | Event |
|------|-------|
| 2026-02 | RBI announces .bank.in mandate in bi-monthly policy |
| 2026-04-22 | RBI formal circular (RBI/2025-26/28) — .bank.in mandatory for banks |
| 2026-05 | IDRBT portal launched |
| 2026-06-08 05:07 | Discovery of unauthenticated user database endpoint |
| 2026-06-08 05:30 | Initial report filed with CERT-In |
| 2026-06-08 07:30 | Extended enumeration: orphan users, phantom domains, DSC proxy |
| 2026-06-08 | CERT-In acknowledges, requests PoC |
| 2026-06-26 | CERT-In confirms vulnerability has been fixed |

## Open Data

All non-sensitive datasets published at:  
https://zo.pub/cashlessconsumer/idrbt-open-data

- `domains.txt` — All 1,497 registered .bank.in domains
- `certificate-transparency.csv` — 6,543 CT log entries

## POC Video  
https://zo.pub/cashlessconsumer/idrbt-poc-video

## Reproducible Methodology

All findings can be independently verified:
```
curl -s 'https://registrar.idrbt.ac.in/api/dr/user/all' | jq '. | length'
# Returns 5461 — unauthenticated user data exposure
```

## Repository
https://github.com/CCAgentOrg/idrbt-bankin-investigation

## Press & Media
For inquiries: Cashless Consumer via CERT-In coordination channels

---

*Published under responsible disclosure principles. User PII, bcrypt hashes, and sensitive data not published.*
