# run_tests.py
import json
import time
import requests
import os
import pandas as pd
import sys

# Add config path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import BASE_URL, GATEWAY_ID, INDUSTRY_TYPE, CHECK_ID

# File paths
INPUT_FILE = "test_case_generator/data/generated_tests.json"
OUTPUT_FILE = "test_case_generator/data/test_execution_log.json"

def load_tests(input_file):
    if input_file.endswith(".json"):
        with open(input_file, "r") as f:
            return json.load(f)
    elif input_file.endswith(".csv"):
        return pd.read_csv(input_file).to_dict(orient="records")
    elif input_file.endswith(".xlsx"):
        return pd.read_excel(input_file).to_dict(orient="records")
    else:
        raise ValueError("Unsupported file format.")

def run_tests(test_cases):
    results = []

    for test in test_cases:
        method = test.get("method", "GET").upper()
        endpoint = test.get("url") or test.get("endpoint")
        payload = test.get("payload", {})

        if not endpoint:
            print("Skipping test with no endpoint.")
            continue

        # Replace placeholders in path
        if isinstance(payload, dict):
            for key, val in payload.items():
                placeholder = f"{{{key}}}"
                endpoint = endpoint.replace(placeholder, str(val))

        url = endpoint if endpoint.startswith("http") else BASE_URL + endpoint

        # Enrich payload with shared defaults
        if isinstance(payload, dict):
            payload.setdefault("gatewayId", GATEWAY_ID)
            payload.setdefault("industryType", INDUSTRY_TYPE)
            payload.setdefault("checkId", CHECK_ID)

            if "request" not in payload:
                payload["request"] = {}
            payload["request"].setdefault("gatewayId", GATEWAY_ID)
            payload["request"].setdefault("industryType", INDUSTRY_TYPE)
            payload["request"].setdefault("checkId", CHECK_ID)

        # Send request and log results
        try:
            start = time.time()
            response = requests.request(method, url, json=payload)
            latency = (time.time() - start) * 1000
            status = response.status_code
            error = response.text if status >= 400 else ""
        except Exception as e:
            latency = None
            status = None
            error = str(e)

        results.append({
            "method": method,
            "url": url,
            "payload": payload,
            "status_code": status,
            "latency_ms": round(latency, 2) if latency else None,
            "error": error
        })

    return results

def save_results(results, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Saved test results to {output_file}")

if __name__ == "__main__":
    test_cases = load_tests(INPUT_FILE)
    results = run_tests(test_cases)
    save_results(results, OUTPUT_FILE)