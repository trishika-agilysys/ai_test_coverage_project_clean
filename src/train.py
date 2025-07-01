# src/train.py
from models.codet5 import CodeT5TestGenerator
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
    
    # Initialize model with LoRA fine-tuning and 4-bit quantization
    model_generator = CodeT5TestGenerator(
        model_name="Salesforce/codet5-base",
        max_input_length=512,   # Reduced from 768 - inputs are shorter
        max_output_length=1024, # Reduced from 2048 - outputs are shorter
        use_lora=True,          # Enable LoRA for parameter-efficient fine-tuning
        use_4bit=True,          # Enable 4-bit quantization for memory efficiency
        lora_r=16,              # LoRA rank - higher for more capacity
        lora_alpha=32,          # LoRA alpha - scaling factor
        lora_dropout=0.1        # LoRA dropout for regularization
    )
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"models/codet5_postman_tests_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize trainer with optimized hyperparameters for small dataset
    trainer = CodeT5Trainer(
        model=model_generator.model,
        tokenizer=model_generator.tokenizer,
        train_data_path="src/data/processed/augmented_postman_tests_for_training.aggressive.jsonl",  # Use aggressive data with 148 samples
        output_dir=output_dir,
        
        # Optimized hyperparameters for small dataset (148 samples) with LoRA
        learning_rate=3e-4,        # Slightly higher for faster convergence with LoRA
        batch_size=4,              # Smaller batch size for better gradient updates on small dataset
        gradient_accumulation_steps=4,  # Effective batch size = 16
        num_train_epochs=25,       # More epochs for thorough LoRA fine-tuning
        warmup_steps=30,           # Shorter warmup for LoRA (10% of total steps)
        
        # Overfitting prevention
        evaluation_strategy="steps",
        eval_steps=10,             # More frequent evaluation for small dataset
        save_steps=25,             # Save more frequently
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        
        # Early stopping to prevent overfitting
        early_stopping_patience=7,  # More patience for LoRA training
        early_stopping_threshold=0.001,  # Very small threshold for precise stopping
        
        # Additional overfitting prevention
        weight_decay=0.05,         # Increased L2 regularization for small dataset
        max_grad_norm=0.5,         # Tighter gradient clipping for LoRA
        
        # Generation parameters for better outputs
        generation_max_length=1024,
        generation_num_beams=4,
        generation_early_stopping=True,
        generation_no_repeat_ngram_size=3,
        
        # Logging for monitoring
        logging_steps=2,           # More frequent logging for better monitoring
        logging_dir=f"{output_dir}/logs",
        
        # Save total steps for monitoring
        save_total_limit=5,        # Keep more checkpoints for analysis
    )
    
    logger.info("Starting training with LoRA fine-tuning and 4-bit quantization...")
    logger.info(f"Dataset: 148 samples")
    logger.info(f"Learning rate: 3e-4 (optimized for LoRA)")
    logger.info(f"LoRA rank: 16, alpha: 32")
    logger.info(f"4-bit quantization: enabled")
    logger.info(f"Early stopping patience: 7 evaluations")
    logger.info(f"Evaluation every: 10 steps")
    
    # Start training
    trainer.train()
    
    # Save the final model
    trainer.save_model()
    logger.info(f"Training completed. Model saved to: {output_dir}")

if __name__ == "__main__":
    main()