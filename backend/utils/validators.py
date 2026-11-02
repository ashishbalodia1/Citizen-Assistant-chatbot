CIVIC_CATEGORIES = [
    "drainage",
    "garbage",
    "pothole",
    "water_leakage",
    "broken_streetlight",
    "illegal_dumping",
    "road_damage",
    "other"
]

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "m4a", "webm", "ogg"}

def is_valid_category(cat: str) -> bool:
    if not cat:
        return False
    return cat.lower().strip() in CIVIC_CATEGORIES

def is_valid_coordinates(lat, lon) -> bool:
    if lat is None or lon is None:
        return True # Optional in some quick reports
    try:
        lat = float(lat)
        lon = float(lon)
        return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0
    except (ValueError, TypeError):
        return False

def allowed_file(filename: str, allowed_set=ALLOWED_EXTENSIONS) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set

