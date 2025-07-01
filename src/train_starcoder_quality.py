# src/train_starcoder_quality.py
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
    
    # Initialize StarCoder2 model with QUALITY-optimized settings
    model_generator = StarCoderTestGenerator(
        model_name="bigcode/starcoder2-3b",
        max_input_length=512,   # Optimal for API endpoint descriptions
        max_output_length=1024, # Optimal for comprehensive Postman tests
        use_lora=True,          # Enable LoRA for parameter-efficient fine-tuning
        use_4bit=True,          # Enable 4-bit quantization for memory efficiency
        lora_r=32,              # HIGHER LoRA rank for better quality
        lora_alpha=64,          # HIGHER alpha for better quality
        lora_dropout=0.1        # Standard dropout for regularization
    )
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"models/starcoder2_quality_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize trainer with QUALITY-optimized hyperparameters
    trainer = CodeT5Trainer(
        model=model_generator.model,
        tokenizer=model_generator.tokenizer,
        train_data_path="data/processed/augmented_postman_tests_for_training.aggressive.jsonl",
        output_dir=output_dir,
        
        # QUALITY-optimized hyperparameters (slower but better)
        learning_rate=3e-5,        # Conservative learning rate for stability
        batch_size=1,              # Minimal batch size for CPU
        gradient_accumulation_steps=32,  # Larger effective batch size = 32
        num_train_epochs=25,       # More epochs for thorough training
        warmup_steps=100,          # Longer warmup for stability
        
        # Thorough evaluation and saving
        evaluation_strategy="steps",
        eval_steps=5,              # Evaluate every 5 steps (very frequent)
        save_steps=10,             # Save every 10 steps
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        
        # Conservative early stopping for quality
        early_stopping_patience=10,  # More patience to find best model
        early_stopping_threshold=0.001,  # Smaller threshold for precise stopping
        
        # Strong regularization to prevent overfitting
        weight_decay=0.1,          # Strong L2 regularization
        max_grad_norm=0.3,         # Tighter gradient clipping
        
        # High-quality generation parameters
        generation_max_length=1024,
        generation_num_beams=4,    # More beams for better generation
        generation_early_stopping=True,
        generation_no_repeat_ngram_size=3,
        
        # Detailed logging for monitoring quality
        logging_steps=5,           # Log every 5 steps
        logging_dir=f"{output_dir}/logs",
        
        # Keep more checkpoints for analysis
        save_total_limit=5,        # Keep more checkpoints
        
        # CRITICAL: Set is_causal=True for StarCoder2 (causal language model)
        is_causal=True,
    )
    
    logger.info("🎯 Starting HIGH-QUALITY StarCoder2 training...")
    logger.info(f"Dataset: 146+ samples (expanding)")
    logger.info(f"Learning rate: 3e-5 (conservative for stability)")
    logger.info(f"LoRA rank: 32, alpha: 64 (higher for quality)")
    logger.info(f"4-bit quantization: enabled")
    logger.info(f"Early stopping patience: 10 evaluations")
    logger.info(f"Evaluation every: 5 steps")
    logger.info(f"Quality Optimizations:")
    logger.info(f"  - Conservative learning rate for stability")
    logger.info(f"  - Higher LoRA parameters (32/64) for better capacity")
    logger.info(f"  - Larger effective batch size (32)")
    logger.info(f"  - More epochs (25) for thorough training")
    logger.info(f"  - Frequent evaluation (every 5 steps)")
    logger.info(f"  - Conservative early stopping (patience=10)")
    logger.info(f"  - Strong regularization (weight_decay=0.1)")
    logger.info(f"  - Tighter gradient clipping (max_grad_norm=0.3)")
    logger.info(f"  - More generation beams (4) for better output")
    logger.info(f"  - Causal language model mode enabled")
    
    # Start training
    trainer.train()
    
    # Save the final model
    trainer.save_model()
    logger.info(f"✅ High-quality training completed. Model saved to: {output_dir}")

if __name__ == "__main__":
    main() 