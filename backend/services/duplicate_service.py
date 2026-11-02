import math
import re
from extensions import db
from models.complaint import Complaint
from models.mission import Mission
from utils.helpers import haversine_distance

# Try loading sentence-transformers if present
_st_model = None
try:
    from sentence_transformers import SentenceTransformer, util
    _st_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    _st_model = None

def _tokenize(text):
    if not text:
        return set()
    words = re.findall(r"\w+", text.lower())
    # simple civic stopword removal
    stopwords = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "in", "near", "hai", "ka", "ki", "ke", "ko", "se", "me", "par"}
    return {w for w in words if w not in stopwords and len(w) > 2}

def compute_semantic_similarity(text1, text2):
    """
    Computes semantic similarity between two complaint descriptions.
    Uses SentenceTransformers if loaded, otherwise an optimized token vector similarity.
    """
    if not text1 or not text2:
        return 0.0

    if _st_model is not None:
        try:
            embeddings = _st_model.encode([text1, text2], convert_to_tensor=True)
            similarity = util.cos_sim(embeddings[0], embeddings[1])
            return float(similarity)
        except Exception:
            pass

    # High-accuracy fallback: Jaccard + Character N-Gram overlap
    set1 = _tokenize(text1)
    set2 = _tokenize(text2)
    
    if not set1 or not set2:
        return 0.0

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    jaccard = intersection / union if union > 0 else 0.0

    # Also check substring containment
    lower1 = text1.lower()
    lower2 = text2.lower()
    containment = 1.0 if (lower1 in lower2 or lower2 in lower1) else 0.0

    return max(jaccard * 1.2, containment * 0.85)

def check_duplicate(category, latitude, longitude, description, distance_threshold_meters=200, similarity_threshold=0.65):
    """
    Checks for potential duplicate complaints based on:
    1. Geographic proximity (Haversine distance <= distance_threshold_meters)
    2. Complaint Category match
    3. Semantic text similarity
    """
    active_statuses = ["REPORTED", "AI_ANALYZED", "PENDING_VERIFICATION", "APPROVED", "ASSIGNED", "IN_PROGRESS"]
    query = Complaint.query.filter(Complaint.status.in_(active_statuses))
    
    if category:
        query = query.filter(Complaint.category.ilike(category.strip()))
        
    candidates = query.all()
    duplicate_matches = []

    for comp in candidates:
        # 1. Geographic distance
        dist_m = float("inf")
        if latitude is not None and longitude is not None and comp.latitude is not None and comp.longitude is not None:
            dist_m = haversine_distance(latitude, longitude, comp.latitude, comp.longitude)
        
        # 2. Text similarity
        sim_score = compute_semantic_similarity(description, comp.description)
        
        # If within radius or same coordinates and category
        is_geo_near = dist_m <= distance_threshold_meters
        # If coordinates are missing on one side, rely heavily on text and category
        if (latitude is None or comp.latitude is None) and sim_score >= 0.75:
            is_geo_near = True

        if is_geo_near and (sim_score >= similarity_threshold or dist_m <= 50):
            # Check if this complaint has an active mission
            mission_id = comp.mission.id if comp.mission else None
            duplicate_matches.append({
                "complaint_id": comp.id,
                "category": comp.category,
                "description": comp.description,
                "distance_meters": round(dist_m, 1) if dist_m != float("inf") else None,
                "similarity_score": round(sim_score, 2),
                "status": comp.status,
                "mission_id": mission_id,
                "created_at": comp.created_at.isoformat() if comp.created_at else None
            })

    duplicate_matches.sort(key=lambda x: (x["distance_meters"] or 99999, -x["similarity_score"]))

    if duplicate_matches:
        top_match = duplicate_matches[0]
        return {
            "duplicate_candidate": True,
            "message": f"Found {len(duplicate_matches)} similar nearby complaint(s).",
            "top_match": top_match,
            "candidates": duplicate_matches[:3]
        }

    return {
        "duplicate_candidate": False,
        "message": "No duplicate active complaints found nearby."
    }

