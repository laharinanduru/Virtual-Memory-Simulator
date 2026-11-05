from flask import Flask, request, jsonify
from bots import analyze_performance

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Virtual Memory Simulator Backend is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    results = request.json.get("results", {})

    if not results:
        return jsonify({
            "error": "No performance results provided"
        }), 400

    try:
        output = analyze_performance(results)
        return jsonify(output)

    except (KeyError, ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
