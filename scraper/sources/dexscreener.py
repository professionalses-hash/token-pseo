import requests

DEXSCREENER_PAIRS = "https://api.dexscreener.com/latest/dex/tokens/{address}"


def fetch_market(address):
    try:
        resp = requests.get(DEXSCREENER_PAIRS.format(address=address), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        pairs = data.get("pairs") or []
        if not pairs:
            return None
        pair = max(pairs, key=lambda p: float(p.get("liquidity", {}).get("usd", 0) or 0))
        return {
            "priceUsd": _safe_float(pair, "priceUsd"),
            "marketCap": _safe_float(pair, "fdv"),
            "liquidityUsd": _safe_float(pair, "liquidity", "usd"),
            "volume24h": _safe_float(pair, "volume", "h24"),
        }
    except Exception:
        return None


def _safe_float(obj, *keys):
    try:
        val = obj
        for k in keys:
            val = val.get(k, 0)
        return float(val) if val else 0.0
    except (TypeError, ValueError):
        return 0.0
