from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import analyze_token

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

