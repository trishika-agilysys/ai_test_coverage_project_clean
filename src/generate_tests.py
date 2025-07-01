# src/generate_tests.py
from models.codet5 import CodeT5TestGenerator
import json
import logging
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_training_data(data_path: str):
    """Load the training data to get endpoint information."""
    with open(data_path, 'r') as f:
        return json.load(f)

def generate_test_cases(model: CodeT5TestGenerator, training_data: list, output_file: str):
    """Generate test cases for each endpoint in the training data."""
    test_cases = []
    
    for example in training_data:
        # Generate test case
        test_case = model.generate_test_case(example['input'])
        
        # Add metadata
        test_case_info = {
            'input': example['input'],
            'generated_test': test_case,
            'expected_test': example['output']
        }
        test_cases.append(test_case_info)
    
    # Save generated test cases
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(test_cases, f, indent=2)
    
    logger.info(f"Generated {len(test_cases)} test cases and saved to {output_file}")

def format_test_case(test_case: dict) -> str:
    # Parse the input to extract the endpoint path and method
    # Example: "GET /v1.5/ondemand/cardcapture/device/{deviceGuid}"
    first_line = test_case['input'].split('\n')[0]
    if ' ' in first_line:
        method, endpoint_path = first_line.split(' ', 1)
        method = method.lower()
    else:
        method = 'get'
        endpoint_path = '/'

    # Build the test function
    return f"""
import requests

def test_endpoint(base_url, headers):
    url = f"{{base_url.rstrip('/')}}/{endpoint_path.lstrip('/')}"
    response = requests.{method}(url, headers=headers)
    assert response.status_code == 200
"""

def main():
    # Create necessary directories
    os.makedirs("data/models/checkpoints", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # First, let's check if we have the model files
    model_path = "src/data/models/checkpoints/latest/checkpoint-8"
    if not os.path.exists(model_path):
        logger.error(f"Model path {model_path} does not exist!")
        logger.info("Please run the training script first to generate the model checkpoints.")
        return
    
    # Load the trained model
    model = CodeT5TestGenerator(
        model_name=model_path,
        max_input_length=512,
        max_output_length=512
    )
    
    # Define a single endpoint input and expected output (from your training data)
    single_example = [{
        'input': 'POST {{payagent-url}}/v1.5/transaction/sale/device/{{deviceGuid}} - [EMV, No Tip, No Sig, $0.01] Validate Successful Sale On Device Response with $0.01',
        'output': 'eval( postman.getGlobalVariable( "payagent-post-request-script" ) );\n\npm.test("Response status code is 200", function () {\n  pm.response.to.have.status(200);\n});\n\npm.test("TransactionReferenceData contains required fields TransactionId, Token and transactionFollowOnData", function () {\n    const responseData = pm.response.json();\n    \n    pm.expect(responseData.transactionReferenceData).to.have.property(\'transactionId\').and.to.be.a(\'string\');\n    pm.expect(responseData.transactionReferenceData).to.have.property(\'token\').and.to.be.a(\'string\');\n    pm.expect(responseData.transactionReferenceData).to.have.property(\'transactionFollowOnData\').and.to.be.a(\'string\');\n});\n\npm.test("AuthorizedAmount, subTotalAmount, tipAmount and totalAmount are non-negative integers", function () {\n    const responseData = pm.response.json();\n\n    pm.expect(responseData.transactionResponseData.authorizedAmount).to.be.a(\'number\').and.to.be.at.least(0);\n    pm.expect(responseData.transactionResponseData.subTotalAmount).to.be.a(\'number\').and.to.be.at.least(0);\n    pm.expect(responseData.transactionResponseData.totalAmount).to.be.a(\'number\').and.to.be.at.least(0);\n});\n\npm.test("TipAmount field should not present in the response", function () {\n    const responseData = pm.response.json();\n    pm.expect(responseData.transactionResponseData).to.not.have.property(\'tipAmount\');\n});\n\npm.test("CardInfo object contains required fields", function () {\n    const responseData = pm.response.json();\n    \n    pm.expect(responseData.cardInfo).to.be.an(\'object\');\n    const requiredFields = ["cardHolderName", "accountNumberMasked", "cardIssuer", "cardType", "entryMode", "expirationYearMonth", "correlationId"];\n    requiredFields.forEach(field => {\n        pm.expect(responseData.cardInfo).to.have.property(field);\n    });\n});\n\n// Test to validate that accountNumberMasked field is masked\npm.test("AccountNumberMasked has middle characters masked", function () {\n    const responseData = pm.response.json();\n    const accountNumberMasked = responseData.cardInfo.accountNumberMasked;\n    if (accountNumberMasked.length > 4) {\n        const middle = accountNumberMasked.substring(6, accountNumberMasked.length - 4);\n        pm.expect(middle).to.match(/^X+$/);\n    }\n});\n\npm.test("ExpirationYearMonth follows the YYYYMM format", function () {\n    const responseData = pm.response.json();\n    const expirationYearMonth = responseData.cardInfo.expirationYearMonth;\n    pm.expect(expirationYearMonth).to.match(/^\\d{6}$/);\n});\n\npm.test("CardIssuer and entryMode should not be \'unknown\' and etnryMode should be \'chip\'", function () {\n    const responseData = pm.response.json();\n    \n    pm.expect(responseData.cardInfo.cardIssuer).to.not.equal(\'unknown\');\n    pm.expect(responseData.cardInfo.entryMode).to.not.equal(\'unknown\');\n    pm.expect(responseData.cardInfo.entryMode).to.equal(\'chip\');\n});\n\npm.test("EmvInfo object contains required fields", function () {\n    const responseData = pm.response.json();\n    \n    pm.expect(responseData.emvInfo).to.be.an(\'object\');\n    const requiredFields = ["isFallback", "mode", "applicationIdentifier", "applicationLabel", "issuerApplicationData", "terminalVerificationResults", "transactionStatusInformation", "authorizationResponseCode"];\n    requiredFields.forEach(field => {\n        pm.expect(responseData.emvInfo).to.have.property(field);\n    });\n});\n\npm.test("GatewayResponseData contains required fields", function () {\n    const responseData = pm.response.json();\n    const gatewayResponseData = responseData.gatewayResponseData;\n    \n    pm.expect(gatewayResponseData).to.be.an(\'object\');\n    \n    const requiredFields = ["decision", "code", "message", "authCode", "referenceId", "referenceCode"];\n    requiredFields.forEach(field => {\n        pm.expect(gatewayResponseData).to.have.property(field);\n    });\n});\n\npm.test("PinVerified is a boolean value", function () {\n    const responseData = pm.response.json();\n    \n    pm.expect(responseData.pinVerified).to.be.a(\'boolean\');\n});'
    }]
    
    # Generate test case for the single endpoint
    output_file = "src/data/generated_test_cases_single.json"
    generate_test_cases(model, single_example, output_file)
    logger.info(f"Generated test case for single endpoint and saved to {output_file}")

    # Print generated and expected outputs for comparison
    print("\n--- Generated Output ---\n")
    print(single_example[0]['input'])
    with open(output_file, 'r') as f:
        result = json.load(f)
        print(result[0]['generated_test'])
    print("\n--- Expected Output ---\n")
    print(single_example[0]['output'])

if __name__ == "__main__":
    main()