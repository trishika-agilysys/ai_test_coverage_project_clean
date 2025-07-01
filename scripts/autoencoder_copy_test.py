import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

DATA_PATH = 'augmented_postman_tests_for_training.cleaned.jsonl'
CHECKPOINT_DIR = 'src/data/models/checkpoints/autoencoder_copy_test/'
MODEL_NAME = 't5-base'
MAX_INPUT_LENGTH = 512
MAX_OUTPUT_LENGTH = 512
BATCH_SIZE = 2
NUM_EPOCHS = 3

os.makedirs(CHECKPOINT_DIR, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Load 3 examples
examples = []
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 3:
            break
        obj = json.loads(line)
        examples.append({'input': obj['output'], 'output': obj['output']})

print('--- Tokenized Lengths of Original Scripts ---')
for i, ex in enumerate(examples):
    input_tokens = tokenizer(ex['input'], truncation=False)['input_ids']
    output_tokens = tokenizer(ex['output'], truncation=False)['input_ids']
    print(f'Sample {i+1}: input tokens = {len(input_tokens)}, output tokens = {len(output_tokens)}')

# Now run the copy test with a very short script
short_script = 'console.log("hello world");'
short_examples = [{'input': short_script, 'output': short_script} for _ in range(3)]

class CopyDataset(Dataset):
    def __init__(self, examples, tokenizer, max_input_length, max_output_length):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_output_length = max_output_length
    def __len__(self):
        return len(self.examples)
    def __getitem__(self, idx):
        item = self.examples[idx]
        input_enc = self.tokenizer(
            item['input'],
            max_length=self.max_input_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        output_enc = self.tokenizer(
            item['output'],
            max_length=self.max_output_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': input_enc['input_ids'].squeeze(),
            'attention_mask': input_enc['attention_mask'].squeeze(),
            'labels': output_enc['input_ids'].squeeze()
        }

dataset = CopyDataset(short_examples, tokenizer, MAX_INPUT_LENGTH, MAX_OUTPUT_LENGTH)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
optimizer = AdamW(model.parameters(), lr=5e-5)

for epoch in range(NUM_EPOCHS):
    model.train()
    total_loss = 0
    for batch in tqdm(dataloader, desc=f'Epoch {epoch+1}/{NUM_EPOCHS}'):
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    avg_loss = total_loss / len(dataloader)
    print(f'Epoch {epoch+1} completed. Average loss: {avg_loss:.4f}')
    # Save checkpoint
    model.save_pretrained(os.path.join(CHECKPOINT_DIR, f'epoch-{epoch+1}'))
    tokenizer.save_pretrained(os.path.join(CHECKPOINT_DIR, f'epoch-{epoch+1}'))
    # Sample generations
    model.eval()
    print(f'\n=== Sample Generations After Epoch {epoch+1} ===')
    for i, ex in enumerate(short_examples):
        inputs = tokenizer(
            ex['input'],
            max_length=MAX_INPUT_LENGTH,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            generated_ids = model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=MAX_OUTPUT_LENGTH,
                num_beams=4,
                early_stopping=True
            )
        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        print(f'Sample {i+1} input: {ex["input"]}')
        print(f'Sample {i+1} generated output: {generated_text}')
        print(f'Sample {i+1} expected output: {ex["output"]}\n') 