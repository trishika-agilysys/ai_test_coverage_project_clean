import csv
import json
import re
import pandas as pd
import os
import glob
from collections import defaultdict

# Process all CSV files in the raw directory
RAW_DATA_DIR = 'data/raw'
POSTMAN_PATH = 'data/raw/rGuest Pay Agent.postman_collection 1.json'
OUTPUT_PATH = 'src/data/test_case_training.jsonl'

# Extract endpoints from Postman
def extract_postman_endpoints(postman_json):
    endpoints = []
    def walk_items(items, parent_url=""):
        for item in items:
            if 'request' in item:
                method = item['request']['method']
                url = item['request']['url']
                if isinstance(url, dict):
                    raw_url = url.get('raw', '')
                    path = '/' + '/'.join(url.get('path', []))
                else:
                    raw_url = url
                    path = url
                params = []
                if 'query' in url and isinstance(url['query'], list):
                    params = [q['key'] for q in url['query']]
                if 'body' in item['request'] and 'formdata' in item['request']['body']:
                    params += [f["key"] for f in item['request']['body']['formdata']]
                
                # Extract path variables from raw_url
                if raw_url:
                    path_params = re.findall(r'\{\{(.*?)\}\}', raw_url)
                    params.extend(path_params)

                endpoints.append({
                    'method': method,
                    'raw_url': raw_url,
                    'path': path,
                    'params': params,
                    'name': item.get('name', ''),
                    'description': item.get('request', {}).get('description', '')
                })
            if 'item' in item:
                walk_items(item['item'], parent_url)
    walk_items(postman_json['item'])
    return endpoints

# Helper: match test case to endpoint by keyword
def match_endpoint(text_to_match, endpoints):
    text_to_match_lower = text_to_match.lower()
    best_match = None
    max_score = 0

    # Create a set of words from the text to match
    text_words = set(re.findall(r'\w+', text_to_match_lower))
    if not text_words:
        return None

    for ep in endpoints:
        score = 0
        
        # 1. Match against endpoint name (high weight)
        ep_name_words = set(re.findall(r'\w+', ep.get('name', '').lower()))
        common_name_words = text_words.intersection(ep_name_words)
        score += len(common_name_words) * 3

        # 2. Match against endpoint path (medium weight)
        ep_path_words = set(re.findall(r'\w+', ep.get('path', '').lower()))
        common_path_words = text_words.intersection(ep_path_words)
        score += len(common_path_words) * 2
        
        # 3. Match against description (low weight)
        ep_desc_words = set(re.findall(r'\w+', ep.get('description', '').lower()))
        common_desc_words = text_words.intersection(ep_desc_words)
        score += len(common_desc_words) * 1

        if score > max_score:
            max_score = score
            best_match = ep

    # Only return a match if there's a reasonable score
    if max_score > 1:
        return best_match
    return None

def load_csv_file(file_path):
    """Load CSV or Excel file and return DataFrame"""
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            return None
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def main():
    # Test cases to exclude
    exclude_test_cases = [
        "Verify the dual MID feature is working fine",
        "Verify the quickchip feature is working fine",
        "Verify the correlation ID returned in the response",
        "Verify the round off by providing three decimal values",
        "Verify the invoice date in all applicable APIs"
    ]

    # Find all CSV and Excel files in the raw data directory
    csv_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
    excel_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.xlsx"))
    all_files = csv_files + excel_files
    
    print(f"Found {len(all_files)} files to process:")
    for file in all_files:
        print(f"  - {os.path.basename(file)}")

    # Read Postman
    with open(POSTMAN_PATH, encoding='utf-8') as f:
        postman = json.load(f)
    endpoints = extract_postman_endpoints(postman)

    # Prepare output
    output = []
    total_match_count = 0
    total_no_match_count = 0
    
    # Process each file
    for file_path in all_files:
        print(f"\nProcessing: {os.path.basename(file_path)}")
        df = load_csv_file(file_path)
        if df is None:
            continue
            
        current_scenario = None
        file_match_count = 0
        file_no_match_count = 0
        
        for idx, row in df.iterrows():
            scenario = row['Test Scenarios'] if pd.notna(row['Test Scenarios']) and row['Test Scenarios'].strip() else current_scenario
            test_case = row['Test Case'] if pd.notna(row['Test Case']) and row['Test Case'].strip() else None
            if not test_case or test_case in exclude_test_cases:
                continue
            current_scenario = scenario
            
            # Try to match endpoint based on scenario and test case text
            match_text = f"{scenario} {test_case}"
            endpoint = match_endpoint(match_text, endpoints)
            if endpoint:
                file_match_count += 1
                api_str = f"{endpoint['method']} {endpoint['raw_url']}"
                params = sorted(list(set(endpoint['params']))) if endpoint['params'] else []
                params_str = ', '.join(params) if params else 'None'
            else:
                file_no_match_count += 1
                print(f"  No match found for Scenario: '{scenario}' | Test Case: '{test_case}'")
                api_str = "UNKNOWN"
                params_str = 'None'
            
            input_str = f"Please write an English test case for the following API endpoint.\nAPI Endpoint: {api_str}\nScenario: {scenario}\nParameters: {params_str}\n\nTest Case:"
            output.append({"input": input_str, "output": test_case})
        
        total_match_count += file_match_count
        total_no_match_count += file_no_match_count
        print(f"  File results: {file_match_count} matched, {file_no_match_count} unmatched")
    
    # Write JSONL
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for ex in output:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    print(f"\nTotal results:")
    print(f"Wrote {len(output)} examples to {OUTPUT_PATH}")
    print(f"Total matched endpoints: {total_match_count}, Total unmatched: {total_no_match_count}")

if __name__ == "__main__":
    main() 