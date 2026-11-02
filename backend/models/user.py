from datetime import datetime
from extensions import db

class Ward(db.Model):
    __tablename__ = "wards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ward_name = db.Column(db.String(100), nullable=False)
    team_name = db.Column(db.String(100), nullable=False)

    users = db.relationship("User", back_populates="ward", lazy=True)
    missions = db.relationship("Mission", back_populates="ward", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ward_name": self.ward_name,
            "team_name": self.team_name
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"), nullable=True)
    role = db.Column(db.String(50), default="CITIZEN") # CITIZEN, MUNICIPAL_OFFICER, ADMIN
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ward = db.relationship("Ward", back_populates="users")
    complaints = db.relationship("Complaint", back_populates="user", lazy=True)
    rewards = db.relationship("Reward", back_populates="user", uselist=False, lazy=True)
    conversations = db.relationship("Conversation", back_populates="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "ward_id": self.ward_id,
            "role": self.role
        }

