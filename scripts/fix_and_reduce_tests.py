#!/usr/bin/env python3
"""
Script to fix missing closing braces in pm.test blocks and reduce to first 3 test cases per sample.
"""
import json
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_and_extract_tests(output_text, max_tests=3):
    """Fix missing closing braces and extract up to max_tests pm.test blocks."""
    fixed_blocks = []
    idx = 0
    count = 0
    while count < max_tests:
        start = output_text.find('pm.test(', idx)
        if start == -1:
            break
        func_start = output_text.find('function', start)
        brace_start = output_text.find('{', func_start)
        if brace_start == -1:
            break
        # Brace counting
        brace_count = 1
        i = brace_start + 1
        while i < len(output_text) and brace_count > 0:
            if output_text[i] == '{':
                brace_count += 1
            elif output_text[i] == '}':
                brace_count -= 1
            i += 1
        # If the next chars are not ');', add them
        end = i
        while end < len(output_text) and output_text[end] in ' \n\r;':
            end += 1
        if not output_text[i:i+2] == ');':
            test_block = output_text[start:i] + ');'
        else:
            test_block = output_text[start:i+2]
        fixed_blocks.append(test_block.strip())
        idx = i
        count += 1
    return '\n\n'.join(fixed_blocks)

def process_file(input_path, output_path, max_tests=3):
    logger.info(f"Processing {input_path} -> {output_path}")
    processed = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if 'output' in obj:
                    fixed = fix_and_extract_tests(obj['output'], max_tests)
                    obj['output'] = fixed
                processed.append(obj)
            except Exception as e:
                logger.warning(f"Line {line_num}: {e}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for obj in processed:
            json.dump(obj, f, ensure_ascii=False)
            f.write('\n')
    logger.info(f"Wrote {len(processed)} samples.")

def main():
    input_path = "augmented_postman_tests_for_training.reduced_tests.jsonl"
    output_path = "augmented_postman_tests_for_training.fixed_reduced.jsonl"
    process_file(input_path, output_path, max_tests=3)

if __name__ == "__main__":
    main() 