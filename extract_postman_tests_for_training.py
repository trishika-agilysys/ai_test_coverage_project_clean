import json

POSTMAN_FILE = "data/raw/AgilysysPayAgent_Integration_TestCases_DisneyMPS.postman_collection.json"
OUTPUT_FILE = "postman_tests_for_training.jsonl"

def extract_tests(item, tests):
    if "item" in item:  # Folder
        for subitem in item["item"]:
            extract_tests(subitem, tests)
    else:  # Request
        request = item.get("request", {})
        method = request.get("method", "")
        url = request.get("url", {}).get("raw", "")
        name = item.get("name", "")
        description = item.get("description", "")
        # Extract test scripts
        events = item.get("event", [])
        for event in events:
            if event.get("listen") == "test":
                script_lines = event.get("script", {}).get("exec", [])
                script = "\n".join(script_lines)
                if script.strip():
                    tests.append({
                        "input": f"{method} {url} - {name}",
                        "description": description,
                        "test_script": script
                    })

def main():
    with open(POSTMAN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    tests = []
    for item in data.get("item", []):
        extract_tests(item, tests)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for test in tests:
            f.write(json.dumps(test, ensure_ascii=False) + "\n")
    print(f"Extracted {len(tests)} test scripts to {OUTPUT_FILE}")

    # --- Overwrite with input/output format ---
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fin:
        lines = fin.readlines()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
        for line in lines:
            obj = json.loads(line)
            prompt = obj["input"]
            if obj.get("description"):
                prompt += "\n" + obj["description"]
            output = obj["test_script"]
            fout.write(json.dumps({"input": prompt, "output": output}, ensure_ascii=False) + "\n")
    print(f"Overwrote {OUTPUT_FILE} with input/output format.")

if __name__ == "__main__":
    main()