# IDRBT .bank.in Security Investigation - Open Data

## Datasets

| File | Description | Records | PII? |
|------|-------------|---------|------|
| `domains.txt` | All registered .bank.in domain names | 1,497 | No |
| `domains-with-ns.txt` | Domains with name servers configured | 1,402 | No |
| `domains-without-ns.txt` | Domains without name servers | 95 | No |
| `billing.csv` | Anonymized billing/invoice records | 1465 | No |
| `billing.json` | Same data as JSON | 1465 | No |
| `certificate-transparency.csv` | CT log data from crt.sh | 6,543 | No |
| `stats.json` | Aggregate statistics | - | No |

## Ethics

- User PII (names, emails, phones, passwords, IPs) **not published**
- Bcrypt hashes, OTP hashes **not published**
- Only domain names, billing amounts (already public via invoice API), and public CT log data
- Every record in billing.csv was accessible via unauthenticated API on registrar.idrbt.ac.in

## License

Published for independent verification and security research under responsible disclosure principles.
