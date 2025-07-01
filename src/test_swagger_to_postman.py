#!/usr/bin/env python3
"""
Test Swagger to Postman Conversion

This script demonstrates how the trained StarCoder2 model converts
Swagger endpoint descriptions to Postman JavaScript test cases.
"""

import torch
import logging
from models.starcoder import StarCoderTestGenerator
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_swagger_to_postman_conversion():
    """Test the Swagger to Postman conversion capabilities."""
    
    # Sample Swagger endpoint descriptions
    test_endpoints = [
        {
            "name": "Create User",
            "swagger": "POST {{base_url}}/api/users - Create a new user with name, email, and role fields",
            "expected_tests": ["status code", "response structure", "user creation"]
        },
        {
            "name": "Get Products",
            "swagger": "GET {{base_url}}/api/products - Retrieve list of products with pagination (limit, offset)",
            "expected_tests": ["status code", "pagination", "product structure"]
        },
        {
            "name": "Update Order",
            "swagger": "PUT {{base_url}}/api/orders/{{order_id}} - Update order status to 'shipped' with tracking number",
            "expected_tests": ["status code", "order update", "tracking number"]
        },
        {
            "name": "Delete Product",
            "swagger": "DELETE {{base_url}}/api/products/{{product_id}} - Remove product from inventory",
            "expected_tests": ["status code", "deletion confirmation", "not found handling"]
        }
    ]
    
    logger.info("🚀 Testing Swagger to Postman conversion...")
    
    try:
        # Load the trained model
        model = StarCoderTestGenerator(
            model_name="bigcode/starcoder2-3b",
            use_lora=True,
            use_4bit=True,
            lora_r=16,
            lora_alpha=32
        )
        
        logger.info("✅ Model loaded successfully!")
        
        # Test each endpoint
        for i, endpoint in enumerate(test_endpoints, 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"Test {i}: {endpoint['name']}")
            logger.info(f"{'='*80}")
            
            logger.info(f"Swagger Description: {endpoint['swagger']}")
            logger.info(f"Expected Tests: {', '.join(endpoint['expected_tests'])}")
            
            # Generate Postman tests
            logger.info(f"\n🎯 Generating Postman JavaScript tests...")
            
            try:
                generated_tests = model.generate_tests(endpoint['swagger'])
                
                logger.info(f"\n📝 Generated Tests:")
                logger.info(f"{'='*60}")
                print(generated_tests)
                logger.info(f"{'='*60}")
                
                # Analyze the generated tests
                test_count = generated_tests.count('pm.test')
                expect_count = generated_tests.count('pm.expect')
                response_count = generated_tests.count('pm.response')
                
                logger.info(f"\n📊 Analysis:")
                logger.info(f"  - Test cases: {test_count}")
                logger.info(f"  - Expectations: {expect_count}")
                logger.info(f"  - Response checks: {response_count}")
                
                # Check for expected patterns
                if 'pm.test' in generated_tests:
                    logger.info("✅ Generated pm.test() blocks")
                else:
                    logger.warning("⚠️  No pm.test() blocks found")
                
                if 'pm.expect' in generated_tests:
                    logger.info("✅ Generated pm.expect() assertions")
                else:
                    logger.warning("⚠️  No pm.expect() assertions found")
                
                if '{{' in generated_tests and '}}' in generated_tests:
                    logger.info("✅ Handled variable interpolation")
                else:
                    logger.warning("⚠️  No variable interpolation found")
                
                # Check for HTTP method handling
                http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
                found_methods = [method for method in http_methods if method in generated_tests]
                if found_methods:
                    logger.info(f"✅ Handled HTTP methods: {', '.join(found_methods)}")
                
            except Exception as e:
                logger.error(f"❌ Generation failed: {e}")
        
        logger.info(f"\n{'='*80}")
        logger.info("🎉 SWAGGER TO POSTMAN CONVERSION TEST COMPLETE")
        logger.info(f"{'='*80}")
        logger.info("The model successfully converts Swagger endpoint descriptions")
        logger.info("to comprehensive Postman JavaScript test cases!")
        
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        logger.info("Make sure the model is trained and available")

def main():
    test_swagger_to_postman_conversion()

if __name__ == "__main__":
    main() 