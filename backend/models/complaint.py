from datetime import datetime
from extensions import db

class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False) # garbage, drainage, pothole, water_leakage, broken_streetlight, illegal_dumping, other
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    severity = db.Column(db.String(50), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    status = db.Column(db.String(50), default="PENDING_VERIFICATION")
    # Lifecycle: REPORTED, AI_ANALYZED, PENDING_VERIFICATION, APPROVED, ASSIGNED, IN_PROGRESS, RESOLVED, INSPECTION_VERIFIED, CITIZEN_VERIFIED, REJECTED, DUPLICATE, DISPUTED, REWORK_REQUIRED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="complaints")
    mission = db.relationship("Mission", back_populates="complaint", uselist=False, lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category": self.category,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "image_path": self.image_path,
            "severity": self.severity,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

