from flask import Blueprint, request, jsonify
from services.workflow_service import execute_workflow, get_workflow_status
from logger import setup_logger

workflow_bp = Blueprint("workflow", __name__)
logger = setup_logger()

@workflow_bp.route("/execute", methods=["POST"])
def execute():
    body = request.get_json()
    if not body or "workflow_id" not in body or "steps" not in body:
        logger.warning("Invalid workflow execution request")
        return jsonify({"error": "workflow_id and steps are required"}), 400
    try:
        result = execute_workflow(body["workflow_id"], body["steps"])
        logger.info(f"Workflow {body['workflow_id']} executed successfully")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        return jsonify({"error": "Workflow execution failed", "detail": str(e)}), 500

@workflow_bp.route("/status/<workflow_id>", methods=["GET"])
def status(workflow_id):
    try:
        result = get_workflow_status(workflow_id)
        if not result:
            return jsonify({"error": "Workflow not found"}), 404
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Status fetch failed for {workflow_id}: {str(e)}")
        return jsonify({"error": "Failed to fetch status"}), 500
