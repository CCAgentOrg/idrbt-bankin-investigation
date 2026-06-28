#!/usr/bin/env python3
"""Upload site directory to Cloudflare Pages."""

import json, sys, os, subprocess, hashlib

SITE_DIR = "/home/workspace/idrbt-bankin-investigation/site"
TOKEN_FILE = "/tmp/cf_token.txt"

with open(TOKEN_FILE) as f:
    token = f.read().strip()

with open("/etc/zo/mcpo/config.json") as f:
    cfg = json.load(f)

base_url = cfg["mcpServers"]["cloudflare"]["url"]

def cf_call(method, args):
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": method, "arguments": args},
        "id": 1
    })
    proc = subprocess.run(
        ["curl", "-s", "-X", "POST", base_url,
         "-H", f"Authorization: Bearer {token}",
         "-H", "Content-Type: application/json",
         "-d", req],
        capture_output=True, text=True
    )
    return json.loads(proc.stdout)

# Get account
data = cf_call("cloudflare_get_accounts_list", {})
account_id = data["result"]["content"][0]["result"][0]["id"]
print(f"Account: {account_id}")

# Gather files
files = []
for root, dirs, fnames in os.walk(SITE_DIR):
    for fn in fnames:
        fp = os.path.join(root, fn)
        rel = os.path.relpath(fp, SITE_DIR)
        with open(fp, "rb") as f:
            content = f.read()
        files.append({"name": rel, "content": content, "hash": hashlib.md5(content).hexdigest()})

print(f"Files: {len(files)}")

# Create manifest
manifest = {f["name"]: f["hash"] for f in files}

# Create deployment
data = cf_call("cloudflare_pages_deployment_create", {
    "account_id": account_id,
    "project_name": "idrbt-bankin-investigation",
    "branch": "main",
    "manifest": json.dumps(manifest)
})

deploy_data = data["result"]["content"][0]["result"]
deploy_id = deploy_data["id"]
upload_urls = deploy_data.get("upload_urls", {})
print(f"Deployment: {deploy_id}")
print(f"Upload URLs: {len(upload_urls)}")

# Upload each file
for f in files:
    url = upload_urls.get(f["name"])
    if not url:
        print(f"  No URL for {f['name']}")
        continue
    proc = subprocess.run(
        ["curl", "-s", "-X", "PUT", url,
         "-H", "Content-Type: application/octet-stream",
         "--data-binary", f"@{os.path.join(SITE_DIR, f['name'])}"],
        capture_output=True, text=True
    )
    print(f"  {'✓' if proc.returncode == 0 else '✗'} {f['name']}")

print(f"\nDone. Live at: https://idrbt-bankin-investigation.pages.dev")
