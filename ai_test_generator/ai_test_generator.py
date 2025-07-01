import json
import random
import requests
import os
import sys
import pandas as pd
from typing import Dict, List, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Add parent directory to path to import ai_model
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from ai_model.codet5_generator import CodeT5TestGenerator
except ImportError:
    # Fallback if CodeT5 generator is not available
    CodeT5TestGenerator = None

from config import DEVICE_GUID, TOKEN, TRANSACTION_ID, GATEWAY_ID, INDUSTRY_TYPE, CHECK_ID

class AITestGenerator:
    def __init__(self, swagger_path: str, historical_data_path: Optional[str] = None):
        """
        Initialize the AI Test Generator.
        
        Args:
            swagger_path: Path to the Swagger/OpenAPI specification file
            historical_data_path: Optional path to historical test execution data
        """
        self.swagger_path = swagger_path
        self.historical_data_path = historical_data_path
        self.spec = self._load_swagger()
        self.historical_data = self._load_historical_data() if historical_data_path else None
        self.vectorizer = TfidfVectorizer()
        self.endpoint_vectors = None
        self._prepare_endpoint_vectors()

    def _load_swagger(self) -> Dict:
        """Load and parse the Swagger/OpenAPI specification."""
        with open(self.swagger_path) as f:
            return json.load(f)

    def _load_historical_data(self) -> pd.DataFrame:
        """Load historical test execution data if available."""
        if os.path.exists(self.historical_data_path):
            return pd.read_csv(self.historical_data_path)
        return None

    def _prepare_endpoint_vectors(self):
        """Prepare TF-IDF vectors for endpoint descriptions."""
        if not self.historical_data is None:
            descriptions = []
            for path, path_item in self.spec.get("paths", {}).items():
                for method, details in path_item.items():
                    desc = f"{method} {path} {details.get('summary', '')} {details.get('description', '')}"
                    descriptions.append(desc)
            
            self.endpoint_vectors = self.vectorizer.fit_transform(descriptions)

    def _generate_smart_payload(self, schema: Dict, endpoint: str, method: str) -> Any:
        """
        Generate intelligent test payload based on schema and historical data.
        
        Args:
            schema: JSON schema for the payload
            endpoint: API endpoint path
            method: HTTP method
        """
        if "type" not in schema:
            return ""

        # Use historical data to influence payload generation
        if self.historical_data is not None:
            similar_endpoints = self._find_similar_endpoints(endpoint, method)
            if similar_endpoints:
                # Use values from successful historical requests
                successful_requests = self.historical_data[
                    (self.historical_data['status_code'] < 400) & 
                    (self.historical_data['url'].str.contains(endpoint))
                ]
                if not successful_requests.empty:
                    # Extract and use successful payload patterns
                    pass

        # Base payload generation logic
        if schema["type"] == "string":
            # Generate more realistic string values based on field name
            field_name = schema.get("name", "").lower()
            if "email" in field_name:
                return "test@example.com"
            elif "date" in field_name:
                return "2024-03-11"
            elif "id" in field_name:
                return str(random.randint(1000, 9999))
            return "sample-string"
        elif schema["type"] == "integer":
            return random.randint(1, 100)
        elif schema["type"] == "number":
            return round(random.uniform(1.0, 100.0), 2)
        elif schema["type"] == "boolean":
            return random.choice([True, False])
        elif schema["type"] == "array":
            item_schema = schema.get("items", {})
            return [self._generate_smart_payload(item_schema, endpoint, method)]
        elif schema["type"] == "object":
            props = schema.get("properties", {})
            required = schema.get("required", [])
            return {
                key: self._generate_smart_payload(value, endpoint, method)
                for key, value in props.items()
                if key in required or random.random() < 0.7
            }
        return None

    def _find_similar_endpoints(self, endpoint: str, method: str) -> List[str]:
        """Find similar endpoints based on historical data."""
        if self.endpoint_vectors is None:
            return []
        
        query = f"{method} {endpoint}"
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.endpoint_vectors)
        similar_indices = np.argsort(similarities[0])[-3:][::-1]  # Top 3 similar endpoints
        
        return [list(self.spec["paths"].keys())[i] for i in similar_indices]

    def _generate_edge_cases(self, schema: Dict) -> List[Any]:
        """Generate edge cases for a given schema."""
        edge_cases = []
        
        if schema["type"] == "string":
            edge_cases.extend([
                "",  # Empty string
                " " * 1000,  # Very long string
                "!@#$%^&*()",  # Special characters
                "null",  # String "null"
            ])
        elif schema["type"] == "integer":
            edge_cases.extend([
                0,
                -1,
                999999999,
            ])
        elif schema["type"] == "number":
            edge_cases.extend([
                0.0,
                -1.0,
                999999.999,
            ])
        elif schema["type"] == "array":
            edge_cases.extend([
                [],  # Empty array
                [None],  # Array with null
            ])
        elif schema["type"] == "object":
            edge_cases.extend([
                {},  # Empty object
                {"key": None},  # Object with null value
            ])
            
        return edge_cases

    def generate_test_cases(self, include_edge_cases: bool = True, prioritized: list = None) -> list:
        """
        Generate test cases, optionally only for prioritized (method, url) pairs.
        """
        tests = []
        BASE_URL = "http://localhost:8502"
        prioritized_set = set()
        if prioritized:
            prioritized_set = set((item["method"].upper(), item["url"]) for item in prioritized)

        for path, path_item in self.spec.get("paths", {}).items():
            for method, details in path_item.items():
                # Replace path parameters with real values
                url = path
                for param in details.get("parameters", []):
                    if param.get("in") == "path":
                        name = param["name"]
                        value_map = {
                            "deviceGuid": DEVICE_GUID,
                            "token": TOKEN,
                            "transactionId": TRANSACTION_ID,
                            "checkId": CHECK_ID,
                        }
                        fake_value = value_map.get(name, f"real-{name}")
                        url = url.replace(f"{{{name}}}", fake_value)
                full_url = BASE_URL + url
                if prioritized and (method.upper(), full_url) not in prioritized_set:
                    continue
                # Generate base test case
                test = {
                    "method": method.upper(),
                    "endpoint": path,
                    "payload": {},
                    "description": details.get("summary", ""),
                    "expected_status": 200
                }
                request_body = details.get("requestBody", {})
                content = request_body.get("content", {})
                app_json = content.get("application/json", {})
                schema = app_json.get("schema", {})
                if "$ref" in schema:
                    schema = self._resolve_schema(schema["$ref"])
                if schema:
                    test["payload"] = self._generate_smart_payload(schema, path, method)
                test["url"] = full_url
                if isinstance(test["payload"], dict):
                    if "request" not in test["payload"]:
                        test["payload"]["request"] = {}
                    test["payload"]["request"].setdefault("gatewayId", GATEWAY_ID)
                    test["payload"]["request"].setdefault("industryType", INDUSTRY_TYPE)
                tests.append(test)
                if include_edge_cases and schema:
                    edge_cases = self._generate_edge_cases(schema)
                    for edge_case in edge_cases:
                        edge_test = test.copy()
                        edge_test["payload"] = edge_case
                        edge_test["description"] = f"Edge case: {test['description']}"
                        edge_test["expected_status"] = 400
                        tests.append(edge_test)
        return tests

    def _resolve_schema(self, ref: str) -> Dict:
        """Resolve $ref to actual schema object."""
        ref_path = ref[2:].split("/")
        result = self.spec
        for part in ref_path:
            result = result.get(part, {})
        return result

    def save_test_cases(self, output_path: str, prioritized: list = None):
        """Save generated test cases to a file, optionally only for prioritized endpoints."""
        test_cases = self.generate_test_cases(prioritized=prioritized)
        
        # Try to use CodeT5 for enhanced test generation if available
        if CodeT5TestGenerator is not None:
            try:
                codet5_generator = CodeT5TestGenerator()
                enhanced_tests = codet5_generator.generate_test_cases(self.spec, num_test_cases=3)
                # Only add enhanced tests that are dicts (ignore strings)
                valid_enhanced_tests = []
                for test in enhanced_tests:
                    if isinstance(test, dict):
                        valid_enhanced_tests.append(test)
                    else:
                        print(f"[WARNING] Skipping non-dict CodeT5 test case: {repr(test)[:80]}...")
                test_cases.extend(valid_enhanced_tests)
            except Exception as e:
                print(f"Warning: CodeT5 generation failed: {e}")
        # Filter out any non-dict entries (shouldn't happen, but just in case)
        test_cases = [t for t in test_cases if isinstance(t, dict)]
        with open(output_path, 'w') as f:
            json.dump(test_cases, f, indent=2)
        print(f"Generated {len(test_cases)} test cases and saved to {output_path}")

def main():
    # Initialize the CodeT5 generator
    generator = CodeT5TestGenerator()
    
    # Load your Swagger specification
    with open("swagger.json", "r") as f:
        swagger_spec = json.load(f)
    
    # Generate test cases
    test_cases = generator.generate_test_cases(swagger_spec, num_test_cases=5)
    
    # Save the generated test cases
    generator.save_test_cases(test_cases, "generated_test_cases.json")
    
    print("Test cases generated successfully!")

if __name__ == "__main__":
    main() 