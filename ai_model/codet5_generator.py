# ai_model/codet5_generator.py
from transformers import T5ForConditionalGeneration, RobertaTokenizer
import torch
import json
from typing import Dict, List, Any
from swagger_parser import SwaggerParser

class CodeT5TestGenerator:
    def __init__(self, model_name: str = "Salesforce/codet5-base"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
    def _prepare_swagger_prompt(self, swagger_spec: Dict[str, Any]) -> str:
        """Convert Swagger specification into a prompt for CodeT5."""
        prompt = "Generate test cases for the following API endpoints:\n\n"
        
        for path, path_item in swagger_spec.get("paths", {}).items():
            for method, operation in path_item.items():
                if method.lower() in ["get", "post", "put", "delete", "patch"]:
                    prompt += f"Endpoint: {method.upper()} {path}\n"
                    if "parameters" in operation:
                        prompt += "Parameters:\n"
                        for param in operation["parameters"]:
                            prompt += f"- {param['name']} ({param['in']}): {param.get('description', 'No description')}\n"
                    if "responses" in operation:
                        prompt += "Responses:\n"
                        for status, response in operation["responses"].items():
                            prompt += f"- {status}: {response.get('description', 'No description')}\n"
                    prompt += "\n"
        
        return prompt

    def generate_test_cases(self, swagger_spec: Dict[str, Any], num_test_cases: int = 5) -> List[str]:
        """Generate test cases for the given Swagger specification."""
        prompt = self._prepare_swagger_prompt(swagger_spec)
        
        # Tokenize the prompt
        inputs = self.tokenizer.encode(
            prompt,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate test cases
        outputs = self.model.generate(
            inputs,
            max_length=512,
            num_return_sequences=num_test_cases,
            temperature=0.7,
            top_p=0.95,
            do_sample=True
        )
        
        # Decode the generated test cases
        test_cases = []
        for output in outputs:
            test_case = self.tokenizer.decode(output, skip_special_tokens=True)
            test_cases.append(test_case)
            
        return test_cases

    def save_test_cases(self, test_cases: List[str], output_file: str):
        """Save generated test cases to a file."""
        with open(output_file, "w") as f:
            json.dump({"test_cases": test_cases}, f, indent=2)

    def load_swagger(self, swagger_file: str) -> Dict[str, Any]:
        """Load and parse a Swagger specification file."""
        parser = SwaggerParser(swagger_file)
        return parser.specification