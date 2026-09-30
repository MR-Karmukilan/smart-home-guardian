import json
import urllib.request

scenarios = [
    {
        "name": "1. NORMAL",
        "payload": {"temperature": 27.5, "gas": 120, "pir": 0, "motion": 0, "flame": 0, "person": 0, "door": 0, "sos": 0}
    },
    {
        "name": "2. PERSON DETECTED",
        "payload": {"temperature": 28.0, "gas": 180, "pir": 1, "motion": 1, "flame": 0, "person": 1, "door": 0, "sos": 0}
    },
    {
        "name": "3. DOOR INTRUSION",
        "payload": {"temperature": 29.0, "gas": 250, "pir": 1, "motion": 1, "flame": 0, "person": 1, "door": 1, "sos": 0}
    },
    {
        "name": "4. GAS LEAK",
        "payload": {"temperature": 31.0, "gas": 800, "pir": 0, "motion": 0, "flame": 0, "person": 0, "door": 0, "sos": 0}
    },
    {
        "name": "5. FIRE EMERGENCY",
        "payload": {"temperature": 36.0, "gas": 850, "pir": 1, "motion": 1, "flame": 1, "person": 1, "door": 1, "sos": 0}
    },
    {
        "name": "6. SOS",
        "payload": {"temperature": 28.0, "gas": 180, "pir": 1, "motion": 1, "flame": 0, "person": 1, "door": 0, "sos": 1}
    }
]

url = "http://127.0.0.1:5000/api/sensor-data"

for sc in scenarios:
    req = urllib.request.Request(
        url,
        data=json.dumps(sc["payload"]).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"=== {sc['name']} ===")
        print("Payload         :", sc["payload"])
        print("Rule Status     :", res.get("security_status"))
        print("ML Prediction   :", res.get("ml_prediction"))
        print("ML Confidence   :", res.get("ml_confidence"), "%")
        print("ML Probabilities:", res.get("ml_probabilities"))
        print()
