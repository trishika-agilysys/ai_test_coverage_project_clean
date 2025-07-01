#!/usr/bin/env python3
"""
Validate training data for CodeT5 model.
This script checks the format and quality of the training data.
"""

import json
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_training_data(file_path: str) -> Dict[str, Any]:
    """Validate the training data format and content."""
    logger.info(f"Validating training data from: {file_path}")
    
    samples = []
    errors = []
    warnings = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                sample = json.loads(line)
                samples.append(sample)
                
                # Validate required fields
                if 'input' not in sample:
                    errors.append(f"Line {line_num}: Missing 'input' field")
                if 'output' not in sample:
                    errors.append(f"Line {line_num}: Missing 'output' field")
                
                # Validate field types
                if 'input' in sample and not isinstance(sample['input'], str):
                    errors.append(f"Line {line_num}: 'input' must be a string")
                if 'output' in sample and not isinstance(sample['output'], str):
                    errors.append(f"Line {line_num}: 'output' must be a string")
                
                # Validate content
                if 'input' in sample and len(sample['input'].strip()) == 0:
                    warnings.append(f"Line {line_num}: Empty input")
                if 'output' in sample and len(sample['output'].strip()) == 0:
                    warnings.append(f"Line {line_num}: Empty output")
                
                # Check for reasonable lengths
                if 'input' in sample and len(sample['input']) > 500:
                    warnings.append(f"Line {line_num}: Input too long ({len(sample['input'])} chars)")
                if 'output' in sample and len(sample['output']) > 1000:
                    warnings.append(f"Line {line_num}: Output too long ({len(sample['output'])} chars)")
                
                # Check for Postman test patterns
                if 'output' in sample and 'pm.test(' not in sample['output']:
                    warnings.append(f"Line {line_num}: Output doesn't contain Postman test pattern")
                
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: JSON decode error: {e}")
    
    # Analyze the data
    if samples:
        input_lengths = [len(sample.get('input', '')) for sample in samples]
        output_lengths = [len(sample.get('output', '')) for sample in samples]
        
        # Check for diversity
        unique_inputs = len(set(sample.get('input', '') for sample in samples))
        diversity_rate = unique_inputs / len(samples) * 100
        
        analysis = {
            'total_samples': len(samples),
            'unique_inputs': unique_inputs,
            'diversity_rate': diversity_rate,
            'input_length_stats': {
                'min': min(input_lengths),
                'max': max(input_lengths),
                'avg': sum(input_lengths) / len(input_lengths),
                'median': sorted(input_lengths)[len(input_lengths)//2]
            },
            'output_length_stats': {
                'min': min(output_lengths),
                'max': max(output_lengths),
                'avg': sum(output_lengths) / len(output_lengths),
                'median': sorted(output_lengths)[len(output_lengths)//2]
            },
            'errors': errors,
            'warnings': warnings,
            'is_valid': len(errors) == 0
        }
    else:
        analysis = {
            'total_samples': 0,
            'errors': errors,
            'warnings': warnings,
            'is_valid': False
        }
    
    return analysis

def print_validation_report(analysis: Dict[str, Any]):
    """Print a comprehensive validation report."""
    print("\n" + "="*60)
    print("TRAINING DATA VALIDATION REPORT")
    print("="*60)
    
    print(f"📊 Dataset Statistics:")
    print(f"  Total samples: {analysis['total_samples']}")
    if 'unique_inputs' in analysis:
        print(f"  Unique inputs: {analysis['unique_inputs']}")
        print(f"  Diversity rate: {analysis['diversity_rate']:.1f}%")
    
    if 'input_length_stats' in analysis:
        print(f"\n📏 Input Length Statistics:")
        stats = analysis['input_length_stats']
        print(f"  Min: {stats['min']} chars")
        print(f"  Max: {stats['max']} chars")
        print(f"  Average: {stats['avg']:.0f} chars")
        print(f"  Median: {stats['median']} chars")
    
    if 'output_length_stats' in analysis:
        print(f"\n📏 Output Length Statistics:")
        stats = analysis['output_length_stats']
        print(f"  Min: {stats['min']} chars")
        print(f"  Max: {stats['max']} chars")
        print(f"  Average: {stats['avg']:.0f} chars")
        print(f"  Median: {stats['median']} chars")
    
    if analysis['errors']:
        print(f"\n❌ ERRORS ({len(analysis['errors'])}):")
        for error in analysis['errors']:
            print(f"  • {error}")
    
    if analysis['warnings']:
        print(f"\n⚠️  WARNINGS ({len(analysis['warnings'])}):")
        for warning in analysis['warnings']:
            print(f"  • {warning}")
    
    print(f"\n{'✅ VALID' if analysis['is_valid'] else '❌ INVALID'}")
    
    if analysis['is_valid']:
        print(f"\n🎉 Training data is ready for CodeT5 training!")
        
        # Provide recommendations
        if 'diversity_rate' in analysis and analysis['diversity_rate'] < 80:
            print(f"💡 Consider adding more diverse samples (current diversity: {analysis['diversity_rate']:.1f}%)")
        
        if 'output_length_stats' in analysis and analysis['output_length_stats']['avg'] > 800:
            print(f"💡 Consider shortening outputs (current avg: {analysis['output_length_stats']['avg']:.0f} chars)")
    
    print("="*60)

def main():
    """Main function to validate training data."""
    file_path = "improved_training_data.jsonl"
    
    try:
        analysis = validate_training_data(file_path)
        print_validation_report(analysis)
        
        if analysis['is_valid']:
            logger.info("✅ Training data validation passed!")
            return True
        else:
            logger.error("❌ Training data validation failed!")
            return False
            
    except FileNotFoundError:
        logger.error(f"❌ Training data file not found: {file_path}")
        print(f"\n💡 Run 'python analyze_and_fix_training_data.py' first to create the improved dataset.")
        return False
    except Exception as e:
        logger.error(f"❌ Error during validation: {e}")
        return False

if __name__ == "__main__":
    main() 