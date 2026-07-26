from flask import Blueprint, jsonify, request

from termos_agent.core.orchestrator import Orchestrator

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    result = Orchestrator().handle("health-check")
    return jsonify({"success": result.success, "message": result.message, "data": result.data})


@api_bp.post("/run")
def run_task():
    payload = request.get_json(force=True, silent=True) or {}
    task = payload.get("task", "")
    result = Orchestrator().handle(task)
    return jsonify({"success": result.success, "message": result.message, "data": result.data})
