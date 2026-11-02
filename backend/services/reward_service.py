from datetime import datetime
from extensions import db
from models.reward import Reward, Coupon
from models.user import User

def get_user_rewards(user_id):
    """
    Retrieve citizen points and badge level.
    """
    reward = Reward.query.filter_by(user_id=user_id).first()
    if not reward:
        reward = Reward(user_id=user_id, points=50, badge_level="New Guardian")
        db.session.add(reward)
        db.session.commit()
    
    return {
        "success": True,
        "points": reward.points,
        "badge": reward.badge_level,
        "badge_level": reward.badge_level,
        "user_id": user_id
    }

def get_available_coupons(user_id=None):
    """
    Retrieve active, eligible civic reward coupons.
    """
    user_points = 0
    if user_id:
        reward = Reward.query.filter_by(user_id=user_id).first()
        if reward:
            user_points = reward.points

    coupons = Coupon.query.filter(Coupon.is_active == True).all()
    results = []
    for c in coupons:
        data = c.to_dict()
        data["eligible"] = user_points >= c.points_required
        data["points_needed"] = max(0, c.points_required - user_points)
        results.append(data)
        
    return {
        "success": True,
        "user_points": user_points,
        "coupons": results
    }

def redeem_coupon(user_id, coupon_id):
    """
    Deduct points and return coupon voucher code.
    """
    reward = Reward.query.filter_by(user_id=user_id).first()
    if not reward:
        return {"success": False, "message": "User reward account not found"}
        
    coupon = Coupon.query.filter_by(id=coupon_id, is_active=True).first()
    if not coupon:
        return {"success": False, "message": "Coupon not found or expired"}
        
    if reward.points < coupon.points_required:
        return {
            "success": False,
            "message": f"Insufficient points ({reward.points}/{coupon.points_required} required)"
        }
        
    reward.points -= coupon.points_required
    db.session.commit()
    
    voucher_code = f"CG-{coupon.id}-{user_id}-{datetime.utcnow().strftime('%m%d%H%M')}"
    return {
        "success": True,
        "voucher_code": voucher_code,
        "coupon": coupon.to_dict(),
        "remaining_points": reward.points
    }

