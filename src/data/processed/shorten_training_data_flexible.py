import json
import re

INPUT_PATH = "data/processed/augmented_postman_tests_for_training.merged_cleaned.jsonl"
OUTPUT_PATH = "data/processed/augmented_postman_tests_for_training.flexible.jsonl"
MIN_TESTS = 2  # Accept samples with at least 2 test cases
MAX_TESTS = 3  # Keep up to 3 test cases

def clean_todo_comments(js_code):
    """Remove TODO comments from the code"""
    # Remove lines containing TODO comments
    lines = js_code.split('\n')
    cleaned_lines = []
    for line in lines:
        if 'TODO' not in line.upper():
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def shorten_tests(js_code, min_tests=MIN_TESTS, max_tests=MAX_TESTS):
    # Split the code into lines to process it more carefully
    lines = js_code.split('\n')
    
    # Find the eval line (setup code)
    setup_lines = []
    test_blocks = []
    current_block = []
    in_test_block = False
    test_count = 0
    
    for line in lines:
        if line.strip().startswith('eval('):
            setup_lines.append(line)
        elif line.strip().startswith('pm.test('):
            if current_block and in_test_block:
                test_blocks.append('\n'.join(current_block))
                test_count += 1
                if test_count >= max_tests:
                    break
            current_block = [line]
            in_test_block = True
        elif in_test_block:
            current_block.append(line)
            if line.strip().endswith('});'):
                test_blocks.append('\n'.join(current_block))
                test_count += 1
                current_block = []
                in_test_block = False
                if test_count >= max_tests:
                    break
    
    # Add any remaining test block
    if current_block and in_test_block and test_count < max_tests:
        test_blocks.append('\n'.join(current_block))
        test_count += 1
    
    # Accept samples with at least MIN_TESTS test blocks
    if test_count < min_tests:
        print(f"Warning: Only found {test_count} test blocks, minimum required is {min_tests}")
        return None  # Skip this sample
    
    # Combine setup code with test blocks
    result = '\n'.join(setup_lines) + '\n\n' + '\n\n'.join(test_blocks)
    
    # Ensure the result ends properly
    if not result.strip().endswith('}'):
        result = result.rstrip() + '\n}'
    
    return result

def main():
    print(f"Processing {INPUT_PATH} with flexible criteria...")
    print(f"Minimum test cases: {MIN_TESTS}")
    print(f"Maximum test cases: {MAX_TESTS}")
    
    processed_samples = 0
    skipped_samples = 0
    todo_cleaned = 0
    
    with open(INPUT_PATH, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            try:
                data = json.loads(line.strip())
                input_text = data['input']
                output_text = data['output']
                
                # Check if sample has TODO comments
                has_todo = 'TODO' in output_text.upper()
                if has_todo:
                    print(f"Line {line_num}: Cleaning TODO comments")
                    output_text = clean_todo_comments(output_text)
                    todo_cleaned += 1
                
                # Shorten the tests
                shortened_output = shorten_tests(output_text, MIN_TESTS, MAX_TESTS)
                
                if shortened_output is None:
                    print(f"Line {line_num}: Skipping - insufficient test blocks")
                    skipped_samples += 1
                    continue
                
                # Create new sample
                new_sample = {
                    'input': input_text,
                    'output': shortened_output
                }
                
                # Write to output file
                outfile.write(json.dumps(new_sample, ensure_ascii=False) + '\n')
                processed_samples += 1
                
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: JSON decode error - {e}")
                skipped_samples += 1
            except Exception as e:
                print(f"Line {line_num}: Error processing - {e}")
                skipped_samples += 1
    
    print(f"\nProcessing complete!")
    print(f"Processed: {processed_samples} samples")
    print(f"Skipped: {skipped_samples} samples")
    print(f"TODO comments cleaned: {todo_cleaned} samples")
    print(f"Output saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 