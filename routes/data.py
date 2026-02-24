from flask import Blueprint, request, jsonify
from services.data_service import ingest_data, get_records
from logger import setup_logger

data_bp = Blueprint("data", __name__)
logger = setup_logger()

@data_bp.route("/ingest", methods=["POST"])
def ingest():
    body = request.get_json()
    if not body or "source" not in body or "records" not in body:
        return jsonify({"error": "source and records are required"}), 400
    if not isinstance(body["records"], list) or len(body["records"]) == 0:
        return jsonify({"error": "records must be a non-empty list"}), 422
    try:
        result = ingest_data(body["source"], body["records"])
        logger.info(f"Ingested {len(body['records'])} records from {body['source']}")
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}")
        return jsonify({"error": "Ingestion failed", "detail": str(e)}), 500

@data_bp.route("/records", methods=["GET"])
def records():
    source = request.args.get("source")
    try:
        data = get_records(source)
        return jsonify({"count": len(data), "records": data}), 200
    except Exception as e:
        logger.error(f"Failed to fetch records: {str(e)}")
        return jsonify({"error": "Failed to fetch records"}), 500
