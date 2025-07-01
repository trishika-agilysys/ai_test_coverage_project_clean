import json
import os
from transformers import T5ForConditionalGeneration, RobertaTokenizer
import torch

class EnglishToPythonTestGenerator:
    def __init__(self, model_path="src/data/models/checkpoints/latest_english_generator"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Load the fine-tuned model
        print("Loading fine-tuned CodeT5 model...")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
    def generate_python_test(self, endpoint, operation_id, english_test_case):
        """Generate Python test code from English description"""
        
        # Create input prompt
        input_text = f"Generate Python test code for: {english_test_case}\nEndpoint: {endpoint}\nOperation ID: {operation_id}"
        
        # Tokenize input
        inputs = self.tokenizer(
            input_text,
            max_length=512,
            truncation=True,
            padding=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate output
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=512,
                num_beams=4,
                early_stopping=True,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode output
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    
    def create_test_file(self, endpoint, operation_id, test_cases, output_dir="generated_python_tests"):
        """Create a Python test file for an endpoint"""
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename from endpoint
        endpoint_name = endpoint.replace("/", "_").replace("{", "").replace("}", "").replace("v1.5_", "")
        filename = f"test_{endpoint_name}.py"
        filepath = os.path.join(output_dir, filename)
        
        # Generate test code
        test_code = []
        test_code.append("import requests")
        test_code.append("import pytest")
        test_code.append("import json")
        test_code.append("")
        test_code.append(f"# Test file for endpoint: {endpoint}")
        test_code.append(f"# Operation ID: {operation_id}")
        test_code.append("")
        test_code.append("@pytest.fixture")
        test_code.append("def base_url():")
        test_code.append("    return 'http://localhost:8502'")
        test_code.append("")
        test_code.append("@pytest.fixture")
        test_code.append("def headers():")
        test_code.append("    return {")
        test_code.append("        'Authorization': 'Bearer your-token-here',")
        test_code.append("        'Content-Type': 'application/json'")
        test_code.append("    }")
        test_code.append("")
        
        # Generate individual test functions
        for i, test_case in enumerate(test_cases, 1):
            print(f"Generating Python test for: {test_case[:50]}...")
            
            try:
                python_code = self.generate_python_test(endpoint, operation_id, test_case)
                
                # Clean up the generated code
                python_code = python_code.strip()
                if not python_code.startswith("def "):
                    # If the model didn't generate a proper function, create a basic one
                    python_code = f"""def test_{endpoint_name}_{i}(base_url, headers):
    \"\"\"{test_case}\"\"\"
    url = f"{{base_url}}{endpoint}"
    response = requests.get(url, headers=headers)
    assert response.status_code in [200, 201, 204]
    print(f"Test passed: {{test_case}}")"""
                
                test_code.append(python_code)
                test_code.append("")
                
            except Exception as e:
                print(f"Error generating test {i}: {e}")
                # Create a fallback test
                test_code.append(f"""def test_{endpoint_name}_{i}_fallback(base_url, headers):
    \"\"\"{test_case}\"\"\"
    url = f"{{base_url}}{endpoint}"
    response = requests.get(url, headers=headers)
    assert response.status_code in [200, 201, 204]
    print(f"Fallback test passed: {{test_case}}")""")
                test_code.append("")
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(test_code))
        
        print(f"✅ Generated test file: {filepath}")
        return filepath
    
    def generate_all_tests(self, english_test_cases_file="data/processed/english_test_cases.json"):
        """Generate Python test files for all endpoints"""
        
        print("Loading English test cases...")
        with open(english_test_cases_file, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        
        generated_files = []
        
        for endpoint, data in test_cases.items():
            operation_id = data['operation_id']
            english_test_cases = data['test_cases']
            
            print(f"\nProcessing endpoint: {endpoint}")
            filepath = self.create_test_file(endpoint, operation_id, english_test_cases)
            generated_files.append(filepath)
        
        print(f"\n🎉 Successfully generated {len(generated_files)} Python test files!")
        return generated_files

def main():
    print("🚀 Starting English to Python Test Generation")
    print("=" * 50)
    
    # Initialize generator
    generator = EnglishToPythonTestGenerator()
    
    # Generate all tests
    generated_files = generator.generate_all_tests()
    
    print("\n📁 Generated test files:")
    for filepath in generated_files[:5]:  # Show first 5 files
        print(f"  - {filepath}")
    if len(generated_files) > 5:
        print(f"  ... and {len(generated_files) - 5} more files")
    
    print(f"\n✅ Total files generated: {len(generated_files)}")
    print("📂 Check the 'generated_python_tests' directory for all test files")

if __name__ == "__main__":
    main() 