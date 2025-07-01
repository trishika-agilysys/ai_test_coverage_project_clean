#!/usr/bin/env python3
"""
Training Monitor for CodeT5 Postman Test Generation

This script monitors the training progress and helps detect overfitting.
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingMonitor:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.log_file = self.output_dir / "training.log"
        self.checkpoints = []
        self.losses = []
        
    def find_latest_checkpoint(self):
        """Find the latest checkpoint directory."""
        if not self.output_dir.exists():
            return None
            
        checkpoint_dirs = [d for d in self.output_dir.iterdir() 
                          if d.is_dir() and d.name.startswith("checkpoint-")]
        
        if not checkpoint_dirs:
            return None
            
        # Sort by creation time
        latest = max(checkpoint_dirs, key=lambda x: x.stat().st_ctime)
        return latest
    
    def get_training_state(self, checkpoint_dir):
        """Get training state from checkpoint."""
        state_file = checkpoint_dir / "training_state.pt"
        if not state_file.exists():
            return None
            
        try:
            import torch
            state = torch.load(state_file, map_location='cpu')
            return state
        except Exception as e:
            logger.warning(f"Failed to load training state: {e}")
            return None
    
    def analyze_training_progress(self):
        """Analyze training progress and detect overfitting signs."""
        latest_checkpoint = self.find_latest_checkpoint()
        
        if not latest_checkpoint:
            logger.info("No checkpoints found yet. Training may not have started.")
            return
        
        logger.info(f"Latest checkpoint: {latest_checkpoint.name}")
        
        # Get training state
        state = self.get_training_state(latest_checkpoint)
        if state:
            logger.info(f"Current epoch: {state.get('epoch', 'N/A')}")
            logger.info(f"Current step: {state.get('step', 'N/A')}")
            logger.info(f"Current loss: {state.get('loss', 'N/A'):.4f}")
            logger.info(f"Best loss: {state.get('best_loss', 'N/A'):.4f}")
            logger.info(f"Early stopping counter: {state.get('early_stopping_counter', 'N/A')}")
        
        # Check for overfitting signs
        self.check_overfitting_signs()
        
        # Check disk usage
        self.check_disk_usage()
    
    def check_overfitting_signs(self):
        """Check for common overfitting signs."""
        logger.info("\n=== Overfitting Analysis ===")
        
        # Check if best model exists
        best_model_dir = self.output_dir / "best_model"
        if best_model_dir.exists():
            logger.info("✅ Best model checkpoint exists")
        else:
            logger.warning("⚠️  No best model checkpoint found yet")
        
        # Check checkpoint count
        checkpoint_dirs = [d for d in self.output_dir.iterdir() 
                          if d.is_dir() and d.name.startswith("checkpoint-")]
        logger.info(f"📁 Total checkpoints: {len(checkpoint_dirs)}")
        
        if len(checkpoint_dirs) > 10:
            logger.warning("⚠️  Many checkpoints - consider reducing save frequency")
        
        # Check for early stopping
        latest_checkpoint = self.find_latest_checkpoint()
        if latest_checkpoint:
            state = self.get_training_state(latest_checkpoint)
            if state and state.get('early_stopping_counter', 0) > 0:
                logger.info(f"🛑 Early stopping counter: {state['early_stopping_counter']}/3")
                if state['early_stopping_counter'] >= 3:
                    logger.warning("⚠️  Early stopping may trigger soon!")
    
    def check_disk_usage(self):
        """Check disk usage of output directory."""
        try:
            total_size = sum(f.stat().st_size for f in self.output_dir.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            logger.info(f"💾 Output directory size: {size_mb:.1f} MB")
            
            if size_mb > 1000:  # 1GB
                logger.warning("⚠️  Large output directory - consider cleanup")
        except Exception as e:
            logger.warning(f"Failed to check disk usage: {e}")
    
    def monitor_continuously(self, interval=30):
        """Monitor training continuously."""
        logger.info(f"Starting continuous monitoring (checking every {interval} seconds)...")
        logger.info("Press Ctrl+C to stop monitoring")
        
        try:
            while True:
                print("\n" + "="*60)
                print(f"Training Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*60)
                
                self.analyze_training_progress()
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Monitor CodeT5 training progress")
    parser.add_argument("--output-dir", type=str, required=True, 
                       help="Training output directory")
    parser.add_argument("--continuous", action="store_true",
                       help="Monitor continuously")
    parser.add_argument("--interval", type=int, default=30,
                       help="Monitoring interval in seconds (default: 30)")
    
    args = parser.parse_args()
    
    monitor = TrainingMonitor(args.output_dir)
    
    if args.continuous:
        monitor.monitor_continuously(args.interval)
    else:
        monitor.analyze_training_progress()

if __name__ == "__main__":
    main() 