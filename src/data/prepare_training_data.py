# src/data/prepare_training_data.py
import json
import os

LOG_PATH = "test_case_generator/data/test_execution_log.json"
OUTPUT_PATH = "src/data/training_dataset.json"

def main():
    if not os.path.exists(LOG_PATH):
        print(f"Log file not found: {LOG_PATH}")
        return

    with open(LOG_PATH) as f:
        logs = json.load(f)

    training_data = []
    for entry in logs:
        # Use 'url' instead of 'endpoint', and handle missing 'test_code'
        input_text = f"{entry.get('method', '')} {entry.get('url', '')}"
        output_text = entry.get('test_code', f"# No test code available for {input_text}")
        training_data.append({"input": input_text, "output": output_text})

    with open(OUTPUT_PATH, "w") as f:
        json.dump(training_data, f, indent=2)
    print(f"Saved {len(training_data)} training pairs to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()