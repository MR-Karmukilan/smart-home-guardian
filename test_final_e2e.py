import urllib.request
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

print('=== TEST A: BACKEND HEALTH ===')
req = urllib.request.urlopen(BASE_URL + '/api/health')
health = json.loads(req.read().decode())
print('Health Response:', health)
assert health['status'] == 'online', 'Health status failed'

print('\n=== TEST D: DEMO SCENARIOS (6 SCENARIOS) ===')
scenarios = [
    {'name': 'NORMAL', 'payload': {'temperature': 27.5, 'gas': 120, 'pir': 0, 'motion': 0, 'flame': 0, 'person': 0, 'door': 0, 'sos': 0, 'source': 'DEMO'}},
    {'name': 'PERSON DETECTED', 'payload': {'temperature': 28, 'gas': 180, 'pir': 1, 'motion': 1, 'flame': 0, 'person': 1, 'door': 0, 'sos': 0, 'source': 'DEMO'}},
    {'name': 'DOOR INTRUSION', 'payload': {'temperature': 29, 'gas': 250, 'pir': 1, 'motion': 1, 'flame': 0, 'person': 1, 'door': 1, 'sos': 0, 'source': 'DEMO'}},
    {'name': 'GAS LEAK', 'payload': {'temperature': 31, 'gas': 800, 'pir': 0, 'motion': 0, 'flame': 0, 'person': 0, 'door': 0, 'sos': 0, 'source': 'DEMO'}},
    {'name': 'FIRE EMERGENCY', 'payload': {'temperature': 36, 'gas': 850, 'pir': 1, 'motion': 1, 'flame': 1, 'person': 1, 'door': 1, 'sos': 0, 'source': 'DEMO'}},
    {'name': 'SOS', 'payload': {'temperature': 28, 'gas': 180, 'pir': 1, 'motion': 1, 'flame': 0, 'person': 1, 'door': 0, 'sos': 1, 'source': 'DEMO'}},
]

for sc in scenarios:
    data = json.dumps(sc['payload']).encode('utf-8')
    request = urllib.request.Request(BASE_URL + '/api/sensor-data', data=data, headers={'Content-Type': 'application/json'})
    res = json.loads(urllib.request.urlopen(request).read().decode())
    evt_id = res.get('event', {}).get('id') if res.get('event') else 'None'
    print(f"Scenario: {sc['name']} -> Rule: {res['security_status']} | ML: {res['ml_prediction']} ({res['ml_confidence']}%) | EvtID: {evt_id}")

print('\n=== TEST E: REAL ESP32 API POST (default source) ===')
esp_payload = {'temperature': 28.5, 'gas': 245, 'pir': 1, 'motion': 1, 'flame': 0, 'person': 1, 'door': 0, 'sos': 0}
data = json.dumps(esp_payload).encode('utf-8')
request = urllib.request.Request(BASE_URL + '/api/sensor-data', data=data, headers={'Content-Type': 'application/json'})
res = json.loads(urllib.request.urlopen(request).read().decode())
print('ESP32 POST Response Keys:', list(res.keys()))
print('Security Status:', res['security_status'])
print('ML Prediction:', res['ml_prediction'])
print('ML Confidence:', res['ml_confidence'])
print('Event Source:', res['event']['source'])
assert res['event']['source'] == 'ESP32', 'Source should be ESP32'

print('\n=== TEST F: EVENT HISTORY (GET /api/events) ===')
req = urllib.request.urlopen(BASE_URL + '/api/events')
events = json.loads(req.read().decode())
print(f'Total events in history: {len(events)}')
print('Newest Event:', events[0])

print('\n=== TEST G: ACKNOWLEDGE EVENT ===')
target_id = events[0]['id']
request = urllib.request.Request(f'{BASE_URL}/api/events/{target_id}/acknowledge', data=b'', headers={'Content-Type': 'application/json'})
ack_res = json.loads(urllib.request.urlopen(request).read().decode())
print('Acknowledge Response:', ack_res)
assert ack_res['event']['acknowledged'] is True, 'Acknowledgement failed'

print('\n=== ALL END-TO-END TESTS PASSED SUCCESSFULLY! ===')
