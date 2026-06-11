import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from discoverer import discover_tokens
from sources.dexscreener import fetch_market
from sources.goplus import fetch_security
from analyzer import calculate_trust_score
from potential import filter_and_rank
from store import load_tokens, save_tokens


def enrich(token):
    market = fetch_market(token["address"])
    security = fetch_security(token["address"], token["chain"])
    if not market or not security:
        return None

    if market.get("name"):
        token["name"] = market["name"]
    if market.get("symbol"):
        token["symbol"] = market["symbol"]

    token["market"] = market
    token["security"] = security
    token["tokenomics"] = {
        "creatorPct": security.get("creatorBalance", 0),
        "top10Pct": 0,
        "buyTax": security.get("buyTax", 0),
        "sellTax": security.get("sellTax", 0),
    }
    token["badges"] = {
        "liquidityLocked": security.get("liquidityLockedPct", 0) >= 80,
        "mintRenounced": security.get("mintAuthority") == "renounced",
        "honeypot": security.get("honeypotRisk") == "detected",
        "highConcentration": False,
    }
    token["trustScore"] = calculate_trust_score(token)
    return token


def slugify(name):
    return name.lower().replace(" ", "-").replace("_", "-")[:64]


def run():
    discovered = discover_tokens()
    enriched = []
    for token in discovered:
        result = enrich(token)
        if result:
            result["slug"] = slugify(result.get("name", "unknown"))
            enriched.append(result)

    ranked = filter_and_rank(enriched)

    existing = load_tokens()
    seen = {t["address"] for t in existing}
    for t in ranked:
        if t["address"] not in seen:
            existing.append(t)
            seen.add(t["address"])

    save_tokens(existing)
    print(f"Discovered {len(discovered)}, enriched {len(enriched)}, ranked {len(ranked)}")
    print(f"Total tokens in store: {len(existing)}")


if __name__ == "__main__":
    run()
