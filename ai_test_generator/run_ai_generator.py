import os
import sys
from .ai_test_generator import AITestGenerator
import json
import pandas as pd

def main():
    # Paths
    swagger_path = "test_case_generator/data/swagger.json"
    postman_path = "test_case_generator/data/rGuest Pay Agent.postman_test_run.json"
    historical_data_path = "ai_model/data/history_logs.csv"
    output_path = "test_case_generator/data/generated_tests.json"
    prioritized_path = "ai_model/data/prioritized_tests.json"

    # Check for prioritized mode (via env or arg)
    prioritized = None
    if os.environ.get("PRIORITIZED") == "1" or (len(sys.argv) > 1 and sys.argv[1] == "--prioritized"):
        if os.path.exists(prioritized_path):
            with open(prioritized_path, "r") as f:
                prioritized = json.load(f)
            print(f"Using prioritized endpoints: {len(prioritized)}")
        else:
            print("Prioritized tests file not found, running full generation.")

    # Generate from Swagger if available
    if os.path.exists(swagger_path):
        generator = AITestGenerator(
            swagger_path=swagger_path,
            historical_data_path=historical_data_path
        )
        generator.save_test_cases(output_path, prioritized=prioritized)
        print("✅ Test cases generated from Swagger.")

    # Generate from Postman if available
    if os.path.exists(postman_path):
        with open(postman_path, "r") as f:
            postman_data = json.load(f)
        # Convert Postman test run to test cases format
        results = postman_data.get("results", [])
        collection_methods = {req["id"]: req["method"] for req in postman_data.get("collection", {}).get("requests", [])}
        postman_tests = []
        for result in results:
            url = result.get("url")
            method = collection_methods.get(result["id"], "GET")
            status_code = result.get("responseCode", {}).get("code", 0)
            time = result.get("time", 0)
            postman_tests.append({
                "method": method,
                "url": url,
                "status_code": status_code,
                "latency_ms": time
            })
        # Save/append to the same output file
        if os.path.exists(output_path):
            with open(output_path, "r") as f:
                existing = json.load(f)
        else:
            existing = []
        all_tests = existing + postman_tests
        with open(output_path, "w") as f:
            json.dump(all_tests, f, indent=2)
        print("✅ Test cases generated from Postman test run.")

if __name__ == "__main__":
    main() 