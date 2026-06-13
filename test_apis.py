import requests, sys, json

print('Testing DexScreener pairs API...')
try:
    r = requests.get('https://api.dexscreener.com/latest/dex/tokens/0x6982508145454ce325ddbe47a25d4ec3d2311933', timeout=10)
    pairs = r.json().get("pairs") or []
    print(f"DexScreener: {r.status_code} - {len(pairs)} pairs - OK")
except Exception as e:
    print(f"DexScreener failed: {e}")

print("Testing GoPlus API...")
try:
    r = requests.get("https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=0x6982508145454ce325ddbe47a25d4ec3d2311933", timeout=10)
    d = r.json()
    has_result = bool(d.get("result"))
    print(f"GoPlus: {r.status_code} - has result: {has_result} - {'OK' if has_result else 'FAIL'}")
except Exception as e:
    print(f"GoPlus failed: {e}")

print("Testing DexScreener profiles...")
try:
    r = requests.get("https://api.dexscreener.com/token-profiles/latest/v1", timeout=10)
    items = r.json()
    print(f"Profiles: {r.status_code} - {len(items)} items - OK")
except Exception as e:
    print(f"Profiles failed: {e}")

print("Testing DexScreener search...")
try:
    r = requests.get("https://api.dexscreener.com/latest/dex/search?q=pepe", timeout=10)
    pairs = r.json().get("pairs") or []
    print(f"Search: {r.status_code} - {len(pairs)} pairs - OK")
except Exception as e:
    print(f"Search failed: {e}")
