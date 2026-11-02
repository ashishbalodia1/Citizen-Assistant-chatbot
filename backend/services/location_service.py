from utils.helpers import haversine_distance

DEFAULT_WARDS = [
    {"id": 1, "ward_name": "Ward 7 - Civil Lines", "lat": 28.6139, "lon": 77.2090},
    {"id": 2, "ward_name": "Ward 12 - Old City", "lat": 28.6500, "lon": 77.2300},
    {"id": 3, "ward_name": "Ward 4 - Metro West", "lat": 28.6300, "lon": 77.1200}
]

def find_nearest_ward(latitude, longitude):
    if latitude is None or longitude is None:
        return DEFAULT_WARDS[0]
    
    nearest = DEFAULT_WARDS[0]
    min_dist = float("inf")
    for ward in DEFAULT_WARDS:
        dist = haversine_distance(latitude, longitude, ward["lat"], ward["lon"])
        if dist < min_dist:
            min_dist = dist
            nearest = ward
            
    return nearest

