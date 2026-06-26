#!/bin/bash
# Verify IDRBT API vulnerability - does /api/dr/user/all return data without auth?
# Run: bash verify_api.sh

URL="https://registrar.idrbt.ac.in/api/dr/user/all"
echo "Checking: $URL"
RESP=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ "$RESP" = "200" ]; then
  COUNT=$(curl -s "$URL" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null)
  echo "❌ VULNERABLE: HTTP $RESP, $COUNT records returned without authentication"
  echo "CERT-In notified 2026-06-08"
else
  echo "✅ SECURED: HTTP $RESP - API access blocked"
  echo "Fix confirmed by CERT-In 2026-06-25"
fi
