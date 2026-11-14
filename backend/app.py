
from flask import Flask, request, jsonify, send_from_directory
from performance_bot import performance_analysis_bot
from algorithms import fifo, lru, optimal
import os

app = Flask(__name__)

# Frontend directory
FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


# Display frontend
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


# Load CSS and JavaScript
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# Existing manual performance analysis API
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json(silent=True) or {}
    results = data.get("results", {})

    if not results:
        return jsonify({
            "success": False,
            "message": "No performance results provided."
        }), 400

    try:
        output = performance_analysis_bot(results)

        if not output.get("success"):
            return jsonify(output), 400

        return jsonify(output)

    except (KeyError, ValueError, TypeError) as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


# NEW: Run all three algorithms automatically
@app.route("/simulate", methods=["POST"])
def simulate():

    data = request.get_json(silent=True) or {}

    pages = data.get("pages")
    capacity = data.get("capacity")

    if not isinstance(pages, list) or not pages:
        return jsonify({
            "success": False,
            "message": "Please provide a valid page reference sequence."
        }), 400

    try:
        pages = [int(page) for page in pages]
        capacity = int(capacity)

        if capacity <= 0:
            raise ValueError("Frame capacity must be greater than zero.")

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Invalid page references or frame capacity."
        }), 400

    try:
        # Run all page replacement algorithms
        simulation_results = {
            "FIFO": fifo(pages, capacity),
            "LRU": lru(pages, capacity),
            "Optimal": optimal(pages, capacity)
        }

        # Analyze their performance automatically
        analysis = performance_analysis_bot(simulation_results)

        if not analysis.get("success"):
            return jsonify(analysis), 400

        return jsonify({
            **analysis,
            "pages": pages,
            "frame_capacity": capacity,
            "simulation_results": simulation_results
        })

    except (KeyError, ValueError, TypeError) as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)
