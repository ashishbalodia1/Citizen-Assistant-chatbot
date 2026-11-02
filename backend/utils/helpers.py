import math
from datetime import datetime

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate geographic distance in meters between two points using Haversine formula.
    """
    if None in (lat1, lon1, lat2, lon2):
        return float("inf")
    
    R = 6371000  # Earth's radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_time_remaining(deadline):
    if not deadline:
        return "No Deadline", 0
    now = datetime.utcnow()
    diff = (deadline - now).total_seconds()
    if diff <= 0:
        return "Expired", 0
    
    days = int(diff // 86400)
    hours = int((diff % 86400) // 3600)
    mins = int((diff % 3600) // 60)
    
    if days > 0:
        return f"{days} Days, {hours} Hours", int(diff)
    return f"{hours} Hours, {mins} Mins", int(diff)

