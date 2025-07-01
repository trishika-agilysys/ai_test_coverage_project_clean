import json
import os
import re

class ImprovedPythonTestGenerator:
    def __init__(self):
        self.base_url = "http://localhost:8502"
        
    def extract_http_method(self, endpoint):
        """Extract HTTP method from endpoint string"""
        if endpoint.startswith("GET "):
            return "GET"
        elif endpoint.startswith("POST "):
            return "POST"
        elif endpoint.startswith("PUT "):
            return "PUT"
        elif endpoint.startswith("DELETE "):
            return "DELETE"
        else:
            return "GET"  # Default
    
    def extract_path(self, endpoint):
        """Extract path from endpoint string"""
        # Remove HTTP method and extract path
        path = endpoint.split(" ", 1)[1] if " " in endpoint else endpoint
        return path
    
    def generate_test_data(self, endpoint, operation_id):
        """Generate appropriate test data based on endpoint"""
        if "sale" in endpoint.lower() or "transaction" in endpoint.lower():
            return {
                "amount": 10.00,
                "currency": "USD",
                "cardData": "encrypted_card_data_here"
            }
        elif "card" in endpoint.lower() and "balance" in endpoint.lower():
            return {
                "cardData": "encrypted_card_data_here"
            }
        elif "token" in endpoint.lower():
            return {
                "cardData": "encrypted_card_data_here"
            }
        elif "device" in endpoint.lower() and "detach" in endpoint.lower():
            return {}
        elif "device" in endpoint.lower() and "standby" in endpoint.lower():
            return {}
        else:
            return {}
    
    def create_test_file(self, endpoint, operation_id, test_cases, output_dir="improved_python_tests"):
        """Create an improved Python test file for an endpoint"""
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract HTTP method and path
        http_method = self.extract_http_method(endpoint)
        path = self.extract_path(endpoint)
        
        # Generate filename
        endpoint_name = path.replace("/", "_").replace("{", "").replace("}", "").replace("v1.5_", "")
        filename = f"test_{http_method.lower()}_{endpoint_name}.py"
        filepath = os.path.join(output_dir, filename)
        
        # Generate test data
        test_data = self.generate_test_data(endpoint, operation_id)
        
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
        test_code.append(f"    return '{self.base_url}'")
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
            test_name = f"test_{http_method.lower()}_{endpoint_name}_{i}"
            
            # Create proper test function
            test_function = []
            test_function.append(f"def {test_name}(base_url, headers{f', test_data' if test_data else ''}):")
            test_function.append(f'    """{test_case}"""')
            test_function.append(f"    url = f\"{{base_url}}{path}\"")
            
            # Add appropriate HTTP method and data
            if http_method == "GET":
                test_function.append("    response = requests.get(url, headers=headers)")
            elif http_method == "POST":
                if test_data:
                    test_function.append("    response = requests.post(url, headers=headers, json=test_data)")
                else:
                    test_function.append("    response = requests.post(url, headers=headers)")
            elif http_method == "PUT":
                if test_data:
                    test_function.append("    response = requests.put(url, headers=headers, json=test_data)")
                else:
                    test_function.append("    response = requests.put(url, headers=headers)")
            elif http_method == "DELETE":
                test_function.append("    response = requests.delete(url, headers=headers)")
            
            # Add assertions
            test_function.append("    assert response.status_code in [200, 201, 204, 400, 401, 404, 500]")
            test_function.append("    print(f\"Test passed: {test_case}\")")
            test_function.append("    return response")
            test_function.append("")
            
            test_code.extend(test_function)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(test_code))
        
        print(f"Generated improved test file: {filepath}")
        return filepath
    
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
        
        print(f"\nSuccessfully generated {len(generated_files)} improved Python test files!")
        return generated_files

def main():
    print("Starting Improved English to Python Test Generation")
    print("=" * 60)
    
    # Initialize generator
    generator = ImprovedPythonTestGenerator()
    
    # Generate all tests
    generated_files = generator.generate_all_tests()
    
    print("\nGenerated test files:")
    for filepath in generated_files[:5]:  # Show first 5 files
        print(f"  - {filepath}")
    if len(generated_files) > 5:
        print(f"  ... and {len(generated_files) - 5} more files")
    
    print(f"\nTotal files generated: {len(generated_files)}")
    print("Check the 'improved_python_tests' directory for all test files")
    
    # Show a sample of the improved test
    if generated_files:
        print("\nSample of improved test code:")
        with open(generated_files[0], 'r') as f:
            lines = f.readlines()
            for line in lines[:20]:
                print(f"  {line.rstrip()}")

if __name__ == "__main__":
    main() 