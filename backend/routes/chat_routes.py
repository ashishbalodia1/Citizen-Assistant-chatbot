from flask import Blueprint, request, jsonify
from ai.agent import run_agent
from models.conversation import Conversation, ChatMessage
from utils.auth import login_required
from schemas.chat_schema import ChatRequest

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id")
    coordinates = data.get("coordinates")

    if not message:
        return jsonify({"success": False, "error": "Message cannot be empty"}), 400

    user_id = getattr(request, "user_id", 1)
    user_role = getattr(request, "user_role", "CITIZEN")

    try:
        response_data = run_agent(
            message=message,
            user_id=user_id,
            user_role=user_role,
            session_id=session_id,
            coordinates=coordinates
        )
        return jsonify(response_data)
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        return jsonify({
            "success": False,
            "error": "Unable to process your request. Please try again.",
            "details": str(e)
        }), 500

@chat_bp.route("/conversations/<session_id>", methods=["GET"])
@login_required
def get_conversation_history(session_id):
    user_id = getattr(request, "user_id", 1)
    convo = Conversation.query.filter_by(session_id=session_id).first()
    if not convo:
        return jsonify({"success": True, "messages": []})
        
    messages = [m.to_dict() for m in convo.messages]
    return jsonify({
        "success": True,
        "session_id": session_id,
        "messages": messages,
        "state": convo.get_state()
    })

