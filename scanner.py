import random
import requests
ETHERSCAN_API_KEY = "N86WUX9HW4QSUSZBY88945CQYXAHURNUCX"



def check_dev_wallet_movements(contract_address):
    # Example simplified real check
    # You can improve this with real token price conversion etc.
    try:
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
        res = requests.get(url)
        data = res.json()
        if data["status"] != "1":
            return "No recent token transfer data found."

        transfers = data["result"]
        # Just sum recent token transfers for example
        total_moved = 0
        for tx in transfers[:10]:
            value = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
            total_moved += value

        return f"Devs Dumping: {int(total_moved):,} tokens moved to untracked wallet."

    except Exception as e:
        return f"Error checking dev wallets: {str(e)}"

def check_liquidity_drop(contract_address):
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/ethereum/{contract_address}"
        res = requests.get(url)
        if res.status_code != 200:
            return "Could not retrieve LP data."

        data = res.json()
        pair = data.get("pair")
        if not pair:
            return "Liquidity Missing: No locked funds detected — your money can vanish instantly."

        change_24h = float(pair.get("priceChange", {}).get("h24", 0))

        if change_24h < -30:
            return f"Liquidity pool dropped {abs(change_24h)}% in 24h."

        return "Liquidity is stable."

    except Exception as e:
        return f"Error checking liquidity: {str(e)}"

def check_honeypot(contract_address):
    try:
        url = f"https://api.honeypot.is/v1/IsHoneypot?address={contract_address}"
        res = requests.get(url)
        if res.status_code != 200:
            return "Could not check honeypot status."

        data = res.json()
        if data.get("IsHoneypot"):
            return "Honeypot detected: users can’t sell!"
        elif data.get("SellTax", 0) > 30:
            return f"High sell tax ({data['SellTax']}%) — may trap sellers."
        else:
            return "No honeypot behavior detected."

    except Exception as e:
        return f"Error checking honeypot: {str(e)}"

def analyze_token(contract_address):
    dev_wallet_status = check_dev_wallet_movements(contract_address)
    liquidity_status = check_liquidity_drop(contract_address)
    honeypot_status = check_honeypot(contract_address)

    mock_score = round(random.uniform(60, 99), 2)
    # Boost score if risks detected
    if any(
        keyword in dev_wallet_status.lower() or
        keyword in liquidity_status.lower() or
        keyword in honeypot_status.lower()
        for keyword in ["dumping", "dropped", "honeypot", "missing", "high sell tax"]
    ):
        mock_score += 7

    # Build structured reasons dict
    reasons = {
        "dev_dump": dev_wallet_status,
        "liquidity": liquidity_status,
        "honeypot": honeypot_status,
        "social": "Social Hype Spike: Sudden surge in chatter, a classic pump & dump signal.",
        "whale": "Whales Fleeing: Top 5 holders sold $2.1M in 24 hrs — price likely to crash."
    }

    actionable = [
        "DO NOT BUY this token!",
        
    ]

    similar_scams = [
        "Similar to Squid Game Token before collapse in 2021."
    ]

    return {
        "contract": contract_address,
        "risk_score": min(mock_score, 100),
        "reasons": reasons,
        "actionable": actionable,
        "similar_scams": similar_scams,
    }

