import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    token["network"] = token.get("chain", "")

    market_clean = {k: v for k, v in market.items() if k not in ("name", "symbol")}
    token["market"] = market_clean
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


def backfill_socials(existing):
    to_fill = [t for t in existing if not t.get("market", {}).get("socials")]
    if not to_fill:
        return
    print(f"Backfilling socials for {len(to_fill)} tokens...", flush=True)
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(fetch_market, t["address"]): t for t in to_fill}
        for future in as_completed(futures):
            try:
                market = future.result(timeout=15)
            except Exception:
                continue
            if market and market.get("socials"):
                token = futures[future]
                token.setdefault("market", {})["socials"] = market["socials"]
                if market.get("website"):
                    token["market"]["website"] = market["website"]


def run():
    discovered = discover_tokens()
    print(f"Discovered {len(discovered)} tokens", flush=True)

    enriched = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(enrich, t): t for t in discovered}
        for future in as_completed(futures):
            try:
                result = future.result(timeout=30)
            except Exception:
                result = None
            if result:
                result["slug"] = slugify(result.get("name", "unknown"))
                enriched.append(result)

    print(f"Enriched {len(enriched)}", flush=True)

    ranked = filter_and_rank(enriched)

    existing = load_tokens()
    backfill_socials(existing)
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
