import json
import re

# Load original JS test data
with open('postman_tests_for_training.jsonl', 'r', encoding='utf-8') as f:
    js_examples = [json.loads(line) for line in f if line.strip()]

# Build a set of (endpoint, scenario) for deduplication
js_keys = set()
for ex in js_examples:
    # Try to extract endpoint and scenario from input
    m = re.match(r'([A-Z]+) (\{\{?.*?\}?\}/[\w/\{\}\-]+) - (.*)', ex['input'])
    if m:
        method, endpoint, scenario = m.groups()
        js_keys.add((method.strip(), endpoint.strip(), scenario.strip()))
    else:
        js_keys.add((ex['input'], '', ''))

# Load English test cases
with open('src/data/test_case_training.jsonl', 'r', encoding='utf-8') as f:
    en_examples = [json.loads(line) for line in f if line.strip()]

# Helper to extract endpoint, scenario, and test desc from English input
EN_RE = re.compile(r'API Endpoint: ([A-Z]+) (.*?)\nScenario: (.*?)\n.*?Test Case:', re.DOTALL)

def extract_en_key(en):
    m = EN_RE.search(en['input'])
    if m:
        method, endpoint, scenario = m.groups()
        return (method.strip(), endpoint.strip(), scenario.strip(), en['output'].strip())
    return (None, None, None, en['output'].strip())

# Generate new JS test cases for unique English cases
new_examples = []
for en in en_examples:
    method, endpoint, scenario, test_desc = extract_en_key(en)
    if not method or not endpoint:
        continue
    key = (method, endpoint, scenario)
    if key in js_keys:
        continue
    # Compose input string
    input_str = f"{method} {endpoint} - {scenario}"
    # Compose a basic JS test script based on the test_desc
    js_script = f"pm.test(\"{test_desc}\", function () {{\n    pm.response.to.have.status(200);\n    // TODO: Add more checks based on scenario\n}});"
    new_examples.append({"input": input_str, "output": js_script})

# Write all to new file
with open('augmented_postman_tests_for_training.jsonl', 'w', encoding='utf-8') as f:
    for ex in js_examples:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    for ex in new_examples:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f"Added {len(new_examples)} new examples. Total: {len(js_examples) + len(new_examples)}") 