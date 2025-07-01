import json
import os
import re
from transformers import T5ForConditionalGeneration, RobertaTokenizer
import torch

class ImprovedEnglishToPythonTestGenerator:
    def __init__(self, model_path="src/data/models/checkpoints/latest_english_generator"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Load the fine-tuned model
        print("Loading fine-tuned CodeT5 model...")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
    
    def extract_http_method_and_path(self, endpoint):
        """Extract HTTP method and path from endpoint string"""
        parts = endpoint.split(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "GET", endpoint
    
    def generate_test_data_for_endpoint(self, endpoint, operation_id):
        """Generate appropriate test data based on endpoint type"""
        endpoint_lower = endpoint.lower()
        
        if "sale" in endpoint_lower or "transaction" in endpoint_lower:
            return {
                "amount": 10.00,
                "currency": "USD",
                "cardData": "encrypted_card_data_here",
                "deviceGuid": "f7da845e-b9cf-4e24-b3f9-d93e00000000",
                "token": "4761730A0012UZDZEKC5IR000011",
                "transactionId": "01Z6MVJMBD97U6HSQ3Q48F347ANN010V"
            }
        elif "card" in endpoint_lower and "balance" in endpoint_lower:
            return {
                "cardData": "encrypted_card_data_here",
                "deviceGuid": "f7da845e-b9cf-4e24-b3f9-d93e00000000",
                "token": "4761730A0012UZDZEKC5IR000011"
            }
        elif "token" in endpoint_lower:
            return {
                "cardData": "encrypted_card_data_here",
                "deviceGuid": "f7da845e-b9cf-4e24-b3f9-d93e00000000"
            }
        elif "device" in endpoint_lower and ("detach" in endpoint_lower or "standby" in endpoint_lower):
            return {
                "deviceGuid": "f7da845e-b9cf-4e24-b3f9-d93e00000000"
            }
        else:
            return {}
    
    def create_improved_prompt(self, endpoint, operation_id, english_test_case):
        """Create a better prompt for Python code generation"""
        http_method, path = self.extract_http_method_and_path(endpoint)
        test_data = self.generate_test_data_for_endpoint(endpoint, operation_id)
        
        # Create a structured prompt with examples
        prompt = f"""Generate Python test code for the following API endpoint.

Endpoint: {http_method} {path}
Operation ID: {operation_id}
Test Case: {english_test_case}

Requirements:
1. Create a proper pytest function
2. Use the correct HTTP method ({http_method})
3. Include proper error handling
4. Add meaningful assertions based on the test case
5. Use the test data provided below

Test Data: {json.dumps(test_data, indent=2)}

Example structure:
def test_function_name(base_url, headers, test_data):
    \"\"\"Test description\"\"\"
    url = f"{{base_url}}{path}"
    response = requests.{http_method.lower()}(url, headers=headers, json=test_data)
    
    # Add assertions based on test case
    if "success" in "{english_test_case.lower()}":
        assert response.status_code in [200, 201, 204]
    elif "error" in "{english_test_case.lower()}" or "fail" in "{english_test_case.lower()}":
        assert response.status_code in [400, 401, 404, 500]
    else:
        assert response.status_code in [200, 201, 204, 400, 401, 404, 500]
    
    print(f"Test result: {{response.status_code}}")

Generate the Python test code:"""
        
        return prompt
    
    def generate_python_test(self, endpoint, operation_id, english_test_case):
        """Generate Python test code from English description with improved prompting"""
        
        # Create improved prompt
        prompt = self.create_improved_prompt(endpoint, operation_id, english_test_case)
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            max_length=1024,  # Increased for better context
            truncation=True,
            padding=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate output with better parameters
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=512,
                num_beams=5,  # Increased for better quality
                early_stopping=True,
                temperature=0.8,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode output
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after the prompt)
        if prompt in generated_text:
            generated_part = generated_text[len(prompt):].strip()
        else:
            generated_part = generated_text.strip()
        
        return generated_part
    
    def create_fallback_test(self, endpoint, operation_id, english_test_case, test_index):
        """Create a fallback test when AI generation fails"""
        http_method, path = self.extract_http_method_and_path(endpoint)
        test_data = self.generate_test_data_for_endpoint(endpoint, operation_id)
        
        # Create a clean endpoint name for function
        endpoint_name = path.replace("/", "_").replace("{", "").replace("}", "").replace("v1.5_", "")
        function_name = f"test_{endpoint_name}_{test_index}"
        
        # Determine expected status codes based on test case
        test_case_lower = english_test_case.lower()
        if any(word in test_case_lower for word in ["success", "working", "correct"]):
            expected_codes = "[200, 201, 204]"
        elif any(word in test_case_lower for word in ["error", "fail", "invalid", "unauthorized"]):
            expected_codes = "[400, 401, 404, 500]"
        else:
            expected_codes = "[200, 201, 204, 400, 401, 404, 500]"
        
        # Generate appropriate HTTP call
        if http_method == "GET":
            http_call = f'response = requests.get(url, headers=headers)'
        elif http_method == "POST":
            if test_data:
                http_call = f'response = requests.post(url, headers=headers, json=test_data)'
            else:
                http_call = f'response = requests.post(url, headers=headers)'
        elif http_method == "PUT":
            if test_data:
                http_call = f'response = requests.put(url, headers=headers, json=test_data)'
            else:
                http_call = f'response = requests.put(url, headers=headers)'
        elif http_method == "DELETE":
            http_call = f'response = requests.delete(url, headers=headers)'
        else:
            http_call = f'response = requests.get(url, headers=headers)'
        
        fallback_code = f"""def {function_name}(base_url, headers{f', test_data' if test_data else ''}):
    \"\"\"{english_test_case}\"\"\"
    url = f"{{base_url}}{path}"
    {http_call}
    
    # Check response status
    assert response.status_code in {expected_codes}
    
    # Log the result
    if response.status_code in [200, 201, 204]:
        print(f"✅ Test passed: {{response.status_code}}")
    else:
        print(f"❌ Test failed: {{response.status_code}}")
        if response.content:
            print(f"Response: {{response.text[:200]}}...")
    
    return response"""
        
        return fallback_code
    
    def create_test_file(self, endpoint, operation_id, test_cases, output_dir="improved_generated_python_tests"):
        """Create an improved Python test file for an endpoint"""
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename from endpoint
        http_method, path = self.extract_http_method_and_path(endpoint)
        endpoint_name = path.replace("/", "_").replace("{", "").replace("}", "").replace("v1.5_", "")
        filename = f"test_{http_method.lower()}_{endpoint_name}.py"
        filepath = os.path.join(output_dir, filename)
        
        # Generate test data
        test_data = self.generate_test_data_for_endpoint(endpoint, operation_id)
        
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
        
        if test_data:
            test_code.append("@pytest.fixture")
            test_code.append("def test_data():")
            test_code.append("    return " + json.dumps(test_data, indent=4))
            test_code.append("")
        
        # Generate individual test functions
        for i, test_case in enumerate(test_cases, 1):
            print(f"Generating Python test {i} for: {test_case[:50]}...")
            
            try:
                python_code = self.generate_python_test(endpoint, operation_id, test_case)
                
                # Clean up the generated code
                python_code = python_code.strip()
                
                # Validate the generated code
                if self.is_valid_python_function(python_code):
                    test_code.append(python_code)
                    test_code.append("")
                else:
                    # Use fallback if generated code is invalid
                    print(f"  ⚠️  Generated code invalid, using fallback for test {i}")
                    fallback_code = self.create_fallback_test(endpoint, operation_id, test_case, i)
                    test_code.append(fallback_code)
                    test_code.append("")
                
            except Exception as e:
                print(f"  ❌ Error generating test {i}: {e}")
                # Create a fallback test
                fallback_code = self.create_fallback_test(endpoint, operation_id, test_case, i)
                test_code.append(fallback_code)
                test_code.append("")
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(test_code))
        
        print(f"✅ Generated improved test file: {filepath}")
        return filepath
    
    def is_valid_python_function(self, code):
        """Basic validation to check if generated code looks like a valid Python function"""
        # Check if it starts with 'def'
        if not code.strip().startswith('def '):
            return False
        
        # Check if it has proper indentation
        lines = code.split('\n')
        if len(lines) < 3:
            return False
        
        # Check if it has proper structure
        has_def = any('def ' in line for line in lines)
        has_colon = any(':' in line for line in lines)
        
        return has_def and has_colon
    
    def generate_all_tests(self, english_test_cases_file="data/processed/english_test_cases.json"):
        """Generate improved Python test files for all endpoints"""
        
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
        
        print(f"\n🎉 Successfully generated {len(generated_files)} improved Python test files!")
        return generated_files

def main():
    print("🚀 Starting Improved English to Python Test Generation")
    print("=" * 60)
    
    # Initialize generator
    generator = ImprovedEnglishToPythonTestGenerator()
    
    # Generate all tests
    generated_files = generator.generate_all_tests()
    
    print("\n📁 Generated test files:")
    for filepath in generated_files[:5]:  # Show first 5 files
        print(f"  - {filepath}")
    if len(generated_files) > 5:
        print(f"  ... and {len(generated_files) - 5} more files")
    
    print(f"\n✅ Total files generated: {len(generated_files)}")
    print("📂 Check the 'improved_generated_python_tests' directory for all test files")

if __name__ == "__main__":
    main() 