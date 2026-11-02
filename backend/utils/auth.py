from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
import os

JWT_SECRET = os.getenv("JWT_SECRET_KEY", "city_guardian_super_secret_jwt_key_2026")
JWT_ALGORITHM = "HS256"

def generate_token(user_id, role="CITIZEN", expires_in_hours=72):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        # For seamless demo testing or frontend usage:
        # If token exists, decode it; if not provided or testing, fallback gracefully to default citizen (user_id=1)
        if token:
            payload = decode_token(token)
            if payload:
                request.user_id = payload.get("user_id", 1)
                request.user_role = payload.get("role", "CITIZEN")
            else:
                return jsonify({"error": "Invalid or expired authorization token"}), 401
        else:
            # Default development / public citizen user
            request.user_id = 1
            request.user_role = "CITIZEN"

        return f(*args, **kwargs)
    return decorated

