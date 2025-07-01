import json
import os
import re
import random
import string

class ComprehensivePythonTestGenerator:
    def __init__(self, base_url="http://localhost:8502"):
        self.base_url = base_url
        
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
            return "GET"
    
    def extract_path(self, endpoint):
        """Extract path from endpoint string"""
        path = endpoint.split(" ", 1)[1] if " " in endpoint else endpoint
        return path
    
    def generate_test_data_for_scenario(self, scenario, endpoint, operation_id):
        """Generate appropriate test data based on scenario type and endpoint"""
        scenario_type = scenario.get('scenario_type', '')
        
        # Base test data
        base_data = {
            "amount": 10.00,
            "currency": "USD",
            "cardData": "encrypted_card_data_here",
            "deviceGuid": "test-device-guid-123",
            "token": "test-token-456",
            "transactionId": "test-transaction-789"
        }
        
        # Scenario-specific modifications
        if scenario_type == 'large_payload':
            # Generate large payload for performance testing
            base_data.update({
                "largeField": "x" * 10000,  # 10KB string
                "arrayField": [{"id": i, "data": f"item_{i}"} for i in range(1000)]
            })
        
        elif scenario_type == 'sql_injection':
            # SQL injection test data
            base_data.update({
                "userInput": "'; DROP TABLE users; --",
                "searchTerm": "1' OR '1'='1",
                "id": "1; INSERT INTO logs VALUES ('hack')"
            })
        
        elif scenario_type == 'xss_test':
            # XSS test data
            base_data.update({
                "userInput": "<script>alert('XSS')</script>",
                "message": "<img src=x onerror=alert('XSS')>",
                "comment": "javascript:alert('XSS')"
            })
        
        elif scenario_type == 'boundary_test':
            # Boundary value testing
            base_data.update({
                "amount": 0.01,  # Minimum amount
                "maxAmount": 999999.99,  # Maximum amount
                "emptyString": "",
                "nullValue": None
            })
        
        elif scenario_type == 'invalid_enum':
            # Invalid enum values
            base_data.update({
                "status": "INVALID_STATUS",
                "type": "UNKNOWN_TYPE",
                "currency": "INVALID_CURRENCY"
            })
        
        elif scenario_type == 'pattern_test':
            # Pattern validation testing
            base_data.update({
                "email": "invalid-email",
                "phone": "123",  # Too short
                "zipCode": "ABCDE"  # Invalid format
            })
        
        # Endpoint-specific modifications
        if "sale" in endpoint.lower() or "transaction" in endpoint.lower():
            base_data.update({
                "transactionType": "sale",
                "merchantId": "test-merchant-123"
            })
        
        elif "card" in endpoint.lower() and "balance" in endpoint.lower():
            base_data.update({
                "cardType": "credit",
                "accountNumber": "4111111111111111"
            })
        
        elif "token" in endpoint.lower():
            base_data.update({
                "tokenType": "card",
                "expirationDate": "12/25"
            })
        
        return base_data
    
    def generate_headers_for_scenario(self, scenario):
        """Generate appropriate headers based on scenario type"""
        base_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        scenario_type = scenario.get('scenario_type', '')
        
        if scenario_type == 'no_auth':
            # No authentication headers
            return base_headers
        
        elif scenario_type == 'invalid_auth':
            # Invalid authentication
            base_headers.update({
                'Authorization': 'Bearer invalid-token-12345',
                'X-API-Key': 'invalid-api-key'
            })
        
        elif scenario_type == 'expired_auth':
            # Expired authentication
            base_headers.update({
                'Authorization': 'Bearer expired-token-67890',
                'X-API-Key': 'expired-api-key'
            })
        
        else:
            # Valid authentication (default)
            base_headers.update({
                'Authorization': 'Bearer your-valid-token-here',
                'X-API-Key': 'your-valid-api-key-here'
            })
        
        return base_headers
    
    def generate_assertions_for_scenario(self, scenario, http_method):
        """Generate appropriate assertions based on scenario type"""
        scenario_type = scenario.get('scenario_type', '')
        
        assertions = []
        
        if scenario_type == 'all_required':
            # Happy path - expect success
            assertions.extend([
                "assert response.status_code in [200, 201, 204]",
                "assert response.headers.get('content-type', '').startswith('application/json')",
                "if response.status_code != 204:",
                "    assert response.json() is not None"
            ])
        
        elif scenario_type == 'missing_required':
            # Missing required parameter - expect error
            assertions.extend([
                "assert response.status_code in [400, 422]",
                "if response.status_code != 204:",
                "    error_data = response.json()",
                "    assert 'error' in error_data or 'message' in error_data"
            ])
        
        elif scenario_type == 'invalid_enum':
            # Invalid enum value - expect error
            assertions.extend([
                "assert response.status_code in [400, 422]",
                "if response.status_code != 204:",
                "    error_data = response.json()",
                "    assert 'validation' in str(error_data).lower() or 'invalid' in str(error_data).lower()"
            ])
        
        elif scenario_type == 'boundary_test':
            # Boundary testing - may succeed or fail
            assertions.extend([
                "assert response.status_code in [200, 201, 204, 400, 422]",
                "if response.status_code in [200, 201]:",
                "    assert response.json() is not None"
            ])
        
        elif scenario_type == 'no_auth':
            # No authentication - expect auth error
            assertions.extend([
                "assert response.status_code in [401, 403]",
                "if response.status_code != 204:",
                "    error_data = response.json()",
                "    assert 'unauthorized' in str(error_data).lower() or 'forbidden' in str(error_data).lower()"
            ])
        
        elif scenario_type == 'invalid_auth':
            # Invalid authentication - expect auth error
            assertions.extend([
                "assert response.status_code in [401, 403]",
                "if response.status_code != 204:",
                "    error_data = response.json()",
                "    assert 'invalid' in str(error_data).lower() or 'unauthorized' in str(error_data).lower()"
            ])
        
        elif scenario_type == 'sql_injection':
            # SQL injection - expect error or sanitized response
            assertions.extend([
                "assert response.status_code in [200, 201, 204, 400, 422, 500]",
                "if response.status_code in [200, 201]:",
                "    # Verify no SQL injection occurred",
                "    response_text = str(response.json())",
                "    assert 'DROP TABLE' not in response_text",
                "    assert 'INSERT INTO' not in response_text"
            ])
        
        elif scenario_type == 'xss_test':
            # XSS testing - expect sanitized response
            assertions.extend([
                "assert response.status_code in [200, 201, 204, 400, 422]",
                "if response.status_code in [200, 201]:",
                "    response_text = str(response.json())",
                "    assert '<script>' not in response_text",
                "    assert 'javascript:' not in response_text"
            ])
        
        elif scenario_type == 'rate_limit':
            # Rate limiting - may succeed or be rate limited
            assertions.extend([
                "assert response.status_code in [200, 201, 204, 429]",
                "if response.status_code == 429:",
                "    assert 'rate limit' in str(response.headers).lower() or 'retry-after' in str(response.headers).lower()"
            ])
        
        elif scenario_type == 'large_payload':
            # Large payload - may succeed or fail
            assertions.extend([
                "assert response.status_code in [200, 201, 204, 400, 413, 500]",
                "if response.status_code == 413:",
                "    assert 'payload' in str(response.json()).lower() or 'too large' in str(response.json()).lower()"
            ])
        
        else:
            # Default assertions
            assertions.extend([
                "assert response.status_code in [200, 201, 204, 400, 401, 404, 422, 500]",
                "if response.status_code in [200, 201]:",
                "    assert response.json() is not None"
            ])
        
        return assertions
    
    def create_comprehensive_test_file(self, endpoint, operation_id, test_scenarios, output_dir="comprehensive_python_tests"):
        """Create a comprehensive Python test file for an endpoint"""
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract HTTP method and path
        http_method = self.extract_http_method(endpoint)
        path = self.extract_path(endpoint)
        
        # Generate filename
        endpoint_name = path.replace("/", "_").replace("{", "").replace("}", "").replace("v1.5_", "")
        filename = f"test_{http_method.lower()}_{endpoint_name}_comprehensive.py"
        filepath = os.path.join(output_dir, filename)
        
        # Generate test code
        test_code = []
        test_code.append("import requests")
        test_code.append("import pytest")
        test_code.append("import json")
        test_code.append("import time")
        test_code.append("import threading")
        test_code.append("")
        test_code.append(f"# Comprehensive test file for endpoint: {endpoint}")
        test_code.append(f"# Operation ID: {operation_id}")
        test_code.append(f"# Total Test Scenarios: {len(test_scenarios)}")
        test_code.append("")
        
        # Add fixtures
        test_code.append("@pytest.fixture")
        test_code.append("def base_url():")
        test_code.append(f"    return '{self.base_url}'")
        test_code.append("")
        
        # Generate individual test functions for each scenario
        for i, scenario in enumerate(test_scenarios, 1):
            scenario_type = scenario.get('scenario_type', 'unknown')
            description = scenario.get('description', 'No description')
            test_case = scenario.get('test_case', 'No test case')
            
            # Generate test data and headers for this scenario
            test_data = self.generate_test_data_for_scenario(scenario, endpoint, operation_id)
            headers = self.generate_headers_for_scenario(scenario)
            assertions = self.generate_assertions_for_scenario(scenario, http_method)
            
            # Create test function name
            test_name = f"test_{http_method.lower()}_{endpoint_name}_{scenario_type}_{i}"
            test_name = re.sub(r'[^a-zA-Z0-9_]', '_', test_name)  # Sanitize name
            
            # Generate test function
            test_function = []
            test_function.append(f"def {test_name}(base_url):")
            test_function.append(f'    """{description}"""')
            test_function.append(f'    """Generated Test Case: {test_case}"""')
            test_function.append(f"    url = f\"{{base_url}}{path}\"")
            test_function.append("")
            
            # Add headers
            test_function.append("    headers = " + json.dumps(headers, indent=8))
            test_function.append("")
            
            # Add test data if needed
            if http_method in ['POST', 'PUT'] and test_data:
                test_function.append("    test_data = " + json.dumps(test_data, indent=8))
                test_function.append("")
            
            # Add HTTP request
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
            
            test_function.append("")
            
            # Add assertions
            for assertion in assertions:
                test_function.append("    " + assertion)
            
            test_function.append("")
            test_function.append(f"    print(f\"✅ Test passed: {scenario_type} - {description}\")")
            test_function.append("    return response")
            test_function.append("")
            
            test_code.extend(test_function)
        
        # Add performance test for concurrent requests
        if any(s.get('scenario_type') == 'concurrent_requests' for s in test_scenarios):
            test_code.append("def test_concurrent_requests(base_url):")
            test_code.append("    \"\"\"Test concurrent request handling\"\"\"")
            test_code.append("    url = f\"{base_url}{path}\"")
            test_code.append("    headers = {'Content-Type': 'application/json'}")
            test_code.append("    test_data = {'test': 'data'}")
            test_code.append("")
            test_code.append("    def make_request():")
            test_code.append("        return requests.post(url, headers=headers, json=test_data)")
            test_code.append("")
            test_code.append("    # Create 10 concurrent requests")
            test_code.append("    threads = []")
            test_code.append("    responses = []")
            test_code.append("")
            test_code.append("    for _ in range(10):")
            test_code.append("        thread = threading.Thread(target=lambda: responses.append(make_request()))")
            test_code.append("        threads.append(thread)")
            test_code.append("        thread.start()")
            test_code.append("")
            test_code.append("    # Wait for all threads to complete")
            test_code.append("    for thread in threads:")
            test_code.append("        thread.join()")
            test_code.append("")
            test_code.append("    # Verify all requests got a response")
            test_code.append("    assert len(responses) == 10")
            test_code.append("    for response in responses:")
            test_code.append("        assert response.status_code in [200, 201, 204, 400, 401, 429, 500]")
            test_code.append("")
            test_code.append("    print(f\"✅ Concurrent requests test passed for {endpoint}\")")
            test_code.append("")
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(test_code))
        
        print(f"Generated comprehensive test file: {filepath}")
        return filepath
    
    def generate_all_comprehensive_tests(self, comprehensive_test_cases_file="data/processed/comprehensive_test_cases.json"):
        """Generate comprehensive Python test files for all endpoints"""
        
        print("Loading comprehensive test cases...")
        with open(comprehensive_test_cases_file, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        
        generated_files = []
        total_test_functions = 0
        
        for endpoint, data in test_cases.items():
            operation_id = data['operation_id']
            test_scenarios = data['test_cases']
            
            print(f"\nProcessing endpoint: {endpoint}")
            print(f"  Scenarios: {len(test_scenarios)}")
            
            filepath = self.create_comprehensive_test_file(endpoint, operation_id, test_scenarios)
            generated_files.append(filepath)
            total_test_functions += len(test_scenarios)
        
        print(f"\n🎉 Comprehensive test generation complete!")
        print(f"📊 Generated {len(generated_files)} test files")
        print(f"🧪 Total test functions: {total_test_functions}")
        print(f"📁 Check the 'comprehensive_python_tests' directory")
        
        return generated_files

def main():
    print("🚀 Starting Comprehensive Python Test Generation")
    print("=" * 70)
    
    # Initialize generator
    generator = ComprehensivePythonTestGenerator()
    
    # Generate all comprehensive tests
    generated_files = generator.generate_all_comprehensive_tests()
    
    print(f"\n📋 Generated test files:")
    for filepath in generated_files[:5]:  # Show first 5 files
        print(f"  - {filepath}")
    if len(generated_files) > 5:
        print(f"  ... and {len(generated_files) - 5} more files")
    
    print(f"\n🎯 Next steps:")
    print(f"  1. Update the base_url in the test files if needed")
    print(f"  2. Update authentication headers with valid tokens")
    print(f"  3. Run tests: cd comprehensive_python_tests && pytest")
    print(f"  4. Review and customize test data as needed")

if __name__ == "__main__":
    main() 