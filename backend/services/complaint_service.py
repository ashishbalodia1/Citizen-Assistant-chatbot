from datetime import datetime
from extensions import db
from models.complaint import Complaint
from models.user import User
from models.reward import Reward

def create_complaint(user_id, category, description, latitude=None, longitude=None, image_path=None, address=None, severity="MEDIUM"):
    """
    Creates a new civic complaint with PENDING_VERIFICATION status.
    Award initial citizen reward points (+15 pts for reporting civic issues).
    """
    try:
        complaint = Complaint(
            user_id=user_id,
            category=category.lower().strip() if category else "other",
            description=description.strip(),
            latitude=float(latitude) if latitude is not None else None,
            longitude=float(longitude) if longitude is not None else None,
            address=address,
            image_path=image_path,
            severity=severity or "MEDIUM",
            status="PENDING_VERIFICATION",
            created_at=datetime.utcnow()
        )
        db.session.add(complaint)
        
        # Award citizen points
        reward = Reward.query.filter_by(user_id=user_id).first()
        if reward:
            reward.points += 15
            if reward.points >= 250:
                reward.badge_level = "Civic Hero"
            elif reward.points >= 100:
                reward.badge_level = "Active Citizen"
        else:
            reward = Reward(user_id=user_id, points=65, badge_level="New Guardian")
            db.session.add(reward)
            
        db.session.commit()
        
        return {
            "success": True,
            "complaint_id": complaint.id,
            "status": complaint.status,
            "category": complaint.category,
            "description": complaint.description,
            "reward_points_earned": 15
        }
    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "error": str(e)
        }

def get_complaint_by_id(complaint_id, user_id=None):
    query = Complaint.query.filter_by(id=complaint_id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    complaint = query.first()
    return complaint.to_dict() if complaint else None

def get_user_complaints(user_id, limit=10):
    complaints = Complaint.query.filter_by(user_id=user_id).order_by(Complaint.created_at.desc()).limit(limit).all()
    return [c.to_dict() for c in complaints]

