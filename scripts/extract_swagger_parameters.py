import json

SWAGGER_FILE = 'data/raw/swagger.json'
OUTPUT_FILE = 'swagger_parameters_human_readable.json'

def main():
    with open(SWAGGER_FILE, 'r', encoding='utf-8') as f:
        swagger = json.load(f)

    endpoint_params = {}
    for path, methods in swagger.get('paths', {}).items():
        for method, details in methods.items():
            key = f"{method.upper()} {path}"
            params = details.get('parameters', [])
            if not params:
                continue
            param_lines = ["Parameters:"]
            for p in params:
                name = p.get('name')
                location = p.get('in')
                typ = p.get('type', p.get('schema', {}).get('type', 'object'))
                required = 'required' if p.get('required', False) else 'optional'
                desc = p.get('description', '')
                param_lines.append(f"- {name} ({location}, {typ}, {required}): {desc}")
            endpoint_params[key] = '\n'.join(param_lines)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        json.dump(endpoint_params, out, indent=2)
    print(f"Extracted parameters for {len(endpoint_params)} endpoints. Output written to {OUTPUT_FILE}")

if __name__ == '__main__':
    main() 