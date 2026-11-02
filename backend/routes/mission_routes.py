from flask import Blueprint, request, jsonify
from utils.auth import login_required
from services.mission_service import get_mission_status, list_user_missions

mission_bp = Blueprint("missions", __name__)

@mission_bp.route("/missions/<int:mission_id>", methods=["GET"])
@login_required
def track_mission_endpoint(mission_id):
    user_id = getattr(request, "user_id", 1)
    user_role = getattr(request, "user_role", "CITIZEN")

    result = get_mission_status(
        mission_id=mission_id,
        user_id=user_id,
        user_role=user_role
    )

    if not result.get("success"):
        status_code = 403 if "Access denied" in result.get("message", "") else 404
        return jsonify(result), status_code

    return jsonify(result)

@mission_bp.route("/missions", methods=["GET"])
@login_required
def list_missions_endpoint():
    user_id = getattr(request, "user_id", 1)
    missions = list_user_missions(user_id=user_id)
    return jsonify({"success": True, "missions": missions})

