import requests
from sources.dexsearch import discover_from_search

DEXSCREENER_PROFILES = "https://api.dexscreener.com/token-profiles/latest/v1"
DEXSCREENER_BOOSTS = "https://api.dexscreener.com/token-boosts/latest/v1"

SUPPORTED_CHAINS = {"ethereum", "bsc", "solana"}


def discover_tokens():
    print("Fetching profiles...", flush=True)
    profiles = _fetch(DEXSCREENER_PROFILES)
    print(f"Profiles: {len(profiles)}", flush=True)
    boosts = _fetch(DEXSCREENER_BOOSTS)
    print(f"Boosts: {len(boosts)}", flush=True)
    print("Searching keywords...", flush=True)
    search = discover_from_search()
    print(f"Search results: {len(search)}", flush=True)
    seen = set()
    tokens = []
    for entry in profiles + boosts:
        token = _normalize(entry)
        if token and token["address"] not in seen:
            seen.add(token["address"])
            tokens.append(token)
    for entry in search:
        if entry["address"] not in seen:
            seen.add(entry["address"])
            tokens.append(entry)
    return tokens


def _fetch(url):
    try:
        resp = requests.get(url, timeout=10)
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
