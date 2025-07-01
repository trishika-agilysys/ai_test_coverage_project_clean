import json
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCaseGenerator:
    def __init__(self):
        """Initialize the test case generator."""
        self.test_cases = []
        
    def generate_test_case(self, description: str) -> Dict:
        """
        Generate a basic test case from a description.
        
        Args:
            description: The test case description
            
        Returns:
            Dictionary containing the generated test case
        """
        try:
            # Determine HTTP method based on description
            method = self._determine_http_method(description)
            
            # Determine endpoint based on description
            endpoint = self._determine_endpoint(description)
            
            # Generate basic test case structure
            test_case = {
                "method": method,
                "endpoint": endpoint,
                "expected_status": 200,
                "description": description,
                "payload": self._generate_payload(method, endpoint),
                "scenario_type": "happy_path"
            }
            
            logger.info(f"Generated test case for: {description}")
            return test_case
            
        except Exception as e:
            logger.error(f"Error generating test case: {str(e)}")
            return self._get_fallback_test_case(description)
    
    def _determine_http_method(self, description: str) -> str:
        """Determine HTTP method based on description keywords."""
        description = description.lower()
        
        if any(word in description for word in ["create", "post", "add"]):
            return "POST"
        elif any(word in description for word in ["get", "retrieve", "fetch"]):
            return "GET"
        elif any(word in description for word in ["update", "modify", "change"]):
            return "PUT"
        elif any(word in description for word in ["delete", "remove"]):
            return "DELETE"
        else:
            return "POST"  # Default to POST
    
    def _determine_endpoint(self, description: str) -> str:
        """Determine endpoint based on description keywords."""
        description = description.lower()
        
        if "device" in description:
            return "/api/device"
        elif "token" in description:
            return "/api/token"
        elif "health" in description:
            return "/api/health"
        elif "payment" in description:
            return "/api/payment"
        else:
            return "/api/endpoint"
    
    def _generate_payload(self, method: str, endpoint: str) -> Dict:
        """Generate a basic payload based on method and endpoint."""
        if method == "GET":
            return {}
            
        if "device" in endpoint:
            return {
                "deviceId": "DEVICE123",
                "status": "active"
            }
        elif "token" in endpoint:
            return {
                "tokenId": "TOKEN123",
                "cardType": "VISA"
            }
        elif "payment" in endpoint:
            return {
                "amount": "100.00",
                "currency": "USD"
            }
        else:
            return {
                "id": "TEST123",
                "status": "active"
            }
    
    def _get_fallback_test_case(self, description: str) -> Dict:
        """Generate a fallback test case structure."""
        return {
            "method": "POST",
            "endpoint": "/api/endpoint",
            "expected_status": 200,
            "description": description,
            "payload": {
                "id": "TEST123",
                "status": "active"
            },
            "scenario_type": "happy_path"
        }
    
    def process_test_cases(self, descriptions: List[str]) -> List[Dict]:
        """
        Process multiple test case descriptions.
        
        Args:
            descriptions: List of test case descriptions
            
        Returns:
            List of generated test cases
        """
        test_cases = []
        for description in descriptions:
            test_case = self.generate_test_case(description)
            test_cases.append(test_case)
        return test_cases 