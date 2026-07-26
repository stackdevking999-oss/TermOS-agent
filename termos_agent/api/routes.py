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


@api_bp.post("/test")
def run_test():
    payload = request.get_json(force=True, silent=True) or {}
    manifest_path = payload.get("manifest_path", "")
    result = Orchestrator().run_test_manifest(manifest_path)
    return jsonify({"success": result.success, "message": result.message, "data": result.data})


@api_bp.post("/reason")
def reason_about_request():
    payload = request.get_json(force=True, silent=True) or {}
    task = payload.get("task", "")
    result = Orchestrator().reason_about_request(task)
    return jsonify({"success": result.success, "message": result.message, "data": result.data})
