from datetime import datetime
from extensions import db

class Reward(db.Model):
    __tablename__ = "rewards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    points = db.Column(db.Integer, default=50)
    badge_level = db.Column(db.String(50), default="New Guardian") # New Guardian, Active Citizen, Civic Hero, Guardian Elite
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="rewards")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "points": self.points,
            "badge_level": self.badge_level,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(120), nullable=False)
    offer = db.Column(db.String(255), nullable=False)
    points_required = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "business": self.business_name,
            "business_name": self.business_name,
            "offer": self.offer,
            "points_required": self.points_required,
            "expiry_date": self.expiry_date.strftime("%Y-%m-%d") if self.expiry_date else "No Expiry",
            "is_active": self.is_active
        }

