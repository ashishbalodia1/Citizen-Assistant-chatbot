from datetime import datetime
from extensions import db

class Mission(db.Model):
    __tablename__ = "missions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey("complaints.id"), nullable=False, unique=True)
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.id"), nullable=False)
    assigned_team = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="ASSIGNED") # ASSIGNED, IN_PROGRESS, RESOLVED, INSPECTION_VERIFIED, CITIZEN_VERIFIED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaint = db.relationship("Complaint", back_populates="mission")
    ward = db.relationship("Ward", back_populates="missions")
    updates = db.relationship("MissionUpdate", back_populates="mission", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        remaining_seconds = 0
        if self.deadline:
            diff = (self.deadline - datetime.utcnow()).total_seconds()
            remaining_seconds = max(0, int(diff))

        days = remaining_seconds // 86400
        hours = (remaining_seconds % 86400) // 3600
        mins = (remaining_seconds % 3600) // 60
        remaining_str = f"{days} Days, {hours} Hours" if days > 0 else f"{hours} Hours, {mins} Mins"

        return {
            "mission_id": self.id,
            "complaint_id": self.complaint_id,
            "category": self.complaint.category if self.complaint else "Civic Issue",
            "description": self.complaint.description if self.complaint else "",
            "ward": self.ward.ward_name if self.ward else f"Ward #{self.ward_id}",
            "team": self.assigned_team,
            "status": self.status,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "remaining_time": remaining_str,
            "remaining_seconds": remaining_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class MissionUpdate(db.Model):
    __tablename__ = "mission_updates"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mission_id = db.Column(db.Integer, db.ForeignKey("missions.id"), nullable=False)
    update_text = db.Column(db.Text, nullable=False)
    evidence_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mission = db.relationship("Mission", back_populates="updates")

    def to_dict(self):
        return {
            "id": self.id,
            "mission_id": self.mission_id,
            "update_text": self.update_text,
            "evidence_path": self.evidence_path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

