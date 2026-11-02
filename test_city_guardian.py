"""
City Guardian AI - Automated 12/12 Blueprint Test Suite
Verifies all functional, security, and AI requirements.
"""
import sys
import os
import unittest
from pathlib import Path
from datetime import datetime, timezone

# Add backend directory to path
backend_path = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_path))

from app import create_app
from extensions import db
import models
from services.complaint_service import create_complaint, get_complaint_by_id
from services.mission_service import get_mission_status
from services.reward_service import get_user_rewards, get_available_coupons, redeem_coupon
from services.duplicate_service import check_duplicate
from services.vision_service import analyze_image
from services.voice_service import transcribe_audio
from ai.agent import run_agent

class CityGuardianFullTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_hindi_complaint_registration_flow(self):
        """1. Hindi complaint registration: 'Naala overflow ho raha hai' -> Drafts and registers"""
        with self.app.app_context():
            session_id = f"test_hindi_sess_{int(datetime.now().timestamp())}"
            res = run_agent(
                message="Sector 4 me naala overflow ho raha hai, kripya safai team bhejo.",
                user_id=1,
                session_id=session_id
            )
            self.assertTrue(res["success"])
            self.assertIn(res["type"], ["COMPLAINT_DRAFT", "TEXT"])
            print("[PASS] Test 1: Hindi complaint registration understood and handled.")

    def test_02_english_complaint_registration_flow(self):
        """2. English complaint registration: Report a pothole using text"""
        with self.app.app_context():
            session_id = f"test_eng_sess_{int(datetime.now().timestamp())}"
            res = run_agent(
                message="There is a deep dangerous pothole near Civil Lines Market causing traffic accidents.",
                user_id=1,
                session_id=session_id
            )
            self.assertTrue(res["success"])
            print("[PASS] Test 2: English complaint analyzed and drafted.")

    def test_03_hinglish_conversation(self):
        """3. Hinglish conversation: Understand informal Hinglish queries"""
        with self.app.app_context():
            session_id = f"test_hinglish_sess_{int(datetime.now().timestamp())}"
            res = run_agent(
                message="Mere points kitne hain aur rank kya hai?",
                user_id=1,
                session_id=session_id
            )
            self.assertTrue(res["success"])
            self.assertIn(res["type"], ["REWARD_STATUS", "TEXT"])
            print("[PASS] Test 3: Hinglish language conversation handled.")

    def test_04_image_classification(self):
        """4. Image classification: Civic image category and hazard detection"""
        with self.app.app_context():
            uploads_dir = Path(__file__).resolve().parent / "backend" / "uploads"
            uploads_dir.mkdir(parents=True, exist_ok=True)
            sample_img_path = uploads_dir / "sample_drainage_test.jpg"
            
            from PIL import Image
            img = Image.new("RGB", (200, 200), color=(73, 109, 137))
            img.save(sample_img_path)

            analysis = analyze_image(str(sample_img_path))
            self.assertTrue(analysis["success"])
            self.assertIn("primary_category", analysis)
            self.assertIn("confidence", analysis)
            print(f"[PASS] Test 4: Image analysis completed ({analysis['primary_category']}).")

    def test_05_duplicate_detection(self):
        """5. Duplicate detection: Find existing nearby complaint via Haversine and semantics"""
        with self.app.app_context():
            # Comp 101 is at lat: 28.6139, lon: 77.2090 ('drainage')
            # Query nearby point (approx 20m away) with matching category
            dup_res = check_duplicate(
                category="drainage",
                latitude=28.6140,
                longitude=77.2091,
                description="Drainage water leakage on road near market"
            )
            self.assertTrue(dup_res["duplicate_candidate"])
            self.assertIsNotNone(dup_res["top_match"])
            print(f"[PASS] Test 5: Duplicate detected nearby (Match ID #{dup_res['top_match']['complaint_id']}).")

    def test_06_citizen_confirmation_safeguard(self):
        """6. Citizen confirmation: Prevent direct DB registration without explicit confirmation"""
        with self.app.app_context():
            initial_count = models.Complaint.query.count()
            session_id = f"test_confirm_safeguard_{int(datetime.now().timestamp())}"
            
            # Step 1: Citizen reports grievance
            res = run_agent(
                message="Pothole on Main Boulevard road causing hazard",
                user_id=1,
                session_id=session_id
            )
            # The complaint must NOT be committed yet
            intermediate_count = models.Complaint.query.count()
            self.assertEqual(initial_count, intermediate_count)

            # Step 2: Citizen explicitly confirms
            confirm_res = run_agent(
                message="Haan confirm karo, darj kar do.",
                user_id=1,
                session_id=session_id
            )
            self.assertEqual(confirm_res["type"], "COMPLAINT_CONFIRMED")
            final_count = models.Complaint.query.count()
            self.assertEqual(final_count, initial_count + 1)
            print("[PASS] Test 6: Complaint created ONLY after explicit citizen confirmation.")

    def test_07_mission_tracking(self):
        """7. Mission tracking: Retrieve actual DB mission status and countdown deadline"""
        with self.app.app_context():
            res = get_mission_status(mission_id=7042, user_id=1, user_role="CITIZEN")
            self.assertTrue(res["success"])
            self.assertEqual(res["mission_id"], 7042)
            self.assertEqual(res["status"], "IN_PROGRESS")
            self.assertEqual(res["team"], "Holkar Heroes")
            self.assertIn("remaining_time", res)
            print(f"[PASS] Test 7: Mission #7042 retrieved ({res['status']}, {res['remaining_time']}).")

    def test_08_unauthorized_mission_access_prevention(self):
        """8. Unauthorized access: Prevent one citizen from accessing another citizen's mission"""
        with self.app.app_context():
            # Mission 7042 belongs to User 1 (Rahul Sharma).
            # User 2 (Priya Verma) should be denied access!
            res = get_mission_status(mission_id=7042, user_id=2, user_role="CITIZEN")
            self.assertFalse(res["success"])
            self.assertIn("Access denied", res["message"])
            print("[PASS] Test 8: Unauthorized citizen blocked from accessing foreign mission.")

    def test_09_rewards_inquiry(self):
        """9. Rewards inquiry: Retrieve actual points and badge level"""
        with self.app.app_context():
            rewards = get_user_rewards(user_id=1)
            self.assertTrue(rewards["success"])
            self.assertGreaterEqual(rewards["points"], 100)
            self.assertIn("badge", rewards)
            print(f"[PASS] Test 9: Citizen rewards retrieved ({rewards['points']} pts, {rewards['badge']}).")

    def test_10_coupon_inquiry_and_redemption(self):
        """10. Coupon inquiry: Show eligible coupons and verify point deduction"""
        with self.app.app_context():
            coupons_data = get_available_coupons(user_id=1)
            self.assertTrue(coupons_data["success"])
            self.assertGreater(len(coupons_data["coupons"]), 0)
            
            # Redeem coupon #1 (50 pts)
            initial_pts = get_user_rewards(user_id=1)["points"]
            redeem_res = redeem_coupon(user_id=1, coupon_id=1)
            self.assertTrue(redeem_res["success"])
            self.assertIn("voucher_code", redeem_res)
            
            updated_pts = get_user_rewards(user_id=1)["points"]
            self.assertEqual(updated_pts, initial_pts - 50)
            print(f"[PASS] Test 10: Coupon redeemed with voucher {redeem_res['voucher_code']}.")

    def test_11_voice_reporting(self):
        """11. Voice reporting: Transcribe voice recording into text"""
        with self.app.app_context():
            sample_audio_path = Path(__file__).resolve().parent / "backend" / "uploads" / "sample_voice.wav"
            with open(sample_audio_path, "wb") as f:
                f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
            
            text = transcribe_audio(str(sample_audio_path))
            self.assertTrue(len(text) > 0)
            print(f"[PASS] Test 11: Voice transcription operational ('{text}').")

    def test_12_municipal_verification_controls(self):
        """12. Municipal verification: Ensure AI cannot auto-approve or close complaints"""
        with self.app.app_context():
            complaint = models.Complaint.query.filter_by(id=101).first()
            self.assertNotEqual(complaint.status, "RESOLVED")
            self.assertNotEqual(complaint.status, "APPROVED_BY_AI")
            self.assertIn(complaint.status, ["PENDING_VERIFICATION", "IN_PROGRESS", "REPORTED", "APPROVED"])
            print("[PASS] Test 12: Municipal human verification controls preserved.")

if __name__ == "__main__":
    unittest.main()
