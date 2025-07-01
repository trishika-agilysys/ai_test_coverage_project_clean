# src/train_starcoder_optimized.py
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
    
    # Initialize StarCoder2 model with optimized settings for CPU training
    model_generator = StarCoderTestGenerator(
        model_name="bigcode/starcoder2-3b",
        max_input_length=512,   # Keep original for compatibility
        max_output_length=1024, # Keep original for compatibility
        use_lora=True,          # Enable LoRA for parameter-efficient fine-tuning
        use_4bit=True,          # Enable 4-bit quantization for memory efficiency
        lora_r=8,               # Reduced LoRA rank for faster training
        lora_alpha=16,          # Reduced alpha for faster training
        lora_dropout=0.05       # Reduced dropout for faster convergence
    )
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"models/starcoder2_optimized_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize trainer with CPU-optimized hyperparameters
    trainer = CodeT5Trainer(
        model=model_generator.model,
        tokenizer=model_generator.tokenizer,
        train_data_path="data/processed/augmented_postman_tests_for_training.aggressive.jsonl",
        output_dir=output_dir,
        
        # CPU-optimized hyperparameters for faster training
        learning_rate=1e-4,        # Higher learning rate for faster convergence
        batch_size=1,              # Minimal batch size for CPU
        gradient_accumulation_steps=16,  # Effective batch size = 16
        num_train_epochs=15,       # Reduced epochs for faster training
        warmup_steps=20,           # Shorter warmup for faster start
        
        # Faster evaluation and saving
        evaluation_strategy="steps",
        eval_steps=10,             # Evaluate every 10 steps (more frequent)
        save_steps=20,             # Save every 20 steps
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        
        # Aggressive early stopping for faster training
        early_stopping_patience=4,  # Less patience for faster stopping
        early_stopping_threshold=0.01,  # Larger threshold for faster stopping
        
        # Reduced regularization for faster convergence
        weight_decay=0.05,         # Reduced L2 regularization
        max_grad_norm=1.0,         # Relaxed gradient clipping
        
        # Simplified generation parameters
        generation_max_length=1024,
        generation_num_beams=2,    # Reduced for faster generation
        generation_early_stopping=True,
        generation_no_repeat_ngram_size=2,
        
        # Reduced logging for less overhead
        logging_steps=10,          # Log every 10 steps
        logging_dir=f"{output_dir}/logs",
        
        # Fewer checkpoints to save disk space
        save_total_limit=3,        # Keep fewer checkpoints
        
        # CRITICAL: Set is_causal=True for StarCoder2 (causal language model)
        is_causal=True,
    )
    
    logger.info("🚀 Starting OPTIMIZED StarCoder2 training for CPU...")
    logger.info(f"Dataset: 146 samples (expanding)")
    logger.info(f"Learning rate: 1e-4 (higher for faster convergence)")
    logger.info(f"LoRA rank: 8, alpha: 16 (reduced for speed)")
    logger.info(f"4-bit quantization: enabled")
    logger.info(f"Early stopping patience: 4 evaluations")
    logger.info(f"Evaluation every: 10 steps")
    logger.info(f"CPU Optimizations:")
    logger.info(f"  - Higher learning rate for faster convergence")
    logger.info(f"  - More frequent evaluation")
    logger.info(f"  - Aggressive early stopping")
    logger.info(f"  - Reduced LoRA parameters")
    logger.info(f"  - Minimal batch size with gradient accumulation")
    logger.info(f"  - Causal language model mode enabled")
    
    # Start training
    trainer.train()
    
    # Save the final model
    trainer.save_model()
    logger.info(f"✅ Training completed. Optimized model saved to: {output_dir}")

if __name__ == "__main__":
    main() 