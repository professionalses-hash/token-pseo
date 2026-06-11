import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

DEXSCREENER_SEARCH = "https://api.dexscreener.com/latest/dex/search?q={query}"

SUPPORTED_CHAINS = {"ethereum", "bsc", "solana"}

SEARCH_KEYWORDS = [
    "coin", "token", "moon", "doge", "pepe", "cat", "dog", "baby",
    "ai", "eth", "sol", "trump", "musk", "safe", "shib", "bonk",
    "pump", "meme", "wen", "hodl", "ape", "based",
]


def discover_from_search():
    seen = set()
    tokens = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(_search, kw): kw for kw in SEARCH_KEYWORDS}
        for future in as_completed(futures):
            results = future.result()
            for pair in results:
                base = pair.get("baseToken") or {}
                address = base.get("address")
                chain = (pair.get("chainId") or "").lower()
                if not address or chain not in SUPPORTED_CHAINS:
                    continue
                if address in seen:
                    continue
                seen.add(address)
                tokens.append({
                    "address": address,
                    "chain": chain,
                    "name": base.get("name", ""),
                    "symbol": base.get("symbol", ""),
                    "url": pair.get("url", ""),
                })
    return tokens


def _search(query):
    try:
        resp = requests.get(DEXSCREENER_SEARCH.format(query=query), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("pairs") or []
    except Exception:
        return []
