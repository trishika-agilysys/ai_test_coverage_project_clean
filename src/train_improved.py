# src/train_improved.py
from models.codet5 import CodeT5TestGenerator
from models.trainer import CodeT5Trainer
import logging
import os
import torch
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_training_data(data_path):
    """Analyze the training data to understand its characteristics."""
    logger.info(f"Analyzing training data from: {data_path}")
    
    total_samples = 0
    input_lengths = []
    output_lengths = []
    validation_errors = []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    
                    # Validate required fields
                    if 'input' not in obj or 'output' not in obj:
                        validation_errors.append(f"Line {line_num}: Missing required fields")
                        continue
                    
                    input_text = obj['input'].strip()
                    output_text = obj['output'].strip()
                    
                    # Check for empty content
                    if not input_text or not output_text:
                        validation_errors.append(f"Line {line_num}: Empty input or output")
                        continue
                    
                    # Check for extremely short outputs (likely incomplete)
                    if len(output_text) < 30:
                        validation_errors.append(f"Line {line_num}: Output too short ({len(output_text)} chars)")
                        continue
                    
                    # Check for minimum test cases (at least 1 pm.test statement)
                    if output_text.count('pm.test') < 1:
                        validation_errors.append(f"Line {line_num}: Output doesn't contain any test cases")
                        continue
                    
                    total_samples += 1
                    input_lengths.append(len(input_text))
                    output_lengths.append(len(output_text))
                    
                except Exception as e:
                    validation_errors.append(f"Line {line_num}: JSON parsing error - {e}")
    
    # Report validation errors
    if validation_errors:
        logger.warning(f"Found {len(validation_errors)} validation errors:")
        for error in validation_errors[:10]:  # Show first 10 errors
            logger.warning(f"  {error}")
        if len(validation_errors) > 10:
            logger.warning(f"  ... and {len(validation_errors) - 10} more errors")
    
    if input_lengths and output_lengths:
        avg_input_length = sum(input_lengths) / len(input_lengths)
        avg_output_length = sum(output_lengths) / len(output_lengths)
        max_input_length = max(input_lengths)
        max_output_length = max(output_lengths)
        
        logger.info(f"Total valid samples: {total_samples}")
        logger.info(f"Average input length: {avg_input_length:.1f} characters")
        logger.info(f"Average output length: {avg_output_length:.1f} characters")
        logger.info(f"Max input length: {max_input_length} characters")
        logger.info(f"Max output length: {max_output_length} characters")
        
        return {
            'total_samples': total_samples,
            'avg_input_length': avg_input_length,
            'avg_output_length': avg_output_length,
            'max_input_length': max_input_length,
            'max_output_length': max_output_length,
            'validation_errors': validation_errors
        }
    
    return None

def main():
    # Ensure the data directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Analyze training data first
    data_path = "../augmented_postman_tests_for_training.merged_cleaned.jsonl"
    data_stats = analyze_training_data(data_path)
    
    if not data_stats:
        logger.error("Failed to analyze training data. Exiting.")
        return
    
    # Check if we have enough valid training data
    if data_stats['total_samples'] < 10:
        logger.error(f"Not enough valid training samples: {data_stats['total_samples']}. Need at least 10.")
        return
    
    # Warn if there are too many validation errors
    if len(data_stats['validation_errors']) > data_stats['total_samples'] * 0.1:  # More than 10% errors
        logger.warning(f"High number of validation errors: {len(data_stats['validation_errors'])} out of {data_stats['total_samples']} samples")
        logger.warning("Consider cleaning the training data before proceeding.")
        response = input("Continue with training anyway? (y/N): ")
        if response.lower() != 'y':
            logger.info("Training cancelled by user.")
            return
    
    # Calculate optimal hyperparameters based on data analysis
    # Use 95th percentile for max lengths to avoid truncating too much
    max_input_length = min(512, int(data_stats['avg_input_length'] * 2.5))
    max_output_length = min(2048, int(data_stats['avg_output_length'] * 2.0))
    
    logger.info(f"Calculated max_input_length: {max_input_length}")
    logger.info(f"Calculated max_output_length: {max_output_length}")
    
    # Initialize model with optimized configuration
    model = CodeT5TestGenerator(
        model_name="Salesforce/codet5-base",
        max_input_length=max_input_length,
        max_output_length=max_output_length
    )
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"src/data/models/checkpoints/{timestamp}_optimized_training"
    
    # Optimized training configuration based on analysis
    # Key improvements:
    # 1. Lower learning rate for more stable training
    # 2. Smaller batch size to prevent gradient explosion
    # 3. More epochs with early stopping
    # 4. Better gradient accumulation for effective batch size
    # 5. More frequent evaluation and checkpointing
    trainer = CodeT5Trainer(
        model=model.model,
        tokenizer=model.tokenizer,
        train_data_path=data_path,
        output_dir=output_dir,
        max_input_length=max_input_length,
        max_output_length=max_output_length,
        batch_size=2,  # Reduced from 1 to 2 for better gradient estimates
        learning_rate=3e-5,  # Reduced from 1e-5 for more stable training
        num_epochs=15,  # Reduced from 20 to prevent overfitting
        warmup_steps=100,  # Reduced warmup for faster convergence
        weight_decay=0.01,  # Keep weight decay for regularization
        gradient_accumulation_steps=8,  # Effective batch size = 2 * 8 = 16
        save_steps=50,  # Save checkpoints more frequently
        eval_steps=25,  # Evaluate more frequently to catch issues early
        logging_steps=10,  # More frequent logging
        early_stopping_patience=3  # Reduced patience for faster stopping
    )
    
    # Start training
    logger.info(f"Starting optimized training with {len(trainer.dataset)} samples")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Max input length: {trainer.max_input_length}")
    logger.info(f"Max output length: {trainer.max_output_length}")
    logger.info(f"Effective batch size: {trainer.batch_size * trainer.gradient_accumulation_steps}")
    logger.info(f"Learning rate: {trainer.learning_rate}")
    logger.info(f"Total training steps: {len(trainer.dataloader) * trainer.num_epochs // trainer.gradient_accumulation_steps}")
    
    try:
        trainer.train()
        logger.info("Training completed successfully!")
    except Exception as e:
        logger.error(f"Training failed with error: {e}")
        raise

if __name__ == "__main__":
    main() 