import os
from datetime import datetime, timedelta
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from config import Config
from extensions import db
from routes.chat_routes import chat_bp
from routes.upload_routes import upload_bp
from routes.complaint_routes import complaint_bp
from routes.mission_routes import mission_bp
from routes.reward_routes import reward_bp
from utils.auth import generate_token
import models

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup CORS for Vite React frontend
    CORS(
        app,
        origins=[app.config["FRONTEND_URL"], "http://localhost:5173", "http://127.0.0.1:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"]
    )

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(complaint_bp, url_prefix="/api")
    app.register_blueprint(mission_bp, url_prefix="/api")
    app.register_blueprint(reward_bp, url_prefix="/api")

    # Static uploads handler
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Health check
    @app.route("/")
    def index():
        return jsonify({
            "service": "CITY GUARDIAN AI - Civic Complaint Assistant Backend",
            "status": "online",
            "version": "2.0",
            "endpoints": {
                "health": "/health",
                "chat": "POST /api/chat",
                "complaints": "/api/complaints",
                "missions": "/api/missions/<id>",
                "rewards": "/api/rewards",
                "coupons": "/api/coupons",
                "image_upload": "POST /api/upload/image",
                "voice_upload": "POST /api/upload/voice"
            },
            "frontend_ui": app.config.get("FRONTEND_URL", "http://localhost:5173"),
            "timestamp": datetime.utcnow().isoformat()
        })

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "CITY GUARDIAN AI",
            "timestamp": datetime.utcnow().isoformat()
        })

    # Auth helper endpoint for frontend or test suites
    @app.route("/api/auth/token", methods=["POST"])
    def get_demo_token():
        data = request.get_json() or {}
        user_id = int(data.get("user_id", 1))
        user = models.User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        token = generate_token(user_id=user.id, role=user.role)
        return jsonify({
            "success": True,
            "access_token": token,
            "user": user.to_dict()
        })

    # Initialize and seed database if empty
    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app

def seed_initial_data():
    # Only seed if no wards exist
    if models.Ward.query.first():
        return

    print("Initializing City Guardian database with seed data...")
    # Wards
    w1 = models.Ward(id=1, ward_name="Ward 7 - Civil Lines", team_name="Holkar Heroes")
    w2 = models.Ward(id=2, ward_name="Ward 12 - Old City", team_name="Shivaji Squad")
    w3 = models.Ward(id=3, ward_name="Ward 4 - Metro West", team_name="Green Sentinels")
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    # Users
    u1 = models.User(id=1, name="Rahul Sharma", phone="9876543210", email="rahul.sharma@example.com", ward_id=1, role="CITIZEN")
    u2 = models.User(id=2, name="Priya Verma", phone="9876543211", email="priya.verma@example.com", ward_id=1, role="CITIZEN")
    u3 = models.User(id=3, name="Officer Gupta", phone="9876543212", email="officer.gupta@citygov.in", ward_id=1, role="MUNICIPAL_OFFICER")
    db.session.add_all([u1, u2, u3])
    db.session.commit()

    # Rewards
    r1 = models.Reward(user_id=1, points=180, badge_level="Active Citizen")
    r2 = models.Reward(user_id=2, points=75, badge_level="New Guardian")
    db.session.add_all([r1, r2])

    # Coupons
    c1 = models.Coupon(business_name="GreenLeaf Nursery", offer="25% Off on Plants & Garden Composts", points_required=50, expiry_date=datetime.utcnow() + timedelta(days=60), is_active=True)
    c2 = models.Coupon(business_name="Metro Smart Mobility", offer="Free Day Pass on City Electric Buses", points_required=100, expiry_date=datetime.utcnow() + timedelta(days=30), is_active=True)
    c3 = models.Coupon(business_name="Cafe Chai & Co", offer="Free Ginger Tea + Samosa with any combo", points_required=40, expiry_date=datetime.utcnow() + timedelta(days=45), is_active=True)
    c4 = models.Coupon(business_name="City Heritage Bookshop", offer="15% Off on Books & Stationery", points_required=80, expiry_date=datetime.utcnow() + timedelta(days=60), is_active=True)
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    # Complaints
    comp1 = models.Complaint(
        id=101,
        user_id=1,
        category="drainage",
        description="Main drainage pipe leaking foul water onto street near market",
        latitude=28.6139,
        longitude=77.2090,
        address="Sector 4, Main Market, Ward 7",
        image_path=None,
        severity="HIGH",
        status="IN_PROGRESS"
    )
    comp2 = models.Complaint(
        id=102,
        user_id=2,
        category="pothole",
        description="Deep pothole causing traffic jam near flyover pillar 14",
        latitude=28.6145,
        longitude=77.2100,
        address="Flyover Road, Pillar 14",
        image_path=None,
        severity="MEDIUM",
        status="APPROVED"
    )
    db.session.add_all([comp1, comp2])
    db.session.commit()

    # Missions
    m1 = models.Mission(
        id=7042,
        complaint_id=101,
        ward_id=1,
        assigned_team="Holkar Heroes",
        deadline=datetime.utcnow() + timedelta(days=2, hours=4),
        status="IN_PROGRESS"
    )
    m2 = models.Mission(
        id=7043,
        complaint_id=102,
        ward_id=1,
        assigned_team="Shivaji Squad",
        deadline=datetime.utcnow() + timedelta(days=1, hours=8),
        status="ASSIGNED"
    )
    db.session.add_all([m1, m2])
    db.session.commit()

    # Mission Update
    up1 = models.MissionUpdate(
        mission_id=7042,
        update_text="Maintenance team dispatched with suction pump truck.",
        created_at=datetime.utcnow()
    )
    db.session.add(up1)
    db.session.commit()
    print("Database seeding completed.")

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)

