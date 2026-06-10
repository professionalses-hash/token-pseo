def calculate_trust_score(token):
    score = 50

    sec = token.get("security", {})
    market = token.get("market", {})
    tokenomics = token.get("tokenomics", {})

    if sec.get("liquidityLockedPct", 0) >= 80:
        score += 15
    if sec.get("mintAuthority") == "renounced":
        score += 10
    if sec.get("buyTax", 99) <= 5:
        score += 10
    if sec.get("sellTax", 99) <= 5:
        score += 10
    if sec.get("honeypotRisk") == "detected":
        score -= 15
    if tokenomics.get("top10Pct", 0) >= 50:
        score -= 10
    if sec.get("holderCount", 0) >= 1000:
        score += 10
    if sec.get("contractAgeDays", 0) >= 30:
        score += 5
    if market.get("liquidityUsd", 0) >= 50000:
        score += 5

    return max(0, min(100, score))
