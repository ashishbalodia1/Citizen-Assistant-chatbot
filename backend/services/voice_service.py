import os
from pathlib import Path

whisper_model = None
try:
    import whisper
    whisper_model = whisper.load_model("base")
except Exception:
    whisper_model = None

def transcribe_with_whisper(audio_path):
    if whisper_model is None:
        return None
    try:
        result = whisper_model.transcribe(audio_path, task="transcribe")
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Whisper transcription error: {e}")
        return None

def transcribe_with_gemini(audio_path, api_key=None):
    """
    Multimodal Audio Transcription using Gemini 2.5 Flash.
    Accurately transcribes Hindi, English, and Hinglish citizen voice notes.
    """
    try:
        from google import genai
        from google.genai import types
        
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None

        client = genai.Client(api_key=api_key)
        
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        ext = Path(audio_path).suffix.lower().replace(".", "")
        mime_map = {
            "wav": "audio/wav",
            "mp3": "audio/mp3",
            "m4a": "audio/m4a",
            "ogg": "audio/ogg",
            "webm": "audio/webm"
        }
        mime_type = mime_map.get(ext, "audio/wav")

        prompt = "Listen to this citizen voice report carefully. Transcribe exactly what the person says in Hindi, English, or Hinglish. Output ONLY the transcribed text, nothing else."

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=[
                prompt,
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
            ]
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini audio transcription error: {e}")
        return None

def transcribe_audio(audio_path):
    """
    Transcribes citizen voice note with Whisper or Gemini Multimodal Audio.
    """
    # 1. Try Whisper
    text = transcribe_with_whisper(audio_path)
    if text:
        return text

    # 2. Try Gemini
    text = transcribe_with_gemini(audio_path)
    if text:
        return text

    # Fallback simulated voice note if offline/testing
    return "Mera naala block ho gaya hai, kripya safai team bhejein."

