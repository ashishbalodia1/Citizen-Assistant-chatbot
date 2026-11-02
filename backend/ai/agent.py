import json
import os
import re
from datetime import datetime
from google import genai
from google.genai import types
from ai.gemini_client import client, MODEL
from ai.prompts import SYSTEM_PROMPT
from ai.tools import (
    TOOLS_DECLARATION,
    track_mission,
    check_similar_complaints,
    get_rewards,
    find_coupons,
    prepare_complaint_draft
)
from ai.intent import detect_quick_intent, extract_mission_id
from ai.response_parser import build_structured_response
from services.complaint_service import create_complaint
from models.conversation import Conversation, ChatMessage
from extensions import db

FUNCTION_MAP = {
    "track_mission": track_mission,
    "check_similar_complaints": check_similar_complaints,
    "get_rewards": get_rewards,
    "find_coupons": find_coupons,
    "prepare_complaint_draft": prepare_complaint_draft
}

def get_or_create_conversation(user_id: int, session_id: str = None):
    if not session_id:
        session_id = f"sess_{user_id}_{int(datetime.utcnow().timestamp())}"
    
    convo = Conversation.query.filter_by(session_id=session_id).first()
    if not convo:
        convo = Conversation(user_id=user_id, session_id=session_id, state_json="{}")
        db.session.add(convo)
        db.session.commit()
    return convo

def detect_civic_category(text: str):
    t = text.lower()
    if any(k in t for k in ["drain", "naala", "sewage", "gutter", "drainage", "pipe"]):
        return "drainage"
    if any(k in t for k in ["pothole", "gaddha", "road", "sadak", "asphalt"]):
        return "pothole"
    if any(k in t for k in ["garbage", "kachra", "dustbin", "waste", "dump"]):
        return "garbage"
    if any(k in t for k in ["light", "streetlight", "batti", "pole", "dark"]):
        return "broken_streetlight"
    if any(k in t for k in ["water", "pani", "leak", "pipeline"]):
        return "water_leakage"
    return "other"

def run_agent(message: str, user_id: int = 1, user_role: str = "CITIZEN", session_id: str = None, coordinates: dict = None):
    """
    City Guardian AI Multi-turn Orchestrator with Function Calling and Human-in-the-Loop Controls.
    """
    convo = get_or_create_conversation(user_id, session_id)
    session_id = convo.session_id
    state = convo.get_state()

    # Save user message
    user_msg_record = ChatMessage(conversation_id=convo.id, role="user", message=message)
    db.session.add(user_msg_record)
    db.session.commit()

    quick_intent = detect_quick_intent(message)

    # 1. Handle Human-in-the-Loop Complaint Confirmation
    if state.get("pending_action") == "CONFIRM_COMPLAINT" and state.get("complaint_draft"):
        draft = state.get("complaint_draft")
        if quick_intent == "CONFIRM_COMPLAINT" or any(w in message.lower() for w in ["confirm", "haan", "yes", "kar do", "theek hai"]):
            # Explicit confirmation received! Execute authoritative creation in DB
            res = create_complaint(
                user_id=user_id,
                category=draft.get("category", "other"),
                description=draft.get("description", "Civic grievance reported"),
                latitude=draft.get("latitude"),
                longitude=draft.get("longitude"),
                address=draft.get("address"),
                image_path=draft.get("image_path")
            )
            state["pending_action"] = None
            state["complaint_draft"] = None
            convo.set_state(state)
            db.session.commit()

            if res.get("success"):
                reply_text = (
                    f"Dhanyawad! Aapki shikayat safalta-purvak darj kar li gayi hai.\n\n"
                    f"**Complaint ID:** #{res['complaint_id']}\n"
                    f"**Status:** {res['status']} (Municipal verification awaited)\n"
                    f"**Rewards Earned:** +15 Citizen Points awarded to your profile!"
                )
                assistant_record = ChatMessage(
                    conversation_id=convo.id,
                    role="assistant",
                    message=reply_text,
                    metadata_json=json.dumps({"type": "COMPLAINT_CONFIRMED", "data": res})
                )
                db.session.add(assistant_record)
                db.session.commit()
                return build_structured_response(reply_text, "COMPLAINT_CONFIRMED", res, session_id)
            else:
                reply_text = f"Shikayat darj karne me samasya aayi: {res.get('error', 'Database error')}"
                return build_structured_response(reply_text, "ERROR", {}, session_id)
        
        elif quick_intent == "CANCEL_COMPLAINT" or any(w in message.lower() for w in ["cancel", "nahi", "no", "abort"]):
            state["pending_action"] = None
            state["complaint_draft"] = None
            convo.set_state(state)
            db.session.commit()
            reply_text = "Theek hai, complaint registration cancel kar di gayi hai. Agar aapko kisi anya cheez me madad chahiye to batayein."
            assistant_record = ChatMessage(conversation_id=convo.id, role="assistant", message=reply_text)
            db.session.add(assistant_record)
            db.session.commit()
            return build_structured_response(reply_text, "TEXT", {}, session_id)

    # 2. Check for explicit mission track number in message
    if quick_intent == "TRACK_MISSION":
        extracted_id = extract_mission_id(message)
        if extracted_id:
            m_res = track_mission(mission_id=extracted_id, user_id=user_id, user_role=user_role)
            if m_res.get("success"):
                reply_text = f"Yeh lijiye aapke Mission #{m_res['mission_id']} ka live status:"
                assistant_record = ChatMessage(
                    conversation_id=convo.id,
                    role="assistant",
                    message=reply_text,
                    metadata_json=json.dumps({"type": "MISSION_STATUS", "data": m_res})
                )
                db.session.add(assistant_record)
                db.session.commit()
                return build_structured_response(reply_text, "MISSION_STATUS", m_res, session_id)
            else:
                reply_text = m_res.get("message", "Mission not found or unauthorized.")
                assistant_record = ChatMessage(conversation_id=convo.id, role="assistant", message=reply_text)
                db.session.add(assistant_record)
                db.session.commit()
                return build_structured_response(reply_text, "TEXT", {}, session_id)

    # 3. Direct fast-path for Rewards and Coupons
    if quick_intent == "GET_REWARDS":
        r_data = get_rewards(user_id)
        reply_text = f"Aapke paas kul **{r_data.get('points', 0)} civic points** hain aur aapka current rank **'{r_data.get('badge')}'** hai!"
        assistant_record = ChatMessage(
            conversation_id=convo.id,
            role="assistant",
            message=reply_text,
            metadata_json=json.dumps({"type": "REWARD_STATUS", "data": r_data})
        )
        db.session.add(assistant_record)
        db.session.commit()
        return build_structured_response(reply_text, "REWARD_STATUS", r_data, session_id)

    if quick_intent == "FIND_COUPONS":
        c_data = find_coupons(user_id)
        reply_text = f"Sheher ke partner businesses dwara upalabdh active reward coupons:"
        assistant_record = ChatMessage(
            conversation_id=convo.id,
            role="assistant",
            message=reply_text,
            metadata_json=json.dumps({"type": "COUPON_LIST", "data": c_data})
        )
        db.session.add(assistant_record)
        db.session.commit()
        return build_structured_response(reply_text, "COUPON_LIST", c_data, session_id)

    # 4. Build Conversation History for Gemini
    history_messages = ChatMessage.query.filter_by(conversation_id=convo.id).order_by(ChatMessage.created_at.asc()).limit(8).all()
    gemini_contents = []
    for msg in history_messages:
        role = "user" if msg.role == "user" else "model"
        gemini_contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.message)]
            )
        )

    # 5. Invoke Gemini with Function Calling Tools
    tools = [types.Tool(function_declarations=TOOLS_DECLARATION)]
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=tools,
        temperature=0.3
    )

    card_type = "TEXT"
    card_data = {}
    reply_text = ""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=gemini_contents,
            config=config
        )

        candidate = response.candidates[0] if response.candidates else None
        if not candidate:
            reply_text = "I could not generate a response. Please try again."
            return build_structured_response(reply_text, "TEXT", {}, session_id)

        has_function_call = False
        tool_results_parts = []

        for part in candidate.content.parts:
            if part.function_call:
                has_function_call = True
                fn_name = part.function_call.name
                fn_args = dict(part.function_call.args) if part.function_call.args else {}

                if fn_name == "track_mission":
                    fn_args["user_id"] = user_id
                    fn_args["user_role"] = user_role
                elif fn_name in ["get_rewards", "find_coupons"]:
                    fn_args["user_id"] = user_id

                fn = FUNCTION_MAP.get(fn_name)
                result = {}
                if fn:
                    try:
                        result = fn(**fn_args)
                    except Exception as fn_err:
                        result = {"error": str(fn_err)}
                
                if fn_name == "track_mission" and result.get("success"):
                    card_type = "MISSION_STATUS"
                    card_data = result
                elif fn_name == "get_rewards" and result.get("success"):
                    card_type = "REWARD_STATUS"
                    card_data = result
                elif fn_name == "find_coupons" and result.get("success"):
                    card_type = "COUPON_LIST"
                    card_data = result
                elif fn_name == "check_similar_complaints" and result.get("duplicate_candidate"):
                    card_type = "DUPLICATE_ALERT"
                    card_data = result
                elif fn_name == "prepare_complaint_draft":
                    card_type = "COMPLAINT_DRAFT"
                    card_data = result
                    state["pending_action"] = "CONFIRM_COMPLAINT"
                    state["complaint_draft"] = result
                    convo.set_state(state)
                    db.session.commit()

                tool_results_parts.append(
                    types.Part.from_function_response(
                        name=fn_name,
                        response={"result": result}
                    )
                )

        if has_function_call:
            conversation_with_tool = list(gemini_contents)
            conversation_with_tool.append(candidate.content)
            conversation_with_tool.append(
                types.Content(role="user", parts=tool_results_parts)
            )

            second_response = client.models.generate_content(
                model=MODEL,
                contents=conversation_with_tool,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3
                )
            )
            reply_text = second_response.text or "Here is the information requested:"
        else:
            reply_text = response.text or "Namaste! Main City Guardian AI hoon, main aapki kya madad kar sakta hoon?"

    except Exception as e:
        print(f"Gemini call fallback (Rate limit or network): {e}")
        # High-performance local heuristic fallback
        cat = detect_civic_category(message)
        if any(w in message.lower() for w in ["overflow", "pothole", "gaddha", "leak", "garbage", "kachra", "light", "problem", "samasya", "road"]):
            draft = prepare_complaint_draft(
                category=cat,
                description=message,
                latitude=coordinates.get("latitude") if coordinates else 28.6139,
                longitude=coordinates.get("longitude") if coordinates else 77.2090,
                address="Sector 4, Ward 7"
            )
            card_type = "COMPLAINT_DRAFT"
            card_data = draft
            state["pending_action"] = "CONFIRM_COMPLAINT"
            state["complaint_draft"] = draft
            convo.set_state(state)
            db.session.commit()
            reply_text = f"Maine aapki shikayat ka draft tayar kiya hai ({cat.upper()}). Kripya draft review karke 'Confirm' karein taaki hum ise official register kar sakein."
        else:
            reply_text = "Namaste! Main City Guardian AI hoon. Kripya apni samasya (jaise sadak pe gaddha, naala overflow, ya kachra) batayein taaki main complaint draft kar sakoon."

    # Save assistant message
    metadata = {"type": card_type, "data": card_data} if card_type != "TEXT" else None
    assistant_record = ChatMessage(
        conversation_id=convo.id,
        role="assistant",
        message=reply_text,
        metadata_json=json.dumps(metadata) if metadata else None
    )
    db.session.add(assistant_record)
    db.session.commit()

    return build_structured_response(reply_text, card_type, card_data, session_id)
