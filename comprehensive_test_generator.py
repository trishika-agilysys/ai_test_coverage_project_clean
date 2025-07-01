import json
import itertools
from transformers import T5ForConditionalGeneration, RobertaTokenizer
import torch
import argparse
import os

class ComprehensiveTestGenerator:
    def __init__(self, model_path="src/data/models/checkpoints/latest_english_generator"):
        # Optimize for CPU
        torch.set_num_threads(1)
        self.device = torch.device("cpu")
        self.model = T5ForConditionalGeneration.from_pretrained(model_path).to(self.device)
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path)
        self.model.eval()

    def load_swagger(self, swagger_file):
        """Load and parse the Swagger specification."""
        with open(swagger_file, 'r') as f:
            return json.load(f)

    def _analyze_parameters(self, method_info):
        """Deep analysis of parameters to generate comprehensive test scenarios."""
        parameters = method_info.get("parameters", [])
        required_params = []
        optional_params = []
        
        for param in parameters:
            param_info = {
                'name': param['name'],
                'in': param['in'],
                'required': param.get('required', False),
                'type': param.get('schema', {}).get('type', 'string'),
                'format': param.get('schema', {}).get('format', ''),
                'description': param.get('description', ''),
                'enum': param.get('schema', {}).get('enum', []),
                'min': param.get('schema', {}).get('minimum'),
                'max': param.get('schema', {}).get('maximum'),
                'pattern': param.get('schema', {}).get('pattern', ''),
                'default': param.get('schema', {}).get('default')
            }
            
            if param_info['required']:
                required_params.append(param_info)
            else:
                optional_params.append(param_info)
        
        return required_params, optional_params

    def _analyze_request_body(self, method_info):
        """Analyze request body schema for comprehensive testing."""
        request_body = method_info.get("requestBody", {})
        if not request_body:
            return None
        
        content = request_body.get("content", {})
        for content_type, content_info in content.items():
            if "schema" in content_info:
                schema = content_info["schema"]
                return {
                    'content_type': content_type,
                    'schema': schema,
                    'required': request_body.get("required", False),
                    'properties': schema.get("properties", {}),
                    'required_props': schema.get("required", [])
                }
        return None

    def _analyze_responses(self, method_info):
        """Analyze all possible response codes and scenarios."""
        responses = method_info.get("responses", {})
        response_scenarios = []
        
        for code, resp_info in responses.items():
            scenario = {
                'code': code,
                'description': resp_info.get('description', ''),
                'content': resp_info.get('content', {}),
                'headers': resp_info.get('headers', {})
            }
            response_scenarios.append(scenario)
        
        return response_scenarios

    def _generate_parameter_test_scenarios(self, required_params, optional_params):
        """Generate test scenarios based on parameter combinations."""
        scenarios = []
        
        # Test with all required parameters
        if required_params:
            scenarios.append({
                'type': 'all_required',
                'description': 'Test with all required parameters',
                'params': required_params
            })
        
        # Test with missing required parameters (error cases)
        for i, param in enumerate(required_params):
            missing_params = required_params[:i] + required_params[i+1:]
            scenarios.append({
                'type': 'missing_required',
                'description': f'Test with missing required parameter: {param["name"]}',
                'params': missing_params,
                'missing': param
            })
        
        # Test with optional parameters
        for i in range(1, len(optional_params) + 1):
            for combo in itertools.combinations(optional_params, i):
                scenarios.append({
                    'type': 'optional_combination',
                    'description': f'Test with optional parameters: {", ".join([p["name"] for p in combo])}',
                    'params': list(combo)
                })
        
        # Test parameter validation scenarios
        for param in required_params + optional_params:
            if param.get('enum'):
                # Test with invalid enum values
                scenarios.append({
                    'type': 'invalid_enum',
                    'description': f'Test with invalid enum value for parameter: {param["name"]}',
                    'params': [param],
                    'invalid_value': 'INVALID_ENUM_VALUE'
                })
            
            if param.get('min') is not None or param.get('max') is not None:
                # Test boundary values
                scenarios.append({
                    'type': 'boundary_test',
                    'description': f'Test boundary values for parameter: {param["name"]}',
                    'params': [param],
                    'boundary_test': True
                })
            
            if param.get('pattern'):
                # Test pattern validation
                scenarios.append({
                    'type': 'pattern_test',
                    'description': f'Test pattern validation for parameter: {param["name"]}',
                    'params': [param],
                    'pattern_test': True
                })
        
        return scenarios

    def _generate_security_test_scenarios(self, method_info):
        """Generate security-focused test scenarios."""
        security_scenarios = [
            {
                'type': 'no_auth',
                'description': 'Test without authentication headers',
                'auth_test': 'missing'
            },
            {
                'type': 'invalid_auth',
                'description': 'Test with invalid authentication token',
                'auth_test': 'invalid'
            },
            {
                'type': 'expired_auth',
                'description': 'Test with expired authentication token',
                'auth_test': 'expired'
            },
            {
                'type': 'sql_injection',
                'description': 'Test for SQL injection vulnerabilities',
                'security_test': 'sql_injection'
            },
            {
                'type': 'xss_test',
                'description': 'Test for XSS vulnerabilities',
                'security_test': 'xss'
            },
            {
                'type': 'rate_limit',
                'description': 'Test rate limiting behavior',
                'security_test': 'rate_limit'
            }
        ]
        return security_scenarios

    def _generate_performance_test_scenarios(self, method_info):
        """Generate performance and load testing scenarios."""
        performance_scenarios = [
            {
                'type': 'large_payload',
                'description': 'Test with large request payload',
                'performance_test': 'large_payload'
            },
            {
                'type': 'concurrent_requests',
                'description': 'Test concurrent request handling',
                'performance_test': 'concurrent'
            },
            {
                'type': 'timeout_test',
                'description': 'Test timeout behavior',
                'performance_test': 'timeout'
            }
        ]
        return performance_scenarios

    def _format_comprehensive_prompt(self, path, method_info, scenario):
        """Format a comprehensive test scenario into a prompt."""
        operation_id = method_info.get("operationId", "N/A")
        summary = method_info.get("summary", "No summary available.")
        
        # Build scenario-specific description
        scenario_desc = scenario['description']
        if scenario.get('params'):
            param_names = [p['name'] for p in scenario['params']]
            scenario_desc += f" (Parameters: {', '.join(param_names)})"
        
        prompt = (
            f"Generate a detailed test case for the following API endpoint and scenario:\n\n"
            f"API Endpoint: {method_info.get('method', 'N/A').upper()} {path}\n"
            f"Operation: {operation_id}\n"
            f"Summary: {summary}\n"
            f"Test Scenario: {scenario_desc}\n"
            f"Scenario Type: {scenario['type']}\n\n"
            f"Generate a comprehensive test case that covers this specific scenario. "
            f"Include specific test data, expected behavior, and validation criteria.\n\n"
            f"Test Case:"
        )
        return prompt

    def generate_comprehensive_test_cases(self, swagger_file, output_file="data/processed/comprehensive_test_cases.json"):
        """Generate comprehensive test cases for all endpoints."""
        swagger_spec = self.load_swagger(swagger_file)
        all_test_cases = {}
        
        total_scenarios = 0
        
        for path, methods in swagger_spec.get('paths', {}).items():
            for method, method_info in methods.items():
                if method.lower() in ['get', 'post', 'put', 'delete']:
                    print(f"\nAnalyzing {method.upper()} {path} for comprehensive test scenarios...")
                    
                    # Analyze endpoint components
                    required_params, optional_params = self._analyze_parameters(method_info)
                    request_body = self._analyze_request_body(method_info)
                    responses = self._analyze_responses(method_info)
                    
                    # Generate different types of test scenarios
                    parameter_scenarios = self._generate_parameter_test_scenarios(required_params, optional_params)
                    security_scenarios = self._generate_security_test_scenarios(method_info)
                    performance_scenarios = self._generate_performance_test_scenarios(method_info)
                    
                    # Combine all scenarios
                    all_scenarios = parameter_scenarios + security_scenarios + performance_scenarios
                    
                    endpoint_test_cases = []
                    
                    for scenario in all_scenarios:
                        print(f"  Generating test case for scenario: {scenario['type']}")
                        
                        prompt = self._format_comprehensive_prompt(path, method_info, scenario)
                        
                        input_ids = self.tokenizer(prompt, return_tensors='pt').input_ids.to(self.device)
                        
                        generated_ids = self.model.generate(
                            input_ids,
                            max_length=200,
                            num_beams=5,
                            repetition_penalty=2.5,
                            length_penalty=1.0,
                            early_stopping=True,
                            num_return_sequences=1,
                            no_repeat_ngram_size=2
                        )
                        
                        test_case = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
                        
                        endpoint_test_cases.append({
                            'scenario_type': scenario['type'],
                            'description': scenario['description'],
                            'test_case': test_case,
                            'parameters': scenario.get('params', []),
                            'security_test': scenario.get('security_test'),
                            'performance_test': scenario.get('performance_test')
                        })
                        
                        total_scenarios += 1
                    
                    all_test_cases[f"{method.upper()} {path}"] = {
                        "operation_id": method_info.get("operationId", "N/A"),
                        "summary": method_info.get("summary", "No summary available."),
                        "required_parameters": len(required_params),
                        "optional_parameters": len(optional_params),
                        "has_request_body": request_body is not None,
                        "response_codes": len(responses),
                        "total_test_scenarios": len(endpoint_test_cases),
                        "test_cases": endpoint_test_cases
                    }
        
        # Save comprehensive test cases
        with open(output_file, 'w') as f:
            json.dump(all_test_cases, f, indent=2)
        
        print(f"\n[SUCCESS] Comprehensive test generation complete!")
        print(f"[INFO] Generated {total_scenarios} test scenarios across {len(all_test_cases)} endpoints")
        print(f"[SAVE] Saved to: {output_file}")
        
        # Print summary statistics
        total_endpoints = len(all_test_cases)
        avg_scenarios_per_endpoint = total_scenarios / total_endpoints if total_endpoints > 0 else 0
        
        print(f"\n[STATS] Summary Statistics:")
        print(f"   • Total Endpoints: {total_endpoints}")
        print(f"   • Total Test Scenarios: {total_scenarios}")
        print(f"   • Average Scenarios per Endpoint: {avg_scenarios_per_endpoint:.1f}")
        
        return all_test_cases

def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive test cases from Swagger specification')
    parser.add_argument('--swagger', default='data/raw/swagger_fixed.json',
                      help='Path to the Swagger specification file')
    parser.add_argument('--output', default='data/processed/comprehensive_test_cases.json',
                      help='Path to save the comprehensive test cases')
    args = parser.parse_args()

    print("[START] Initializing Comprehensive Test Generator...")
    generator = ComprehensiveTestGenerator()
    
    print(f"[LOAD] Loading Swagger specification from {args.swagger}")
    
    print(f"[GENERATE] Generating comprehensive test scenarios...")
    test_cases = generator.generate_comprehensive_test_cases(args.swagger, args.output)
    
    # Show sample of generated test cases
    print(f"\n[SAMPLE] Sample of generated test scenarios:")
    for endpoint, data in list(test_cases.items())[:2]:
        print(f"\n[ENDPOINT] Endpoint: {endpoint}")
        print(f"   [OP] Operation: {data['operation_id']}")
        print(f"   [COUNT] Scenarios: {data['total_test_scenarios']}")
        print(f"   [TESTS] Sample Test Cases:")
        for i, test_case in enumerate(data['test_cases'][:3], 1):
            print(f"     {i}. [{test_case['scenario_type']}] {test_case['description']}")

if __name__ == "__main__":
    main() 