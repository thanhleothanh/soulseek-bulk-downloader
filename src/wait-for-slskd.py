import os
import sys
import time
import urllib.request
import json

SLSKD_HOST = os.environ.get("SLSKD_HOST", "http://slskd:5030")
TIMEOUT = 120

print(f"Waiting for slskd to log in (timeout: {TIMEOUT}s)...")
start = time.time()
while time.time() - start < TIMEOUT:
    try:
        req = urllib.request.Request(f"{SLSKD_HOST}/api/v0/application")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            server = data.get("server", {})
            if server.get("isLoggedIn", False):
                print(f"slskd is ready! (state: {server.get('state')})")
                sys.exit(0)
    except Exception:
        pass
    time.sleep(2)

print(f"❌ slskd did not log in within {TIMEOUT}s")
sys.exit(1)
