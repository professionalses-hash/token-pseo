import requests

DEXSCREENER_PROFILES = "https://api.dexscreener.com/token-profiles/latest/v1"
DEXSCREENER_BOOSTS = "https://api.dexscreener.com/token-boosts/latest/v1"

SUPPORTED_CHAINS = {"ethereum", "bsc", "solana"}


def discover_tokens():
    profiles = _fetch(DEXSCREENER_PROFILES)
    boosts = _fetch(DEXSCREENER_BOOSTS)
    seen = set()
    tokens = []
    for entry in profiles + boosts:
        token = _normalize(entry)
        if token and token["address"] not in seen:
            seen.add(token["address"])
            tokens.append(token)
    return tokens


def _fetch(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


def _normalize(entry):
    chain = (entry.get("chainId") or "").lower()
    if chain not in SUPPORTED_CHAINS:
        return None
    address = entry.get("tokenAddress")
    if not address:
        return None
    return {
        "address": address,
        "chain": chain,
        "name": "",
        "symbol": "",
        "url": entry.get("url", ""),
    }
