#!/usr/bin/env python3
"""
Monitor StarCoder2 Training Progress

This script monitors the StarCoder2 training progress and alerts when training completes.
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_latest_training_dir():
    """Find the latest StarCoder2 training directory."""
    models_dir = Path("models")
    if not models_dir.exists():
        return None
    
    # Look for StarCoder2 training directories
    training_dirs = [d for d in models_dir.iterdir() 
                    if d.is_dir() and d.name.startswith("starcoder2_swagger_to_postman_")]
    
    if not training_dirs:
        return None
    
    # Return the most recent one
    return max(training_dirs, key=lambda x: x.stat().st_ctime)

def check_training_progress():
    """Check the current training progress."""
    training_dir = find_latest_training_dir()
    
    if not training_dir:
        logger.info("No StarCoder2 training directory found yet.")
        return False
    
    logger.info(f"Monitoring training directory: {training_dir.name}")
    
    # Check for checkpoints
    checkpoint_dirs = [d for d in training_dir.iterdir() 
                      if d.is_dir() and d.name.startswith("checkpoint-")]
    
    if checkpoint_dirs:
        latest_checkpoint = max(checkpoint_dirs, key=lambda x: x.stat().st_ctime)
        logger.info(f"Latest checkpoint: {latest_checkpoint.name}")
        
        # Check for training state
        state_file = latest_checkpoint / "training_state.pt"
        if state_file.exists():
            try:
                import torch
                state = torch.load(state_file, map_location='cpu')
                logger.info(f"Current epoch: {state.get('epoch', 'N/A')}")
                logger.info(f"Current step: {state.get('step', 'N/A')}")
                logger.info(f"Current loss: {state.get('loss', 'N/A'):.4f}")
                logger.info(f"Best loss: {state.get('best_loss', 'N/A'):.4f}")
                logger.info(f"Early stopping counter: {state.get('early_stopping_counter', 'N/A')}")
            except Exception as e:
                logger.warning(f"Could not load training state: {e}")
    
    # Check for best model
    best_model_dir = training_dir / "best_model"
    if best_model_dir.exists():
        logger.info("✅ Best model checkpoint exists")
    
    # Check for final model
    final_model_dir = training_dir / "final_model"
    if final_model_dir.exists():
        logger.info("🎉 Training completed! Final model saved.")
        return True
    
    # Check disk usage
    try:
        total_size = sum(f.stat().st_size for f in training_dir.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        logger.info(f"Training directory size: {size_mb:.1f} MB")
    except Exception as e:
        logger.warning(f"Could not check disk usage: {e}")
    
    return False

def monitor_training():
    """Monitor training continuously."""
    logger.info("🔍 Starting StarCoder2 training monitoring...")
    logger.info("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            print("\n" + "="*60)
            print(f"StarCoder2 Training Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            completed = check_training_progress()
            
            if completed:
                logger.info("🎉 TRAINING COMPLETED SUCCESSFULLY!")
                logger.info("You can now use the trained model for Swagger to Postman conversion.")
                break
            
            # Check if training process is still running
            import subprocess
            try:
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                      capture_output=True, text=True)
                if 'python.exe' in result.stdout:
                    logger.info("✅ Training process is still running")
                else:
                    logger.warning("⚠️  No Python training process found")
            except Exception as e:
                logger.warning(f"Could not check process status: {e}")
            
            logger.info("Waiting 30 seconds before next check...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")

def main():
    monitor_training()

if __name__ == "__main__":
    main() 