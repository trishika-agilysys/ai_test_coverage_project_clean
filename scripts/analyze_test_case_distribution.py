#!/usr/bin/env python3
"""
Analyze the distribution of test cases in the training data.
"""

import json
import re
from collections import Counter

def analyze_test_case_distribution(data_path):
    """Analyze the distribution of pm.test calls in the training data."""
    
    test_case_counts = []
    total_samples = 0
    valid_samples = 0
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_samples += 1
            try:
                obj = json.loads(line.strip())
                
                if 'input' not in obj or 'output' not in obj:
                    print(f"Line {line_num}: Missing required fields")
                    continue
                
                output = obj['output'].strip()
                if not output:
                    print(f"Line {line_num}: Empty output")
                    continue
                
                # Count pm.test calls
                test_count = output.count('pm.test')
                test_case_counts.append(test_count)
                valid_samples += 1
                
                # Show samples with fewer than 3 test cases
                if test_count < 3:
                    print(f"Line {line_num}: Only {test_count} test cases")
                    print(f"  Input: {obj['input'][:100]}...")
                    print(f"  Output preview: {output[:200]}...")
                    print()
                
            except Exception as e:
                print(f"Line {line_num}: Error parsing: {e}")
    
    # Analyze distribution
    counter = Counter(test_case_counts)
    
    print(f"\n=== ANALYSIS RESULTS ===")
    print(f"Total samples: {total_samples}")
    print(f"Valid samples: {valid_samples}")
    print(f"\nTest case distribution:")
    for count in sorted(counter.keys()):
        percentage = (counter[count] / valid_samples) * 100
        print(f"  {count} test cases: {counter[count]} samples ({percentage:.1f}%)")
    
    print(f"\nSamples that would be filtered out by current criteria:")
    filtered_out = sum(counter[count] for count in counter if count < 3)
    print(f"  < 3 test cases: {filtered_out} samples")
    
    print(f"\nSamples that would pass current criteria:")
    passing = sum(counter[count] for count in counter if count >= 3)
    print(f"  >= 3 test cases: {passing} samples")
    
    return counter

if __name__ == "__main__":
    data_path = "src/data/processed/augmented_postman_tests_for_training.aggressive.jsonl"
    analyze_test_case_distribution(data_path) 