# src/evaluate_trained_model.py
import torch
from models.codet5 import CodeT5TestGenerator
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import re
from difflib import SequenceMatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self, model_path: str):
        """
        Initialize model evaluator.
        
        Args:
            model_path: Path to the trained model checkpoint
        """
        self.model_path = Path(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load model and tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)
        self.model.to(self.device)
        self.model.eval()
        
        logger.info(f"Model loaded from: {model_path}")
        logger.info(f"Using device: {self.device}")
    
    def generate_test(self, input_text: str, max_length: int = 512) -> str:
        """Generate test case for given input."""
        inputs = self.tokenizer(
            input_text,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=max_length,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
                length_penalty=1.0,
                repetition_penalty=1.2
            )
        
        generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return generated_text
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using SequenceMatcher."""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def extract_test_functions(self, text: str) -> List[str]:
        """Extract test function names from generated text."""
        pattern = r'pm\.test\("([^"]+)"'
        matches = re.findall(pattern, text)
        return matches
    
    def count_test_assertions(self, text: str) -> int:
        """Count the number of test assertions in the text."""
        patterns = [
            r'pm\.expect\(',
            r'pm\.response\.to\.have\.status\(',
            r'pm\.response\.to\.be\.json\(',
            r'pm\.response\.to\.have\.property\('
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text))
        return count
    
    def evaluate_single_example(self, input_text: str, expected_output: str) -> Dict[str, Any]:
        """Evaluate a single input-output pair."""
        generated_output = self.generate_test(input_text)
        
        # Calculate metrics
        similarity = self.calculate_similarity(generated_output, expected_output)
        
        expected_tests = self.extract_test_functions(expected_output)
        generated_tests = self.extract_test_functions(generated_output)
        
        expected_assertions = self.count_test_assertions(expected_output)
        generated_assertions = self.count_test_assertions(generated_output)
        
        # Calculate test coverage
        test_coverage = len(set(generated_tests) & set(expected_tests)) / len(expected_tests) if expected_tests else 0
        
        # Calculate assertion coverage
        assertion_coverage = min(generated_assertions / expected_assertions, 1.0) if expected_assertions > 0 else 0
        
        return {
            'input': input_text,
            'expected_output': expected_output,
            'generated_output': generated_output,
            'similarity': similarity,
            'expected_test_count': len(expected_tests),
            'generated_test_count': len(generated_tests),
            'test_coverage': test_coverage,
            'expected_assertions': expected_assertions,
            'generated_assertions': generated_assertions,
            'assertion_coverage': assertion_coverage,
            'expected_tests': expected_tests,
            'generated_tests': generated_tests
        }
    
    def evaluate_dataset(self, data_path: str, num_samples: int = 10) -> Dict[str, Any]:
        """Evaluate model on a dataset."""
        # Load test data
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
        
        # Sample data for evaluation
        if num_samples < len(test_data):
            import random
            test_data = random.sample(test_data, num_samples)
        
        logger.info(f"Evaluating on {len(test_data)} samples...")
        
        results = []
        total_similarity = 0
        total_test_coverage = 0
        total_assertion_coverage = 0
        
        for i, item in enumerate(test_data):
            logger.info(f"Evaluating sample {i+1}/{len(test_data)}")
            result = self.evaluate_single_example(item['input'], item['output'])
            results.append(result)
            
            total_similarity += result['similarity']
            total_test_coverage += result['test_coverage']
            total_assertion_coverage += result['assertion_coverage']
        
        # Calculate averages
        avg_similarity = total_similarity / len(results)
        avg_test_coverage = total_test_coverage / len(results)
        avg_assertion_coverage = total_assertion_coverage / len(results)
        
        return {
            'results': results,
            'summary': {
                'num_samples': len(results),
                'avg_similarity': avg_similarity,
                'avg_test_coverage': avg_test_coverage,
                'avg_assertion_coverage': avg_assertion_coverage
            }
        }
    
    def generate_sample_tests(self, num_samples: int = 5) -> List[Dict[str, str]]:
        """Generate sample test cases for demonstration."""
        sample_inputs = [
            "Generate all Postman JavaScript tests for: POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [EMV, No Tip, No Sig] Validate Successful Sale On Device Response\n\nNow, write the JavaScript code:",
            "Generate all Postman JavaScript tests for: POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [Tap, Tip, No Sig] Validate Successful Sale On Device Response\n\nNow, write the JavaScript code:",
            "Generate all Postman JavaScript tests for: POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [Swipe, Manual Tip, No Sig] Validate Successful Sale On Device Response\n\nNow, write the JavaScript code:",
            "Generate all Postman JavaScript tests for: POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [EMV, No Tip, No Sig, $0.01] Validate Successful Sale On Device Response\n\nNow, write the JavaScript code:",
            "Generate all Postman JavaScript tests for: POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [EMV, Tip Percentage, No Sig] Validate Successful Sale On Device Response\n\nNow, write the JavaScript code:"
        ]
        
        generated_tests = []
        for i, input_text in enumerate(sample_inputs[:num_samples]):
            logger.info(f"Generating test {i+1}/{num_samples}")
            generated_output = self.generate_test(input_text)
            generated_tests.append({
                'input': input_text,
                'generated_output': generated_output
            })
        
        return generated_tests

def main():
    # Path to your trained model (update this path)
    model_path = "src/data/models/checkpoints/6_27_merged"  # Update with your actual checkpoint path
    
    # Initialize evaluator
    evaluator = ModelEvaluator(model_path)
    
    # Generate sample tests
    logger.info("Generating sample test cases...")
    sample_tests = evaluator.generate_sample_tests(5)
    
    # Save sample tests
    output_file = "generated_sample_tests.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_tests, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Sample tests saved to: {output_file}")
    
    # Evaluate on test dataset
    logger.info("Evaluating model performance...")
    evaluation_results = evaluator.evaluate_dataset(
        "augmented_postman_tests_for_training.merged_cleaned.jsonl",
        num_samples=10
    )
    
    # Print evaluation summary
    summary = evaluation_results['summary']
    logger.info("=== Evaluation Summary ===")
    logger.info(f"Number of samples: {summary['num_samples']}")
    logger.info(f"Average similarity: {summary['avg_similarity']:.4f}")
    logger.info(f"Average test coverage: {summary['avg_test_coverage']:.4f}")
    logger.info(f"Average assertion coverage: {summary['avg_assertion_coverage']:.4f}")
    
    # Save detailed results
    results_file = "evaluation_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Detailed results saved to: {results_file}")
    
    # Print some example comparisons
    logger.info("\n=== Sample Comparisons ===")
    for i, result in enumerate(evaluation_results['results'][:3]):
        logger.info(f"\nSample {i+1}:")
        logger.info(f"Similarity: {result['similarity']:.4f}")
        logger.info(f"Test coverage: {result['test_coverage']:.4f}")
        logger.info(f"Assertion coverage: {result['assertion_coverage']:.4f}")
        logger.info(f"Expected tests: {result['expected_test_count']}")
        logger.info(f"Generated tests: {result['generated_test_count']}")

if __name__ == "__main__":
    main() 