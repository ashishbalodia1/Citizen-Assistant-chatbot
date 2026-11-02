import re

INTENTS = {
    "TRACK_MISSION": [
        r"mission", r"track", r"status", r"kahan tak", r"kaha tak", r"progress", r"complaint no", r"shikayat number", r"#\d+"
    ],
    "GET_REWARDS": [
        r"point", r"points", r"badge", r"level", r"mere point", r"kitne point", r"reward", r"rank"
    ],
    "FIND_COUPONS": [
        r"coupon", r"coupons", r"offer", r"discount", r"redeem", r"vouchers", r"inam"
    ],
    "CONFIRM_COMPLAINT": [
        r"confirm", r"yes", r"haan", r"ha", r"kar do", r"file it", r"submit", r"theek hai", r"proceed"
    ],
    "CANCEL_COMPLAINT": [
        r"cancel", r"nahi", r"no", r"mat karo", r"abort", r"stop"
    ]
}

def detect_quick_intent(message: str) -> str:
    msg = message.lower().strip()
    for intent, patterns in INTENTS.items():
        for pat in patterns:
            if re.search(pat, msg):
                return intent
    return "CONVERSATION"

def extract_mission_id(message: str):
    matches = re.findall(r"(?:mission|#|id|number)?\s*(\d{4,6})\b", message.lower())
    if matches:
        return matches[0]
    return None

