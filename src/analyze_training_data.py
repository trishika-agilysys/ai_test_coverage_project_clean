#!/usr/bin/env python3
"""
Script to analyze training data quality for the CodeT5 test generation model.
"""

import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_training_data(data_path: str):
    """Analyze the training data file and provide statistics."""
    logger.info(f"Analyzing training data from: {data_path}")
    
    data = []
    if data_path.endswith('.jsonl'):
        with open(data_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        obj = json.loads(line)
                        data.append(obj)
                    except Exception as e:
                        logger.error(f"Line {line_num}: JSON parsing error: {e}")
    else:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    logger.info(f"Total samples: {len(data)}")
    
    if not data:
        logger.error("No valid data found!")
        return
    
    # Analyze input/output lengths
    input_lengths = []
    output_lengths = []
    valid_samples = 0
    
    for i, item in enumerate(data):
        if 'input' not in item or 'output' not in item:
            logger.warning(f"Sample {i}: Missing 'input' or 'output' field")
            continue
        
        input_text = item['input'].strip()
        output_text = item['output'].strip()
        
        if not input_text or not output_text:
            logger.warning(f"Sample {i}: Empty input or output")
            continue
        
        input_lengths.append(len(input_text))
        output_lengths.append(len(output_text))
        valid_samples += 1
    
    logger.info(f"Valid samples: {valid_samples}/{len(data)}")
    
    if valid_samples == 0:
        logger.error("No valid samples found!")
        return
    
    # Statistics
    logger.info(f"Input length statistics:")
    logger.info(f"  Min: {min(input_lengths)}")
    logger.info(f"  Max: {max(input_lengths)}")
    logger.info(f"  Average: {sum(input_lengths)/len(input_lengths):.1f}")
    logger.info(f"  Median: {sorted(input_lengths)[len(input_lengths)//2]}")
    
    logger.info(f"Output length statistics:")
    logger.info(f"  Min: {min(output_lengths)}")
    logger.info(f"  Max: {max(output_lengths)}")
    logger.info(f"  Average: {sum(output_lengths)/len(output_lengths):.1f}")
    logger.info(f"  Median: {sorted(output_lengths)[len(output_lengths)//2]}")
    
    # Show sample inputs and outputs
    logger.info("\nSample data:")
    for i in range(min(3, len(data))):
        item = data[i]
        logger.info(f"Sample {i+1}:")
        logger.info(f"  Input: {item.get('input', 'MISSING')[:100]}...")
        logger.info(f"  Output: {item.get('output', 'MISSING')[:100]}...")
        logger.info("")
    
    # Check for common patterns
    input_patterns = {}
    output_patterns = {}
    
    for item in data[:10]:  # Check first 10 samples
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # Check input patterns
        if 'Generate all Postman JavaScript tests for:' in input_text:
            input_patterns['postman_test_generation'] = input_patterns.get('postman_test_generation', 0) + 1
        
        # Check output patterns
        if 'pm.test(' in output_text:
            output_patterns['pm_test'] = output_patterns.get('pm_test', 0) + 1
        if 'pm.expect(' in output_text:
            output_patterns['pm_expect'] = output_patterns.get('pm_expect', 0) + 1
        if 'pm.response.to.have.status(200)' in output_text:
            output_patterns['status_200_check'] = output_patterns.get('status_200_check', 0) + 1
    
    logger.info("Input patterns (first 10 samples):")
    for pattern, count in input_patterns.items():
        logger.info(f"  {pattern}: {count}")
    
    logger.info("Output patterns (first 10 samples):")
    for pattern, count in output_patterns.items():
        logger.info(f"  {pattern}: {count}")

def main():
    data_path = "../augmented_postman_tests_for_training.merged_cleaned.jsonl"
    
    if not Path(data_path).exists():
        logger.error(f"Data file not found: {data_path}")
        return
    
    analyze_training_data(data_path)

if __name__ == "__main__":
    main() 