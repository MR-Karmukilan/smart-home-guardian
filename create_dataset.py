import os
import pandas as pd
import numpy as np

os.makedirs("backend/data", exist_ok=True)
os.makedirs("backend/data/uploads", exist_ok=True)

np.random.seed(42)

# Generate 1000 rows with exact required class distribution:
# SAFE = 400, WARNING = 250, ALERT = 200, EMERGENCY = 150
rows = []

# 400 SAFE samples
for _ in range(400):
    rows.append({
        "temperature": round(np.random.uniform(20.0, 29.5), 1),
        "gas": int(np.random.randint(100, 249)),
        "pir": 0,
        "motion": 0,
        "flame": 0,
        "person": 0,
        "door": 0,
        "sos": 0,
        "security_status": "SAFE"
    })

# 250 WARNING samples
for _ in range(250):
    has_pir = np.random.choice([0, 1], p=[0.4, 0.6])
    has_person = has_pir
    has_motion = has_pir
    gas_val = int(np.random.randint(250, 499)) if not has_pir else int(np.random.randint(100, 400))
    rows.append({
        "temperature": round(np.random.uniform(22.0, 34.0), 1),
        "gas": gas_val,
        "pir": has_pir,
        "motion": has_motion,
        "flame": 0,
        "person": has_person,
        "door": 0,
        "sos": 0,
        "security_status": "WARNING"
    })

# 200 ALERT samples
for _ in range(200):
    high_temp = np.random.choice([True, False])
    temp_val = round(np.random.uniform(35.0, 39.5), 1) if high_temp else round(np.random.uniform(22.0, 34.0), 1)
    gas_val = int(np.random.randint(500, 699)) if not high_temp else int(np.random.randint(100, 499))
    pir_val = np.random.choice([0, 1])
    rows.append({
        "temperature": temp_val,
        "gas": gas_val,
        "pir": pir_val,
        "motion": pir_val,
        "flame": 0,
        "person": pir_val,
        "door": 0,
        "sos": 0,
        "security_status": "ALERT"
    })

# 150 EMERGENCY samples
for _ in range(150):
    flame_val = np.random.choice([0, 1], p=[0.5, 0.5])
    temp_val = round(np.random.uniform(40.5, 48.0), 1) if flame_val == 0 else round(np.random.uniform(25.0, 45.0), 1)
    gas_val = int(np.random.randint(701, 3500)) if flame_val == 0 else int(np.random.randint(200, 2500))
    pir_val = np.random.choice([0, 1])
    sos_val = np.random.choice([0, 1], p=[0.7, 0.3])
    rows.append({
        "temperature": temp_val,
        "gas": gas_val,
        "pir": pir_val,
        "motion": pir_val,
        "flame": flame_val,
        "person": pir_val,
        "door": 0,
        "sos": sos_val,
        "security_status": "EMERGENCY"
    })

df = pd.DataFrame(rows)
# Shuffle rows reproducibly
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

csv_path = "backend/data/smart_home_training.csv"
df.to_csv(csv_path, index=False)
print(f"Created {csv_path} with {len(df)} rows.")
print("Class counts:")
print(df["security_status"].value_counts())
