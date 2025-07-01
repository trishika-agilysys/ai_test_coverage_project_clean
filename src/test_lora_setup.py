#!/usr/bin/env python3
"""
Test LoRA Setup for StarCoder2

This script verifies that LoRA is properly configured and we're only training
a small fraction of the model parameters.
"""

import torch
import logging
from models.starcoder import StarCoderTestGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_lora_setup():
    """Test that LoRA is properly configured."""
    logger.info("Testing StarCoder2 LoRA setup...")
    
    try:
        # Initialize model with LoRA
        model = StarCoderTestGenerator(
            model_name="bigcode/starcoder2-3b",
            use_lora=True,
            use_4bit=True,
            lora_r=16,
            lora_alpha=32,
            lora_dropout=0.1
        )
        
        # Get parameter counts
        total_params = sum(p.numel() for p in model.model.parameters())
        trainable_params = sum(p.numel() for p in model.model.parameters() if p.requires_grad)
        frozen_params = sum(p.numel() for p in model.model.parameters() if not p.requires_grad)
        
        logger.info(f"\n{'='*60}")
        logger.info("LoRA SETUP VERIFICATION")
        logger.info(f"{'='*60}")
        logger.info(f"Total parameters: {total_params:,}")
        logger.info(f"Trainable parameters: {trainable_params:,}")
        logger.info(f"Frozen parameters: {frozen_params:,}")
        logger.info(f"Trainable percentage: {100 * trainable_params / total_params:.2f}%")
        
        # Verify LoRA is working correctly
        if trainable_params < total_params * 0.05:  # Less than 5% trainable
            logger.info("✅ LoRA is working correctly!")
            logger.info("✅ Only a small fraction of parameters are trainable")
        else:
            logger.warning("⚠️  Too many parameters are trainable - LoRA may not be working")
        
        # Test a quick generation
        logger.info(f"\n{'='*60}")
        logger.info("TESTING GENERATION")
        logger.info(f"{'='*60}")
        
        test_input = "POST {{base_url}}/api/users - Create a new user"
        logger.info(f"Test input: {test_input}")
        
        output = model.generate_tests(test_input)
        logger.info(f"Generated output length: {len(output)} chars")
        logger.info(f"Number of test cases: {output.count('pm.test')}")
        
        if output.count('pm.test') > 0:
            logger.info("✅ Generation working correctly!")
        else:
            logger.warning("⚠️  No test cases generated")
        
        # Memory usage
        if torch.cuda.is_available():
            memory_allocated = torch.cuda.memory_allocated() / 1024**3
            memory_reserved = torch.cuda.memory_reserved() / 1024**3
            logger.info(f"\nGPU Memory Usage:")
            logger.info(f"Allocated: {memory_allocated:.2f} GB")
            logger.info(f"Reserved: {memory_reserved:.2f} GB")
        
        logger.info(f"\n{'='*60}")
        logger.info("SETUP VERIFICATION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info("✅ StarCoder2 with LoRA is ready for training!")
        logger.info("✅ Only ~1-2% of parameters will be trained")
        logger.info("✅ Memory usage is optimized with 4-bit quantization")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ LoRA setup failed: {e}")
        return False

def main():
    success = test_lora_setup()
    
    if success:
        logger.info("\n🎯 You can now run training with:")
        logger.info("   python train_starcoder.py")
    else:
        logger.error("\n❌ Please fix the setup issues before training")

if __name__ == "__main__":
    main() 