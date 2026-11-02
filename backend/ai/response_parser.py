def build_structured_response(text: str, response_type: str = "TEXT", data: dict = None, session_id: str = None):
    return {
        "success": True,
        "response": text,
        "type": response_type,
        "data": data or {},
        "session_id": session_id
    }

