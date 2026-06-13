import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scraper"))

from sources.dexscreener import fetch_market
from sources.goplus import fetch_security

print("Testing fetch_market...")
market = fetch_market("0x6982508145454ce325ddbe47a25d4ec3d2311933")
print("  market:", "OK" if market else "None")
if market:
    print("  name:", market.get("name"))

print("Testing fetch_security...")
security = fetch_security("0x6982508145454ce325ddbe47a25d4ec3d2311933", "ethereum")
print("  security:", "OK" if security else "None")
if security:
    print("  mint:", security.get("mintAuthority"))
