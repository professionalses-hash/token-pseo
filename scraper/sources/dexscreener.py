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
        base = pair.get("baseToken") or {}
        info = pair.get("info") or {}
        socials = {}
        for s in info.get("socials") or []:
            t = s.get("type", "").lower()
            u = s.get("url", "")
            if t and u:
                socials[t] = u
        websites = [w.get("url", "") for w in info.get("websites") or [] if w.get("url")]
        return {
            "name": base.get("name", ""),
            "symbol": base.get("symbol", ""),
            "priceUsd": _safe_float(pair, "priceUsd"),
            "marketCap": _safe_float(pair, "fdv"),
            "liquidityUsd": _safe_float(pair, "liquidity", "usd"),
            "volume24h": _safe_float(pair, "volume", "h24"),
            "socials": socials,
            "website": websites[0] if websites else "",
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
