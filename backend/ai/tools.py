from google.genai import types
from services.complaint_service import create_complaint, get_user_complaints
from services.mission_service import get_mission_status, list_user_missions
from services.reward_service import get_user_rewards, get_available_coupons
from services.duplicate_service import check_duplicate

def track_mission(mission_id: str, user_id: int = 1, user_role: str = "CITIZEN"):
    return get_mission_status(mission_id=mission_id, user_id=user_id, user_role=user_role)

def check_similar_complaints(category: str, description: str, latitude: float = None, longitude: float = None):
    return check_duplicate(category=category, latitude=latitude, longitude=longitude, description=description)

def get_rewards(user_id: int = 1):
    return get_user_rewards(user_id=user_id)

def find_coupons(user_id: int = 1):
    return get_available_coupons(user_id=user_id)

def prepare_complaint_draft(category: str, description: str, latitude: float = None, longitude: float = None, address: str = None, image_path: str = None):
    # Check for duplicates first
    dup_check = check_duplicate(category=category, latitude=latitude, longitude=longitude, description=description)
    return {
        "action": "DRAFT_COMPLAINT",
        "category": category,
        "description": description,
        "latitude": latitude,
        "longitude": longitude,
        "address": address or "Current citizen location",
        "image_path": image_path,
        "duplicate_alert": dup_check if dup_check.get("duplicate_candidate") else None,
        "ready_for_confirmation": True
    }

TOOLS_DECLARATION = [
    {
        "name": "track_mission",
        "description": "Retrieve authoritative real-time status, ward, assigned squad, and countdown deadline of a municipal mission.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "mission_id": {
                    "type": "STRING",
                    "description": "The numeric ID of the mission (e.g. 7042)."
                }
            },
            "required": ["mission_id"]
        }
    },
    {
        "name": "check_similar_complaints",
        "description": "Search active civic complaints near a geographic location to avoid submitting duplicates.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": "Civic category: garbage, drainage, pothole, water_leakage, broken_streetlight, illegal_dumping, road_damage"
                },
                "description": {
                    "type": "STRING",
                    "description": "Description of the problem."
                },
                "latitude": {
                    "type": "NUMBER",
                    "description": "GPS latitude."
                },
                "longitude": {
                    "type": "NUMBER",
                    "description": "GPS longitude."
                }
            },
            "required": ["category", "description"]
        }
    },
    {
        "name": "get_rewards",
        "description": "Get the current citizen's earned civic points and guardian badge level.",
        "parameters": {
            "type": "OBJECT",
            "properties": {}
        }
    },
    {
        "name": "find_coupons",
        "description": "List available local business reward coupons that citizens can redeem with their civic points.",
        "parameters": {
            "type": "OBJECT",
            "properties": {}
        }
    },
    {
        "name": "prepare_complaint_draft",
        "description": "Prepare a structured civic complaint draft for citizen verification before registration.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": "Category of the civic issue."
                },
                "description": {
                    "type": "STRING",
                    "description": "Detailed explanation of the issue."
                },
                "latitude": {
                    "type": "NUMBER",
                    "description": "Latitude if provided."
                },
                "longitude": {
                    "type": "NUMBER",
                    "description": "Longitude if provided."
                },
                "address": {
                    "type": "STRING",
                    "description": "Location description, street name or ward."
                }
            },
            "required": ["category", "description"]
        }
    }
]

