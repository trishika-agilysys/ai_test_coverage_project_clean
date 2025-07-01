import json
import re
from collections import defaultdict

INPUT_FILE = '../augmented_postman_tests_for_training.split_cleaned.jsonl'
OUTPUT_FILE = '../augmented_postman_tests_for_training.merged_cleaned.jsonl'
PARAMS_FILE = 'swagger_parameters_human_readable.json'
SCHEMA_FILE = 'data/raw/swagger_fixed.json'
MAX_PROMPT_LEN = 1024

# Regex to match and remove chunk info from input
CHUNK_RE = re.compile(r" ?\[chunk \d+/\d+\]$", re.IGNORECASE)

# Regex to match hardcoded base URLs (localhost or any http(s)://...)
BASE_URL_RE = re.compile(r"https?://localhost:\d+|https?://[^/]+", re.IGNORECASE)

# Helper to check if output is likely complete
def is_complete_script(script):
    stack = []
    pairs = {'{': '}', '(': ')', '[': ']'}
    openers = pairs.keys()
    closers = pairs.values()
    for c in script:
        if c in openers:
            stack.append(pairs[c])
        elif c in closers:
            if not stack or c != stack.pop():
                return False
    if stack:
        return False
    if script.strip().endswith(('}', ");", ")")):
        return True
    return False

def standardize_base_url(s):
    # Replace any hardcoded base URL with {{payagent-url}}
    return BASE_URL_RE.sub("{{payagent-url}}", s)

def extract_method_and_path(scenario):
    # Standardize base URL for parameter lookup
    scenario = standardize_base_url(scenario)
    match = re.match(r"(GET|POST|PUT|DELETE|PATCH|VIEW) +([^ ]+)", scenario, re.IGNORECASE)
    if match:
        method = match.group(1).upper()
        path = match.group(2)
        # Remove base URL variable or http(s)://... from the path
        path = re.sub(r"^(\{\{[^}]+\}\}|https?://[^/]+)", '', path)
        # Replace all {{var}} with {var}
        path = re.sub(r"\{\{([^}]+)\}\}", r"{\1}", path)
        return f"{method} {path}", method, path
    return None, None, None

def abbreviate_param_line(line):
    # Keep only the part before the first colon (name/type/required)
    if ':' in line:
        before, after = line.split(':', 1)
        return before.strip() + ':'
    return line.strip()

def get_short_schema(swagger, method, path, which):
    # which: 'request' or 'response'
    # Find the path in swagger
    path_obj = None
    for k in swagger.get('paths', {}):
        # Normalize path for matching
        norm_k = re.sub(r"\{([^}]+)\}", r"{\1}", k)
        if norm_k == path:
            path_obj = swagger['paths'][k]
            break
    if not path_obj:
        return None
    op = path_obj.get(method.lower())
    if not op:
        return None
    if which == 'request':
        req_body = op.get('requestBody')
        if req_body:
            content = req_body.get('content', {})
            for ct in ['application/json', 'application/x-www-form-urlencoded']:
                if ct in content:
                    schema = content[ct].get('schema')
                    if schema:
                        return json.dumps(schema.get('properties', {}), indent=2) if 'properties' in schema else json.dumps(schema, indent=2)
    elif which == 'response':
        responses = op.get('responses', {})
        for code in ['200', '201', 'default']:
            if code in responses:
                content = responses[code].get('content', {})
                for ct in ['application/json', 'application/x-www-form-urlencoded']:
                    if ct in content:
                        schema = content[ct].get('schema')
                        if schema:
                            return json.dumps(schema.get('properties', {}), indent=2) if 'properties' in schema else json.dumps(schema, indent=2)
    return None

def main():
    # Load parameter descriptions
    with open(PARAMS_FILE, 'r', encoding='utf-8') as pf:
        param_map = json.load(pf)
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as sf:
        swagger = json.load(sf)

    # Read all lines
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = [json.loads(line) for line in f if line.strip()]

    # Group by scenario (input without chunk info)
    scenario_dict = defaultdict(list)
    for entry in lines:
        input_base = CHUNK_RE.sub('', entry['input']).strip()
        chunk_match = re.search(r"\[chunk (\d+)/(\d+)\]$", entry['input'])
        chunk_num = int(chunk_match.group(1)) if chunk_match else 1
        scenario_dict[input_base].append((chunk_num, entry['output']))

    merged, removed, written, truncated = 0, 0, 0, 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for scenario, outputs in scenario_dict.items():
            outputs_sorted = [o for _, o in sorted(outputs)]
            merged_output = ''.join(outputs_sorted)
            # Standardize base URL in scenario for prompt
            scenario_std = standardize_base_url(scenario)
            method_path, method, path = extract_method_and_path(scenario_std)
            param_text = param_map.get(method_path)
            prompt_input = f"Generate all Postman JavaScript tests for: {scenario_std}\n"
            # Add request/response schema if available
            req_schema = get_short_schema(swagger, method, path, 'request')
            if req_schema:
                prompt_input += f"\nRequest body schema:\n{req_schema}\n"
            resp_schema = get_short_schema(swagger, method, path, 'response')
            if resp_schema:
                prompt_input += f"\nResponse body schema:\n{resp_schema}\n"
            # Truncation logic
            truncated_flag = False
            if len(prompt_input) > MAX_PROMPT_LEN:
                prompt_input = prompt_input[:MAX_PROMPT_LEN] + '\n[truncated]'
                truncated_flag = True
            if is_complete_script(merged_output):
                json.dump({'input': prompt_input, 'output': merged_output}, out)
                out.write('\n')
                written += 1
                if len(outputs) > 1:
                    merged += 1
                if truncated_flag:
                    truncated += 1
            else:
                removed += 1
    print(f"Merged: {merged}, Removed: {removed}, Written: {written}, Truncated: {truncated}")

if __name__ == '__main__':
    main() 