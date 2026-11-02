"""
City Guardian AI - Real-World Citizen Queries & Stress Test Script
Simulates realistic citizen messages across Hindi, English, Hinglish,
duplicate detection, mission tracking, rewards, and human-in-the-loop confirmation.
"""
import sys
import json
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_path))

from app import create_app
from extensions import db
import models
from ai.agent import run_agent
from services.vision_service import analyze_image
from services.voice_service import transcribe_audio

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f" {title.upper()} ")
        print("=" * 70)

def simulate_query(app, test_num, title, user_id, user_role, session_id, message, coordinates=None):
    print(f"\n--- [Query #{test_num}] {title} ---")
    print(f"Citizen (User #{user_id}): \"{message}\"")
    if coordinates:
        print(f"GPS Attached: {coordinates}")

    with app.app_context():
        res = run_agent(
            message=message,
            user_id=user_id,
            user_role=user_role,
            session_id=session_id,
            coordinates=coordinates
        )

        print("\nCity Guardian AI Response:")
        print(res["response"])
        print(f"\nResponse Card Type: {res.get('type')}")
        if res.get("data"):
            print("Structured Card Data Preview:")
            for k, v in list(res["data"].items())[:4]:
                print(f"  - {k}: {v}")
        return res

def main():
    app = create_app()

    print_separator("CITY GUARDIAN AI - REAL WORLD SCENARIO TESTING")

    # =========================================================================
    # Scenario 1: Pure Hindi Garbage Grievance (Registration Draft)
    # =========================================================================
    sess_1 = "real_world_sess_rahul_1"
    simulate_query(
        app=app,
        test_num=1,
        title="Pure Hindi Garbage Complaint",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_1,
        message="Hamare ghar ke samne kachre ka dher laga hua hai aur bahut badboo aa rahi hai, kripya safai team bhejo.",
        coordinates={"latitude": 28.6180, "longitude": 77.2150}
    )

    # =========================================================================
    # Scenario 2: Citizen Confirmation (Human-in-the-Loop)
    # =========================================================================
    simulate_query(
        app=app,
        test_num=2,
        title="Citizen Explicit Confirmation ('Haan, darj kar do')",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_1,
        message="Haan theek hai, confirm kar do."
    )

    # =========================================================================
    # Scenario 3: Real-Time Mission Tracking by Complaint Owner (Rahul Sharma)
    # =========================================================================
    sess_2 = "real_world_sess_rahul_2"
    simulate_query(
        app=app,
        test_num=3,
        title="Tracking Active Mission #7042 (Assigned Squad & Remaining Time)",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_2,
        message="Mera mission number 7042 kahan tak pahuncha? Kab tak theek hoga?"
    )

    # =========================================================================
    # Scenario 4: Security Check - Unauthorized Mission Access
    # (Priya Verma tries to access Rahul Sharma's Mission 7042)
    # =========================================================================
    sess_3 = "real_world_sess_priya"
    simulate_query(
        app=app,
        test_num=4,
        title="Security & Privacy: Unauthorized Citizen queries Foreign Mission",
        user_id=2, # User 2 is Priya
        user_role="CITIZEN",
        session_id=sess_3,
        message="Check status of mission #7042"
    )

    # =========================================================================
    # Scenario 5: Duplicate Complaint Detection (Drainage overflow near existing issue)
    # Comp 101 is at lat: 28.6139, lon: 77.2090
    # =========================================================================
    sess_4 = "real_world_sess_dup"
    simulate_query(
        app=app,
        test_num=5,
        title="Duplicate Complaint Detection (Same spot drainage leakage)",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_4,
        message="Sector 4 Main market road par nali ka ganda pani sadak par beh raha hai.",
        coordinates={"latitude": 28.6140, "longitude": 77.2091}
    )

    # =========================================================================
    # Scenario 6: Citizen Points & Badges Inquiry in Hinglish
    # =========================================================================
    sess_5 = "real_world_sess_rewards"
    simulate_query(
        app=app,
        test_num=6,
        title="Citizen Points & Guardian Badges Inquiry",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_5,
        message="Bhai mere total points kitne hue hain aur mera badge kya hai?"
    )

    # =========================================================================
    # Scenario 7: Local Business Coupons & Rewards Inquiry
    # =========================================================================
    simulate_query(
        app=app,
        test_num=7,
        title="Local Partner Rewards & Coupons Inquiry",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_5,
        message="Kya points se koi coupon ya discount redeem kar sakta hoon?"
    )

    # =========================================================================
    # Scenario 8: English Pothole Report with Danger keywords
    # =========================================================================
    sess_6 = "real_world_sess_english"
    simulate_query(
        app=app,
        test_num=8,
        title="English Road Hazard Report",
        user_id=1,
        user_role="CITIZEN",
        session_id=sess_6,
        message="There is a deep dangerous pothole near Civil Lines Metro pillar 14 causing vehicle damage.",
        coordinates={"latitude": 28.6250, "longitude": 77.2200}
    )

    # =========================================================================
    # Scenario 9: Image Evidence Analysis Test
    # =========================================================================
    print_separator("TEST SCENARIO 9: CIVIC IMAGE EVIDENCE ANALYSIS")
    with app.app_context():
        uploads_dir = Path(__file__).resolve().parent / "backend" / "uploads"
        test_img = uploads_dir / "sample_pothole_evidence.jpg"
        from PIL import Image
        img = Image.new("RGB", (300, 300), color=(100, 80, 70))
        img.save(test_img)

        analysis = analyze_image(str(test_img))
        print(f"Uploaded Image: {test_img.name}")
        print(f"Identified Civic Category: {analysis.get('primary_category')}")
        print(f"Confidence Score: {int((analysis.get('confidence') or 0.85)*100)}%")
        print(f"Severity Assessment: {analysis.get('severity')}")
        print(f"Observation Summary: {analysis.get('summary')}")
        print(f"Hazards: {analysis.get('hazards')}")

    # =========================================================================
    # Scenario 10: Voice Reporting Simulation
    # =========================================================================
    print_separator("TEST SCENARIO 10: VOICE NOTE REPORTING")
    with app.app_context():
        voice_file = uploads_dir / "sample_hindi_voice.wav"
        with open(voice_file, "wb") as f:
            f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
        transcription = transcribe_audio(str(voice_file))
        print(f"Audio File: {voice_file.name}")
        print(f"Transcribed Text (Hindi/Hinglish): \"{transcription}\"")

    print_separator("ALL REAL-WORLD TEST SCENARIOS COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()

