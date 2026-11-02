from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from extensions import db
import models
from utils.auth import login_required
from utils.validators import is_valid_category, is_valid_coordinates
from services.complaint_service import create_complaint, get_user_complaints, get_complaint_by_id
from services.duplicate_service import check_duplicate

complaint_bp = Blueprint("complaints", __name__)

@complaint_bp.route("/complaints", methods=["POST"])
@login_required
def register_complaint():
    data = request.get_json() or {}
    user_id = getattr(request, "user_id", 1)

    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    address = data.get("address")
    image_path = data.get("image_path")
    severity = data.get("severity", "MEDIUM")

    if not category or not description:
        return jsonify({"success": False, "error": "Category and description are required"}), 400

    if not is_valid_coordinates(latitude, longitude):
        return jsonify({"success": False, "error": "Invalid GPS coordinates"}), 400

    result = create_complaint(
        user_id=user_id,
        category=category,
        description=description,
        latitude=latitude,
        longitude=longitude,
        image_path=image_path,
        address=address,
        severity=severity
    )

    if result.get("success"):
        return jsonify(result), 201
    return jsonify(result), 500

@complaint_bp.route("/complaints", methods=["GET"])
@login_required
def list_my_complaints():
    user_id = getattr(request, "user_id", 1)
    user_role = getattr(request, "user_role", "CITIZEN")

    if user_role in ["MUNICIPAL_OFFICER", "ADMIN"]:
        # Officer sees all complaints
        status_filter = request.args.get("status")
        query = models.Complaint.query.order_by(models.Complaint.created_at.desc())
        if status_filter:
            query = query.filter_by(status=status_filter)
        complaints = [c.to_dict() for c in query.all()]
    else:
        complaints = get_user_complaints(user_id=user_id)
        
    return jsonify({"success": True, "complaints": complaints})

@complaint_bp.route("/complaints/<int:complaint_id>", methods=["GET"])
@login_required
def get_complaint(complaint_id):
    user_id = getattr(request, "user_id", 1)
    user_role = getattr(request, "user_role", "CITIZEN")
    
    uid = user_id if user_role == "CITIZEN" else None
    complaint = get_complaint_by_id(complaint_id, user_id=uid)
    if not complaint:
        return jsonify({"success": False, "error": "Complaint not found or access denied"}), 404
        
    return jsonify({"success": True, "complaint": complaint})

@complaint_bp.route("/complaints/<int:complaint_id>/verify", methods=["POST"])
@login_required
def verify_complaint_by_officer(complaint_id):
    """
    Human Municipal Verification Workflow:
    Enforces that municipal officers must review and approve/reject complaints.
    """
    user_role = getattr(request, "user_role", "CITIZEN")
    if user_role not in ["MUNICIPAL_OFFICER", "ADMIN"]:
        return jsonify({"success": False, "error": "Unauthorized: Only municipal officers can verify complaints"}), 403

    complaint = models.Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify({"success": False, "error": "Complaint not found"}), 404

    data = request.get_json() or {}
    action = data.get("action", "APPROVE").upper() # APPROVE, REJECT, REWORK_REQUIRED, RESOLVE
    notes = data.get("notes", "Reviewed by municipal officer.")

    if action == "APPROVE":
        complaint.status = "APPROVED"
        # Check if mission already exists, else create one
        if not complaint.mission:
            ward_id = complaint.user.ward_id if (complaint.user and complaint.user.ward_id) else 1
            ward = models.Ward.query.get(ward_id)
            team_name = ward.team_name if ward else "Holkar Heroes"
            
            # 48 hour resolution deadline
            deadline = datetime.utcnow() + timedelta(days=2)
            mission = models.Mission(
                complaint_id=complaint.id,
                ward_id=ward_id,
                assigned_team=team_name,
                deadline=deadline,
                status="ASSIGNED"
            )
            db.session.add(mission)
            db.session.commit()
            
            # Initial update
            update = models.MissionUpdate(
                mission_id=mission.id,
                update_text=f"Municipal verification approved by Officer. Assigned to squad: {team_name}."
            )
            db.session.add(update)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": f"Complaint #{complaint_id} verified and approved. Mission #{mission.id} initiated.",
                "complaint_status": complaint.status,
                "mission_id": mission.id,
                "assigned_team": team_name
            })
            
    elif action == "REJECT":
        complaint.status = "REJECTED"
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Complaint #{complaint_id} rejected with reason: {notes}",
            "complaint_status": complaint.status
        })
        
    elif action == "RESOLVE":
        complaint.status = "RESOLVED"
        if complaint.mission:
            complaint.mission.status = "RESOLVED"
            update = models.MissionUpdate(
                mission_id=complaint.mission.id,
                update_text=f"Resolution verified by Municipal Inspection Officer: {notes}"
            )
            db.session.add(update)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Complaint #{complaint_id} marked as RESOLVED and inspection verified.",
            "complaint_status": complaint.status
        })

    db.session.commit()
    return jsonify({"success": True, "complaint_status": complaint.status})

@complaint_bp.route("/complaints/check-duplicate", methods=["POST"])
@login_required
def check_duplicate_route():
    data = request.get_json() or {}
    category = data.get("category", "")
    description = data.get("description", "")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    res = check_duplicate(
        category=category,
        latitude=latitude,
        longitude=longitude,
        description=description
    )
    return jsonify(res)
