
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

# 8-bit memory configuration
ADDRESS_BITS = 8
ADDRESS_SPACE = 2 ** ADDRESS_BITS  # 256 bytes

PAGE_SIZE = 16
PAGE_BITS = 4
OFFSET_BITS = 4

TOTAL_VIRTUAL_PAGES = ADDRESS_SPACE // PAGE_SIZE  # 16
MAX_FRAMES = 16


def translate_address(binary_address):
    """Convert an 8-bit logical address into page and offset."""

    if (
        not isinstance(binary_address, str)
        or len(binary_address) != ADDRESS_BITS
        or any(bit not in "01" for bit in binary_address)
    ):
        raise ValueError(
            "Each logical address must be exactly 8 binary digits."
        )

    decimal_address = int(binary_address, 2)

    page_number = decimal_address // PAGE_SIZE
    offset = decimal_address % PAGE_SIZE

    return {
        "logical_address": binary_address,
        "logical_decimal": decimal_address,
        "page_number": page_number,
        "page_binary": format(page_number, "04b"),
        "offset": offset,
        "offset_binary": format(offset, "04b"),
    }


def build_page_table(frames):
    """Build the current page-to-frame mapping."""

    page_table = []

    for frame_number, page_number in enumerate(frames):
        page_table.append({
            "page_number": page_number,
            "frame_number": frame_number,
            "frame_binary": format(frame_number, "04b"),
            "valid": True
        })

    return page_table


def enrich_history(history, translations):
    """Add physical address information to each simulation step."""

    enriched = []

    for step, translation in zip(history, translations):
        current_frames = step["frames"]

        # Find the physical frame containing the requested page.
        frame_number = current_frames.index(step["page"])

        physical_address = (
            frame_number * PAGE_SIZE + translation["offset"]
        )

        enriched.append({
            **step,
            **translation,
            "physical_frame": frame_number,
            "physical_frame_binary": format(frame_number, "04b"),
            "physical_address": physical_address,
            "physical_address_binary": format(
                physical_address, "08b"
            ),
        })

    return enriched


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


@app.route("/api/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a valid JSON object."
        }), 400

    addresses = data.get("addresses")

    if not isinstance(addresses, list) or not addresses:
        return jsonify({
            "error": "'addresses' must be a non-empty list."
        }), 400

    try:
        translations = [
            translate_address(address)
            for address in addresses
        ]
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "address_bits": ADDRESS_BITS,
        "address_space": ADDRESS_SPACE,
        "page_size": PAGE_SIZE,
        "page_bits": PAGE_BITS,
        "offset_bits": OFFSET_BITS,
        "total_virtual_pages": TOTAL_VIRTUAL_PAGES,
        "translations": translations
    }), 200


@app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a valid JSON object."
        }), 400

    frames = data.get("frames")
    algorithm = data.get("algorithm")

    if type(frames) is not int or not 1 <= frames <= MAX_FRAMES:
        return jsonify({
            "error": "'frames' must be an integer between 1 and 16."
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

    # New 8-bit input mode.
    if "addresses" in data:
        addresses = data.get("addresses")

        if not isinstance(addresses, list) or not addresses:
            return jsonify({
                "error": "'addresses' must be a non-empty list."
            }), 400

        try:
            translations = [
                translate_address(address)
                for address in addresses
            ]
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        pages = [
            item["page_number"]
            for item in translations
        ]

    # Legacy page-reference mode, retained for compatibility.
    else:
        pages = data.get("pages")

        if not isinstance(pages, list) or not pages:
            return jsonify({
                "error": "Provide a non-empty 'addresses' or 'pages' list."
            }), 400

        if any(
            type(page) is not int or not 0 <= page < TOTAL_VIRTUAL_PAGES
            for page in pages
        ):
            return jsonify({
                "error": "Page references must be integers from 0 to 15."
            }), 400

        translations = None

    result = ALGORITHMS[algorithm](pages, frames)

    response = {
        "algorithm": algorithm,
        "frames_count": frames,
        "address_bits": ADDRESS_BITS,
        "page_size": PAGE_SIZE,
        **result
    }

    if translations is not None:
        response["translations"] = translations

        response["history"] = enrich_history(
            result["history"],
            translations
        )

        response["page_table"] = build_page_table(
            result["history"][-1]["frames"]
        )

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
