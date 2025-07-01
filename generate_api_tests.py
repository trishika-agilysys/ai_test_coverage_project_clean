# generate_api_tests.py
import json
from ai_model.codet5_generator import CodeT5TestGenerator

def main():
    # Initialize the CodeT5 generator
    generator = CodeT5TestGenerator()
    
    # Load your Swagger specification
    swagger_file = "swagger_fixed.json"  # Update this path to your Swagger file
    swagger_spec = generator.load_swagger(swagger_file)
    
    # Generate test cases
    test_cases = generator.generate_test_cases(swagger_spec, num_test_cases=5)
    
    # Save the generated test cases
    generator.save_test_cases(test_cases, "generated_test_cases.json")
    
    print("Test cases generated successfully!")
    print(f"Generated {len(test_cases)} test cases")
    print("Test cases have been saved to generated_test_cases.json")

if __name__ == "__main__":
    main()