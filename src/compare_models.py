#!/usr/bin/env python3
"""
Model Comparison Script for Postman Test Generation

This script compares CodeT5 and StarCoder2 models to help you choose the best one for your project.
"""

import torch
import logging
from models.codet5 import CodeT5TestGenerator
from models.starcoder import StarCoderTestGenerator
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_performance(model_generator, model_name, test_inputs):
    """Test model performance and generation quality."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing {model_name}")
    logger.info(f"{'='*60}")
    
    # Log model info
    total_params = sum(p.numel() for p in model_generator.model.parameters())
    trainable_params = sum(p.numel() for p in model_generator.model.parameters() if p.requires_grad)
    
    logger.info(f"Total parameters: {total_params:,}")
    logger.info(f"Trainable parameters: {trainable_params:,}")
    logger.info(f"Trainable percentage: {100 * trainable_params / total_params:.2f}%")
    logger.info(f"Device: {model_generator.device}")
    
    if torch.cuda.is_available():
        memory_allocated = torch.cuda.memory_allocated() / 1024**3
        logger.info(f"GPU memory: {memory_allocated:.2f} GB")
    
    # Test generation performance
    generation_times = []
    outputs = []
    
    for i, test_input in enumerate(test_inputs):
        logger.info(f"\nTest {i+1}: {test_input[:100]}...")
        
        start_time = time.time()
        try:
            output = model_generator.generate_tests(test_input)
            generation_time = time.time() - start_time
            generation_times.append(generation_time)
            outputs.append(output)
            
            logger.info(f"Generation time: {generation_time:.2f}s")
            logger.info(f"Output length: {len(output)} chars")
            logger.info(f"Test cases: {output.count('pm.test')}")
            
            # Show first 200 chars of output
            preview = output[:200] + "..." if len(output) > 200 else output
            logger.info(f"Output preview: {preview}")
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            generation_times.append(float('inf'))
            outputs.append("")
    
    # Calculate statistics
    avg_time = sum(t for t in generation_times if t != float('inf')) / len([t for t in generation_times if t != float('inf')])
    success_rate = len([o for o in outputs if o]) / len(outputs)
    
    logger.info(f"\n{model_name} Performance Summary:")
    logger.info(f"Average generation time: {avg_time:.2f}s")
    logger.info(f"Success rate: {success_rate:.1%}")
    
    return {
        'model_name': model_name,
        'total_params': total_params,
        'trainable_params': trainable_params,
        'trainable_percentage': 100 * trainable_params / total_params,
        'avg_generation_time': avg_time,
        'success_rate': success_rate,
        'outputs': outputs
    }

def main():
    # Test inputs (sample API endpoints)
    test_inputs = [
        "POST {{base_url}}/api/users - Create a new user with name, email, and role",
        "GET {{base_url}}/api/products - Retrieve list of products with pagination",
        "PUT {{base_url}}/api/orders/{{order_id}} - Update order status to 'shipped'"
    ]
    
    logger.info("Starting model comparison for Postman test generation...")
    logger.info(f"Testing {len(test_inputs)} sample API endpoints")
    
    results = []
    
    # Test CodeT5
    try:
        logger.info("\nLoading CodeT5 model...")
        codet5_model = CodeT5TestGenerator(
            model_name="Salesforce/codet5-base",
            use_lora=True,
            use_4bit=True,
            lora_r=16,
            lora_alpha=32
        )
        
        codet5_result = test_model_performance(codet5_model, "CodeT5", test_inputs)
        results.append(codet5_result)
        
    except Exception as e:
        logger.error(f"Failed to load CodeT5: {e}")
    
    # Test StarCoder2
    try:
        logger.info("\nLoading StarCoder2 model...")
        starcoder_model = StarCoderTestGenerator(
            model_name="bigcode/starcoder2-3b",
            use_lora=True,
            use_4bit=True,
            lora_r=16,
            lora_alpha=32
        )
        
        starcoder_result = test_model_performance(starcoder_model, "StarCoder2", test_inputs)
        results.append(starcoder_result)
        
    except Exception as e:
        logger.error(f"Failed to load StarCoder2: {e}")
    
    # Print comparison summary
    logger.info(f"\n{'='*80}")
    logger.info("MODEL COMPARISON SUMMARY")
    logger.info(f"{'='*80}")
    
    if len(results) >= 2:
        codet5 = results[0]
        starcoder = results[1]
        
        logger.info(f"{'Metric':<20} {'CodeT5':<15} {'StarCoder2':<15} {'Winner':<10}")
        logger.info("-" * 60)
        
        # Parameter comparison
        logger.info(f"{'Total Params':<20} {codet5['total_params']:<15,} {starcoder['total_params']:<15,} {'CodeT5' if codet5['total_params'] < starcoder['total_params'] else 'StarCoder2'}")
        logger.info(f"{'Trainable %':<20} {codet5['trainable_percentage']:<15.2f} {starcoder['trainable_percentage']:<15.2f} {'CodeT5' if codet5['trainable_percentage'] < starcoder['trainable_percentage'] else 'StarCoder2'}")
        
        # Performance comparison
        logger.info(f"{'Avg Gen Time':<20} {codet5['avg_generation_time']:<15.2f} {starcoder['avg_generation_time']:<15.2f} {'CodeT5' if codet5['avg_generation_time'] < starcoder['avg_generation_time'] else 'StarCoder2'}")
        logger.info(f"{'Success Rate':<20} {codet5['success_rate']:<15.1%} {starcoder['success_rate']:<15.1%} {'CodeT5' if codet5['success_rate'] > starcoder['success_rate'] else 'StarCoder2'}")
        
        # Recommendations
        logger.info(f"\n{'='*80}")
        logger.info("RECOMMENDATIONS")
        logger.info(f"{'='*80}")
        
        if starcoder['success_rate'] > codet5['success_rate']:
            logger.info("🎯 RECOMMENDATION: Use StarCoder2")
            logger.info("   - Better success rate for Postman test generation")
            logger.info("   - More natural JavaScript/TypeScript code generation")
            logger.info("   - Optimized for programming tasks")
        else:
            logger.info("🎯 RECOMMENDATION: Use CodeT5")
            logger.info("   - Better success rate for your specific use case")
            logger.info("   - Smaller model size")
            logger.info("   - Faster generation")
        
        logger.info(f"\n💡 For your 148-sample dataset:")
        logger.info(f"   - StarCoder2: Better code quality, slightly slower")
        logger.info(f"   - CodeT5: Faster training, smaller memory footprint")
        
    else:
        logger.error("Could not compare models - at least one failed to load")

if __name__ == "__main__":
    main() 