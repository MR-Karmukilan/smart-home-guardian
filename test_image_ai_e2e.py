import urllib.request
import json
import os

BASE = "http://127.0.0.1:5000"

print("=== 1. TEST EXISTING SENSOR ML & BACKEND ENDPOINTS ===")

# Health
res = json.loads(urllib.request.urlopen(BASE + "/api/health").read().decode())
print("Health:", res)
assert res["status"] == "online"

# Readings
res = json.loads(urllib.request.urlopen(BASE + "/api/readings").read().decode())
print("Readings API working, latest reading:", res.get("latest") is not None)

# Sensor Data POST
payload = json.dumps({"temperature": 28.0, "gas": 200, "pir": 1, "motion": 1, "flame": 0, "person": 1, "door": 0, "sos": 0, "source": "DEMO"}).encode('utf-8')
req = urllib.request.Request(BASE + "/api/sensor-data", data=payload, headers={"Content-Type": "application/json"})
res = json.loads(urllib.request.urlopen(req).read().decode())
print("Sensor Data API response:", res["security_status"], res["ml_prediction"], res["ml_confidence"])
assert "ml_prediction" in res

# Events API
res = json.loads(urllib.request.urlopen(BASE + "/api/events").read().decode())
print("Events API working, total events:", len(res))

print("\n=== 2. TEST NEW IMAGE AI ENDPOINTS ===")

# Image AI Info
res = json.loads(urllib.request.urlopen(BASE + "/api/image-ai/info").read().decode())
print("Image AI Info:", res["status"], "| Normal images:", res["normal_room_count"], "| Person images:", res["person_count"])
assert res["normal_room_count"] == 7
assert res["person_count"] == 0
assert res["status"] == "PERSON training samples are missing."

# Image Detection Sample POST
payload = json.dumps({"sample_filename": "room_normal_01.jpg"}).encode('utf-8')
req = urllib.request.Request(BASE + "/api/image-detection", data=payload, headers={"Content-Type": "application/json"})
res = json.loads(urllib.request.urlopen(req).read().decode())
print("Image Detection Sample 1 Result:", res["status"], "| Detected:", res["person_detected"], "| Confidence:", res["confidence"])
assert res["success"] is True

print("\n=== ALL INTEGRATION & VERIFICATION TESTS PASSED SUCCESSFULLY! ===")
