# src/evaluate_model.py
from models.codet5 import CodeT5TestGenerator
import json
import logging
from typing import List, Dict, Any
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_test_data(data_path: str) -> List[Dict[str, str]]:
    """Load test data from JSONL file."""
    test_data = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    test_data.append(obj)
                except Exception as e:
                    logger.warning(f"Skipping malformed line: {e}")
    return test_data

def calculate_metrics(generated: str, expected: str) -> Dict[str, float]:
    """Calculate various metrics for generated vs expected output."""
    metrics = {}
    
    # Basic length metrics
    metrics['generated_length'] = len(generated)
    metrics['expected_length'] = len(expected)
    metrics['length_ratio'] = len(generated) / len(expected) if len(expected) > 0 else 0
    
    # Code structure metrics
    generated_lines = generated.split('\n')
    expected_lines = expected.split('\n')
    
    metrics['generated_lines'] = len(generated_lines)
    metrics['expected_lines'] = len(expected_lines)
    
    # Count test functions
    generated_tests = len(re.findall(r'pm\.test\(', generated))
    expected_tests = len(re.findall(r'pm\.test\(', expected))
    metrics['test_count_ratio'] = generated_tests / expected_tests if expected_tests > 0 else 0
    
    # Count assertions
    generated_assertions = len(re.findall(r'pm\.expect\(', generated))
    expected_assertions = len(re.findall(r'pm\.expect\(', expected))
    metrics['assertion_count_ratio'] = generated_assertions / expected_assertions if expected_assertions > 0 else 0
    
    # Repetition metrics
    words = generated.split()
    if len(words) > 0:
        unique_words = len(set(words))
        metrics['repetition_ratio'] = 1 - (unique_words / len(words))
    else:
        metrics['repetition_ratio'] = 0
    
    # Syntax validity (basic check)
    syntax_errors = 0
    if not generated.strip().endswith(';') and not generated.strip().endswith('}'):
        syntax_errors += 1
    if generated.count('(') != generated.count(')'):
        syntax_errors += 1
    if generated.count('{') != generated.count('}'):
        syntax_errors += 1
    
    metrics['syntax_errors'] = syntax_errors
    
    return metrics

def evaluate_model(model_path: str, test_data_path: str, num_samples: int = 10):
    """Evaluate the model on test data."""
    
    # Load model
    model = CodeT5TestGenerator(
        model_name=model_path,
        max_input_length=512,
        max_output_length=512
    )
    
    # Load test data
    test_data = load_test_data(test_data_path)
    
    # Sample test cases
    sample_data = test_data[:num_samples]
    
    print(f"=== Model Evaluation ===\n")
    print(f"Model: {model_path}")
    print(f"Test samples: {len(sample_data)}\n")
    
    all_metrics = []
    
    for i, sample in enumerate(sample_data, 1):
        print(f"Sample {i}:")
        print(f"Input: {sample['input']}")
        
        try:
            generated_output = model.generate_test_case(sample['input'])
            expected_output = sample['output']
            
            # Calculate metrics
            metrics = calculate_metrics(generated_output, expected_output)
            all_metrics.append(metrics)
            
            print(f"Generated length: {metrics['generated_length']}")
            print(f"Expected length: {metrics['expected_length']}")
            print(f"Length ratio: {metrics['length_ratio']:.2f}")
            print(f"Test count ratio: {metrics['test_count_ratio']:.2f}")
            print(f"Assertion count ratio: {metrics['assertion_count_ratio']:.2f}")
            print(f"Repetition ratio: {metrics['repetition_ratio']:.2f}")
            print(f"Syntax errors: {metrics['syntax_errors']}")
            
            print("\nGenerated Output (first 200 chars):")
            print(generated_output[:200] + "..." if len(generated_output) > 200 else generated_output)
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "-"*60 + "\n")
    
    # Calculate average metrics
    if all_metrics:
        avg_metrics = {}
        for key in all_metrics[0].keys():
            avg_metrics[key] = sum(m[key] for m in all_metrics) / len(all_metrics)
        
        print("=== Average Metrics ===")
        for key, value in avg_metrics.items():
            print(f"{key}: {value:.3f}")

if __name__ == "__main__":
    # Evaluate the current model
    evaluate_model(
        model_path="src/data/models/checkpoints/6_26_split/checkpoint-epoch-6",
        test_data_path="augmented_postman_tests_for_training.split_cleaned.jsonl",
        num_samples=5
    ) 