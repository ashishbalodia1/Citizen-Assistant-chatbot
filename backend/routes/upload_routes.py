import os
import uuid
from flask import Blueprint, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from utils.auth import login_required
from utils.validators import allowed_file, ALLOWED_EXTENSIONS, ALLOWED_AUDIO_EXTENSIONS
from services.vision_service import analyze_image
from services.voice_service import transcribe_audio
from models.conversation import Conversation
from extensions import db

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload/image", methods=["POST"])
@login_required
def upload_complaint_image():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
        return jsonify({"success": False, "error": "Unsupported image format. Allowed: JPG, PNG, WEBP"}), 400

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"img_{uuid.uuid4().hex[:10]}_{secure_filename(file.filename)}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # Perform Image Analysis (YOLO + Gemini Multimodal Vision)
    analysis = analyze_image(filepath)

    session_id = request.form.get("session_id")
    if session_id:
        convo = Conversation.query.filter_by(session_id=session_id).first()
        if convo:
            state = convo.get_state()
            if "complaint_draft" not in state or not state["complaint_draft"]:
                state["complaint_draft"] = {}
            state["complaint_draft"]["image_path"] = f"uploads/{filename}"
            state["complaint_draft"]["category"] = analysis.get("primary_category", "other")
            convo.set_state(state)
            db.session.commit()

    return jsonify({
        "success": True,
        "image_path": f"uploads/{filename}",
        "filename": filename,
        "analysis": analysis
    })

@upload_bp.route("/upload/voice", methods=["POST"])
@login_required
def upload_voice_note():
    if "audio" not in request.files:
        return jsonify({"success": False, "error": "No audio file provided"}), 400

    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"voice_{uuid.uuid4().hex[:10]}_{secure_filename(file.filename or 'audio.wav')}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # Perform Voice-to-Text Transcription
    try:
        transcribed_text = transcribe_audio(filepath)
    except Exception as e:
        transcribed_text = "Audio recorded successfully. Could not transcribe."

    return jsonify({
        "success": True,
        "audio_path": f"uploads/{filename}",
        "transcription": transcribed_text
    })

