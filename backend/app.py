
from flask import Flask, jsonify, request
from flask_cors import CORS

from algorithms import (
    simulate_fifo,
    simulate_lru,
    simulate_optimal,
)

app = Flask(__name__)
CORS(app)

ALGORITHMS = {
    "FIFO": simulate_fifo,
    "LRU": simulate_lru,
    "OPTIMAL": simulate_optimal,
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Virtual Memory Simulator API is running!",
        "status": "success"
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Virtual Memory Simulator Backend"
    })


@app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a valid JSON object."
        }), 400

    pages = data.get("pages")
    frames = data.get("frames")
    algorithm = data.get("algorithm")

    if not isinstance(pages, list) or not pages:
        return jsonify({
            "error": "'pages' must be a non-empty list."
        }), 400

    if any(type(page) is not int or page < 0 for page in pages):
        return jsonify({
            "error": "Page references must be non-negative integers."
        }), 400

    if type(frames) is not int or frames < 1:
        return jsonify({
            "error": "'frames' must be a positive integer."
        }), 400

    if not isinstance(algorithm, str):
        return jsonify({
            "error": "'algorithm' must be FIFO, LRU, or Optimal."
        }), 400

    algorithm = algorithm.strip().upper()

    if algorithm not in ALGORITHMS:
        return jsonify({
            "error": "Unsupported algorithm. Choose FIFO, LRU, or Optimal."
        }), 400

    result = ALGORITHMS[algorithm](pages, frames)

    return jsonify({
        "algorithm": algorithm,
        "frames_count": frames,
        **result
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
