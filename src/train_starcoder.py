# src/train_starcoder.py
from models.starcoder import StarCoderTestGenerator
from models.trainer import CodeT5Trainer
import logging
import os
import torch
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Ensure the data directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Initialize StarCoder2 model with LoRA fine-tuning and 4-bit quantization
    model_generator = StarCoderTestGenerator(
        model_name="bigcode/starcoder2-3b",
        max_input_length=512,   # Optimal for API endpoint descriptions
        max_output_length=1024, # Optimal for Postman test generation
        use_lora=True,          # Enable LoRA for parameter-efficient fine-tuning
        use_4bit=True,          # Enable 4-bit quantization for memory efficiency
        lora_r=16,              # LoRA rank - higher for more capacity
        lora_alpha=32,          # LoRA alpha - scaling factor
        lora_dropout=0.1        # LoRA dropout for regularization
    )
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"models/starcoder2_postman_tests_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize trainer with optimized hyperparameters for StarCoder2
    trainer = CodeT5Trainer(
        model=model_generator.model,
        tokenizer=model_generator.tokenizer,
        train_data_path="data/processed/augmented_postman_tests_for_training.aggressive.jsonl",  # Use aggressive data with 148 samples
        output_dir=output_dir,
        
        # Optimized hyperparameters for StarCoder2 with small dataset (148 samples)
        learning_rate=5e-5,        # Lower learning rate for StarCoder2 (more stable)
        batch_size=2,              # Smaller batch size for StarCoder2 (larger model)
        gradient_accumulation_steps=8,  # Effective batch size = 16
        num_train_epochs=30,       # More epochs for thorough StarCoder2 fine-tuning
        warmup_steps=50,           # Longer warmup for StarCoder2
        
        # Overfitting prevention
        evaluation_strategy="steps",
        eval_steps=20,             # Evaluate every 20 steps
        save_steps=40,             # Save every 40 steps
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        
        # Early stopping to prevent overfitting
        early_stopping_patience=8,  # More patience for StarCoder2 training
        early_stopping_threshold=0.001,  # Very small threshold for precise stopping
        
        # Additional overfitting prevention
        weight_decay=0.1,          # Stronger L2 regularization for StarCoder2
        max_grad_norm=0.3,         # Tighter gradient clipping for StarCoder2
        
        # Generation parameters for better outputs
        generation_max_length=1024,
        generation_num_beams=4,
        generation_early_stopping=True,
        generation_no_repeat_ngram_size=3,
        
        # Logging for monitoring
        logging_steps=5,           # Log every 5 steps
        logging_dir=f"{output_dir}/logs",
        
        # Save total steps for monitoring
        save_total_limit=5,        # Keep more checkpoints for analysis
    )
    
    logger.info("Starting StarCoder2 training with LoRA fine-tuning and 4-bit quantization...")
    logger.info(f"Dataset: 148 samples")
    logger.info(f"Learning rate: 5e-5 (optimized for StarCoder2)")
    logger.info(f"LoRA rank: 16, alpha: 32")
    logger.info(f"4-bit quantization: enabled")
    logger.info(f"Early stopping patience: 8 evaluations")
    logger.info(f"Evaluation every: 20 steps")
    logger.info(f"StarCoder2 advantages:")
    logger.info(f"  - Better code generation for JavaScript/TypeScript")
    logger.info(f"  - More natural Postman test patterns")
    logger.info(f"  - Optimized for programming tasks")
    
    # Start training
    trainer.train()
    
    # Save the final model
    trainer.save_model()
    logger.info(f"Training completed. StarCoder2 model saved to: {output_dir}")

if __name__ == "__main__":
    main() 