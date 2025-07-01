import json
import pandas as pd
import os
from datetime import datetime

# Load test execution log
with open("test_case_generator/data/test_execution_log.json", "r") as f:
    logs = json.load(f)

data = []
timestamp = datetime.now().isoformat()

for entry in logs:
    method = entry.get("method", "")
    url = entry.get("url", "")
    status_code = entry.get("status_code")
    latency = entry.get("latency_ms")
    error = entry.get("error", "")
    
    is_error = 1 if status_code is not None and status_code >= 400 else 0

    def bucket_latency(ms):
        if ms is None:
            return "unknown"
        if ms < 500:
            return "fast"
        elif ms < 2000:
            return "medium"
        return "slow"

    latency_bucket = bucket_latency(latency)

    data.append({
        "method": method,
        "url": url,
        "status_code": status_code,
        "latency_ms": latency,
        "is_error": is_error,
        "latency_bucket": latency_bucket,
        "timestamp": timestamp
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save current run to processed_logs.csv
df.to_csv("ai_model/data/processed_logs.csv", index=False)

# Append to historical file 
history_path = "ai_model/data/history_logs.csv"
try:
    df.to_csv(history_path, mode="a", index=False, header=not os.path.exists(history_path))
except Exception as e:
    print(f"Failed to append to history: {e}")

print("Features saved to processed_logs.csv and history_logs.csv")
