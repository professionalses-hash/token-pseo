RPC_URLS = {
    "ethereum": "https://eth.llamarpc.com",
    "bsc": "https://bsc-dataseed1.binance.org",
    "solana": None,  # Solana holder data via other means
}


def fetch_holders(address, chain):
    if chain == "solana":
        return None
    rpc = RPC_URLS.get(chain)
    if not rpc:
        return None
    try:
        import requests
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{"to": address, "data": "0x"}, "latest"],
            "id": 1,
        }
        resp = requests.post(rpc, json=payload, timeout=15)
        resp.raise_for_status()
        return None
    except Exception:
        return None


def fetch_contract_age(address, chain):
    if chain == "solana":
        return None
    return None
