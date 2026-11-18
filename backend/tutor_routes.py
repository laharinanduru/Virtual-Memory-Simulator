
from flask import Blueprint, request, jsonify

from bots import (
    virtual_memory_tutor,
    generate_virtual_memory_report
)

# Create a separate group of Flask routes
tutor_bp = Blueprint("tutor", __name__)


# 1. AI Tutor API
@tutor_bp.route("/api/tutor", methods=["POST"])
def tutor():
    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        answer = virtual_memory_tutor(question)
        return jsonify({"answer": answer}), 200

    except Exception as error:
        return jsonify({"error": "Tutor could not generate an answer."}), 500


# 2. AI Report Generator API
@tutor_bp.route("/api/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json(silent=True) or {}

    topic = data.get("topic", "").strip()
    requirements = data.get("requirements", "").strip()

    if not topic:
        return jsonify({"error": "Please enter a report topic."}), 400

    try:
        report = generate_virtual_memory_report(
            topic,
            requirements
        )
        return jsonify({"report": report}), 200

    except Exception as error:
        return jsonify({"error": "Report generation failed."}), 500
