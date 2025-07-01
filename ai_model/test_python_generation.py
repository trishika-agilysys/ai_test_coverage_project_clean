import torch
from transformers import T5ForConditionalGeneration, RobertaTokenizer
import json

def test_python_generation():
    # Load the fine-tuned model
    model_path = "src/data/models/checkpoints/latest_english_generator"
    
    print("Loading fine-tuned model...")
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    
    # Test prompts for Python generation
    test_prompts = [
        "Please write a Python test case for the following API endpoint.\nAPI Endpoint: GET /health\nScenario: Verify health check functionality\nParameters: None\n\nTest Case:",
        "Generate a pytest function for the following API endpoint.\nAPI Endpoint: POST /device/{deviceGuid}/sale\nScenario: Verify sale transaction with device\nParameters: deviceGuid, amount, currency\n\nTest Case:",
        "Write Python code to test the following API endpoint.\nAPI Endpoint: GET /device/list\nScenario: Verify device listing functionality\nParameters: None\n\nTest Case:",
        "Create a Python unittest for the following API endpoint.\nAPI Endpoint: POST /token/create\nScenario: Verify token creation with card data\nParameters: cardNumber, expirationDate, cvv\n\nTest Case:",
        "Generate Python test code for the following API endpoint.\nAPI Endpoint: POST /transaction/refund\nScenario: Verify refund transaction processing\nParameters: transactionId, amount\n\nTest Case:"
    ]
    
    print("\n" + "="*80)
    print("TESTING PYTHON CODE GENERATION")
    print("="*80)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {prompt}")
        
        # Tokenize input
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate output
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=300,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode output
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after the prompt)
        if prompt in generated_text:
            generated_part = generated_text[len(prompt):].strip()
        else:
            generated_part = generated_text.strip()
        
        print(f"Generated: {generated_part}")
        print("-" * 50)

if __name__ == "__main__":
    test_python_generation() 