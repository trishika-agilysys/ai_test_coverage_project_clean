import json
from transformers import AutoTokenizer

INPUT_PATH = 'augmented_postman_tests_for_training.jsonl'
OUTPUT_PATH = 'augmented_postman_tests_for_training.split_cleaned.jsonl'
MODEL_NAME = 'Salesforce/codet5-base'
MAX_TOKENS = 512

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

seen = set()
new_examples = []
summary = []

def chunk_text(text, max_tokens):
    tokens = tokenizer(text, truncation=False)['input_ids']
    n_chunks = (len(tokens) + max_tokens - 1) // max_tokens
    chunks = []
    for i in range(n_chunks):
        chunk_tokens = tokens[i*max_tokens:(i+1)*max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
    return chunks

with open(INPUT_PATH, 'r', encoding='utf-8') as infile:
    for idx, line in enumerate(infile):
        obj = json.loads(line)
        input_text = obj['input'].strip()
        output_text = obj['output'].strip()
        input_chunks = chunk_text(input_text, MAX_TOKENS)
        output_chunks = chunk_text(output_text, MAX_TOKENS)
        n_chunks = max(len(input_chunks), len(output_chunks))
        for i in range(n_chunks):
            # Use chunked input if input is long, else repeat full input for each output chunk
            chunk_input = input_chunks[i] if len(input_chunks) > 1 else input_text
            chunk_output = output_chunks[i] if i < len(output_chunks) else ''
            # Optionally, append chunk index to input for clarity
            if n_chunks > 1:
                chunk_input = f"{chunk_input} [chunk {i+1}/{n_chunks}]"
            pair = (chunk_input, chunk_output)
            if pair not in seen:
                seen.add(pair)
                new_examples.append({'input': chunk_input, 'output': chunk_output})
        summary.append(f'Original example {idx+1}: {n_chunks} chunk(s)')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
    for ex in new_examples:
        outfile.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f'Split and cleaned {len(summary)} original examples into {len(new_examples)} chunked examples.')
for s in summary:
    print(s) 