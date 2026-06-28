# IDRBT .bank.in Security Investigation - Open Data

## Datasets

| File | Description | Records | PII? |
|------|-------------|---------|------|
| `domains.txt` | All registered .bank.in domain names | 1,497 | No |
| `domains-with-ns.txt` | Domains with name servers configured | 1,402 | No |
| `domains-without-ns.txt` | Domains without name servers | 95 | No |
| `certificate-transparency.csv` | CT log data from crt.sh | 6,543 | No |

## Ethics

- User PII (names, emails, phones, passwords, IPs) **not published**
- Bcrypt hashes, OTP hashes **not published**
- Only domain names and public CT log data
- Every record was accessible via unauthenticated API on registrar.idrbt.ac.in

## License

Published for independent verification and security research under responsible disclosure principles.
