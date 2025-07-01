# src/create_test_files.py
import json
import os
from pathlib import Path
import logging
import re
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_VALUES = {
    'gatewayId': 'freedompay',
    'industryType': 'foodAndBeverage',
    'amount': 100.00,
    'currencyCultureName': 'en-US',
    'currencyCode': 'USD',
    'invoiceId': '123456789',
    'invoiceDate': '2024-06-01T12:00:00Z',
    'registerId': '1',
    'clerkId': '2',
    'checkNumber': 'CHK-1001',
    'checkOpenDate': '2024-06-01T12:00:00Z',
    'referenceCode': '123ABC',
    'roomNumber': '101',
    'deviceGuid': 'f7da845e-b9cf-4e24-b3f9-d93e00000000',
    'transactionId': '01Z6N0610T97U6HUCBQTI31QNTVDDJEN',
    'checkId': '20170802123700154',
    'token': '4761730A0012UZDZEKC5IR000011',
    'laneState': 'open',
}

BASE_URL = "http://localhost:8502"
SWAGGER_PATH = 'swagger.json'

def load_generated_tests(file_path: str):
    """Load the generated test cases."""
    with open(file_path, 'r') as f:
        return json.load(f)

def load_swagger(swagger_path: str):
    with open(swagger_path, 'r') as f:
        return json.load(f)

def get_schema_for_endpoint(swagger, path, method):
    method = method.lower()
    path_item = swagger['paths'].get(path)
    if not path_item:
        return None, None
    op = path_item.get(method)
    if not op:
        return None, None
    # Request body (OpenAPI 2.0/3.0)
    parameters = op.get('parameters', [])
    body_schema = None
    for param in parameters:
        if param.get('in') == 'body' and 'schema' in param:
            body_schema = param['schema']
            break
    # OpenAPI 3.0 style
    if not body_schema and 'requestBody' in op:
        content = op['requestBody'].get('content', {})
        if 'application/json' in content:
            body_schema = content['application/json'].get('schema')
    return body_schema, parameters

def fill_schema(schema, definitions=None):
    """Recursively fill a schema with user values or dummy data."""
    if not schema:
        return None
    if definitions is None:
        definitions = {}
    if '$ref' in schema:
        ref = schema['$ref']
        ref_name = ref.split('/')[-1]
        schema = definitions.get(ref_name, {})
    t = schema.get('type')
    if t == 'object' or ('properties' in schema):
        result = {}
        for prop, prop_schema in schema.get('properties', {}).items():
            # Use user value if available
            if prop in USER_VALUES:
                result[prop] = USER_VALUES[prop]
            else:
                result[prop] = fill_schema(prop_schema, definitions)
        # Fill required fields if missing
        for req in schema.get('required', []):
            if req not in result:
                if req in USER_VALUES:
                    result[req] = USER_VALUES[req]
                else:
                    result[req] = fill_schema(schema['properties'][req], definitions)
        return result
    elif t == 'array':
        item_schema = schema.get('items', {})
        return [fill_schema(item_schema, definitions)]
    elif t == 'string':
        # Use user value if available
        if 'enum' in schema:
            return schema['enum'][0]
        return "string"
    elif t == 'number' or t == 'integer':
        return 1
    elif t == 'boolean':
        return True
    else:
        return None

def format_test_case(test_case: dict, swagger: dict) -> str:
    input_lines = test_case['input'].split('\n')
    first_line = input_lines[0].strip()
    for prefix in ['Generate test case for', 'test case for']:
        if first_line.lower().startswith(prefix.lower()):
            first_line = first_line[len(prefix):].strip()
    if ' ' in first_line:
        method, endpoint_path = first_line.split(' ', 1)
        method = method.lower()
    else:
        method = 'get'
        endpoint_path = '/'
    # Replace path parameters with user values
    endpoint_path = re.sub(r'\{deviceGuid\}', USER_VALUES['deviceGuid'], endpoint_path)
    endpoint_path = re.sub(r'\{transactionId\}', USER_VALUES['transactionId'], endpoint_path)
    endpoint_path = re.sub(r'\{checkId\}', USER_VALUES['checkId'], endpoint_path)
    endpoint_path = re.sub(r'\{token\}', USER_VALUES['token'], endpoint_path)
    endpoint_path = re.sub(r'\{laneState\}', USER_VALUES['laneState'], endpoint_path)
    # Query params
    body_schema, parameters = get_schema_for_endpoint(swagger, endpoint_path, method)
    query_params = []
    if parameters:
        for param in parameters:
            if param.get('in') == 'query':
                pname = param['name']
                pval = USER_VALUES.get(pname, 'string')
                query_params.append(f"{pname}={pval}")
    query_str = ''
    if query_params:
        query_str = '?' + '&'.join(query_params)
    url = f"{BASE_URL.rstrip('/')}/{endpoint_path.lstrip('/')}" + query_str
    # Fill request body
    definitions = swagger.get('definitions', {})
    body = fill_schema(body_schema, definitions) if body_schema else None
    # Use Python's None, not JSON null
    body_str = ''
    if method in {'post', 'put', 'patch'} and body:
        body_str = f", json={repr(body)}"
    # Generate test code
    code = f"""
def test_endpoint(base_url, headers):
    url = '{url}'
    response = requests.{method}(url, headers=headers{body_str})
    assert response.status_code == 200
"""
    return code

def main():
    generated_tests_path = "src/data/generated_test_cases.json"
    output_dir = Path("src/tests/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    test_cases = load_generated_tests(generated_tests_path)
    swagger = load_swagger(SWAGGER_PATH)
    for i, test_case in enumerate(test_cases):
        code = format_test_case(test_case, swagger)
        test_file = output_dir / f"test_endpoint_{i}.py"
        with open(test_file, 'w') as f:
            f.write("import requests\n")
            f.write("import pytest\n")
            f.write("\n")
            f.write("@pytest.fixture\ndef base_url():\n    return 'http://localhost:8502'\n\n")
            f.write("@pytest.fixture\ndef headers():\n    return {\n        'Authorization': 'PMAK-6852cde6134d13000180adc0-0a0c477664d3aa340e51077f563a400e82e',\n        'Content-Type': 'application/json'\n    }\n\n")
            f.write(code)
        logger.info(f"Wrote {test_file}")

if __name__ == "__main__":
    main()