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
        res = requests.get(url)
        data = res.json().get("data", [])
        tokens = [pair.get("token", {}).get("contract") for pair in data if pair.get("token")]
        return jsonify(tokens[:10])  # return top 10 trending token addresses
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

