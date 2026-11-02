from flask import Blueprint, request, jsonify
from utils.auth import login_required
from services.reward_service import get_user_rewards, get_available_coupons, redeem_coupon

reward_bp = Blueprint("rewards", __name__)

@reward_bp.route("/rewards", methods=["GET"])
@login_required
def get_rewards_endpoint():
    user_id = getattr(request, "user_id", 1)
    result = get_user_rewards(user_id=user_id)
    return jsonify(result)

@reward_bp.route("/coupons", methods=["GET"])
@login_required
def get_coupons_endpoint():
    user_id = getattr(request, "user_id", 1)
    result = get_available_coupons(user_id=user_id)
    return jsonify(result)

@reward_bp.route("/coupons/redeem", methods=["POST"])
@login_required
def redeem_coupon_endpoint():
    user_id = getattr(request, "user_id", 1)
    data = request.get_json() or {}
    coupon_id = data.get("coupon_id")
    if not coupon_id:
        return jsonify({"success": False, "message": "coupon_id is required"}), 400

    result = redeem_coupon(user_id=user_id, coupon_id=coupon_id)
    if not result.get("success"):
        return jsonify(result), 400
    return jsonify(result)

