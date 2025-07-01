from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import analyze_token
import requests
app = Flask(__name__)
CORS(app, supports_credentials=True)  # ✅ Wide-open CORS

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        # Preflight CORS check
        return jsonify({"ok": True}), 200

    data = request.json
    contract = data.get("contract")
    if not contract:
        return jsonify({"error": "No contract address provided"}), 400

    result = analyze_token(contract)
    return jsonify(result)


@app.route('/trending', methods=['GET'])
def get_trending_tokens():
    try:
        url = "https://public-api.dextools.io/trending/pairs?chain=ether&interval=1h"
        headers = {
            "accept": "application/json",
            "origin": "https://www.dextools.io",
            "referer": "https://www.dextools.io/"
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        raw = res.json()
        print("🧪 DEXTOOLS RAW RESPONSE:", raw)  # See exact structure

        data = raw.get("data", [])
        if not isinstance(data, list) or not data:
            raise ValueError("DexTools returned invalid or empty data.")

        tokens = []
        for pair in data:
            token = pair.get("token") or pair.get("baseToken")  # Try alternate keys
            if token and token.get("contract"):
                tokens.append(token["contract"])

        if not tokens:
            raise ValueError("No token contracts found in trending pairs.")

        return jsonify(tokens[:10])

    except Exception as e:
        print("🔥 Error in /trending:", str(e))
        print("⚠️ Returning fallback tokens.")
        return jsonify([
            "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",  # Shiba
            "0x63d2d1ca2d3bb8da2d477db0f0e6555d65bf89c5",  # ScamX
            "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"  # Fake RugCoin
        ])





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

