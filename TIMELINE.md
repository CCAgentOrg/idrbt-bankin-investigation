# IDRBT .bank.in Security Investigation — Complete Timeline

## Phase 1: Discovery & Disclosure

| Date | Event | Details |
|------|-------|---------|
| Feb 7, 2025 | RBI announces .bank.in namespace | Bi-monthly policy statement introduces exclusive banking domain |
| Apr 22, 2025 | RBI circular RBI/2025-26/28 | Formal mandate: all banks must adopt .bank.in domains |
| May 2025 | IDRBT Portal launched | Portal built by IKCON Technologies without public tender |
| May–Oct 2025 | Migration period | Banks migrate to .bank.in; NIXI activation |
| Jun 8, 2026 05:07 UTC | Discovery | CashlessConsumer discovers /api/dr/user/all during OSINT scan |
| Jun 8, 2026 05:20 UTC | Evidence collection | Raw user data (5,461 records), schema collected |
| Jun 8, 2026 05:30 UTC | Initial CERT-In report | Filed with incident@cert-in.org.in |
| Jun 8, 2026 06:30 UTC | Invoice discovery | 1,535 billing records (₹4.72 Cr) found via /api/dr/invoice/ |
| Jun 8, 2026 07:30 UTC | Extended enumeration | Orphan users (1,072), DSC proxy, config endpoints documented |
| Jun 8, 2026 | Updated report filed | All 33+ endpoints submitted to CERT-In |
| Jun 8, 2026 | Evidence archive published | zo.pub/cashlessconsumer/idrbt-bankin-security |
| Jun 25, 2026 | CERT-In confirmation | IDRBT confirms vulnerability fixed |

## Phase 2: Public Disclosure (2026-06-26)

| Date | Event | Details |
|------|-------|---------|
| Jun 26, 2026 | Research report published | cashlessconsumer.zo.space/bankin-report |
| Jun 26, 2026 | Open data published | github.com/CCAgentOrg/idrbt-bankin-investigation |
| Jun 26, 2026 | Open data package | zo.pub/cashlessconsumer/idrbt-open-data |
| Jun 26, 2026 | POC video | zo.pub/cashlessconsumer/idrbt-poc-video |

## Key Facts

- **Total unauthenticated endpoints:** 33+
- **User records exposed:** 5,576 unique
- **Bcrypt password hashes:** 6,752 (across all endpoints, with overlaps)
- **Ongoing OTP hashes:** 2,726 (49% of records)
- **Super Admin orphan accounts:** 1,072 (100% Super Admin role)
- **Invoice records:** 1,535
- **Total billed amount:** ₹4,72,90,751.98
- **Organizations affected:** 1,327
- **Domains registered:** 1,497
- **No public tender:** Portal built by IKCON Technologies without RFP
- **No DMARC/DNSSEC mandate:** 80% no DNSSEC, 40% no DMARC
- **Data residency violation:** Cooperative banks hosted in US/Lithuania/Singapore
