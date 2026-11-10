
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from algorithms import (
    simulate_fifo,
    simulate_lru,
    simulate_optimal
)

app = Flask(__name__)
CORS(app)

ALGORITHMS = {
    "FIFO": simulate_fifo,
    "LRU": simulate_lru,
    "OPTIMAL": simulate_optimal
}

# Memory configuration
ADDRESS_BITS = 8
ADDRESS_SPACE = 2 ** ADDRESS_BITS
PAGE_SIZE = 16
PAGE_BITS = 4
OFFSET_BITS = 4
TOTAL_VIRTUAL_PAGES = ADDRESS_SPACE // PAGE_SIZE
MAX_FRAMES = 16


def translate_address(binary_address):
    """Convert an 8-bit logical address into page number and offset."""

    if not isinstance(binary_address, str):
        raise ValueError("Each address must be a string.")

    if (
        len(binary_address) != ADDRESS_BITS
        or any(bit not in "01" for bit in binary_address)
    ):
        raise ValueError(
            "Each logical address must contain exactly 8 binary digits."
        )

    logical_address = int(binary_address, 2)

    page_binary = binary_address[:PAGE_BITS]
    offset_binary = binary_address[PAGE_BITS:]

    return {
        "logical_address": binary_address,
        "logical_address_decimal": logical_address,
        "page_number": int(page_binary, 2),
        "page_binary": page_binary,
        "offset": int(offset_binary, 2),
        "offset_binary": offset_binary
    }


def build_page_table(frames):
    """Build a page table from the final frame list."""

    page_table = []

    for frame_number, page_number in enumerate(frames):
        if page_number is not None:
            page_table.append({
                "page_number": page_number,
                "frame_number": frame_number,
                "valid": True
            })

    return page_table


def enrich_history(history, translations):
    """Add logical and physical address information to simulation history."""

    enriched_history = []

    for index, step in enumerate(history):
        frames = step["frames"]
        page_number = step["page"]

        frame_number = frames.index(page_number)
        translation = translations[index]

        physical_address = (
            frame_number * PAGE_SIZE + translation["offset"]
        )

        enriched_step = {
            **step,
            "logical_address": translation["logical_address"],
            "logical_address_decimal": translation["logical_address_decimal"],
            "page_number": translation["page_number"],
            "page_binary": translation["page_binary"],
            "offset": translation["offset"],
            "offset_binary": translation["offset_binary"],
            "frame_number": frame_number,
            "physical_address": physical_address,
            "physical_address_binary": format(
                physical_address, "08b"
            )
        }

        enriched_history.append(enriched_step)

    return enriched_history


def validate_frames(frames):
    """Validate the number of physical memory frames."""

    if type(frames) is not int or not 1 <= frames <= MAX_FRAMES:
        raise ValueError("Frames must be an integer between 1 and 16.")


def process_addresses(addresses):
    """Validate addresses and return translations and page numbers."""

    if not isinstance(addresses, list) or not addresses:
        raise ValueError("Addresses must be a non-empty list.")

    translations = [
        translate_address(address) for address in addresses
    ]

    pages = [
        translation["page_number"] for translation in translations
    ]

    return translations, pages


@app.route("/")
def home():
    return send_from_directory("..", "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Backend is running"
    }), 200


@app.route("/api/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be a JSON object."
            }), 400

        binary_address = data.get("address")
        translation = translate_address(binary_address)

        return jsonify(translation), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/simulate", methods=["POST"])
def simulate():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be a JSON object."
            }), 400

        frames = data.get("frames")
        validate_frames(frames)

        algorithm_name = data.get("algorithm", "").strip().upper()

        if algorithm_name not in ALGORITHMS:
            return jsonify({
                "error": "Invalid algorithm. Choose FIFO, LRU, or OPTIMAL."
            }), 400

        # 8-bit logical address mode
        if "addresses" in data:
            translations, pages = process_addresses(data["addresses"])

            result = ALGORITHMS[algorithm_name](pages, frames)

            result["history"] = enrich_history(
                result["history"], translations
            )

            result["page_table"] = build_page_table(
                result["history"][-1]["frames"]
            )

            result["translations"] = translations

        # Legacy page number mode
        elif "pages" in data:
            pages = data["pages"]

            if (
                not isinstance(pages, list)
                or not pages
                or any(type(page) is not int for page in pages)
                or any(not 0 <= page < TOTAL_VIRTUAL_PAGES for page in pages)
            ):
                return jsonify({
                    "error": "Pages must be a non-empty list of integers between 0 and 15."
                }), 400

            result = ALGORITHMS[algorithm_name](pages, frames)

            result["page_table"] = build_page_table(
                result["history"][-1]["frames"]
            )

        else:
            return jsonify({
                "error": "Provide either addresses or pages."
            }), 400

        result["algorithm"] = algorithm_name
        result["frames_count"] = frames

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/compare", methods=["POST"])
def compare():
    """Run only the algorithms selected by the frontend."""

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be a JSON object."
            }), 400

        frames = data.get("frames")
        validate_frames(frames)

        translations, pages = process_addresses(
            data.get("addresses")
        )

        selected_algorithms = data.get("algorithms")

        if (
            not isinstance(selected_algorithms, list)
            or len(selected_algorithms) not in (2, 3)
        ):
            return jsonify({
                "error": "Select either 2 or 3 algorithms to compare."
            }), 400

        if any(not isinstance(name, str) for name in selected_algorithms):
            return jsonify({
                "error": "Algorithm names must be strings."
            }), 400

        selected_algorithms = [
            name.strip().upper() for name in selected_algorithms
        ]

        if len(set(selected_algorithms)) != len(selected_algorithms):
            return jsonify({
                "error": "Duplicate algorithms are not allowed."
            }), 400

        invalid_algorithms = [
            name for name in selected_algorithms
            if name not in ALGORITHMS
        ]

        if invalid_algorithms:
            return jsonify({
                "error": (
                    "Invalid algorithm(s): "
                    + ", ".join(invalid_algorithms)
                )
            }), 400

        comparison = {}

        for algorithm_name in selected_algorithms:
            result = ALGORITHMS[algorithm_name](pages, frames)

            history = enrich_history(
                result["history"], translations
            )

            comparison[algorithm_name] = {
                "algorithm": algorithm_name,
                "frames_count": frames,
                "total_references": result["total_references"],
                "page_hits": result["page_hits"],
                "page_faults": result["page_faults"],
                "hit_rate": result["hit_rate"],
                "fault_rate": result["fault_rate"],
                "history": history,
                "page_table": build_page_table(
                    result["history"][-1]["frames"]
                )
            }

        return jsonify({
            "message": "Algorithm comparison completed successfully.",
            "selected_algorithms": selected_algorithms,
            "translations": translations,
            "comparison": comparison
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
