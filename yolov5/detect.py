"""
City Guardian YOLOv5 Civic Issue Inference Module
Supports local detection of:
- garbage
- drainage
- pothole
- water_leakage
- broken_streetlight
- illegal_dumping
"""
import os
import sys
from pathlib import Path

CIVIC_CLASSES = [
    "garbage",
    "drainage",
    "pothole",
    "water_leakage",
    "broken_streetlight",
    "illegal_dumping"
]

def run_detection(image_path, weights_path=None):
    if not weights_path:
        weights_path = Path(__file__).parent / "weights" / "best.pt"

    if not os.path.exists(weights_path):
        return {
            "status": "simulated",
            "message": "Custom weights not found at best.pt. Using vision service analysis.",
            "detections": []
        }

    try:
        import torch
        model = torch.hub.load("ultralytics/yolov5", "custom", path=str(weights_path), source="github")
        results = model(image_path)
        df = results.pandas().xyxy[0]
        detections = []
        for _, row in df.iterrows():
            detections.append({
                "category": row["name"],
                "confidence": float(row["confidence"]),
                "box": [float(row["xmin"]), float(row["ymin"]), float(row["xmax"]), float(row["ymax"])]
            })
        return {"status": "success", "detections": detections}
    except Exception as e:
        return {"status": "error", "error": str(e), "detections": []}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = run_detection(sys.argv[1])
        print(res)
    else:
        print("Usage: python detect.py <image_path>")

