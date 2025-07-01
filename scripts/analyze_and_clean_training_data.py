#!/usr/bin/env python3
"""
Script to analyze and clean training data for better model performance.
"""

import json
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_training_data(data_path: str):
    """Analyze the training data and identify issues."""
    logger.info(f"Analyzing training data from: {data_path}")
    
    total_samples = 0
    valid_samples = 0
    issues = {
        'empty_input': 0,
        'empty_output': 0,
        'short_output': 0,
        'todo_comments': 0,
        'few_tests': 0,
        'incomplete_output': 0,
        'malformed_json': 0
    }
    
    cleaned_data = []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            total_samples += 1
            
            try:
                obj = json.loads(line)
                
                # Check for required fields
                if 'input' not in obj or 'output' not in obj:
                    issues['malformed_json'] += 1
                    continue
                
                input_text = obj['input'].strip()
                output_text = obj['output'].strip()
                
                # Check for empty fields
                if not input_text:
                    issues['empty_input'] += 1
                    continue
                    
                if not output_text:
                    issues['empty_output'] += 1
                    continue
                
                # Check for very short outputs (more lenient)
                if len(output_text) < 50:
                    issues['short_output'] += 1
                    continue
                
                # Check for TODO comments (but be more lenient)
                if 'TODO' in output_text and output_text.count('TODO') > 2:
                    issues['todo_comments'] += 1
                    continue
                
                # Check for too few test cases (more lenient)
                test_count = output_text.count('pm.test')
                if test_count < 1:  # Allow at least 1 test case
                    issues['few_tests'] += 1
                    continue
                
                # Check for incomplete outputs (more lenient)
                if not output_text.endswith('}') and not output_text.endswith(';'):
                    # Check if it's at least 80% complete
                    if len(output_text) < 500:  # Very short outputs might be incomplete
                        issues['incomplete_output'] += 1
                        continue
                
                # Additional quality checks (more lenient)
                if not output_text.startswith('eval(') and not output_text.startswith('pm.test'):
                    logger.warning(f"Line {line_num}: Output doesn't start with expected pattern")
                    # Don't reject, just warn
                
                # Check for balanced braces (more lenient)
                brace_diff = output_text.count('{') - output_text.count('}')
                if abs(brace_diff) > 2:  # Allow some imbalance
                    logger.warning(f"Line {line_num}: Significant brace imbalance ({brace_diff})")
                    # Don't reject, just warn
                
                # Check for proper test structure (more lenient)
                if not re.search(r'pm\.test\([^)]+\)', output_text):
                    logger.warning(f"Line {line_num}: No proper pm.test() calls found")
                    # Don't reject, just warn
                
                # If we get here, the sample is valid
                valid_samples += 1
                cleaned_data.append({
                    'input': input_text,
                    'output': output_text
                })
                
            except json.JSONDecodeError:
                issues['malformed_json'] += 1
                continue
    
    # Print analysis results
    logger.info(f"Analysis Results:")
    logger.info(f"Total samples: {total_samples}")
    logger.info(f"Valid samples: {valid_samples}")
    logger.info(f"Rejection rate: {((total_samples - valid_samples) / total_samples * 100):.1f}%")
    
    logger.info(f"\nIssues found:")
    for issue, count in issues.items():
        if count > 0:
            logger.info(f"  {issue}: {count}")
    
    return cleaned_data

def save_cleaned_data(cleaned_data, output_path: str):
    """Save the cleaned data to a new file."""
    logger.info(f"Saving {len(cleaned_data)} cleaned samples to: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in cleaned_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
    
    logger.info("Cleaned data saved successfully!")

def main():
    input_path = "augmented_postman_tests_for_training.merged_cleaned.jsonl"
    output_path = "augmented_postman_tests_for_training.cleaned_improved.jsonl"
    
    if not Path(input_path).exists():
        logger.error(f"Input file not found: {input_path}")
        return
    
    # Analyze and clean the data
    cleaned_data = analyze_training_data(input_path)
    
    if cleaned_data:
        save_cleaned_data(cleaned_data, output_path)
        
        # Print some statistics about the cleaned data
        input_lengths = [len(item['input']) for item in cleaned_data]
        output_lengths = [len(item['output']) for item in cleaned_data]
        test_counts = [item['output'].count('pm.test') for item in cleaned_data]
        
        logger.info(f"\nCleaned data statistics:")
        logger.info(f"Input length - Min: {min(input_lengths)}, Max: {max(input_lengths)}, Avg: {sum(input_lengths)/len(input_lengths):.1f}")
        logger.info(f"Output length - Min: {min(output_lengths)}, Max: {max(output_lengths)}, Avg: {sum(output_lengths)/len(output_lengths):.1f}")
        logger.info(f"Test cases - Min: {min(test_counts)}, Max: {max(test_counts)}, Avg: {sum(test_counts)/len(test_counts):.1f}")
    else:
        logger.error("No valid samples found after cleaning!")

if __name__ == "__main__":
    main() 