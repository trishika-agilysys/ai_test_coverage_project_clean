from transformers import T5ForConditionalGeneration, RobertaTokenizer

# Path to your fine-tuned model directory
model_dir = "src/data/models"

# Load the tokenizer and model
print("Loading model and tokenizer from", model_dir)
tokenizer = RobertaTokenizer.from_pretrained(model_dir)
model = T5ForConditionalGeneration.from_pretrained(model_dir)

# Use a prompt from the training data
prompt = "POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [EMV, No Tip, No Sig] Validate Successful Sale On Device Response"

# Tokenize input
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# Generate output
outputs = model.generate(
    input_ids,
    max_length=512,
    num_return_sequences=1,
    do_sample=False,
    early_stopping=True
)

# Decode and print the result
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\nGenerated JavaScript Postman test:\n")
print(result) 