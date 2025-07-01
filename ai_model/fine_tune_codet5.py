import json
from transformers import T5ForConditionalGeneration, RobertaTokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from torch.utils.data import Dataset
import torch
import argparse

TRAIN_FILE = "src/data/test_case_training.jsonl"
MODEL_NAME = "Salesforce/codet5-base"
OUTPUT_DIR = "src/data/models/checkpoints/latest"

def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

class TestCaseDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        input_enc = self.tokenizer(
            item["input"], truncation=True, padding=False, max_length=self.max_length, return_tensors="np"
        )
        output_enc = self.tokenizer(
            item["output"], truncation=True, padding=False, max_length=self.max_length, return_tensors="np"
        )
        return {
            "input_ids": input_enc["input_ids"].squeeze(),
            "attention_mask": input_enc["attention_mask"].squeeze(),
            "labels": output_enc["input_ids"].squeeze()
        }

def main(train_file, output_dir, model_name, num_train_epochs):
    # Optimize for CPU
    torch.set_num_threads(1)
    
    print(f"CUDA available: {torch.cuda.is_available()}")
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    print(f"Number of available GPUs: {device_count}")
    
    data = load_jsonl(train_file)

    tokenizer = RobertaTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Enable gradient checkpointing
    model.gradient_checkpointing_enable()

    dataset = TestCaseDataset(data, tokenizer)

    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=16,  # Increased from 8
        gradient_accumulation_steps=4,    # Added gradient accumulation
        num_train_epochs=num_train_epochs,
        save_steps=50,                    # Reduced checkpoint frequency
        save_total_limit=1,              # Keep only the latest checkpoint
        logging_steps=10,
        learning_rate=1e-4,              # Slightly increased learning rate
        warmup_ratio=0.1,               # Added warmup
        fp16=False,                      # Mixed precision training
        remove_unused_columns=False,
        dataloader_num_workers=0,        # Use 0 workers for CPU training on Windows
        gradient_checkpointing=True,     # Enable gradient checkpointing
        optim="adamw_torch",            # Use PyTorch's AdamW implementation
        bf16=False,                     # Disable bfloat16 since we're using fp16
        weight_decay=0.01,              # Added weight decay for regularization
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Fine-tuned model saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune CodeT5 model for test case generation.")
    parser.add_argument("--train_file", type=str, default="src/data/test_case_training.jsonl", help="Path to the training data file (JSONL format).")
    parser.add_argument("--output_dir", type=str, default="src/data/models/checkpoints/latest_english_generator", help="Directory to save the fine-tuned model.")
    parser.add_argument("--model_name", type=str, default="Salesforce/codet5-base", help="Name of the base model to fine-tune.")
    parser.add_argument("--num_train_epochs", type=int, default=20, help="Number of training epochs.")
    args = parser.parse_args()
    main(args.train_file, args.output_dir, args.model_name, args.num_train_epochs) 