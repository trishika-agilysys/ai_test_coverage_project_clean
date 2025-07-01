import json
import re

INPUT_FILE = '../augmented_postman_tests_for_training.merged_cleaned.jsonl'
OUTPUT_FILE = '../augmented_postman_tests_for_training.cleaned_no_prompt.jsonl'

def main():
    # Read all lines
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = [json.loads(line) for line in f if line.strip()]
    
    # Remove the problematic phrase from input
    cleaned_lines = []
    for entry in lines:
        # Remove "Now, write the JavaScript code:" from input
        cleaned_input = entry['input'].replace("\nNow, write the JavaScript code:", "")
        cleaned_lines.append({
            'input': cleaned_input,
            'output': entry['output']
        })
    
    # Write cleaned data
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for entry in cleaned_lines:
            json.dump(entry, out)
            out.write('\n')
    
    print(f"Cleaned {len(cleaned_lines)} training examples")
    print(f"Removed 'Now, write the JavaScript code:' phrase from all inputs")

if __name__ == '__main__':
    main() 