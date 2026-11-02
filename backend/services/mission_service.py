from datetime import datetime
from extensions import db
from models.mission import Mission
from models.user import User

def get_mission_status(mission_id, user_id=None, user_role="CITIZEN"):
    """
    Retrieve real-time mission status.
    Enforces authorization:
    - If user is CITIZEN: must own the linked complaint.
    - If user is MUNICIPAL_OFFICER or ADMIN: can view any mission.
    """
    try:
        mission_id = int(mission_id)
    except (ValueError, TypeError):
        return {
            "success": False,
            "message": f"Invalid mission ID: {mission_id}"
        }

    mission = Mission.query.filter_by(id=mission_id).first()
    if not mission:
        return {
            "success": False,
            "message": f"Mission #{mission_id} not found in database."
        }

    # Authorization Check
    if user_role not in ["MUNICIPAL_OFFICER", "ADMIN"]:
        if mission.complaint and user_id is not None and mission.complaint.user_id != user_id:
            return {
                "success": False,
                "message": f"Access denied: You are not authorized to view Mission #{mission_id}."
            }

    mission_data = mission.to_dict()
    updates = [u.to_dict() for u in mission.updates]
    mission_data["updates"] = updates

    return {
        "success": True,
        "mission_id": mission.id,
        "status": mission.status,
        "ward": mission_data["ward"],
        "team": mission.assigned_team,
        "deadline": mission_data["deadline"],
        "remaining_time": mission_data["remaining_time"],
        "remaining_seconds": mission_data["remaining_seconds"],
        "category": mission_data["category"],
        "description": mission_data["description"],
        "updates": updates
    }

def list_user_missions(user_id):
    """
    List all active missions for a citizen's complaints.
    """
    missions = (
        Mission.query.join(Mission.complaint)
        .filter(Mission.complaint.has(user_id=user_id))
        .all()
    )
    return [m.to_dict() for m in missions]

