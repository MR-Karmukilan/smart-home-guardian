import json
import urllib.request
import urllib.error

url = "http://127.0.0.1:5000/api/sensor-data"
payload = {"temperature": 27.5, "gas": 120, "pir": 0, "motion": 0, "flame": 0, "person": 0, "door": 0, "sos": 0}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Error Body:", e.read().decode("utf-8"))
