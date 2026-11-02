from datetime import datetime
import json
from extensions import db

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    state_json = db.Column(db.Text, default="{}") # Stores pending_action, complaint_data, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="conversations")
    messages = db.relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan", lazy=True, order_by="ChatMessage.created_at")

    def get_state(self):
        try:
            return json.loads(self.state_json) if self.state_json else {}
        except Exception:
            return {}

    def set_state(self, state_dict):
        self.state_json = json.dumps(state_dict or {})


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False) # user, assistant, system
    message = db.Column(db.Text, nullable=False)
    metadata_json = db.Column(db.Text, nullable=True) # Cards, payload, function calls
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversation = db.relationship("Conversation", back_populates="messages")

    def to_dict(self):
        meta = None
        if self.metadata_json:
            try:
                meta = json.loads(self.metadata_json)
            except Exception:
                meta = None
        return {
            "id": self.id,
            "role": self.role,
            "message": self.message,
            "metadata": meta,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

