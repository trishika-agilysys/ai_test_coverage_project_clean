# src/test_improved_model.py
import json
import logging
from pathlib import Path
from models.codet5 import CodeT5TestGenerator
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_generation(model_path: str, test_samples: int = 5):
    """Test the trained model on sample inputs."""
    
    # Load the trained model
    model = CodeT5TestGenerator(
        model_name=model_path,
        max_input_length=512,
        max_output_length=2048
    )
    
    # Load test data
    test_data = []
    with open("augmented_postman_tests_for_training.merged_cleaned.jsonl", 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    test_data.append(obj)
                except Exception as e:
                    logger.warning(f"Skipping malformed line: {e}")
    
    logger.info(f"Testing model on {min(test_samples, len(test_data))} samples...")
    
    for i in range(min(test_samples, len(test_data))):
        sample = test_data[i]
        input_text = sample['input']
        expected_output = sample['output']
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Sample {i+1}")
        logger.info(f"{'='*80}")
        
        # Generate output
        generated_output = model.generate_test_case(input_text)
        
        # Analyze outputs
        expected_test_count = expected_output.count('pm.test(')
        generated_test_count = generated_output.count('pm.test(')
        
        expected_length = len(expected_output)
        generated_length = len(generated_output)
        
        logger.info(f"Input: {input_text}")
        logger.info(f"\nGenerated Output ({generated_length} chars, {generated_test_count} tests):")
        logger.info(f"{generated_output}")
        logger.info(f"\nExpected Output ({expected_length} chars, {expected_test_count} tests):")
        logger.info(f"{expected_output}")
        
        # Calculate metrics
        length_ratio = generated_length / expected_length if expected_length > 0 else 0
        test_count_ratio = generated_test_count / expected_test_count if expected_test_count > 0 else 0
        
        logger.info(f"\nMetrics:")
        logger.info(f"  Length ratio: {length_ratio:.2f} (target: 1.0)")
        logger.info(f"  Test count ratio: {test_count_ratio:.2f} (target: 1.0)")
        
        # Check for key components
        key_components = [
            'pm.response.to.have.status(200)',
            'transactionReferenceData',
            'cardInfo',
            'gatewayResponseData',
            'pm.expect(',
            'pm.test('
        ]
        
        logger.info(f"\nKey component analysis:")
        for component in key_components:
            expected_has = component in expected_output
            generated_has = component in generated_output
            status = "✅" if expected_has == generated_has else "❌"
            logger.info(f"  {component}: {status} (Expected: {expected_has}, Generated: {generated_has})")

def find_latest_checkpoint():
    """Find the latest checkpoint directory."""
    checkpoint_dir = Path("src/data/models/checkpoints")
    if not checkpoint_dir.exists():
        return None
    
    # Find directories with timestamps
    checkpoints = [d for d in checkpoint_dir.iterdir() if d.is_dir() and d.name.startswith("202")]
    if not checkpoints:
        return None
    
    # Return the most recent one
    return str(sorted(checkpoints)[-1])

def main():
    # Find the latest checkpoint
    checkpoint_path = find_latest_checkpoint()
    
    if not checkpoint_path:
        logger.error("No checkpoint found. Please train the model first.")
        return
    
    logger.info(f"Testing model from: {checkpoint_path}")
    
    # Test the model
    test_model_generation(checkpoint_path, test_samples=3)

if __name__ == "__main__":
    main() 