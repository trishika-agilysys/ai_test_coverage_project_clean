#!/usr/bin/env python3
"""
Test the training setup with improved data.
This script verifies that the model and trainer can load the improved training data correctly.
"""

import sys
import os
import json
import logging
from pathlib import Path

# Add src to path
sys.path.append('src')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_data_loading():
    """Test that the improved training data can be loaded correctly."""
    logger.info("Testing data loading...")
    
    data_file = "improved_training_data.jsonl"
    if not os.path.exists(data_file):
        logger.error(f"❌ Training data file not found: {data_file}")
        return False
    
    samples = []
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    sample = json.loads(line)
                    samples.append(sample)
        
        logger.info(f"✅ Successfully loaded {len(samples)} samples")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading data: {e}")
        return False

def test_model_import():
    """Test that the model classes can be imported."""
    logger.info("Testing model imports...")
    
    try:
        from models.codet5 import CodeT5TestGenerator
        from models.trainer import CodeT5Trainer
        logger.info("✅ Successfully imported model classes")
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_model_initialization():
    """Test that the model can be initialized with the new configuration."""
    logger.info("Testing model initialization...")
    
    try:
        from models.codet5 import CodeT5TestGenerator
        
        # Test with smaller model for faster testing
        model = CodeT5TestGenerator(
            model_name="Salesforce/codet5-base",
            max_input_length=256,
            max_output_length=512
        )
        
        logger.info("✅ Successfully initialized CodeT5 model")
        return True
        
    except Exception as e:
        logger.error(f"❌ Model initialization error: {e}")
        return False

def test_trainer_initialization():
    """Test that the trainer can be initialized with the improved data."""
    logger.info("Testing trainer initialization...")
    
    try:
        from models.codet5 import CodeT5TestGenerator
        from models.trainer import CodeT5Trainer
        
        # Initialize model
        model = CodeT5TestGenerator(
            model_name="Salesforce/codet5-base",
            max_input_length=256,
            max_output_length=512
        )
        
        # Initialize trainer with correct path
        trainer = CodeT5Trainer(
            model=model.model,
            tokenizer=model.tokenizer,
            train_data_path="improved_training_data.jsonl",  # Fixed path
            output_dir="test_output",
            max_input_length=256,
            max_output_length=512,
            batch_size=2,  # Small batch for testing
            learning_rate=3e-5,
            num_epochs=1,  # Just 1 epoch for testing
            warmup_steps=10,
            weight_decay=0.01,
            gradient_accumulation_steps=2,
            save_steps=10,
            eval_steps=10,
            logging_steps=5,
            early_stopping_patience=2
        )
        
        logger.info(f"✅ Successfully initialized trainer with {len(trainer.dataset)} samples")
        return True
        
    except Exception as e:
        logger.error(f"❌ Trainer initialization error: {e}")
        return False

def test_data_processing():
    """Test that the data can be processed by the dataset class."""
    logger.info("Testing data processing...")
    
    try:
        from models.trainer import SwaggerDataset
        from models.codet5 import CodeT5TestGenerator
        
        # Initialize model for tokenizer
        model = CodeT5TestGenerator(
            model_name="Salesforce/codet5-base",
            max_input_length=256,
            max_output_length=512
        )
        
        # Create dataset with correct path
        dataset = SwaggerDataset(
            data_path="improved_training_data.jsonl",  # Fixed path
            tokenizer=model.tokenizer,
            max_input_length=256,
            max_output_length=512
        )
        
        # Test getting a sample
        sample = dataset[0]
        logger.info(f"✅ Successfully processed sample with keys: {list(sample.keys())}")
        
        # Check sample structure
        required_keys = ['input_ids', 'attention_mask', 'labels']
        for key in required_keys:
            if key not in sample:
                logger.error(f"❌ Missing required key: {key}")
                return False
        
        logger.info("✅ Sample structure is correct")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data processing error: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🧪 Starting training setup tests...")
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Model Import", test_model_import),
        ("Model Initialization", test_model_initialization),
        ("Trainer Initialization", test_trainer_initialization),
        ("Data Processing", test_data_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Training setup is ready.")
        logger.info("\n💡 You can now run training with:")
        logger.info("   cd src")
        logger.info("   python train.py")
    else:
        logger.error("❌ Some tests failed. Please fix the issues before training.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 