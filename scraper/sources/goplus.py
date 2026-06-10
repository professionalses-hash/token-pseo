import requests

GOPLUS_URL = "https://api.gopluslabs.io/api/v1/token_security/{chain}?contract_addresses={address}"

CHAIN_MAP = {
    "ethereum": "1",
    "bsc": "56",
    "solana": "solana",
}


def fetch_security(address, chain):
    chain_id = CHAIN_MAP.get(chain)
    if not chain_id:
        return None
    try:
        url = GOPLUS_URL.format(chain=chain_id, address=address)
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        result = (data.get("result") or {}).get(address.lower()) or {}
        return {
            "liquidityLockedPct": _parse_pct(result.get("lockedLiquidity")),
            "mintAuthority": _parse_mint(result.get("mintAuthority")),
            "honeypotRisk": "none" if result.get("is_honeypot") == "0" else "detected",
            "buyTax": _parse_tax(result.get("buy_tax")),
            "sellTax": _parse_tax(result.get("sell_tax")),
            "creatorBalance": _parse_pct(result.get("creator_balance")),
            "holderCount": int(result.get("holder_count", 0)),
        }
    except Exception:
        return None


def _parse_pct(val):
    try:
        return float(val) if val else 0.0
    except (TypeError, ValueError):
        return 0.0


def _parse_tax(val):
    try:
        return float(val) if val else 0.0
    except (TypeError, ValueError):
        return 0.0


def _parse_mint(val):
    if val is None:
        return "unknown"
    return "renounced" if val in ("0", "false") else "active"
