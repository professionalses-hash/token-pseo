MIN_LIQUIDITY = 500
MAX_TAX = 15


def calculate_potential(token):
    market = token.get("market", {})
    security = token.get("security", {})

    liquidity = market.get("liquidityUsd", 0)
    if liquidity < MIN_LIQUIDITY:
        return 0

    if security.get("honeypotRisk") == "detected":
        return 0

    buy_tax = security.get("buyTax", 0)
    sell_tax = security.get("sellTax", 0)
    if buy_tax > MAX_TAX or sell_tax > MAX_TAX:
        return 0

    trust = token.get("trustScore", 0)
    volume = market.get("volume24h", 0)
    score = trust * 0.4 + (volume / liquidity if liquidity else 0) * 10
    return round(score, 1)


def filter_and_rank(tokens):
    for t in tokens:
        t["potentialScore"] = calculate_potential(t)
    ranked = [t for t in tokens if t["potentialScore"] > 0]
    ranked.sort(key=lambda x: x["potentialScore"], reverse=True)
    return ranked
