import json
import re

INPUT_PATH = "data/processed/augmented_postman_tests_for_training.merged_cleaned.jsonl"
OUTPUT_PATH = "data/processed/augmented_postman_tests_for_training.aggressive.jsonl"
MAX_TESTS = 3  # Keep up to 3 test cases

def clean_todo_comments(js_code):
    """Remove TODO comments and clean up the code"""
    lines = js_code.split('\n')
    # Remove the specific TODO line and any other TODO lines
    cleaned_lines = [line for line in lines if 'TODO: Add more checks based on scenario' not in line and 'TODO' not in line.upper()]
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)
    return result.strip()

def fix_incomplete_output(js_code):
    # Add a closing brace if missing
    if not js_code.strip().endswith('}'):  # crude but effective for Postman tests
        js_code = js_code.rstrip() + '\n}'
    return js_code

def extract_test_blocks(js_code, max_tests=MAX_TESTS):
    lines = js_code.split('\n')
    setup_lines = []
    test_blocks = []
    current_block = []
    in_test_block = False
    for line in lines:
        if line.strip().startswith('eval('):
            setup_lines.append(line)
        elif line.strip().startswith('pm.test('):
            if current_block and in_test_block:
                test_blocks.append('\n'.join(current_block))
            current_block = [line]
            in_test_block = True
        elif in_test_block:
            current_block.append(line)
            if line.strip().endswith('});'):
                test_blocks.append('\n'.join(current_block))
                current_block = []
                in_test_block = False
    if current_block and in_test_block:
        test_blocks.append('\n'.join(current_block))
    # Only keep up to max_tests
    test_blocks = test_blocks[:max_tests]
    return setup_lines, test_blocks

def repair_and_combine(setup_lines, test_blocks):
    # Always include setup if present, then test blocks
    result = ''
    if setup_lines:
        result += '\n'.join(setup_lines) + '\n\n'
    result += '\n\n'.join(test_blocks)
    result = fix_incomplete_output(result)
    return result

def main():
    print(f"Processing {INPUT_PATH} with aggressive repair criteria...")
    print(f"Maximum test cases: {MAX_TESTS}")
    processed_samples = 0
    repaired_samples = 0
    with open(INPUT_PATH, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
        for line_num, line in enumerate(infile, 1):
            try:
                data = json.loads(line.strip())
                input_text = data['input']
                output_text = data['output']
                # Remove TODOs
                output_text = clean_todo_comments(output_text)
                # Extract test blocks
                setup_lines, test_blocks = extract_test_blocks(output_text, MAX_TESTS)
                if not test_blocks:
                    print(f"Line {line_num}: No pm.test blocks found, skipping.")
                    continue  # Only skip if truly no test blocks
                # Repair and combine
                repaired_output = repair_and_combine(setup_lines, test_blocks)
                if repaired_output != output_text:
                    repaired_samples += 1
                new_sample = {'input': input_text, 'output': repaired_output}
                outfile.write(json.dumps(new_sample, ensure_ascii=False) + '\n')
                processed_samples += 1
            except Exception as e:
                print(f"Line {line_num}: Error processing - {e}")
    print(f"\nProcessing complete!")
    print(f"Processed: {processed_samples} samples")
    print(f"Samples repaired: {repaired_samples}")
    print(f"Output saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 