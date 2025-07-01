# src/train_swagger_to_postman.py
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
    
    # Initialize StarCoder2 model specifically for Swagger to Postman conversion
    model_generator = StarCoderTestGenerator(
        model_name="bigcode/starcoder2-3b",
        max_input_length=768,   # Larger for Swagger endpoint descriptions
        max_output_length=1024, # Optimal for Postman test generation
        use_lora=True,          # Enable LoRA for parameter-efficient fine-tuning
        use_4bit=True,          # Enable 4-bit quantization for memory efficiency
        lora_r=16,              # LoRA rank - higher for more capacity
        lora_alpha=32,          # LoRA alpha - scaling factor
        lora_dropout=0.1        # LoRA dropout for regularization
    )
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"models/starcoder2_swagger_to_postman_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize trainer with hyperparameters optimized for Swagger to Postman conversion
    trainer = CodeT5Trainer(
        model=model_generator.model,
        tokenizer=model_generator.tokenizer,
        train_data_path="data/processed/augmented_postman_tests_for_training.aggressive.jsonl",  # Use aggressive data with 148 samples
        output_dir=output_dir,
        is_causal=True,  # StarCoder2 is a causal language model
        
        # Hyperparameters optimized for Swagger to Postman conversion
        learning_rate=3e-5,        # Conservative learning rate for stable training
        batch_size=2,              # Small batch size for StarCoder2
        gradient_accumulation_steps=8,  # Effective batch size = 16
        num_train_epochs=25,       # More epochs for thorough learning
        warmup_steps=40,           # Gradual warmup
        
        # Overfitting prevention for small dataset
        evaluation_strategy="steps",
        eval_steps=15,             # Evaluate every 15 steps
        save_steps=30,             # Save every 30 steps
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        
        # Early stopping to prevent overfitting
        early_stopping_patience=6,  # Patient early stopping
        early_stopping_threshold=0.001,  # Small improvement threshold
        
        # Strong regularization for small dataset
        weight_decay=0.1,          # Strong L2 regularization
        max_grad_norm=0.3,         # Tight gradient clipping
        
        # Generation parameters optimized for Postman tests
        generation_max_length=1024,
        generation_num_beams=4,
        generation_early_stopping=True,
        generation_no_repeat_ngram_size=3,
        
        # Logging for monitoring
        logging_steps=3,           # Frequent logging
        logging_dir=f"{output_dir}/logs",
        
        # Save total steps for monitoring
        save_total_limit=5,        # Keep more checkpoints
    )
    
    logger.info("🚀 Starting StarCoder2 training for Swagger to Postman conversion...")
    logger.info(f"Dataset: 148 samples (aggressive cleaning)")
    logger.info(f"Learning rate: 3e-5 (conservative for stability)")
    logger.info(f"LoRA rank: 16, alpha: 32")
    logger.info(f"4-bit quantization: enabled")
    logger.info(f"Early stopping patience: 6 evaluations")
    logger.info(f"Evaluation every: 15 steps")
    
    logger.info(f"\n🎯 Training Objectives:")
    logger.info(f"  - Convert Swagger endpoint descriptions to Postman JavaScript tests")
    logger.info(f"  - Generate comprehensive pm.test() blocks")
    logger.info(f"  - Handle different HTTP methods (GET, POST, PUT, DELETE)")
    logger.info(f"  - Include proper variable interpolation ({{{{variable}}}})")
    logger.info(f"  - Add response validation and error handling")
    
    logger.info(f"\n📊 Model Efficiency:")
    logger.info(f"  - Only ~1-2% of parameters will be trained (LoRA)")
    logger.info(f"  - 75% memory reduction (4-bit quantization)")
    logger.info(f"  - Fast training and inference")
    
    # Start training
    trainer.train()
    
    # Save the final model
    trainer.save_model()
    logger.info(f"✅ Training completed! StarCoder2 model saved to: {output_dir}")
    
    # Save training summary
    training_summary = {
        'model_name': 'bigcode/starcoder2-3b',
        'task': 'swagger_to_postman_conversion',
        'dataset_size': 148,
        'training_config': {
            'learning_rate': 3e-5,
            'batch_size': 2,
            'effective_batch_size': 16,
            'epochs': 25,
            'lora_r': 16,
            'lora_alpha': 32,
            'early_stopping_patience': 6
        },
        'output_directory': output_dir,
        'timestamp': timestamp
    }
    
    import json
    with open(f"{output_dir}/training_summary.json", 'w') as f:
        json.dump(training_summary, f, indent=2)
    
    logger.info(f"📋 Training summary saved to: {output_dir}/training_summary.json")

if __name__ == "__main__":
    main() 