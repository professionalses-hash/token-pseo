import requests

# Test GoPlus with raw response
url = "https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=0x6982508145454ce325ddbe47a25d4ec3d2311933"
r = requests.get(url, timeout=10)
data = r.json()
print("Status:", r.status_code)
print("Keys in response:", list(data.keys()))
print("Result keys:", list((data.get("result") or {}).keys()))
result = data.get("result") or {}
pepe_result = result.get("0x6982508145454ce325ddbe47a25d4ec3d2311933")
print("Has pepe result:", pepe_result is not None)
if pepe_result:
    print("Pepe result keys:", list(pepe_result.keys())[:10])

# Try with lowercase
pepe_lower = result.get("0x6982508145454ce325ddbe47a25d4ec3d2311933".lower())
print("Has lowercase result:", pepe_lower is not None)
